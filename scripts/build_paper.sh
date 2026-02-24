#!/usr/bin/env bash
set -euo pipefail
# Builds the LaTeX paper (pdflatex + bibtex) and places PDF in `latex/`
cd "$(dirname "$0")/../latex"
TEXFILE=main.tex
OUTDIR=.

echo "Running pdflatex (1)..."
pdflatex -interaction=nonstopmode -halt-on-error "$TEXFILE"
if [ -f main.aux ]; then
  echo "Running bibtex..."
  bibtex main || true
fi
echo "Running pdflatex (2)..."
pdflatex -interaction=nonstopmode -halt-on-error "$TEXFILE"
echo "Running pdflatex (3)..."
pdflatex -interaction=nonstopmode -halt-on-error "$TEXFILE"

echo "Build complete: $(pwd)/main.pdf"
