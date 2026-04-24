#!/usr/bin/env python3
"""Second-pass merge: extend the existing master with 4 new shards.

Keeps the existing master's email enrichment (74 verified addresses).
Adds new companies from the second-pass shards (agent5..agent8).
Dedupe by normalized company name. Never overwrites an existing email.
"""
import csv
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent
EXISTING_MASTER = BASE / "eu_healthcare_robotics_smes_master.csv"
NEW_SHARDS = [
    BASE / "shards/agent5_medica_tradeshows.csv",
    BASE / "shards/agent6_cluster_deep_dives.csv",
    BASE / "shards/agent7_cee_baltic_nordic.csv",
    BASE / "shards/agent8_cordis_spinoffs.csv",
]
OUT_MASTER = BASE / "eu_healthcare_robotics_smes_master_expanded.csv"

MASTER_HEADERS = [
    "company", "country", "sub_domain", "website",
    "email", "email_type", "sme_likely",
    "source_url", "notes", "confidence",
]


def normalize_name(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(
        r"\b(gmbh|ag|sa|sas|srl|s\.r\.l\.|s\.p\.a\.|spa|ltd|limited|plc|"
        r"bv|b\.v\.|nv|n\.v\.|ab|aps|oy|uab|aisbl|sl|ou|zrt)\b",
        "",
        s,
    )
    trailing = r"\s+(technologies|systems|group|medical|robotics|bionics|healthcare|devices|medtech|labs|lab|company|co|solutions|international|global)$"
    prev = None
    while prev != s:
        prev = s
        s = re.sub(trailing, "", s)
    s = re.sub(r"\([^)]*\)", "", s)
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def normalize_country(c: str) -> str:
    c = (c or "").strip().upper()
    mapping = {
        "UK": "GB", "UNITED KINGDOM": "GB",
        "DEUTSCHLAND": "DE", "GERMANY": "DE",
        "FRANCE": "FR",
        "ITALY": "IT", "ITALIA": "IT",
        "SPAIN": "ES", "ESPANA": "ES",
        "SWITZERLAND": "CH",
        "DENMARK": "DK",
        "NETHERLANDS": "NL",
        "SWEDEN": "SE",
        "IRELAND": "IE",
        "AUSTRIA": "AT",
        "BELGIUM": "BE",
        "POLAND": "PL",
        "LITHUANIA": "LT", "LATVIA": "LV", "ESTONIA": "EE",
        "LUXEMBOURG": "LU",
        "NORWAY": "NO",
        "PORTUGAL": "PT",
        "FINLAND": "FI",
        "CZECH REPUBLIC": "CZ", "CZECHIA": "CZ",
        "SLOVAKIA": "SK",
        "HUNGARY": "HU",
        "ROMANIA": "RO",
        "BULGARIA": "BG",
        "SLOVENIA": "SI",
        "CROATIA": "HR",
        "GREECE": "GR",
    }
    return mapping.get(c, c[:2] if len(c) >= 2 else c)


def row_quality_score(row: dict) -> int:
    score = 0
    conf = (row.get("confidence") or "").lower()
    score += {"high": 30, "medium": 15, "low": 5}.get(conf, 0)
    if row.get("email"):
        score += 20
    if row.get("email_type") == "generic":
        score += 10
    if row.get("website"):
        score += 10
    if row.get("sme_likely") in ("Yes", "No"):
        score += 5
    if row.get("source_url"):
        score += 5
    # Boost existing master rows (which carry enriched emails + confirmed cross-sourcing)
    if row.get("_origin") == "master":
        score += 25
    notes_len = len(row.get("notes") or "")
    score += min(notes_len // 20, 5)
    return score


def read_csv(path: Path, origin: str) -> list[dict]:
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            for h in MASTER_HEADERS:
                r.setdefault(h, "")
            r["company"] = (r.get("company") or "").strip()
            r["country"] = normalize_country(r.get("country") or "")
            r["website"] = (r.get("website") or "").strip().rstrip("/")
            r["email"] = (r.get("email") or "").strip().lower()
            if r.get("email_type") == "role":
                r["email_type"] = "generic"
            r["_origin"] = origin
            rows.append(r)
    return rows


def main():
    if not EXISTING_MASTER.exists():
        print(f"MISSING MASTER: {EXISTING_MASTER}", file=sys.stderr)
        sys.exit(1)

    master_rows = read_csv(EXISTING_MASTER, origin="master")
    print(f"existing master: {len(master_rows)} rows")

    new_rows: list[dict] = []
    for shard in NEW_SHARDS:
        if not shard.exists():
            print(f"MISSING SHARD: {shard}", file=sys.stderr)
            continue
        rs = read_csv(shard, origin=shard.stem)
        print(f"{shard.name}: {len(rs)} rows")
        new_rows.extend(rs)

    all_rows = master_rows + new_rows

    groups: dict[str, list[dict]] = {}
    for r in all_rows:
        key = normalize_name(r["company"])
        if not key:
            continue
        groups.setdefault(key, []).append(r)

    merged: list[dict] = []
    added_count = 0
    for key, group in groups.items():
        group.sort(key=row_quality_score, reverse=True)
        best = dict(group[0])
        origins = {r["_origin"] for r in group}
        for r in group[1:]:
            for field in ("website", "sub_domain", "notes", "source_url"):
                if not best.get(field) and r.get(field):
                    best[field] = r[field]
            # Never overwrite an existing email with a blank; prefer any verified one
            if not best.get("email") and r.get("email"):
                best["email"] = r["email"]
                if r.get("email_type"):
                    best["email_type"] = r["email_type"]
            if best.get("email_type") != "generic" and r.get("email_type") == "generic":
                best["email_type"] = "generic"
            if best.get("sme_likely") == "unknown" and r.get("sme_likely") in ("Yes", "No"):
                best["sme_likely"] = r["sme_likely"]
        if "master" not in origins:
            added_count += 1
            # Mark as new-pass addition
            note = best.get("notes") or ""
            tag = " [pass-2]"
            if tag not in note:
                best["notes"] = (note + tag).strip()
        merged.append(best)

    merged.sort(key=lambda r: (r["country"], (r["sub_domain"] or "").lower(), r["company"].lower()))

    with open(OUT_MASTER, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=MASTER_HEADERS)
        w.writeheader()
        for r in merged:
            w.writerow({h: r.get(h, "") for h in MASTER_HEADERS})

    total = len(merged)
    with_email = sum(1 for r in merged if r.get("email"))
    sme_yes = sum(1 for r in merged if r.get("sme_likely") == "Yes")
    sme_no = sum(1 for r in merged if r.get("sme_likely") == "No")
    sme_unknown = sum(1 for r in merged if r.get("sme_likely") not in ("Yes", "No"))
    countries = sorted({r["country"] for r in merged if r["country"]})
    print()
    print(f"EXPANDED MASTER: {total} unique companies ({len(master_rows)} existing + {added_count} new)")
    print(f"  with email: {with_email}")
    print(f"  SME likely Yes: {sme_yes}  No: {sme_no}  unknown: {sme_unknown}")
    print(f"  countries ({len(countries)}): {', '.join(countries)}")


if __name__ == "__main__":
    main()
