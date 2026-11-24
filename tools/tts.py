#!/usr/bin/env python3
"""Generate one voice clip per narration beat.

usage: python tools/tts.py EPISODE [--lang en|zh] [--engine kokoro|say|none] [--voice NAME] [--speed 1.0]

Writes audio/<episode>/<lang>/<beat-id>.wav (24 kHz mono). Existing clips whose text did not change are kept
(a sidecar .txt stores the text that produced each clip).

Engines
  kokoro  local neural TTS, no API key (pip install kokoro soundfile; zh also needs `misaki[zh]`).
          Default voices: en "af_heart", zh "zf_xiaobei".
  say     macOS built-in `say` (+ ffmpeg to convert); default voices: en "Samantha", zh "Tingting".
  none    silent clips of the beat's current `seconds` (layout / timing previews without a voice).
"""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_VOICE = {("kokoro", "en"): "af_heart", ("kokoro", "zh"): "zf_xiaobei",
                 ("say", "en"): "Samantha", ("say", "zh"): "Tingting"}


def beats(episode):
    data = json.loads((ROOT / "episodes" / episode / "narration.json").read_text(encoding="utf-8"))
    for scene, bs in data["scenes"].items():
        for b in bs:
            yield scene, b


def synth_kokoro(items, lang, voice, speed, out_dir):
    try:
        from kokoro import KPipeline
        import soundfile as sf
    except ImportError:
        sys.exit("kokoro not installed: pip install kokoro soundfile  (zh: pip install 'misaki[zh]')")
    pipe = KPipeline(lang_code="a" if lang == "en" else "z")
    import numpy as np
    for beat_id, text in items:
        chunks = [audio for _, _, audio in pipe(text, voice=voice, speed=speed)]
        sf.write(out_dir / f"{beat_id}.wav", np.concatenate(chunks), 24000)
        print("  wrote", beat_id)


def synth_say(items, lang, voice, speed, out_dir):
    if not shutil.which("say"):
        sys.exit("`say` is only available on macOS")
    rate = str(int(175 * speed))
    for beat_id, text in items:
        with tempfile.TemporaryDirectory() as tmp:
            aiff = Path(tmp) / "a.aiff"
            subprocess.run(["say", "-v", voice, "-r", rate, "-o", str(aiff), text], check=True)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(aiff), "-ar", "24000", "-ac", "1",
                            str(out_dir / f"{beat_id}.wav")], check=True)
        print("  wrote", beat_id)


def synth_none(items_with_seconds, out_dir):
    for beat_id, seconds in items_with_seconds:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                        "-t", f"{max(0.5, seconds - 0.4):.2f}", str(out_dir / f"{beat_id}.wav")], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--lang", default="en", choices=["en", "zh"])
    ap.add_argument("--engine", default="kokoro", choices=["kokoro", "say", "none"])
    ap.add_argument("--voice")
    ap.add_argument("--speed", type=float, default=1.0)
    a = ap.parse_args()
    out_dir = ROOT / "audio" / a.episode / a.lang
    out_dir.mkdir(parents=True, exist_ok=True)
    todo, silent = [], []
    for _, b in beats(a.episode):
        text = b[a.lang].strip()
        side = out_dir / f"{b['id']}.txt"
        if (out_dir / f"{b['id']}.wav").exists() and side.exists() and side.read_text(encoding="utf-8") == text:
            continue
        side.write_text(text, encoding="utf-8")
        todo.append((b["id"], text))
        silent.append((b["id"], float(b.get("seconds", 3))))
    print(f"{a.episode}/{a.lang}: {len(todo)} clip(s) to synthesise with {a.engine}")
    if not todo:
        return
    voice = a.voice or DEFAULT_VOICE.get((a.engine, a.lang))
    if a.engine == "kokoro":
        synth_kokoro(todo, a.lang, voice, a.speed, out_dir)
    elif a.engine == "say":
        synth_say(todo, a.lang, voice, a.speed, out_dir)
    else:
        synth_none(silent, out_dir)


if __name__ == "__main__":
    main()
