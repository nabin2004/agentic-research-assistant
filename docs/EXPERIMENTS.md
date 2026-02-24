# Experiments and Planning

Use this file to outline experiments and reproducible steps.

Example experiment:

- Goal: Evaluate topical overlap between arXiv preprints and published proceedings in 2024.
- Data: `outputs/arxiv_results.enriched.csv` (use `--max 200`)
- Steps:
  1. Run `python scripts/arxiv_search.py --query "topic" --max 200`.
  2. Enrich with `python scripts/enrich_metadata.py --csv outputs/arxiv_results.csv`.
  3. Inspect `venue` and `publisher` fields; sample manually for accuracy.

Record results, plots and decisions here.
