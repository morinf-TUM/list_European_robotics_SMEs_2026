#!/usr/bin/env python3
"""Merge shard CSVs + seed into a master, dedupe by normalized company name."""
import csv
import re
import sys
from pathlib import Path

BASE = Path("/home/fom/Documents/Docs/TEF-Health/listSMEs")
SHARDS = [
    BASE / "eu_healthcare_robotics_smes.csv",  # seed
    BASE / "shards/agent1_eu_programs.csv",
    BASE / "shards/agent2_robotics_clusters.csv",
    BASE / "shards/agent3_national_incubators.csv",
    BASE / "shards/agent4_public_lists.csv",
]

OUT_MASTER = BASE / "eu_healthcare_robotics_smes_master.csv"
OUT_NEEDS_EMAIL = BASE / "needs_email_enrichment.csv"

# Canonical headers for master
MASTER_HEADERS = [
    "company", "country", "sub_domain", "website",
    "email", "email_type", "sme_likely",
    "source_url", "notes", "confidence",
]

SEED_HEADERS = [
    "company", "country", "sub_domain", "website",
    "email", "email_type", "sme_likely", "notes", "data_confidence",
]


def normalize_name(name: str) -> str:
    """Normalize company name for dedup. Keeps meaningful distinctions."""
    s = name.lower().strip()
    # strip common legal suffixes
    s = re.sub(
        r"\b(gmbh|ag|sa|sas|srl|s\.r\.l\.|s\.p\.a\.|spa|ltd|limited|plc|"
        r"bv|b\.v\.|nv|n\.v\.|ab|aps|oy|uab|aisbl|sl|sas|ou|zrt)\b",
        "",
        s,
    )
    # strip common trailing descriptors iteratively
    trailing = r"\s+(technologies|systems|group|medical|robotics|bionics|healthcare|devices|medtech|labs|lab|company|co|solutions|international|global)$"
    prev = None
    while prev != s:
        prev = s
        s = re.sub(trailing, "", s)
    # strip parenthetical
    s = re.sub(r"\([^)]*\)", "", s)
    # collapse whitespace and punctuation
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def normalize_country(c: str) -> str:
    c = (c or "").strip().upper()
    # map a couple of common variants to ISO alpha-2
    mapping = {
        "UK": "GB", "UNITED KINGDOM": "GB",
        "UNITED STATES": "US",
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
        "LITHUANIA": "LT",
        "LUXEMBOURG": "LU",
        "NORWAY": "NO",
        "PORTUGAL": "PT",
        "FINLAND": "FI",
    }
    return mapping.get(c, c[:2] if len(c) >= 2 else c)


def row_quality_score(row: dict) -> int:
    """Higher = better row to keep when merging duplicates."""
    score = 0
    conf = (row.get("confidence") or row.get("data_confidence") or "").lower()
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
    notes_len = len(row.get("notes") or "")
    score += min(notes_len // 20, 5)
    return score


def read_shard(path: Path) -> list[dict]:
    """Read a shard, normalize to MASTER_HEADERS schema."""
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # Map seed's data_confidence → confidence
            if "data_confidence" in r and "confidence" not in r:
                r["confidence"] = r.pop("data_confidence")
            # Normalize missing fields
            for h in MASTER_HEADERS:
                r.setdefault(h, "")
            # Strip source_url for seed (not in seed schema)
            if "source_url" not in r or r["source_url"] is None:
                r["source_url"] = r.get("source_url") or ""
            r["company"] = (r.get("company") or "").strip()
            r["country"] = normalize_country(r.get("country") or "")
            r["website"] = (r.get("website") or "").strip().rstrip("/")
            r["email"] = (r.get("email") or "").strip().lower()
            # fix "role" → "generic" (agent3 used "role")
            if r.get("email_type") == "role":
                r["email_type"] = "generic"
            rows.append(r)
    return rows


def main():
    all_rows: list[dict] = []
    for shard in SHARDS:
        if not shard.exists():
            print(f"MISSING SHARD: {shard}", file=sys.stderr)
            continue
        shard_rows = read_shard(shard)
        print(f"{shard.name}: {len(shard_rows)} rows")
        all_rows.extend(shard_rows)

    # Dedup: group by normalized name, keep best row, merge a few fields
    groups: dict[str, list[dict]] = {}
    for r in all_rows:
        key = normalize_name(r["company"])
        if not key:
            continue
        groups.setdefault(key, []).append(r)

    merged: list[dict] = []
    for key, group in groups.items():
        group.sort(key=row_quality_score, reverse=True)
        best = dict(group[0])
        # Merge complementary fields from lower-ranked rows
        for r in group[1:]:
            for field in ("email", "website", "sub_domain", "notes", "source_url"):
                if not best.get(field) and r.get(field):
                    best[field] = r[field]
            # Prefer "generic" email_type if any row has one
            if best.get("email_type") != "generic" and r.get("email_type") == "generic":
                best["email_type"] = "generic"
            # Prefer decisive SME flag over "unknown"
            if best.get("sme_likely") == "unknown" and r.get("sme_likely") in ("Yes", "No"):
                best["sme_likely"] = r["sme_likely"]
            # Track merge count
        # Flag merged companies
        if len(group) > 1:
            base_notes = best.get("notes") or ""
            merge_tag = f" [cross-sourced x{len(group)}]"
            if merge_tag not in base_notes:
                best["notes"] = (base_notes + merge_tag).strip()
        merged.append(best)

    # Sort by country, sub_domain, company
    merged.sort(key=lambda r: (r["country"], r["sub_domain"].lower(), r["company"].lower()))

    # Write master
    with open(OUT_MASTER, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=MASTER_HEADERS)
        w.writeheader()
        for r in merged:
            w.writerow({h: r.get(h, "") for h in MASTER_HEADERS})

    # Write "needs email enrichment" shortlist: companies with website but no email
    needs_email = [
        r for r in merged
        if r.get("website") and not r.get("email")
        and r.get("sme_likely") != "No"  # skip scale-ups
    ]
    with open(OUT_NEEDS_EMAIL, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["company", "country", "website", "sme_likely"])
        w.writeheader()
        for r in needs_email:
            w.writerow({
                "company": r["company"],
                "country": r["country"],
                "website": r["website"],
                "sme_likely": r.get("sme_likely", ""),
            })

    # Summary
    total = len(merged)
    with_email = sum(1 for r in merged if r.get("email"))
    sme_yes = sum(1 for r in merged if r.get("sme_likely") == "Yes")
    sme_no = sum(1 for r in merged if r.get("sme_likely") == "No")
    sme_unknown = sum(1 for r in merged if r.get("sme_likely") not in ("Yes", "No"))
    countries = sorted({r["country"] for r in merged if r["country"]})
    print()
    print(f"MASTER: {total} unique companies")
    print(f"  with email: {with_email}")
    print(f"  SME likely Yes: {sme_yes}  No: {sme_no}  unknown: {sme_unknown}")
    print(f"  countries: {', '.join(countries)}")
    print(f"  needs email enrichment: {len(needs_email)}")
    print(f"  duplicates merged: {len(all_rows) - total}")


if __name__ == "__main__":
    main()
