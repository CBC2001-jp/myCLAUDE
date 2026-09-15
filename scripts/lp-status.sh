#!/usr/bin/env bash
# CBC LP の状態確認: ローカル/リモートの差分、GitHub Pages ビルド、本番の反映状況
set -euo pipefail
cd "$(dirname "$0")/.."

REPO="CBC2001-jp/myCLAUDE"
URL="https://www.cbc2001.com/"

echo "== Git =="
git fetch -q origin
echo "branch : $(git rev-parse --abbrev-ref HEAD)"
echo "local  : $(git log -1 --format='%h %s' HEAD)"
echo "origin : $(git log -1 --format='%h %s' origin/main)"
read -r behind ahead < <(git rev-list --left-right --count origin/main...HEAD)
echo "ahead=$ahead behind=$behind  (未コミット: $(git status --porcelain | grep -vc '^??' || true) 件)"

echo
echo "== GitHub Pages build =="
gh api "repos/$REPO/pages/builds/latest" \
  -q '"status : " + .status + "\ncommit : " + .commit[0:7] + "\nbuilt  : " + .updated_at + (if .error.message then "\nERROR  : " + .error.message else "" end)'

echo
echo "== 本番 ($URL) =="
curl -sI "$URL" | grep -iE '^(HTTP|last-modified|etag)' | sed 's/^/  /'
live_hash=$(curl -sL "$URL" | shasum | cut -c1-12)
local_hash=$(shasum index.html | cut -c1-12)
if [ "$live_hash" = "$local_hash" ]; then
  echo "  index.html: 本番とローカルは一致 ✅"
else
  echo "  index.html: 本番とローカルが不一致（未デプロイ or キャッシュ）: live=$live_hash local=$local_hash"
fi
