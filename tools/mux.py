#!/usr/bin/env python3
"""Assemble one episode: concatenate the rendered scenes, lay the voice clips at the beat start times recorded by
NarratedScene, and write subtitles.

usage: python tools/mux.py EPISODE [--quality h|m|l] [--lang en] [--subs en|zh|both|none] [--burn]

Inputs : media/videos/scenes/<res>/<Scene>.mp4 (from render.sh), media/timeline/<Scene>.json,
         audio/<episode>/<lang>/<beat>.wav
Outputs: out/<episode>.mp4 and out/<episode>.<lang>.srt (soft subtitles; --burn draws them into the picture)
Scene order is the order of the "scenes" object in narration.json.
"""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = {"l": "480p15", "m": "720p30", "h": "1080p60", "k": "2160p60"}


def srt_time(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--quality", default="h", choices=list(RES))
    ap.add_argument("--lang", default="en")
    ap.add_argument("--subs", default="both", choices=["en", "zh", "both", "none"])
    ap.add_argument("--burn", action="store_true", help="burn the first subtitle language into the video")
    a = ap.parse_args()

    ep = a.episode
    narr = json.loads((ROOT / "episodes" / ep / "narration.json").read_text(encoding="utf-8"))
    scenes = list(narr["scenes"])
    vid_dir = ROOT / "media" / "videos" / "scenes" / RES[a.quality]
    out = ROOT / "out"
    out.mkdir(exist_ok=True)

    offset, placed, cues = 0.0, [], {"en": [], "zh": []}
    files = []
    for sc in scenes:
        mp4 = vid_dir / f"{sc}.mp4"
        if not mp4.exists():
            raise SystemExit(f"missing {mp4}: run ./render.sh {ep} first")
        files.append(mp4)
        tl = json.loads((ROOT / "media" / "timeline" / f"{sc}.json").read_text(encoding="utf-8"))
        for b in tl["beats"]:
            clip = ROOT / "audio" / ep / a.lang / f"{b['id']}.wav"
            if clip.exists():
                placed.append((offset + b["start"], clip))
            for lang in ("en", "zh"):
                if b.get(lang):
                    cues[lang].append((offset + b["start"], offset + b["end"] - 0.05, b[lang]))
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                    "default=nw=1:nk=1", str(mp4)], capture_output=True, text=True).stdout)
        offset += dur

    langs = {"both": ["en", "zh"], "none": []}.get(a.subs, [a.subs])
    for lang in langs:
        with open(out / f"{ep}.{lang}.srt", "w", encoding="utf-8") as f:
            for i, (s, e, text) in enumerate(cues[lang], 1):
                f.write(f"{i}\n{srt_time(s)} --> {srt_time(e)}\n{text}\n\n")

    with tempfile.TemporaryDirectory() as tmp:
        lst = Path(tmp) / "list.txt"
        lst.write_text("".join(f"file '{p}'\n" for p in files))
        silent = Path(tmp) / "video.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                        "-c", "copy", str(silent)], check=True)
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(silent)]
        for _, clip in placed:
            cmd += ["-i", str(clip)]
        if placed:
            delays = "".join(f"[{i + 1}:a]adelay={int(t * 1000)}:all=1[a{i}];" for i, (t, _) in enumerate(placed))
            mix = "".join(f"[a{i}]" for i in range(len(placed))) + \
                f"amix=inputs={len(placed)}:normalize=0,apad[aout]"
            vf = []
            if a.burn and langs:
                vf = [f"[0:v]subtitles={out / f'{ep}.{langs[0]}.srt'}[vout]"]
            fc = delays + mix + (";" + vf[0] if vf else "")
            cmd += ["-filter_complex", fc, "-map", "[vout]" if vf else "0:v", "-map", "[aout]", "-shortest",
                    "-c:v", "libx264" if vf else "copy", "-c:a", "aac", "-b:a", "192k"]
        else:
            cmd += ["-c", "copy"]
        cmd.append(str(out / f"{ep}.mp4"))
        subprocess.run(cmd, check=True)
    print(f"wrote out/{ep}.mp4 ({offset / 60:.1f} min) and subtitles {langs}")


if __name__ == "__main__":
    main()
