#!/usr/bin/env python3
"""
HUD de LADY OF LAMENTS: moldura gotica de encaje negro con amatistas, corona en el centro y
lagrimas colgando; logo del titulo. La barra morada es la de Old Ender (no se cambia aqui).

  Bossbar (Mobs/Boss_07_LadyOfLaments/Ladyoflaments_mobs.yml):  "&f &5&lLADY OF LAMENTS&f "
  Titulo  (Skills/lady_of_laments_skills.yml -> LL_Spawn):       /title con texto traducible

Uso: python3 tools/b07_hud.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import boss_hud as BH  # noqa: E402
import dextra_pack as DP  # noqa: E402
import b02_hud  # noqa: E402

BOSS = "lady_of_laments"
NAME = "LADY OF LAMENTS"
PREVIEW = Path(__file__).resolve().parent.parent / "Modelos/07_LadyOfLaments/preview/hud_preview.png"
TITLE_PREVIEW = PREVIEW.with_name("titulo_preview.png")
LOGO_H = 15

EXT = 4
W, H = BH.glyph_width(NAME, EXT), 32
BAR_Y = 14

OUT = (14, 8, 20)
BLACK = [(20, 14, 26), (44, 30, 56)]
AME = [(100, 50, 160), (170, 100, 230), (226, 150, 255), (250, 230, 255)]
GOLD = [(150, 110, 40), (214, 170, 70)]
SILVER = [(150, 146, 160), (210, 206, 220)]


def frame():
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    c = W // 2
    b0, b1 = BAR_Y, BAR_Y + BH.BAR_H - 1
    for x in range(EXT, W - EXT):
        d.point((x, b0 - 4), fill=SILVER[1] + (255,))
        d.point((x, b0 - 3), fill=(AME[1] if x % 4 == 0 else BLACK[1]) + (255,))
        d.point((x, b0 - 2), fill=BLACK[0] + (255,))
        d.point((x, b1 + 2), fill=BLACK[1] + (255,))
        d.point((x, b1 + 3), fill=(AME[0] if x % 3 == 0 else BLACK[0]) + (255,))
    for x in range(EXT + 2, W - EXT - 2, 4):                   # encaje: arcos
        d.point((x, b0 - 5), fill=SILVER[0] + (255,))
        d.point((x + 1, b0 - 6), fill=SILVER[0] + (255,))
        d.point((x + 2, b0 - 5), fill=SILVER[0] + (255,))
    # corona de amatista en el centro
    d.rectangle([c - 5, b0 - 8, c + 4, b0 - 7], fill=GOLD[1] + (255,))
    for dx, h in ((-5, 3), (-2, 5), (1, 5), (4, 3)):
        for y in range(h):
            d.point((c + dx, b0 - 9 - y), fill=AME[2 if y < h - 1 else 3] + (255,))
    d.point((c - 1, b0 - 7), fill=AME[3] + (255,))
    # lagrimas colgando
    for k, x in enumerate(range(EXT + 3, W - EXT - 3, 5)):
        ln = 1 + (k * 3) % 4
        for y in range(ln):
            d.point((x, b1 + 4 + y), fill=AME[1] + (255,))
        d.point((x, b1 + 4 + ln), fill=AME[3] + (255,))
    # agujas goticas con amatista
    for x0 in (0, W - EXT):
        for y in range(4, H - 3):
            for k in range(EXT):
                d.point((x0 + k, y), fill=BLACK[1 if k in (1, 2) else 0] + (255,))
        d.rectangle([x0 + 1, 0, x0 + 2, 3], fill=BLACK[1] + (255,))
        d.rectangle([x0 + 1, 8, x0 + 2, 10], fill=AME[2] + (255,))
        d.rectangle([x0 + 1, H - 9, x0 + 2, H - 7], fill=AME[1] + (255,))
    BH.outline(img, OUT)
    d.rectangle([EXT, b0, W - EXT - 1, b1], fill=(0, 0, 0, 0))
    d.line([(EXT, b0 - 1), (W - EXT - 1, b0 - 1)], fill=OUT + (255,))
    d.line([(EXT, b1 + 1), (W - EXT - 1, b1 + 1)], fill=OUT + (255,))
    BH.mirror_complete(img)
    return BH.fix_width(img)


def logo():
    txt = BH.logo_text(NAME, [AME[3], AME[3], AME[2], AME[2], AME[1], AME[1]], OUT, AME[0], scale=2, gap=3,
                       band=(range(6, 8), SILVER[1]))
    side, top = 18, 13
    img = Image.new("RGBA", (txt.width + 2 * side, txt.height + top + 7))
    img.alpha_composite(txt, (side, top))
    d = ImageDraw.Draw(img)
    c = img.width // 2
    d.rectangle([c - 8, top - 3, c + 7, top - 2], fill=GOLD[1] + (255,))
    for dx, h in ((-8, 4), (-4, 7), (0, 10), (4, 7), (7, 4)):
        for y in range(h):
            w = 1 if y > h - 3 else 2
            d.rectangle([c + dx - w + 1, top - 4 - y, c + dx + w - 1, top - 4 - y], fill=AME[2 + (y > h - 3)] + (255,))
    for sgn, x0 in ((1, 4), (-1, img.width - 5)):          # rosas/espinas a los lados
        for k in range(12):
            d.point((x0 + sgn * k, top + 12 - k // 2), fill=BLACK[1] + (255,))
        d.ellipse([x0 - 2, top + 2, x0 + 3, top + 7], fill=AME[1] + (255,))
        d.point((x0, top + 4), fill=AME[3] + (255,))
    for k, x in enumerate(range(side + 4, side + txt.width - 4, 9)):
        ln = 2 + (k * 3) % 4
        for y in range(ln):
            d.point((x, top + txt.height - 2 + y), fill=AME[1] + (255,))
        d.point((x, top + txt.height - 2 + ln), fill=AME[3] + (255,))
    BH.outline(img, OUT)
    return img


def main():
    DP.ensure_pack()
    g = frame()
    DP.register_bossbar(BOSS, g, ascent=BAR_Y - 2, height=H)
    lg = logo()
    DP.register_title(BOSS, lg, height=LOGO_H + 3, ascent=LOGO_H - 3)
    p, b = b02_hud.bars()
    BH.preview(PREVIEW, NAME, (170, 0, 170), g, BAR_Y, EXT, p, b, BH.VANILLA_PURPLE)
    BH.title_preview(TITLE_PREVIEW, lg, LOGO_H + 3, NAME, (170, 0, 170), "Purple Castle - Reina del Lamento Eterno")
    print("OK", PREVIEW, "W =", W)


if __name__ == "__main__":
    main()
