#!/usr/bin/env python3
"""
HUD de THOR: moldura de acero con nudos nordicos, Mjolnir en el centro, rayos que bajan por
los pilares y alas en lo alto; logo del titulo con alas, martillo y rayos. La barra azul es
la de Ragnarok (no se cambia aqui).

  Bossbar (Mobs/Boss_15_Thor/Thor_Mobs.yml):  "&f<C>&b&lTHOR&f<C>"  (C = U+00A0)
  Titulo  (Skills/Thor_Combate.yml -> TH_Spawn): /title con texto traducible

Uso: python3 tools/b15_hud.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import boss_hud as BH  # noqa: E402
import dextra_pack as DP  # noqa: E402
import b05_hud  # noqa: E402

BOSS = "thor"
NAME = "THOR"
PREVIEW = Path(__file__).resolve().parent.parent / "Modelos/15_Thor/preview/hud_preview.png"
TITLE_PREVIEW = PREVIEW.with_name("titulo_preview.png")
LOGO_H = 16

EXT = 5
W, H = BH.glyph_width(NAME, EXT), 32
BAR_Y = 14

OUT = (10, 14, 24)
STEEL = [(70, 74, 86), (120, 124, 136), (180, 186, 200)]
BOLT = [(60, 120, 220), (140, 230, 255), (250, 255, 255)]
GOLD = (220, 180, 70)
WING = (235, 235, 240)


def frame():
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    c = W // 2
    b0, b1 = BAR_Y, BAR_Y + BH.BAR_H - 1
    for x in range(EXT, W - EXT):
        d.point((x, b0 - 3), fill=STEEL[2] + (255,))
        d.point((x, b0 - 2), fill=STEEL[1] + (255,))
        d.point((x, b1 + 2), fill=STEEL[1] + (255,))
        d.point((x, b1 + 3), fill=(GOLD if x % 4 == 0 else STEEL[0]) + (255,))
    d.rectangle([c - 3, b0 - 9, c + 2, b0 - 6], fill=STEEL[2] + (255,))   # Mjolnir
    d.line([(c - 3, b0 - 8), (c + 2, b0 - 8)], fill=BOLT[1] + (255,))
    d.line([(c - 1, b0 - 5), (c - 1, b0 - 4)], fill=(92, 60, 36, 255))
    for x0 in (0, W - EXT):
        cx = x0 + EXT // 2
        for y in range(6, H - 3):
            for k in range(EXT):
                d.point((x0 + k, y), fill=STEEL[0 if k in (0, EXT - 1) else 1] + (255,))
        x = cx
        for y in range(8, H - 4):                                       # rayo bajando por el pilar
            d.point((x, y), fill=BOLT[1] + (255,))
            x = cx + (1 if (y // 2) % 2 else -1)
        for i in range(4):                                              # ala arriba
            d.line([(cx - 2 + i, 5 - i), (cx - 2 + i, 5)], fill=WING + (255,))
        d.point((cx, H - 3), fill=GOLD + (255,))
    BH.outline(img, OUT)
    d.rectangle([EXT, b0, W - EXT - 1, b1], fill=(0, 0, 0, 0))
    d.line([(EXT, b0 - 1), (W - EXT - 1, b0 - 1)], fill=OUT + (255,))
    d.line([(EXT, b1 + 1), (W - EXT - 1, b1 + 1)], fill=OUT + (255,))
    BH.mirror_complete(img)
    return BH.fix_width(img)


def logo():
    txt = BH.logo_text(NAME, [BOLT[2], BOLT[2], BOLT[1], BOLT[1], BOLT[0], BOLT[0], STEEL[0]], OUT, BOLT[0], scale=2, gap=3,
                       band=(range(4, 5), GOLD))
    side, top = 22, 14
    img = Image.new("RGBA", (txt.width + 2 * side, txt.height + top + 6))
    img.alpha_composite(txt, (side, top))
    d = ImageDraw.Draw(img)
    c = img.width // 2
    d.rectangle([c - 5, top - 9, c + 4, top - 4], fill=STEEL[2] + (255,))     # martillo encima
    d.line([(c - 5, top - 7), (c + 4, top - 7)], fill=BOLT[1] + (255,))
    d.rectangle([c - 1, top - 4, c, top - 2], fill=(92, 60, 36, 255))
    for sx in (-1, 1):                                                     # alas a los lados
        x0 = c + sx * (txt.width // 2 + 1)
        pts = [(x0, top + 4), (x0 + sx * 8, top - 2), (x0 + sx * 18, top - 6), (x0 + sx * 15, top + 1),
               (x0 + sx * 17, top + 3), (x0 + sx * 13, top + 6), (x0 + sx * 14, top + 9), (x0 + sx * 8, top + 10),
               (x0, top + 12)]
        d.polygon(pts, fill=WING + (255,))
        for i in range(1, 4):                                              # separacion de plumas
            d.line([(x0 + sx * 2, top + 4 + i * 2), (x0 + sx * (6 + i * 3), top + 1 + i * 2)], fill=STEEL[1] + (255,))
        d.line([(x0, top + 4), (x0 + sx * 17, top - 5)], fill=STEEL[2] + (255,))
    BH.outline(img, OUT)
    return img


def main():
    DP.ensure_pack()
    g = frame()
    DP.register_bossbar(BOSS, g, ascent=BAR_Y - 2, height=H)
    lg = logo()
    DP.register_title(BOSS, lg, height=LOGO_H + 4, ascent=LOGO_H - 2)
    p, b = b05_hud.bars()
    BH.preview(PREVIEW, NAME, (85, 255, 255), g, BAR_Y, EXT, p, b, b05_hud.VANILLA_BLUE)
    BH.title_preview(TITLE_PREVIEW, lg, LOGO_H + 4, NAME, (85, 255, 255), "Cumbre de Asgard - El Dios del Trueno desciende")
    print("OK", PREVIEW, "W =", W)


if __name__ == "__main__":
    main()
