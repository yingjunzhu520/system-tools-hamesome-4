#!/usr/bin/env bash
# q13 本地质量门禁：依次运行 ruff format --check / ruff check / pytest
# 任一步失败即以非零退出，便于接入 pre-commit 或 CI。
set -euo pipefail

echo "== ruff format --check =="
ruff format --check .

echo "== ruff check =="
ruff check .

echo "== pytest =="
pytest -q

echo "ALL CHECKS PASSED"
