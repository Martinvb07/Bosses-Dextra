#!/usr/bin/env python3
"""
HUD de RED HAND: moldura gotica de hierro negro (agujas, gema roja, cadenas y gotas de sangre),
logo del titulo y barra roja.

  Bossbar (Mobs/Boss_04_RedHand/Redhand_mobs.yml):  "&f &4&lRED HAND&f "
  Titulo  (Skills/redhand_skills.yml -> RH_Spawn):   /title con texto traducible
  Sin pack se ve exactamente igual que siempre (ver dextra_pack.py y boss_hud.py).

Uso: python3 tools/b04_hud.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import boss_hud as BH  # noqa: E402
import dextra_pack as DP  # noqa: E402

BOSS = "red_hand"
NAME = "RED HAND"
PREVIEW = Path(__file__).resolve().parent.parent / "Modelos/04_RedHand/preview/hud_preview.png"
TITLE_PREVIEW = PREVIEW.with_name("titulo_preview.png")
LOGO_H = 18

EXT = 4
W, H = BH.glyph_width(NAME, EXT), 32
BAR_Y = 14

OUT = (14, 8, 10)
IRON = [(34, 32, 38), (62, 60, 70), (104, 102, 116), (160, 158, 172)]
BLOOD = [(90, 6, 10), (150, 14, 20), (220, 40, 40), (255, 110, 90)]
BRASS = [(120, 84, 34), (190, 140, 60)]
VANILLA_RED = ([(230, 60, 60)] * 2 + [(180, 20, 20)] * 3, [(70, 20, 20)] * 5)


def frame():
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    c = W // 2
    b0, b1 = BAR_Y, BAR_Y + BH.BAR_H - 1
    for x in range(EXT, W - EXT):
        d.point((x, b0 - 4), fill=IRON[3] + (255,))
        d.point((x, b0 - 3), fill=IRON[1] + (255,))
        d.point((x, b0 - 2), fill=(BLOOD[1] if (x // 4) % 2 else IRON[0]) + (255,))
        d.point((x, b1 + 2), fill=IRON[1] + (255,))
        d.point((x, b1 + 3), fill=IRON[0] + (255,))
    # almenas sobre la banda
    for x in range(EXT + 3, W - EXT - 3, 6):
        d.rectangle([x, b0 - 7, x + 2, b0 - 5], fill=IRON[2] + (255,))
        d.point((x, b0 - 7), fill=IRON[3] + (255,))
    # escudo central con la mano roja
    for y in range(b0 - 13, b0 - 1):
        half = 6 if y < b0 - 5 else 6 - (y - (b0 - 5))
        for x in range(c - half, c + half):
            d.point((x, y), fill=IRON[1] + (255,))
    d.rectangle([c - 6, b0 - 13, c + 5, b0 - 13], fill=BRASS[1] + (255,))
    hand = ["..1.1.1...", "..1.1.1...", ".11111111.", ".1111111..", "..11111...", "...111...."]
    for ry, row in enumerate(hand):
        for rx, ch in enumerate(row):
            if ch == "1":
                d.point((c - 5 + rx, b0 - 12 + ry), fill=BLOOD[2] + (255,))
    # cadenas colgando con gotas de sangre
    for cx in (c - 10, c + 9):
        for k in range(4):
            d.point((cx, b1 + 4 + k * 2), fill=IRON[2] + (255,))
            d.point((cx + (1 if k % 2 else -1), b1 + 5 + k * 2), fill=IRON[1] + (255,))
    for cx, ln in ((c - 4, 5), (c, 8), (c + 3, 4), (c - 16, 3), (c + 15, 4)):
        for k in range(ln):
            d.point((cx, b1 + 4 + k), fill=BLOOD[1] + (255,))
        d.point((cx, b1 + 4 + ln), fill=BLOOD[2] + (255,))
    # agujas goticas en los extremos (cruzan la barra)
    for x0 in (0, W - EXT):
        for y in range(4, H - 3):
            for k in range(EXT):
                col = IRON[2] if k == 1 else IRON[1] if k == 2 else IRON[0]
                d.point((x0 + k, y), fill=col + (255,))
        d.rectangle([x0 + 1, 1, x0 + 2, 3], fill=IRON[3] + (255,))
        d.point((x0 + 1, 0), fill=IRON[3] + (255,))
        d.rectangle([x0 + 1, 8, x0 + 2, 9], fill=BLOOD[2] + (255,))         # gema
        d.rectangle([x0, H - 3, x0 + EXT - 1, H - 2], fill=IRON[0] + (255,))
    BH.outline(img, OUT)
    d.rectangle([EXT, b0, W - EXT - 1, b1], fill=(0, 0, 0, 0))
    d.line([(EXT, b0 - 1), (W - EXT - 1, b0 - 1)], fill=OUT + (255,))
    d.line([(EXT, b1 + 1), (W - EXT - 1, b1 + 1)], fill=OUT + (255,))
    BH.mirror_complete(img)
    return BH.fix_width(img)


def logo():
    """RED HAND en acero con franja de sangre, mano roja encima, espadas cruzadas y gotas."""
    txt = BH.logo_text(NAME, [IRON[3], IRON[3], IRON[2], IRON[2], IRON[1], IRON[1]], OUT, BLOOD[1],
                       scale=3, gap=4, band=(range(9, 12), BLOOD[2]))
    side, top = 20, 19
    img = Image.new("RGBA", (txt.width + 2 * side, txt.height + top + 9))
    img.alpha_composite(txt, (side, top))
    d = ImageDraw.Draw(img)
    c = img.width // 2
    hand = ["...1.1.1....", "..11.1.1....", "..1111111...", ".111111111..", "..1111111.11",
            "..11111111..", "...111111...", "....1111...."]
    for ry, row in enumerate(hand):
        for rx, ch in enumerate(row):
            if ch == "1":
                d.rectangle([c - 12 + rx * 2, top - 18 + ry * 2, c - 11 + rx * 2, top - 17 + ry * 2],
                            fill=(BLOOD[3] if ry < 2 else BLOOD[2]) + (255,))
    # espadas a los lados
    for sgn, x0 in ((1, 3), (-1, img.width - 4)):
        for k in range(14):
            d.point((x0 + sgn * k, top + 18 - k), fill=IRON[3] + (255,))
            d.point((x0 + sgn * k, top + 19 - k), fill=IRON[1] + (255,))
        d.line([(x0 + sgn * 1, top + 13), (x0 + sgn * 6, top + 18)], fill=BRASS[1] + (255,))
    # gotas de sangre que caen de las letras
    for k, x in enumerate(range(side + 4, side + txt.width - 4, 9)):
        ln = 3 + (k * 5) % 6
        for y in range(ln):
            d.point((x, top + txt.height - 2 + y), fill=BLOOD[1] + (255,))
        d.point((x, top + txt.height - 2 + ln), fill=BLOOD[2] + (255,))
    BH.outline(img, OUT)
    return img


def bars():
    p, b = BH.bar_sprites([BLOOD[3], BLOOD[2], BLOOD[1], BLOOD[1], BLOOD[0]],
                          [(50, 14, 16), (38, 10, 12), (32, 8, 10), (32, 8, 10), (20, 4, 6)])
    px = p.load()
    for x in range(5, BH.BAR_W, 13):
        px[x, 3] = (255, 160, 140, 255)
        px[x, 4] = (200, 30, 30, 255)
    return p, b


def main():
    DP.ensure_pack()
    g = frame()
    DP.register_bossbar(BOSS, g, ascent=BAR_Y - 2, height=H)
    lg = logo()
    DP.register_title(BOSS, lg, height=LOGO_H + 5, ascent=LOGO_H - 3)
    p, b = bars()
    DP.save_bar_sprites("red", p, b)
    BH.preview(PREVIEW, NAME, (170, 0, 0), g, BAR_Y, EXT, p, b, VANILLA_RED)
    BH.title_preview(TITLE_PREVIEW, lg, LOGO_H + 5, NAME, (170, 0, 0), "Red Castle - Un caballero caido busca sangre")
    print("OK", PREVIEW, "W =", W)


if __name__ == "__main__":
    main()
