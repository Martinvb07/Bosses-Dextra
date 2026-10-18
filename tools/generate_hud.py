#!/usr/bin/env python3
"""
Genera el HUD olimpico de Heracles (pixel art a 1x):

  - bossbar_left.png / bossbar_right.png   las dos mitades del marco de la
                       bossbar (font images de ItemsAdder)
  - title_laurel_left.png / title_laurel_right.png   laureles del titulo
  - yellow_progress.png / yellow_background.png  barra vanilla (182x5)
  - preview/hud_preview.png  vista previa

Funciona CON y SIN resource pack:
  Titulo de la bossbar:  "&f\u200c&6&lHERACLES&f\u2001"
  Titulo en pantalla:    "&f\u2002&6⚔ &e&lHERACLES &6⚔&f\u2003"
  \u200c (ancho cero) y \u2001/\u2002/\u2003 (espacios) no se ven en vanilla,
  asi que SIN pack el texto se ve exactamente igual que antes. CON pack,
  ItemsAdder convierte esos caracteres en imagenes: las dos mitades del marco
  a los lados del nombre y los laureles a los lados del titulo.

Como encaja el marco con la barra (Minecraft 1.21):
  la barra se dibuja en (centro - 91, y) y el titulo en y - 9, centrado
  (x = centro - ancho/2). Un glyph con ascent A se dibuja con su borde
  superior en y - 2 - A; el hueco de la barra esta en la fila BAR_Y del png
  -> A = BAR_Y - 2. Un glyph avanza (ultima columna visible + 1) + 1, por eso
  cada mitad lleva un pixel casi transparente en su ultima columna.
  "HERACLES" en negrita mide TEXT_W = 8 x 7 = 56 px:
    [mitad izq. 90 px, avanza 91][HERACLES 56][mitad der. 91 px, avanza 92]
    total 239 -> empieza en centro - 119 = columna 0 del marco completo,
    asi que la barra (columna BAR_X = 28) cae en centro - 91.

Uso: python3 tools/generate_hud.py
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent / "Modelos" / "01_Heracles"
FONT_DIR = ROOT / "ItemsAdder/contents/heracles_hud/textures/font"
BAR_DIR = ROOT / "ResourcePack/HeraclesPack/assets/minecraft/textures/gui/sprites/boss_bar"
PREVIEW = ROOT / "preview/hud_preview.png"

FRAME_W, FRAME_H = 256, 48
BAR_W, BAR_H = 182, 5
BAR_X = (FRAME_W - BAR_W) // 2      # 37
BAR_Y = 20                           # -> y_position (ascent) = 18
CX = BAR_X + BAR_W // 2              # 119: centro de la barra en el marco
TEXT_W = 56                          # "&lHERACLES": 8 letras de 6 px + 1 de negrita
LEFT_W = CX - TEXT_W // 2 - 1        # 90: columnas 0..89 -> mitad izquierda
RIGHT_X = LEFT_W + 1 + TEXT_W        # 147: desde aqui -> mitad derecha
SHIELD_R = 15

# ----------------------------------------------------------------- paleta
OUT = (34, 20, 8, 255)
GOLD = [(120, 70, 12), (186, 122, 26), (232, 170, 44), (255, 214, 96), (255, 244, 186)]
MARBLE = [(96, 96, 112), (156, 156, 172), (204, 204, 216), (232, 232, 242), (252, 252, 255)]
RED = [(96, 12, 12), (160, 28, 24), (214, 56, 40), (246, 108, 76)]
BRONZE = [(78, 44, 18), (128, 76, 32), (172, 112, 52), (210, 150, 80)]
LEAF = [(70, 92, 24), (112, 140, 36), (158, 186, 60), (204, 224, 110)]

# ----------------------------------------------------------------- letras
LETTERS = {
    "H": ["XX..XX", "XX..XX", "XX..XX", "XX..XX", "XXXXXX", "XX..XX", "XX..XX", "XX..XX", "XX..XX"],
    "E": ["XXXXXX", "XXXXXX", "XX....", "XX....", "XXXXX.", "XX....", "XX....", "XXXXXX", "XXXXXX"],
    "R": ["XXXXX.", "XXXXXX", "XX..XX", "XX..XX", "XXXXX.", "XX.XX.", "XX..XX", "XX..XX", "XX..XX"],
    "A": [".XXXX.", "XXXXXX", "XX..XX", "XX..XX", "XXXXXX", "XX..XX", "XX..XX", "XX..XX", "XX..XX"],
    "C": [".XXXXX", "XXXXXX", "XX....", "XX....", "XX....", "XX....", "XX....", "XXXXXX", ".XXXXX"],
    "L": ["XX....", "XX....", "XX....", "XX....", "XX....", "XX....", "XX....", "XXXXXX", "XXXXXX"],
    "S": [".XXXXX", "XXXXXX", "XX....", "XXXXX.", ".XXXXX", "....XX", "....XX", "XXXXXX", "XXXXX."],
}


def text_mask(text, scale=1, gap=1):
    w = sum(len(LETTERS[c][0]) for c in text) * scale + gap * scale * (len(text) - 1)
    h = 9 * scale
    m = Image.new("L", (w, h))
    p = m.load()
    x0 = 0
    for c in text:
        rows = LETTERS[c]
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch == "X":
                    for dy in range(scale):
                        for dx in range(scale):
                            p[x0 + x * scale + dx, y * scale + dy] = 255
        x0 += (len(rows[0]) + gap) * scale
    return m


def dilate(mask):
    w, h = mask.size
    src = mask.load()
    out = Image.new("L", (w, h))
    p = out.load()
    for y in range(h):
        for x in range(w):
            if src[x, y]:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and src[nx, ny]:
                    p[x, y] = 255
                    break
    return out


def paste_text(img, text, x, y, scale=1):
    """Letras doradas con borde oscuro, degradado vertical y brillo arriba."""
    m = text_mask(text, scale)
    pad = Image.new("L", (m.width + 2, m.height + 2))
    pad.paste(m, (1, 1))
    ring = dilate(pad)
    px = img.load()
    mp, rp = pad.load(), ring.load()
    h = m.height
    for yy in range(pad.height):
        for xx in range(pad.width):
            X, Y = x + xx - 1, y + yy - 1
            if not (0 <= X < img.width and 0 <= Y < img.height):
                continue
            if rp[xx, yy]:
                px[X, Y] = OUT
            elif mp[xx, yy]:
                t = (yy - 1) / max(1, h - 1)
                c = GOLD[4] if t < 0.12 else GOLD[3] if t < 0.4 else GOLD[2] if t < 0.75 else GOLD[1]
                # sombra interior abajo-derecha
                if xx + 1 < pad.width and yy + 1 < pad.height and not mp[xx + 1, yy + 1]:
                    c = GOLD[1] if t >= 0.4 else GOLD[2]
                px[X, Y] = c + (255,)


def outline(img, color=OUT):
    """Borde oscuro de 1 px alrededor de todo lo opaco."""
    a = img.split()[3]
    ring = dilate(a.point(lambda v: 255 if v else 0))
    px, rp = img.load(), ring.load()
    for y in range(img.height):
        for x in range(img.width):
            if rp[x, y]:
                px[x, y] = color


def shade_disc(d, cx, cy, r, pal):
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            dist = math.hypot(x - cx, y - cy)
            if dist <= r + 0.3:
                light = -(x - cx) * 0.5 - (y - cy) * 0.8   # luz arriba-izquierda
                i = 1 + (light > -2) + (light > 4)
                d.point((x, y), fill=pal[min(i, len(pal) - 1)] + (255,))


# ----------------------------------------------------------------- piezas
LEAF_SPRITE = [   # hoja hacia arriba-derecha; el tallo sale de abajo-izquierda
    "....LL",
    "..MMML",
    "DMMD..",
]


def leaf(d, x, y, dirx, diry):
    """Hoja de laurel 6x3; dirx/diry = +-1 para reflejarla."""
    cols = {"L": LEAF[3], "M": LEAF[2], "D": LEAF[1]}
    for r, row in enumerate(LEAF_SPRITE):
        for c, ch in enumerate(row):
            if ch in cols:
                yy = y - (2 - r) if diry < 0 else y + (2 - r)
                d.point((x + c * dirx, yy), fill=cols[ch] + (255,))


def leaf_poly(d, x, y, ang, length=8, width=3):
    """Hoja apuntada (para el logo), girada 'ang' grados."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    pts = []
    for i in range(9):
        t = i / 8
        w = width / 2 * math.sin(t * math.pi)
        pts.append((x + ux * length * t + nx * w, y + uy * length * t + ny * w))
    for i in range(8, -1, -1):
        t = i / 8
        w = width / 2 * math.sin(t * math.pi)
        pts.append((x + ux * length * t - nx * w, y + uy * length * t - ny * w))
    d.polygon(pts, fill=LEAF[2] + (255,))
    d.line([(x + ux, y + uy), (x + ux * length * 0.7, y + uy * length * 0.7)], fill=LEAF[3] + (255,))


def laurel_branch(d, x_from, x_to, y_top, y_bot):
    """Rama de laurel por encima y por debajo de la barra, hacia fuera."""
    step = 1 if x_to > x_from else -1
    for x in range(x_from, x_to, step):
        d.point((x, y_top), fill=LEAF[0] + (255,))
        d.point((x, y_bot), fill=LEAF[0] + (255,))
    for k, x in enumerate(range(x_from + 2 * step, x_to - 6 * step, 7 * step)):
        leaf(d, x, y_top - 1, step, -1)
        leaf(d, x + 3 * step, y_bot + 1, step, 1)
        if k % 2:  # bayas doradas
            d.point((x - step, y_top - 2), fill=GOLD[3] + (255,))
            d.point((x + 2 * step, y_bot + 2), fill=GOLD[3] + (255,))


def column(img, x, y_top, y_bot, flip):
    """Columna jonica de marmol con volutas."""
    d = ImageDraw.Draw(img)
    w = 10
    # fuste con estrias
    for yy in range(y_top + 6, y_bot - 2):
        for xx in range(w - 2):
            c = MARBLE[3] if xx in (1, 2) else MARBLE[1] if xx in (3, 6) else MARBLE[2]
            if xx == 7:
                c = MARBLE[1]
            d.point((x + 1 + xx, yy), fill=c + (255,))
    # capitel (abaco) + volutas
    d.rectangle([x - 2, y_top + 2, x + w + 1, y_top + 3], fill=MARBLE[3] + (255,))
    d.rectangle([x - 2, y_top + 4, x + w + 1, y_top + 4], fill=MARBLE[1] + (255,))
    for vx in (x - 1, x + w):
        shade_disc(d, vx, y_top + 6, 2, MARBLE)
        d.point((vx, y_top + 6), fill=MARBLE[0] + (255,))
    # dorado arriba
    d.rectangle([x - 1, y_top, x + w, y_top + 1], fill=GOLD[3] + (255,))
    d.point((x - 1, y_top), fill=GOLD[4] + (255,))
    # basa
    d.rectangle([x - 1, y_bot - 2, x + w, y_bot - 1], fill=MARBLE[2] + (255,))
    d.rectangle([x - 2, y_bot, x + w + 1, y_bot], fill=MARBLE[1] + (255,))


def wing(img, x_root, y_root, flip):
    """Ala blanca de Nike hacia fuera (flip=-1 izquierda, 1 derecha)."""
    d = ImageDraw.Draw(img)
    feathers = [(22, -9), (24, -4), (22, 1), (18, 5), (13, 8)]
    for i, (lx, ly) in enumerate(feathers):
        tip = (x_root + flip * lx, y_root + ly)
        base1 = (x_root, y_root - 3 + i * 2)
        base2 = (x_root, y_root + i * 2)
        d.polygon([base1, tip, base2], fill=MARBLE[2 + (i % 2)] + (255,))
        d.line([base1, tip], fill=MARBLE[4] + (255,))
    # arco dorado del ala
    for i in range(0, 20):
        t = i / 19
        xx = x_root + flip * round(4 + t * 18)
        yy = y_root - 4 - round(6 * math.sin(t * math.pi * 0.85))
        d.point((xx, yy), fill=GOLD[3] + (255,))
        d.point((xx, yy + 1), fill=GOLD[2] + (255,))


def helmet(img, cx, top):
    """Casco corintio dorado con penacho rojo (vista frontal)."""
    d = ImageDraw.Draw(img)
    # penacho en abanico con crines radiales
    pcx, pcy, pr = cx, top + 13, 13
    for y in range(top, top + 13):
        for x in range(cx - pr, cx + pr):
            dist = math.hypot(x + 0.5 - pcx, y + 0.5 - pcy)
            if dist <= pr and dist >= 3:
                ang = math.degrees(math.atan2(pcy - y, x + 0.5 - pcx))
                stripe = int(ang // 9) % 2
                c = RED[3] if dist > pr - 1.5 else RED[2] if stripe else RED[1]
                d.point((x, y), fill=c + (255,))
    # soporte del penacho
    d.rectangle([cx - 2, top + 10, cx + 1, top + 12], fill=GOLD[1] + (255,))
    # cupula y carrilleras
    h_top = top + 12
    for y in range(h_top, h_top + 20):
        t = y - h_top
        half = 8 if t > 3 else [5, 7, 8, 8][t]
        if t > 15:
            half = 8 - (t - 15)
        for x in range(cx - half, cx + half):
            rel = (x - cx + 0.5) / half
            c = GOLD[4] if rel < -0.5 and t < 8 else GOLD[3] if rel < 0 else GOLD[2] if rel < 0.6 else GOLD[1]
            d.point((x, y), fill=c + (255,))
    # ranura en T (ojos + nariz + boca)
    ey = h_top + 7
    d.rectangle([cx - 6, ey, cx - 2, ey + 1], fill=OUT)
    d.rectangle([cx + 1, ey, cx + 5, ey + 1], fill=OUT)
    d.rectangle([cx - 1, ey + 3, cx, ey + 12], fill=OUT)
    d.rectangle([cx - 2, ey + 8, cx + 1, ey + 12], fill=OUT)
    # ojos rojos encendidos
    d.point((cx - 4, ey), fill=RED[3] + (255,))
    d.point((cx + 3, ey), fill=RED[3] + (255,))
    # ceja
    d.line([(cx - 7, ey - 1), (cx + 6, ey - 1)], fill=GOLD[1] + (255,))


SKY = [(18, 28, 70), (30, 52, 120), (52, 86, 168), (96, 140, 214)]


def shield(img, cx, cy, r):
    """Escudo redondo (aspis) azul con borde dorado y puntos de meandro."""
    d = ImageDraw.Draw(img)
    shade_disc(d, cx, cy, r, SKY)
    for a in range(0, 360, 1):
        rad = math.radians(a)
        for rr, base in ((r, 3), (r - 1, 2)):
            x, y = round(cx + rr * math.cos(rad)), round(cy + rr * math.sin(rad))
            c = GOLD[base] if math.sin(rad) < 0.2 else GOLD[base - 1]
            d.point((x, y), fill=c + (255,))
    for a in range(0, 360, 30):
        rad = math.radians(a)
        d.point((round(cx + (r - 3) * math.cos(rad)), round(cy + (r - 3) * math.sin(rad))), fill=GOLD[3] + (255,))


# ----------------------------------------------------------------- marco
def bossbar_frame():
    img = Image.new("RGBA", (FRAME_W, FRAME_H))
    d = ImageDraw.Draw(img)
    x0, x1 = BAR_X, BAR_X + BAR_W - 1
    y0, y1 = BAR_Y, BAR_Y + BAR_H - 1

    # alas y columnas en los extremos
    wing(img, x0 - 12, y0 + 2, -1)
    wing(img, x1 + 12, y0 + 2, 1)
    column(img, x0 - 11, y0 - 9, y1 + 9, -1)
    column(img, x1 + 2, y0 - 9, y1 + 9, 1)

    # marco dorado de la barra (el hueco queda transparente)
    d.rectangle([x0 - 2, y0 - 2, x1 + 2, y1 + 2], fill=GOLD[2] + (255,))
    d.line([(x0 - 2, y0 - 2), (x1 + 2, y0 - 2)], fill=GOLD[4] + (255,))
    d.line([(x0 - 2, y1 + 2), (x1 + 2, y1 + 2)], fill=GOLD[1] + (255,))
    d.rectangle([x0 - 1, y0 - 1, x1 + 1, y1 + 1], fill=OUT)
    d.rectangle([x0, y0, x1, y1], fill=(0, 0, 0, 0))

    # laureles desde el nombre hacia las columnas
    laurel_branch(d, RIGHT_X + 2, x1 - 1, y0 - 3, y1 + 3)
    laurel_branch(d, LEFT_W - 3, x0 + 1, y0 - 3, y1 + 3)

    outline(img)
    # el contorno no debe invadir el hueco de la barra
    d.rectangle([x0, y0, x1, y1], fill=(0, 0, 0, 0))
    # hueco central para el nombre (lo escribe Minecraft) con remates dorados
    d.rectangle([LEFT_W, 0, RIGHT_X - 1, FRAME_H - 1], fill=(0, 0, 0, 0))
    for x in (LEFT_W - 2, RIGHT_X):
        d.rectangle([x, y0 - 3, x + 1, y1 + 3], fill=GOLD[3] + (255,))
        d.rectangle([x, y0 - 3, x + 1, y0 - 3], fill=GOLD[4] + (255,))
    return img


def half(img, x0, x1):
    """Recorta una mitad del marco y fija su ancho con un pixel casi invisible."""
    out = img.crop((x0, 0, x1, img.height))
    out.putpixel((out.width - 1, out.height - 1), (0, 0, 0, 1))
    return out


def laurel_side(side):
    """Media corona de laurel para un lado del titulo (side -1 izq., 1 der.)."""
    w, h = 24, 24
    img = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(img)
    wx = w - 4 if side < 0 else 3
    R = 9
    for i in range(40):
        phi = math.radians(-75 + 150 * i / 39)
        d.point((wx + side * round(R * math.cos(phi)), 12 + round(R * math.sin(phi))), fill=LEAF[0] + (255,))
    for i in range(6):
        phi = math.radians(-60 + 140 * i / 5)
        x = wx + side * R * math.cos(phi)
        y = 12 + R * math.sin(phi)
        up = math.degrees(math.atan2(-math.cos(phi), side * math.sin(phi)))
        leaf_poly(d, x, y, up + side * 35, 6, 3)
        leaf_poly(d, x, y, up - side * 35, 5, 3)
    outline(img)
    img.putpixel((w - 1, h - 1), (0, 0, 0, 1))
    return img


def bar_sprites():
    prog_rows = [GOLD[4], GOLD[3], GOLD[2], GOLD[2], GOLD[1]]
    back_rows = [(64, 48, 28), (48, 36, 20), (40, 30, 16), (40, 30, 16), (28, 20, 10)]

    def make(rows, notch):
        img = Image.new("RGBA", (BAR_W, BAR_H))
        p = img.load()
        for y, c in enumerate(rows):
            for x in range(BAR_W):
                p[x, y] = c + (255,)
        for k in range(1, 10):
            sx = round(BAR_W * k / 10)
            for y in range(1, BAR_H - 1):
                p[sx, y] = notch + (255,)
        return img

    return make(prog_rows, GOLD[1]), make(back_rows, (24, 16, 8))


def main():
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    BAR_DIR.mkdir(parents=True, exist_ok=True)
    frame = bossbar_frame()
    left, right = half(frame, 0, LEFT_W), half(frame, RIGHT_X, FRAME_W)
    prog, back = bar_sprites()
    left.save(FONT_DIR / "bossbar_left.png")
    right.save(FONT_DIR / "bossbar_right.png")
    laurel_side(-1).save(FONT_DIR / "title_laurel_left.png")
    laurel_side(1).save(FONT_DIR / "title_laurel_right.png")
    prog.save(BAR_DIR / "yellow_progress.png")
    back.save(BAR_DIR / "yellow_background.png")

    # comprobacion de la alineacion (ver docstring)
    total = (left.width + 1) + TEXT_W + (right.width + 1)
    assert -(total // 2) + BAR_X == -91, "el marco no cuadra con la barra"
    assert left.width + 1 + TEXT_W == RIGHT_X, "la mitad derecha no empieza tras el nombre"

    # vista previa (escala x4): bossbar al 65 % con el nombre + titulo
    sw = 300
    scene = Image.new("RGBA", (sw, 120), (120, 116, 112, 255))
    bx = sw // 2 - 91
    fx = bx - BAR_X
    scene.alpha_composite(left, (fx, 8))
    scene.alpha_composite(right, (fx + RIGHT_X, 8))
    scene.alpha_composite(back, (bx, 8 + BAR_Y))
    scene.alpha_composite(prog.crop((0, 0, round(BAR_W * 0.65), BAR_H)), (bx, 8 + BAR_Y))
    paste_text(scene, "HERACLES", fx + LEFT_W + 2, 8 + BAR_Y - 10)     # lo que escribe Minecraft
    tl, tr = laurel_side(-1), laurel_side(1)
    tx = sw // 2 - 34
    paste_text(scene, "HERACLES", tx + 6, 82)
    scene.alpha_composite(tl, (tx - tl.width + 2, 76))
    scene.alpha_composite(tr, (tx + 72, 76))
    scene.resize((sw * 4, 120 * 4), Image.NEAREST).save(PREVIEW)
    print("OK")


if __name__ == "__main__":
    main()
