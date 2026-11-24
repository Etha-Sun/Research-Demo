#!/usr/bin/env python3
"""Set every beat's `seconds` in narration.json to the length of its voice clip plus padding.

usage: python tools/sync_durations.py EPISODE [--lang en] [--pad 0.6] [--min 2.0]

Run after tools/tts.py and before rendering, so that animations and voice line up. Beats without a clip keep
their current value. The video is timed to one language; the other language is shown as subtitles.
"""
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1",
                          str(path)], capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--pad", type=float, default=0.6)
    ap.add_argument("--min", type=float, default=2.0)
    a = ap.parse_args()
    path = ROOT / "episodes" / a.episode / "narration.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = 0
    for scene, bs in data["scenes"].items():
        for b in bs:
            clip = ROOT / "audio" / a.episode / a.lang / f"{b['id']}.wav"
            if clip.exists():
                new = round(max(a.min, duration(clip) + a.pad), 2)
                if abs(new - float(b.get("seconds", 0))) > 0.01:
                    b["seconds"] = new
                    changed += 1
    data["timed_to"] = a.lang
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    total = sum(float(b["seconds"]) for bs in data["scenes"].values() for b in bs)
    print(f"{a.episode}: {changed} beat(s) updated; narration total {total / 60:.1f} min")


if __name__ == "__main__":
    main()
