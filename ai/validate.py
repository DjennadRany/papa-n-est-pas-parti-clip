"""Fail loudly if footage is missing; never silently render a slideshow."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
data=json.loads((root/"scenes.json").read_text(encoding="utf-8"))
scenes=data["scenes"]
missing=[]
for s in scenes:
    p=root/"public/assets/video"/f'{s["id"]:02d}.mp4'
    if not p.is_file() or p.stat().st_size<10000: missing.append(s["id"])
audio=root/"public/assets/audio/Papa n'est pas parti(1).mp3"
if not audio.is_file(): raise SystemExit(f"Audio missing: {audio}")
if missing: raise SystemExit(f"Missing {len(missing)} video shots: {', '.join(map(str,missing))}. Upload clips or generate them before rendering.")
print(f"Ready: {len(scenes)} video clips and original audio.")
