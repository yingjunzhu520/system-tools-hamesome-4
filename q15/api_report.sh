#!/usr/bin/env bash
# q15：抓取本地 HTTP 服务上的 packages.json，用 jq 过滤+排序，
# 生成可读的 Markdown 报告 summary.md。
set -euo pipefail

URL="http://127.0.0.1:8000/packages.json"
OUT="summary.md"

# 过滤：status==active 且 downloads>=100；排序：下载量降序、包名升序
ROWS=$(curl -fsS "$URL" | jq -r '
  map(select(.status == "active" and (.downloads | tonumber) >= 100))
  | sort_by([-.downloads, .name])
  | .[] | "| \(.name) | \(.version) | \(.downloads) |"')

{
  echo "# Active Packages Report"
  echo ""
  echo "数据来源：$URL"
  echo "筛选条件：status=active 且 downloads>=100；排序：下载量降序、包名升序。"
  echo ""
  echo "| name | version | downloads |"
  echo "| --- | --- | --- |"
  echo "$ROWS"
} > "$OUT"

echo "wrote $OUT"
cat "$OUT"
