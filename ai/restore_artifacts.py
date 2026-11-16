"""Restore prior valid MP4s from non-expired GitHub Actions artifacts.
Uses GitHub Actions GITHUB_TOKEN; never requires user credentials in code.
"""
import io
import json
import os
import re
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/"public/assets/video"
DEST.mkdir(parents=True,exist_ok=True)
TOKEN=os.getenv("GITHUB_TOKEN","")
REPO=os.getenv("GITHUB_REPOSITORY","")
if not TOKEN or not REPO:
    print("No Actions token/repository: skipping remote restoration")
    raise SystemExit(0)

def get(url):
    request=urllib.request.Request(url,headers={
      "Authorization":f"Bearer {TOKEN}",
      "Accept":"application/vnd.github+json",
      "X-GitHub-Api-Version":"2022-11-28",
      "User-Agent":"papa-clip-producer"})
    with urllib.request.urlopen(request,timeout=90) as r:
        return r.read()

artifacts=[]
for page in range(1,11):
    try:
        response=json.loads(get(f"https://api.github.com/repos/{REPO}/actions/artifacts?per_page=100&page={page}"))
    except (urllib.error.HTTPError,urllib.error.URLError) as e:
        print(f"Artifact list unavailable: {e}")
        break
    batch=response.get("artifacts",[])
    artifacts.extend(a for a in batch if not a.get("expired") and
       a.get("name") in {"papa-ai-footage-and-film","papa-ai-shots-checkpoint","ai-shot-1"})
    if len(batch)<100:break

artifacts.sort(key=lambda a:a.get("created_at",""),reverse=True)
restored=0
for artifact in artifacts:
    try:
        with zipfile.ZipFile(io.BytesIO(get(artifact["archive_download_url"]))) as z:
            for entry in z.infolist():
                m=re.search(r"(?:^|/)([0-4][0-9])\.mp4$",entry.filename)
                if not m or not 1<=int(m.group(1))<=48:continue
                target=DEST/f"{int(m.group(1)):02d}.mp4"
                if target.exists() and target.stat().st_size>=10000:continue
                if entry.file_size>250_000_000:continue
                data=z.read(entry)
                if len(data)<10000 or b"ftyp" not in data[:64]:continue
                target.write_bytes(data)
                restored+=1
                print(f"Restored {target.name} from artifact {artifact['id']}",flush=True)
    except (urllib.error.HTTPError,urllib.error.URLError,zipfile.BadZipFile) as e:
        print(f"Cannot read artifact {artifact['id']}: {e}",flush=True)
print(f"Restored {restored} MP4 files",flush=True)
