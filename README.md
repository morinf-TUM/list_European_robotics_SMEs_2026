# EU Healthcare Robotics SMEs — research-grade list

**Pass 1 data collection:** 2026-04-23 (130 companies).
**Pass 2 data collection:** 2026-04-24 (+97 new → 227 total). Pass 2 targets the gaps explicitly logged in pass 1: MEDICA exhibitor scan, cluster member directories, CEE/Baltic deep-dive, CORDIS/EIC beneficiaries, university spin-offs.

Full methodology, per-agent source pools, rejection log, and documented remaining gaps are in [`METHODOLOGY.md`](METHODOLOGY.md) — read that before acting on the list.

## Files
- **`eu_healthcare_robotics_smes_master_expanded.csv`** ← **use this**. 227 unique companies. Pass-2 additions are tagged `[pass-2]` in their `notes`.
- **`eu_healthcare_robotics_smes_master.csv`** — pass-1 master (130 companies). Kept for provenance and because pass-2 is a superset.
- **`eu_healthcare_robotics_smes.csv`** — original 26-company seed list (kept for provenance).
- **`METHODOLOGY.md`** — pipeline, per-agent mandates and reported gaps, rejection log, how to reproduce (both passes).
- **`shards/`** — raw per-source outputs from 8 parallel research agents + manual enrichment. Use these to audit where any row came from. Pass-1 shards: `agent1..agent4`. Pass-2 shards: `agent5_medica_tradeshows`, `agent6_cluster_deep_dives`, `agent7_cee_baltic_nordic`, `agent8_cordis_spinoffs`.
- **`merge.py`** — pass-1 dedupe + merge script (NOTE: has a stale `BASE` path; see METHODOLOGY §4).
- **`extend.py`** — pass-2 merge: takes the pass-1 master + 4 new shards and writes the expanded master. Resolves paths relative to its own location.
- **`apply_enrichment.py`** — applies the manual contact-email pass onto the pass-1 master.

## Coverage (as of 2026-04-24, expanded master)
- **227 unique companies** across **28 European countries**: AT, BE, BG, CH, CZ, DE, DK, EE, ES, FI, FR, GB, GR, HR, HU, IE, IT, LT, LU, LV, NL, NO, PL, PT, RO, SE, SI, SK. (Pass 1: 18 countries. Pass 2 adds BG, CZ, EE, GR, HR, HU, LV, RO, SI, SK.)
- **79 with verified role-level email** carried over from pass 1 (info@, contact@, hello@, sales@, office@, business@). Pass-2 rows are mostly email-blank — an enrichment run is still owed on the 97 new companies.
- **21 contact-form-only** (from pass 1).
- **14 `unreachable`** (from pass 1; not retried in pass 2).
- **148 rows currently without an email** (≈21 pass-1 deliberate skips + ≈97 pass-2 additions + 30 borderline).
- **`sme_likely` breakdown:** Yes = 194, No = 24, unknown = 9.
- **Sub-domains covered (expanded):** surgical robotics (laparoscopy, spine, ortho, urology, ENT, ophthalmology, microsurgery, neurosurgery, cardiac, endodontics, bone-selective burring, MRI-guided biopsy, ultrasonic scalpels), rehab/exoskeleton (gait, upper-limb, hand, ICU, back, motorised knee orthosis, stroke arm), prosthetics/bionics, endovascular/TAVI/thrombectomy/guidewires/aortic-occlusion, microrobotics (magnetic catheters, MEMS), capsule endoscopy, disinfection (UV-C + H2O2 dry-mist), pharmacy automation (dispensing, vending, blister packing), clinical lab automation (pipetting, cell culture, digital pathology), assistive/elderly-care (humanoid, self-driving wheelchair, transport AMR), radiotherapy positioning, social/service robots, **intubation robotics** (new), **medical drone logistics** (new), **tele-operated remote imaging/MRI-CT** (new), **surgical training hardware** (new), **BCI / neurostim / biofeedback** (expanded).

## Sources mined
Aggregated candidates from ~60+ sources across two passes — every row cites which one in `source_url`:

**EU-level programs**
EIT Health (Catapult 2023-24 + 2024-25, Headstart, Bridgehead, InnoStars 2024, Wild Card), EIC Accelerator beneficiaries, EIC Fund, CORDIS Horizon Europe (project pages with SME participant lists, e.g. 101113904 ARVIS, 688592 ENDOO, 101211633 IRE4Health, 190171705 VEMOtion), Eurostars, DIH-HERO / RI4EU success stories, EIT Digital, EIB InvestEU.

**Robotics clusters & accelerators**
RobotUnion (H2020), euRobotics AISBL, Odense Robotics cluster (full member list incl. MedTech Robot Pathway — pass 2), Medicen Paris Region, I-RIM Italy, Catalonia Robotics Cluster, SPECTARIS medtech (DE — pass 2), Venturelab / Venture Kick (CH — incl. Venture Leaders Medtech 2025), Fongit (CH), BioAlps (CH — pass 2), MedLife-EV (DE — pass 2), I3P Turin incubator.

**National health incubators**
YES!Delft (incl. MedTech Accelerator 2024 cohort), HighTechXL, Eindhoven Medical Robotics, Haventure (Grenoble — incl. 2024 KAT+LinkX+Ostesys → Kyniska merger), Eurasanté (Lille), Medicalps (Grenoble — full directory pass 2), Biocat / Barcelona Health Hub, Norway Health Tech (full member list — pass 2), Startup Luxembourg, parisantecampus-adjacent coverage, Digital Health London, CRAASH Barcelona, BaseLaunch (observed, low yield), BioInnovation Institute (observed, low yield).

**University spin-off directories (pass 2)**
UCL Business, Imperial Enterprise Lab, University of Leeds STORM Lab, University of Glasgow, Trinity College Dublin, TU Delft / YES!Delft, TU/e, University of Twente TechMed Centre, Erasmus MC, Scuola Superiore Sant'Anna BioRobotics (Pisa), Istituto Italiano di Tecnologia (IIT Genoa), Politecnico di Milano, EPFL Innovation Park, ETH Zurich MSRL / Pioneer Fellowship, University of Zurich / UniversitätsSpital Zürich, Chalmers, KTH, Medical University of Vienna, University of Innsbruck, TU Munich, University of Freiburg, Heidelberg, FORTH Heraklion, University of Zagreb (RONNA), TalTech.

**Trade shows (pass 2)**
MEDICA Düsseldorf main exhibitor directory + Start-up Competition finalists 2024/2025, COMPAMED, MedtecLIVE with T4M Nuremberg, Automatica Healthtech Pavilion 2025, SLAS Europe 2025, Arab Health, DMEA Berlin.

**Country-specific sources (pass 2)**
Wediditinpoland, Warsaw University of Technology spin-off portal, Poznań/Wrocław/Gdańsk university portals, Czech National Medical Device agency SÚKL, CzechInvest, BUT Brno spin-off portal, STU Bratislava, BME/Semmelweis (HU), UPB / UMF Cluj (RO), TU Sofia, Aristotle Univ Thessaloniki, Tehnopol TalTech, Portugal Ventures portfolio, Fraunhofer AICOS.

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
1. **Completeness.** Tracxn claims 177 "robotics in healthcare" companies in Europe; Dealroom shows a broader hardware-health pool. We have 227 after pass 2, filtering non-robotic and non-SME candidates. Remaining gaps: **dental surgery robotics** (no confirmed EU SME — market is US-dominated), **hair transplant robotics** (no EU competitor identified), **EU capsule endoscopy** (only BioCam), **TEF-Health Call 1/2 awardees** (still not published — zero direct TEF-Health beneficiaries in the list), and **pass-2 email enrichment for the 97 new rows** (owed but not yet run).
2. **SME check is rough.** 194 flagged `Yes`, 24 `No`, 9 `unknown`. Pass-1 `No` flags (CMR Surgical, Distalmotion, Wandercraft, MMI, German Bionic, Hocoma, UVD/Blue Ocean, Spineart, Mauna Kea, Corin, Renishaw, Caranx, Exopulse, Mentice, Bioservo, Preceyes, Endocontrol, Idrogenet/Gloreha) remain. Pass 2 adds `No` flags on: BTL Industries (CZ), 3DHISTECH (HU), SpineGuard (FR, Euronext-listed), IMSTec (DE, ~150 staff), ab medica (IT, large distributor group), Generative Bionics (IT, €70M seed). Verify headcount/turnover against Orbis or the Business Registry before including in a formal SME-only outreach.
3. **Sub-domain edge cases.** A handful of entries are borderline-robotic (Neuroelectrics: EEG/stimulation wearable; Fundamental Surgery: haptic VR training; SoundCell: graphene nanodrum sensor; Somnox: breathing sleep robot with some motion). Agents included them because the sources did; re-classify per your definition of "robotics."
4. **Email enrichment stopped at role-level.** We did not harvest named-person addresses. Apollo / Lusha / Cognism / LinkedIn Sales Navigator are the right tools for that — and they require documenting a lawful basis under GDPR/PECR before you send.
5. **Merged duplicates** — 40 rows were merged across shards (e.g. ABLE Human Motion appeared in 3 sources). The surviving row carries `[cross-sourced xN]` in its notes so you can tell.
6. **Unreachable sites:** 14 companies had TLS/DNS/connection issues during enrichment (DEAM, Preceyes, Tendo, Rejoint, Meditek, BEC GmbH, qbrobotics, Heaxel/ordonnances.org redirect, Virtualware, YouRehab/Rehastim, Hipermotion, Perceive3D, Fundamental Surgery, Caranx Medical post-acquisition). Each flagged in the CSV. Manually retry before dismissing.

## GDPR / PECR before any send
- Role addresses (info@, sales@, partnerships@) to B2B targets with a relevant service offer → low risk. Include identity + clear opt-out.
- Named-person addresses scraped or guessed → high risk in EU/EEA; UK PECR also bans unsolicited marketing to sole traders/partnerships without consent.
- Document for each contact: (a) source, (b) why you believe you have a legitimate interest, (c) how to unsubscribe.

## To extend further (post pass 2)
1. **Email enrichment on the 97 pass-2 additions** — the pipeline's missing step. Regenerate `needs_email_enrichment.csv` from the expanded master and run the same WebFetch enrichment that pass 1 used.
2. **CORDIS / EIC Accelerator paid-tier and authenticated access** — pass-2 agents could surface CORDIS candidates from search-snippet snapshots but could not enumerate full Horizon Europe Cluster 1 (Health) SME participant lists. Interactive filtering in the CORDIS UI and the EIC Dashboard will add more.
3. **Dealroom / Tracxn paid tiers**: turn on the robotics + healthtech filters and export for 1-click overlap analysis.
4. **Collapse legacy Haventure rows into Kyniska Robotics** — KAT Robotics, LinkX Robotics, and OSTESYS all merged into Kyniska in Sept 2024 (pass-2 finding). Four rows currently, should be one with merger history in notes.
5. **Niches where EU coverage is genuinely thin** (market gap, not oversight): dental surgery robotics (no confirmed EU SME — Neocis/Perceptive are US), hair-transplant robotics (US-dominated), capsule-endoscopy robotics (only BioCam EU-side), robotic ophthalmology (Preceyes → Zeiss), robotic ENT (Medineering → Brainlab). Pass 2 did not find new candidates in these.
6. **Ukrainian medtech robotics SMEs** (CheckEye and similar) — currently out of scope. Widen scope if EU candidate countries are in play.

## How to audit a row
Open the CSV, find the row, click the `source_url`. If the source page still names the company, confidence is at least `medium`. To raise to `high`: visit the company's own site, confirm the email in the CSV appears there verbatim, and confirm HQ country from the footer or imprint.
