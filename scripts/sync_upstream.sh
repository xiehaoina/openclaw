#!/bin/bash
set -e

echo "开始同步上游OpenClaw主分支..."
git fetch upstream
git checkout main
git merge upstream/main --no-edit
echo "同步完成，推送到个人仓库..."
git push origin main
echo "✅ 上游同步完成"
