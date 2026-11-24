#!/usr/bin/env python3
"""Static checks for one episode (no rendering).

usage: python tools/check_episode.py EPISODE

- narration.json parses; every beat has id/seconds/en/zh; ids unique
- every scene in narration.json is a class in scenes.py and every beat id is used exactly once, in order
- scene names are unique across all episodes
- prints total narration length and every cite(...) string (for the source audit)
"""
import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    ep = sys.argv[1]
    d = ROOT / "episodes" / ep
    narr = json.loads((d / "narration.json").read_text(encoding="utf-8"))
    src = (d / "scenes.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    classes = {n.name: n for n in tree.body if isinstance(n, ast.ClassDef)}
    errors = []
    ids = set()
    total = 0.0
    for scene, beats in narr["scenes"].items():
        if scene not in classes:
            errors.append(f"scene {scene} missing in scenes.py")
            continue
        body = ast.get_source_segment(src, classes[scene]) or ""
        used = re.findall(r'self\.beat\(\s*"([^"]+)"', body)
        want = [b["id"] for b in beats]
        if used != want:
            errors.append(f"{scene}: beats used {used} != narration {want}")
        for b in beats:
            for k in ("id", "seconds", "en", "zh"):
                if k not in b or b[k] in ("", None):
                    errors.append(f"{scene}/{b.get('id')}: missing {k}")
            if b["id"] in ids:
                errors.append(f"duplicate beat id {b['id']}")
            ids.add(b["id"])
            total += float(b.get("seconds", 0))
    # scene name uniqueness across episodes
    for other in (ROOT / "episodes").iterdir():
        if other.name == ep or not (other / "narration.json").exists():
            continue
        o = json.loads((other / "narration.json").read_text(encoding="utf-8"))
        clash = set(o["scenes"]) & set(narr["scenes"])
        if clash:
            errors.append(f"scene names also used in {other.name}: {sorted(clash)}")
    cites = re.findall(r'cite\(\s*(?:f?"([^"]*)"|f?\'([^\']*)\')', src)
    print(f"{ep}: {len(narr['scenes'])} scenes, {len(ids)} beats, narration ~{total / 60:.1f} min")
    print("citations on screen:")
    for a, b in cites:
        print("  -", a or b)
    if errors:
        print("ERRORS:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
