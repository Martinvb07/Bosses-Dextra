#!/usr/bin/env python3
"""
Boss 02 - OLD ENDER y sus subditos (modelos de ModelEngine).

  old_ender        enderman faraon: cuerpo del vacio con vetas moradas, nemes dorado
                   y azul con cobra, collar usekh, vendas de lino, garras y orbes
  sand_warden      guardian de arenisca (HUSK)
  mummy_guardian   momia vendada con amuleto de escarabajo (HUSK)
  giant_scarab     escarabajo gigante de oro y lapislazuli (SPIDER)
  desert_priest    sacerdote con mascara de chacal y baston con ankh (STRAY)

Uso: python3 tools/b02_oldender.py [modelo ...] [--no-preview]
"""
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
from bbmodel import Model, mul  # noqa: E402
import generate_minions as GM  # noqa: E402
import anatomy as AN  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent / "Modelos/02_OldEnder"
BLUEPRINTS = ROOT / "ModelEngine/blueprints"
PREVIEW = ROOT / "preview"

PURPLE_GLOW = (214, 120, 255)
GOLD_HI = (255, 236, 150)


def egypt_decor(m):
    D = m.decor

    @D
    def d_ender_face(f):
        w = f.w
        for ex in (1, w - 7):
            f.rect(ex, 7, ex + 6, 9, (120, 30, 170))
            f.rect(ex + 1, 7, ex + 5, 8, PURPLE_GLOW)
            f.put(ex + 2, 7, (250, 220, 255))

    @D
    def d_void(f):
        rng = random.Random(f.x0 * 31 + f.y0)
        for _ in range(max(1, f.w * f.h // 18)):
            x, y = rng.randrange(f.w), rng.randrange(f.h)
            f.put(x, y, (70, 30, 110))
            if rng.random() < 0.4 and y + 1 < f.h:
                f.put(x, y + 1, (110, 50, 160))

    @D
    def d_linen(f):
        for y in range(f.h):
            for x in range(f.w):
                if (x + y * 2) % 6 == 0:
                    f.shade(x, y, 0.82)
        for x in range(f.w):
            f.shade(x, 0, 1.08)

    @D
    def d_nemes(f):
        lapis = m.MAT["lapis"]
        if f.name in ("up", "down"):
            for x in range(f.w):
                if (x // 2) % 2:
                    for y in range(f.h):
                        f.put(x, y, mul(lapis, 1.05 if f.name == "up" else 0.8))
            return
        for x in range(f.w):
            if (x // 2) % 2:
                for y in range(f.h):
                    f.put(x, y, mul(lapis, 1.0 - 0.12 * y / max(1, f.h)))

    @D
    def d_usekh(f):
        rows = [m.MAT["gold"], m.MAT["lapis"], m.MAT["turquoise"], m.MAT["gold"], (190, 40, 40), m.MAT["gold"]]
        for y in range(f.h):
            c = rows[(y // 1) % len(rows)]
            for x in range(f.w):
                f.put(x, y, mul(c, 1.0 if x % 3 else 0.85))

    @D
    def d_shendyt(f):
        if f.name in ("up", "down"):
            return
        for x in range(0, f.w, 3):
            for y in range(f.h):
                f.shade(x, y, 0.8)
        for x in range(f.w):
            f.put(x, f.h - 1, m.MAT["gold"])
            f.put(x, 0, m.MAT["gold"])

    @D
    def d_orb(f):
        f.rect(0, 0, f.w, f.h, (90, 20, 130))
        f.rect(1, 1, f.w - 1, f.h - 1, PURPLE_GLOW)
        f.put(1, 1, (250, 230, 255))

    @D
    def d_claw(f):
        for y in range(f.h):
            f.put(f.w // 2, y, (230, 180, 255))

    @D
    def d_gold_band(f):
        for x in range(f.w):
            f.put(x, 1, GOLD_HI)
        for x in range(1, f.w, 3):
            f.put(x, f.h // 2, m.MAT["lapis"])

    @D
    def d_sandstone(f):
        for y in range(0, f.h, 4):
            for x in range(f.w):
                f.shade(x, y, 0.85)
        for y in range(f.h):
            off = 0 if (y // 4) % 2 else 3
            for x in range(off, f.w, 6):
                f.shade(x, y, 0.82)

    @D
    def d_warden_face(f):
        w = f.w
        f.rect(1, 5, w - 1, 6, (110, 80, 40))
        for ex in (2, w - 5):
            f.rect(ex, 6, ex + 3, 8, (255, 170, 40))
            f.put(ex + 1, 6, (255, 240, 170))
        f.rect(w // 2 - 2, 10, w // 2 + 2, 11, (90, 60, 30))

    @D
    def d_mummy_face(f):
        w = f.w
        for y in range(0, f.h, 2):
            for x in range(w):
                f.shade(x, (y + x // 3) % f.h, 0.85)
        for ex in (2, w - 5):
            f.rect(ex, 6, ex + 3, 8, (20, 15, 10))
            f.put(ex + 1, 7, (120, 255, 140))

    @D
    def d_scarab_shell(f):
        if f.name == "down":
            return
        w = f.w
        for y in range(f.h):
            f.put(w // 2, y, GOLD_HI)
        for y in range(1, f.h, 3):
            for x in range(1, w - 1):
                if x != w // 2:
                    f.shade(x, y, 1.12)

    @D
    def d_jackal(f):
        w = f.w
        for ex in (1, w - 4):
            f.rect(ex, 3, ex + 3, 5, (250, 200, 60))
            f.put(ex + 1, 4, (30, 20, 10))
        for x in range(w):
            f.put(x, f.h - 2, m.MAT["gold"])

    @D
    def d_robe(f):
        if f.name in ("up", "down"):
            return
        for x in range(0, f.w, 4):
            for y in range(f.h):
                f.shade(x, y, 0.85)
        for x in range(f.w):
            f.put(x, f.h - 2, m.MAT["gold"])

    @D
    def d_warden_face2(f):
        w = f.w
        for ex in (2, w - 5):
            f.rect(ex, 6, ex + 3, 8, (255, 160, 30))
            f.put(ex + 1, 6, (255, 240, 170))
        for y in range(8, f.h):
            f.shade(w // 2 - 1 + (y % 2), y, 0.7)

    @D
    def d_core(f):
        f.rect(0, 0, f.w, f.h, (255, 120, 20))
        for y in range(f.h):
            f.put((y * 2) % f.w, y, (255, 230, 140))

    @D
    def d_wrap(f):
        rng = random.Random(f.x0 * 13 + f.y0 * 7)
        for y in range(f.h):
            for x in range(f.w):
                if (x + y) % 4 == 0:
                    f.shade(x, y, 0.84)
                elif (x - y) % 7 == 0:
                    f.shade(x, y, 1.08)
        for _ in range(f.w * f.h // 30):
            f.shade(rng.randrange(f.w), rng.randrange(f.h), 0.7)

    @D
    def d_mummy_face2(f):
        w = f.w
        dark = (24, 18, 12)
        for ex in (2, w - 6):
            f.rect(ex, 6, ex + 4, 9, dark)
            f.rect(ex + 1, 7, ex + 3, 8, (110, 255, 140))
            f.put(ex + 1, 7, (220, 255, 220))
        f.rect(w // 2 - 1, 9, w // 2 + 1, 11, (150, 132, 96))
        f.rect(w // 2 - 3, 12, w // 2 + 3, 13, dark)

    @D
    def d_jackal2(f):
        w = f.w
        for ex in (1, w - 5):
            f.rect(ex, 6, ex + 4, 8, (250, 200, 60))
            f.put(ex + (1 if ex < w // 2 else 2), 7, (20, 14, 10))
            f.rect(ex, 8, ex + 4, 9, m.MAT["lapis"])

    @D
    def d_ear_in(f):
        f.rect(1, 1, f.w - 1, f.h, m.MAT["gold"])
        f.rect(2, 2, f.w - 2, f.h, (150, 40, 40))

    @D
    def d_apron(f):
        if f.name in ("up", "down"):
            return
        for y in range(f.h):
            c = m.MAT["lapis"] if (y // 2) % 2 else m.MAT["gold"]
            for x in range(1, f.w - 1):
                f.put(x, y, mul(c, 1.0 if x % 2 else 0.88))


MATS = {
    "void": ((22, 16, 32), 4), "purple": ((150, 60, 210), 8), "gold": ((222, 172, 52), 9),
    "linen": ((212, 194, 150), 8), "lapis": ((40, 72, 168), 6), "turquoise": ((60, 168, 160), 6),
    "skin": ((22, 16, 32), 4), "leather": ((110, 72, 40), 9), "bronze": ((196, 140, 58), 8), "hitbox": ((255, 255, 255), 0),
}


# ===========================================================================
# OLD ENDER
# ===========================================================================
OE_BONES = ["body", "torso", "h_head", "right_arm", "right_forearm", "right_hand", "left_arm",
            "left_forearm", "left_hand", "right_leg", "right_lower_leg", "left_leg", "left_lower_leg",
            "shendyt_front", "shendyt_back", "orb_r", "orb_l", "nemes_tail"]


def build_old_ender():
    m = Model("old_ender", MATS, seed=202)
    m.SHINE |= {"gold"}
    egypt_decor(m)
    root = m.root
    hb = m.bone("hitbox", (0, 44, 0), root)
    m.cube(hb, "hitbox", (-7, 0, -7), (7, 49, 7), "hitbox")
    m.bone("tag_name", (0, 54, 0), root)

    V = {"decor": {"all": "void"}}
    LN = {"decor": {"all": "linen"}}
    GB = {"decor": {"all": "gold_band"}}
    legs = {}
    for side, sx in (("right", 1), ("left", -1)):
        leg = m.bone(f"{side}_leg", (2.5 * sx, 26, 0), root)
        low = m.bone(f"{side}_lower_leg", (2.5 * sx, 13, 0), leg)
        legs[side] = (leg, low)
    R, L = legs["right"], legs["left"]
    m.cube_lr(R[0], L[0], "thigh", (0.8, 19, -1.7), (4.2, 26.4, 1.7), "void", **V)
    m.cube_lr(R[0], L[0], "thigh_low", (1.1, 13.5, -1.4), (3.9, 19.2, 1.4), "void", **V)
    m.cube_lr(R[0], L[0], "knee_wrap", (0.85, 12.2, -1.75), (4.15, 15, 1.75), "linen", **LN)
    m.cube_lr(R[0], L[0], "thigh_strip", (3.6, 15.5, -1.0), (4.2, 20.5, 0.2), "linen", rot=("z", 22.5),
              pivot=(3.9, 20.5, 0), **LN)
    m.cube_lr(R[1], L[1], "calf", (1.1, 7, -1.3), (3.9, 13, 1.6), "void", **V)
    m.cube_lr(R[1], L[1], "shin", (1.4, 1.6, -1.1), (3.6, 7.2, 1.1), "void", **V)
    m.cube_lr(R[1], L[1], "anklet", (1.1, 1.6, -1.4), (3.9, 3.0, 1.4), "gold", **GB)
    m.cube_lr(R[1], L[1], "foot", (0.9, 0, -2.4), (4.1, 1.6, 1.5), "void")
    for i, x in enumerate((1.4, 2.5, 3.6)):
        m.cube_lr(R[1], L[1], f"toe_claw{i}", (x - 0.35, 0, -4.0), (x + 0.35, 0.8, -2.3), "purple")

    body = m.bone("body", (0, 26, 0), root)
    waist = m.bone("waist", (0, 26, 0), body)
    m.cube(waist, "belt", (-4.3, 24.6, -2.4), (4.3, 27, 2.4), "gold", **GB)
    m.cube_lr(waist, waist, "shendyt_side", (3.4, 17.5, -2.3), (4.1, 25, 2.3), "linen", rot=("z", 22.5),
              pivot=(3.8, 25, 0), decor={"all": "shendyt"})
    sf = m.bone("shendyt_front", (0, 24.5, -2.5), waist)
    m.cube(sf, "shendyt_front", (-3.6, 15.5, -2.9), (3.6, 24.5, -2.35), "linen", decor={"all": "shendyt"})
    m.cube(sf, "apron", (-1.4, 14.2, -3.2), (1.4, 24.2, -2.8), "gold", decor={"all": "gold_band"})
    sb = m.bone("shendyt_back", (0, 24.5, 2.5), waist)
    m.cube(sb, "shendyt_back", (-3.6, 16.5, 2.35), (3.6, 24.5, 2.9), "linen", decor={"all": "shendyt"})

    torso = m.bone("torso", (0, 27, 0), body)
    m.cube(torso, "waist_void", (-3.0, 27, -1.7), (3.0, 31.5, 1.7), "void", **V)
    m.cube(torso, "ribs", (-3.7, 31, -2.0), (3.7, 34.5, 2.0), "void", **V)
    m.cube(torso, "chest", (-4.4, 34, -2.2), (4.4, 37.6, 2.1), "void", **V)
    m.cube(torso, "chest_wrap", (-4.1, 29.4, -2.1), (4.1, 30.6, 2.1), "linen", rot=("z", 22.5), **LN)
    m.cube(torso, "chest_wrap2", (-4.1, 31.6, -2.2), (4.1, 32.6, 2.2), "linen", rot=("z", -22.5), **LN)
    m.cube(torso, "usekh", (-4.8, 35.2, -2.9), (4.8, 38.2, 2.7), "gold", decor={"all": "usekh"})
    m.cube_lr(torso, torso, "usekh_shoulder", (0.8, 37.4, -2.5), (6.8, 38.6, 2.5), "gold", rot=("z", -22.5),
              pivot=(0.8, 38, 0), decor={"all": "usekh"})
    m.cube(torso, "pendant", (-1.0, 33.0, -2.7), (1.0, 35.4, -2.2), "lapis", **GB)
    m.cube(torso, "pendant_gem", (-0.5, 33.6, -2.95), (0.5, 34.6, -2.6), "purple", decor={"all": "orb"})
    m.cube(torso, "neck", (-1.4, 37.6, -1.4), (1.4, 39.6, 1.4), "void")
    strip = m.bone("chest_strip", (2.5, 29.5, -2.1), torso)
    m.cube(strip, "chest_strip", (2.0, 23.5, -2.4), (3.0, 29.5, -2.0), "linen", rot=("z", -22.5),
           pivot=(2.5, 29.5, -2.2), **LN)

    head = m.bone("h_head", (0, 39, 0), torso)
    m.cube(head, "head", (-4, 39.6, -4), (4, 47, 4), "void", decor={"north": "ender_face", "all": "void"})
    m.cube(head, "jaw", (-3.4, 38.8, -3.8), (3.4, 40.2, 3.0), "void", **V)
    m.cube(head, "nemes_top", (-4.5, 44.5, -4.5), (4.5, 48, 4.5), "gold", decor={"all": "nemes"})
    m.cube(head, "nemes_crown", (-3.6, 48, -3.8), (3.6, 49, 4.0), "gold", decor={"all": "nemes"})
    m.cube(head, "nemes_band", (-4.6, 44, -4.6), (4.6, 45, 4.6), "gold", **GB)
    m.cube_lr(head, head, "lappet", (4.0, 36.0, -3.4), (5.4, 45.0, 0.2), "gold", rot=("z", 22.5),
              pivot=(4.7, 45, -1.6), decor={"all": "nemes"})
    m.cube_lr(head, head, "lappet_front", (3.6, 33.6, -3.6), (5.0, 38.4, -1.4), "gold", decor={"all": "nemes"})
    m.cube(head, "uraeus_body", (-0.6, 46.6, -5.4), (0.6, 48.4, -4.4), "gold")
    m.cube(head, "uraeus_hood", (-1.6, 48.0, -5.7), (1.6, 50.2, -4.9), "gold", rot=("x", -22.5),
           pivot=(0, 48, -5.3), decor={"all": "gold_band"})
    m.cube(head, "uraeus_head", (-0.6, 49.8, -6.6), (0.6, 50.8, -5.2), "gold")
    m.cube(head, "uraeus_eye", (-0.3, 50.3, -6.75), (0.3, 50.7, -6.5), "purple")
    tail = m.bone("nemes_tail", (0, 46, 4.5), head)
    m.cube(tail, "nemes_tail", (-2.4, 37.5, 4.2), (2.4, 46, 5.3), "gold", decor={"all": "nemes"})
    m.cube(tail, "nemes_tail_tip", (-1.6, 35.5, 4.2), (1.6, 37.6, 5.0), "gold", decor={"all": "gold_band"})

    arms = {}
    for side, sx in (("right", 1), ("left", -1)):
        arm = m.bone(f"{side}_arm", (5.75 * sx, 37, 0), torso)
        fore = m.bone(f"{side}_forearm", (5.75 * sx, 26, 0), arm)
        hand = m.bone(f"{side}_hand", (5.75 * sx, 15, 0), fore)
        arms[side] = (arm, fore, hand)
    AR, AL = arms["right"], arms["left"]
    m.cube_lr(AR[0], AL[0], "deltoid", (4.3, 33.6, -1.7), (7.3, 37.8, 1.7), "void", **V)
    m.cube_lr(AR[0], AL[0], "upper_arm", (4.6, 26, -1.2), (6.9, 34, 1.2), "void", **V)
    m.cube_lr(AR[0], AL[0], "arm_wrap", (4.35, 29.5, -1.45), (7.15, 30.6, 1.45), "linen", rot=("z", 22.5), **LN)
    m.cube_lr(AR[1], AL[1], "elbow", (4.5, 24.4, -1.3), (7.0, 26.6, 1.5), "void", **V)
    m.cube_lr(AR[1], AL[1], "forearm", (4.7, 15, -1.1), (6.8, 24.6, 1.1), "void", **V)
    m.cube_lr(AR[1], AL[1], "bracer", (4.4, 15.8, -1.4), (7.1, 19.6, 1.4), "gold", **GB)
    m.cube_lr(AR[1], AL[1], "wrist_strip", (6.3, 13.0, 0.4), (7.0, 18.5, 1.1), "linen", rot=("x", 22.5),
              pivot=(6.6, 18.5, 0.7), **LN)
    m.cube_lr(AR[2], AL[2], "palm", (4.6, 12.4, -1.35), (6.9, 15.2, 1.35), "void")
    for i, z in enumerate((-1.0, 0, 1.0)):
        m.cube_lr(AR[2], AL[2], f"claw_{i}", (5.4, 10, z - 0.35), (6.1, 12.6, z + 0.35), "purple", decor={"all": "claw"})
        m.cube_lr(AR[2], AL[2], f"claw_tip_{i}", (5.5, 7.8, z - 0.3), (6.0, 10.2, z + 0.3), "purple",
                  rot=("x", -22.5), pivot=(5.75, 10.1, z), decor={"all": "claw"})

    for side, sx in (("r", 1), ("l", -1)):
        orb = m.bone(f"orb_{side}", (10 * sx, 40, 3), torso)
        cx = 10 * sx
        m.cube(orb, f"orb_{side}", (cx - 1, 39, 2), (cx + 1, 41, 4), "purple", decor={"all": "orb"},
               rot=("y", 45), pivot=(cx, 40, 3))
        m.cube(orb, f"orb_{side}_ring", (cx - 1.6, 39.8, 1.4), (cx + 1.6, 40.2, 4.6), "gold",
               rot=("z", 22.5), pivot=(cx, 40, 3))

    m.ZERO_BONES = list(OE_BONES) + ["chest_strip"]

    def orbs(a, t, s):
        a.pos("orb_r", t, 0, 1.2 * s, 0)
        a.pos("orb_l", t, 0, -1.2 * s + 1.2, 0)

    # ---- IDLE / WALK ----
    a = m.anim("idle", 3.0, "loop")
    for t, s in ((0, 0), (1.5, 1), (3.0, 0)):
        a.pos("body", t, 0, -0.3 * s, 0)
        a.rot("torso", t, 4 - 2 * s, 0, 0)
        a.rot("h_head", t, -3 + 3 * s, 4 * s - 2, 0)
        a.rot("right_arm", t, 0, 0, 4 + 2 * s)
        a.rot("left_arm", t, 0, 0, -4 - 2 * s)
        a.rot("right_forearm", t, -6 - 3 * s, 0, 0)
        a.rot("left_forearm", t, -6 - 3 * s, 0, 0)
        a.rot("nemes_tail", t, 3 * s, 0, 0)
        orbs(a, t, s)
    a = m.anim("walk", 1.6, "loop")
    h, q = 0.8, 0.4
    for t, s in ((0, 1), (h, -1), (1.6, 1)):
        a.rot("right_leg", t, -22 * s, 0, 0)
        a.rot("left_leg", t, 22 * s, 0, 0)
        a.rot("right_arm", t, 14 * s, 0, 4)
        a.rot("left_arm", t, -14 * s, 0, -4)
        a.rot("torso", t, 6, -4 * s, 0)
        a.rot("h_head", t, -4, 4 * s, 0)
        a.rot("shendyt_front", t, -10, 0, 0)
        a.rot("nemes_tail", t, 8, 0, 3 * s)
    for t, s in ((0, 0), (q, 1), (h, 0), (h + q, 1), (1.6, 0)):
        a.pos("body", t, 0, -0.6 * s, 0)
        orbs(a, t, s)
    for bone, keys in (("right_lower_leg", (0, 10, 30, 12, 0)), ("left_lower_leg", (30, 12, 0, 10, 30))):
        for t, x in zip((0, q, h, h + q, 1.6), keys):
            a.rot(bone, t, x, 0, 0)

    # ---- ATTACK: zarpazo (impacto 0.25 s = 5 ticks) ----
    a = m.anim("attack", 0.6, "once")
    a.rest(0)
    a.pose(0.15, {"right_arm": (-150, 0, 20), "right_forearm": (-30, 0, 0), "torso": (-6, 20, 0)})
    a.pose(0.25, {"right_arm": (-30, 0, -15), "right_forearm": (-10, 0, 0), "torso": (12, -20, 0),
                  "h_head": (-8, 10, 0)}, i="linear")
    a.rest(0.6)

    # ---- TELEPORT_STRIKE: se encoge, desaparece y golpea (impacto 0.6 s = 12 ticks) ----
    a = m.anim("teleport_strike", 1.0, "once")
    a.rest(0)
    a.pose(0.2, {"body": {"p": (0, -6, 0)}, "torso": (30, 0, 0), "right_arm": (40, 0, 30), "left_arm": (40, 0, -30),
                 "right_leg": (-40, 0, 0), "left_leg": (-40, 0, 0), "right_lower_leg": (70, 0, 0),
                 "left_lower_leg": (70, 0, 0)})
    a.pose(0.45, {"body": {"p": (0, 1, -2)}, "torso": (-10, 0, 0), "right_arm": (-170, 0, 10),
                  "left_arm": (-170, 0, -10), "right_leg": (0, 0, 0), "left_leg": (0, 0, 0),
                  "right_lower_leg": (0, 0, 0), "left_lower_leg": (0, 0, 0)})
    a.pose(0.6, {"body": {"p": (0, -2, -2)}, "torso": (35, 0, 0), "right_arm": (-40, 0, -10),
                 "left_arm": (-40, 0, 10), "h_head": (-25, 0, 0)}, i="linear")
    a.rest(1.0)

    # ---- PULSE: abre los brazos y libera la onda (impacto 0.15 s) ----
    a = m.anim("pulse", 0.9, "once")
    a.rest(0)
    a.pose(0.08, {"right_arm": (-20, 0, 30), "left_arm": (-20, 0, -30), "torso": (10, 0, 0)})
    a.pose(0.15, {"right_arm": (-10, 0, 95), "left_arm": (-10, 0, -95), "right_forearm": (0, 0, 0),
                  "left_forearm": (0, 0, 0), "torso": (-14, 0, 0), "h_head": (-20, 0, 0)}, i="linear")
    a.pose(0.5, {"right_arm": (-10, 0, 90), "left_arm": (-10, 0, -90), "torso": (-12, 0, 0)})
    a.rest(0.9)

    # ---- COLLAPSE: golpe a dos manos contra el suelo (impacto 0.5 s = 10 ticks) ----
    a = m.anim("collapse", 1.1, "once")
    a.rest(0)
    a.pose(0.35, {"right_arm": (-175, 0, -10), "left_arm": (-175, 0, 10), "torso": (-10, 0, 0),
                  "h_head": (-15, 0, 0), "body": {"p": (0, 1.5, 0)}})
    a.pose(0.5, {"right_arm": (-40, 0, -10), "left_arm": (-40, 0, 10), "torso": (40, 0, 0), "h_head": (-25, 0, 0),
                 "body": {"p": (0, -5, 0)}, "right_leg": (-30, 0, 0), "left_leg": (-30, 0, 0),
                 "right_lower_leg": (55, 0, 0), "left_lower_leg": (55, 0, 0)}, i="linear")
    a.pose(0.7, {"torso": (38, 0, 0), "body": {"p": (0, -4.5, 0)}})
    a.rest(1.1)

    # ---- GAZE: clava la mirada (rayo en 0.5 s = 10 ticks) ----
    a = m.anim("gaze", 1.1, "once")
    a.rest(0)
    gaze = {"h_head": (-10, 0, 0), "torso": (14, 0, 0), "right_arm": (25, 0, 25), "left_arm": (25, 0, -25),
            "right_forearm": (-40, 0, 0), "left_forearm": (-40, 0, 0)}
    a.pose(0.3, gaze)
    for i, t in enumerate([0.35 + 0.05 * n for n in range(5)]):
        a.rot("h_head", t, -10, 0, 3 if i % 2 else -3, i="linear")
    a.pose(0.6, gaze)
    a.rest(1.1)

    # ---- SANDSTORM: gira con los brazos en alto (1.6 s) ----
    a = m.anim("sandstorm", 1.6, "once")
    a.rest(0)
    storm = {"right_arm": (-160, 0, 30), "left_arm": (-160, 0, -30), "h_head": (-25, 0, 0), "torso": (-8, 0, 0)}
    a.pose(0.3, storm)
    for t, y in ((0.3, 0), (0.7, 120), (1.1, 240), (1.4, 360)):
        a.rot("body", t, 0, y, 0, i="linear")
    a.pose(1.4, storm)
    a.rot("body", 1.6, 0, 360, 0)
    a.rest(1.6, ["right_arm", "left_arm", "h_head", "torso"])

    # ---- WARP: se retuerce y arrastra (golpe 0.4 s = 8 ticks) ----
    a = m.anim("warp", 0.9, "once")
    a.rest(0)
    a.pose(0.2, {"torso": (0, 45, 0), "right_arm": (-90, 60, 0), "left_arm": (-90, -20, 0)})
    a.pose(0.4, {"torso": (10, -40, 0), "right_arm": (-60, -40, 0), "left_arm": (-60, 40, 0)}, i="linear")
    a.rest(0.9)

    # ---- SUMMON / PHASE / HURT / SPAWN / DEATH ----
    a = m.anim("summon", 1.4, "once")
    a.rest(0)
    up = {"right_arm": (-170, 0, 20), "left_arm": (-170, 0, -20), "h_head": (-35, 0, 0), "torso": (-10, 0, 0)}
    a.pose(0.4, up)
    a.pose(1.0, up)
    a.rest(1.4)

    a = m.anim("phase_change", 1.8, "once")
    a.rest(0)
    a.pose(0.4, {"body": {"p": (0, -4, 0)}, "torso": (35, 0, 0), "right_arm": (30, 0, 20), "left_arm": (30, 0, -20),
                 "right_leg": (-25, 0, 0), "left_leg": (-25, 0, 0), "right_lower_leg": (45, 0, 0),
                 "left_lower_leg": (45, 0, 0)})
    a.pose(0.9, {"body": {"p": (0, 1, 0)}, "torso": (-18, 0, 0), "h_head": (-35, 0, 0), "right_arm": (-30, 0, 90),
                 "left_arm": (-30, 0, -90), "right_leg": (0, 0, 0), "left_leg": (0, 0, 0),
                 "right_lower_leg": (0, 0, 0), "left_lower_leg": (0, 0, 0)})
    a.pose(1.4, {"torso": (-18, 0, 0), "right_arm": (-30, 0, 90), "left_arm": (-30, 0, -90)})
    a.rest(1.8)

    a = m.anim("hurt", 0.35, "once")
    bones = ["torso", "h_head", "right_arm", "left_arm"]
    a.rest(0, bones)
    a.pose(0.08, {"torso": (-10, 0, 4), "h_head": (-14, 0, 0), "right_arm": (8, 0, 10), "left_arm": (8, 0, -10)})
    a.rest(0.35, bones)

    a = m.anim("spawn", 2.4, "once")
    a.pos("body", 0, 0, -27, 0)
    a.pose(0, {"torso": (20, 0, 0), "right_arm": (-170, 0, 20), "left_arm": (-170, 0, -20), "h_head": (-30, 0, 0)})
    a.pos("body", 1.4, 0, 0, 0)
    a.pose(1.4, {"torso": (-10, 0, 0), "right_arm": (-160, 0, 30), "left_arm": (-160, 0, -30), "h_head": (-30, 0, 0)})
    a.pose(1.9, {"torso": (-10, 0, 0), "right_arm": (-20, 0, 80), "left_arm": (-20, 0, -80), "h_head": (-15, 0, 0)})
    a.rest(2.4)
    for t, s in ((0, 0), (1.2, 1), (2.4, 0)):
        orbs(a, t, s)

    a = m.anim("death", 2.6, "hold")
    a.rest(0)
    a.pose(0.4, {"torso": (-20, 0, 0), "h_head": (-40, 0, 0), "right_arm": (-60, 0, 70), "left_arm": (-60, 0, -70)})
    a.pose(1.2, {"body": {"p": (0, -9, 0)}, "torso": (25, 0, 0), "h_head": (20, 0, 0), "right_leg": (10, 0, 0),
                 "left_leg": (10, 0, 0), "right_lower_leg": (85, 0, 0), "left_lower_leg": (85, 0, 0),
                 "right_arm": (10, 0, 10), "left_arm": (10, 0, -10)}, i="linear")
    # se hunde en la arena
    a.pos("body", 1.6, 0, -9, 0)
    a.pos("body", 2.6, 0, -40, 0, i="linear")
    a.pos("orb_r", 1.2, 0, 0, 0)
    a.pos("orb_r", 2.0, 0, 12, 0, i="linear")
    a.pos("orb_l", 1.2, 0, 0, 0)
    a.pos("orb_l", 2.0, 0, 12, 0, i="linear")
    return m


# ===========================================================================
# SUBDITOS HUMANOIDES (usan el cuerpo base de generate_minions)
# ===========================================================================
def _base(name, mats, seed):
    m = Model(name, {**MATS, **mats}, seed=seed)
    m.SHINE |= {"gold"}
    GM.add_common_decor(m)
    egypt_decor(m)
    return m


def build_sand_warden():
    m = _base("sand_warden", {"skin": ((214, 190, 128), 10), "sandstone": ((214, 190, 128), 10),
                              "rock": ((176, 146, 92), 12), "core": ((255, 150, 40), 6)}, 2021)
    m.SHINE |= {"core"}
    S = {"decor": {"all": "sandstone"}}

    def head(m, hd):
        m.cube(hd, "skull", (-3.6, 25.2, -3.4), (3.6, 31.4, 3.6), "sandstone", decor={"north": "warden_face2", "all": "sandstone"})
        m.cube(hd, "jaw", (-3.2, 24.2, -3.9), (3.2, 26.0, 2.0), "rock", **S)
        m.cube(hd, "brow", (-4.0, 29.4, -4.3), (4.0, 30.8, -2.6), "rock", **S)
        m.cube(hd, "crown", (-3.2, 31.2, -2.8), (3.2, 32.4, 3.0), "rock", **S)
        m.cube(hd, "crown_spike", (-1.0, 31.8, -1.5), (1.0, 34.6, 0.5), "rock", rot=("x", -22.5), **S)
        m.cube_lr(hd, hd, "cheek", (3.2, 25.6, -3.2), (4.2, 28.4, 1.0), "rock", **S)

    H = AN.humanoid(m, k=1.25, mats={"skin": "sandstone", "hand": "rock", "foot": "rock"}, head=head)
    torso, (AR, AL) = H["torso"], (H["arms"]["right"], H["arms"]["left"])
    for c in m.CUBES:
        if c.mat in ("sandstone", "rock"):
            c.decor.setdefault("all", "sandstone")
    # nucleo encendido que asoma por las grietas del pecho
    m.cube(torso, "core", (-1.6, 19.6, -3.9), (1.6, 22.4, -3.3), "core", decor={"all": "core"})
    m.cube_lr(torso, torso, "chest_slab", (1.4, 19.0, -4.0), (5.6, 23.8, -2.8), "rock", rot=("z", -22.5),
              pivot=(1.4, 23.8, -3.4), **S)
    m.cube(torso, "back_slab", (-4.6, 18.4, 2.9), (4.6, 23.6, 4.0), "rock", **S)
    for i, (x, y) in enumerate(((-2.4, 21.6), (1.8, 22.2), (0, 19.2))):
        m.cube(torso, f"back_spike{i}", (x - 0.9, y, 3.6), (x + 0.9, y + 1.8, 6.4), "rock", rot=("x", 22.5),
               pivot=(x, y + 0.9, 3.6), **S)
    m.cube_lr(AR[0], AL[0], "boulder", (4.4, 21.8, -2.9), (9.6, 26.2, 2.9), "rock", rot=("z", -22.5),
              pivot=(6.5, 23, 0), **S)
    m.cube_lr(AR[2], AL[2], "fist", (4.4, 8.0, -2.3), (8.6, 12.0, 2.3), "rock", **S)
    m.cube_lr(AR[2], AL[2], "knuckles", (4.6, 7.4, -2.6), (8.4, 9.0, -0.6), "rock", **S)
    m.cube_lr(H["legs"]["right"][1], H["legs"]["left"][1], "shin_rock", (0.4, 3.0, -2.5), (4.6, 6.6, -1.4),
              "rock", rot=("x", 22.5), pivot=(2.5, 6.6, -2), **S)
    m.cube(H["waist"], "loin", (-3.2, 8.6, -3.6), (3.2, 13.4, -3.0), "rock", **S)

    GM.human_idle(m, arm_l=(-8, 0, -8), arm_r=(-8, 0, 8),
                  extra=lambda a, t, s: a.rot("torso", t, 10 - 2 * s, 0, 0))
    GM.human_walk(m, leg=22, arm=14, bob=0.9, lean=10)
    a = m.anim("attack", 0.7, "once")          # golpe con el puno (impacto 0.3 s)
    a.rest(0)
    a.pose(0.18, {"right_arm": (-140, 0, 15), "torso": (-6, 15, 0)})
    a.pose(0.3, {"right_arm": (-40, 0, -10), "torso": (16, -15, 0), "h_head": (-8, 0, 0)}, i="linear")
    a.rest(0.7)
    GM.human_hurt(m)
    a = m.anim("spawn", 1.6, "once")            # sale de la arena
    a.pos("body", 0, 0, -16, 0)
    a.pose(0, {"right_arm": (-160, 0, 15), "left_arm": (-160, 0, -15)})
    a.pos("body", 1.0, 0, 0, 0)
    a.pose(1.0, {"right_arm": (-30, 0, 20), "left_arm": (-30, 0, -20), "torso": (-10, 0, 0)})
    a.rest(1.6)
    a = m.anim("death", 2.0, "hold")            # se deshace en arena
    a.rest(0)
    a.pose(0.5, {"torso": (25, 0, 0), "h_head": (20, 0, 0), "right_arm": (10, 0, 20), "left_arm": (10, 0, -20)})
    a.pos("body", 0.5, 0, 0, 0)
    a.pos("body", 2.0, 0, -18, 0, i="linear")
    return m


def build_mummy_guardian():
    m = _base("mummy_guardian", {"skin": ((200, 186, 150), 9), "bandage": ((206, 192, 156), 9),
                                 "dirty": ((150, 132, 96), 9), "rot": ((58, 44, 34), 6)}, 2022)
    W = {"decor": {"all": "wrap"}}

    def head(m, hd):
        m.cube(hd, "skull", (-3.3, 25.6, -3.2), (3.3, 32.0, 3.4), "bandage", decor={"north": "mummy_face2", "all": "wrap"})
        m.cube(hd, "jaw", (-2.6, 24.6, -3.3), (2.6, 26.2, 1.4), "dirty", **W)
        m.cube(hd, "brow", (-3.4, 28.8, -3.7), (3.4, 29.7, -3.0), "dirty", **W)
        m.cube(hd, "head_wrap", (-3.6, 27.6, -3.6), (3.6, 28.6, 3.7), "bandage", rot=("z", 22.5), **W)
        m.cube(hd, "head_wrap2", (-3.5, 30.4, -3.5), (3.5, 31.2, 3.6), "dirty", rot=("z", -22.5), **W)
        tail = m.bone("head_strip", (1.5, 29.5, 3.4), hd)
        m.cube(tail, "head_strip", (1.0, 22.5, 3.3), (2.2, 29.5, 3.8), "bandage", rot=("x", 22.5),
               pivot=(1.5, 29.5, 3.4), **W)

    H = AN.humanoid(m, k=0.85, mats={"skin": "bandage", "belly": "rot", "hand": "dirty", "foot": "dirty"}, head=head)
    torso, waist, (AR, AL) = H["torso"], H["waist"], (H["arms"]["right"], H["arms"]["left"])
    for c in m.CUBES:
        if c.mat in ("bandage", "dirty"):
            c.decor.setdefault("all", "wrap")
    # vendas cruzadas en diagonal (dejan ver la carne seca del vientre)
    for i, (y, ang, mat) in enumerate(((16.0, 22.5, "bandage"), (17.6, -22.5, "dirty"), (19.6, 22.5, "bandage"),
                                       (21.6, -22.5, "bandage"))):
        m.cube(torso, f"wrap{i}", (-4.0, y, -2.9), (4.0, y + 0.9, 2.8), mat, rot=("z", ang), **W)
    m.cube(torso, "collar", (-4.2, 22.4, -2.95), (0.6, 23.8, -2.4), "gold", decor={"all": "usekh"})  # collar roto
    m.cube(torso, "amulet", (-0.9, 19.4, -3.5), (0.9, 21.2, -3.0), "lapis", decor={"all": "gold_band"})
    m.cube_lr(AR[0], AL[0], "arm_wrap", (5.0, 19.2, -1.8), (8.0, 20.0, 1.8), "dirty", rot=("z", 22.5), **W)
    m.cube_lr(AR[1], AL[1], "fore_wrap", (5.2, 14.6, -1.7), (7.8, 15.4, 1.6), "dirty", rot=("z", -22.5), **W)
    m.cube(AL[1], "bracelet", (-7.7, 12.4, -1.45), (-5.3, 13.6, 1.45), "gold", decor={"all": "gold_band"})
    for side, sx in (("right", 1), ("left", -1)):
        st = m.bone(f"{side}_strip", (6.5 * sx, 13, 1.2), H["arms"][side][1])
        m.cube(st, f"{side}_strip", (6.5 * sx - 0.5, 7.5, 1.0), (6.5 * sx + 0.5, 13, 1.4), "bandage",
               rot=("x", 22.5), pivot=(6.5 * sx, 13, 1.2), **W)
    m.cube_lr(H["legs"]["right"][0], H["legs"]["left"][0], "thigh_wrap", (0.6, 9.4, -1.8), (4.4, 10.2, 1.9),
              "dirty", rot=("z", -22.5), **W)
    m.cube_lr(H["legs"]["right"][1], H["legs"]["left"][1], "shin_wrap", (0.8, 4.6, -1.6), (4.2, 5.4, 2.1),
              "bandage", rot=("z", 22.5), **W)
    strip = m.bone("strip", (1.8, 13, -2.6), waist)
    m.cube(strip, "strip", (1.2, 4.5, -2.9), (2.4, 13, -2.4), "bandage", rot=("z", -22.5), pivot=(1.8, 13, -2.6), **W)
    m.cube(waist, "strip2", (-3.0, 8.5, -2.85), (-1.8, 13, -2.45), "dirty", **W)
    m.cube(waist, "loin", (-4.6, 11.6, -2.8), (4.6, 13.2, 2.8), "dirty", rot=("z", 22.5), **W)
    m.ZERO_BONES += ["strip", "head_strip", "right_strip", "left_strip"]

    def sway(a, t, s, base=0):
        a.rot("strip", t, base + 6 * s, 0, 4 * s)
        a.rot("head_strip", t, 4 * s, 0, 0)
        a.rot("right_strip", t, 8 * s, 0, 0)
        a.rot("left_strip", t, -6 * s, 0, 0)

    # encorvado, con los brazos hacia delante como las momias de siempre
    GM.human_idle(m, arm_l=(-75, 0, -4), arm_r=(-85, 0, 6),
                  extra=lambda a, t, s: (sway(a, t, s), a.rot("torso", t, 16, 0, 2 * s - 1),
                                         a.rot("h_head", t, -12 + 3 * s, 6 * s - 3, 4)))
    GM.human_walk(m, leg=18, bob=0.4, lean=16, length=1.4, arm_r=(-85, 0, 6), arm_l=(-75, 0, -4),
                  extra=lambda a, t, s: (sway(a, t, s, 12), a.rot("h_head", t, -14, 3 * s, 4)))
    a = m.anim("attack", 0.8, "once")          # agarre con las dos manos (impacto 0.35 s)
    a.rest(0)
    a.pose(0.2, {"right_arm": (-115, -20, 20), "left_arm": (-115, 20, -20), "torso": (4, 0, 0), "h_head": (-12, 0, 0)})
    a.pose(0.35, {"right_arm": (-85, 20, 0), "left_arm": (-85, -20, 0), "torso": (24, 0, 0),
                  "h_head": (-20, 0, 0)}, i="linear")
    a.rest(0.8)
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-90, 0, 10), "left_arm": (-90, 0, -10), "h_head": (-20, 0, 0)})
    GM.human_death(m)
    return m


def build_desert_priest():
    m = _base("desert_priest", {"skin": ((150, 104, 66), 8), "robe": ((232, 222, 196), 6),
                                "jackal": ((30, 26, 30), 4), "wood": ((112, 76, 44), 9)}, 2023)
    m.WOOD |= {"wood"}
    m.SHINE |= {"jackal"}

    def head(m, hd):
        m.cube(hd, "skull", (-3.1, 25.2, -2.8), (3.1, 30.8, 3.2), "jackal", decor={"north": "jackal2"})
        m.cube(hd, "brow", (-2.6, 28.6, -3.3), (2.6, 29.6, -2.6), "jackal")
        m.cube(hd, "muzzle", (-2.0, 25.2, -5.4), (2.0, 28.4, -2.7), "jackal")
        m.cube(hd, "snout", (-1.5, 25.3, -7.6), (1.5, 27.7, -5.3), "jackal")
        m.cube(hd, "bridge", (-1.2, 27.1, -7.4), (1.2, 28.3, -3.2), "jackal", rot=("x", -22.5), pivot=(0, 28.2, -3.2))
        m.cube(hd, "nose", (-0.9, 26.6, -8.5), (0.9, 27.7, -7.5), "void")
        m.cube(hd, "lower_jaw", (-1.3, 24.6, -7.0), (1.3, 25.4, -2.8), "jackal")
        m.cube(hd, "band", (-3.3, 28.0, -3.0), (3.3, 28.8, 3.4), "gold", decor={"all": "gold_band"})
        m.cube_lr(hd, hd, "ear", (0.8, 30.2, -0.4), (2.9, 34.4, 0.8), "jackal", decor={"north": "ear_in"},
                  rot=("z", -22.5), pivot=(1.8, 30.4, 0.2))
        m.cube_lr(hd, hd, "ear_tip", (1.2, 34.2, -0.2), (2.5, 36.8, 0.6), "jackal", rot=("z", -22.5),
                  pivot=(1.8, 30.4, 0.2))
        m.cube_lr(hd, hd, "lappet", (2.5, 22.2, -1.0), (3.4, 29.0, 1.2), "lapis", decor={"all": "nemes"})
        m.cube(hd, "nemes_back", (-3.0, 23.4, 2.8), (3.0, 29.6, 3.6), "lapis", decor={"all": "nemes"})

    H = AN.humanoid(m, k=0.9, mats={"chest": "skin"}, head=head)
    torso, waist, (AR, AL) = H["torso"], H["waist"], (H["arms"]["right"], H["arms"]["left"])
    # faja de lino en diagonal y collar usekh ancho sobre los hombros
    m.cube(torso, "sash", (-6.0, 19.6, -3.1), (6.0, 21.2, 2.9), "robe", decor={"all": "robe"}, rot=("z", 45),
           pivot=(0, 20.4, 0))
    m.cube(torso, "usekh", (-4.4, 21.6, -3.3), (4.4, 23.8, -2.7), "gold", decor={"all": "usekh"})
    m.cube(torso, "usekh_back", (-4.0, 22.2, 2.6), (4.0, 23.8, 3.1), "gold", decor={"all": "usekh"})
    m.cube_lr(torso, torso, "usekh_shoulder", (0.6, 23.4, -2.4), (5.4, 24.4, 2.6), "gold", decor={"all": "usekh"},
              rot=("z", -22.5), pivot=(0.6, 23.9, 0))
    m.cube(torso, "pendant", (-0.8, 19.2, -3.4), (0.8, 21.6, -2.9), "turquoise", decor={"all": "gold_band"})
    # faldellin plisado (shendyt) que se abre hacia abajo, con delantal dorado
    m.cube(waist, "kilt", (-4.2, 10.2, -2.7), (4.2, 15.0, 2.7), "robe", decor={"all": "robe"})
    m.cube_lr(waist, waist, "kilt_side", (3.6, 7.0, -2.6), (4.4, 13.8, 2.6), "robe", decor={"all": "robe"},
              rot=("z", 22.5), pivot=(4.0, 13.8, 0))
    m.cube(m.BONES["skirt_front"], "apron", (-1.8, 6.4, -3.3), (1.8, 13.6, -2.8), "gold", decor={"all": "apron"})
    m.cube(m.BONES["skirt_front"], "apron_tip", (-1.1, 5.4, -3.3), (1.1, 6.4, -2.8), "gold")
    m.cube(m.BONES["skirt_back"], "kilt_back", (-3.8, 7.2, 2.5), (3.8, 13.6, 3.1), "robe", decor={"all": "robe"})
    m.cube(waist, "belt", (-4.5, 13.6, -2.95), (4.5, 15.0, 2.95), "gold", decor={"all": "gold_band"})
    # brazaletes y tobilleras de oro
    m.cube_lr(AR[0], AL[0], "armband", (5.0, 19.0, -1.75), (8.0, 20.0, 1.75), "gold", decor={"all": "gold_band"})
    m.cube_lr(AR[1], AL[1], "bracelet", (5.4, 12.0, -1.45), (7.7, 13.4, 1.45), "gold", decor={"all": "gold_band"})
    m.cube_lr(H["legs"]["right"][1], H["legs"]["left"][1], "anklet", (1.0, 2.2, -1.45), (4.0, 3.0, 1.55), "gold")
    # baston con ankh en la mano derecha
    staff = m.bone("staff", (6.5, 10.5, -2), AR[2])
    m.cube(staff, "staff_pole", (6.05, -2, -2.45), (6.95, 24, -1.55), "wood")
    for y in (4, 12, 20):
        m.cube(staff, f"staff_ring{y}", (5.85, y, -2.65), (7.15, y + 0.6, -1.35), "gold")
    m.cube(staff, "ankh_bar", (4.6, 24, -2.5), (8.4, 24.9, -1.5), "gold")
    m.cube(staff, "ankh_stem", (6.0, 24.9, -2.5), (7.0, 26.4, -1.5), "gold")
    m.cube(staff, "ankh_loop_l", (5.0, 26.6, -2.5), (5.9, 29.2, -1.5), "gold")
    m.cube(staff, "ankh_loop_r", (7.1, 26.6, -2.5), (8.0, 29.2, -1.5), "gold")
    m.cube(staff, "ankh_loop_t", (5.7, 29.0, -2.5), (7.3, 29.9, -1.5), "gold")
    m.cube(staff, "ankh_loop_b", (5.7, 26.2, -2.5), (7.3, 26.9, -1.5), "gold")
    m.cube(staff, "ankh_gem", (6.1, 27.2, -2.7), (6.9, 28.6, -1.3), "turquoise")
    m.ZERO_BONES += ["staff"]
    GM.human_idle(m, arm_r=(-15, 0, 6))
    GM.human_walk(m, leg=20, arm=12, bob=0.4, arm_r=(-15, 0, 6))
    a = m.anim("attack", 0.7, "once")          # golpe con el baston (impacto 0.3 s)
    a.rest(0)
    a.pose(0.18, {"right_arm": (-150, 0, 10), "staff": (40, 0, 0), "torso": (-6, 12, 0)})
    a.pose(0.3, {"right_arm": (-60, 0, 0), "staff": (60, 0, 0), "torso": (12, -10, 0)}, i="linear")
    a.rest(0.7)
    a = m.anim("cast", 1.4, "once")            # cura a sus aliados alzando el ankh
    a.rest(0)
    cast = {"right_arm": (-170, 0, 5), "left_arm": (-60, 0, -40), "h_head": (-14, 0, 0), "torso": (-8, 0, 0)}
    a.pose(0.35, cast)
    a.pose(1.0, cast)
    a.rest(1.4)
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-170, 0, 5), "h_head": (-25, 0, 0)})
    GM.human_death(m)
    return m


# ===========================================================================
# ESCARABAJO GIGANTE (SPIDER)
# ===========================================================================
SC_LEGS = [f"leg_{s}{i}" for s in "rl" for i in range(3)]
SC_BONES = ["body", "head", "mandible_r", "mandible_l", "abdomen"] + SC_LEGS + [f"{n}_low" for n in SC_LEGS]


def build_giant_scarab():
    m = Model("giant_scarab", {**MATS, "shell": ((32, 60, 110), 8), "chitin": ((30, 26, 22), 6)}, seed=2024)
    m.SHINE |= {"gold", "shell"}
    egypt_decor(m)
    root = m.root
    hb = m.bone("hitbox", (0, 8, 0), root)
    m.cube(hb, "hitbox", (-7, 0, -7), (7, 12, 7), "hitbox")
    m.bone("tag_name", (0, 18, 0), root)
    body = m.bone("body", (0, 7, 0), root)
    m.cube(body, "thorax", (-4.5, 4.5, -6), (4.5, 10, 0), "chitin")
    m.cube(body, "pronotum", (-5, 8, -6.5), (5, 11, 0.5), "shell", decor={"all": "scarab_shell"})
    m.cube(body, "pronotum_top", (-3.8, 11, -5.6), (3.8, 11.8, -0.2), "shell", decor={"all": "scarab_shell"})
    abd = m.bone("abdomen", (0, 7, 0), body)
    m.cube(abd, "abdomen", (-6, 3.5, 0), (6, 11, 11), "chitin")
    m.cube(abd, "elytra", (-6.5, 7, -0.5), (6.5, 10.8, 11.5), "shell", decor={"all": "scarab_shell"})
    m.cube(abd, "elytra_mid", (-5.6, 10.8, 0.2), (5.6, 12.3, 10.8), "shell", decor={"all": "scarab_shell"})
    m.cube(abd, "elytra_top", (-4.0, 12.3, 1.2), (4.0, 13.0, 9.6), "shell", decor={"all": "scarab_shell"})
    m.cube(abd, "elytra_tail", (-5.0, 7.4, 11.0), (5.0, 10.6, 12.8), "shell", rot=("x", -22.5),
           pivot=(0, 10.6, 11.0), decor={"all": "scarab_shell"})
    m.cube(abd, "elytra_rim", (-6.75, 6.5, -0.25), (6.75, 7.25, 11.75), "gold", decor={"all": "gold_band"})
    head = m.bone("head", (0, 7, -6), body)
    m.cube(head, "head", (-3, 4.5, -10), (3, 8.5, -6), "chitin")
    m.cube(head, "clypeus", (-3.5, 7.5, -10.5), (3.5, 9, -6.5), "gold", decor={"all": "gold_band"})
    m.cube(head, "horn", (-1, 8.6, -10.2), (1, 11.4, -8.2), "gold", rot=("x", 22.5), pivot=(0, 9, -9.2))
    m.cube(head, "horn_tip", (-0.7, 11.2, -10.0), (0.7, 13.4, -8.8), "gold", rot=("x", 45), pivot=(0, 11.2, -9.4))
    for side, sx in (("r", 1), ("l", -1)):
        mb = m.bone(f"mandible_{side}", (2 * sx, 5.5, -9.5), head)
        x0, x1 = (1, 3) if sx > 0 else (-3, -1)
        m.cube(mb, f"mandible_{side}", (x0, 5, -12.5), (x1, 6.5, -9.5), "gold")
        m.cube(head, f"eye_{side}", (2.75 * sx - 0.75, 6.5, -9.5), (2.75 * sx + 0.75, 7.75, -8.5), "purple",
               decor={"all": "orb"})
    for side, sx in (("r", 1), ("l", -1)):
        for i, z in enumerate((-4.5, -1.5, 2.5)):
            n = f"leg_{side}{i}"
            leg = m.bone(n, (4.5 * sx, 7, z), body)
            x0, x1 = (4.5, 10.5) if sx > 0 else (-10.5, -4.5)
            m.cube(leg, n, (x0, 6.4, z - 0.6), (x1, 7.6, z + 0.6), "chitin")
            low = m.bone(f"{n}_low", (10.5 * sx, 7, z), leg)
            x0, x1 = (9.9, 11.1) if sx > 0 else (-11.1, -9.9)
            m.cube(low, f"{n}_low", (x0, 0, z - 0.5), (x1, 7, z + 0.5), "chitin")
    m.ZERO_BONES = list(SC_BONES)

    a = m.anim("idle", 2.0, "loop")
    for t, s in ((0, 0), (1.0, 1), (2.0, 0)):
        a.pos("body", t, 0, -0.3 * s, 0)
        a.rot("head", t, 3 * s, 4 * s - 2, 0)
        a.rot("abdomen", t, -2 * s, 0, 0)
    for t, s in ((0, 0), (0.15, 1), (0.3, 0), (2.0, 0)):
        a.rot("mandible_r", t, 0, -18 * s, 0)
        a.rot("mandible_l", t, 0, 18 * s, 0)

    a = m.anim("walk", 0.6, "loop")             # marcha en tripode
    groups = {0: ["leg_r0", "leg_l1", "leg_r2"], 1: ["leg_l0", "leg_r1", "leg_l2"]}
    for g, legs in groups.items():
        for t, s in ((0, 1), (0.3, -1), (0.6, 1)):
            s = s if g == 0 else -s
            for n in legs:
                a.rot(n, t, 0, 22 * s, 0)
                a.rot(f"{n}_low", t, 0, 0, (12 if n[4] == "r" else -12) * max(s, 0))
    for t, s in ((0, 0), (0.15, 1), (0.3, 0), (0.45, 1), (0.6, 0)):
        a.pos("body", t, 0, 0.4 * s, 0)

    a = m.anim("attack", 0.6, "once")          # mordisco (impacto 0.25 s)
    a.rest(0)
    a.pose(0.12, {"head": (-20, 0, 0), "body": {"p": (0, 1, 1.5)}, "mandible_r": (0, -35, 0), "mandible_l": (0, 35, 0)})
    a.pose(0.25, {"head": (15, 0, 0), "body": {"p": (0, -0.5, -2.5)}, "mandible_r": (0, 10, 0),
                  "mandible_l": (0, -10, 0)}, i="linear")
    a.rest(0.6)
    a = m.anim("hurt", 0.35, "once")
    a.rest(0, ["head", "abdomen"])
    a.pose(0.08, {"head": (-15, 0, 0), "abdomen": (10, 0, 0)})
    a.rest(0.35, ["head", "abdomen"])
    a = m.anim("spawn", 1.4, "once")            # sale escarbando de la arena
    a.pos("body", 0, 0, -12, 0)
    a.rot("body", 0, -30, 0, 0)
    a.pos("body", 0.9, 0, 0, 0)
    a.rot("body", 0.9, 0, 0, 0)
    a.rest(1.4)
    a = m.anim("death", 1.6, "hold")            # se da la vuelta, patas arriba
    a.rest(0)
    a.rot("root", 0, 0, 0, 0)
    a.pos("root", 0, 0, 0, 0)
    a.rot("root", 0.6, 0, 0, 180, i="linear")
    a.pos("root", 0.6, 0, 12, 0, i="linear")
    for n in SC_LEGS:
        for t, z in ((0.6, 0), (0.9, 25), (1.2, -10), (1.6, 15)):
            a.rot(f"{n}_low", t, 0, 0, z if n[4] == "r" else -z)
    return m


BUILDERS = {"old_ender": build_old_ender, "sand_warden": build_sand_warden,
            "mummy_guardian": build_mummy_guardian, "giant_scarab": build_giant_scarab,
            "desert_priest": build_desert_priest}
SHOTS = {
    "old_ender": [("rest", 0, -30), ("rest", 0, 150), ("collapse", 0.35, -60), ("gaze", 0.4, -30)],
    "sand_warden": [("rest", 0, -30), ("rest", 0, 150), ("attack", 0.18, -60), ("attack", 0.3, -60)],
    "mummy_guardian": [("idle", 0.5, -30), ("idle", 0.5, -80), ("attack", 0.35, -60), ("rest", 0, 150)],
    "giant_scarab": [("rest", 0, -30), ("rest", 0, 150), ("attack", 0.12, -70), ("walk", 0.15, -30)],
    "desert_priest": [("rest", 0, -30), ("rest", 0, -75), ("cast", 0.5, -30), ("attack", 0.3, -60)],
}


def previews(name, m):
    import render_preview as RP
    RP.G = m
    tw, th = m.pack()
    tex = m.paint(tw, th)
    anims = {a.name: a for a in m.ANIMS}
    focus, scale = {"old_ender": (26, 6.5), "giant_scarab": (8, 9.0)}.get(name, (18, 8.5))
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
    main()
