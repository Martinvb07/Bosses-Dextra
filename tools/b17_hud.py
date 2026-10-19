#!/usr/bin/env python3
"""
HUD de NEZARETH: moldura de quitina negra con telaranas en las esquinas, una arana colgando
del centro con su hilo, pilares con ojos rojos; logo del titulo con telarana detras y patas
de arana a los lados. La barra azul es la de Ragnarok (no se cambia aqui).

  Bossbar (Mobs/Boss_17_Nezareth/Nezareth_Mobs.yml):  "&f<C>&8&lNEZARETH&f<C>"  (C = U+2003)
  Titulo  (Skills/Nezareth_Combate.yml -> NZ_Spawn):   /title con texto traducible

Uso: python3 tools/b17_hud.py
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import boss_hud as BH  # noqa: E402
import dextra_pack as DP  # noqa: E402
import b05_hud  # noqa: E402

BOSS = "nezareth"
NAME = "NEZARETH"
PREVIEW = Path(__file__).resolve().parent.parent / "Modelos/17_Nezareth/preview/hud_preview.png"
TITLE_PREVIEW = PREVIEW.with_name("titulo_preview.png")
LOGO_H = 16

EXT = 5
W, H = BH.glyph_width(NAME, EXT), 32
BAR_Y = 14

OUT = (8, 6, 10)
CHIT = [(30, 26, 36), (60, 54, 70), (100, 92, 112)]
SILK = (220, 218, 228)
EYE = (230, 30, 40)


def frame():
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    c = W // 2
    b0, b1 = BAR_Y, BAR_Y + BH.BAR_H - 1
    for x in range(EXT, W - EXT):
        d.point((x, b0 - 3), fill=CHIT[2] + (255,))
        d.point((x, b0 - 2), fill=CHIT[1] + (255,))
        d.point((x, b1 + 2), fill=CHIT[1] + (255,))
        d.point((x, b1 + 3), fill=CHIT[0] + (255,))
    for x0, sx in ((EXT, 1), (W - EXT - 1, -1)):                       # telaranas en las esquinas
        for r in (3, 6):
            for k in range(7):
                a = math.pi / 2 * k / 6
                d.point((round(x0 + sx * r * math.cos(a)), round(b0 - 3 - r * math.sin(a))), fill=SILK + (255,))
        for a in (0.3, 0.8, 1.3):
            for r in range(1, 7):
                d.point((round(x0 + sx * r * math.cos(a)), round(b0 - 3 - r * math.sin(a))), fill=SILK + (200,))
    d.line([(c, 0), (c, b0 - 7)], fill=SILK + (255,))                  # arana colgando
    d.ellipse([c - 2, b0 - 8, c + 1, b0 - 5], fill=CHIT[0] + (255,))
    d.point((c - 1, b0 - 7), fill=EYE + (255,))
    for dy in (0, 2):
        d.point((c - 3, b0 - 8 + dy), fill=CHIT[1] + (255,))
        d.point((c + 2, b0 - 8 + dy), fill=CHIT[1] + (255,))
    for x0 in (0, W - EXT):
        cx = x0 + EXT // 2
        for y in range(4, H - 3):
            for k in range(EXT):
                d.point((x0 + k, y), fill=CHIT[1 if k in (1, 3) else 0] + (255,))
        for yy in (6, 9, H - 7):
            d.point((cx, yy), fill=EYE + (255,))
        d.line([(cx - 2, 3), (cx, 1), (cx + 2, 3)], fill=CHIT[2] + (255,))
    BH.outline(img, OUT)
    d.rectangle([EXT, b0, W - EXT - 1, b1], fill=(0, 0, 0, 0))
    d.line([(EXT, b0 - 1), (W - EXT - 1, b0 - 1)], fill=OUT + (255,))
    d.line([(EXT, b1 + 1), (W - EXT - 1, b1 + 1)], fill=OUT + (255,))
    BH.mirror_complete(img)
    return BH.fix_width(img)


def logo():
    txt = BH.logo_text(NAME, [SILK, SILK, (180, 176, 190), CHIT[2], CHIT[2], CHIT[1], CHIT[1]], OUT, (120, 20, 30), scale=2,
                       gap=3, band=(range(4, 5), EYE))
    side, top = 16, 12
    img = Image.new("RGBA", (txt.width + 2 * side, txt.height + top + 6))
    d = ImageDraw.Draw(img)
    c = img.width // 2
    cy = top + txt.height // 2
    for k in range(10):                                                   # telarana detras
        a = 2 * math.pi * k / 10
        d.line([(c, cy), (round(c + 70 * math.cos(a)), round(cy + 24 * math.sin(a)))], fill=SILK + (140,))
    for r in (0.35, 0.65, 0.95):
        pts = [(round(c + 70 * r * math.cos(2 * math.pi * k / 10)), round(cy + 24 * r * math.sin(2 * math.pi * k / 10)))
               for k in range(11)]
        d.line(pts, fill=SILK + (140,))
    img.alpha_composite(txt, (side, top))
    for sx in (-1, 1):                                                    # patas a los lados
        x0 = c + sx * (txt.width // 2 + 1)
        for i in range(3):
            y = top + 3 + i * 4
            d.line([(x0, y), (x0 + sx * 6, y - 4), (x0 + sx * 12, y + 3)], fill=CHIT[2] + (255,))
    d.line([(c, 0), (c, top - 3)], fill=SILK + (255,))
    d.ellipse([c - 2, top - 5, c + 2, top - 1], fill=CHIT[0] + (255,))
    d.point((c, top - 3), fill=EYE + (255,))
    BH.outline(img, OUT)
    return img


def main():
    DP.ensure_pack()
    g = frame()
    DP.register_bossbar(BOSS, g, ascent=BAR_Y - 2, height=H)
    lg = logo()
    DP.register_title(BOSS, lg, height=LOGO_H + 4, ascent=LOGO_H - 2)
    p, b = b05_hud.bars()
    BH.preview(PREVIEW, NAME, (85, 85, 85), g, BAR_Y, EXT, p, b, b05_hud.VANILLA_BLUE)
    BH.title_preview(TITLE_PREVIEW, lg, LOGO_H + 4, NAME, (85, 85, 85), "La Telarana del Destino - La Tejedora Eterna despierta")
    print("OK", PREVIEW, "W =", W)


if __name__ == "__main__":
    main()
