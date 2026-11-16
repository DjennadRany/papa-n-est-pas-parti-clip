"""Production controller: reusable, resumable, fail-closed video generation.
Uses existing Wan Gradio provider. Additional providers can be added via adapters.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCENES=json.loads((ROOT/"scenes.json").read_text(encoding="utf8"))["scenes"]
VIDEO=ROOT/"public/assets/video"
VIDEO.mkdir(parents=True,exist_ok=True)

def valid(path):
    if not path.exists() or path.stat().st_size<10000:
        return False
    with path.open("rb") as f:
        return b"ftyp" in f.read(64)

def missing():
    return [s for s in SCENES if not valid(VIDEO/f'{s["id"]:02d}.mp4')]

def generate(max_new):
    created=0
    for scene in missing():
        if created>=max_new:break
        sid=scene["id"]
        dest=VIDEO/f"{sid:02d}.mp4"
        print(f"START scene {sid:02d}: {scene['title']}",flush=True)
        proc=subprocess.run([sys.executable,str(ROOT/"ai/generate.py"),"--scene",str(sid),"--duration","3.5"],check=False)
        if proc.returncode==75:
            print("QUOTA_EXHAUSTED; preserved all previously generated shots",flush=True)
            return 0
        if proc.returncode or not valid(dest):
            print(f"SCENE_FAILED {sid:02d}; stop without discarding progress",flush=True)
            return 0
        created+=1
    print(f"New shots: {created}; total: {len(SCENES)-len(missing())}/{len(SCENES)}",flush=True)
    return 0

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("command",choices=["generate","status","validate"])
    parser.add_argument("--max-new",type=int,default=2)
    args=parser.parse_args()
    if args.command=="generate":
        if args.max_new<0:parser.error("--max-new must be nonnegative")
        return generate(args.max_new)
    remaining=missing()
    print(json.dumps({"total":len(SCENES),"ready":len(SCENES)-len(remaining),
      "missing":[s["id"] for s in remaining]},ensure_ascii=False))
    if args.command=="validate" and remaining:
        return 1
    return 0

if __name__=="__main__":raise SystemExit(main())
