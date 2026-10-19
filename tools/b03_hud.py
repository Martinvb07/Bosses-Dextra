#!/usr/bin/env python3
"""
HUD de BAAL: moldura japonesa de la bossbar (torii, laca, sakura y shimenawa), logo del
titulo y barra rosa.

  Bossbar (Mobs/Boss_03_Baal/baal_mobs.yml):  "&f &d&lBAAL&f "
  Titulo  (Skills/baal_skills.yml -> Baal_Spawn): /title con texto traducible
  Sin pack se ve exactamente igual que siempre (ver dextra_pack.py y boss_hud.py).

Uso: python3 tools/b03_hud.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import boss_hud as BH  # noqa: E402
import dextra_pack as DP  # noqa: E402

BOSS = "baal"
NAME = "BAAL"
PREVIEW = Path(__file__).resolve().parent.parent / "Modelos/03_Baal/preview/hud_preview.png"
TITLE_PREVIEW = PREVIEW.with_name("titulo_preview.png")
LOGO_H = 18

EXT = 4
W, H = BH.glyph_width(NAME, EXT), 32
BAR_Y = 14

OUT = (26, 10, 18)
RED = [(120, 14, 22), (184, 28, 38), (226, 60, 64)]
LAC = [(18, 14, 22), (40, 32, 46)]
GOLD = [(122, 74, 14), (190, 128, 30), (232, 174, 48), (255, 216, 100), (255, 244, 190)]
PINK = [(200, 80, 150), (255, 150, 210), (255, 206, 230), (255, 240, 248)]
STRAW = [(150, 112, 50), (204, 164, 92)]
PAPER = (246, 242, 230)
VANILLA_PINK = ([(236, 120, 200)] * 2 + [(200, 70, 160)] * 3, [(80, 30, 64)] * 5)


def blossom(d, cx, cy, big=False):
    pts = [(0, -1), (1, 0), (0, 1), (-1, 0)] + ([(1, -1), (-1, -1), (1, 1), (-1, 1)] if big else [])
    for dx, dy in pts:
        d.point((cx + dx, cy + dy), fill=PINK[1 + (dy < 0)] + (255,))
    d.point((cx, cy), fill=GOLD[3] + (255,))


def frame():
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    c = W // 2
    b0, b1 = BAR_Y, BAR_Y + BH.BAR_H - 1
    # banda de laca negra arriba con filo dorado, y banda roja abajo
    for x in range(EXT, W - EXT):
        d.point((x, b0 - 4), fill=GOLD[3] + (255,))
        d.point((x, b0 - 3), fill=LAC[1] + (255,))
        d.point((x, b0 - 2), fill=LAC[0] + (255,))
        d.point((x, b1 + 2), fill=RED[1] + (255,))
        d.point((x, b1 + 3), fill=RED[0] + (255,))
    # ramas de sakura sobre la banda
    for x in range(EXT + 6, W - EXT - 6, 9):
        blossom(d, x, b0 - 6, big=(x // 9) % 2 == 0)
    for x in range(EXT + 3, W - EXT - 3):
        if (x // 3) % 3 == 0:
            d.point((x, b0 - 5), fill=(70, 40, 30, 255))
    # mon central: sakura dentro de un circulo dorado
    for y in range(b0 - 13, b0 - 2):
        for x in range(c - 6, c + 6):
            dx, dy = x + 0.5 - c, y + 0.5 - (b0 - 8)
            r2 = dx * dx + dy * dy
            if r2 <= 25:
                col = GOLD[3] if dy < 0 else GOLD[2]
                if r2 <= 12:
                    col = LAC[0]
                d.point((x, y), fill=col + (255,))
    blossom(d, c, b0 - 8, big=True)
    # shimenawa (cuerda de paja) y shide (papeles en zigzag) colgando en el centro
    for x in range(c - 14, c + 14):
        d.point((x, b1 + 4 + (1 if (x // 2) % 2 else 0)), fill=STRAW[(x // 2) % 2] + (255,))
    for sx in (c - 9, c - 1, c + 7):
        for k, (dx, dy) in enumerate(((0, 0), (1, 1), (0, 2), (1, 3), (0, 4), (1, 5))):
            d.point((sx + dx, b1 + 6 + dy), fill=PAPER + (255,))
    # pilares de torii en los extremos (cruzan la barra)
    for x0 in (0, W - EXT):
        for y in range(4, H - 3):
            for k in range(EXT):
                col = RED[2] if k == 1 else RED[1] if k == 2 else RED[0]
                d.point((x0 + k, y), fill=col + (255,))
        d.rectangle([x0 - 0, 1, x0 + EXT - 1, 3], fill=LAC[1] + (255,))     # kasagi
        d.point((x0 + (0 if x0 == 0 else EXT - 1), 1), fill=GOLD[3] + (255,))
        d.rectangle([x0, H - 3, x0 + EXT - 1, H - 2], fill=LAC[0] + (255,))  # base negra
        d.rectangle([x0, 7, x0 + EXT - 1, 7], fill=LAC[1] + (255,))          # nuki
    BH.outline(img, OUT)
    d.rectangle([EXT, b0, W - EXT - 1, b1], fill=(0, 0, 0, 0))
    d.line([(EXT, b0 - 1), (W - EXT - 1, b0 - 1)], fill=OUT + (255,))
    d.line([(EXT, b1 + 1), (W - EXT - 1, b1 + 1)], fill=OUT + (255,))
    BH.mirror_complete(img)
    return BH.fix_width(img)


def logo():
    """BAAL en letras blancas y rosas con franja carmesi, torii encima y ramas de sakura."""
    txt = BH.logo_text(NAME, [PINK[3], PINK[2], PINK[2], PINK[1], PINK[1], PINK[0]], OUT, (120, 30, 90),
                       scale=3, gap=4, band=(range(9, 12), RED[1]))
    side, top = 22, 14
    img = Image.new("RGBA", (txt.width + 2 * side, txt.height + top + 4))
    img.alpha_composite(txt, (side, top))
    d = ImageDraw.Draw(img)
    c = img.width // 2
    # torii pequeno encima del nombre
    d.rectangle([c - 13, top - 12, c + 12, top - 10], fill=LAC[1] + (255,))
    d.rectangle([c - 11, top - 9, c + 10, top - 8], fill=RED[1] + (255,))
    d.rectangle([c - 9, top - 7, c + 8, top - 6], fill=RED[0] + (255,))
    for px in (c - 8, c + 6):
        d.rectangle([px, top - 9, px + 1, top - 2], fill=RED[2] + (255,))
    d.rectangle([c - 1, top - 9, c, top - 7], fill=GOLD[3] + (255,))
    # ramas de sakura a los lados
    for sgn, x0 in ((1, 2), (-1, img.width - 3)):
        for k in range(16):
            d.point((x0 + sgn * k, top + 14 - k // 2), fill=(90, 50, 34, 255))
        for k, (dx, dy) in enumerate(((3, 0), (8, -3), (13, -6), (6, 4), (11, 1), (16, -2))):
            blossom(d, x0 + sgn * dx, top + 12 + dy, big=k % 2 == 0)
    BH.outline(img, OUT)
    return img


def bars():
    p, b = BH.bar_sprites([PINK[3], PINK[2], PINK[1], PINK[1], PINK[0]],
                          [(70, 30, 56), (54, 22, 44), (46, 18, 38), (46, 18, 38), (30, 10, 24)])
    px = p.load()
    for x in range(3, BH.BAR_W, 11):                # petalos blancos
        px[x, 1] = (255, 255, 255, 255)
        px[x + 1, 2] = (255, 236, 246, 255)
    return p, b


def main():
    DP.ensure_pack()
    g = frame()
    DP.register_bossbar(BOSS, g, ascent=BAR_Y - 2, height=H)
    lg = logo()
    DP.register_title(BOSS, lg, height=LOGO_H, ascent=LOGO_H - 5)
    p, b = bars()
    DP.save_bar_sprites("pink", p, b)
    BH.preview(PREVIEW, NAME, (255, 85, 255), g, BAR_Y, EXT, p, b, VANILLA_PINK)
    BH.title_preview(TITLE_PREVIEW, lg, LOGO_H, NAME, (255, 85, 255), "Blossom Temple - Espiritu vengativo")
    print("OK", PREVIEW, "W =", W)


if __name__ == "__main__":
    main()
