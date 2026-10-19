#!/usr/bin/env python3
"""
HUD del YETI: moldura de hielo con carambanos colgando, nieve acumulada encima y colmillos
de marfil en los pilares; logo del titulo con escarcha. La barra azul es la de Ragnarok
(no se cambia aqui).

  Bossbar (Mobs/Boss_08_Yeti/Yeti_mobs.yml):  "&f &b&lYETI&f "
  Titulo  (Skills/yeti_skills.yml -> Yeti_Spawn):  /title con texto traducible

Uso: python3 tools/b08_hud.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import boss_hud as BH  # noqa: E402
import dextra_pack as DP  # noqa: E402
import b05_hud  # noqa: E402

BOSS = "yeti"
NAME = "YETI"
PREVIEW = Path(__file__).resolve().parent.parent / "Modelos/08_Yeti/preview/hud_preview.png"
TITLE_PREVIEW = PREVIEW.with_name("titulo_preview.png")
LOGO_H = 15

EXT = 5
W, H = BH.glyph_width(NAME, EXT), 32
BAR_Y = 14

OUT = (12, 24, 44)
ICE = [(70, 130, 200), (150, 210, 245), (215, 245, 255), (255, 255, 255)]
SNOW = [(196, 210, 226), (238, 244, 250)]
IVORY = [(200, 190, 160), (240, 232, 205)]
ROCK = [(60, 74, 92), (96, 112, 132)]


def frame():
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    c = W // 2
    b0, b1 = BAR_Y, BAR_Y + BH.BAR_H - 1
    for x in range(EXT, W - EXT):
        d.point((x, b0 - 3), fill=ICE[1] + (255,))
        d.point((x, b0 - 2), fill=ICE[0] + (255,))
        d.point((x, b1 + 2), fill=ICE[0] + (255,))
        d.point((x, b1 + 3), fill=ROCK[1] + (255,))
        bump = 1 + ((x * 7) % 5 == 0) + ((x * 3) % 7 == 0)    # nieve acumulada encima
        for y in range(bump):
            d.point((x, b0 - 4 - y), fill=SNOW[1 if y == bump - 1 else 0] + (255,))
    for k, x in enumerate(range(EXT + 2, W - EXT - 2, 3)):     # carambanos
        ln = 1 + (k * 5) % 5
        for y in range(ln):
            d.point((x, b1 + 4 + y), fill=ICE[1 if y < ln - 1 else 2] + (255,))
    # cristal grande en el centro
    for y in range(7):
        w = 3 - abs(y - 3) if y >= 3 else min(y, 2)
        d.line([(c - w, b0 - 6 - y), (c + w - 1, b0 - 6 - y)], fill=ICE[2 if y > 2 else 1] + (255,))
    d.point((c - 1, b0 - 10), fill=ICE[3] + (255,))
    # pilares de roca helada con colmillos de marfil
    for x0, sgn in ((0, 1), (W - EXT, -1)):
        for y in range(5, H - 4):
            for k in range(EXT):
                d.point((x0 + k, y), fill=ROCK[1 if k in (1, 2) else 0] + (255,))
        d.rectangle([x0, 3, x0 + EXT - 1, 5], fill=SNOW[1] + (255,))
        tusk = [(1, 8), (2, 9), (2, 10), (3, 11), (3, 12), (4, 13)]
        for dx, y in tusk:
            xx = x0 + dx if sgn > 0 else x0 + EXT - 1 - dx
            d.point((xx, y), fill=IVORY[1] + (255,))
        for y in range(H - 10, H - 6):
            d.point((x0 + 2, y), fill=ICE[2] + (255,))
    BH.outline(img, OUT)
    d.rectangle([EXT, b0, W - EXT - 1, b1], fill=(0, 0, 0, 0))
    d.line([(EXT, b0 - 1), (W - EXT - 1, b0 - 1)], fill=OUT + (255,))
    d.line([(EXT, b1 + 1), (W - EXT - 1, b1 + 1)], fill=OUT + (255,))
    BH.mirror_complete(img)
    return BH.fix_width(img)


def logo():
    txt = BH.logo_text(NAME, [ICE[3], ICE[3], ICE[2], ICE[2], ICE[1], ICE[0]], OUT, ICE[0], scale=2, gap=3,
                       band=(range(0, 2), SNOW[1]))
    side, top = 14, 10
    img = Image.new("RGBA", (txt.width + 2 * side, txt.height + top + 8))
    img.alpha_composite(txt, (side, top))
    d = ImageDraw.Draw(img)
    c = img.width // 2
    for k in range(-1, 2):                                      # tres cristales en la cima
        h = 8 if k == 0 else 5
        for y in range(h):
            w = 1 if y > h - 3 else 2
            d.rectangle([c + k * 7 - w + 1, top - 2 - y, c + k * 7 + w - 1, top - 2 - y], fill=ICE[1 + (y > h - 3)] + (255,))
    for cx in (side // 2, img.width - 1 - side // 2):            # copos de nieve a los lados
        cy = top + txt.height // 2
        for r in range(1, 5):
            col = ICE[3 if r < 3 else 1] + (255,)
            for dx, dy in ((r, 0), (-r, 0), (0, r), (0, -r)):
                d.point((cx + dx, cy + dy), fill=col)
            if r < 4:
                for dx, dy in ((r, r), (-r, r), (r, -r), (-r, -r)):
                    d.point((cx + dx, cy + dy), fill=ICE[2] + (255,))
        d.point((cx, cy), fill=ICE[3] + (255,))
    for k, x in enumerate(range(side + 3, side + txt.width - 3, 5)):
        ln = 2 + (k * 3) % 5
        for y in range(ln):
            d.point((x, top + txt.height - 2 + y), fill=ICE[1 if y < ln - 1 else 3] + (255,))
    BH.outline(img, OUT)
    return img


def main():
    DP.ensure_pack()
    g = frame()
    DP.register_bossbar(BOSS, g, ascent=BAR_Y - 2, height=H)
    lg = logo()
    DP.register_title(BOSS, lg, height=LOGO_H + 3, ascent=LOGO_H - 3)
    p, b = b05_hud.bars()
    BH.preview(PREVIEW, NAME, (85, 255, 255), g, BAR_Y, EXT, p, b, b05_hud.VANILLA_BLUE)
    BH.title_preview(TITLE_PREVIEW, lg, LOGO_H + 3, NAME, (85, 255, 255), "Ice Biome - Bestia del Invierno Eterno")
    print("OK", PREVIEW, "W =", W)


if __name__ == "__main__":
    main()
