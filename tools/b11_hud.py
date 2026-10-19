#!/usr/bin/env python3
"""
HUD de AZATHOTH: moldura de vacio con estrellas, un ojo abierto en el centro, tentaculos que
cuelgan y ojos en los pilares; logo del titulo con un gran ojo encima y tentaculos debajo.
La barra morada es la de Old Ender (no se cambia aqui).

  Bossbar (Mobs/Boss_11_Azathoth/Azathoth_Mobs.yml):  "&f &5&lAZATHOTH&f "
  Titulo  (Skills/Azathoth_Combate.yml -> AZ_Spawn):   /title con texto traducible

Uso: python3 tools/b11_hud.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import boss_hud as BH  # noqa: E402
import dextra_pack as DP  # noqa: E402
import b02_hud  # noqa: E402

BOSS = "azathoth"
NAME = "AZATHOTH"
PREVIEW = Path(__file__).resolve().parent.parent / "Modelos/11_Azathoth/preview/hud_preview.png"
TITLE_PREVIEW = PREVIEW.with_name("titulo_preview.png")
LOGO_H = 16

EXT = 5
W, H = BH.glyph_width(NAME, EXT), 32
BAR_Y = 14

OUT = (10, 4, 16)
VOID = [(20, 10, 34), (40, 20, 64), (70, 36, 104)]
NEB = [(130, 60, 210), (230, 80, 255), (255, 200, 255)]
EYE = (240, 236, 220)
STAR = (255, 240, 200)


def eye(d, cx, cy, r=2):
    d.ellipse([cx - r - 1, cy - r, cx + r + 1, cy + r], fill=EYE + (255,))
    d.rectangle([cx - 1, cy - r + 1, cx, cy + r - 1], fill=NEB[1] + (255,))
    d.point((cx, cy), fill=OUT + (255,))


def frame():
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    c = W // 2
    b0, b1 = BAR_Y, BAR_Y + BH.BAR_H - 1
    for x in range(EXT, W - EXT):
        d.point((x, b0 - 3), fill=VOID[2] + (255,))
        d.point((x, b0 - 2), fill=VOID[1] + (255,))
        d.point((x, b1 + 2), fill=VOID[1] + (255,))
        d.point((x, b1 + 3), fill=VOID[0] + (255,))
        if (x * 7) % 11 == 0:
            d.point((x, b0 - 3), fill=STAR + (255,))
    for k, x in enumerate(range(EXT + 3, W - EXT - 2, 6)):     # tentaculos colgando
        ln = 2 + (k * 5) % 5
        for y in range(ln):
            d.point((x + (y // 2) % 2, b1 + 4 + y), fill=(NEB[0] if y < ln - 1 else NEB[1]) + (255,))
    eye(d, c, b0 - 6, 2)                                       # ojo central
    d.line([(c - 4, b0 - 9), (c + 3, b0 - 9)], fill=VOID[2] + (255,))
    for x0 in (0, W - EXT):                                    # pilares con ojos
        cx = x0 + EXT // 2
        for y in range(3, H - 3):
            for k in range(EXT):
                d.point((x0 + k, y), fill=VOID[1 if k in (1, 3) else 2] + (255,))
        for yy in (7, H - 8):
            d.point((cx, yy), fill=EYE + (255,))
            d.point((cx - 1, yy), fill=EYE + (255,))
            d.point((cx + 1, yy), fill=EYE + (255,))
            d.point((cx, yy), fill=NEB[1] + (255,))
        d.point((cx, 2), fill=NEB[1] + (255,))
        d.point((cx, H - 3), fill=NEB[1] + (255,))
    BH.outline(img, OUT)
    d.rectangle([EXT, b0, W - EXT - 1, b1], fill=(0, 0, 0, 0))
    d.line([(EXT, b0 - 1), (W - EXT - 1, b0 - 1)], fill=OUT + (255,))
    d.line([(EXT, b1 + 1), (W - EXT - 1, b1 + 1)], fill=OUT + (255,))
    BH.mirror_complete(img)
    return BH.fix_width(img)


def logo():
    txt = BH.logo_text(NAME, [NEB[2], NEB[1], NEB[1], NEB[0], NEB[0], VOID[2], VOID[2]], OUT, NEB[0], scale=2, gap=3,
                       band=(range(3, 4), STAR))
    side, top = 8, 13
    img = Image.new("RGBA", (txt.width + 2 * side, txt.height + top + 9))
    img.alpha_composite(txt, (side, top))
    d = ImageDraw.Draw(img)
    c = img.width // 2
    d.ellipse([c - 9, 1, c + 9, top - 2], fill=VOID[2] + (255,))   # gran ojo encima
    d.ellipse([c - 7, 2, c + 7, top - 3], fill=EYE + (255,))
    d.ellipse([c - 3, 3, c + 3, top - 4], fill=NEB[1] + (255,))
    d.rectangle([c - 1, 3, c, top - 4], fill=OUT + (255,))
    for k, x in enumerate(range(side + 4, side + txt.width - 3, 7)):   # tentaculos debajo
        ln = 3 + (k * 3) % 5
        for y in range(ln):
            d.point((x + (y // 2) % 2, top + txt.height - 2 + y), fill=(NEB[0] if y < ln - 1 else NEB[1]) + (255,))
    for x, y in ((3, 5), (img.width - 4, 7), (side + 2, 2), (img.width - side - 3, 3)):
        d.point((x, y), fill=STAR + (255,))
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
    BH.title_preview(TITLE_PREVIEW, lg, LOGO_H + 4, NAME, (170, 0, 170), "El Vacio Exterior - El Caos Ancestral abre los ojos")
    print("OK", PREVIEW, "W =", W)


if __name__ == "__main__":
    main()
