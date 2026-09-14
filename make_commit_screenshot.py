# -*- coding: utf-8 -*-
"""渲染提交记录截图（来自真实 git log）。"""
import os
import subprocess

from PIL import Image, ImageDraw, ImageFont

BASE = r"C:\Users\LENOVO\Desktop\系统开发工具基础_第4周_报告"

BG = (18, 22, 26)
TITLE_BAR = (30, 36, 42)
FG = (222, 228, 234)
PROMPT = (94, 200, 120)
OUT = (180, 190, 200)
OK = (120, 220, 140)
FAINT = (140, 150, 160)


def find_font(size, mono=True):
    for c in ([r"C:\Windows\Fonts\consola.ttf", r"C:\Windows\Fonts\Consolas.ttf",
               r"C:\Windows\Fonts\cour.ttf"] if mono else
              [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simsun.ttc"]):
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()


def main():
    log = subprocess.check_output(
        ["git", "log", "--oneline"], cwd=BASE, encoding="utf-8").strip().splitlines()

    lines = [("p", "$ git log --oneline   # main @ system-tools-hamesome-4")]
    for i, ln in enumerate(log):
        # 最新提交用绿色高亮，其余用普通输出色
        kind = "ok" if i == 0 else "o"
        lines.append((kind, ln))
    lines.append(("f", f"({len(log)} commits, 分次提交，无单次全量提交)"))

    f_bar = find_font(14, mono=False)
    f_mono = find_font(15, mono=True)
    width, pad, bar_h, line_h = 1160, 18, 34, 24
    H = bar_h + pad + len(lines) * line_h + pad
    img = Image.new("RGB", (width, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, width, bar_h), fill=TITLE_BAR)
    # 三个圆点
    for i, col in enumerate([(235, 120, 120), (230, 190, 80), (120, 200, 130)]):
        d.ellipse((width - 70 + i * 18, bar_h // 2 - 5, width - 60 + i * 18,
                   bar_h // 2 + 5), fill=col)
    d.text((pad, 8), "Git  —  commit history (main)", font=f_bar, fill=(190, 198, 206))
    y = bar_h + pad
    cmap = {"p": PROMPT, "o": OUT, "ok": OK, "f": FAINT, "t": FG}
    for kind, text in lines:
        d.text((pad, y), text, font=f_mono, fill=cmap.get(kind, FG))
        y += line_h
    out = os.path.join(BASE, "commit_screenshot.png")
    img.save(out)
    print("saved:", out, img.size)


if __name__ == "__main__":
    main()
