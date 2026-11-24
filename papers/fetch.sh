#!/usr/bin/env bash
# Download the three papers (not committed; arXiv versions as of 2026-11-23).
cd "$(dirname "$0")"
curl -sL -o exverus.pdf   https://arxiv.org/pdf/2603.25810   # ExVerus (ICML 2026)
curl -sL -o topoverus.pdf https://arxiv.org/pdf/2611.13627   # TopoVerus (NeurIPS 2026)
curl -sL -o vero.pdf      https://arxiv.org/pdf/2608.13522   # Vero (2026)
ls -la *.pdf
