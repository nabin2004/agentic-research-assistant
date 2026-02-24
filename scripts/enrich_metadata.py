#!/usr/bin/env python3
"""Enrich arXiv CSV with Crossref metadata (DOI, venue, publisher).

Usage: python scripts/enrich_metadata.py --csv outputs/arxiv_results.csv
"""
import argparse
import csv
import requests
import time
import os


def query_crossref_title(title):
    url = "https://api.crossref.org/works"
    params = {"query.title": title, "rows": 1}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    if data.get("message", {}).get("items"):
        return data["message"]["items"][0]
    return None


def enrich(csv_path, out_dir="outputs"):
    os.makedirs(out_dir, exist_ok=True)
    rows = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    enriched = []
    for r in rows:
        title = r.get("title", "")
        try:
            item = query_crossref_title(title)
        except Exception:
            item = None
        if item:
            doi = item.get("DOI")
            container = ", ".join(item.get("container-title", []))
            publisher = item.get("publisher")
        else:
            doi = None
            container = None
            publisher = None

        r2 = dict(r)
        r2.update({"doi": doi, "venue": container, "publisher": publisher})
        enriched.append(r2)
        time.sleep(1.0)

    out_csv = os.path.join(out_dir, "arxiv_results.enriched.csv")
    with open(out_csv, "w", newline='', encoding='utf-8') as f:
        fieldnames = list(enriched[0].keys()) if enriched else []
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in enriched:
            writer.writerow(row)

    print(f"Wrote enriched metadata to {out_csv}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True)
    p.add_argument("--out", default="outputs")
    args = p.parse_args()
    enrich(args.csv, out_dir=args.out)


if __name__ == "__main__":
    main()
