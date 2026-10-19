#!/usr/bin/env python3
"""
Utilidades comunes del HUD de los bosses 02-17 (ver dextra_pack.py).

Bossbar con UN solo caracter por boss
-------------------------------------
Titulo de la bossbar en MythicMobs:  "&f<C>&5&lNOMBRE&f<C>"
Con pack, <C> es una imagen de ancho W (avanza W + 1) que se dibuja dos veces,
a la izquierda y a la derecha del nombre. Como es la MISMA imagen, tiene que ser
simetrica. Minecraft centra el texto: x0 = c - total // 2, con
total = 2 (W + 1) + T (T = ancho del nombre en negrita) y la barra en c - 91.
Con W = 60 + EXT:
  - copia izquierda: la barra empieza en la columna EXT (las EXT primeras columnas
    quedan fuera, a la izquierda de la barra);
  - copia derecha: la barra termina en la columna 59 (las EXT ultimas quedan fuera).
Asi que cada copia cubre 60 px de barra, y lo que se dibuje en las filas de la
barra en los bordes de la imagen tapa la barra en el lado del nombre: por eso los
bordes son pilares finos (EXT px) que la cruzan.
"""
from PIL import Image, ImageDraw

BAR_W, BAR_H = 182, 5
COVER = 60          # px de barra que cubre cada copia

# --------------------------------------------------------------- texto tipo Minecraft
F5 = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "11110", "10001", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "11110", "10000", "10000", "10000", "11111"],
    "F": ["11111", "10000", "11110", "10000", "10000", "10000", "10000"],
    "G": ["01111", "10000", "10011", "10001", "10001", "10001", "01110"],
    "H": ["10001", "10001", "11111", "10001", "10001", "10001", "10001"],
    "I": ["111", "010", "010", "010", "010", "010", "111"],
    "J": ["00001", "00001", "00001", "00001", "00001", "10001", "01110"],
    "K": ["10001", "10010", "11100", "10010", "10001", "10001", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10001", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "11110", "10000", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10001", "10010", "01101"],
    "R": ["11110", "10001", "11110", "10001", "10001", "10001", "10001"],
    "S": ["01111", "10000", "01110", "00001", "00001", "10001", "01110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10001", "10101", "11011", "10001"],
    "X": ["10001", "01010", "00100", "01010", "10001", "10001", "10001"],
    "Y": ["10001", "01010", "00100", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "'": ["1", "1", "0", "0", "0", "0", "0"],
    "-": ["000", "000", "000", "111", "000", "000", "000"],
    ".": ["0", "0", "0", "0", "0", "0", "1"],
}


def text_width(text, bold=True):
    """Ancho en px como lo mide Minecraft (letra + 1; espacio 4; negrita +1 cada uno)."""
    w = 0
    for ch in text:
        w += (4 if ch == " " else len(F5[ch][0]) + 1) + (1 if bold else 0)
    return w


def draw_text(img, text, x, y, color, bold=True, shadow=True):
    p = img.load()

    def put(px, py, c):
        if 0 <= px < img.width and 0 <= py < img.height:
            p[px, py] = c + (255,)

    for pass_, off, col in ((0, 1, tuple(v // 4 for v in color)), (1, 0, color)):
        if pass_ == 0 and not shadow:
            continue
        cx = x
        for ch in text:
            if ch == " ":
                cx += 4 + (1 if bold else 0)
                continue
            rows = F5[ch]
            for ry, row in enumerate(rows):
                for rx, v in enumerate(row):
                    if v == "1":
                        put(cx + rx + off, y + ry + off, col)
                        if bold:
                            put(cx + rx + 1 + off, y + ry + off, col)
            cx += len(rows[0]) + 1 + (1 if bold else 0)


# --------------------------------------------------------------- pixel art
def dilate(alpha):
    w, h = alpha.size
    src = alpha.load()
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


def outline(img, color):
    a = img.split()[3].point(lambda v: 255 if v else 0)
    ring = dilate(a)
    px, rp = img.load(), ring.load()
    for y in range(img.height):
        for x in range(img.width):
            if rp[x, y]:
                px[x, y] = color + (255,)


def sprite(img, x, y, rows, pal, flip=False):
    """Dibuja un sprite ASCII: cada letra es un color de 'pal' ('.' = vacio)."""
    p = img.load()
    w = max(len(r) for r in rows)
    for ry, row in enumerate(rows):
        for rx, ch in enumerate(row):
            if ch in pal:
                X = x + (w - 1 - rx if flip else rx)
                if 0 <= X < img.width and 0 <= y + ry < img.height:
                    p[X, y + ry] = pal[ch] + (255,)


def mirror_complete(img):
    """Hace la imagen simetrica copiando la mitad izquierda sobre la derecha."""
    w = img.width
    left = img.crop((0, 0, (w + 1) // 2, img.height))
    img.paste(left.transpose(Image.FLIP_LEFT_RIGHT), (w // 2, 0))
    return img


def fix_width(img):
    """Pixel casi transparente en la ultima columna: fija el avance del glifo."""
    img.putpixel((img.width - 1, img.height - 1), (0, 0, 0, 1))
    return img


# --------------------------------------------------------------- barra vanilla
def bar_sprites(prog_rows, back_rows):
    def make(rows):
        img = Image.new("RGBA", (BAR_W, BAR_H))
        p = img.load()
        for y, c in enumerate(rows):
            for x in range(BAR_W):
                p[x, y] = c + (255,)
        return img
    return make(prog_rows), make(back_rows)


# --------------------------------------------------------------- vista previa
VANILLA_PURPLE = ([(196, 112, 230)] * 2 + [(150, 60, 200)] * 3, [(70, 34, 86)] * 5)


def preview(path, name, name_color, glyph, bar_y, bar_ext, prog, back, vanilla_bar, title_l, title_r,
            title_color, title_scale_px, subtitle="", health=0.62):
    """Compara la bossbar y el titulo SIN pack (vanilla) y CON pack. Escala x3."""
    T = text_width(name)
    W = glyph.width
    total = 2 * (W + 1) + T
    sw = 340
    c = sw // 2
    scene = Image.new("RGBA", (sw * 2 + 20, 150), (104, 112, 92, 255))
    for col, with_pack in ((0, False), (1, True)):
        ox = col * (sw + 20)
        bx = ox + c - 91
        by = 26
        if with_pack:
            x0 = ox + c - total // 2
            pb, bk = prog, back
        else:
            x0 = ox + c - T // 2 - 2
            pb, bk = bar_sprites(*vanilla_bar)
        scene.alpha_composite(bk, (bx, by))
        scene.alpha_composite(pb.crop((0, 0, round(BAR_W * health), BAR_H)), (bx, by))
        if with_pack:
            gy = by - bar_y
            scene.alpha_composite(glyph, (x0, gy))
            scene.alpha_composite(glyph, (x0 + W + 1 + T, gy))
            draw_text(scene, name, x0 + W + 1, by - 9, name_color)
        else:
            draw_text(scene, name, ox + c - T // 2, by - 9, name_color)
        # titulo en pantalla (escala 2 en la vista previa)
        big = Image.new("RGBA", (sw // 2, 40))
        tw = T
        if with_pack:
            sl, sr = title_l, title_r
            lw = round(sl.width * title_scale_px / sl.height)
            sl = sl.resize((lw, title_scale_px), Image.NEAREST)
            sr = sr.resize((lw, title_scale_px), Image.NEAREST)
            full = lw + 1 + 4 + tw + 4 + lw + 1
            tx = big.width // 2 - full // 2
            ty = 20
            big.alpha_composite(sl, (tx, ty + 7 - title_scale_px + 2))
            draw_text(big, name, tx + lw + 1 + 4, ty, title_color)
            big.alpha_composite(sr, (tx + lw + 1 + 4 + tw + 4, ty + 7 - title_scale_px + 2))
        else:
            draw_text(big, name, big.width // 2 - tw // 2, 20, title_color)
        big = big.resize((big.width * 2, big.height * 2), Image.NEAREST)
        scene.alpha_composite(big, (ox, 52))
        if subtitle:
            draw_text(scene, subtitle.upper(), ox + c - text_width(subtitle.upper(), False) // 2, 136,
                      (200, 200, 200), bold=False)
        lab = ImageDraw.Draw(scene)
        lab.text((ox + 6, 4), "CON PACK" if with_pack else "SIN PACK (vanilla)", fill=(255, 255, 255, 255))
    scene.resize((scene.width * 3, scene.height * 3), Image.NEAREST).save(path)
