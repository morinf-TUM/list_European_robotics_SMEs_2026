#!/usr/bin/env python3
"""Apply manual email enrichment to the master CSV."""
import csv
from pathlib import Path

BASE = Path("/home/fom/Documents/Docs/TEF-Health/listSMEs")
MASTER = BASE / "eu_healthcare_robotics_smes_master.csv"
ENRICH = BASE / "shards/enrich_manual.csv"
OUT = BASE / "eu_healthcare_robotics_smes_master.csv"  # overwrite

# Load enrichment into dict keyed by company name (case-insensitive, stripped)
enrich = {}
with open(ENRICH, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        key = r["company"].strip().lower()
        enrich[key] = r

# Load master, apply, rewrite
rows = []
with open(MASTER, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for r in reader:
        key = r["company"].strip().lower()
        if key in enrich:
            e = enrich[key]
            # Only overwrite if the master doesn't already have a better email
            if e.get("email") and not r.get("email"):
                r["email"] = e["email"]
                r["email_type"] = e["email_type"]
            elif not e.get("email") and not r.get("email"):
                # Keep the email_type info even without an email
                r["email_type"] = e["email_type"]
            # Append enrichment notes
            if e.get("notes"):
                existing = r.get("notes") or ""
                sep = " | " if existing else ""
                r["notes"] = (existing + sep + "enrich: " + e["notes"]).strip()[:350]
        rows.append(r)

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for r in rows:
        w.writerow(r)

# Summary
total = len(rows)
with_email = sum(1 for r in rows if r.get("email"))
form_only = sum(1 for r in rows if r.get("email_type") == "contact_form_only")
unreachable = sum(1 for r in rows if r.get("email_type") == "unreachable")
print(f"TOTAL rows: {total}")
print(f"  with verified email:    {with_email}")
print(f"  contact-form-only:      {form_only}")
print(f"  unreachable (flagged):  {unreachable}")
print(f"  remaining unknown:      {total - with_email - form_only - unreachable}")
