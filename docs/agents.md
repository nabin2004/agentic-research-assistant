# Agents and Automation Guide

This document lists lightweight agent patterns, prompt templates, and safe automation steps you can use to run parts of the research pipeline autonomously.

1) Roles

- Research Assistant Agent: collects raw ideas, expands into title/abstract drafts, and maintains `docs/raw_ideas.md`.
- Literature Miner Agent: runs `scripts/arxiv_search.py`, filters results, and stores CSV/BibTeX in `outputs/`.
- Metadata Enricher Agent: runs `scripts/enrich_metadata.py` to add DOI/venue/publisher information.
- Paper Builder Agent: builds the LaTeX paper using `scripts/build_paper.sh` and prepares the arXiv package with `scripts/prepare_arxiv.py`.
- Handoff Agent: creates `hand_off.zip` via `scripts/generate_handoff.py` and notifies the writer.

2) Safe automation checklist

- Always keep outputs under `outputs/` (gitignored) and commit only curated files.
- Require human approval before publishing or submitting to arXiv.
- Log agent actions to `logs/` (create if needed) and include timestamps.

3) Example prompt templates

- Title + abstract request to writer:

  "I've collected these raw ideas: <paste>. Please propose 3 concise titles and a 150-word abstract focused on the main contribution. Mark any unclear claims."

- Ask Literature Miner to shortlist papers:

  "Search arXiv for '<query>' and return top 30 results sorted by relevance. For each result output: title, authors, date, arXiv id, and top 2 keywords."

4) Automation commands (examples)

```bash
# Run literature search and enrich metadata
python scripts/arxiv_search.py --query "self-supervised learning 2024" --max 100 --out outputs
python scripts/enrich_metadata.py --csv outputs/arxiv_results.csv --out outputs

# Build paper and prepare arXiv package
./scripts/build_paper.sh
python scripts/prepare_arxiv.py --out arXiv_submission.zip --pdf

# Create handoff bundle
python scripts/generate_handoff.py --out hand_off.zip
```

5) Next steps

- If you want, configure an agent runner (cron, GitHub Actions workflow, or a small service) to execute safe steps and write logs; ensure explicit checks before publishing.
