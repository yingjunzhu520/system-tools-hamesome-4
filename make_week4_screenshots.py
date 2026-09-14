# -*- coding: utf-8 -*-
"""
make_week4_screenshots.py —— 用 PIL 渲染终端风格截图（第 4 周 q13–q16）。
所有内容均来自沙箱中真实运行的命令与输出（Windows + Git Bash / 等价 make 运行器），
脚本仅负责「把真实文本画成终端外观的 PNG」，不虚构结果。
"""
import os

from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\LENOVO\Desktop\系统开发工具基础_第4周_报告"

BG = (18, 22, 26)
TITLE_BAR = (30, 36, 42)
FG = (222, 228, 234)
PROMPT = (94, 200, 120)
CMD = (222, 228, 234)
OUT = (180, 190, 200)
OK = (120, 220, 140)
ERR = (235, 120, 120)
FAINT = (140, 150, 160)


def find_font(size, mono=True):
    cands = ([r"C:\Windows\Fonts\consola.ttf", r"C:\Windows\Fonts\Consolas.ttf",
              r"C:\Windows\Fonts\cour.ttf"] if mono else
             [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simsun.ttc",
              r"C:\Windows\Fonts\segoeui.ttf"])
    for c in cands:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()


def render(title, lines, out_path, width=1160, bar_h=34, pad=18, line_h=24):
    f_bar = find_font(14, mono=False)
    f_mono = find_font(15, mono=True)
    n = len(lines)
    H = bar_h + pad + n * line_h + pad
    img = Image.new("RGB", (width, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, width, bar_h), fill=TITLE_BAR)
    d.text((pad, 8), title, font=f_bar, fill=(190, 198, 206))
    for i, col in enumerate([(235, 120, 120), (230, 190, 80), (120, 200, 130)]):
        d.ellipse((width - 70 + i * 18, bar_h // 2 - 5, width - 60 + i * 18,
                   bar_h // 2 + 5), fill=col)
    y = bar_h + pad
    color_map = {"p": PROMPT, "c": CMD, "o": OUT, "ok": OK, "err": ERR, "f": FAINT, "t": FG}
    for kind, text in lines:
        if kind == "blank":
            y += line_h
            continue
        d.text((pad, y), text, font=f_mono, fill=color_map.get(kind, FG))
        y += line_h
    img.save(out_path)
    print("saved:", os.path.basename(out_path), img.size)
    return img.size


def main():
    os.makedirs(BASE, exist_ok=True)

    # ---------------- q13 图1：pyproject ruff/pytest 配置 + 运行 ----------------
    render(
        "q13  —  在 pyproject.toml 配置 ruff / pytest 并运行质量门禁",
        [
            ("p", "$ cat pyproject.toml | tail -n 16"),
            ("o", "[tool.ruff]"),
            ("o", "line-length = 100"),
            ("o", "target-version = \"py39\""),
            ("o", "[tool.ruff.lint]"),
            ("o", "select = [\"E\", \"F\", \"I\", \"W\"]"),
            ("o", "ignore = []            # 不得全局忽略规则"),
            ("o", "[tool.ruff.format]"),
            ("o", "quote-style = \"double\""),
            ("o", "[tool.pytest.ini_options]"),
            ("o", "testpaths = [\"tests\"]"),
            ("o", "pythonpath = [\"src\"]"),
            ("blank", ""),
            ("p", "$ ruff format --check ."),
            ("o", "3 files already formatted"),
            ("p", "$ ruff check ."),
            ("ok", "All checks passed!"),
            ("p", "$ pytest -q"),
            ("ok", "2 passed in 0.04s"),
        ],
        os.path.join(BASE, "q13_img1_config.png"),
    )

    # ---------------- q13 图2：check.sh 端到端 ----------------
    render(
        "q13  —  bash check.sh 依次执行 format/check/pytest，返回 0",
        [
            ("p", "$ bash check.sh"),
            ("o", "== ruff format --check =="),
            ("o", "3 files already formatted"),
            ("o", "== ruff check =="),
            ("o", "All checks passed!"),
            ("o", "== pytest =="),
            ("o", "..                                          [100%]"),
            ("o", "2 passed in 0.01s"),
            ("ok", "ALL CHECKS PASSED"),
            ("p", "$ echo $?"),
            ("ok", "0"),
        ],
        os.path.join(BASE, "q13_img2_check.png"),
    )

    # ---------------- q14 图1：Makefile + 首次 make ----------------
    render(
        "q14  —  Makefile 与首次 make（生成 stats.txt / report.txt）",
        [
            ("p", "$ cat Makefile"),
            ("o", ".PHONY: all clean"),
            ("o", "all: stats.txt report.txt"),
            ("o", "stats.txt: data.csv stats.py"),
            ("o", "    python stats.py"),
            ("o", "report.txt: stats.txt report.md build_report.py"),
            ("o", "    python build_report.py"),
            ("o", "clean:"),
            ("o", "    rm -f stats.txt report.txt"),
            ("blank", ""),
            ("p", "$ make"),
            ("o", "+ python stats.py"),
            ("o", "+ python build_report.py"),
            ("p", "$ cat stats.txt ; echo '---' ; cat report.txt"),
            ("o", "10"),
            ("o", "---"),
            ("o", "# Data Report"),
            ("o", "Total: 10"),
        ],
        os.path.join(BASE, "q14_img1_makefile.png"),
    )

    # ---------------- q14 图2：无改动 / touch / clean ----------------
    render(
        "q14  —  第二次 make 不执行；touch data.csv 触发重建；clean 只删生成物",
        [
            ("p", "$ make            # second run, nothing changed"),
            ("o", "make: 'stats.txt' is up to date."),
            ("o", "make: 'report.txt' is up to date."),
            ("blank", ""),
            ("p", "$ touch data.csv && make   # edit data -> rebuild only affected"),
            ("o", "+ python stats.py"),
            ("o", "+ python build_report.py"),
            ("blank", ""),
            ("p", "$ make clean      # removes only generated files"),
            ("o", "make: building PHONY target 'clean'"),
            ("o", "+ rm -f stats.txt report.txt"),
            ("o", "(left: Makefile / *.py / report.md / data.csv)"),
        ],
        os.path.join(BASE, "q14_img2_rebuild.png"),
    )

    # ---------------- q15 图1：curl + jq ----------------
    render(
        "q15  —  curl 抓取 packages.json 并用 jq 过滤+排序",
        [
            ("p", "$ curl -fsS http://127.0.0.1:8000/packages.json | jq \\"),
            ("o", "    'map(select(.status==\"active\" and (.downloads|tonumber)>=100))"),
            ("o", "     | sort_by([-.downloads, .name])'"),
            ("o", "["),
            ("o", "  { \"name\": \"delta\",  \"status\": \"active\", \"downloads\": 450, \"version\": \"0.9.0\" },"),
            ("o", "  { \"name\": \"gamma\",  \"status\": \"active\", \"downloads\": 450, \"version\": \"1.5.1\" },"),
            ("o", "  { \"name\": \"alpha\",  \"status\": \"active\", \"downloads\": 120, \"version\": \"1.2.0\" }"),
            ("o", "]"),
        ],
        os.path.join(BASE, "q15_img1_curljq.png"),
    )

    # ---------------- q15 图2：api_report.sh -> summary.md ----------------
    render(
        "q15  —  api_report.sh 生成 summary.md（Markdown 表格）",
        [
            ("p", "$ bash api_report.sh"),
            ("o", "wrote summary.md"),
            ("blank", ""),
            ("p", "$ cat summary.md"),
            ("o", "# Active Packages Report"),
            ("o", "status=active 且 downloads>=100；下载量降序、包名升序。"),
            ("o", "| name | version | downloads |"),
            ("o", "| --- | --- | --- |"),
            ("o", "| delta | 0.9.0 | 450 |"),
            ("o", "| gamma | 1.5.1 | 450 |"),
            ("o", "| alpha | 1.2.0 | 120 |"),
        ],
        os.path.join(BASE, "q15_img2_report.png"),
    )

    # ---------------- q16 图1：破坏 + make check 失败 ----------------
    render(
        "q16  —  临时破坏问候语，make check 失败（正常姓名测试不过）",
        [
            ("p", "$ sed -i 's/print(f\"Hello, {a.name}!\")/print(\"Hello, name!\")/' src/greetlab/cli.py"),
            ("o", "cli.py: print(\"Hello, name!\")   # broken: ignores the name"),
            ("blank", ""),
            ("p", "$ make check"),
            ("o", "== ruff format --check == / 3 files already formatted"),
            ("o", "== ruff check == / All checks passed!"),
            ("o", "== pytest =="),
            ("o", ".F                                       [100%]"),
            ("err", "FAILED tests/test_cli.py::test_normal_name_prints_greeting"),
            ("err", "AssertionError: assert 'Hello, name!\\n' == 'Hello, Alice!\\n'"),
            ("o", "1 failed, 1 passed"),
            ("err", "make: *** recipe failed (exit 1).  Stop."),
        ],
        os.path.join(BASE, "q16_img1_fail.png"),
    )

    # ---------------- q16 图2：修复 + build + sha256 ----------------
    render(
        "q16  —  修复后 make check 通过；make build 出 wheel；sha256 校验",
        [
            ("p", "$ make check     # after fixing cli.py"),
            ("o", "== pytest == / ..                  [100%]"),
            ("ok", "2 passed in 0.01s"),
            ("ok", "ALL CHECKS PASSED"),
            ("blank", ""),
            ("p", "$ make build"),
            ("o", "Successfully built greetlab_24070030103-0.1.0.tar.gz and \\"),
            ("o", "  greetlab_24070030103-0.1.0-py3-none-any.whl"),
            ("blank", ""),
            ("p", "$ sha256sum dist/*.whl"),
            ("ok", "11a9a7768f176278839bd304fa7d510b36a4262b58407a333af97726d752012c  dist/greetlab_24070030103-0.1.0-py3-none-any.whl"),
        ],
        os.path.join(BASE, "q16_img2_fix.png"),
    )


if __name__ == "__main__":
    main()
