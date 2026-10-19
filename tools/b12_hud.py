#!/usr/bin/env python3
"""
HUD de LEVIATAN: moldura de olas con espuma, corales en los pilares, perlas y un tridente en el
centro; logo del titulo con olas y tridente. La barra rosa es la de Baal (no se cambia aqui).

  Bossbar (Mobs/Boss_12_Leviatan/Leviatan_Mobs.yml):  "&f &3&lLEVIATAN&f "
  Titulo  (Skills/Leviatan_Combate.yml -> LV_Spawn):   /title con texto traducible

Uso: python3 tools/b12_hud.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import boss_hud as BH  # noqa: E402
import dextra_pack as DP  # noqa: E402
import b03_hud  # noqa: E402

BOSS = "leviatan"
NAME = "LEVIATAN"
PREVIEW = Path(__file__).resolve().parent.parent / "Modelos/12_Leviatan/preview/hud_preview.png"
TITLE_PREVIEW = PREVIEW.with_name("titulo_preview.png")
LOGO_H = 15

EXT = 5
W, H = BH.glyph_width(NAME, EXT), 32
BAR_Y = 14

OUT = (6, 20, 34)
SEA = [(20, 60, 100), (40, 110, 160), (90, 200, 220), (220, 250, 255)]
CORAL = [(150, 50, 80), (230, 90, 110)]
GOLD = (214, 176, 70)
PEARL = (240, 240, 255)


def frame():
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    c = W // 2
    b0, b1 = BAR_Y, BAR_Y + BH.BAR_H - 1
    for x in range(EXT, W - EXT):
        crest = (x % 6) in (0, 1)
        d.point((x, b0 - 3), fill=(SEA[3] if crest else SEA[2]) + (255,))
        d.point((x, b0 - 2), fill=SEA[1] + (255,))
        if (x % 6) == 0:
            d.point((x, b0 - 4), fill=SEA[3] + (255,))
        d.point((x, b1 + 2), fill=SEA[1] + (255,))
        d.point((x, b1 + 3), fill=(SEA[2] if (x % 6) in (3, 4) else SEA[0]) + (255,))
    for k, x in enumerate(range(EXT + 4, W - EXT - 3, 7)):     # perlas colgando
        d.point((x, b1 + 4), fill=SEA[2] + (255,))
        d.point((x, b1 + 5), fill=PEARL + (255,))
    for dx in (-2, 0, 2):                                       # tridente en el centro
        h = 4 if dx == 0 else 3
        d.line([(c + dx, b0 - 5 - h), (c + dx, b0 - 5)], fill=GOLD + (255,))
    d.line([(c - 2, b0 - 5), (c + 2, b0 - 5)], fill=GOLD + (255,))
    d.point((c, b0 - 10), fill=SEA[3] + (255,))
    for x0 in (0, W - EXT):                                     # pilares de roca con coral
        cx = x0 + EXT // 2
        for y in range(6, H - 3):
            for k in range(EXT):
                d.point((x0 + k, y), fill=SEA[0 if k in (0, EXT - 1) else 1] + (255,))
        for y, dx in ((1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (2, -1), (3, -2), (3, 1), (4, 2)):
            d.point((cx + dx, y), fill=CORAL[1] + (255,))
        d.point((cx, H - 7), fill=PEARL + (255,))
        d.point((cx, 9), fill=SEA[2] + (255,))
    BH.outline(img, OUT)
    d.rectangle([EXT, b0, W - EXT - 1, b1], fill=(0, 0, 0, 0))
    d.line([(EXT, b0 - 1), (W - EXT - 1, b0 - 1)], fill=OUT + (255,))
    d.line([(EXT, b1 + 1), (W - EXT - 1, b1 + 1)], fill=OUT + (255,))
    BH.mirror_complete(img)
    return BH.fix_width(img)


def logo():
    txt = BH.logo_text(NAME, [SEA[3], SEA[3], SEA[2], SEA[2], SEA[1], SEA[1], SEA[0]], OUT, SEA[1], scale=2, gap=3,
                       band=(range(9, 10), PEARL))
    side, top = 16, 12
    img = Image.new("RGBA", (txt.width + 2 * side, txt.height + top + 7))
    img.alpha_composite(txt, (side, top))
    d = ImageDraw.Draw(img)
    c = img.width // 2
    for dx in (-4, 0, 4):                                       # tridente arriba
        h = 9 if dx == 0 else 6
        d.rectangle([c + dx - 1, top - 2 - h, c + dx, top - 3], fill=GOLD + (255,))
        d.point((c + dx, top - 3 - h), fill=SEA[3] + (255,))
    d.rectangle([c - 5, top - 3, c + 4, top - 2], fill=GOLD + (255,))
    y0 = top + txt.height + 1                                   # olas debajo
    for x in range(side - 4, side + txt.width + 4):
        yy = y0 + (0 if (x // 3) % 2 else 1)
        d.point((x, yy), fill=SEA[2] + (255,))
        if (x % 6) == 0:
            d.point((x, yy - 1), fill=SEA[3] + (255,))
    for sx in (-1, 1):                                          # corales a los lados
        x = c + sx * (txt.width // 2 + 9)
        d.line([(x, top + 2), (x, top + txt.height)], fill=CORAL[1] + (255,))
        d.line([(x, top + 6), (x - 3 * sx, top + 3)], fill=CORAL[1] + (255,))
        d.line([(x, top + 9), (x + 3 * sx, top + 6)], fill=CORAL[0] + (255,))
    BH.outline(img, OUT)
    return img


def main():
    DP.ensure_pack()
    g = frame()
    DP.register_bossbar(BOSS, g, ascent=BAR_Y - 2, height=H)
    lg = logo()
    DP.register_title(BOSS, lg, height=LOGO_H + 4, ascent=LOGO_H - 2)
    p, b = b03_hud.bars()
    BH.preview(PREVIEW, NAME, (0, 170, 170), g, BAR_Y, EXT, p, b, b03_hud.VANILLA_PINK)
    BH.title_preview(TITLE_PREVIEW, lg, LOGO_H + 4, NAME, (0, 170, 170), "Fosa Abisal - El Rey del Abismo emerge")
    print("OK", PREVIEW, "W =", W)


if __name__ == "__main__":
    main()
