#!/usr/bin/env bash
# Builds dist/brand-identity-poster.zip with only what the skill needs
# (no examples, no README). dist/ is git-ignored: claude.ai rejects a ZIP that
# contains another ZIP, and the repository ZIP must stay uploadable as is.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p dist
rm -f dist/brand-identity-poster.zip
tmp="$(mktemp -d)"
mkdir "$tmp/brand-identity-poster"
cp -R SKILL.md LICENSE scripts references assets "$tmp/brand-identity-poster/"
(cd "$tmp" && zip -qrX - brand-identity-poster -x '*.DS_Store' '*__pycache__*') > dist/brand-identity-poster.zip
rm -rf "$tmp"
unzip -l dist/brand-identity-poster.zip
