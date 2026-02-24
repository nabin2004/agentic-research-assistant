# Publishing and arXiv Submission Guide

This document describes how to build the paper locally and prepare an arXiv submission package.

Local build (requires TeX distribution with pdflatex and bibtex):

```bash
python -m pip install -r requirements.txt
./scripts/build_paper.sh
# PDF will be at latex/main.pdf
```

If you prefer `latexmk` you can replace the commands with `latexmk -pdf main.tex`.

Preparing an arXiv package:

```bash
# create source-only zip for arXiv
python scripts/prepare_arxiv.py --out arXiv_submission.zip
# optionally include PDF inside the zip
python scripts/prepare_arxiv.py --out arXiv_submission_with_pdf.zip --pdf
```

Notes for submission:
- Use the arXiv web interface to upload `arXiv_submission.zip`.
- Provide the title and abstract during submission (you can copy from `latex/main.tex`).
- Add categories and related comments as needed.

Automating via GitHub Actions:
- The CI workflow builds a small test run and can upload the resulting PDF as an artifact.
