#!/usr/bin/env python3
"""
HUD de RAGNAROK: moldura nordica (madera y hierro con nudos, piedras runicas, carambanos y
casco con cuernos), logo del titulo y barra azul helada.

  Bossbar (Mobs/Boss_05_Ragnarok/Ragnarok_mobs.yml):  "&f &b&lRAGNAROK&f "
  Titulo  (Skills/ragnarok_skills.yml -> Ragnarok_Spawn): /title con texto traducible
  Sin pack se ve exactamente igual que siempre (ver dextra_pack.py y boss_hud.py).

Uso: python3 tools/b05_hud.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import boss_hud as BH  # noqa: E402
import dextra_pack as DP  # noqa: E402

BOSS = "ragnarok"
NAME = "RAGNAROK"
PREVIEW = Path(__file__).resolve().parent.parent / "Modelos/05_Ragnarok/preview/hud_preview.png"
TITLE_PREVIEW = PREVIEW.with_name("titulo_preview.png")
LOGO_H = 18

EXT = 4
W, H = BH.glyph_width(NAME, EXT), 32
BAR_Y = 14

OUT = (10, 16, 30)
ICE = [(60, 120, 190), (120, 190, 240), (180, 230, 255), (235, 250, 255)]
WOOD = [(70, 44, 24), (110, 74, 42)]
IRON = [(60, 64, 72), (110, 116, 126)]
GOLD = [(150, 110, 40), (214, 168, 60)]
STONE = [(80, 84, 92), (120, 124, 132)]
IVORY = (230, 220, 196)
VANILLA_BLUE = ([(110, 180, 255)] * 2 + [(40, 110, 220)] * 3, [(20, 40, 80)] * 5)


def frame():
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    c = W // 2
    b0, b1 = BAR_Y, BAR_Y + BH.BAR_H - 1
    for x in range(EXT, W - EXT):
        d.point((x, b0 - 4), fill=IRON[1] + (255,))
        d.point((x, b0 - 3), fill=(GOLD[1] if (x % 4) in (0, 1) else WOOD[1]) + (255,))   # nudo
        d.point((x, b0 - 2), fill=(GOLD[0] if (x % 4) in (2, 3) else WOOD[0]) + (255,))
        d.point((x, b1 + 2), fill=WOOD[1] + (255,))
        d.point((x, b1 + 3), fill=IRON[0] + (255,))
    # cristales de hielo sobre la banda
    for x in range(EXT + 4, W - EXT - 4, 7):
        h = 2 + (x // 7) % 3
        for k in range(h):
            d.point((x, b0 - 5 - k), fill=ICE[2 + (k == h - 1)] + (255,))
            if k < h - 1:
                d.point((x + 1, b0 - 5 - k), fill=ICE[1] + (255,))
    # casco con cuernos en el centro
    d.rectangle([c - 4, b0 - 10, c + 3, b0 - 5], fill=IRON[1] + (255,))
    d.rectangle([c - 3, b0 - 11, c + 2, b0 - 11], fill=IRON[1] + (255,))
    d.rectangle([c - 4, b0 - 6, c + 3, b0 - 6], fill=GOLD[1] + (255,))
    d.rectangle([c - 1, b0 - 7, c, b0 - 3], fill=IRON[0] + (255,))
    for sx in (-1, 1):
        base = c + (4 if sx > 0 else -5)
        for k, (dx, dy) in enumerate(((0, 0), (1, -1), (2, -2), (3, -4), (3, -5), (3, -6))):
            d.point((base + sx * dx, b0 - 9 + dy), fill=IVORY + (255,))
            d.point((base + sx * dx, b0 - 8 + dy), fill=IVORY + (255,))
    # carambanos colgando
    for k, x in enumerate(range(EXT + 3, W - EXT - 3, 5)):
        ln = 2 + (k * 3) % 5
        for y in range(ln):
            d.point((x, b1 + 4 + y), fill=ICE[2 if y < ln - 1 else 3] + (255,))
        d.point((x + 1, b1 + 4), fill=ICE[1] + (255,))
    # piedras runicas en los extremos (cruzan la barra)
    for x0 in (0, W - EXT):
        for y in range(3, H - 3):
            for k in range(EXT):
                d.point((x0 + k, y), fill=STONE[1 if k in (1, 2) else 0] + (255,))
        d.rectangle([x0 + 1, 2, x0 + 2, 2], fill=STONE[1] + (255,))
        for y in range(6, H - 6, 5):
            d.point((x0 + 1, y), fill=ICE[2] + (255,))
            d.point((x0 + 2, y + 1), fill=ICE[2] + (255,))
            d.point((x0 + 1, y + 2), fill=ICE[2] + (255,))
    BH.outline(img, OUT)
    d.rectangle([EXT, b0, W - EXT - 1, b1], fill=(0, 0, 0, 0))
    d.line([(EXT, b0 - 1), (W - EXT - 1, b0 - 1)], fill=OUT + (255,))
    d.line([(EXT, b1 + 1), (W - EXT - 1, b1 + 1)], fill=OUT + (255,))
    BH.mirror_complete(img)
    return BH.fix_width(img)


def logo():
    """RAGNAROK en hielo con franja de oro, cristales encima, hachas a los lados y carambanos."""
    txt = BH.logo_text(NAME, [ICE[3], ICE[3], ICE[2], ICE[2], ICE[1], ICE[1]], OUT, ICE[0],
                       scale=3, gap=4, band=(range(9, 12), GOLD[1]))
    side, top = 20, 12
    img = Image.new("RGBA", (txt.width + 2 * side, txt.height + top + 7))
    img.alpha_composite(txt, (side, top))
    d = ImageDraw.Draw(img)
    c = img.width // 2
    for k, (dx, h) in enumerate(((-12, 5), (-6, 8), (0, 11), (6, 8), (12, 5))):
        for y in range(h):
            w = 1 if y > h - 3 else 2
            d.rectangle([c + dx - w + 1, top - 1 - y, c + dx + w - 1, top - 1 - y], fill=ICE[2 + (y > h - 3)] + (255,))
    for sgn, x0 in ((1, 3), (-1, img.width - 4)):
        for k in range(16):
            d.point((x0 + sgn * k, top + 20 - k), fill=WOOD[1] + (255,))
        for y in range(6):
            for x in range(4 - abs(y - 2)):
                d.point((x0 + sgn * (12 + x), top + 4 + y), fill=IRON[1] + (255,))
    for k, x in enumerate(range(side + 5, side + txt.width - 5, 8)):
        ln = 2 + (k * 3) % 4
        for y in range(ln):
            d.point((x, top + txt.height - 2 + y), fill=ICE[2 if y < ln - 1 else 3] + (255,))
    BH.outline(img, OUT)
    return img


def bars():
    p, b = BH.bar_sprites([ICE[3], ICE[2], ICE[1], ICE[1], ICE[0]],
                          [(26, 40, 66), (20, 32, 54), (16, 26, 46), (16, 26, 46), (10, 16, 30)])
    px = p.load()
    for x in range(2, BH.BAR_W, 9):
        px[x, 1] = (255, 255, 255, 255)
        px[x + 1, 2] = (220, 245, 255, 255)
    return p, b


def main():
    DP.ensure_pack()
    g = frame()
    DP.register_bossbar(BOSS, g, ascent=BAR_Y - 2, height=H)
    lg = logo()
    DP.register_title(BOSS, lg, height=LOGO_H + 2, ascent=LOGO_H - 4)
    p, b = bars()
    DP.save_bar_sprites("blue", p, b)
    BH.preview(PREVIEW, NAME, (85, 255, 255), g, BAR_Y, EXT, p, b, VANILLA_BLUE)
    BH.title_preview(TITLE_PREVIEW, lg, LOGO_H + 2, NAME, (85, 255, 255), "Volcano - El fin ha llegado")
    print("OK", PREVIEW, "W =", W)


if __name__ == "__main__":
    main()
