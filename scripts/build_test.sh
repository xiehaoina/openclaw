#!/bin/bash
set -e

echo "🔧 开始本地构建与测试..."
echo "1. 安装依赖..."
pnpm install --frozen-lockfile

echo "2. 执行构建..."
pnpm run build

echo "3. 运行单元测试（简化版）..."
pnpm run test:unit --run src/agents/pi-embedded-helpers/sanitize-user-facing-text.test.ts

echo "✅ 本地构建与测试通过"
