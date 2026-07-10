#!/usr/bin/env bash
# Point this repo's git at the tracked hooks in tools/hooks/.
# Run once from anywhere inside the repo. Idempotent.
set -euo pipefail
root="$(git rev-parse --show-toplevel)"
git -C "$root" config core.hooksPath tools/hooks
chmod +x "$root"/tools/hooks/* 2>/dev/null || true
echo "Installed: core.hooksPath -> tools/hooks (blocking pre-commit active; override a cleared file via tools/hooks/compliance-allowlist.txt or 'git commit --no-verify')"
