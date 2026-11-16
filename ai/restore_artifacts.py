"""Recover all previously generated AI shots from GitHub Actions artifacts.

Only MP4s from public/assets/video/NN.mp4 are accepted. Newest artifact wins.
Uses GITHUB_TOKEN in Actions, avoiding binary commits and re-generations.
"""
import io
import json
import os
import re
import sys
import urllib.request
import zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DEST = BASE / "public" / "assets" / "video"
DEST.mkdir(parents=True, exist_ok=True)
token = os.getenv("GITHUB_TOKEN", "")
repo = os.getenv("GITHUB_REPOSITORY", "")
if not token or not repo:
    sys.exit("Set GITHUB_TOKEN and GITHUB_REPOSITORY to restore saved shots")

def request(url):
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "PapaAIClip/1.0",
    })
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read()

endpoint = f"https://api.github.com/repos/{repo}/actions/artifacts?per_page=100"
data = json.loads(request(endpoint))
artifacts = sorted(
    (a for a in data.get("artifacts", [])
     if not a.get("expired") and a.get("name") in
     ("papa-ai-footage-and-film", "papa-ai-shots-checkpoint", "ai-shot-1")),
    key=lambda a: a.get("created_at", ""), reverse=True
)
found = []
for a in artifacts:
    if len(found) >= 48:
        break
    try:
        raw = request(a["archive_download_url"])
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            for name in z.namelist():
                m = re.search(r"(?:^|/)public/assets/video/([0-4][0-9])\.mp4$", name)
                if not m:
                    m = re.search(r"(?:^|/)([0-4][0-9])\.mp4$", name)
                if not m:
                    continue
                num = int(m.group(1))
                if not (1 <= num <= 48):
                    continue
                p = DEST / f"{num:02d}.mp4"
                if p.exists() and p.stat().st_size > 10000:
                    continue
                content = z.read(name)
                if len(content) < 10000 or b"ftyp" not in content[:64]:
                    print(f"Skipping invalid MP4: {name}", flush=True)
                    continue
                p.write_bytes(content)
                found.append(num)
                print(f"Restored scene {num:02d} from artifact {a['id']}", flush=True)
    except Exception as error:
        print(f"Warning: could not read artifact {a['id']}: {error}", flush=True)

present = [f"{i:02d}" for i in range(1,49) if (DEST / f"{i:02d}.mp4").exists()]
print(f"Available shots: {len(present)}/48: {', '.join(present)}", flush=True)
