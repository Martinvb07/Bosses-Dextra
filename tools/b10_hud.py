#!/usr/bin/env python3
"""
HUD de KRONOS: moldura de oro con engranajes en los pilares, un reloj de arena en cada
extremo y numeros romanos grabados; logo del titulo con aureola de reloj. La barra morada es
la de Old Ender (no se cambia aqui).

  Bossbar (Mobs/Boss_10_Kronos/Kronos_Mobs.yml):  "&f &5&lKronos &8• &r&fEl Tirano del Tiempo&f "
  Titulo  (Skills/Kronos_Combate.yml -> KR_Intro):  /title con texto traducible

Uso: python3 tools/b10_hud.py
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import boss_hud as BH  # noqa: E402
import dextra_pack as DP  # noqa: E402
import b02_hud  # noqa: E402

BOSS = "kronos"
NAME = [("Kronos ", (170, 0, 170), True), ("• ", (85, 85, 85), False), ("El Tirano del Tiempo", (255, 255, 255), False)]
LOGO_NAME = "KRONOS"
PREVIEW = Path(__file__).resolve().parent.parent / "Modelos/10_Kronos/preview/hud_preview.png"
TITLE_PREVIEW = PREVIEW.with_name("titulo_preview.png")
LOGO_H = 15

EXT = 7
W, H = BH.glyph_width(NAME, EXT), 32
BAR_Y = 14

OUT = (20, 10, 30)
GOLD = [(120, 84, 30), (180, 136, 50), (230, 190, 80), (255, 240, 170)]
VIOLET = [(60, 26, 100), (120, 60, 190), (214, 140, 255)]
SAND = (236, 200, 120)
GLASS = (200, 226, 255)


def frame():
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    b0, b1 = BAR_Y, BAR_Y + BH.BAR_H - 1
    for x in range(EXT, W - EXT):
        d.point((x, b0 - 3), fill=GOLD[2] + (255,))
        d.point((x, b0 - 2), fill=GOLD[1] + (255,))
        d.point((x, b1 + 2), fill=GOLD[1] + (255,))
        d.point((x, b1 + 3), fill=GOLD[0] + (255,))
    for x in range(EXT + 1, W - EXT - 1, 3):                    # numeros romanos (palitos) grabados
        d.point((x, b0 - 4), fill=GOLD[3] + (255,))
    # pilares: engranaje arriba, reloj de arena en el centro de la barra
    for x0 in (0, W - EXT):
        cx = x0 + EXT // 2
        for y in range(9, H - 6):
            for k in range(EXT):
                d.point((x0 + k, y), fill=GOLD[1 if k in (0, EXT - 1) else 2] + (255,))
        for k in range(8):                                    # engranaje
            a = 2 * math.pi * k / 8
            d.point((round(cx + 3.6 * math.cos(a)), round(5 + 3.6 * math.sin(a))), fill=GOLD[2] + (255,))
        d.ellipse([cx - 3, 2, cx + 3, 8], fill=GOLD[1] + (255,))
        d.point((cx, 5), fill=VIOLET[2] + (255,))
        for y in range(b0 - 3, b1 + 4):                        # reloj de arena
            hw = abs(y - (b0 + 2)) // 2
            d.line([(cx - hw, y), (cx + hw, y)], fill=(SAND if y > b0 + 2 else GLASS) + (255,))
        d.line([(x0, b0 - 4), (x0 + EXT - 1, b0 - 4)], fill=GOLD[3] + (255,))
        d.line([(x0, b1 + 4), (x0 + EXT - 1, b1 + 4)], fill=GOLD[3] + (255,))
        d.point((cx, H - 4), fill=VIOLET[2] + (255,))
        d.line([(cx - 1, H - 5), (cx + 1, H - 5)], fill=GOLD[2] + (255,))
    BH.outline(img, OUT)
    d.rectangle([EXT, b0, W - EXT - 1, b1], fill=(0, 0, 0, 0))
    d.line([(EXT, b0 - 1), (W - EXT - 1, b0 - 1)], fill=OUT + (255,))
    d.line([(EXT, b1 + 1), (W - EXT - 1, b1 + 1)], fill=OUT + (255,))
    BH.mirror_complete(img)
    return BH.fix_width(img)


def logo():
    txt = BH.logo_text(LOGO_NAME, [GOLD[3], GOLD[3], GOLD[2], GOLD[2], GOLD[1], GOLD[1], GOLD[0]], OUT, VIOLET[1], scale=2,
                       gap=3, band=(range(6, 8), VIOLET[2]))
    side, top = 16, 12
    img = Image.new("RGBA", (txt.width + 2 * side, txt.height + top + 6))
    d = ImageDraw.Draw(img)
    c = img.width // 2
    # aureola de reloj detras de las letras
    R = 15
    cy = top + txt.height // 2 - 2
    for k in range(96):
        a = 2 * math.pi * k / 96
        d.point((round(c + R * 1.9 * math.cos(a)), round(cy + R * math.sin(a))), fill=GOLD[1] + (255,))
    for k in range(12):
        a = 2 * math.pi * k / 12
        x, y = round(c + R * 1.9 * math.cos(a)), round(cy + R * math.sin(a))
        d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=(VIOLET[2] if k % 3 == 0 else GOLD[2]) + (255,))
    img.alpha_composite(txt, (side, top))
    for sx in (-1, 1):                                          # relojes de arena a los lados
        x = c + sx * (txt.width // 2 + 9)
        for y in range(top + 2, top + txt.height - 1):
            hw = abs(y - (top + txt.height // 2)) // 2 + 1
            d.line([(x - hw, y), (x + hw, y)], fill=(SAND if y > top + txt.height // 2 else GLASS) + (255,))
        d.line([(x - 4, top + 1), (x + 4, top + 1)], fill=GOLD[2] + (255,))
        d.line([(x - 4, top + txt.height - 1), (x + 4, top + txt.height - 1)], fill=GOLD[2] + (255,))
    BH.outline(img, OUT)
    return img


def main():
    DP.ensure_pack()
    g = frame()
    DP.register_bossbar(BOSS, g, ascent=BAR_Y - 2, height=H)
    lg = logo()
    DP.register_title(BOSS, lg, height=LOGO_H + 4, ascent=LOGO_H - 2)
    p, b = b02_hud.bars()
    BH.preview(PREVIEW, NAME, (170, 0, 170), g, BAR_Y, EXT, p, b, BH.VANILLA_PURPLE)
    BH.title_preview(TITLE_PREVIEW, lg, LOGO_H + 4, LOGO_NAME, (170, 0, 170), "Sala del Reloj Roto - El Tirano del Tiempo despierta")
    print("OK", PREVIEW, "W =", W)


if __name__ == "__main__":
    main()
