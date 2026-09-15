#!/usr/bin/env bash
# CBC LP を本番デプロイ: main へ push し、Pages ビルド完了まで待って反映を確認
# 使い方: scripts/lp-deploy.sh "コミットメッセージ"   （引数なしなら既存コミットを push するだけ）
set -euo pipefail
cd "$(dirname "$0")/.."

REPO="CBC2001-jp/myCLAUDE"
URL="https://www.cbc2001.com/"

[ "$(git rev-parse --abbrev-ref HEAD)" = "main" ] || { echo "main ブランチで実行してください"; exit 1; }

if [ -n "${1:-}" ]; then
  # .gitignore 対象は自動除外。素材置き場 2026_CBC_HP/ の未追跡ファイルは意図せず公開しないよう除外
  git add -A -- . ':!2026_CBC_HP'
  git commit -m "$1"
fi

git pull --ff-only origin main
git push origin main
head=$(git rev-parse HEAD)
echo "pushed $head"

echo "Pages ビルド待ち..."
for i in $(seq 1 30); do
  sleep 10
  read -r status commit < <(gh api "repos/$REPO/pages/builds/latest" -q '.status + " " + .commit')
  echo "  [$i] $status ($commit)"
  if [ "$commit" = "$head" ] && [ "$status" = "built" ]; then
    echo "✅ ビルド完了。CDN 反映まで最大 10 分（cache-control: max-age=600）"
    curl -sI "$URL" | grep -iE '^(last-modified|etag)'
    exit 0
  fi
  if [ "$status" = "errored" ]; then
    gh api "repos/$REPO/pages/builds/latest" -q .error.message
    exit 1
  fi
done
echo "タイムアウト。scripts/lp-status.sh で再確認してください"
exit 1
