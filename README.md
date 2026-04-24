# EU Healthcare Robotics SMEs — research-grade list

**Data collection date:** 2026-04-23. Full methodology, per-agent source pools, rejection log, and documented gaps are in [`METHODOLOGY.md`](METHODOLOGY.md) — read that before acting on the list.

## Files
- **`eu_healthcare_robotics_smes_master.csv`** — 130 unique companies, the master list. Every row has a `source_url`.
- **`eu_healthcare_robotics_smes.csv`** — original 26-company seed list (kept for provenance).
- **`METHODOLOGY.md`** — pipeline, per-agent mandates and reported gaps, rejection log, how to reproduce.
- **`shards/`** — raw per-source outputs from 4 parallel research agents + manual enrichment. Use these to audit where any row came from.
- **`merge.py`** — dedupe + merge script (normalizes company names across legal-suffix variants).
- **`apply_enrichment.py`** — applies the manual contact-email pass onto the master.

## Coverage (as of 2026-04-23)
- **130 unique companies** across 18 European countries (AT, BE, CH, DE, DK, ES, FI, FR, GB, IE, IT, LT, LU, NL, NO, PL, PT, SE).
- **74 with verified role-level email** (info@, contact@, hello@, sales@, office@, business@, etc. — pulled live from each company's own website).
- **21 documented as contact-form-only** (site has a form but no email address visible).
- **14 flagged `unreachable`** (site down, TLS expired, 403/404/connection refused on repeated attempts — listed so you know to retry manually).
- **21 remaining without email**: mostly scale-ups we flagged `sme_likely=No` and deliberately excluded from enrichment (Spineart, Mauna Kea, Renishaw, Corin, Mentice, Exopulse, …), plus Haventure/YES!Delft portfolio companies without public sites yet.
- **Sub-domains covered:** surgical robotics (laparoscopy, spine, ortho, urology, ENT, ophthalmology, microsurgery, neurosurgery), rehab/exoskeleton (gait, upper-limb, hand, ICU, back), prosthetics/bionics, endovascular/TAVI/thrombectomy, microrobotics, capsule endoscopy, disinfection, pharmacy automation, clinical lab automation, assistive/elderly-care, radiotherapy positioning, social/service robots.

## Sources mined
Aggregated candidates from ~40+ sources — every row cites which one in `source_url`:

**EU-level programs**
EIT Health (Catapult, Headstart, Bridgehead, InnoStars, Wild Card), EIC Accelerator, DIH-HERO / RI4EU success stories, EIT Digital, Horizon Europe / CORDIS references, EIB InvestEU.

**Robotics clusters & accelerators**
RobotUnion (H2020), euRobotics AISBL, Odense Robotics cluster, Medicen Paris Region, I-RIM Italy, Catalonia Robotics Cluster, Venturelab / Venture Kick (CH), Fongit (CH).

**National health incubators**
YES!Delft, HighTechXL, Eindhoven Medical Robotics, Haventure (Grenoble), Eurasanté (Lille), Medicalps (Grenoble), Biocat / Barcelona Health Hub, Norway Health Tech, Startup Luxembourg, parisantecampus-adjacent coverage, Digital Health London, CRAASH Barcelona, BaseLaunch (observed, low yield), BioInnovation Institute (observed, low yield).

**Public lists & directories**
Dealroom public robotics list, Tracxn "Robotics in Healthcare Europe," Sifted curated lists, EU-Startups directory, Exoskeleton Report directory, MedicalStartups.org, StartUs Insights, Surgical Robotics Technology company directory, Foundernest, The Robot Report, tech.eu, Wellfound, Crunchbase hub pages, MedTech Pulse.

## Columns
- `company`, `country` (ISO alpha-2), `sub_domain`, `website`.
- `email` — **role-level only** (info@, contact@, hello@, sales@, office@, business@, support@, partnerships@, press@, etc.). Never named-person emails (GDPR/PECR reasons; see below).
- `email_type` — `generic` | `contact_form_only` | `unreachable` | `unknown` | blank.
- `sme_likely` — `Yes` | `No` | `unknown`. `No` = verified scale-up that likely exceeds EU SME thresholds (<250 staff, ≤€50M turnover or ≤€43M balance sheet), or acquired by a non-SME parent. `unknown` = couldn't verify size from public sources.
- `source_url` — exact URL of the incubator / accelerator / list page where the company was identified. **Every row has one.**
- `notes` — HQ city, funding stage, product, cross-sourcing tag, enrichment notes.
- `confidence` — `high` (from program's own portfolio page or the company's own site), `medium` (from news/derivative source), `low` (single unverified reference).

## Known limitations (be honest about these before you act on the list)
1. **Completeness.** Tracxn claims 177 "robotics in healthcare" companies in Europe. We have 130 after filtering non-robotic and non-SME candidates. There are still gaps in: Czech/Slovak/Hungarian/Romanian/Baltic coverage; full Odense Robotics & Medicen member directories (require interactive filtering behind portals); EIC Accelerator / EIT Health full beneficiary rosters (TEF-Health itself does not publish Call 1/2 awardees publicly).
2. **SME check is rough.** 103 flagged `Yes`, 18 `No`, 9 `unknown`. The `No` flags are conservative — companies like CMR Surgical, Distalmotion, Wandercraft, MMI, German Bionic, Hocoma, UVD/Blue Ocean, Spineart, Mauna Kea, Corin, Renishaw Neurosurgery, Caranx Medical, Artedrone, Exopulse, Preceyes, Endocontrol, Idrogenet/Gloreha, Mentice, Bioservo are **likely** over the EU SME threshold OR recently acquired. Verify headcount/turnover against Orbis or the Business Registry before including in a formal SME-only outreach.
3. **Sub-domain edge cases.** A handful of entries are borderline-robotic (Neuroelectrics: EEG/stimulation wearable; Fundamental Surgery: haptic VR training; SoundCell: graphene nanodrum sensor; Somnox: breathing sleep robot with some motion). Agents included them because the sources did; re-classify per your definition of "robotics."
4. **Email enrichment stopped at role-level.** We did not harvest named-person addresses. Apollo / Lusha / Cognism / LinkedIn Sales Navigator are the right tools for that — and they require documenting a lawful basis under GDPR/PECR before you send.
5. **Merged duplicates** — 40 rows were merged across shards (e.g. ABLE Human Motion appeared in 3 sources). The surviving row carries `[cross-sourced xN]` in its notes so you can tell.
6. **Unreachable sites:** 14 companies had TLS/DNS/connection issues during enrichment (DEAM, Preceyes, Tendo, Rejoint, Meditek, BEC GmbH, qbrobotics, Heaxel/ordonnances.org redirect, Virtualware, YouRehab/Rehastim, Hipermotion, Perceive3D, Fundamental Surgery, Caranx Medical post-acquisition). Each flagged in the CSV. Manually retry before dismissing.

## GDPR / PECR before any send
- Role addresses (info@, sales@, partnerships@) to B2B targets with a relevant service offer → low risk. Include identity + clear opt-out.
- Named-person addresses scraped or guessed → high risk in EU/EEA; UK PECR also bans unsolicited marketing to sole traders/partnerships without consent.
- Document for each contact: (a) source, (b) why you believe you have a legitimate interest, (c) how to unsubscribe.

## To extend further
1. **CORDIS**: query `project.topic contains 'robotics' AND participant.type = SME AND country in EU27`. Will surface Eurostars / Horizon Europe SME beneficiaries not in this list. Requires the web UI, cannot be scraped statically.
2. **Dealroom / Tracxn paid tiers**: turn on the robotics + healthtech filters and export.
3. **Country-specific follow-ups** (flagged thin by the research agents): German Fraunhofer IPA / IFF spin-offs; French Medicen full directory; Spanish Biocat BioRegion directory; Italian I-RIM conference attendees; Swiss euRobotics healthcare topic group leaders; Czech Robotics Cluster members; Polish Robotics Cluster beyond EGZOTech / BioCam / Aether / ACCREA.
4. **Niches where EU coverage is thin**: dental surgery robotics (no confirmed EU SME), hair-transplant robotics (US-dominated), capsule-endoscopy robotics (only BioCam), dedicated robotic ophthalmology (Preceyes acquired by Zeiss), robotic ENT (Medineering absorbed by Brainlab). These are real gaps, not oversights — the market is small in Europe.

## How to audit a row
Open the CSV, find the row, click the `source_url`. If the source page still names the company, confidence is at least `medium`. To raise to `high`: visit the company's own site, confirm the email in the CSV appears there verbatim, and confirm HQ country from the footer or imprint.
