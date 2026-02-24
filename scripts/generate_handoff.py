#!/usr/bin/env python3
"""Package the paper draft and relevant files for the writer.

Creates `hand_off.zip` containing LaTeX sources, README, feedback template and enriched metadata if present.
"""
import argparse
import zipfile
import os


def make_handoff(root='.', out='hand_off.zip'):
    include = [
        'latex/main.tex',
        'latex/references.bib',
        'README.md',
        'docs/FEEDBACK_TEMPLATE.md',
        'docs/raw_ideas.md',
        'docs/PROCESS.md',
    ]
    # include enriched metadata if present
    if os.path.exists('outputs/arxiv_results.enriched.csv'):
        include.append('outputs/arxiv_results.enriched.csv')
    elif os.path.exists('outputs/arxiv_results.csv'):
        include.append('outputs/arxiv_results.csv')

    with zipfile.ZipFile(out, 'w') as z:
        for p in include:
            if os.path.exists(p):
                z.write(p)
    print(f'Wrote {out}')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', default='hand_off.zip')
    args = p.parse_args()
    make_handoff(out=args.out)


if __name__ == '__main__':
    main()
