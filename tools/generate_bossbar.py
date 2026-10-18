#!/usr/bin/env python3
"""
Genera la textura de la bossbar de Heracles (estilo griego: oro con meandro)
y una vista previa.

Sustituye los sprites vanilla de la barra AMARILLA (YELLOW) de 1.21.x:
  assets/minecraft/textures/gui/sprites/boss_bar/yellow_background.png
  assets/minecraft/textures/gui/sprites/boss_bar/yellow_progress.png

Vanilla mide 182x5; aqui se dibuja a 4x (728x20) para tener mas detalle.
Minecraft la escala sola al tamano de la barra.

Uso: python3 tools/generate_bossbar.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent / "Heracles"
OUT = ROOT / "ResourcePack/HeraclesPack/assets/minecraft/textures/gui/sprites/boss_bar"
PREVIEW = ROOT / "preview/bossbar.png"

S = 4                      # escala respecto a vanilla
W, H = 182 * S, 5 * S      # 728 x 20
SEGMENTS = 10

# Meandro griego (6x6 celdas de 2 px); se repite en horizontal
MEANDER = [
    "XXXXX.",
    "X...X.",
    "X.X.X.",
    "X.XXX.",
    "X.....",
    "XXXXXX",
]
CELL = 2
TILE_W = len(MEANDER[0]) * CELL
TILE_TOP = 4               # filas 4..15 (12 px) dentro del relleno 2..17


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient(stops, t):
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        if t <= t1:
            return lerp(c0, c1, (t - t0) / (t1 - t0))
    return stops[-1][1]


def bar(fill_stops, meander, notch, border, highlight, shadow):
    img = Image.new("RGBA", (W, H))
    px = img.load()
    for y in range(H):
        row = gradient(fill_stops, (y - 2) / (H - 5))
        for x in range(W):
            px[x, y] = row + (255,)

    # meandro
    for x in range(W):
        cx = (x % TILE_W) // CELL
        for r, line in enumerate(MEANDER):
            if line[cx] == "X":
                for dy in range(CELL):
                    px[x, TILE_TOP + r * CELL + dy] = meander + (255,)

    # brillo arriba y sombra abajo
    for x in range(W):
        px[x, 2] = highlight + (255,)
        px[x, H - 3] = shadow + (255,)

    # separadores de los 10 segmentos
    for k in range(1, SEGMENTS):
        sx = round(W * k / SEGMENTS)
        for y in range(2, H - 2):
            px[sx - 1, y] = notch + (255,)
            px[sx, y] = highlight + (255,) if y == 2 else notch + (255,)

    # borde de bronce oscuro
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, 1], fill=border)
    d.rectangle([0, H - 2, W - 1, H - 1], fill=border)
    d.rectangle([0, 0, 1, H - 1], fill=border)
    d.rectangle([W - 2, 0, W - 1, H - 1], fill=border)
    return img


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    border = (43, 26, 8)

    progress = bar(
        fill_stops=[(0, (255, 228, 122)), (0.45, (235, 178, 48)), (1, (150, 96, 14))],
        meander=(255, 214, 92),
        notch=(120, 74, 10),
        border=border,
        highlight=(255, 245, 190),
        shadow=(110, 66, 6),
    )
    background = bar(
        fill_stops=[(0, (58, 44, 26)), (1, (30, 22, 12))],
        meander=(86, 64, 30),
        notch=(22, 15, 6),
        border=border,
        highlight=(78, 60, 34),
        shadow=(20, 14, 6),
    )
    progress.save(OUT / "yellow_progress.png")
    background.save(OUT / "yellow_background.png")

    # vista previa: barra al 60 % sobre fondo oscuro, escalada x2
    pw, ph = W + 120, 110
    prev = Image.new("RGBA", (pw, ph), (24, 28, 36, 255))
    ox, oy = 60, 62
    prev.alpha_composite(background, (ox, oy))
    fill = round(W * 0.6)
    prev.alpha_composite(progress.crop((0, 0, fill, H)), (ox, oy))
    d = ImageDraw.Draw(prev)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
    parts = [("⚔ ", (255, 170, 0)), ("HERACLES", (255, 255, 85)), (" • ", (85, 85, 85)),
             ("Campeón del Olimpo", (255, 170, 0)), (" ⚔", (255, 170, 0))]
    total = sum(d.textlength(t, font=font) for t, _ in parts)
    x = (pw - total) / 2
    for t, c in parts:
        d.text((x + 2, 22 + 2), t, font=font, fill=(40, 40, 10))
        d.text((x, 22), t, font=font, fill=c)
        x += d.textlength(t, font=font)
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    prev.save(PREVIEW)
    print("OK:", OUT, PREVIEW)


if __name__ == "__main__":
    main()
