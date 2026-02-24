#!/usr/bin/env python3
"""Prepare an arXiv submission package.

Creates `arXiv_submission.zip` containing LaTeX sources, bibliography, figures,
and a short README with build instructions. Optionally includes compiled PDF.
"""
import argparse
import os
import zipfile
from pathlib import Path


def collect_sources(latex_dir='latex'):
    p = Path(latex_dir)
    patterns = ['*.tex', '*.bib', '*.sty', '*.cls', '*.bst', 'images/*', 'figures/*']
    files = set()
    for pat in patterns:
        for f in p.glob(pat):
            if f.is_file():
                files.add(f)
    # also include any files in latex root
    for f in p.iterdir():
        if f.is_file() and f.suffix in ['.tex', '.bib']:
            files.add(f)
    return sorted(files)


def make_readme(latex_dir='latex'):
    return ("This archive contains the LaTeX sources for submission to arXiv.\n"
            "Build steps (on a system with TeX installed):\n"
            "1. cd latex\n"
            "2. sh ../scripts/build_paper.sh\n"
            "If compilation fails, ensure all packages are available or include them in the archive.\n")


def create_package(out='arXiv_submission.zip', include_pdf=False):
    files = collect_sources()
    with zipfile.ZipFile(out, 'w') as z:
        for f in files:
            arcname = os.path.join('source', os.path.relpath(f, 'latex'))
            z.write(f, arcname)
        # add README
        readme = make_readme()
        z.writestr('source/README_arXiv.txt', readme)
        # optional: add compiled PDF if exists
        pdf_path = Path('latex') / 'main.pdf'
        if include_pdf and pdf_path.exists():
            z.write(pdf_path, 'main.pdf')
    print(f'Wrote {out} with {len(files)} source files')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', default='arXiv_submission.zip')
    p.add_argument('--pdf', action='store_true', help='Include compiled PDF if present')
    args = p.parse_args()
    create_package(out=args.out, include_pdf=args.pdf)


if __name__ == '__main__':
    main()
