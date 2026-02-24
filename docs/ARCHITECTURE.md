# Architecture Overview

This project is structured to support a reproducible research workflow:

- `scripts/` : Python utilities to query arXiv, enrich metadata, and package handoff bundles
- `latex/` : LaTeX paper sources and bibliography
- `docs/` : process notes, feedback templates, and experiment planning
- `outputs/` : generated CSV/BibTeX and enriched metadata (gitignored)

Flow:
1. Add raw ideas to `docs/raw_ideas.md`.
2. Run `scripts/arxiv_search.py` to get `outputs/arxiv_results.csv` and `outputs/arxiv_results.bib`.
3. Run `scripts/enrich_metadata.py` to add DOI/venue using Crossref.
4. Iterate on `latex/main.tex` and use `scripts/generate_handoff.py` to create a bundle for the writer.
