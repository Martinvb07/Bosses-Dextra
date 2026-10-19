#!/usr/bin/env python3
"""
HUD de OLD ENDER: moldura egipcia de la bossbar, logo del titulo y barra morada.

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
TITLE_PREVIEW = PREVIEW.with_name("titulo_preview.png")
LOGO_H = 18                 # alto del logo en px de fuente (el texto normal mide 8)

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


def logo():
    """Logo del titulo: OLD ENDER en oro con franja de lapislazuli, sol alado y dos ankh."""
    txt = BH.logo_text(NAME, [GOLD[4], GOLD[3], GOLD[3], GOLD[2], GOLD[2], GOLD[1]], OUT, PURP[2],
                       scale=3, gap=4, band=(range(9, 12), LAPIS[2]))
    side, top = 18, 12
    img = Image.new("RGBA", (txt.width + 2 * side, txt.height + top + 4))
    img.alpha_composite(txt, (side, top))
    d = ImageDraw.Draw(img)
    c = img.width // 2
    # sol alado encima del nombre
    for i in range(30):
        x = i + 6
        hh = max(1, 5 - i // 6)
        for k in range(hh):
            col = (GOLD[3], LAPIS[2], TURQ, LAPIS[1], GOLD[2])[k]
            d.point((c - x, top - 3 - k + i // 10), fill=col + (255,))
            d.point((c + x - 1, top - 3 - k + i // 10), fill=col + (255,))
    for y in range(top - 11, top - 1):
        for x in range(c - 6, c + 6):
            dx, dy = x + 0.5 - c, y + 0.5 - (top - 6)
            r2 = dx * dx + dy * dy
            if r2 <= 25:
                col = PURP[3] if r2 < 4 and dy < 0 else PURP[2] if r2 < 10 else PURP[1]
                if r2 > 16:
                    col = GOLD[3] if dy < 0 else GOLD[1]
                d.point((x, y), fill=col + (255,))
    # ankh a cada lado
    for ax in (side // 2, img.width - side // 2 - 1):
        ay = top + 2
        d.ellipse([ax - 3, ay, ax + 3, ay + 6], outline=GOLD[3] + (255,), width=2)
        d.rectangle([ax - 5, ay + 7, ax + 5, ay + 8], fill=GOLD[3] + (255,))
        d.rectangle([ax - 1, ay + 7, ax + 1, ay + 18], fill=GOLD[2] + (255,))
        d.point((ax, ay + 3), fill=PURP[2] + (255,))
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
    lg = logo()
    DP.register_title(BOSS, lg, height=LOGO_H, ascent=LOGO_H - 5)
    p, b = bars()
    DP.save_bar_sprites("purple", p, b)
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    BH.preview(PREVIEW, NAME, (170, 0, 170), g, BAR_Y, EXT, p, b, BH.VANILLA_PURPLE)
    BH.title_preview(TITLE_PREVIEW, lg, LOGO_H, NAME, (170, 0, 170), "Desert Biome - El ancestral emerge entre arenas")
    print("OK", PREVIEW)


if __name__ == "__main__":
    main()
