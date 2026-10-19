#!/usr/bin/env python3
"""
HUD de OLD ENDER: moldura egipcia de la bossbar, ojos de Horus del titulo y barra morada.

  Bossbar (Mobs/Boss_02_OldEnder/OldEnder_Mobs.yml):  "&f &5&lOLD ENDER&f "
  Titulo  (Skills/old_ender_skills.yml -> OD_Spawn):   /title con texto traducible
  Sin pack se ve exactamente igual que siempre (ver dextra_pack.py y boss_hud.py).

Uso: python3 tools/b02_hud.py
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import boss_hud as BH  # noqa: E402
import dextra_pack as DP  # noqa: E402

BOSS = "old_ender"
NAME = "OLD ENDER"
PREVIEW = Path(__file__).resolve().parent.parent / "Modelos/02_OldEnder/preview/hud_preview.png"

EXT = 4                     # ancho de los pilares
W, H = BH.COVER + EXT, 32
BAR_Y = 14                  # fila de la barra dentro de la imagen -> ascent = BAR_Y - 2

OUT = (24, 14, 30)
GOLD = [(122, 74, 14), (190, 128, 30), (232, 174, 48), (255, 216, 100), (255, 244, 190)]
LAPIS = [(22, 36, 96), (34, 60, 150), (60, 96, 196)]
TURQ = (64, 178, 168)
PURP = [(70, 20, 110), (130, 50, 190), (190, 110, 240), (240, 200, 255)]


def frame():
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    c = W // 2                                   # centro (la imagen es simetrica)
    b0, b1 = BAR_Y, BAR_Y + BH.BAR_H - 1         # filas de la barra

    # bandas arriba y abajo de la barra (estilo nemes: oro y lapislazuli)
    for x in range(EXT, W - EXT):
        stripe = LAPIS[1] if (x // 2) % 2 else GOLD[2]
        d.point((x, b0 - 4), fill=GOLD[3] + (255,))
        d.point((x, b0 - 3), fill=stripe + (255,))
        d.point((x, b0 - 2), fill=GOLD[1] + (255,))
        d.point((x, b1 + 2), fill=GOLD[2] + (255,))
        d.point((x, b1 + 3), fill=(LAPIS[0] if (x // 2) % 2 else GOLD[1]) + (255,))

    # sol alado con gema morada en el centro de la banda superior
    for i in range(18):                          # alas: plumas que se afinan hacia fuera
        x = c - 4 - i
        h = max(1, 4 - i // 5)
        for k in range(h):
            col = (GOLD[3], LAPIS[2], TURQ, LAPIS[1])[k % 4]
            d.point((x, b0 - 5 - k), fill=col + (255,))
    for y in range(b0 - 10, b0 - 3):
        for x in range(c - 4, c + 4):
            dx, dy = x + 0.5 - c, y + 0.5 - (b0 - 7)
            r2 = dx * dx + dy * dy
            if r2 <= 12.5:
                col = PURP[3] if r2 < 2 and dy < 0 else PURP[2] if r2 < 5 else PURP[1]
                if r2 > 8:
                    col = GOLD[3] if dy < 0 else GOLD[1]
                d.point((x, y), fill=col + (255,))
    # cobra (uraeus) encima del sol
    d.rectangle([c - 1, b0 - 13, c, b0 - 11], fill=GOLD[3] + (255,))
    d.point((c - 1, b0 - 13), fill=GOLD[4] + (255,))

    # ankh colgando de la banda inferior
    ax = c
    for y in range(b1 + 4, b1 + 11):
        d.point((ax - 1, y), fill=GOLD[2] + (255,))
        d.point((ax, y), fill=GOLD[1] + (255,))
    d.rectangle([ax - 3, b1 + 6, ax + 2, b1 + 6], fill=GOLD[3] + (255,))
    d.rectangle([ax - 2, b1 + 11, ax + 1, b1 + 11], fill=GOLD[2] + (255,))
    for (x, y) in ((ax - 2, b1 + 12), (ax + 1, b1 + 12), (ax - 2, b1 + 13), (ax + 1, b1 + 13)):
        d.point((x, y), fill=GOLD[2] + (255,))
    d.rectangle([ax - 1, b1 + 14, ax, b1 + 14], fill=GOLD[3] + (255,))

    # obeliscos en los extremos (cruzan la barra)
    for x0 in (0, W - EXT):
        for y in range(3, H - 3):
            for k in range(EXT):
                col = GOLD[3] if k == 1 else GOLD[2] if k == 2 else GOLD[1]
                if y in (b0 - 1, b1 + 1):
                    col = GOLD[4]
                d.point((x0 + k, y), fill=col + (255,))
        d.rectangle([x0 + 1, 1, x0 + 2, 2], fill=GOLD[4] + (255,))     # piramidion
        d.rectangle([x0, H - 3, x0 + EXT - 1, H - 2], fill=GOLD[1] + (255,))
        for y in range(6, H - 6, 4):                                   # jeroglificos
            d.point((x0 + 1 + (y // 4) % 2, y), fill=LAPIS[1] + (255,))

    BH.outline(img, OUT)
    # el contorno no puede invadir la barra entre los pilares
    d.rectangle([EXT, b0, W - EXT - 1, b1], fill=(0, 0, 0, 0))
    # linea oscura pegada a la barra (marco fino)
    d.line([(EXT, b0 - 1), (W - EXT - 1, b0 - 1)], fill=OUT + (255,))
    d.line([(EXT, b1 + 1), (W - EXT - 1, b1 + 1)], fill=OUT + (255,))
    BH.mirror_complete(img)
    return BH.fix_width(img)


EYE = [
    "...LLLLLLLLLLLLLLLLL......",
    ".LLLLLLLLLLLLLLLLLLLLLL...",
    "......................LL..",
    "......GGGGGGGGG........L..",
    "....GGG.......GGG.........",
    "...G...WWPPPWW...GGGGGGGGG",
    "..G...WWPPDPPWW..GGGGGGGGG",
    "...G...WWPPPWW...G........",
    "....GGG.......GGG.........",
    "......GGGGGGGGG...........",
    ".......G.....G............",
    ".......G......G...........",
    ".......G.......G..........",
    ".......G........G...GG....",
    "......GG.........G.G..G...",
    ".....GG...........G...G...",
    "....GG.............GGG....",
]


def eye(flip):
    img = Image.new("RGBA", (28, 19))
    pal = {"L": LAPIS[1], "G": GOLD[3], "W": (250, 246, 230), "P": PURP[1], "D": PURP[0]}
    BH.sprite(img, 1, 1, EYE, pal, flip=flip)
    BH.outline(img, OUT)
    return img


def bars():
    prog = [PURP[3], PURP[2], PURP[1], PURP[1], PURP[0]]
    back = [(56, 34, 72), (40, 24, 54), (34, 20, 46), (34, 20, 46), (22, 12, 30)]
    p, b = BH.bar_sprites(prog, back)
    px = p.load()
    for x in range(0, BH.BAR_W, 7):                # brillo de gema cada 7 px
        px[x, 1] = (250, 230, 255, 255)
    return p, b


def main():
    DP.ensure_pack()
    g = frame()
    DP.register_bossbar(BOSS, g, ascent=BAR_Y - 2, height=H)
    el, er = eye(True), eye(False)
    DP.register_title(BOSS, "§5§lOLD ENDER", el, er, height=19, ascent=14)
    p, b = bars()
    DP.save_bar_sprites("purple", p, b)
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    BH.preview(PREVIEW, NAME, (170, 0, 170), g, BAR_Y, EXT, p, b, BH.VANILLA_PURPLE, el, er,
               (170, 0, 170), 17, subtitle="Desert Biome - El ancestral emerge entre arenas")
    print("OK", PREVIEW)


if __name__ == "__main__":
    main()
