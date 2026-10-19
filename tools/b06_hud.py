#!/usr/bin/env python3
"""
HUD de MUSHLORD: moldura de tronco con musgo, setas, micelio colgando y esporas que brillan;
logo del titulo y barra verde.

  Bossbar (Mobs/Boss_06_Mushlord/Mushlord_mobs.yml):  "&f &2&lMUSHLORD&f "
  Titulo  (Skills/mushlord_skills.yml -> Mushlord_Spawn): /title con texto traducible
  Sin pack se ve exactamente igual que siempre (ver dextra_pack.py y boss_hud.py).

Uso: python3 tools/b06_hud.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import boss_hud as BH  # noqa: E402
import dextra_pack as DP  # noqa: E402

BOSS = "mushlord"
NAME = "MUSHLORD"
PREVIEW = Path(__file__).resolve().parent.parent / "Modelos/06_Mushlord/preview/hud_preview.png"
TITLE_PREVIEW = PREVIEW.with_name("titulo_preview.png")
LOGO_H = 18

EXT = 4
W, H = BH.glyph_width(NAME, EXT), 32
BAR_Y = 14

OUT = (16, 22, 12)
GREEN = [(40, 90, 32), (80, 150, 56), (130, 210, 90), (190, 250, 150)]
GLOW = (160, 255, 110)
BARK = [(70, 50, 34), (104, 76, 52)]
CAP = [(80, 30, 90), (130, 54, 140), (180, 100, 190)]
STEM = (214, 204, 176)
VANILLA_GREEN = ([(110, 230, 90)] * 2 + [(40, 170, 40)] * 3, [(20, 60, 20)] * 5)


def cap(d, cx, top, r, col=CAP, spot=GLOW):
    for y in range(r):
        half = r - y // 1 if y < r // 2 else r
        half = max(1, r - (r // 2 - y) if y < r // 2 else r)
        d.line([(cx - half, top + y), (cx + half - 1, top + y)], fill=col[1 if y < r - 1 else 0] + (255,))
    d.line([(cx - r + 1, top), (cx + r - 2, top)], fill=col[2] + (255,))
    d.point((cx - 1, top + 1), fill=spot + (255,))
    d.point((cx + r // 2, top + 2), fill=spot + (255,))


def frame():
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    c = W // 2
    b0, b1 = BAR_Y, BAR_Y + BH.BAR_H - 1
    for x in range(EXT, W - EXT):
        d.point((x, b0 - 4), fill=GREEN[2] + (255,))
        d.point((x, b0 - 3), fill=(GREEN[1] if (x // 3) % 2 else BARK[1]) + (255,))
        d.point((x, b0 - 2), fill=BARK[0] + (255,))
        d.point((x, b1 + 2), fill=BARK[1] + (255,))
        d.point((x, b1 + 3), fill=GREEN[0] + (255,))
    # setas pequenas sobre la banda
    for k, x in enumerate(range(EXT + 5, W - EXT - 5, 9)):
        d.line([(x, b0 - 5), (x, b0 - 7)], fill=STEM + (255,))
        cap(d, x, b0 - 9, 2 + k % 2)
    # seta grande en el centro
    d.rectangle([c - 1, b0 - 8, c, b0 - 4], fill=STEM + (255,))
    cap(d, c, b0 - 14, 6)
    # micelio y gotas colgando
    for k, x in enumerate(range(EXT + 3, W - EXT - 3, 4)):
        ln = 2 + (k * 7) % 6
        for y in range(ln):
            d.point((x, b1 + 4 + y), fill=(STEM if y < ln - 1 else GLOW) + (255,))
    # troncos de seta en los extremos (cruzan la barra)
    for x0 in (0, W - EXT):
        for y in range(6, H - 3):
            for k in range(EXT):
                d.point((x0 + k, y), fill=(STEM if k in (1, 2) else (180, 170, 146)) + (255,))
        d.rectangle([x0 - 0, 2, x0 + EXT - 1, 5], fill=CAP[1] + (255,))
        d.point((x0 + 1, 3), fill=GLOW + (255,))
        for y in range(9, H - 6, 6):
            d.point((x0 + 2, y), fill=GREEN[1] + (255,))
    BH.outline(img, OUT)
    d.rectangle([EXT, b0, W - EXT - 1, b1], fill=(0, 0, 0, 0))
    d.line([(EXT, b0 - 1), (W - EXT - 1, b0 - 1)], fill=OUT + (255,))
    d.line([(EXT, b1 + 1), (W - EXT - 1, b1 + 1)], fill=OUT + (255,))
    BH.mirror_complete(img)
    return BH.fix_width(img)


def logo():
    txt = BH.logo_text(NAME, [GREEN[3], GREEN[3], GREEN[2], GREEN[2], GREEN[1], GREEN[1]], OUT, (60, 160, 40),
                       scale=3, gap=4, band=(range(9, 12), CAP[1]))
    p = txt.load()
    for k in range(40):                                           # esporas que brillan sobre las letras
        x, y = (k * 37) % txt.width, (k * 13) % txt.height
        if p[x, y][3] and p[x, y][:3] != OUT:
            p[x, y] = GLOW + (255,)
    side, top = 22, 16
    img = Image.new("RGBA", (txt.width + 2 * side, txt.height + top + 8))
    img.alpha_composite(txt, (side, top))
    d = ImageDraw.Draw(img)
    c = img.width // 2
    for dx, r, h in ((-14, 4, 4), (0, 7, 6), (13, 5, 5)):
        d.rectangle([c + dx - 1, top - h, c + dx, top - 1], fill=STEM + (255,))
        cap(d, c + dx, top - h - r, r)
    for sgn, x0 in ((1, 6), (-1, img.width - 7)):
        d.rectangle([x0 - 1, top + 6, x0, top + 18], fill=STEM + (255,))
        cap(d, x0, top + 1, 5)
    for k, x in enumerate(range(side + 4, side + txt.width - 4, 7)):
        ln = 2 + (k * 5) % 5
        for y in range(ln):
            d.point((x, top + txt.height - 2 + y), fill=(GREEN[2] if y < ln - 1 else GLOW) + (255,))
    BH.outline(img, OUT)
    return img


def bars():
    p, b = BH.bar_sprites([GREEN[3], GREEN[2], GREEN[1], GREEN[1], GREEN[0]],
                          [(30, 46, 24), (24, 38, 20), (20, 32, 16), (20, 32, 16), (12, 20, 10)])
    px = p.load()
    for x in range(4, BH.BAR_W, 10):
        px[x, 2] = GLOW + (255,)
        px[x + 1, 1] = (230, 255, 210, 255)
    return p, b


def main():
    DP.ensure_pack()
    g = frame()
    DP.register_bossbar(BOSS, g, ascent=BAR_Y - 2, height=H)
    lg = logo()
    DP.register_title(BOSS, lg, height=LOGO_H + 4, ascent=LOGO_H - 3)
    p, b = bars()
    DP.save_bar_sprites("green", p, b)
    BH.preview(PREVIEW, NAME, (0, 170, 0), g, BAR_Y, EXT, p, b, VANILLA_GREEN)
    BH.title_preview(TITLE_PREVIEW, lg, LOGO_H + 4, NAME, (0, 170, 0), "Mushroom Island - Senor de las Espiras")
    print("OK", PREVIEW, "W =", W)


if __name__ == "__main__":
    main()
