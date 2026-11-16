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
    image=ROOT / "public" / scene["image"]
    if not image.is_file(): raise SystemExit(f"Missing image: {image}")
    output=OUT / f"{args.scene:02d}.mp4"
    if output.exists() and output.stat().st_size>1000:
        print(f"Already generated: {output}")
        return
    prompt=MOTIONS.get(args.scene,DEFAULT)
    print(f"Submitting scene {args.scene} to {SPACE}; public GPU may be unavailable.",flush=True)
    client=Client(SPACE)
    result=client.predict(input_image=handle_file(str(image)),prompt=prompt,steps=6,
      duration_seconds=min(args.duration,4.0),guidance_scale=1,guidance_scale_2=1,
      seed=42+args.scene,randomize_seed=False,api_name="/generate_video")
    source=result[0] if isinstance(result,(tuple,list)) else result
    if isinstance(source,dict): source=source.get("video") or source.get("path")
    if not source or not Path(source).exists(): raise RuntimeError(f"No local MP4 from provider: {result}")
    shutil.copyfile(source,output)
    if output.stat().st_size<1000: raise RuntimeError("Output MP4 is empty")
    print(f"GENERATED {output} ({output.stat().st_size} bytes)",flush=True)

if __name__=="__main__":main()
