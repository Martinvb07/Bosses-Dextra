#!/usr/bin/env python3
"""
Genera los blueprints de ModelEngine de los subditos de Heracles:

  hoplit           Hoplita: linotorax blanco, casco corintio, lanza y escudo con sol
  spartan_warrior  Guerrero espartano: coraza de bronce, capa roja, xiphos y escudo Λ
  greek_archer     Arquero griego: tunica verde, gorro frigio, carcaj y arco
  minotaur         Minotauro: cabeza de toro, cuernos, aro dorado y hacha doble (labrys)

Mismo formato que heracles.bbmodel (Blockbench "Generic Model", ModelEngine R4).

Uso: python3 tools/generate_minions.py            # genera los 4 + vistas previas
     python3 tools/generate_minions.py --no-preview
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

import bbmodel
from bbmodel import Model, mul

ROOT = Path(__file__).resolve().parent.parent / "Modelos" / "01_Heracles"
BLUEPRINTS = ROOT / "ModelEngine/blueprints"
PREVIEW = ROOT / "preview/minions"

GOLD_HI = (255, 236, 150)
GLOW_RED = (255, 70, 40)


# ===========================================================================
# Decoraciones comunes
# ===========================================================================
def add_common_decor(m):
    D = m.decor

    @D
    def d_face(f):
        skin = m.MAT["skin"]
        w = f.w
        brow = mul(m.MAT.get("hair", (60, 40, 25)), 0.8)
        f.rect(2, 5, 7, 6, brow)
        f.rect(w - 7, 5, w - 2, 6, brow)
        for ex in (3, w - 6):
            f.rect(ex, 6, ex + 3, 8, (240, 236, 224))
            f.rect(ex + 1, 6, ex + 2, 8, (60, 90, 140))
        f.rect(w // 2 - 1, 6, w // 2 + 1, 10, mul(skin, 1.08))
        f.rect(w // 2 - 1, 10, w // 2 + 1, 11, mul(skin, 0.75))
        f.rect(w // 2 - 3, 12, w // 2 + 3, 13, (110, 50, 40))

    @D
    def d_beard(f):
        for y in range(f.h):
            for x in range(f.w):
                if (x + y * 2) % 5 == 0:
                    f.shade(x, y, 1.25)

    @D
    def d_corinthian(f):
        # casco corintio de frente: ranura en T con ojos encendidos
        w, h = f.w, f.h
        dark = (26, 16, 8)
        f.rect(2, h // 2 - 2, w // 2 - 1, h // 2, dark)
        f.rect(w // 2 + 1, h // 2 - 2, w - 2, h // 2, dark)
        f.rect(w // 2 - 1, h // 2 - 2, w // 2 + 1, h - 1, dark)
        f.rect(w // 2 - 3, h - 5, w // 2 + 3, h, dark)
        f.put(4, h // 2 - 2, GLOW_RED)
        f.put(w - 5, h // 2 - 2, GLOW_RED)
        # nasal y cejas en relieve
        for x in range(1, w - 1):
            f.put(x, h // 2 - 3, GOLD_HI)
        for y in range(h // 2 - 2, h - 5):
            f.shade(w // 2 - 2, y, 1.15)
            f.shade(w // 2 + 1, y, 1.15)

    @D
    def d_helmet_side(f):
        for y in range(f.h):
            f.shade(f.w // 2, y, 0.82)
        for x in range(f.w):
            f.put(x, 1, GOLD_HI)

    @D
    def d_crest(f):
        if f.name in ("up", "down"):
            return
        for x in range(0, f.w):
            for y in range(f.h):
                if (x + (y // 2)) % 3 == 0:
                    f.shade(x, y, 0.72)
                elif (x + y) % 5 == 0:
                    f.shade(x, y, 1.2)

    @D
    def d_linothorax(f):
        # lino blanco con franja de meandro azul y escamas de bronce en el vientre
        blue = (40, 70, 150)
        if f.name in ("up", "down"):
            return
        for x in range(f.w):
            f.put(x, 2, blue)
            f.put(x, 3, blue)
            if x % 4 == 0:
                f.put(x, 4, blue)
        for y in range(f.h - 7, f.h - 1):
            for x in range(f.w):
                c = m.MAT["bronze"] if (x + (y % 2) * 2) % 4 else mul(m.MAT["bronze"], 0.7)
                f.put(x, y, c)
        if f.name == "north":
            f.rect(f.w // 2 - 2, 6, f.w // 2 + 2, 10, m.MAT["bronze"])
            f.rect(f.w // 2 - 1, 7, f.w // 2 + 1, 9, (190, 40, 30))

    @D
    def d_cuirass(f):
        # coraza musculada de bronce
        w = f.w
        if f.name == "north":
            for y in range(f.h):
                f.shade(w // 2, y, 0.75)
            for x in range(2, w - 2):
                f.shade(x, 6, 0.75)
                f.shade(x, 7, 1.15)
            for y in (10, 13):
                for x in range(4, w - 4):
                    f.shade(x, y, 0.8)
            f.put(5, 4, (255, 245, 200))
            f.put(w - 6, 4, (255, 245, 200))
        for x in range(w):
            f.put(x, f.h - 2, mul(m.MAT["bronze"], 0.6))

    @D
    def d_pteruges(f):
        if f.name in ("up", "down"):
            return
        for x in range(0, f.w, 3):
            for y in range(f.h):
                f.shade(x, y, 0.62)
        for x in range(1, f.w, 3):
            f.put(x, f.h - 2, mul(m.MAT["bronze"], 1.1))

    @D
    def d_greave(f):
        for y in range(f.h):
            f.put(f.w // 2, y, GOLD_HI)
        for x in range(f.w):
            f.shade(x, f.h // 2, 0.75)

    @D
    def d_straps(f):
        if f.name in ("up", "down"):
            return
        for x in range(1, f.w, 3):
            for y in range(f.h):
                f.shade(x, y, 0.7)

    @D
    def d_rim(f):
        for x in range(f.w):
            f.put(x, 0, GOLD_HI)

    @D
    def d_blade(f):
        for y in range(f.h):
            f.put(f.w // 2, y, (250, 252, 255))

    @D
    def d_grip(f):
        for y in range(0, f.h, 2):
            for x in range(f.w):
                f.shade(x, (y + x) % f.h, 0.7)

    @D
    def d_meander(f):
        dark = mul(m.MAT.get("bronze", (200, 150, 60)), 0.6)
        pattern = ["####.", "#..#.", "#.##."]
        if f.h < 4 or f.name in ("up", "down"):
            return
        for x in range(f.w):
            for yy in range(3):
                if pattern[yy][x % 5] == "#":
                    f.put(x, 1 + yy, dark)


def shield_disc(m, bone, cx, cy, z0, z1, r, mat, decor):
    """Escudo redondo hecho con 3 cubos en cruz (vista frontal casi circular)."""
    m.cube(bone, "shield_core", (cx - r, cy - r * 0.72, z0), (cx + r, cy + r * 0.72, z1), mat, decor=decor)
    m.cube(bone, "shield_v", (cx - r * 0.72, cy - r, z0 + 0.01), (cx + r * 0.72, cy + r, z1 - 0.01), mat, decor=decor)
    m.cube(bone, "shield_rim", (cx - r * 0.9, cy - r * 0.9, z0 + 0.25), (cx + r * 0.9, cy + r * 0.9, z1 + 0.25),
           "bronze", decor={"all": "rim"})


# ===========================================================================
# Cuerpo humano base (~2 bloques). Frente al NORTE (-Z), derecha = +X.
# ===========================================================================
HUMAN_BONES = ["body", "torso", "h_head", "right_arm", "right_forearm", "right_hand",
               "left_arm", "left_forearm", "left_hand", "right_leg", "right_lower_leg",
               "left_leg", "left_lower_leg", "skirt_front", "skirt_back"]


def humanoid(m, top_mat, skirt_mat, leg_mat="skin"):
    root = m.root
    hb = m.bone("hitbox", (0, 28, 0), root)                  # pivot Y = altura de los ojos
    m.cube(hb, "hitbox", (-5, 0, -5), (5, 34, 5), "hitbox")
    m.bone("tag_name", (0, 40, 0), root)

    legs = {}
    for side, sx in (("right", 1), ("left", -1)):
        leg = m.bone(f"{side}_leg", (2.5 * sx, 14, 0), root)
        lower = m.bone(f"{side}_lower_leg", (2.5 * sx, 7.5, 0), leg)
        legs[side] = (leg, lower)
    R, L = legs["right"], legs["left"]
    m.cube_lr(R[0], L[0], "thigh", (0.5, 7, -2), (4.5, 14, 2), leg_mat)
    m.cube_lr(R[1], L[1], "shin", (0.75, 1, -1.75), (4.25, 7.5, 1.75), leg_mat)
    m.cube_lr(R[1], L[1], "sandal", (0.5, 0, -2.75), (4.5, 1.25, 2), "leather", decor={"all": "straps"})

    body = m.bone("body", (0, 14, 0), root)
    waist = m.bone("waist", (0, 14, 0), body)
    m.cube(waist, "belt", (-5.25, 13, -3.25), (5.25, 15, 3.25), "leather")
    sf = m.bone("skirt_front", (0, 13.5, -3.25), waist)
    m.cube(sf, "skirt_front", (-5, 7.5, -3.75), (5, 13.5, -3), skirt_mat, decor={"all": "pteruges"})
    sb = m.bone("skirt_back", (0, 13.5, 3.25), waist)
    m.cube(sb, "skirt_back", (-5, 7.5, 3), (5, 13.5, 3.75), skirt_mat, decor={"all": "pteruges"})
    m.cube(waist, "skirt_right", (4.75, 8.5, -3), (5.5, 13.5, 3), skirt_mat, decor={"all": "pteruges"})
    m.cube(waist, "skirt_left", (-5.5, 8.5, -3), (-4.75, 13.5, 3), skirt_mat, decor={"all": "pteruges"})

    torso = m.bone("torso", (0, 15, 0), body)
    m.cube(torso, "chest", (-5, 15, -3), (5, 24, 3), top_mat)
    m.cube(torso, "neck", (-1.5, 24, -1.5), (1.5, 25, 1.5), "skin")

    head = m.bone("h_head", (0, 24.5, 0), torso)
    m.cube(head, "head", (-4, 24.5, -4), (4, 32.5, 4), "skin", decor={"north": "face"})

    arms = {}
    for side, sx in (("right", 1), ("left", -1)):
        arm = m.bone(f"{side}_arm", (6.5 * sx, 23, 0), torso)
        fore = m.bone(f"{side}_forearm", (6.5 * sx, 17.5, 0), arm)
        hand = m.bone(f"{side}_hand", (6.5 * sx, 11.5, 0), fore)
        arms[side] = (arm, fore, hand)
    AR, AL = arms["right"], arms["left"]
    m.cube_lr(AR[0], AL[0], "upper_arm", (5, 17.5, -1.75), (8, 24, 1.75), "skin")
    m.cube_lr(AR[1], AL[1], "forearm", (5.1, 11.5, -1.6), (7.9, 17.5, 1.6), "skin")
    m.cube_lr(AR[2], AL[2], "hand", (5.25, 9.5, -1.5), (7.75, 11.5, 1.5), "skin")

    m.ZERO_BONES = list(HUMAN_BONES)
    return dict(torso=torso, head=head, arms=arms, legs=legs, waist=waist)


# ===========================================================================
# Animaciones humanas comunes
# ===========================================================================
def human_idle(m, extra=None, arm_l=(0, 0, -3), arm_r=(0, 0, 3)):
    a = m.anim("idle", 2.4, "loop")
    for t, s in ((0, 0), (1.2, 1), (2.4, 0)):
        a.pos("body", t, 0, -0.25 * s, 0)
        a.rot("torso", t, -1.5 * s, 0, 0)
        a.rot("h_head", t, 1.5 * s, 2 * s - 1, 0)
        a.rot("right_arm", t, arm_r[0], arm_r[1], arm_r[2] + 1.5 * s)
        a.rot("left_arm", t, arm_l[0], arm_l[1], arm_l[2] - 1.5 * s)
        if extra:
            extra(a, t, s)
    return a


def human_walk(m, name="walk", length=1.0, leg=28, arm=20, bob=0.6, lean=3, arm_r=None, arm_l=None, extra=None):
    a = m.anim(name, length, "loop")
    h, q = length / 2, length / 4
    for t, s in ((0, 1), (h, -1), (length, 1)):
        a.rot("right_leg", t, -leg * s, 0, 0)
        a.rot("left_leg", t, leg * s, 0, 0)
        a.rot("right_arm", t, *(arm_r or (arm * s, 0, 3)))
        a.rot("left_arm", t, *(arm_l or (-arm * s, 0, -3)))
        a.rot("torso", t, lean, -4 * s, 0)
        a.rot("h_head", t, -lean * 0.6, 3 * s, 0)
        a.rot("skirt_front", t, -8, 0, 0)
        if extra:
            extra(a, t, s)
    for t, s in ((0, 0), (q, 1), (h, 0), (h + q, 1), (length, 0)):
        a.pos("body", t, 0, -bob * s, 0)
    for bone, keys in (("right_lower_leg", (0, 10, 35, 15, 0)), ("left_lower_leg", (35, 15, 0, 10, 35))):
        for t, x in zip((0, q, h, h + q, length), keys):
            a.rot(bone, t, x, 0, 0)
    return a


KNEEL = {"body": {"p": (0, -5.5, 0)}, "right_leg": (8, 0, 0), "right_lower_leg": (85, 0, 0),
         "left_leg": (-78, 0, 0), "left_lower_leg": (78, 0, 0)}


def human_spawn(m, raise_pose, length=1.6):
    """Aparece arrodillado, se levanta y alza el arma (pose final en 1.1 s)."""
    a = m.anim("spawn", length, "once")
    kneel = {**KNEEL, "torso": (25, 0, 0), "h_head": (20, 0, 0), "right_arm": (-10, 0, 6), "left_arm": (-10, 0, -6)}
    a.pose(0, kneel)
    a.pose(0.5, {**kneel, "torso": (18, 0, 0), "h_head": (-5, 0, 0)})
    a.pose(0.85, {"body": {"p": (0, 0, 0)}, "right_leg": (0, 0, 0), "right_lower_leg": (0, 0, 0),
                  "left_leg": (0, 0, 0), "left_lower_leg": (0, 0, 0), "torso": (-6, 0, 0),
                  "h_head": (-10, 0, 0), "right_arm": (0, 0, 5), "left_arm": (0, 0, -5)})
    a.pose(1.1, raise_pose)
    a.pose(1.3, raise_pose)
    a.rest(length)
    return a


def human_death(m, length=2.0):
    a = m.anim("death", length, "hold")
    a.rest(0)
    a.rot("root", 0, 0, 0, 0)
    a.pos("root", 0, 0, 0, 0)
    a.pose(0.3, {"torso": (-15, 0, 8), "h_head": (-20, 0, 0), "right_arm": (10, 0, 30), "left_arm": (10, 0, -30)})
    a.pose(0.8, {**KNEEL, "torso": (20, 0, 4), "h_head": (25, 0, 0), "right_arm": (15, 0, 10),
                 "left_arm": (15, 0, -10)}, i="linear")
    a.rot("root", 1.1, 0, 0, 0)
    a.pos("root", 1.1, 0, 0, 0)
    a.rot("root", 1.6, 84, 0, 0, i="linear")
    a.pos("root", 1.6, 0, 0, -1.5, i="linear")
    a.pose(1.6, {"right_arm": (-160, 0, 25), "left_arm": (-160, 0, -25), "h_head": (-10, 0, 0)}, i="linear")
    a.rot("root", 1.75, 80, 0, 0)
    a.rot("root", length, 82, 0, 0)
    return a


def human_hurt(m):
    a = m.anim("hurt", 0.35, "once")
    bones = ["torso", "h_head", "right_arm", "left_arm"]
    a.rest(0, bones)
    a.pose(0.08, {"torso": (-9, 0, 3), "h_head": (-12, 0, 0), "right_arm": (8, 0, 8), "left_arm": (8, 0, -8)})
    a.rest(0.35, bones)
    return a


# ===========================================================================
# HOPLITA
# ===========================================================================
def build_hoplit():
    m = Model("hoplit", {
        "skin": ((196, 140, 98), 7), "bronze": ((206, 146, 58), 9), "linen": ((226, 220, 200), 6),
        "red": ((168, 34, 30), 8), "leather": ((112, 72, 42), 9), "wood": ((120, 82, 48), 10),
        "iron": ((178, 182, 190), 6), "blue": ((38, 66, 140), 6), "hair": ((70, 46, 28), 9),
    }, seed=101)
    m.SHINE |= {"bronze", "iron"}
    m.WOOD |= {"wood"}
    add_common_decor(m)

    @m.decor
    def d_aspis_sun(f):
        if f.name != "north":
            return
        cx, cy = f.w / 2, f.h / 2
        for y in range(f.h):
            for x in range(f.w):
                d = ((x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2) ** 0.5
                if d < f.w * 0.16:
                    f.put(x, y, (245, 200, 80))
                elif d < f.w * 0.3 and (int((x - cx) * 3) % 2 == 0) ^ (int((y - cy) * 3) % 2 == 0):
                    f.put(x, y, (226, 170, 58))

    H = humanoid(m, "linen", "linen")
    torso, head, (AR, AL) = H["torso"], H["head"], (H["arms"]["right"], H["arms"]["left"])
    m.cube(torso, "linothorax", (-5.25, 15.5, -3.25), (5.25, 24, 3.25), "linen", decor={"all": "linothorax"})
    m.cube_lr(AR[0], AL[0], "shoulder_flap", (4.75, 21.5, -2.25), (8.25, 24.5, 2.25), "linen", decor={"all": "pteruges"})
    m.cube_lr(H["legs"]["right"][1], H["legs"]["left"][1], "greave", (0.5, 1.5, -2), (4.5, 7.25, -1.5), "bronze",
              decor={"north": "greave"})
    # casco corintio + penacho
    m.cube(head, "helmet", (-4.5, 26, -4.5), (4.5, 33, 4.5), "bronze",
           decor={"north": "corinthian", "east": "helmet_side", "west": "helmet_side"})
    m.cube(head, "cheek_guards", (-4.5, 24, -4.75), (4.5, 26, -3.5), "bronze")
    crest = m.bone("crest", (0, 33, 0), head)
    m.cube(crest, "crest_holder", (-0.75, 33, -2), (0.75, 34, 2), "bronze")
    m.cube(crest, "crest", (-0.75, 34, -5), (0.75, 37.5, 4.5), "red", decor={"all": "crest"})
    m.cube(crest, "crest_tail", (-0.75, 31, 4.5), (0.75, 35, 6), "red", decor={"all": "crest"})
    # escudo (aspis) en el antebrazo izquierdo
    shield = m.bone("shield", (-6.5, 14.5, 0), AL[1])
    shield_disc(m, shield, -6.5, 14.5, -4, -2.75, 6.5, "blue", {"north": "aspis_sun"})
    # lanza (dory) en la mano derecha
    spear = m.bone("spear", (6.5, 10.5, -2.25), AR[2])
    m.cube(spear, "spear_shaft", (6, -6, -2.75), (7, 30, -1.75), "wood", decor={"all": "grip"})
    m.cube(spear, "spear_tip", (5.75, 30, -3), (7.25, 34.5, -1.5), "iron", decor={"north": "blade", "south": "blade"})
    m.cube(spear, "spear_butt", (6.1, -8, -2.65), (6.9, -6, -1.85), "bronze")
    m.ZERO_BONES += ["shield", "spear", "crest"]

    # ---- animaciones ----
    human_idle(m, arm_l=(-12, 0, -6), arm_r=(-8, 0, 4))
    human_walk(m, arm_l=(-14, 0, -6), extra=lambda a, t, s: a.rot("right_arm", t, 12 * s - 6, 0, 4))
    # ATTACK: lanzazo por encima del hombro (impacto 0.35 s = 7 ticks)
    a = m.anim("attack", 0.8, "once")
    a.rest(0)
    a.pose(0.2, {"right_arm": (-160, 0, 6), "right_forearm": (-30, 0, 0), "spear": (280, 0, 0),
                 "torso": (-6, 22, 0), "left_arm": (-30, 0, -8), "h_head": (0, -15, 0)})
    a.pose(0.35, {"right_arm": (-100, 0, 4), "right_forearm": (0, 0, 0), "spear": (190, 0, 0),
                  "torso": (14, -12, 0), "left_arm": (-20, 0, -8), "h_head": (-10, 8, 0),
                  "right_leg": (-20, 0, 0), "right_lower_leg": (20, 0, 0), "body": {"p": (0, -0.6, -1)}}, i="linear")
    a.pose(0.48, {"right_arm": (-102, 0, 4), "spear": (192, 0, 0), "torso": (12, -12, 0)})
    a.rest(0.8)
    human_hurt(m)
    human_spawn(m, {"right_arm": (-170, 0, 8), "right_forearm": (-10, 0, 0), "left_arm": (-40, 0, -10),
                    "h_head": (-25, 0, 0), "torso": (-8, 0, 0)})
    human_death(m)
    return m


# ===========================================================================
# GUERRERO ESPARTANO
# ===========================================================================
def build_spartan():
    m = Model("spartan_warrior", {
        "skin": ((186, 128, 88), 7), "bronze": ((210, 150, 54), 9), "red": ((156, 24, 22), 8),
        "leather": ((96, 58, 32), 9), "iron": ((186, 190, 198), 6), "hair": ((40, 28, 20), 8),
    }, seed=202)
    m.SHINE |= {"bronze", "iron"}
    add_common_decor(m)

    @m.decor
    def d_lambda(f):
        if f.name != "north":
            return
        cx = f.w / 2
        top, bot = int(f.h * 0.2), int(f.h * 0.8)
        for y in range(top, bot):
            t = (y - top) / (bot - top)
            off = t * f.w * 0.28
            for dx in (0, 1):
                f.put(int(cx - off) - dx, y, (230, 178, 60))
                f.put(int(cx + off) + dx - 1, y, (230, 178, 60))

    @m.decor
    def d_cape(f):
        for x in range(0, f.w, 3):
            for y in range(f.h):
                f.shade(x, y, 0.8)
        for x in range(f.w):
            f.shade(x, f.h - 1, 0.6)

    H = humanoid(m, "skin", "red")
    torso, head, (AR, AL) = H["torso"], H["head"], (H["arms"]["right"], H["arms"]["left"])
    m.cube(head, "beard", (-4, 24, -4.6), (4, 27.5, -3.9), "hair", decor={"all": "beard"})
    m.cube(torso, "cuirass", (-5.3, 15.5, -3.3), (5.3, 24, 3.3), "bronze", decor={"all": "cuirass"})
    m.cube_lr(AR[1], AL[1], "bracer", (4.9, 12, -1.8), (8.1, 15.5, 1.8), "leather", decor={"all": "straps"})
    m.cube_lr(H["legs"]["right"][1], H["legs"]["left"][1], "greave", (0.5, 1.5, -2), (4.5, 7.5, 2), "bronze",
              decor={"north": "greave"})
    # casco con penacho transversal (de oficial)
    m.cube(head, "helmet", (-4.5, 26, -4.5), (4.5, 33, 4.5), "bronze",
           decor={"north": "corinthian", "east": "helmet_side", "west": "helmet_side"})
    m.cube(head, "cheek_guards", (-4.5, 24, -4.75), (4.5, 26, -3.5), "bronze")
    crest = m.bone("crest", (0, 33, 0), head)
    m.cube(crest, "crest", (-6.5, 33, -0.75), (6.5, 37, 0.75), "red", decor={"all": "crest"})
    # capa roja
    cape = m.bone("cape", (0, 24, 3.5), torso)
    m.cube(cape, "cape_upper", (-5.5, 14, 3.4), (5.5, 24.25, 4.4), "red", decor={"all": "cape"})
    cape_low = m.bone("cape_lower", (0, 14, 3.9), cape)
    m.cube(cape_low, "cape_lower", (-5.5, 4, 3.4), (5.5, 14, 4.4), "red", decor={"all": "cape"})
    # escudo con lambda
    shield = m.bone("shield", (-6.5, 14.5, 0), AL[1])
    shield_disc(m, shield, -6.5, 14.5, -4, -2.75, 7, "red", {"north": "lambda"})
    # xiphos (espada corta): la hoja apunta hacia delante en reposo
    sword = m.bone("sword", (6.5, 10.5, 0), AR[2], rotation=(-70, 0, 0))
    m.cube(sword, "sword_grip", (6, 9.5, -0.5), (7, 12.5, 0.5), "leather", decor={"all": "grip"})
    m.cube(sword, "sword_guard", (5.25, 12.5, -0.75), (7.75, 13.25, 0.75), "bronze")
    m.cube(sword, "sword_blade", (6, 13.25, -0.3), (7, 21.5, 0.3), "iron", decor={"north": "blade", "south": "blade"})
    m.ZERO_BONES += ["shield", "sword", "crest", "cape", "cape_lower"]

    def cape_sway(a, t, s):
        a.rot("cape", t, 4 + 2 * s, 0, 0)

    human_idle(m, extra=cape_sway, arm_l=(-14, 0, -6), arm_r=(-10, 0, 5))
    human_walk(m, leg=30, arm_l=(-16, 0, -6),
               extra=lambda a, t, s: (a.rot("cape", t, 12 + 4 * s, 0, 0), a.rot("cape_lower", t, 6 + 4 * s, 0, 0)))
    # ATTACK: golpe de escudo + estocada (impacto 0.3 s = 6 ticks)
    a = m.anim("attack", 0.75, "once")
    a.rest(0)
    a.pose(0.15, {"left_arm": (-40, 25, -10), "left_forearm": (-50, 0, 0), "shield": (40, 0, 0),
                  "right_arm": (20, 0, 10), "right_forearm": (-60, 0, 0), "torso": (-4, 18, 0),
                  "cape": (10, 0, 0)})
    a.pose(0.3, {"left_arm": (-20, 0, -8), "left_forearm": (-30, 0, 0), "shield": (20, 0, 0),
                 "right_arm": (-85, -10, 0), "right_forearm": (-5, 0, 0), "sword": (55, 0, 0),
                 "torso": (12, -18, 0), "h_head": (-6, 10, 0), "right_leg": (-22, 0, 0),
                 "right_lower_leg": (22, 0, 0), "body": {"p": (0, -0.6, -1.2)}, "cape": (22, 0, 0)}, i="linear")
    a.pose(0.42, {"right_arm": (-88, -10, 0), "sword": (55, 0, 0), "torso": (10, -18, 0)})
    a.rest(0.75)
    # BLOCK: alza el escudo (para Spartan_Block)
    a = m.anim("block", 0.8, "once")
    a.rest(0)
    guard = {"left_arm": (-55, 30, -5), "left_forearm": (-45, 0, 0), "shield": (55, 0, 0),
             "torso": (6, 15, 0), "h_head": (8, -10, 0), "right_arm": (15, 0, 10),
             "right_forearm": (-50, 0, 0), "body": {"p": (0, -1, 0)}, "right_leg": (-15, 0, 0),
             "right_lower_leg": (25, 0, 0), "left_leg": (10, 0, 0), "left_lower_leg": (15, 0, 0)}
    a.pose(0.12, guard)
    a.pose(0.6, guard)
    a.rest(0.8)
    human_hurt(m)
    human_spawn(m, {"right_arm": (-165, 0, 10), "sword": (60, 0, 0), "left_arm": (-50, 20, -10),
                    "left_forearm": (-40, 0, 0), "h_head": (-25, 0, 0), "torso": (-8, 0, 0)})
    human_death(m)
    return m


# ===========================================================================
# ARQUERO GRIEGO
# ===========================================================================
def build_archer():
    m = Model("greek_archer", {
        "skin": ((200, 146, 104), 7), "tunic": ((96, 126, 70), 8), "leather": ((120, 80, 46), 9),
        "cap": ((150, 40, 34), 8), "wood": ((126, 86, 46), 9), "white": ((236, 232, 220), 5),
        "bronze": ((204, 146, 60), 8), "string": ((240, 236, 210), 2), "hair": ((92, 60, 34), 9),
        "iron": ((176, 180, 188), 6),
    }, seed=303)
    m.SHINE |= {"bronze"}
    m.WOOD |= {"wood"}
    add_common_decor(m)

    @m.decor
    def d_tunic(f):
        if f.name in ("up", "down"):
            return
        for x in range(f.w):
            f.put(x, f.h - 2, (226, 196, 90))
        for x in range(0, f.w, 4):
            for y in range(2, f.h - 3):
                f.shade(x, y, 0.88)

    @m.decor
    def d_arrows(f):
        if f.name != "up":
            return
        for x in range(0, f.w, 2):
            for y in range(0, f.h, 2):
                f.put(x, y, (240, 240, 240) if (x + y) % 4 else (200, 40, 30))

    H = humanoid(m, "tunic", "tunic")
    torso, head, (AR, AL) = H["torso"], H["head"], (H["arms"]["right"], H["arms"]["left"])
    m.cube(torso, "tunic", (-5.25, 15.5, -3.25), (5.25, 24, 3.25), "tunic", decor={"all": "tunic"})
    m.cube(torso, "strap", (-5.4, 16, -3.4), (5.4, 17.25, 3.4), "leather")
    m.cube(head, "beard", (-4, 24.25, -4.5), (4, 26.5, -3.9), "hair", decor={"all": "beard"})
    # gorro frigio con la punta caida hacia delante
    m.cube(head, "cap", (-4.4, 29, -4.4), (4.4, 33.5, 4.4), "cap", decor={"north": "meander"})
    m.cube(head, "cap_tip", (-2.25, 33.5, -3.5), (2.25, 35.5, 1.5), "cap")
    m.cube(head, "cap_curl", (-1.75, 32, -5.25), (1.75, 35, -3.5), "cap")
    m.cube(head, "cap_flaps", (-4.4, 24.5, 1), (4.4, 29, 4.4), "cap")
    # carcaj a la espalda
    quiver = m.bone("quiver", (0, 18, 4), torso)
    m.cube(quiver, "quiver", (-2.25, 12, 3.5), (1.25, 24, 5.5), "leather", decor={"all": "straps"})
    m.cube(quiver, "arrows", (-2, 24, 3.75), (1, 27, 5.25), "white", decor={"all": "arrows"})
    m.cube_lr(AR[1], AL[1], "bracer", (4.9, 12, -1.8), (8.1, 15, 1.8), "leather")
    # arco en la mano izquierda (en el plano YZ, cuerda hacia atras)
    bow = m.bone("bow", (-6.5, 10.5, 0), AL[2])
    m.cube(bow, "bow_grip", (-7, 9, -1.75), (-6, 12, -0.75), "leather", decor={"all": "grip"})
    for i, (y0, y1, z) in enumerate(((12, 15, -1.25), (15, 18, -0.5), (18, 20, 0.25))):
        m.cube(bow, f"bow_up_{i}", (-7, y0, z - 0.5), (-6, y1, z + 0.5), "wood")
        m.cube(bow, f"bow_down_{i}", (-7, 21 - y1, z - 0.5), (-6, 21 - y0, z + 0.5), "wood")
    m.cube(bow, "bow_tip_up", (-7.1, 19.5, 0.25), (-5.9, 20.5, 1.25), "bronze")
    m.cube(bow, "bow_tip_down", (-7.1, 0.5, 0.25), (-5.9, 1.5, 1.25), "bronze")
    s_up = m.bone("string_up", (-6.5, 20, 1), bow)
    m.cube(s_up, "string_up", (-6.6, 10.5, 0.9), (-6.4, 20, 1.1), "string")
    s_dn = m.bone("string_down", (-6.5, 1, 1), bow)
    m.cube(s_dn, "string_down", (-6.6, 1, 0.9), (-6.4, 10.5, 1.1), "string")
    # flecha en la mano derecha (pegada al antebrazo en reposo)
    arrow = m.bone("arrow", (6.5, 10.5, 0), AR[2])
    m.cube(arrow, "arrow_shaft", (6.4, 10, -0.1), (6.6, 22, 0.1), "wood")
    m.cube(arrow, "arrow_head", (6.25, 22, -0.25), (6.75, 23.5, 0.25), "iron")
    m.cube(arrow, "arrow_fletch", (6.3, 9, -0.6), (6.7, 11.5, 0.6), "white")
    m.ZERO_BONES += ["bow", "string_up", "string_down", "arrow", "quiver"]

    human_idle(m, arm_l=(-6, 0, -4), arm_r=(-4, 0, 4))
    human_walk(m, arm=16, leg=30, bob=0.7)
    # SHOOT: tensa y suelta (suelta en 0.4 s = 8 ticks)
    a = m.anim("shoot", 0.7, "once")
    a.rest(0)
    # pose calculada para que la cola de la flecha quede junto a la barbilla
    # y la punta apunte al arco
    aim = {"torso": (0, 35, 0), "h_head": (0, -32, 0), "left_arm": (-90, 35, 0), "left_forearm": (0, 0, 0),
           "bow": (90, 0, 0), "right_arm": (-120, -20, 60), "right_forearm": (-120, 0, 0),
           "arrow": (-30, 0, 0)}
    a.pose(0.15, {**aim, "right_forearm": (-90, 0, 0)})
    a.pose(0.38, {**aim, "string_up": (35, 0, 0), "string_down": (-35, 0, 0)})
    a.pose(0.4, {**aim, "string_up": (0, 0, 0), "string_down": (0, 0, 0), "right_arm": (-110, -20, 85),
                 "right_forearm": (-100, 0, 0)}, i="linear")
    a.pose(0.55, {**aim, "right_arm": (-110, -20, 85), "right_forearm": (-100, 0, 0)})
    a.rest(0.7)
    human_hurt(m)
    human_spawn(m, {"left_arm": (-150, 0, -10), "bow": (90, 0, 0), "h_head": (-25, 0, 0), "torso": (-6, 0, 0)})
    human_death(m)
    return m


# ===========================================================================
# MINOTAURO (~3 bloques)
# ===========================================================================
MINO_BONES = ["body", "torso", "h_head", "jaw", "right_arm", "right_forearm", "right_hand",
              "left_arm", "left_forearm", "left_hand", "right_leg", "right_lower_leg",
              "left_leg", "left_lower_leg", "tail", "loincloth", "axe"]


def build_minotaur():
    m = Model("minotaur", {
        "fur": ((104, 66, 40), 14), "skin": ((132, 90, 62), 10), "dark": ((58, 38, 26), 10),
        "horn": ((228, 216, 186), 6), "hoof": ((46, 36, 30), 6), "gold": ((228, 178, 50), 9),
        "leather": ((96, 56, 30), 9), "wood": ((102, 70, 40), 10), "bronze": ((196, 136, 56), 9),
        "red": ((150, 30, 26), 8), "muzzle": ((176, 132, 112), 8),
    }, seed=404)
    m.FUR |= {"fur", "dark"}
    m.SHINE |= {"gold", "bronze"}
    m.WOOD |= {"wood"}
    add_common_decor(m)
    m.BODY = "body"

    @m.decor
    def d_bull_face(f):
        w = f.w
        for ex in (2, w - 5):
            f.rect(ex, 4, ex + 3, 6, (30, 10, 8))
            f.rect(ex + 1, 4, ex + 2, 6, GLOW_RED)
        f.rect(1, 3, w - 1, 4, mul(m.MAT["dark"], 0.8))

    @m.decor
    def d_snout(f):
        w = f.w
        f.rect(1, 1, 3, 3, (24, 14, 12))
        f.rect(w - 3, 1, w - 1, 3, (24, 14, 12))
        for x in range(w):
            f.shade(x, f.h - 1, 0.7)

    @m.decor
    def d_horn(f):
        for x in range(0, f.w, 3):
            for y in range(f.h):
                f.shade(x, y, 0.88)

    @m.decor
    def d_muscle(f):
        if f.name != "north":
            return
        w = f.w
        for y in range(f.h):
            f.shade(w // 2, y, 0.78)
        for x in range(2, w - 2):
            f.shade(x, 9, 0.75)
            f.shade(x, 10, 1.12)
        for y in (15, 19, 23):
            for x in range(w // 2 - 6, w // 2 + 6):
                f.shade(x, y, 0.82)

    @m.decor
    def d_labrys(f):
        if f.name not in ("north", "south"):
            return
        for y in range(f.h):
            f.put(0, y, (255, 246, 200))
            f.put(f.w - 1, y, (255, 246, 200))
        for x in range(f.w // 2 - 1, f.w // 2 + 1):
            for y in range(2, f.h - 2):
                f.shade(x, y, 0.7)

    root = m.root
    hb = m.bone("hitbox", (0, 42, 0), root)
    m.cube(hb, "hitbox", (-10, 0, -10), (10, 48, 10), "hitbox")
    m.bone("tag_name", (0, 56, 0), root)

    legs = {}
    for side, sx in (("right", 1), ("left", -1)):
        leg = m.bone(f"{side}_leg", (4.5 * sx, 20, 0), root)
        lower = m.bone(f"{side}_lower_leg", (4.5 * sx, 10, 1), leg)
        legs[side] = (leg, lower)
    R, L = legs["right"], legs["left"]
    m.cube_lr(R[0], L[0], "thigh", (1, 9.5, -3.5), (8.5, 20.5, 3.5), "fur")
    m.cube_lr(R[1], L[1], "shin", (1.75, 3, -2), (7.75, 10.5, 3.5), "fur")
    m.cube_lr(R[1], L[1], "hoof", (1.5, 0, -3), (8, 3, 3), "hoof")
    m.cube_lr(R[1], L[1], "fetlock", (1.25, 2.5, -2.5), (8.25, 4, 3.75), "dark")

    body = m.bone("body", (0, 20, 0), root)
    m.cube(body, "belt", (-9.5, 19, -5.5), (9.5, 22, 5.5), "leather")
    m.cube(body, "buckle", (-2, 19.25, -6), (2, 21.75, -5.5), "gold")
    lc = m.bone("loincloth", (0, 19.5, -5.5), body)
    m.cube(lc, "loincloth", (-4.5, 11, -6), (4.5, 19.5, -5.25), "red", decor={"all": "pteruges"})
    tail = m.bone("tail", (0, 20, 5), body)
    m.cube(tail, "tail", (-0.6, 9, 4.6), (0.6, 20, 5.8), "fur")
    m.cube(tail, "tail_tuft", (-1.25, 6, 4), (1.25, 9.5, 6.5), "dark")

    torso = m.bone("torso", (0, 22, 0), body)
    m.cube(torso, "chest", (-10, 22, -6), (10, 40, 6), "skin", decor={"north": "muscle"})
    m.cube(torso, "fur_back", (-10.5, 26, 3), (10.5, 41, 7), "fur")
    m.cube(torso, "hump", (-8, 38, -3), (8, 44, 6), "fur")
    m.cube(torso, "chest_fur", (-6, 33, -6.75), (6, 40, -5.75), "fur")

    head = m.bone("h_head", (0, 40, -2), torso)
    m.cube(head, "skull", (-5.5, 38.5, -11), (5.5, 48, -1), "fur", decor={"north": "bull_face"})
    m.cube(head, "brow", (-6, 45, -11.5), (6, 48.5, -5), "dark")
    m.cube(head, "snout", (-4.5, 38, -16), (4.5, 44, -10), "muzzle", decor={"north": "snout"})
    jaw = m.bone("jaw", (0, 39, -9), head)
    m.cube(jaw, "jaw", (-4, 35.5, -15.5), (4, 38.5, -9), "muzzle")
    m.cube(head, "nose_ring", (-2, 36.5, -16.5), (2, 38, -16), "gold")
    m.cube(head, "ear_r", (5.5, 44, -6), (8.5, 45.5, -4), "fur")
    m.cube(head, "ear_l", (-8.5, 44, -6), (-5.5, 45.5, -4), "fur")
    for side, sx in (("r", 1), ("l", -1)):
        def X(a, b):
            return (a, b) if sx > 0 else (-b, -a)
        x0, x1 = X(5.5, 12)
        m.cube(head, f"horn_{side}_1", (x0, 44.5, -8.5), (x1, 47.5, -5.5), "horn", decor={"all": "horn"})
        x0, x1 = X(10.5, 13.5)
        m.cube(head, f"horn_{side}_2", (x0, 47, -8.25), (x1, 52, -5.75), "horn", decor={"all": "horn"})
        x0, x1 = X(11, 13)
        m.cube(head, f"horn_{side}_3", (x0, 52, -9.5), (x1, 55, -7.5), "horn")
        x0, x1 = X(11.25, 12.75)
        m.cube(head, f"horn_{side}_tip", (x0, 55, -10.5), (x1, 57, -9), "dark")

    arms = {}
    for side, sx in (("right", 1), ("left", -1)):
        arm = m.bone(f"{side}_arm", (12 * sx, 37, 0), torso)
        fore = m.bone(f"{side}_forearm", (12.5 * sx, 27, 0), arm)
        hand = m.bone(f"{side}_hand", (12.5 * sx, 17, 0), fore)
        arms[side] = (arm, fore, hand)
    AR, AL = arms["right"], arms["left"]
    m.cube_lr(AR[0], AL[0], "shoulder", (9.5, 32, -4.5), (15.5, 40.5, 4.5), "fur")
    m.cube_lr(AR[0], AL[0], "upper_arm", (9.75, 27, -3.5), (15.25, 32.5, 3.5), "skin")
    m.cube_lr(AR[1], AL[1], "forearm", (9.75, 17, -3.25), (15.25, 27, 3.25), "skin")
    m.cube_lr(AR[1], AL[1], "cuff", (9.5, 19, -3.5), (15.5, 22.5, 3.5), "bronze", decor={"all": "rim"})
    m.cube_lr(AR[2], AL[2], "fist", (10, 12.5, -3), (15, 17, 3), "skin")

    # hacha doble (labrys) en la mano derecha, cuelga con la hoja hacia abajo/delante
    axe = m.bone("axe", (12.5, 15, 0), AR[2], rotation=(60, 0, 0))
    m.cube(axe, "axe_handle", (11.75, -4, -0.75), (13.25, 18, 0.75), "wood", decor={"all": "grip"})
    m.cube(axe, "axe_head_core", (11.5, -8, -1.25), (13.5, -1, 1.25), "bronze")
    m.cube(axe, "axe_blade_f", (11.9, -10, -7), (13.1, 1, -1.25), "bronze", decor={"all": "labrys"})
    m.cube(axe, "axe_blade_b", (11.9, -10, 1.25), (13.1, 1, 7), "bronze", decor={"all": "labrys"})
    m.cube(axe, "axe_spike", (12, -12, -0.5), (13, -10, 0.5), "bronze")

    m.ZERO_BONES = list(MINO_BONES)

    # ---- animaciones ----
    a = m.anim("idle", 2.0, "loop")
    for t, s in ((0, 0), (1.0, 1), (2.0, 0)):
        a.pos("body", t, 0, -0.5 * s, 0)
        a.rot("torso", t, 8 - 3 * s, 0, 0)
        a.rot("h_head", t, -6 + 3 * s, 0, 0)
        a.rot("right_arm", t, -6, 0, 6 + 3 * s)
        a.rot("left_arm", t, -6, 0, -6 - 3 * s)
        a.rot("right_forearm", t, -12 - 4 * s, 0, 0)
        a.rot("left_forearm", t, -18 - 4 * s, 0, 0)
    for t, z in ((0, -10), (0.5, 0), (1.0, 10), (1.5, 0), (2.0, -10)):
        a.rot("tail", t, 15, 0, z)
    # bufido
    a.rot("jaw", 0, 0, 0, 0)
    a.rot("jaw", 1.4, 0, 0, 0)
    a.rot("jaw", 1.55, -12, 0, 0)
    a.rot("jaw", 1.75, 0, 0, 0)

    a = m.anim("walk", 1.3, "loop")
    length, h, q = 1.3, 0.65, 0.325
    for t, s in ((0, 1), (h, -1), (length, 1)):
        a.rot("right_leg", t, -26 * s, 0, 0)
        a.rot("left_leg", t, 26 * s, 0, 0)
        a.rot("right_arm", t, 16 * s, 0, 6)
        a.rot("left_arm", t, -16 * s, 0, -6)
        a.rot("torso", t, 10, -6 * s, 3 * s)
        a.rot("h_head", t, -6, 5 * s, 0)
        a.rot("loincloth", t, -12, 0, 0)
    for t, s in ((0, 0), (q, 1), (h, 0), (h + q, 1), (length, 0)):
        a.pos("body", t, 0, -1.2 * s, 0)
    for bone, keys in (("right_lower_leg", (0, 12, 40, 18, 0)), ("left_lower_leg", (40, 18, 0, 12, 40))):
        for t, x in zip((0, q, h, h + q, length), keys):
            a.rot(bone, t, x, 0, 0)
    for t, z in ((0, -14), (h, 14), (length, -14)):
        a.rot("tail", t, 20, 0, z)

    # ATTACK: hachazo vertical (impacto 0.45 s = 9 ticks)
    a = m.anim("attack", 1.0, "once")
    a.rest(0)
    a.pose(0.3, {"right_arm": (-150, 0, -10), "left_arm": (-140, 0, 20), "right_forearm": (-20, 0, 0),
                 "left_forearm": (-20, 0, 0), "axe": (50, 0, 0), "torso": (-12, 0, 0), "h_head": (-10, 0, 0),
                 "body": {"p": (0, 0.5, 0)}})
    a.pose(0.45, {"right_arm": (-40, 0, -10), "left_arm": (-40, 0, 20), "right_forearm": (-10, 0, 0),
                  "left_forearm": (-10, 0, 0), "axe": (10, 0, 0), "torso": (28, 0, 0), "h_head": (-20, 0, 0),
                  "body": {"p": (0, -2, 0)}, "right_leg": (-28, 0, 0), "right_lower_leg": (40, 0, 0),
                  "left_leg": (-8, 0, 0), "left_lower_leg": (25, 0, 0), "jaw": (-15, 0, 0)}, i="linear")
    a.pose(0.6, {"torso": (26, 0, 0), "body": {"p": (0, -1.8, 0)}, "axe": (10, 0, 0)})
    a.rest(1.0)

    # CHARGE: baja los cuernos y embiste (salto 0.25 s, impacto 0.5 s)
    a = m.anim("charge", 1.1, "once")
    a.rest(0)
    a.pose(0.25, {"torso": (40, 0, 0), "h_head": (20, 0, 0), "body": {"p": (0, -3, 0)},
                  "right_arm": (35, 0, 15), "left_arm": (35, 0, -15), "right_leg": (-30, 0, 0),
                  "right_lower_leg": (40, 0, 0), "left_leg": (25, 0, 0), "left_lower_leg": (15, 0, 0),
                  "tail": (40, 0, 0)})
    a.pose(0.5, {"torso": (48, 0, 0), "h_head": (30, 0, 0), "body": {"p": (0, -2, -4)},
                 "right_arm": (50, 0, 20), "left_arm": (50, 0, -20), "right_leg": (30, 0, 0),
                 "right_lower_leg": (10, 0, 0), "left_leg": (-40, 0, 0), "left_lower_leg": (35, 0, 0),
                 "jaw": (-15, 0, 0)}, i="linear")
    a.pose(0.7, {"torso": (44, 0, 0), "h_head": (25, 0, 0), "body": {"p": (0, -2, -4)}})
    a.rest(1.1)

    # ROAR (al aparecer y para el ataque especial)
    a = m.anim("roar", 1.6, "once")
    a.rest(0)
    roar = {"torso": (-14, 0, 0), "h_head": (-35, 0, 0), "jaw": (-28, 0, 0), "right_arm": (-30, 0, 55),
            "left_arm": (-30, 0, -55), "right_forearm": (-40, 0, 0), "left_forearm": (-40, 0, 0),
            "tail": (50, 0, 0)}
    a.pose(0.35, roar)
    for i, t in enumerate([0.45 + 0.1 * n for n in range(8)]):
        s = 1 if i % 2 == 0 else -1
        a.rot("h_head", t, -35, 3 * s, 0, i="linear")
        a.rot("torso", t, -14, 0, 1.5 * s, i="linear")
    a.pose(1.25, roar)
    a.rest(1.6)

    # SPAWN: sale encorvado, pisotea y ruge (2 s)
    a = m.anim("spawn", 2.0, "once")
    crouch = {"body": {"p": (0, -6, 0)}, "torso": (45, 0, 0), "h_head": (10, 0, 0), "right_leg": (-50, 0, 0),
              "right_lower_leg": (80, 0, 0), "left_leg": (-50, 0, 0), "left_lower_leg": (80, 0, 0),
              "right_arm": (20, 0, 20), "left_arm": (20, 0, -20)}
    a.pose(0, crouch)
    a.pose(0.5, crouch)
    a.pose(0.8, {"body": {"p": (0, 0, 0)}, "torso": (0, 0, 0), "h_head": (0, 0, 0), "right_leg": (-40, 0, 0),
                 "right_lower_leg": (30, 0, 0), "left_leg": (0, 0, 0), "left_lower_leg": (0, 0, 0),
                 "right_arm": (0, 0, 10), "left_arm": (0, 0, -10)})
    a.pose(0.95, {"right_leg": (0, 0, 0), "right_lower_leg": (0, 0, 0), "body": {"p": (0, -1, 0)}}, i="linear")
    a.pose(1.3, {**roar, "body": {"p": (0, 0, 0)}})
    a.pose(1.7, roar)
    a.rest(2.0)

    a = m.anim("hurt", 0.4, "once")
    bones = ["torso", "h_head", "right_arm", "left_arm"]
    a.rest(0, bones)
    a.pose(0.1, {"torso": (-6, 0, 4), "h_head": (-14, 0, 0), "right_arm": (6, 0, 8), "left_arm": (6, 0, -8)})
    a.rest(0.4, bones)

    a = m.anim("death", 2.4, "hold")
    a.rest(0)
    a.rot("root", 0, 0, 0, 0)
    a.pos("root", 0, 0, 0, 0)
    a.pose(0.4, {**roar, "h_head": (-45, 0, 0)})
    a.pose(1.0, {"body": {"p": (0, -9, 0)}, "torso": (25, 0, 6), "h_head": (20, 0, 0), "jaw": (-10, 0, 0),
                 "right_leg": (5, 0, 0), "right_lower_leg": (85, 0, 0), "left_leg": (5, 0, 0),
                 "left_lower_leg": (85, 0, 0), "right_arm": (10, 0, 15), "left_arm": (10, 0, -15)}, i="linear")
    a.rot("root", 1.4, 0, 0, 0)
    a.rot("root", 1.4, 0, 0, 0)
    a.rot("root", 2.0, 0, 0, 86, i="linear")
    a.pos("root", 1.4, 0, 0, 0)
    a.pos("root", 2.0, -3, 0, 0, i="linear")
    a.rot("root", 2.15, 0, 0, 82)
    a.rot("root", 2.4, 0, 0, 84)
    return m


BUILDERS = {"hoplit": build_hoplit, "spartan_warrior": build_spartan,
            "greek_archer": build_archer, "minotaur": build_minotaur}

# vistas de muestra para la hoja de previsualizacion: (anim, tiempo, yaw)
SHOTS = {
    "hoplit": [("rest", 0, -30), ("rest", 0, 150), ("attack", 0.2, -60), ("attack", 0.35, -60)],
    "spartan_warrior": [("rest", 0, -30), ("rest", 0, 150), ("attack", 0.3, -60), ("block", 0.4, -30)],
    "greek_archer": [("rest", 0, -30), ("rest", 0, 150), ("shoot", 0.38, -60), ("shoot", 0.38, 30)],
    "minotaur": [("rest", 0, -30), ("rest", 0, 150), ("attack", 0.3, -60), ("charge", 0.5, -70)],
}


def previews(name, m):
    import render_preview as RP
    RP.G = m
    tw, th = m.pack()
    tex = m.paint(tw, th)
    anims = {a.name: a for a in m.ANIMS}
    focus, scale = (26, 6.0) if name == "minotaur" else (18, 8.5)
    frames = []
    for an, t, yaw in SHOTS[name]:
        im = RP.render(tex, anims.get(an), t, yaw=yaw, size=(340, 420), focus=focus, scale=scale)
        ImageDraw.Draw(im).text((8, 8), f"{name}  {an} {t:g}s", fill=(230, 230, 230))
        frames.append(im)
    W, H = frames[0].size
    sheet = Image.new("RGB", (W * len(frames), H), (20, 20, 24))
    for i, f in enumerate(frames):
        sheet.paste(f, (i * W, 0))
    PREVIEW.mkdir(parents=True, exist_ok=True)
    sheet.save(PREVIEW / f"{name}.png")


def main():
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    for name, fn in BUILDERS.items():
        if only and name not in only:
            continue
        m = fn()
        m.build(BLUEPRINTS / name / f"{name}.bbmodel")
        print(f"OK {name}: cubos={len(m.CUBES)} huesos={len(m.BONES)} anims={[a.name for a in m.ANIMS]}")
        if "--no-preview" not in sys.argv:
            previews(name, m)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    main()
