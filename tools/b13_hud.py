#!/usr/bin/env python3
"""
HUD de XYLAR: moldura de metal estelar negro con filo magenta, una estrella de cuatro puntas
en el centro, constelaciones y pilares con cristales; logo del titulo con corona de cristales
y estrellas. La barra roja es la de Red Hand (no se cambia aqui).

  Bossbar (Mobs/Boss_13_Xylar/Xylar_Mobs.yml):  "&fﾠ&d&lXYLAR&fﾠ"
  Titulo  (Skills/Xylar_Combate.yml -> XY_Spawn): /title con texto traducible

Uso: python3 tools/b13_hud.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import boss_hud as BH  # noqa: E402
import dextra_pack as DP  # noqa: E402
import b04_hud  # noqa: E402

BOSS = "xylar"
NAME = "XYLAR"
PREVIEW = Path(__file__).resolve().parent.parent / "Modelos/13_Xylar/preview/hud_preview.png"
TITLE_PREVIEW = PREVIEW.with_name("titulo_preview.png")
LOGO_H = 16

EXT = 5
W, H = BH.glyph_width(NAME, EXT), 32
BAR_Y = 14

OUT = (8, 4, 14)
METAL = [(20, 14, 30), (40, 28, 56), (80, 60, 110)]
MAG = [(150, 40, 150), (230, 80, 220), (255, 170, 255)]
STAR = (255, 240, 220)


def star4(d, cx, cy, r, col, core):
    for i in range(-r, r + 1):
        d.point((cx + i, cy), fill=col + (255,))
        d.point((cx, cy + i), fill=col + (255,))
    d.point((cx, cy), fill=core + (255,))


def frame():
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    c = W // 2
    b0, b1 = BAR_Y, BAR_Y + BH.BAR_H - 1
    for x in range(EXT, W - EXT):
        d.point((x, b0 - 3), fill=MAG[1] + (255,))
        d.point((x, b0 - 2), fill=METAL[1] + (255,))
        d.point((x, b1 + 2), fill=METAL[1] + (255,))
        d.point((x, b1 + 3), fill=MAG[0] + (255,))
    for x in range(EXT + 3, W - EXT - 2, 5):                    # constelacion arriba
        d.point((x, b0 - 5 - (x % 3)), fill=STAR + (255,))
    star4(d, c, b0 - 7, 3, MAG[1], STAR)
    for x0 in (0, W - EXT):
        cx = x0 + EXT // 2
        for y in range(7, H - 4):
            for k in range(EXT):
                d.point((x0 + k, y), fill=METAL[2 if k == 2 else 1] + (255,))
        for y in range(1, 7):                                  # cristal en la cima
            hw = min(y - 1, 2)
            d.line([(cx - hw, y), (cx + hw, y)], fill=MAG[2 if y < 3 else 1] + (255,))
        d.line([(cx - 1, H - 4), (cx + 1, H - 4)], fill=MAG[1] + (255,))
        d.point((cx, H - 3), fill=MAG[2] + (255,))
        d.point((cx, 10), fill=MAG[2] + (255,))
        d.point((cx, H - 8), fill=MAG[2] + (255,))
    BH.outline(img, OUT)
    d.rectangle([EXT, b0, W - EXT - 1, b1], fill=(0, 0, 0, 0))
    d.line([(EXT, b0 - 1), (W - EXT - 1, b0 - 1)], fill=OUT + (255,))
    d.line([(EXT, b1 + 1), (W - EXT - 1, b1 + 1)], fill=OUT + (255,))
    BH.mirror_complete(img)
    return BH.fix_width(img)


def logo():
    txt = BH.logo_text(NAME, [MAG[2], MAG[2], MAG[1], MAG[1], MAG[0], METAL[2], METAL[2]], OUT, MAG[0], scale=2, gap=3,
                       band=(range(4, 5), STAR))
    side, top = 18, 13
    img = Image.new("RGBA", (txt.width + 2 * side, txt.height + top + 5))
    img.alpha_composite(txt, (side, top))
    d = ImageDraw.Draw(img)
    c = img.width // 2
    for dx, h in ((-8, 5), (-4, 8), (0, 11), (4, 8), (8, 5)):    # corona de cristales
        for y in range(h):
            w = 1 if y > h - 3 else 2
            d.rectangle([c + dx - w + 1, top - 2 - y, c + dx + w - 1, top - 2 - y], fill=MAG[1 + (y > h - 3)] + (255,))
    for sx in (-1, 1):
        star4(d, c + sx * (txt.width // 2 + 10), top + txt.height // 2, 4, MAG[1], STAR)
        d.point((c + sx * (txt.width // 2 + 4), top + 1), fill=STAR + (255,))
        d.point((c + sx * (txt.width // 2 + 14), top + txt.height), fill=STAR + (255,))
    BH.outline(img, OUT)
    return img


def main():
    DP.ensure_pack()
    g = frame()
    DP.register_bossbar(BOSS, g, ascent=BAR_Y - 2, height=H)
    lg = logo()
    DP.register_title(BOSS, lg, height=LOGO_H + 4, ascent=LOGO_H - 2)
    p, b = b04_hud.bars()
    BH.preview(PREVIEW, NAME, (255, 85, 255), g, BAR_Y, EXT, p, b, b04_hud.VANILLA_RED)
    BH.title_preview(TITLE_PREVIEW, lg, LOGO_H + 4, NAME, (255, 85, 255), "Trono Galactico - El Senor de las estrellas desciende")
    print("OK", PREVIEW, "W =", W)


if __name__ == "__main__":
    main()
