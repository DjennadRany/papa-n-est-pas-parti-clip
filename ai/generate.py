"""Generate genuine AI motion clips with a public Wan 2.2 Hugging Face Space.
No fake Ken Burns animation. This requires upstream free GPU availability.
Run: python ai/generate.py --scene 1
"""
import argparse
import json
import os
import shutil
import sys
import time
import subprocess
from pathlib import Path
from gradio_client import Client, handle_file

ROOT = Path(__file__).resolve().parents[1]
TIMELINE = json.loads((ROOT / "scenes.json").read_text(encoding="utf-8"))
SPACE = os.getenv("WAN_SPACE", "zerogpu-aoti/wan2-2-fp8da-aoti-faster")
OUT = ROOT / "public" / "assets" / "video"
OUT.mkdir(parents=True, exist_ok=True)

MOTIONS = {
  1: "A father slowly walks toward the empty second cushion, stops and lowers his head, hands moving naturally, expressive character acting, cinematic Japanese fantasy 3D animation, warm hand-painted environment, continuous fluid full-body motion, no text",
  17: "A colossal fantasy dragon attacks the bridge, the father dodges and rolls to safety, strong cinematic action, believable full-body motion, expressive stylized 3D animation, no text",
  18: "A huge dragon claw strikes the bridge rails, wood splinters and the hero jumps back, dynamic camera follows action, stylized fantasy 3D film animation, no text",
  19: "The father uses his staff as a lever to protect the bridge, he plants his feet and pushes with effort, dramatic cinematic motion, stylized fantasy 3D animation, no text",
  24: "Two small lamps glow across a magical bridge at night, a breeze gently moves the grass, warm cinematic fantasy animation, no text",
}
DEFAULT = "The characters perform subtle natural physical actions, eyes blink, hands and bodies move expressively, hair and clothing react to wind, cinematic 3D Japanese fantasy animation with painterly backgrounds, continuous coherent movement, no subtitles, no text, no slideshow, no still image."

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--scene",type=int,required=True,help="Original scene ID 1-48")
    p.add_argument("--duration",type=float,default=3.5)
    args=p.parse_args()
    scene=next((s for s in TIMELINE["scenes"] if s["id"]==args.scene),None)
    if scene is None: raise SystemExit(f"Unknown scene {args.scene}")
    # All transition sources 25–48 have filename labels baked in.
    # Use prepared/inpainted source exclusively; NEVER reintroduce watermarks.
    image=(ROOT / "public/assets/prepared" / f"{args.scene:02d}.jpg"
           if args.scene >= 25 else ROOT / "public" / scene["image"])
    if not image.is_file():
        raise SystemExit(f"Missing prepared illustration: {image}. Run python ai/prepare_images.py first.")
    output=OUT / f"{args.scene:02d}.mp4"
    if output.exists() and output.stat().st_size>10000:
        with output.open("rb") as existing:
            if b"ftyp" in existing.read(64):
                print(f"Already generated: {output}")
                return
    # Derive scene-specific action and visual continuity instead of 43 identical prompts.
    ordered=sorted(TIMELINE["scenes"],key=lambda item:item["start"])
    idx=next(i for i,item in enumerate(ordered) if item["id"]==args.scene)
    before=ordered[idx-1]["title"] if idx else "opening"
    after=ordered[idx+1]["title"] if idx+1<len(ordered) else "ending"
    context=(f"Scene: {scene['title']}. Previous scene: {before}. "
             f"Next scene: {after}. Show a clear character action motivated by this scene, "
             "with natural articulated movement and expressive acting, coherent cinematic "
             "continuity, hand-painted fantasy backgrounds and stylized 3D characters, "
             "a warm poetic Japanese animated feature aesthetic. No text, no subtitles. ")
    prompt=context+MOTIONS.get(args.scene,DEFAULT)
    plan_path=ROOT/"ai"/"scene_prompts.json"
    if plan_path.exists():
        custom=json.loads(plan_path.read_text(encoding="utf-8"))
        prompt=context+custom.get(str(args.scene),MOTIONS.get(args.scene,DEFAULT))
    print(f"Submitting scene {args.scene} to {SPACE}; public GPU may be unavailable.",flush=True)
    try:
        client=Client(SPACE)
        result=client.predict(input_image=handle_file(str(image)),prompt=prompt,steps=6,
      duration_seconds=min(args.duration,4.0),guidance_scale=1,guidance_scale_2=1,
          seed=42+args.scene,randomize_seed=False,api_name="/generate_video")
    except Exception as e:
        if any(term in str(e).lower() for term in ["zerogpu runs limit","exceeded your zerogpu","quota exceeded","rate limit exceeded"]):
            print("QUOTA_EXHAUSTED: Stop and save footage; never retry same quota.",flush=True)
            raise SystemExit(75)
        raise
    source=result[0] if isinstance(result,(tuple,list)) else result
    if isinstance(source,dict): source=source.get("video") or source.get("path")
    if not source or not Path(source).exists(): raise RuntimeError(f"No local MP4 from provider: {result}")
    temporary=output.with_suffix(".partial.mp4")
    try:
        shutil.copyfile(source,temporary)
        if temporary.stat().st_size<10000: raise RuntimeError("Output MP4 is empty")
        with temporary.open("rb") as generated:
            if b"ftyp" not in generated.read(64): raise RuntimeError("Provider did not return an MP4")
        os.replace(temporary,output)
    finally:
        temporary.unlink(missing_ok=True)
    print(f"GENERATED {output} ({output.stat().st_size} bytes)",flush=True)

if __name__=="__main__":main()
