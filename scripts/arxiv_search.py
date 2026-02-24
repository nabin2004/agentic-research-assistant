#!/usr/bin/env python3
"""Query arXiv and store metadata as CSV and BibTeX.

Usage: python scripts/arxiv_search.py --query "machine learning" --max 50
"""
import argparse
import arxiv
import csv
import os
import bibtexparser


def search_arxiv(query, max_results=50, out_dir="outputs"):
    os.makedirs(out_dir, exist_ok=True)
    search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)
    rows = []
    bib_entries = []
    for result in search.results():
        meta = {
            "title": result.title,
            "authors": "; ".join([a.name for a in result.authors]),
            "published": result.published.strftime("%Y-%m-%d"),
            "id": result.entry_id,
            "pdf_url": result.pdf_url,
            "summary": result.summary.replace("\n", " ")[:1000],
        }
        rows.append(meta)
        # create minimal bibtex entry
        bib_entries.append({
            'ENTRYTYPE': 'article',
            'ID': result.get_short_id(),
            'title': result.title,
            'author': ' and '.join([a.name for a in result.authors]),
            'year': str(result.published.year),
            'eprint': result.get_short_id(),
            'archivePrefix': 'arXiv',
        })

    csv_path = os.path.join(out_dir, "arxiv_results.csv")
    with open(csv_path, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "title", "authors", "published", "pdf_url", "summary"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    bib_db = bibtexparser.bibdatabase.BibDatabase()
    bib_db.entries = bib_entries
    bib_path = os.path.join(out_dir, "arxiv_results.bib")
    with open(bib_path, "w", encoding='utf-8') as f:
        f.write(bibtexparser.dumps(bib_db))

    print(f"Wrote {len(rows)} results to {csv_path} and {bib_path}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--query", required=True)
    p.add_argument("--max", type=int, default=50)
    p.add_argument("--out", default="outputs")
    args = p.parse_args()
    search_arxiv(args.query, max_results=args.max, out_dir=args.out)


if __name__ == "__main__":
    main()
