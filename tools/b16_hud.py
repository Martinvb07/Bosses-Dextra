#!/usr/bin/env python3
"""
HUD de KUKULKAN: moldura de piedra con greca escalonada de jade y oro, un sol en el centro,
pilares-serpiente con plumas de quetzal; logo del titulo con penacho de plumas y cabezas de
serpiente a los lados. La barra morada es la de Old Ender (no se cambia aqui).

  Bossbar (Mobs/Boss_16_Kukulkan/Kukulkan_Mobs.yml):  "&f<C>&a&lKUKULKAN&f<C>"  (C = U+2002)
  Titulo  (Skills/Kukulkan_Combate.yml -> KK_Spawn):   /title con texto traducible

Uso: python3 tools/b16_hud.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import boss_hud as BH  # noqa: E402
import dextra_pack as DP  # noqa: E402
import b02_hud  # noqa: E402

BOSS = "kukulkan"
NAME = "KUKULKAN"
PREVIEW = Path(__file__).resolve().parent.parent / "Modelos/16_Kukulkan/preview/hud_preview.png"
TITLE_PREVIEW = PREVIEW.with_name("titulo_preview.png")
LOGO_H = 16

EXT = 5
W, H = BH.glyph_width(NAME, EXT), 32
BAR_Y = 14

OUT = (16, 24, 14)
STONE = [(90, 84, 70), (150, 140, 120), (190, 180, 160)]
JADE = [(20, 110, 70), (60, 190, 140), (150, 240, 200)]
GOLD = [(170, 120, 30), (225, 180, 60), (255, 220, 120)]
RED = (200, 50, 40)
BLUE = (40, 130, 200)


def frame():
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    c = W // 2
    b0, b1 = BAR_Y, BAR_Y + BH.BAR_H - 1
    for x in range(EXT, W - EXT):
        k = (x - EXT) % 6
        step = k if k < 3 else 5 - k
        d.point((x, b0 - 2), fill=STONE[1] + (255,))
        d.point((x, b0 - 3), fill=STONE[2] + (255,))
        d.point((x, b0 - 4 - step % 2), fill=JADE[1] + (255,))
        d.point((x, b1 + 2), fill=STONE[1] + (255,))
        d.point((x, b1 + 3), fill=(GOLD[1] if step == 0 else STONE[0]) + (255,))
    d.ellipse([c - 4, b0 - 11, c + 3, b0 - 4], fill=GOLD[1] + (255,))       # sol
    d.ellipse([c - 2, b0 - 9, c + 1, b0 - 6], fill=GOLD[2] + (255,))
    for dx, dy in ((-5, -7), (4, -7), (0, -12), (0, -3)):
        d.point((c + dx - (1 if dx > 0 else 0), b0 + dy), fill=GOLD[2] + (255,))
    for x0 in (0, W - EXT):                                                 # pilar-serpiente
        cx = x0 + EXT // 2
        for y in range(7, H - 3):
            for k in range(EXT):
                d.point((x0 + k, y), fill=(JADE[0] if (y + k) % 3 == 0 else JADE[1]) + (255,))
        d.rectangle([x0, 5, x0 + EXT - 1, 8], fill=JADE[1] + (255,))
        d.point((cx - 1, 6), fill=GOLD[2] + (255,))
        d.point((cx + 1, 6), fill=GOLD[2] + (255,))
        for i, col in enumerate((RED, JADE[1], BLUE)):                     # plumas encima
            d.line([(cx - 1 + i, 4), (cx - 2 + i * 2, 0)], fill=col + (255,))
        d.point((cx, H - 3), fill=RED + (255,))
    BH.outline(img, OUT)
    d.rectangle([EXT, b0, W - EXT - 1, b1], fill=(0, 0, 0, 0))
    d.line([(EXT, b0 - 1), (W - EXT - 1, b0 - 1)], fill=OUT + (255,))
    d.line([(EXT, b1 + 1), (W - EXT - 1, b1 + 1)], fill=OUT + (255,))
    BH.mirror_complete(img)
    return BH.fix_width(img)


def logo():
    txt = BH.logo_text(NAME, [JADE[2], JADE[2], JADE[1], JADE[1], JADE[0], JADE[0], (10, 60, 40)], OUT, GOLD[0], scale=2,
                       gap=3, band=(range(9, 10), GOLD[2]))
    side, top = 16, 14
    img = Image.new("RGBA", (txt.width + 2 * side, txt.height + top + 5))
    img.alpha_composite(txt, (side, top))
    d = ImageDraw.Draw(img)
    c = img.width // 2
    for i, dx in enumerate(range(-12, 13, 3)):                              # penacho
        col = (JADE[1], RED, BLUE, GOLD[1])[i % 4]
        h = 12 - abs(dx) // 2
        d.line([(c, top - 1), (c + dx, top - 1 - h)], fill=col + (255,))
    d.rectangle([c - 6, top - 3, c + 5, top - 1], fill=GOLD[1] + (255,))
    for sx in (-1, 1):                                                     # cabezas de serpiente
        x0 = c + sx * (txt.width // 2 + 2)
        d.polygon([(x0, top + 3), (x0 + sx * 11, top + 5), (x0 + sx * 12, top + 10), (x0, top + 13)], fill=JADE[1] + (255,))
        d.point((x0 + sx * 7, top + 6), fill=GOLD[2] + (255,))
        d.line([(x0 + sx * 12, top + 10), (x0 + sx * 15, top + 11)], fill=RED + (255,))
        for i in range(3):
            d.line([(x0 + sx * (2 + i * 3), top + 3), (x0 + sx * (1 + i * 3), top - 2)], fill=(JADE[2], RED, BLUE)[i] + (255,))
    BH.outline(img, OUT)
    return img


def main():
    DP.ensure_pack()
    g = frame()
    DP.register_bossbar(BOSS, g, ascent=BAR_Y - 2, height=H)
    lg = logo()
    DP.register_title(BOSS, lg, height=LOGO_H + 4, ascent=LOGO_H - 2)
    p, b = b02_hud.bars()
    BH.preview(PREVIEW, NAME, (85, 255, 85), g, BAR_Y, EXT, p, b, BH.VANILLA_PURPLE)
    BH.title_preview(TITLE_PREVIEW, lg, LOGO_H + 4, NAME, (85, 255, 85), "Piramide del Sol - La Serpiente Emplumada despliega sus alas")
    print("OK", PREVIEW, "W =", W)


if __name__ == "__main__":
    main()
