#!/usr/bin/env bash
# Render one episode (or all) end to end on a local machine.
#
#   ./render.sh EPISODE [quality] [engine] [lang]
#     EPISODE  exverus | topoverus | vero | vekto | all
#     quality  l (480p preview, fast) | m (720p) | h (1080p60, default) | k (4K)
#     engine   kokoro (default) | say (macOS) | none (silent preview)
#     lang     en (default, voice language; the other language becomes subtitles) | zh
#
# Steps: voice clips -> beat durations -> manim scenes -> mux (voice + subtitles).
set -euo pipefail
cd "$(dirname "$0")"
EP=${1:?episode}; Q=${2:-h}; ENGINE=${3:-kokoro}; LANG_=${4:-en}
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"
PY=${PYTHON:-python3}

if [ "$EP" = all ]; then
  for e in exverus topoverus vero vekto; do "$0" "$e" "$Q" "$ENGINE" "$LANG_"; done
  exit 0
fi

"$PY" tools/tts.py "$EP" --engine "$ENGINE" --lang "$LANG_"
if [ "$ENGINE" != none ]; then "$PY" tools/sync_durations.py "$EP" --lang "$LANG_"; fi

SCENES=$("$PY" -c "import json,sys; print(' '.join(json.load(open('episodes/$EP/narration.json',encoding='utf-8'))['scenes']))")
# all scenes of one file in one manim call; output name = scene name
manim -q"$Q" --media_dir media episodes/"$EP"/scenes.py $SCENES
# manim writes to media/videos/scenes/<res>/ because every episode module is called scenes.py
"$PY" tools/mux.py "$EP" --quality "$Q" --lang "$LANG_"
