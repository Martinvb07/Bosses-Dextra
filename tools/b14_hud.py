#!/usr/bin/env python3
"""
HUD de SAMHAIN: moldura de madera vieja con enredaderas, una calabaza tallada en cada pilar,
velas encima y murcielagos; logo del titulo con calabaza, cera que gotea y murcielagos.
La barra azul es la de Ragnarok (no se cambia aqui).

  Bossbar (Mobs/Boss_14_Samhain/Samhain_Mobs.yml):  "&f<C>&6&lSAMHAIN&f<C>"  (C = U+202F)
  Titulo  (Skills/Samhain_Combate.yml -> SH_Spawn): /title con texto traducible

Uso: python3 tools/b14_hud.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import boss_hud as BH  # noqa: E402
import dextra_pack as DP  # noqa: E402
import b05_hud  # noqa: E402

BOSS = "samhain"
NAME = "SAMHAIN"
PREVIEW = Path(__file__).resolve().parent.parent / "Modelos/14_Samhain/preview/hud_preview.png"
TITLE_PREVIEW = PREVIEW.with_name("titulo_preview.png")
LOGO_H = 16

EXT = 7
W, H = BH.glyph_width(NAME, EXT), 32
BAR_Y = 14

OUT = (16, 8, 4)
WOOD = [(60, 40, 26), (90, 62, 40), (120, 86, 56)]
PUMP = [(170, 80, 10), (230, 120, 20), (255, 210, 80)]
LEAF = (70, 130, 40)
WAX = (235, 225, 200)
FLAME = (255, 200, 80)


def bat(d, x, y):
    for dx, dy in ((0, 0), (-1, -1), (1, -1), (-2, 0), (2, 0), (-3, -1), (3, -1)):
        d.point((x + dx, y + dy), fill=(30, 20, 30, 255))


def frame():
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    c = W // 2
    b0, b1 = BAR_Y, BAR_Y + BH.BAR_H - 1
    for x in range(EXT, W - EXT):
        d.point((x, b0 - 3), fill=WOOD[2] + (255,))
        d.point((x, b0 - 2), fill=WOOD[1] + (255,))
        d.point((x, b1 + 2), fill=WOOD[1] + (255,))
        d.point((x, b1 + 3), fill=WOOD[0] + (255,))
        if (x // 3) % 3 == 0:                                     # enredadera
            d.point((x, b0 - 4 + (x % 2)), fill=LEAF + (255,))
    bat(d, c, b0 - 7)
    for x0 in (0, W - EXT):
        cx = x0 + EXT // 2
        for y in range(10, H - 3):
            for k in range(1, EXT - 1):
                d.point((x0 + k, y), fill=WOOD[1 if k % 2 else 2] + (255,))
        d.ellipse([x0, 2, x0 + EXT - 1, 9], fill=PUMP[1] + (255,))     # calabaza
        d.point((cx - 1, 5), fill=PUMP[2] + (255,))
        d.point((cx + 1, 5), fill=PUMP[2] + (255,))
        d.line([(cx - 1, 7), (cx + 1, 7)], fill=PUMP[2] + (255,))
        d.point((cx, 1), fill=LEAF + (255,))
        d.line([(cx, H - 3), (cx, H - 6)], fill=WAX + (255,))          # vela abajo
        d.point((cx, H - 7), fill=FLAME + (255,))
    BH.outline(img, OUT)
    d.rectangle([EXT, b0, W - EXT - 1, b1], fill=(0, 0, 0, 0))
    d.line([(EXT, b0 - 1), (W - EXT - 1, b0 - 1)], fill=OUT + (255,))
    d.line([(EXT, b1 + 1), (W - EXT - 1, b1 + 1)], fill=OUT + (255,))
    BH.mirror_complete(img)
    return BH.fix_width(img)


def logo():
    txt = BH.logo_text(NAME, [PUMP[2], PUMP[2], PUMP[1], PUMP[1], PUMP[1], PUMP[0], PUMP[0]], OUT, PUMP[0], scale=2, gap=3,
                       band=(range(9, 10), (255, 240, 160)))
    side, top = 14, 12
    img = Image.new("RGBA", (txt.width + 2 * side, txt.height + top + 7))
    img.alpha_composite(txt, (side, top))
    d = ImageDraw.Draw(img)
    c = img.width // 2
    d.ellipse([c - 6, top - 10, c + 6, top - 1], fill=PUMP[1] + (255,))       # calabaza encima
    for dx in (-3, 2):
        d.polygon([(c + dx, top - 7), (c + dx + 2, top - 7), (c + dx + 1, top - 5)], fill=PUMP[2] + (255,))
    d.line([(c - 3, top - 3), (c + 3, top - 3)], fill=PUMP[2] + (255,))
    d.line([(c, top - 11), (c + 1, top - 13)], fill=LEAF + (255,))
    for k, x in enumerate(range(side + 5, side + txt.width - 4, 8)):     # cera que gotea
        ln = 2 + (k * 3) % 4
        d.line([(x, top + txt.height - 2), (x, top + txt.height - 2 + ln)], fill=WAX + (255,))
    for x, y in ((5, 6), (img.width - 6, 9), (side - 4, top + txt.height)):
        bat(d, x, y)
    BH.outline(img, OUT)
    return img


def main():
    DP.ensure_pack()
    g = frame()
    DP.register_bossbar(BOSS, g, ascent=BAR_Y - 2, height=H)
    lg = logo()
    DP.register_title(BOSS, lg, height=LOGO_H + 4, ascent=LOGO_H - 2)
    p, b = b05_hud.bars()
    BH.preview(PREVIEW, NAME, (255, 170, 0), g, BAR_Y, EXT, p, b, b05_hud.VANILLA_BLUE)
    BH.title_preview(TITLE_PREVIEW, lg, LOGO_H + 4, NAME, (255, 170, 0), "La Noche de las Animas - El velo entre mundos se rompe")
    print("OK", PREVIEW, "W =", W)


if __name__ == "__main__":
    main()
