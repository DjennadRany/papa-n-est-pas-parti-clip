#!/usr/bin/env bash
# Recover clips from GitHub Actions. Never reuse old watermarked transition shots.
set -euo pipefail
mkdir -p public/assets/video
if [[ -z "${GH_TOKEN:-}" ]]; then echo "GH_TOKEN unavailable";exit 1;fi
gh run list --repo "$GITHUB_REPOSITORY" --workflow film-ai.yml --limit 100 --json databaseId,status,createdAt --jq 'sort_by(.createdAt) | reverse | .[] | select(.status == "completed") | .databaseId' > /tmp/clip-run-ids.txt
# The most recent complete checkpoint wins; older archives only fill missing scenes.
# Never download artifacts from an active run.
while read -r run; do
  for artifact in papa-clean-ai-checkpoint-v2 papa-ai-footage-and-film papa-ai-shots-checkpoint ai-shot-1; do
    dir="/tmp/clip-assets-$run-$artifact"
    mkdir -p "$dir"
    if ! gh run download "$run" --repo "$GITHUB_REPOSITORY" --name "$artifact" --dir "$dir" >/dev/null 2>&1;then
      continue
    fi
    while IFS= read -r -d '' src; do
      name="$(basename "$src")"
      if ! [[ "$name" =~ ^(0[1-9]|[1-3][0-9]|4[0-8])\.mp4$ ]];then continue;fi
      number=$((10#${name%.mp4}))
      # The old images 25–48 contain an embedded NN.jpg label.
      # Only clips generated from newly cleaned inputs are allowed for them.
      if [[ "$artifact" != "papa-clean-ai-checkpoint-v2" && "$number" -ge 25 ]];then
        echo "Discard old watermarked scene $name"
        continue
      fi
      if [[ -s "$src" ]] && [[ ! -s "public/assets/video/$name" ]];then
        cp "$src" "public/assets/video/$name"
        echo "Recovered $name from run $run"
      fi
    done < <(find "$dir" -type f -name '*.mp4' -print0)
    rm -rf "$dir"
  done
done < /tmp/clip-run-ids.txt
echo "Recovered total $(find public/assets/video -maxdepth 1 -type f -name '*.mp4' | wc -l) candidate clips from completed runs"\npython ai/produce.py status
