# Methodology

How the list in `eu_healthcare_robotics_smes_master.csv` was built, so anyone opening this folder later can verify or extend the work.

**Data collection date:** 2026-04-23.
**Collector:** Claude Opus 4.7, run interactively. Every row in the master CSV carries a `source_url` pointing to the page where the company was found.

---

## 1. Scope and inclusion rules

**Geography.** EU27 + UK + Switzerland + Norway + Iceland + Liechtenstein. Non-European companies were excluded even when they had EU offices (e.g. Intuitive, Vicarious, Procept, Neocis, EndoQuest, Motorika, Check-Cap, Kinova).

**Domain.** Healthcare robotics with a physical / hardware robotic component: surgical robotics (laparoscopy, spine, orthopedic, urology, ENT, ophthalmology, microsurgery, neurosurgery), rehab/exoskeleton (gait, upper-limb, hand, ICU mobilization, back support), prosthetics/bionics, endovascular/TAVI/thrombectomy, microrobotics, capsule endoscopy, hospital disinfection, pharmacy automation, clinical lab automation, assistive/elderly-care, radiotherapy positioning, social/service robots in hospital settings.

**Excluded.** Pure-software AI/ML health products with no robotic actuation (Kheiron, Proximie tele-mentoring, Brainomix, Kepler Vision, Avatar Medical VR, dentalrobot.ai). Non-health robotics (agri, inspection/maintenance, defense). Manual/passive devices flagged "robotic" by marketing (Nua Surgical retractor, Hemosquid vacuum, CastPrint 3D-printed cast).

**SME filter.** EU definition = <250 employees AND (≤€50M turnover OR ≤€43M balance sheet). This could not be verified per-company without Orbis/registry access, so the `sme_likely` column is a conservative public-signal heuristic:
- `Yes` — no visible scale-up signals.
- `No` — unicorn, IPO, acquired by a megacorp, or headcount >~250 per public sources.
- `unknown` — candidate looks SME-sized but can't confirm.

The user's end-goal is a TEF-Health outreach list. TEF-Health subsidies cap at €300k per SME over 3 fiscal years under de-minimis state aid. Companies flagged `sme_likely=No` are kept in the list for completeness but flagged so they can be filtered out of a formal SME-only outreach.

---

## 2. Pipeline

```
Seed CSV (26)                                    ┐
                                                 │
4 parallel research agents (general-purpose)     │
  ├── Agent 1: EU-level programs                 │
  ├── Agent 2: Robotics clusters                 │       merge.py            apply_enrichment.py
  ├── Agent 3: National health incubators        │ ─►   (dedup +    ─►     (overlay role-level
  └── Agent 4: Public lists / directories        │       normalize)          emails onto master)
                                                 │
Each writes own shard CSV to shards/             ┘

Result: eu_healthcare_robotics_smes_master.csv (130 unique companies)
```

### 2.1 Agent directives (common to all four)

Each agent was given the same no-compromise rules in its prompt, encoded verbatim:
1. Every company must carry a `source_url` to the incubator/program/list page where it was found. No source ⇒ don't include.
2. Blanks over guesses. Never invent URLs, emails, or countries.
3. European only (list of allowed countries given).
4. Healthcare-robotics hardware only (explicit inclusion and exclusion lists).
5. `sme_likely=unknown` when can't verify; don't assume.
6. Role-level emails only (info@, contact@, hello@, sales@, etc.). Never named-person emails.
7. Each agent was given the seed list (26 companies) and told not to re-add them.

Output format was fixed: `company,country,sub_domain,website,email,email_type,sme_likely,source_url,notes,confidence`. ISO alpha-2 country codes. Quote commas with double-quotes.

### 2.2 Agent-by-agent source pools

The four agents were given distinct, non-overlapping source pools to avoid duplicated work.

| Agent | Source pool | Shard | Rows |
|---|---|---|---|
| 1 | EU-level programs: TEF-Health, EIT Health (Catapult/Headstart/Bridgehead/InnoStars), EIC Accelerator, CORDIS, EIT Jumpstarter, EDIH, EIT Digital, EUREKA Eurostars, DIH² / DIH-World, RIMA network | `shards/agent1_eu_programs.csv` | 33 |
| 2 | Robotics clusters: RobotUnion (H2020), euRobotics AISBL, Odense Robotics (DK), Medicen Paris Region (FR), SPECTARIS (DE), VDMA Robotics, I-RIM (IT), CATROBOTICS (ES), Polish Robotics Cluster, Czech Robotics Cluster, Robotdalen (SE), Norwegian Catapult, Healthtech Nordic, EARTO spin-offs, AIT/Fraunhofer IPA spin-offs | `shards/agent2_robotics_clusters.csv` | 37 |
| 3 | National health incubators (~35 named): Kickstart Innovation, MassChallenge Switzerland, Venturelab/Venture Kick, Fongit, BaseLaunch (CH); BII, Copenhagen Health Tech Cluster, Norway Health Tech (Nordics); Flying Health, UnternehmerTUM, XPRENEURS, Fraunhofer (DE); Bpifrance Deeptech, PariSanté Campus, Eurasanté, Station F (FR); Barcelona Health Hub, Biocat, Lanzadera, Startup Italia (ES/IT); Imec.istart, HighTechXL, YES!Delft (Benelux); Digital Health London, SETsquared, NHS CEP, NDRC (UK/IE); Startup Wise Guys, xPORT (CEE) | `shards/agent3_national_incubators.csv` | 33 |
| 4 | Public lists & directories: Dealroom public lists, Tracxn Europe Healthcare Robotics, Sifted, EU-Startups, The Robot Report, Exoskeleton Report directory, MedicalStartups.org, StartUs Insights, MedTech Dive, Surgical Robotics Technology, Crunchbase hubs, Wellfound, F6S, MedTech Pulse, Roots Analysis, Inven.ai, Foundernest, Orthofeed/ODT Magazine; plus sub-domain deep-dives (dental, hair, capsule, microsurgery, ophthalmology, ENT, stroke rehab) | `shards/agent4_public_lists.csv` | 41 |

Gross candidates before dedup: 33 + 37 + 33 + 41 = **144** new companies.

### 2.3 Known sandbox limitation that shaped agent output

All four research agents reported that `WebFetch` and direct shell `curl`/`Bash` were blocked in their sub-agent sandbox. They relied on `WebSearch` (Google search result snippets) rather than directly scraping the incubator/cluster member directories. This means:

- Candidates surfaced in a search snippet got a `source_url`, but the agent did not load the page itself.
- Gated member directories (Medicen 500+, SPECTARIS ~130 medtech, Odense Robotics 300+, euRobotics 250+) could not be enumerated end-to-end. The agents captured only the members that public news/snippets named.
- Company contact pages could not be fetched by agents, which is why the email column was almost entirely blank after the agent pass and required a separate enrichment step (§2.5).

This is the single biggest methodological caveat in the collection. It means the list is **skewed towards companies that have press coverage** (funding announcements, award news, curated "top N" articles) and systematically under-represents quieter SMEs that exist in cluster directories but haven't been reviewed in English-language media.

### 2.4 Merge and dedup (`merge.py`)

Runs over seed + 4 shards = 5 CSVs, total 170 rows in.

- Normalizes country codes to ISO alpha-2.
- Normalizes company names for duplicate detection: lowercases, strips common legal suffixes (gmbh, ag, sa, sas, srl, spa, ltd, plc, bv, nv, ab, aps, oy, uab), strips trailing descriptors iteratively (technologies, systems, group, medical, robotics, bionics, healthcare, devices, medtech, labs, company, solutions). Parenthetical text removed. Punctuation collapsed.
- For each dedup group, keeps the highest-`row_quality_score` row where score = confidence tier + has-email + generic-email-type + has-website + sme-likely decisive + has-source + notes length.
- Merges complementary fields: fills blank email/website/sub_domain/notes/source_url from lower-ranked rows. Prefers `generic` over other email_types. Prefers decisive SME flag over `unknown`.
- Tags cross-sourced rows with `[cross-sourced x<N>]` in the notes so you can see when a company appeared in multiple lists (signal of credibility).

Result: **130 unique companies.** 40 duplicates merged. One missed dedup ("Japet Medical" vs "Japet Medical Devices") caught on review and fixed by extending the trailing-descriptor regex.

### 2.5 Email enrichment

The original plan was to launch two parallel agents (A and B) to each take ~40 companies and scrape `/contact`, `/about`, footer, etc. for role-level emails.

**What actually happened:**
- **Agent A** (batch of 40, AT–FR alphabetical) — sandbox denied WebFetch on all 10 initial parallel fetches. Agent aborted without writing output.
- **Agent B** (batch of 41, FR–SE alphabetical) — same WebFetch denial; agent wrote three scratch Python scripts (`enrich_emails.py`, `enrich_retry.py`, `enrich_retry2.py`) attempting to work around the sandbox via `urllib.request`, but produced no CSV output. Scripts were removed from `shards/` during cleanup.

**Fallback:** I did the enrichment myself from the main conversation, which has `WebFetch` permission. Ran ~90 `WebFetch` calls in parallel batches of 15, covering all 81 companies that had a website but no email. Each fetch prompted for role-level addresses verbatim only, never synthesized. Retried failures on homepages / alternate paths (`/contact-us`, `/kontakt`, `/contacto`).

**Outcome:**
- **48 new verified role-level emails** added on top of the seed's 26 (total 74 verified).
- 21 confirmed `contact_form_only` (site has a form, no email).
- 14 `unreachable` (TLS expired, DNS refused, 403/404/503 on repeated attempts). Listed with the error type in the `notes` column so they can be retried manually.
- 21 rows remain without email — these are deliberate skips: 18 are `sme_likely=No` scale-ups we exempted from enrichment, plus a handful of Haventure/YES!Delft portfolio entries with no public website yet.

Results written to `shards/enrich_manual.csv` and applied to master via `apply_enrichment.py` (which preserves any email already in the master and appends an `enrich:` note for provenance).

---

## 3. Gaps — where this list is incomplete, and why

### 3.1 Gaps acknowledged by the research agents themselves

**Agent 1 (EU programs):**
- Could not fetch `tefhealth.eu/news-progress`, `tefhealth.eu/call`, or `eithealth.eu/our-network/our-supported-start-ups/` directly (sandbox). Findings derived from WebSearch snippets.
- **TEF-Health does not publicly publish its Call 1 / Call 2 awardees** — zero direct TEF-Health awardees in the list.
- Still worth exploring manually: CORDIS project-level SME participants in Horizon Europe Cluster 1 (Health); EIC Dashboard / eCORDA beneficiary list (authenticated); EIT Health Flagships 2024-25 consortia; EDIH catalogue (TechMed Innovation Hub NL, smartHEALTH EDIH, InnDIH Valencia); Eurostars beneficiary database; Horizon Europe robotics-health project consortia (SoftEnable, TAILOR, DIH-HERO successor at U. Twente).

**Agent 2 (robotics clusters):**
- Could not scrape full member lists for: Odense Robotics (300+ members), euRobotics AISBL (250+ members), SPECTARIS (~130 medtech members), Medicen Paris Region (500+ members), Polish Robotics Cluster (WR Tech), Catalonia CATROBOTICS, Czech Robotics Cluster, Norwegian Catapult healthcare slice, EARTO spin-off directory.
- Likely adds (estimate): 10–20 more from euRobotics healthcare/lab/rehab topic groups; 10+ French from Medicen full directory; 5–10 Italian from I-RIM conference attendees; 6–10 Danish from Odense Robotics MedTech Robot Pathway cohort.

**Agent 3 (national incubators):**
- Portfolio pages not directly fetchable (sandbox): kickstart-innovation.com, bii.dk, flying.health, imec-istart.com, barcelonahealthhub.com, baselaunch.ch, parisantecampus.fr, biocat.cat/craash-barcelona, digitalhealth.london/cohort, norwayhealthtech.com/members, stationf.co.
- Incubators that yielded **zero qualifying companies** (noted because absence matters): BioInnovation Institute (therapeutics-weighted, not device), Flying Health (digital-only), Digital Health London Accelerator (app/software skew), Startup Wise Guys (candidates didn't pass robotics-hardware test), Kickstart Innovation / DayOne CH (digital/diagnostic software), most German Fraunhofer "spin-offs" found via search are still in-house projects (DeKonBot is Fraunhofer-internal).
- Worth deeper manual scraping: Medicalps Grenoble beyond Haventure seven; Paris Santé Campus resident list; Catalonia.com/Biocat BioRegion directory; Norway Health Tech members beyond Respinor; SETsquared and NHS Clinical Entrepreneur Programme.

**Agent 4 (public lists):**
- Sub-domains where **EU SME coverage is genuinely thin**, not an oversight — the market is small:
  - **Dental surgery robotics**: no confirmed EU-headquartered SME (Neocis, Perceptive are US).
  - **Hair transplant robotics**: ARTAS (Venus Concept / Restoration Robotics) is US; no EU competitor identified.
  - **Capsule endoscopy robotics**: only BioCam (Poland) on the EU side; market dominated by US (Medtronic PillCam, CapsoVision) and Asia.
  - **Radiotherapy/radiosurgery positioning robotics**: dominated by Accuray (US), Elekta (SE, too large), Brainlab (DE, too large). Leo Cancer Care (UK) mentioned but not verified as robotic.
  - **Robotic ophthalmology**: only Preceyes, now part of Zeiss.
  - **Robotic hearing/ENT**: Medineering absorbed into Brainlab (2019).
  - **Dedicated stroke rehab robots**: most candidates are general rehab, not stroke-specific SMEs.

### 3.2 Companies intentionally rejected (per agents' own reports)

Documented here so future extensions don't re-add them:

**Non-robotic / misclassified as robotics:**
Mecuris (software/3D-print platform), Nimble Diagnostics (microwave stent diagnostic), Adapttech (scanner/sensor — acquired by US Amparo), Pixee Medical (AR glasses), Brainomix (pure-software AI imaging), Proximie (AR tele-mentoring software), MindMaze (VR/BCI software), Avatar Medical (VR), Sensible Healthcare (biosensor patch), CastPrint (3D-printed passive cast), Nua Surgical (manual retractor), Hemosquid (passive vacuum), Scanvio / EarlySight (imaging software), Kheiron, Kepler Vision, dentalrobot.ai (software).

**Research group, not company:**
Project MARCH (student team).

**Already acquired / no longer independent (some kept in list with `sme_likely=No` for completeness; others dropped):**
KB Medical (→ Globus), Imactis (→ GE HealthCare), Aeon Scientific (→ Stereotaxis), Medineering (→ Brainlab), Orthotaxy (→ DePuy Synthes), Caranx Medical (→ Carvolix/Affluent Medical Dec 2025 — kept, flagged), Artedrone (→ Carvolix — kept, flagged), Preceyes (→ Zeiss — kept, flagged), Gloreha/Idrogenet (→ BTL — kept, flagged), Endocontrol (→ Canady Life Sciences US — kept, flagged), Exopulse/Inerventions (→ Ottobock — kept, flagged).

**Large-cap / not SME:**
BD Rowa (BD-owned), Stryker Mako, Zimmer ROSA, Smith+Nephew CORI, Medtronic Hugo, Intuitive (US), Asensus (US), Vicarious (US), Procept (US), Titan Medical (US), Medicaroid (JP), IntroMedic (KR), Fourier Intelligence (CN), Check-Cap (IL), Motorika (IL), Kinova (CA), Human In Motion (CA), Spineart (>370 staff, kept and flagged), Mauna Kea Technologies (Euronext-listed, kept and flagged), Renishaw Neurosurgery (large UK plc, kept and flagged), Corin Group (PE-backed, likely >250, kept and flagged), Mentice (Nasdaq First North, kept and flagged), Bioservo (Nasdaq First North, kept and flagged), MetraLabs (kept, flagged), Hocoma (~160 staff, kept and flagged), German Bionic (kept, flagged), Evondos (~200 staff, kept and flagged), UVD Robots / Blue Ocean Robotics (owned by Ecolab since 2022, kept and flagged), CMR Surgical (unicorn, kept and flagged), Distalmotion (raised $150M 2024, kept and flagged), Wandercraft (€64M Series D 2025, kept and flagged), Medical Microinstruments MMI (well-funded Series C+, kept and flagged).

### 3.3 Gaps introduced by my own pipeline

- **Email enrichment was serial, not agent-parallelized.** ~90 `WebFetch` calls from the main conversation. Some sites returned `contact_form_only` or `unreachable` after 1–2 tries; a human with a browser might extract emails from JavaScript-rendered pages I couldn't.
- **No fuzzy matching beyond normalized-name equality.** Near-duplicates with very different brand names (e.g., a renamed company or a subsidiary) would not have merged. The 40 merges reported are confident exact-match groupings.
- **No headcount/turnover verification.** `sme_likely` is inferred from funding stage and press coverage, not Orbis. A TEF-Health-grade SME check still requires the Business Registry or Orbis per-company.
- **Sub-domain classification is agent-authored, not standardized.** Some rows use `rehab-exoskeleton`, others `rehab/exoskeleton`, others `Rehabilitation (rehab)`. The field is useful for filtering but not perfectly normalized.

---

## 4. How to reproduce or extend

### To reproduce this run
```
# Shards are already in place; if you want to regenerate the master:
cd /home/fom/Documents/Docs/TEF-Health/listSMEs
python3 merge.py                # 5 CSVs in → master CSV out + needs_email_enrichment.csv
python3 apply_enrichment.py     # overlays shards/enrich_manual.csv
```

### To extend the list
1. **Highest ROI, free:** CORDIS advanced search for Horizon Europe SME participants whose topic contains "robotics" and whose project is in the health cluster. Likely adds 20–50 SMEs. Requires interactive filtering — not scriptable.
2. **Dealroom and Tracxn paid tiers** with "robotics + health" filters will 2x the list in one export.
3. **Cluster directories that were gated for the agents** (see §3.1): Medicen Paris Region full directory, Odense Robotics MedTech Robot Pathway, SPECTARIS medtech members, I-RIM conference attendee lists, Norway Health Tech member directory.
4. **Country gaps**: Czech, Slovak, Hungarian, Romanian, Balkan, Baltic (beyond Sentante / Rubedo Sistemos).
5. When adding a row, keep `source_url` mandatory and `confidence` honest — that's the discipline this list's credibility rests on.

### To convert this into a CRM-ready outreach list
- Strip `sme_likely=No` rows if you need strict SME filtering.
- Verify headcount via Orbis / national business registry for `sme_likely=Yes` rows before pitching TEF-Health de-minimis services.
- Do NOT harvest named-person emails by guessing patterns (firstname.lastname@domain). Use LinkedIn Sales Navigator or a GDPR-aware enrichment tool (Apollo, Lusha, Cognism) with a documented legitimate-interest assessment.
