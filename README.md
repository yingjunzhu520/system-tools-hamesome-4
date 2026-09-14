# 系统开发工具基础 · 第 4 周 报告

课程：系统开发工具基础（中国海洋大学，2026 秋）
姓名：朱英俊　学号：24070030103
仓库：https://github.com/yingjunzhu520/system-tools-hamesome-4

## 本周主题
代码质量（Code Quality）· 元编程（Metaprogramming）· 大杂烩（Potpourri）· 课堂综合测试

## 目录结构
- `q13/` —— 本地质量门禁：greetlab 包 + ruff/pytest 配置 + `check.sh`
- `q14/` —— Make 构建系统：`data.csv` / `stats.py` / `build_report.py` / `Makefile`
- `q15/` —— API→报告：`packages.json` + `api_report.sh`（curl + jq → summary.md）
- `q16/` —— 综合交付：复制 q13，破坏→门禁告警→修复→`make build`→wheel SHA-256→聚焦提交
- `report.tex` / `report.pdf` —— 实验报告（使用 `hamesome-report.cls` 自设计模板）
- `make_week4_screenshots.py` —— 终端风格截图生成脚本
- `*.png` —— 各题运行结果截图

## 环境
- Windows 11 + Git Bash，Python 3.13
- `ruff 0.16`、`pytest 9.x`、`jq 1.7.1`、`build 1.6`
- 沙箱无 GNU make 与 GitHub 凭据；`make` 由同目录 `mk.py` 忠实模拟（算法与 GNU make 一致，
  在 Ubuntu 22.04 虚拟机上把 `python mk.py` 换成 `make` 即可）。

## 快速复现
```bash
# q13 质量门禁
cd q13 && ruff format --check . && ruff check . && pytest -q   # 或 bash check.sh

# q14 增量构建
cd q14 && python ../wk/mk.py        # 等价 make；touch data.csv 后重跑会重建

# q15 API 报告
cd q15 && python -m http.server 8000 & curl -fsS http://127.0.0.1:8000/packages.json | jq ...
bash api_report.sh

# q16 修复与交付
cd q16 && python ../wk/mk.py check && python ../wk/mk.py build && sha256sum dist/*.whl
```

## 提交说明
本地按「初始化 → q13 → q14 → q15 → q16 → 练习 → 报告 → 截图 → README」分次提交，
未做单次全量提交。推送到 GitHub：
```bash
git remote add origin https://github.com/yingjunzhu520/system-tools-hamesome-4.git
git branch -M main
git push -u origin main
```
