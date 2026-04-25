# EU Healthcare Robotics SMEs — research-grade list

**Pass 1 data collection:** 2026-04-23 (130 companies).
**Pass 2 data collection:** 2026-04-24 (+97 → 227 total). Filled the gaps logged in pass 1: MEDICA exhibitor scan, cluster member directories, CEE/Baltic deep-dive, CORDIS/EIC beneficiaries, university spin-offs.
**Pass 3 data collection:** 2026-04-25 (+42 → 269 total). Tier 1 of the exhaustive plan: deeper CORDIS/EIT Health, MEDICA + COMPAMED full product-group scan, EIC + EIB beneficiaries 2021-2025, gated cluster member directories. See `METHODOLOGY.md` §6.

Full methodology, per-agent source pools, rejection log, and documented remaining gaps are in [`METHODOLOGY.md`](METHODOLOGY.md) — read that before acting on the list.

## Files
- **`eu_healthcare_robotics_smes_master_expanded.csv`** ← **use this**. 269 unique companies. Pass-2 + pass-3 additions are tagged `[pass-2]` in their `notes`.
- **`eu_healthcare_robotics_smes_master.csv`** — pass-1 master (130 companies). Kept for provenance.
- **`eu_healthcare_robotics_smes.csv`** — original 26-company seed list.
- **`METHODOLOGY.md`** — pipeline, per-agent mandates, gaps, rejection log, how to reproduce (all three passes + future tiers).
- **`shards/`** — raw per-source outputs from 12 parallel research agents + manual enrichment. Use these to audit where any row came from.
  - Pass-1 shards: `agent1_eu_programs`, `agent2_robotics_clusters`, `agent3_national_incubators`, `agent4_public_lists`.
  - Pass-2 shards: `agent5_medica_tradeshows`, `agent6_cluster_deep_dives`, `agent7_cee_baltic_nordic`, `agent8_cordis_spinoffs`.
  - Pass-3 shards: `agent9_cordis_eithealth`, `agent10_medica_compamed`, `agent11_eic_eib`, `agent12_gated_clusters`.
- **`merge.py`** — pass-1 dedupe + merge script (NOTE: stale `BASE` path; see METHODOLOGY §4).
- **`extend.py`** — pass-2 + pass-3 merge: existing master + 8 new shards → expanded master. Resolves paths relative to its own location. Re-runnable.
- **`apply_enrichment.py`** — applies the manual contact-email pass onto the pass-1 master.

## Coverage (as of 2026-04-25, expanded master)
- **269 unique companies** across **28 European countries**: AT, BE, BG, CH, CZ, DE, DK, EE, ES, FI, FR, GB, GR, HR, HU, IE, IT, LT, LU, LV, NL, NO, PL, PT, RO, SE, SI, SK.
- **84 with verified role-level email**. Pass-3 added 5 (info@precisis.de, info@inbrain-neuroelectronics.com, info@overture.life, info@nyxoah.com, investor.relations@edap-tms.com).
- **~185 rows still without an email** — enrichment run is still owed on pass-2 and pass-3 rows.
- **21 contact-form-only** (from pass 1).
- **14 `unreachable`** (from pass 1; not retried since).
- **`sme_likely` breakdown:** Yes = 225, No = 35, unknown = 9. Pass 3 added 11 to the `No` bucket (large public companies and parent-owned subsidiaries: Surgical Science, Inpeco, United Robotics Group, Universal Robots, Kassow Robots, Robotnik Automation, Andrew Alliance/Waters, Demcon Medical Robotics, Sonceboz, Nyxoah, EDAP TMS).
- **Sub-domains covered (after pass 3):** surgical robotics (laparoscopy, spine, ortho, urology, ENT, ophthalmology, microsurgery, neurosurgery, cardiac, endodontics, bone-selective burring, MRI-guided biopsy, ultrasonic scalpels, NOTES, percutaneous needle), **robotic HIFU**, **robotic IVF/embryology**, **robotic intravitreal injection**, rehab/exoskeleton (gait, upper-limb, hand, ICU, back, motorised knee orthosis, stroke arm, soft exosuit), prosthetics/bionics, endovascular/TAVI/thrombectomy/guidewires/aortic-occlusion, microrobotics, capsule endoscopy, **robotic phlebotomy** (new), **sample-collection robotics** (new), **CO2 angiography automation** (new), disinfection (UV-C + H2O2 dry-mist), pharmacy automation, clinical lab automation (pipetting, cell culture, digital pathology), assistive/elderly-care (humanoid, self-driving wheelchair, transport AMR, dementia robot, companion robot), radiotherapy positioning, **active implantable neurostim** (expanded — epilepsy, brain interface, sleep apnea, post-prostatectomy, neuromuscular), social/service robots, intubation robotics, medical drone logistics, tele-operated remote imaging/MRI-CT, surgical training hardware, BCI/neurostim/biofeedback, **medical-grade actuator/motor/electronics OEMs** (component-supplier tier — Sonceboz, Mirmex Motor, KOCO MOTION, Solectrix, Hankamp Gears).

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
1. **Completeness.** Tracxn claims 177 "robotics in healthcare" companies in Europe; Dealroom shows a broader hardware-health pool. We have **269 after pass 3**, filtering non-robotic and non-SME candidates. Remaining gaps: **dental surgery robotics** (no confirmed EU SME — US-dominated market), **hair transplant robotics** (no EU competitor identified), **EU capsule endoscopy** (only BioCam + Atlas Endoscopy), **TEF-Health Call 1/2 awardees** (still not published — zero direct TEF-Health beneficiaries on the list), and **email enrichment owed for the 185 rows added in passes 2 and 3** (only 84/269 have a role-level email).
2. **SME check is rough.** 225 flagged `Yes`, 35 `No`, 9 `unknown`. Pass-1 `No` flags (CMR Surgical, Distalmotion, Wandercraft, MMI, German Bionic, Hocoma, UVD/Blue Ocean, Spineart, Mauna Kea, Corin, Renishaw, Caranx, Exopulse, Mentice, Bioservo, Preceyes, Endocontrol, Idrogenet/Gloreha) remain. Pass 2 added `No` flags on: BTL Industries (CZ), 3DHISTECH (HU), SpineGuard (FR Euronext), IMSTec (DE ~150 staff), ab medica (IT large distributor group), Generative Bionics (IT €70M seed). Pass 3 added `No` flags on: Surgical Science (SE Nasdaq Stockholm), Inpeco (CH ~2600 systems shipped), United Robotics Group (DE integrator/holding), Universal Robots (DK Teradyne), Kassow Robots (DK Bosch Rexroth), Robotnik Automation (ES URG-acquired), Andrew Alliance (CH Waters Lab Automation brand), Demcon Medical Robotics (NL group >1000 staff), Sonceboz (CH ~700 staff), Nyxoah (BE Euronext/Nasdaq), EDAP TMS (FR Nasdaq). Verify headcount/turnover against Orbis or the Business Registry before any formal SME-only outreach. Orbis NACE-26.60/32.50 query is the single highest-yield missing source.
3. **Sub-domain edge cases.** A handful of entries are borderline-robotic (Neuroelectrics: EEG/stimulation wearable; Fundamental Surgery: haptic VR training; SoundCell: graphene nanodrum sensor; Somnox: breathing sleep robot with some motion). Agents included them because the sources did; re-classify per your definition of "robotics."
4. **Email enrichment stopped at role-level.** We did not harvest named-person addresses. Apollo / Lusha / Cognism / LinkedIn Sales Navigator are the right tools for that — and they require documenting a lawful basis under GDPR/PECR before you send.
5. **Merged duplicates** — 40 rows were merged across shards (e.g. ABLE Human Motion appeared in 3 sources). The surviving row carries `[cross-sourced xN]` in its notes so you can tell.
6. **Unreachable sites:** 14 companies had TLS/DNS/connection issues during enrichment (DEAM, Preceyes, Tendo, Rejoint, Meditek, BEC GmbH, qbrobotics, Heaxel/ordonnances.org redirect, Virtualware, YouRehab/Rehastim, Hipermotion, Perceive3D, Fundamental Surgery, Caranx Medical post-acquisition). Each flagged in the CSV. Manually retry before dismissing.

## GDPR / PECR before any send
- Role addresses (info@, sales@, partnerships@) to B2B targets with a relevant service offer → low risk. Include identity + clear opt-out.
- Named-person addresses scraped or guessed → high risk in EU/EEA; UK PECR also bans unsolicited marketing to sole traders/partnerships without consent.
- Document for each contact: (a) source, (b) why you believe you have a legitimate interest, (c) how to unsubscribe.

## To extend further (post pass 3)

Pass 3 closed Tier 1 of the exhaustive plan (CORDIS + MEDICA full + EIC + gated clusters). What remains:

1. **Orbis / Bureau van Dijk NACE-26.60/32.50 SME query** — the single highest-yield remaining source. Filters: NACE 26.60 (irradiation/electromedical) + 32.50 (medical instruments) ∧ headcount 10–249 ∧ turnover ≤ €50M ∧ EU27+CH+UK+NO+IS+LI ∧ keyword `robot*`/`exoskeleton`/`surgical platform`. Paid; TEF-Health institutional access likely. Expected yield: 50–100 net new + retroactive `sme_likely` verification of all 269.
2. **Email enrichment on the ~185 rows currently without one** — pipeline's missing step. Regenerate `needs_email_enrichment.csv` from the expanded master and run a WebFetch pass like pass-1's enrichment.
3. **Tier 2 of the plan** — vertical surgical-conference exhibitor lists (Hamlyn Symposium, CRAS, EAU, EFORT, EANS, CIRSE, ESGE, IEEE ICRA/IROS health-demo); regional innovation agencies (Medical Valley EMN, Lyonbiopôle, Toscana Life Sciences, OBN, ACMIT, Health Cluster Portugal, Corallia, etc.); university TTOs not yet hit (Oxford, Cambridge, Fraunhofer Venture, Politecnico Milano/Torino, KTH, NTNU, BME Hungary, AGH Krakow); Eurostars beneficiary database; EUDAMED + Notified Body certificate searches. Expected yield: 60–120.
4. **Tier 3** — Dealroom/Tracxn/PitchBook paid-tier exports; EPO/WIPO patent mining; LinkedIn Sales Navigator manual filter; M&A reverse-engineering of Stryker/Zimmer/Smith+Nephew/Medtronic/JJ/BD/Philips/Zeiss/Brainlab/Ottobock acquisition history.
5. **Reclassification pass** — review the `confidence=low` rows now on master against a tightened active-actuation definition. Likely outcome: −10 to −20 rows but higher credibility.
6. **Cluster directories that even pass 3 couldn't walk**: SPECTARIS Mitglieder, CATROBOTICS members, Biocat Salesforce-hosted directory, Medicen full adherents page, full Odense Robotics member roster. Same companies likely in Orbis or Tracxn paid tiers.
7. **Collapse legacy rows where mergers are documented** — KAT + LinkX + OSTESYS → Kyniska Robotics (2024); Caranx Medical + Artedrone → Carvolix (Dec 2025). Currently kept as separate rows for source-URL provenance.
8. **Niches where EU coverage is genuinely thin** (market gap, not oversight): dental surgery robotics (Neocis/Perceptive are US), hair-transplant robotics (US-dominated), robotic ophthalmology (Preceyes → Zeiss), robotic ENT (Medineering → Brainlab).
9. **Ukrainian medtech robotics SMEs** (CheckEye and similar) — currently out of scope. Widen scope if EU candidate countries are in play.
10. **TEF-Health Call 1/2 awardees** — not publicly published. Direct ask to the TEF-Health consortium is the only fix.

## How to audit a row
Open the CSV, find the row, click the `source_url`. If the source page still names the company, confidence is at least `medium`. To raise to `high`: visit the company's own site, confirm the email in the CSV appears there verbatim, and confirm HQ country from the footer or imprint.
