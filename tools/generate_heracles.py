#!/usr/bin/env python3
"""
Genera el blueprint de ModelEngine para HERACLES (heracles.bbmodel).

- Formato Blockbench "Generic Model" (free), compatible con ModelEngine R4 (Java 1.21.x).
- Textura pintada proceduralmente (2 px por unidad) e incrustada en el .bbmodel.
- Huesos con tags de ModelEngine: hitbox (hitbox + altura de ojos), h_ (cabeza).
- Animaciones: idle, walk, spawn, death (estados por defecto) + estados de combate.

Uso:  python3 tools/generate_heracles.py  [ruta_salida.bbmodel]
"""
import base64
import io
import json
import math
import random
import sys
import uuid as uuidlib
from pathlib import Path

from PIL import Image

PX = 2            # pixeles de textura por unidad de modelo
ATLAS_W = 128     # ancho del atlas en unidades UV (=> 256 px)
RNG = random.Random(1337)


def uid():
    return str(uuidlib.UUID(int=RNG.getrandbits(128), version=4))


# ---------------------------------------------------------------------------
# Paleta
# ---------------------------------------------------------------------------
MAT = {
    "skin":     (198, 138, 92),
    "gold":     (226, 176, 48),
    "pelt":     (192, 146, 70),
    "mane":     (118, 70, 32),
    "hair":     (82, 52, 32),
    "wood":     (112, 74, 42),
    "leather":  (118, 76, 44),
    "white":    (232, 226, 208),
    "red":      (150, 30, 28),
    "hitbox":   (255, 255, 255),
}


def clamp(v):
    return max(0, min(255, int(v)))


def mul(c, f):
    return tuple(clamp(x * f) for x in c)


def mix(a, b, t):
    return tuple(clamp(a[i] * (1 - t) + b[i] * t) for i in range(3))


# ---------------------------------------------------------------------------
# Modelo: huesos y cubos
# ---------------------------------------------------------------------------
class Bone:
    def __init__(self, name, origin, parent=None, rotation=(0, 0, 0)):
        self.name = name
        self.origin = list(origin)
        self.rotation = list(rotation)
        self.uuid = uid()
        self.children = []   # Bone o Cube, en orden
        self.parent = parent
        if parent:
            parent.children.append(self)


class Cube:
    def __init__(self, bone, name, frm, to, mat, decor=None, inflate=0):
        self.bone = bone
        self.name = name
        self.frm = list(frm)
        self.to = list(to)
        self.mat = mat
        self.decor = decor or {}
        self.inflate = inflate
        self.uuid = uid()
        self.uv = {}
        bone.children.append(self)

    @property
    def size(self):
        return [self.to[i] - self.frm[i] for i in range(3)]


CUBES = []


def cube(bone, name, frm, to, mat, **kw):
    c = Cube(bone, name, frm, to, mat, **kw)
    CUBES.append(c)
    return c


def mirror_x(v):
    return [-v[0], v[1], v[2]]


def cube_lr(bone_r, bone_l, name, frm, to, mat, **kw):
    """Crea un cubo en el lado derecho (+X) y su espejo en el izquierdo (-X)."""
    cube(bone_r, "right_" + name, frm, to, mat, **kw)
    cube(bone_l, "left_" + name, [-to[0], frm[1], frm[2]], [-frm[0], to[1], to[2]], mat, **kw)


# El frente del modelo mira hacia el NORTE (-Z), como pide ModelEngine.
# El lado derecho del personaje es +X.
root = Bone("root", (0, 0, 0))

hitbox = Bone("hitbox", (0, 42, 0), root)       # pivot Y = altura de los ojos
cube(hitbox, "hitbox", (-12, 0, -12), (12, 46, 12), "hitbox")

# ---------------- Piernas ----------------
legs = {}
for side, sx in (("right", 1), ("left", -1)):
    leg = Bone(f"{side}_leg", (4.5 * sx, 18, 0), root)
    lower = Bone(f"{side}_lower_leg", (4.5 * sx, 9.5, 0), leg)
    legs[side] = (leg, lower)

cube_lr(legs["right"][0], legs["left"][0], "thigh", (1, 9, -3.5), (8, 18.5, 3.5), "skin", decor={"north": "thigh"})
cube_lr(legs["right"][1], legs["left"][1], "shin", (1.5, 1.5, -3), (7.5, 9.5, 3), "skin")
cube_lr(legs["right"][1], legs["left"][1], "greave", (1.25, 3, -3.5), (7.75, 9, -2.5), "gold", decor={"north": "greave"})
cube_lr(legs["right"][1], legs["left"][1], "strap", (1.25, 1.5, -3.25), (7.75, 3, 3.25), "leather", decor={"all": "straps"})
cube_lr(legs["right"][1], legs["left"][1], "sandal", (1, 0, -4.5), (8, 1.5, 3.5), "leather", decor={"up": "sandal"})

# ---------------- Cuerpo ----------------
body = Bone("body", (0, 18, 0), root)
waist = Bone("waist", (0, 18, 0), body)
cube(waist, "belt", (-10, 17, -5.5), (10, 20, 5.5), "gold", decor={"all": "meander"})
cube(waist, "buckle", (-2, 17.25, -6.25), (2, 19.75, -5.5), "gold", decor={"north": "buckle"})
skirt_front = Bone("skirt_front", (0, 17.5, -5.5), waist)
cube(skirt_front, "skirt_front", (-9.5, 10, -6.25), (9.5, 17.5, -5.25), "leather", decor={"all": "pteruges"})
skirt_back = Bone("skirt_back", (0, 17.5, 5.5), waist)
cube(skirt_back, "skirt_back", (-9.5, 10, 5.25), (9.5, 17.5, 6.25), "leather", decor={"all": "pteruges"})
cube(waist, "skirt_right", (9.25, 11, -5), (10.25, 17.5, 5), "leather", decor={"all": "pteruges"})
cube(waist, "skirt_left", (-10.25, 11, -5), (-9.25, 17.5, 5), "leather", decor={"all": "pteruges"})

torso = Bone("torso", (0, 20, 0), body)
cube(torso, "chest", (-10, 20, -5), (10, 37, 5), "skin", decor={"north": "chest", "south": "back"})
cube(torso, "pecs", (-9, 30, -6), (9, 35.5, -5), "skin", decor={"north": "pecs"})
cube(torso, "abs", (-5, 20.5, -5.75), (5, 30, -5), "skin", decor={"north": "abs"})
cube(torso, "traps", (-7, 37, -3), (7, 38.5, 3.5), "skin")
cube(torso, "neck", (-3, 37, -3), (3, 40, 3), "skin")
# Patas del leon de Nemea colgando sobre el pecho
cube(torso, "paw_right", (5.5, 28, -7), (9.5, 37.5, -5), "pelt", decor={"all": "fur", "north": "paw"})
cube(torso, "paw_left", (-9.5, 28, -7), (-5.5, 37.5, -5), "pelt", decor={"all": "fur", "north": "paw"})

# Piel del leon (capa) con cola
pelt = Bone("pelt", (0, 37.5, 6), torso)
cube(pelt, "pelt_upper", (-10.5, 23, 5), (10.5, 38.5, 7), "pelt", decor={"all": "fur"})
pelt_lower = Bone("pelt_lower", (0, 23, 6), pelt)
cube(pelt_lower, "pelt_lower", (-9.5, 9, 5.5), (9.5, 23, 7), "pelt", decor={"all": "fur", "south": "fur_hem"})
tail = Bone("tail", (0, 10, 6.5), pelt_lower)
cube(tail, "tail", (-0.75, 3, 6), (0.75, 10, 7.5), "pelt", decor={"all": "fur"})
cube(tail, "tail_tuft", (-1.25, 0.5, 5.5), (1.25, 3.5, 8), "mane", decor={"all": "fur"})

# ---------------- Cabeza ----------------
head = Bone("h_head", (0, 38, 0), torso)
cube(head, "head", (-5, 38, -5), (5, 48, 5), "skin", decor={"north": "face"})
cube(head, "beard", (-5, 35.5, -6), (5, 41, -5), "hair", decor={"all": "curls", "north": "beard"})
cube(head, "mustache", (-3.5, 41, -5.75), (3.5, 42, -5), "hair", decor={"all": "curls"})
cube(head, "hair_back", (-5.5, 39, 2), (5.5, 46, 5.5), "hair", decor={"all": "curls"})
cube(head, "lion_hood", (-6, 45, -6), (6, 50.5, 6), "pelt", decor={"all": "fur", "north": "lion_brow", "up": "fur_top"})
cube(head, "lion_snout", (-3.5, 45, -8.5), (3.5, 48, -6), "pelt", decor={"all": "fur", "north": "lion_snout", "up": "lion_snout_top"})
cube(head, "lion_ear_right", (4, 50.5, -3), (6, 52, -1.5), "pelt", decor={"north": "ear"})
cube(head, "lion_ear_left", (-6, 50.5, -3), (-4, 52, -1.5), "pelt", decor={"north": "ear"})
cube(head, "mane_right", (5, 37.5, -4.5), (6.75, 50, 6), "mane", decor={"all": "fur"})
cube(head, "mane_left", (-6.75, 37.5, -4.5), (-5, 50, 6), "mane", decor={"all": "fur"})
cube(head, "mane_back", (-6.75, 36.5, 5), (6.75, 50, 7.25), "mane", decor={"all": "fur"})

tag = Bone("tag_name", (0, 55, 0), root)  # hueso de nametag (opcional)

# ---------------- Brazos ----------------
arms = {}
for side, sx in (("right", 1), ("left", -1)):
    arm = Bone(f"{side}_arm", (12.5 * sx, 35, 0), torso)
    fore = Bone(f"{side}_forearm", (13 * sx, 26, 0), arm)
    hand = Bone(f"{side}_hand", (13 * sx, 17, 0), fore)
    arms[side] = (arm, fore, hand)

R, L = arms["right"], arms["left"]
cube_lr(R[0], L[0], "shoulder", (10, 30.5, -4), (16, 38, 4), "skin", decor={"north": "deltoid"})
cube_lr(R[0], L[0], "upper_arm", (10.5, 25.5, -3), (15.5, 31, 3), "skin", decor={"north": "bicep"})
cube_lr(R[1], L[1], "forearm", (10.5, 17, -3), (15.5, 26, 3), "skin")
cube_lr(R[1], L[1], "bracer", (10.25, 17.75, -3.25), (15.75, 23.5, 3.25), "gold", decor={"all": "bracer"})
cube_lr(R[2], L[2], "fist", (10.5, 12.5, -3), (15.5, 17, 3), "skin", decor={"north": "fist"})
# Hombrera: piel de leon en el hombro izquierdo, oro en el derecho
cube(R[0], "pauldron", (9.5, 34, -4.5), (16.5, 38.75, 4.5), "gold", decor={"all": "pauldron"})
cube(L[0], "pelt_shoulder", (-16.75, 33, -4.75), (-9.5, 39, 4.75), "pelt", decor={"all": "fur"})

# ---------------- Garrote ----------------
# Cuelga hacia abajo desde el puno; en pose de reposo apunta hacia adelante/abajo.
club = Bone("club", (13, 15, 0), R[2], rotation=(55, 0, 0))
cube(club, "club_grip", (12, 7, -1), (14, 17.5, 1), "leather", decor={"all": "grip"})
cube(club, "club_shaft", (11.5, 0, -1.5), (14.5, 7, 1.5), "wood", decor={"all": "wood"})
cube(club, "club_head", (11, -9, -2), (15, 0, 2), "wood", decor={"all": "wood"})
cube(club, "club_tip", (11.5, -10.5, -1.5), (14.5, -9, 1.5), "wood", decor={"all": "wood"})
cube(club, "knot_1", (10, -6, -1), (11, -4, 1), "wood", decor={"all": "knot"})
cube(club, "knot_2", (15, -3, -1), (16, -1, 0.5), "wood", decor={"all": "knot"})
cube(club, "knot_3", (12, -8, -3), (14, -6, -2), "wood", decor={"all": "knot"})
cube(club, "knot_4", (12.5, -2, 2), (14, 0, 3), "wood", decor={"all": "knot"})
cube(club, "knot_5", (12, 3, -2.5), (13.5, 4.5, -1.5), "wood", decor={"all": "knot"})
cube(club, "club_band", (11.25, 6, -1.75), (14.75, 7.5, 1.75), "gold", decor={"all": "bracer"})


# ---------------------------------------------------------------------------
# Atlas UV (layout tipo "box" por cubo, colocado con un empaquetador por filas)
# ---------------------------------------------------------------------------
def pack():
    items = []
    for c in CUBES:
        if c.mat == "hitbox":
            continue
        w, h, d = c.size
        items.append((c, 2 * (d + w), d + h))
    items.sort(key=lambda t: -t[2])
    x = y = 0.0
    row_h = 0.0
    for c, rw, rh in items:
        if x + rw > ATLAS_W:
            x = 0.0
            y += row_h
            row_h = 0.0
        c.region = (x, y)
        w, h, d = c.size
        u, v = x, y
        c.uv = {
            "east":  [u, v + d, u + d, v + d + h],
            "north": [u + d, v + d, u + d + w, v + d + h],
            "west":  [u + d + w, v + d, u + 2 * d + w, v + d + h],
            "south": [u + 2 * d + w, v + d, u + 2 * d + 2 * w, v + d + h],
            "up":    [u + d, v, u + d + w, v + d],
            "down":  [u + d + w, v, u + d + 2 * w, v + d],
        }
        x += rw
        row_h = max(row_h, rh)
    total_h = y + row_h
    # El hitbox no se renderiza: usa un pixel transparente al final del atlas.
    for c in CUBES:
        if c.mat == "hitbox":
            spot = [ATLAS_W - 1, total_h, ATLAS_W, total_h + 1]
            c.uv = {f: list(spot) for f in ("north", "east", "south", "west", "up", "down")}
    total_h += 1
    hh = 16
    while hh < total_h:
        hh *= 2
    return ATLAS_W, hh


# ---------------------------------------------------------------------------
# Pintado de textura
# ---------------------------------------------------------------------------
class Face:
    def __init__(self, img, box, name, cube):
        self.img = img
        self.x0, self.y0, self.x1, self.y1 = box
        self.w = self.x1 - self.x0
        self.h = self.y1 - self.y0
        self.name = name
        self.cube = cube

    def put(self, x, y, col):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.img.putpixel((self.x0 + x, self.y0 + y), col)

    def get(self, x, y):
        return self.img.getpixel((self.x0 + x, self.y0 + y))

    def rect(self, x0, y0, x1, y1, col):
        for yy in range(y0, y1):
            for xx in range(x0, x1):
                self.put(xx, yy, col)

    def shade(self, x, y, f):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.put(x, y, mul(self.get(x, y), f))


def base_fill(f, mat):
    col = MAT[mat]
    noise = {"skin": 8, "gold": 10, "pelt": 16, "mane": 16, "hair": 10, "wood": 12,
             "leather": 10, "white": 6, "red": 8, "hitbox": 0}[mat]
    light = {"up": 1.12, "down": 0.72, "north": 1.0, "south": 0.9, "east": 0.95, "west": 0.95}[f.name]
    for y in range(f.h):
        for x in range(f.w):
            n = RNG.uniform(-noise, noise)
            # degradado vertical suave (luz desde arriba)
            g = 1.0
            if f.name not in ("up", "down") and f.h > 2:
                g = 1.06 - 0.14 * (y / (f.h - 1))
            c = tuple(clamp((v + n) * light * g) for v in col)
            f.put(x, y, c)
    if mat == "gold":
        for x in range(f.w):
            f.put(x, 0, mix(f.get(x, 0), (255, 236, 140), 0.6))
            f.put(x, f.h - 1, mul(f.get(x, f.h - 1), 0.7))
    if mat in ("pelt", "mane", "hair"):
        fur(f)
    if mat == "wood":
        wood(f)
    if mat != "hitbox":
        outline(f)


def outline(f, k=0.82):
    for x in range(f.w):
        f.shade(x, 0, k + 0.08)
        f.shade(x, f.h - 1, k)
    for y in range(1, f.h - 1):
        f.shade(0, y, k + 0.05)
        f.shade(f.w - 1, y, k + 0.05)


def fur(f):
    for x in range(f.w):
        start = RNG.randint(0, 3)
        for y in range(start, f.h, RNG.randint(3, 5)):
            f.shade(x, y, RNG.choice((0.8, 0.86, 1.12)))
            if y + 1 < f.h:
                f.shade(x, y + 1, 0.9)


def wood(f):
    for x in range(f.w):
        if x % 3 == 1:
            for y in range(f.h):
                f.shade(x, y, 0.84)
    for _ in range(max(1, f.w * f.h // 40)):
        x, y = RNG.randrange(f.w), RNG.randrange(f.h)
        f.shade(x, y, 0.7)


# ---- decoraciones especificas ----
def d_face(f):
    # Cara 20x20 px; filas 0..5 cubiertas por la capucha (y 45..48) y 12+ por el bigote/barba.
    skin = MAT["skin"]
    brow = (60, 38, 24)
    for x in (3, 4, 5, 6, 7):
        f.put(x, 6, brow)
        f.put(f.w - 1 - x, 6, brow)
    # ojos brillantes (sangre divina)
    for ex in (4, 13):
        f.rect(ex, 7, ex + 3, 9, (245, 240, 225))
        f.rect(ex + (1 if ex < 10 else 0), 7, ex + (3 if ex < 10 else 2), 9, (255, 196, 40))
        f.put(ex + (2 if ex < 10 else 0), 8, (120, 70, 10))
        f.rect(ex, 9, ex + 3, 10, mul(skin, 0.78))
    # nariz
    f.rect(9, 7, 11, 11, mul(skin, 1.08))
    f.rect(8, 10, 9, 12, mul(skin, 0.8))
    f.rect(11, 10, 12, 12, mul(skin, 0.8))
    f.rect(9, 11, 11, 12, mul(skin, 0.7))
    # mejillas
    f.rect(2, 10, 6, 12, mul(skin, 0.93))
    f.rect(14, 10, 18, 12, mul(skin, 0.93))


def d_beard(f):
    for y in range(f.h):
        for x in range(f.w):
            if (x + y * 2) % 5 == 0:
                f.shade(x, y, 1.25)
    # boca
    f.rect(f.w // 2 - 3, 0, f.w // 2 + 3, 1, (60, 28, 22))


def d_curls(f):
    for y in range(0, f.h, 2):
        for x in range((y // 2) % 2, f.w, 3):
            f.shade(x, y, 1.3)


def d_chest(f):
    skin = MAT["skin"]
    w = f.w
    # linea central del torso y sombra de costillas laterales
    for y in range(0, f.h):
        f.put(w // 2, y, mul(f.get(w // 2, y), 0.85))
    for y in range(6, f.h - 4, 4):
        for x in range(1, 5):
            f.shade(x, y, 0.82)
            f.shade(w - 1 - x, y, 0.82)
    # cinturas (oblicuos)
    for i in range(6):
        f.shade(9 - i, f.h - 3 - i, 0.85)
        f.shade(w - 10 + i, f.h - 3 - i, 0.85)
    _ = skin


def d_back(f):
    w = f.w
    for y in range(f.h):
        f.shade(w // 2, y, 0.82)
    for i in range(10):
        f.shade(6 + i // 2, 4 + i, 0.88)
        f.shade(w - 7 - i // 2, 4 + i, 0.88)


def d_pecs(f):
    w = f.w
    for y in range(f.h):
        f.shade(w // 2, y, 0.75)
        f.shade(w // 2 - 1, y, 0.9)
    for x in range(2, w - 2):
        f.shade(x, f.h - 1, 0.7)
        f.shade(x, f.h - 2, 0.85)
    for x in range(1, w - 1):
        f.shade(x, 0, 1.1)


def d_abs(f):
    w = f.w
    for y in range(f.h):
        f.shade(w // 2, y, 0.78)
    for y in (4, 9, 14):
        for x in range(1, w - 1):
            f.shade(x, y, 0.8)
    for y in range(0, f.h):
        for x in range(1, w - 1):
            if y % 5 in (1, 2) and x not in (w // 2,):
                f.shade(x, y, 1.06)


def d_meander(f):
    # Greca griega en oro oscuro
    dark = mul(MAT["gold"], 0.55)
    if f.h < 4:
        return
    y0 = 1
    for x in range(0, f.w):
        f.put(x, y0, dark)
        f.put(x, f.h - 2, dark)
    pattern = ["#####.", "#...#.", "#.#.#.", "#.###."]
    for x in range(f.w):
        for yy in range(min(4, f.h - 4)):
            ch = pattern[yy][x % 6]
            if ch == "#":
                f.put(x, y0 + 1 + yy, dark)


def d_buckle(f):
    f.rect(2, 1, f.w - 2, f.h - 1, (250, 220, 110))
    f.rect(3, 2, f.w - 3, f.h - 2, (180, 40, 30))  # gema roja
    f.put(4, 2, (255, 150, 140))


def d_pteruges(f):
    if f.name in ("up", "down"):
        return
    for x in range(0, f.w, 4):
        for y in range(f.h):
            f.shade(x, y, 0.65)
    # remaches dorados al final de cada tira
    for x in range(2, f.w, 4):
        f.put(x, f.h - 3, (240, 196, 70))
        f.put(x, 2, (240, 196, 70))


def d_fur_hem(f):
    for x in range(f.w):
        cut = RNG.randint(0, 3)
        for y in range(f.h - cut, f.h):
            f.put(x, y, mul(MAT["mane"], 0.8))


def d_fur_top(f):
    for _ in range(f.w * f.h // 6):
        f.shade(RNG.randrange(f.w), RNG.randrange(f.h), 0.85)


def d_lion_brow(f):
    # frente del leon (sobre la cara de Heracles): ojos oscuros con brillo
    for ex in (2, f.w - 7):
        f.rect(ex, 3, ex + 5, 5, (30, 20, 12))
        f.put(ex + 2, 3, (255, 210, 60))
        f.rect(ex - 1, 2, ex + 6, 3, mul(MAT["mane"], 0.9))
    for y in range(5, f.h):
        f.shade(f.w // 2, y, 0.8)


def d_lion_snout(f):
    # hocico: nariz oscura arriba, boca/encias abajo
    w = f.w
    f.rect(w // 2 - 3, 0, w // 2 + 3, 3, (48, 30, 26))
    f.rect(w // 2 - 1, 3, w // 2 + 1, 4, (48, 30, 26))
    f.rect(1, f.h - 2, w - 1, f.h, (120, 40, 40))
    for x in range(2, w - 2, 3):
        f.put(x, f.h - 2, MAT["white"])
    for x in range(1, w - 1, 2):
        f.shade(x, f.h // 2, 0.85)


def d_lion_snout_top(f):
    for x in range(f.w):
        f.shade(x, f.h // 2, 0.85)


def d_ear(f):
    f.rect(1, 1, f.w - 1, f.h - 1, mul(MAT["mane"], 0.7))


def d_paw(f):
    # garras blancas en el extremo inferior
    for x in range(1, f.w - 1, 2):
        f.put(x, f.h - 1, MAT["white"])
        f.put(x, f.h - 2, MAT["white"])
    for x in range(0, f.w, 2):
        f.shade(x, f.h - 4, 0.75)


def d_grip(f):
    for y in range(0, f.h, 3):
        for x in range(f.w):
            f.shade(x, (y + x // 2) % f.h, 0.7)


def d_wood(f):
    pass


def d_knot(f):
    f.rect(1, 1, max(2, f.w - 1), max(2, f.h - 1), mul(MAT["wood"], 0.6))


def d_bracer(f):
    if f.name in ("up", "down"):
        return
    dark = mul(MAT["gold"], 0.6)
    for x in range(f.w):
        f.put(x, 2, dark)
        f.put(x, f.h - 3, dark)
    for x in range(1, f.w, 4):
        f.put(x, f.h // 2, (255, 240, 170))


def d_greave(f):
    w = f.w
    for y in range(f.h):
        f.put(w // 2, y, (255, 236, 150))
        f.shade(w // 2 - 1, y, 0.8)
        f.shade(w // 2 + 1, y, 0.8)
    for x in range(1, w - 1, 3):
        f.shade(x, f.h // 2, 0.75)


def d_straps(f):
    if f.name in ("up", "down"):
        return
    for x in range(f.w):
        f.shade(x, 1, 0.65)
        f.shade(x, f.h - 2, 0.65)
    for x in range(1, f.w, 4):
        for y in range(f.h):
            f.shade(x, y, 0.75)


def d_sandal(f):
    for x in range(f.w):
        f.shade(x, 0, 0.8)


def d_thigh(f):
    for y in range(f.h):
        f.shade(f.w // 2, y, 0.9)


def d_deltoid(f):
    for x in range(f.w):
        f.shade(x, f.h - 1, 0.8)


def d_bicep(f):
    for y in range(2, f.h - 2):
        f.shade(f.w // 2, y, 1.1)
    for x in range(1, f.w - 1):
        f.shade(x, f.h - 1, 0.8)


def d_fist(f):
    for x in range(1, f.w - 1, 3):
        for y in range(2, f.h - 1):
            f.shade(x, y, 0.82)


def d_pauldron(f):
    if f.name == "down":
        return
    dark = mul(MAT["gold"], 0.6)
    for y in range(3, f.h, 4):
        for x in range(f.w):
            f.put(x, y, dark)
    if f.name in ("north", "south", "east", "west"):
        f.put(f.w // 2, 1, (180, 40, 30))


DECOR = {k[2:]: v for k, v in globals().items() if k.startswith("d_")}
DECOR["fur"] = lambda f: None


def paint(tex_w, tex_h):
    img = Image.new("RGBA", (tex_w * PX, tex_h * PX), (0, 0, 0, 0))
    for c in CUBES:
        for face, (u0, v0, u1, v1) in c.uv.items():
            box = (round(u0 * PX), round(v0 * PX), round(u1 * PX), round(v1 * PX))
            if box[2] - box[0] <= 0 or box[3] - box[1] <= 0:
                continue
            if c.mat == "hitbox":
                continue
            f = Face(img, box, face, c)
            base_fill(f, c.mat)
            for key in ("all", face):
                name = c.decor.get(key)
                if name and name in DECOR:
                    DECOR[name](f)
    return img


# ---------------------------------------------------------------------------
# Animaciones
# ---------------------------------------------------------------------------
BONES = {}


def collect(b):
    BONES[b.name] = b
    for ch in b.children:
        if isinstance(ch, Bone):
            collect(ch)


collect(root)


class Anim:
    def __init__(self, name, length, loop="once", snapping=20):
        self.name = name
        self.length = length
        self.loop = loop
        self.snapping = snapping
        self.tracks = {}   # (bone, channel) -> {time: (x,y,z,interp)}

    def k(self, bone, channel, t, x=0, y=0, z=0, interp="catmullrom"):
        assert bone in BONES, bone
        self.tracks.setdefault((bone, channel), {})[round(t, 4)] = (x, y, z, interp)
        return self

    def rot(self, bone, t, x=0, y=0, z=0, i="catmullrom"):
        return self.k(bone, "rotation", t, x, y, z, i)

    def pos(self, bone, t, x=0, y=0, z=0, i="catmullrom"):
        return self.k(bone, "position", t, x, y, z, i)

    def scl(self, bone, t, x=1, y=1, z=1, i="linear"):
        return self.k(bone, "scale", t, x, y, z, i)

    def pose(self, t, poses, i="catmullrom"):
        """poses: {bone: (rx,ry,rz)} o {bone: {'r':(..), 'p':(..)}}"""
        for b, v in poses.items():
            if isinstance(v, dict):
                if "r" in v:
                    self.rot(b, t, *v["r"], i=i)
                if "p" in v:
                    self.pos(b, t, *v["p"], i=i)
            else:
                self.rot(b, t, *v, i=i)
        return self

    def to_json(self):
        animators = {}
        for (bone, channel), kfs in self.tracks.items():
            b = BONES[bone]
            an = animators.setdefault(b.uuid, {"name": bone, "type": "bone", "keyframes": []})
            for t in sorted(kfs):
                x, y, z, interp = kfs[t]
                an["keyframes"].append({
                    "channel": channel,
                    "data_points": [{"x": fmt(x), "y": fmt(y), "z": fmt(z)}],
                    "uuid": uid(),
                    "time": t,
                    "color": -1,
                    "interpolation": interp,
                })
        return {
            "uuid": uid(),
            "name": self.name,
            "loop": self.loop,
            "override": False,
            "length": self.length,
            "snapping": self.snapping,
            "selected": False,
            "anim_time_update": "",
            "blend_weight": "",
            "start_delay": "",
            "loop_delay": "",
            "animators": animators,
        }


def fmt(v):
    v = round(float(v), 3)
    return str(int(v)) if v == int(v) else str(v)


ZERO_BONES = ["body", "torso", "h_head", "right_arm", "right_forearm", "right_hand", "club",
              "left_arm", "left_forearm", "left_hand", "right_leg", "right_lower_leg",
              "left_leg", "left_lower_leg", "pelt", "pelt_lower", "tail", "skirt_front", "skirt_back"]


def rest(a, t, bones=None, i="catmullrom"):
    for b in bones or ZERO_BONES:
        a.rot(b, t, 0, 0, 0, i=i)
    a.pos("body", t, 0, 0, 0, i=i)
    return a


# Convenciones (Blockbench, modelo mirando al norte):
#   rot X negativo en brazos/piernas  -> se mueven hacia ADELANTE
#   rot X positivo en torso/cabeza     -> se inclinan hacia ADELANTE
#   rot Z positivo en brazo derecho   -> se abre hacia afuera (izq. usa Z negativo)
ANIMS = []


def anim(*a, **kw):
    x = Anim(*a, **kw)
    ANIMS.append(x)
    return x


# ---- IDLE (loop) ----
a = anim("idle", 3.0, "loop")
for t, s in ((0, 0), (1.5, 1), (3.0, 0)):
    a.pos("body", t, 0, -0.4 * s, 0)
    a.rot("torso", t, -2 * s, 0, 0)
    a.rot("h_head", t, 2 * s, 3 * s - 1.5, 0)
    a.rot("right_arm", t, 0, 0, 3 + 2 * s)
    a.rot("left_arm", t, 0, 0, -3 - 2 * s)
    a.rot("right_forearm", t, -4 - 3 * s, 0, 0)
    a.rot("left_forearm", t, -4 - 3 * s, 0, 0)
    a.rot("pelt", t, 2 + 2 * s, 0, 0)
    a.rot("pelt_lower", t, 2 * s, 0, 0)
for t, z in ((0, -6), (0.75, 0), (1.5, 6), (2.25, 0), (3.0, -6)):
    a.rot("tail", t, 8, 0, z)

# ---- WALK (loop) ----
def walk(name, length, leg, arm, bob, lean, extra_tail=10):
    a = anim(name, length, "loop")
    h = length / 2
    q = length / 4
    for t, s in ((0, 1), (h, -1), (length, 1)):
        a.rot("right_leg", t, -leg * s, 0, 0)
        a.rot("left_leg", t, leg * s, 0, 0)
        a.rot("right_arm", t, arm * s, 0, 4)
        a.rot("left_arm", t, -arm * s, 0, -4)
        a.rot("torso", t, lean, -5 * s, 0)
        a.rot("h_head", t, -lean * 0.6, 4 * s, 0)
        a.rot("skirt_front", t, -10 * max(s, 0) - 10 * max(-s, 0), 0, 0)
    for t, s in ((0, 0), (q, 1), (h, 0), (h + q, 1), (length, 0)):
        a.pos("body", t, 0, -bob * s, 0)
        a.rot("pelt", t, 6 + 4 * s, 0, 0)
        a.rot("pelt_lower", t, 4 + 4 * s, 0, 0)
    # rodillas: se doblan al pasar la pierna hacia atras
    a.rot("right_lower_leg", 0, 0, 0, 0)
    a.rot("right_lower_leg", q, 10, 0, 0)
    a.rot("right_lower_leg", h, 35, 0, 0)
    a.rot("right_lower_leg", h + q, 15, 0, 0)
    a.rot("right_lower_leg", length, 0, 0, 0)
    a.rot("left_lower_leg", 0, 35, 0, 0)
    a.rot("left_lower_leg", q, 15, 0, 0)
    a.rot("left_lower_leg", h, 0, 0, 0)
    a.rot("left_lower_leg", h + q, 10, 0, 0)
    a.rot("left_lower_leg", length, 35, 0, 0)
    for t, z in ((0, -extra_tail), (h, extra_tail), (length, -extra_tail)):
        a.rot("tail", t, 15, 0, z)
    return a


walk("walk", 1.2, leg=25, arm=18, bob=0.8, lean=4)

# ---- ATTACK: golpe vertical con el garrote (impacto en 0.5s = 10 ticks) ----
a = anim("attack", 1.0, "once")
rest(a, 0)
a.pose(0.35, {"right_arm": (-165, 0, 10), "right_forearm": (-20, 0, 0), "torso": (-12, 18, 0),
              "h_head": (-8, -10, 0), "left_arm": (-30, 0, -15), "body": {"p": (0, 0.5, 0)},
              "pelt": (-6, 0, 0)})
a.pose(0.5, {"right_arm": (-35, 0, 0), "right_forearm": (-5, 0, 0), "torso": (22, -8, 0),
             "h_head": (-14, 0, 0), "left_arm": (20, 0, -20), "body": {"p": (0, -1.2, 0)},
             "right_leg": (-25, 0, 0), "right_lower_leg": (35, 0, 0), "left_leg": (-10, 0, 0),
             "left_lower_leg": (25, 0, 0), "pelt": (25, 0, 0)}, i="linear")
a.pose(0.62, {"right_arm": (-38, 0, 0), "torso": (20, -8, 0), "body": {"p": (0, -1.1, 0)}})
rest(a, 1.0)

# ---- QUAKE: salto y golpe a dos manos contra el suelo (impacto en 1.0s = 20 ticks) ----
a = anim("quake", 1.6, "once")
rest(a, 0)
a.pose(0.45, {"right_arm": (-170, 0, -10), "left_arm": (-170, 0, 25), "right_forearm": (-15, 0, 0),
              "left_forearm": (-15, 0, 0), "torso": (-6, 0, 0), "h_head": (-12, 0, 0),
              "body": {"p": (0, -2, 0)}, "right_leg": (-30, 0, 0), "left_leg": (-30, 0, 0),
              "right_lower_leg": (55, 0, 0), "left_lower_leg": (55, 0, 0)})
a.pose(0.75, {"right_arm": (-175, 0, -10), "left_arm": (-175, 0, 25), "torso": (-9, 0, 0),
              "body": {"p": (0, 7, 0)}, "right_leg": (-10, 0, 0), "left_leg": (5, 0, 0),
              "right_lower_leg": (20, 0, 0), "left_lower_leg": (30, 0, 0), "pelt": (25, 0, 0),
              "pelt_lower": (15, 0, 0)})
a.pose(1.0, {"right_arm": (-30, 0, -10), "left_arm": (-30, 0, 25), "right_forearm": (-5, 0, 0),
             "left_forearm": (-5, 0, 0), "torso": (32, 0, 0), "h_head": (-25, 0, 0),
             "body": {"p": (0, -2.5, 0)}, "right_leg": (-35, 0, 0), "left_leg": (-35, 0, 0),
             "right_lower_leg": (60, 0, 0), "left_lower_leg": (60, 0, 0), "pelt": (-10, 0, 0),
             "pelt_lower": (-10, 0, 0)}, i="linear")
a.pose(1.15, {"torso": (30, 0, 0), "body": {"p": (0, -2.3, 0)}})
rest(a, 1.6)

# ---- ROAR: grito al Olimpo (rugido en 0.4s = 8 ticks) ----
a = anim("roar", 2.0, "once")
rest(a, 0)
open_pose = {"torso": (-16, 0, 0), "h_head": (-32, 0, 0), "right_arm": (-25, 0, 65),
             "left_arm": (-25, 0, -65), "right_forearm": (-35, 0, 0), "left_forearm": (-35, 0, 0),
             "body": {"p": (0, 0.6, 0)}, "pelt": (-8, 0, 0), "tail": (30, 0, 0)}
a.pose(0.4, open_pose)
for i, t in enumerate([0.5 + 0.1 * n for n in range(11)]):
    s = 1 if i % 2 == 0 else -1
    a.rot("torso", t, -16, 0, 1.5 * s, i="linear")
    a.rot("h_head", t, -32, 2 * s, 0, i="linear")
a.pose(1.6, open_pose)
rest(a, 2.0)

# ---- CHARGE: embestida (impacto en 0.5s = 10 ticks) ----
a = anim("charge", 1.2, "once")
rest(a, 0)
a.pose(0.25, {"torso": (25, 0, 0), "h_head": (-20, 0, 0), "body": {"p": (0, -2, 0)},
              "right_arm": (35, 0, 10), "left_arm": (25, 0, -10), "right_leg": (-35, 0, 0),
              "right_lower_leg": (40, 0, 0), "left_leg": (20, 0, 0), "left_lower_leg": (20, 0, 0)})
a.pose(0.5, {"torso": (38, 0, 0), "h_head": (-30, 0, 0), "body": {"p": (0, -1, -3)},
             "right_arm": (-100, 0, 5), "right_forearm": (0, 0, 0), "left_arm": (40, 0, -15),
             "right_leg": (30, 0, 0), "right_lower_leg": (10, 0, 0), "left_leg": (-40, 0, 0),
             "left_lower_leg": (30, 0, 0), "pelt": (40, 0, 0), "pelt_lower": (20, 0, 0)}, i="linear")
a.pose(0.7, {"torso": (35, 0, 0), "body": {"p": (0, -1.2, -3)}, "right_arm": (-95, 0, 5)})
rest(a, 1.2)

# ---- SPAWN: se levanta arrodillado y alza el garrote (3s) ----
a = anim("spawn", 3.0, "once")
KNEEL_LEGS = {"body": {"p": (0, -8, 0)}, "right_leg": (8, 0, 0), "right_lower_leg": (88, 0, 0),
              "left_leg": (-80, 0, 0), "left_lower_leg": (80, 0, 0), "club": (-45, 0, 0)}
kneel = {**KNEEL_LEGS, "torso": (30, 0, 0), "h_head": (25, 0, 0),
         "right_arm": (-10, 0, 8), "left_arm": (-55, 0, -5), "left_forearm": (-30, 0, 0),
         "pelt": (-20, 0, 0)}
a.pose(0, kneel)
a.pose(1.4, {**kneel, "torso": (24, 0, 0), "h_head": (10, 0, 0)})
a.pose(2.1, {"body": {"p": (0, 0, 0)}, "torso": (-8, 0, 0), "h_head": (-15, 0, 0),
             "right_leg": (0, 0, 0), "right_lower_leg": (0, 0, 0), "left_leg": (0, 0, 0),
             "left_lower_leg": (0, 0, 0), "right_arm": (-60, 0, 10), "left_arm": (0, 0, -15),
             "left_forearm": (0, 0, 0), "pelt": (5, 0, 0), "club": (0, 0, 0)})
a.pose(2.45, {"right_arm": (-180, 0, 5), "right_forearm": (-10, 0, 0), "h_head": (-30, 0, 0),
              "torso": (-12, 0, 0), "left_arm": (-20, 0, -40)})
a.pose(2.7, {"right_arm": (-180, 0, 5), "h_head": (-30, 0, 0), "torso": (-12, 0, 0)})
rest(a, 3.0)

# ---- DEATH: cae de rodillas y luego hacia adelante (hold) ----
a = anim("death", 3.0, "hold")
rest(a, 0)
a.rot("root", 0, 0, 0, 0)
a.pose(0.5, {"torso": (-18, 0, 6), "h_head": (-25, 0, 0), "right_arm": (10, 0, 25),
             "left_arm": (10, 0, -25), "body": {"p": (0, 0.5, 0)}})
a.pose(1.2, {"body": {"p": (0, -8.5, 0)}, "torso": (15, 0, 4), "h_head": (20, 0, 0),
             "right_leg": (5, 0, 0), "right_lower_leg": (88, 0, 0), "left_leg": (5, 0, 0),
             "left_lower_leg": (88, 0, 0), "right_arm": (15, 0, 8), "left_arm": (10, 0, -8),
             "club": (-45, 0, 0)}, i="linear")
a.pose(2.0, {"torso": (22, 0, 2), "h_head": (30, 0, 0)})
a.rot("root", 2.0, 0, 0, 0)
a.rot("root", 2.6, 82, 0, 0, i="linear")
a.pos("root", 2.0, 0, 0, 0)
a.pos("root", 2.6, 0, 0, -2, i="linear")
a.pose(2.6, {"torso": (10, 0, 0), "h_head": (-10, 0, 0), "right_arm": (-150, 0, 20),
             "left_arm": (-150, 0, -20)}, i="linear")
a.rot("root", 2.75, 78, 0, 0)
a.rot("root", 3.0, 80, 0, 0)

# ---- PHASE_CHANGE: golpe al suelo + pose de fuerza (2.2s) ----
a = anim("phase_change", 2.2, "once")
rest(a, 0)
a.pose(0.4, {**KNEEL_LEGS, "torso": (30, 0, 0), "left_arm": (-140, 0, 0), "h_head": (-10, 0, 0)})
a.pose(0.6, {**KNEEL_LEGS, "left_arm": (-30, 0, 0), "torso": (42, 0, 0)}, i="linear")
a.pose(1.1, {"body": {"p": (0, 0, 0)}, "torso": (-10, 0, 0), "right_leg": (0, 0, 10),
             "left_leg": (0, 0, -10), "right_lower_leg": (0, 0, 0), "left_lower_leg": (0, 0, 0),
             "right_arm": (0, 0, 85), "left_arm": (0, 0, -85), "right_forearm": (0, 0, 0),
             "left_forearm": (0, 0, 0), "h_head": (-20, 0, 0), "club": (0, 0, 0)})
flex = {"right_arm": (0, 0, 85), "left_arm": (0, 0, -85), "right_forearm": (0, 0, 95),
        "left_forearm": (0, 0, -95), "torso": (-12, 0, 0), "h_head": (-25, 0, 0),
        "right_leg": (0, 0, 10), "left_leg": (0, 0, -10)}
a.pose(1.35, flex)
a.rot("torso", 1.5, -12, 0, 1.5)
a.rot("torso", 1.65, -12, 0, -1.5)
a.pose(1.8, flex)
rest(a, 2.2)

# ---- SUMMON: alza el garrote al cielo para llamar refuerzos (1.6s) ----
a = anim("summon", 1.6, "once")
rest(a, 0)
up = {"right_arm": (-178, 0, 8), "right_forearm": (-5, 0, 0), "left_arm": (-20, 0, -45),
      "left_forearm": (-30, 0, 0), "torso": (-10, 0, 0), "h_head": (-35, 0, 0),
      "body": {"p": (0, 0.5, 0)}, "club": (-55, 0, 0)}
a.pose(0.4, up)
a.pose(1.2, up)
rest(a, 1.6)

# ---- LAST_BREATH: tambalea, cae a una rodilla y se reincorpora (2s) ----
a = anim("last_breath", 2.0, "once")
rest(a, 0)
a.pose(0.3, {"torso": (-10, 0, 8), "h_head": (-15, 0, 0), "body": {"p": (0, 0, 0.5)}})
a.pose(0.8, {**KNEEL_LEGS, "torso": (28, 0, -4), "h_head": (20, 0, 0),
             "left_arm": (-45, 0, -10), "right_arm": (20, 0, 10)})
a.pose(1.3, {**KNEEL_LEGS, "torso": (20, 0, 0), "h_head": (-10, 0, 0)})
a.pose(1.6, {"body": {"p": (0, 0, 0)}, "torso": (-14, 0, 0), "h_head": (-30, 0, 0),
             "right_leg": (0, 0, 0), "right_lower_leg": (0, 0, 0), "left_leg": (0, 0, 0),
             "left_lower_leg": (0, 0, 0), "left_arm": (-10, 0, -50), "right_arm": (-10, 0, 50),
             "club": (0, 0, 0)})
rest(a, 2.0)

# ---- HURT (aditivo corto) ----
a = anim("hurt", 0.4, "once")
rest(a, 0, ["torso", "h_head", "right_arm", "left_arm"])
a.pose(0.1, {"torso": (-8, 0, 3), "h_head": (-10, 0, 0), "right_arm": (8, 0, 6), "left_arm": (8, 0, -6)})
rest(a, 0.4, ["torso", "h_head", "right_arm", "left_arm"])

# ---- IDLE_RAGE / WALK_RAGE (fase 2+): respiracion agitada, encorvado ----
a = anim("idle_rage", 1.4, "loop")
for t, s in ((0, 0), (0.7, 1), (1.4, 0)):
    a.pos("body", t, 0, -0.3 * s - 0.3, 0)
    a.rot("torso", t, 10 - 3 * s, 0, 0)
    a.rot("h_head", t, -8 + 2 * s, 0, 0)
    a.rot("right_arm", t, -8, 0, 10 + 3 * s)
    a.rot("left_arm", t, -8, 0, -10 - 3 * s)
    a.rot("right_forearm", t, -18 - 4 * s, 0, 0)
    a.rot("left_forearm", t, -25 - 4 * s, 0, 0)
    a.rot("right_leg", t, -6, 0, 6)
    a.rot("left_leg", t, 4, 0, -6)
    a.rot("right_lower_leg", t, 10, 0, 0)
    a.rot("left_lower_leg", t, 6, 0, 0)
    a.rot("pelt", t, 10 + 3 * s, 0, 0)
for t, z in ((0, -10), (0.35, 0), (0.7, 10), (1.05, 0), (1.4, -10)):
    a.rot("tail", t, 20, 0, z)

walk("walk_rage", 0.9, leg=32, arm=28, bob=1.2, lean=14, extra_tail=16)


# ---------------------------------------------------------------------------
# Serializacion .bbmodel
# ---------------------------------------------------------------------------
def outliner(b):
    return {
        "name": b.name,
        "origin": b.origin,
        "rotation": b.rotation,
        "color": 0,
        "uuid": b.uuid,
        "export": True,
        "mirror_uv": False,
        "isOpen": b.name in ("root", "body", "torso"),
        "locked": False,
        "visibility": True,
        "autouv": 0,
        "children": [outliner(c) if isinstance(c, Bone) else c.uuid for c in b.children],
    }


def element(c):
    faces = {}
    for f in ("north", "east", "south", "west", "up", "down"):
        u0, v0, u1, v1 = c.uv[f]
        if f == "down":
            u0, v0, u1, v1 = u0, v1, u1, v0  # convencion de Blockbench para la cara inferior
        faces[f] = {"uv": [u0, v0, u1, v1], "texture": 0}
    return {
        "name": c.name,
        "box_uv": False,
        "rescale": False,
        "locked": False,
        "light_emission": 0,
        "render_order": "default",
        "allow_mirror_modeling": True,
        "from": c.frm,
        "to": c.to,
        "autouv": 0,
        "color": 0,
        "inflate": c.inflate,
        "origin": c.bone.origin,
        "faces": faces,
        "type": "cube",
        "uuid": c.uuid,
    }


def build(out_path):
    tw, th = pack()
    img = paint(tw, th)
    buf = io.BytesIO()
    img.save(buf, "PNG")
    tex_b64 = base64.b64encode(buf.getvalue()).decode()
    model = {
        "meta": {"format_version": "4.10", "model_format": "free", "box_uv": False},
        "name": "heracles",
        "model_identifier": "",
        "visible_box": [2, 3, 1.4],
        "variable_placeholders": "",
        "variable_placeholder_buttons": [],
        "timeline_setups": [],
        "unhandled_root_fields": {},
        "resolution": {"width": tw, "height": th},
        "elements": [element(c) for c in CUBES],
        "outliner": [outliner(root)],
        "textures": [{
            "path": "",
            "name": "heracles.png",
            "folder": "",
            "namespace": "",
            "id": "0",
            "group": "",
            "width": tw * PX,
            "height": th * PX,
            "uv_width": tw,
            "uv_height": th,
            "particle": False,
            "use_as_default": False,
            "layers_enabled": False,
            "sync_to_project": "",
            "render_mode": "default",
            "render_sides": "auto",
            "frame_time": 1,
            "frame_order_type": "loop",
            "frame_order": "",
            "frame_interpolate": False,
            "visible": True,
            "internal": True,
            "saved": True,
            "uuid": uid(),
            "relative_path": "",
            "source": "data:image/png;base64," + tex_b64,
        }],
        "animations": [an.to_json() for an in ANIMS],
    }
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(model, fh, indent=1, ensure_ascii=False)
    return model, img


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "Modelos/01_Heracles/ModelEngine/blueprints/heracles/heracles.bbmodel"
    model, img = build(out)
    img.save(Path(out).with_name("heracles_texture.png"))
    print(f"OK -> {out}")
    print(f"  cubos: {len(CUBES)}  huesos: {len(BONES)}  animaciones: {[a.name for a in ANIMS]}")
    print(f"  textura: {img.size[0]}x{img.size[1]} px")
