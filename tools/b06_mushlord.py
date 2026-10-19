#!/usr/bin/env python3
"""
Boss 06 - MUSHLORD y sus subditos (modelos de ModelEngine).

  mushlord          senor de las esporas: gran sombrero de hongo morado con manchas que brillan,
                    laminas debajo, filamentos colgando, cuerpo de corteza y musgo con setas repisa,
                    brazos de raiz con garras y baston con un orbe de esporas
  mush_zombie       zombi con cabeza de seta roja y hongos en los hombros (ZOMBIE)
  shroom_creeper    creeper cubierto de setas y sacos de esporas que se hinchan (CREEPER)
  living_spore      bola de esporas flotante con filamentos (SILVERFISH)
  ms_toxic_zone     charco toxico con setas que brotan (Mushlord_ToxicZone)
  ms_breath         nube toxica a ras de suelo (Mushlord_PersistentBreath)

Uso: python3 tools/b06_mushlord.py [modelo ...] [--no-preview]
"""
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
from bbmodel import Model, mul  # noqa: E402
import anatomy as AN  # noqa: E402
import generate_minions as GM  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent / "Modelos/06_Mushlord"
BLUEPRINTS = ROOT / "ModelEngine/blueprints"
PREVIEW = ROOT / "preview"

SPORE_GLOW = (150, 255, 110)

MATS = {
    "bark": ((88, 66, 46), 9), "moss": ((72, 112, 50), 10), "stem": ((206, 196, 168), 7), "cap": ((112, 46, 120), 7),
    "cap_dark": ((70, 26, 80), 6), "gill": ((220, 200, 210), 5), "glow": ((150, 255, 110), 3),
    "red_cap": ((180, 36, 36), 7), "white": ((240, 236, 226), 3), "rot": ((96, 120, 80), 8),
    "slime": ((110, 190, 80), 6), "creeper": ((90, 160, 70), 9), "myc": ((214, 206, 186), 6),
    "wood": ((100, 70, 44), 8), "stone": ((120, 120, 124), 6), "toxic": ((70, 150, 50), 6),
    "fog": ((150, 210, 120), 5), "skin": ((88, 66, 46), 9), "leather": ((90, 60, 40), 7),
    "bronze": ((196, 140, 58), 8), "hitbox": ((255, 255, 255), 0),
}


def fungal_decor(m):
    D = m.decor

    @D
    def d_spots(f):
        """Manchas que brillan sobre el sombrero."""
        rng = random.Random(f.x0 * 7 + f.y0 * 3)
        for _ in range(max(1, f.w * f.h // 14)):
            x, y = rng.randrange(f.w), rng.randrange(f.h)
            f.put(x, y, SPORE_GLOW if rng.random() < 0.6 else (240, 255, 220))
            if x + 1 < f.w:
                f.put(x + 1, y, mul(SPORE_GLOW, 0.8))

    @D
    def d_white_spots(f):
        rng = random.Random(f.x0 * 5 + f.y0)
        for _ in range(max(1, f.w * f.h // 12)):
            x, y = rng.randrange(max(1, f.w - 1)), rng.randrange(max(1, f.h - 1))
            f.rect(x, y, x + 2, y + 2, (245, 240, 230))

    @D
    def d_gills(f):
        if f.name != "down":
            return
        cx, cy = f.w / 2, f.h / 2
        for y in range(f.h):
            for x in range(f.w):
                ang = math.atan2(y - cy, x - cx)
                if int(ang * 8) % 2 == 0:
                    f.shade(x, y, 0.75)

    @D
    def d_bark(f):
        for x in range(0, f.w, 3):
            for y in range(f.h):
                f.shade(x, y, 0.75)
        rng = random.Random(f.x0 + f.y0)
        for _ in range(f.w * f.h // 10):
            f.put(rng.randrange(f.w), rng.randrange(f.h), m.MAT["moss"])
        for _ in range(f.w * f.h // 50):
            f.put(rng.randrange(f.w), rng.randrange(f.h), SPORE_GLOW)

    @D
    def d_mossy(f):
        rng = random.Random(f.x0 * 3 + f.y0)
        for y in range(f.h):
            for x in range(f.w):
                if rng.random() < 0.3:
                    f.shade(x, y, rng.choice((0.8, 1.15)))
        for x in range(f.w):
            f.put(x, 0, mul(m.MAT["moss"], 1.2))

    @D
    def d_shroom_face(f):
        w = f.w
        f.rect(1, 3, w - 1, f.h - 2, (30, 22, 20))
        for ex in (2, w - 5):
            f.rect(ex, 5, ex + 3, 7, SPORE_GLOW)
            f.put(ex + 1, 5, (240, 255, 220))
        f.rect(w // 2 - 3, f.h - 5, w // 2 + 3, f.h - 4, mul(SPORE_GLOW, 0.6))

    @D
    def d_zombie_face(f):
        w = f.w
        for ex in (2, w - 5):
            f.rect(ex, 6, ex + 3, 8, (16, 12, 10))
            f.put(ex + 1, 7, SPORE_GLOW)
        f.rect(w // 2 - 3, 11, w // 2 + 3, 12, (40, 30, 20))

    @D
    def d_creeper_face(f):
        w, h = f.w, f.h
        dark = (20, 30, 16)
        f.rect(2, 3, 6, 7, dark)
        f.rect(w - 6, 3, w - 2, 7, dark)
        f.rect(w // 2 - 2, 7, w // 2 + 2, h - 3, dark)
        f.rect(w // 2 - 4, 9, w // 2 + 4, h - 1, dark)
        f.put(3, 4, SPORE_GLOW)
        f.put(w - 5, 4, SPORE_GLOW)

    @D
    def d_creeper_skin(f):
        rng = random.Random(f.x0 + f.y0 * 13)
        for y in range(f.h):
            for x in range(f.w):
                r = rng.random()
                if r < 0.25:
                    f.shade(x, y, 0.75)
                elif r < 0.4:
                    f.shade(x, y, 1.2)

    @D
    def d_puff(f):
        rng = random.Random(f.x0 + f.y0 * 7)
        for y in range(f.h):
            for x in range(f.w):
                if rng.random() < 0.2:
                    f.shade(x, y, 1.2)
        for _ in range(max(1, f.w * f.h // 20)):
            f.put(rng.randrange(f.w), rng.randrange(f.h), SPORE_GLOW)


def _model(name, seed, atlas=256):
    m = Model(name, MATS, seed=seed, atlas_w=atlas)
    m.SHINE |= {"cap", "glow", "slime"}
    m.WOOD |= {"wood"}
    GM.add_common_decor(m)
    fungal_decor(m)
    return m


B = {"decor": {"all": "bark"}}


def shroom(m, bone, name, x, y, z, stem_h, cap_r, mat="cap", tilt=None, spots="spots"):
    """Seta pequena: tallo + sombrero en dos pisos."""
    m.cube(bone, f"{name}_stem", (x - cap_r * 0.3, y, z - cap_r * 0.3), (x + cap_r * 0.3, y + stem_h, z + cap_r * 0.3),
           "stem", rot=tilt, pivot=(x, y, z))
    m.cube(bone, f"{name}_cap", (x - cap_r, y + stem_h, z - cap_r), (x + cap_r, y + stem_h + cap_r * 0.6, z + cap_r),
           mat, rot=tilt, pivot=(x, y, z), decor={"all": spots, "down": "gills"})
    m.cube(bone, f"{name}_top", (x - cap_r * 0.6, y + stem_h + cap_r * 0.6, z - cap_r * 0.6),
           (x + cap_r * 0.6, y + stem_h + cap_r, z + cap_r * 0.6), mat, rot=tilt, pivot=(x, y, z), decor={"all": spots})


def bracket(m, bone, name, x, y, z, w, d, rot=None):
    """Seta repisa (yesquero) pegada a la corteza."""
    m.cube(bone, name, (x - w, y, z - d), (x + w, y + 0.9, z + d), "cap_dark", rot=rot, pivot=(x, y, z),
           decor={"up": "spots", "down": "gills", "all": "mossy"})


# ===========================================================================
# MUSHLORD
# ===========================================================================
def ms_head(m, hd):
    m.cube(hd, "face", (-3.0, 24.8, -3.0), (3.0, 30.0, 3.0), "stem", decor={"north": "shroom_face"})
    m.cube(hd, "gills", (-8.0, 29.6, -8.0), (8.0, 30.2, 8.0), "gill", decor={"down": "gills"})
    m.cube(hd, "cap_brim", (-8.4, 30.2, -8.4), (8.4, 31.8, 8.4), "cap", decor={"all": "spots"})
    m.cube(hd, "cap_mid", (-6.8, 31.8, -6.8), (6.8, 33.6, 6.8), "cap", decor={"all": "spots"})
    m.cube(hd, "cap_top", (-4.4, 33.6, -4.4), (4.4, 35.2, 4.4), "cap", decor={"all": "spots"})
    m.cube(hd, "cap_crown", (-2.4, 35.2, -2.4), (2.4, 36.2, 2.4), "cap", decor={"all": "spots"})
    for side, rot, frm, to, piv in (("r", ("z", 22.5), (7.8, 28.4, -7.8), (8.6, 31.0, 7.8), (8.2, 30.6, 0)),
                                     ("l", ("z", -22.5), (-8.6, 28.4, -7.8), (-7.8, 31.0, 7.8), (-8.2, 30.6, 0)),
                                     ("f", ("x", -22.5), (-7.8, 28.4, -8.6), (7.8, 31.0, -7.8), (0, 30.6, -8.2)),
                                     ("b", ("x", 22.5), (-7.8, 28.4, 7.8), (7.8, 31.0, 8.6), (0, 30.6, 8.2))):
        m.cube(hd, f"cap_droop_{side}", frm, to, "cap", rot=rot, pivot=piv, decor={"all": "spots"})
    shroom(m, hd, "mini1", -2.6, 35.0, 1.2, 1.8, 1.2, tilt=("z", 22.5))
    shroom(m, hd, "mini2", 2.4, 34.8, -1.0, 2.4, 1.4, tilt=("z", -22.5))
    shroom(m, hd, "mini3", 0.4, 35.6, 2.4, 1.4, 0.9, tilt=("x", 22.5))
    rng = random.Random(3)
    for k in range(10):
        th = 2 * math.pi * k / 10
        x, z = 7.6 * math.cos(th), 7.6 * math.sin(th)
        ln = rng.uniform(2.5, 5.0)
        m.cube(hd, f"tendril{k}", (x - 0.25, 29.6 - ln, z - 0.25), (x + 0.25, 29.6, z + 0.25), "myc")
        m.cube(hd, f"tendril{k}_tip", (x - 0.35, 29.4 - ln, z - 0.35), (x + 0.35, 30.0 - ln, z + 0.35), "glow")


def build_mushlord():
    m = _model("mushlord", 606)
    H = AN.humanoid(m, k=1.3, mats={"skin": "bark", "foot": "bark"}, head=ms_head)
    for c in m.CUBES:
        if c.mat == "bark":
            c.decor.setdefault("all", "bark")
    torso, waist = H["torso"], H["waist"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    RL, LL = H["legs"]["right"], H["legs"]["left"]
    # musgo, setas repisa y setas sobre los hombros
    m.cube(torso, "moss_chest", (-5.8, 20.0, -3.8), (5.8, 24.4, 3.6), "moss", decor={"all": "mossy"})
    m.cube(torso, "spore_heart", (-1.4, 17.2, -3.9), (1.4, 20.0, -3.3), "glow", decor={"all": "puff"})
    bracket(m, torso, "bracket_back1", 0, 21.0, 4.8, 4.0, 1.8, ("x", -22.5))
    bracket(m, torso, "bracket_back2", 1.6, 17.0, 4.4, 3.0, 1.5, ("x", -22.5))
    bracket(m, torso, "bracket_side", -5.4, 18.4, 0, 1.6, 3.0, ("z", 22.5))
    shroom(m, AR[0], "sh_r1", 7.0, 24.0, -0.8, 2.4, 1.8)
    shroom(m, AR[0], "sh_r2", 8.2, 23.4, 1.6, 1.6, 1.2, tilt=("z", -22.5))
    bracket(m, AL[0], "bracket_l", -8.8, 21.8, 0, 2.2, 3.2, ("z", 22.5))
    shroom(m, AL[0], "sh_l1", -7.0, 24.2, 1.0, 1.8, 1.3, tilt=("x", 22.5))
    # cintura de raices y faldon de musgo con filamentos
    m.cube(waist, "root_belt", (-5.0, 12.8, -3.4), (5.0, 15.4, 3.2), "bark", **B)
    m.cube(m.BONES["skirt_front"], "moss_f", (-4.0, 6.4, -3.8), (4.0, 13.4, -3.0), "moss", decor={"all": "mossy"})
    m.cube(m.BONES["skirt_back"], "moss_b", (-4.2, 6.4, 3.0), (4.2, 13.4, 3.8), "moss", decor={"all": "mossy"})
    m.cube_lr(waist, waist, "moss_s", (4.6, 7.2, -3.0), (5.4, 13.4, 3.0), "moss", rot=("z", 22.5), pivot=(5.0, 13.4, 0),
              decor={"all": "mossy"})
    # raices en los pies
    for sx, (leg, low) in ((1, RL), (-1, LL)):
        for k, (ang, dz) in enumerate(((22.5, -2.6), (-22.5, -2.6), (0, 2.2))):
            x = 2.5 * sx
            m.cube(low, f"root_{sx}_{k}", (x - 0.6, 0, dz - 0.6), (x + 0.6, 2.8, dz + 0.6), "bark",
                   rot=("z", ang * sx) if ang else ("x", 22.5), pivot=(x, 2.8, dz), **B)
    # garras de raiz
    for side, sx, arm in (("r", 1, AR), ("l", -1, AL)):
        for k, z in enumerate((-1.2, 0.0, 1.2)):
            x = 6.5 * sx
            m.cube(arm[2], f"claw_{side}{k}", (x - 0.4, 5.0, z - 0.4), (x + 0.4, 8.6, z + 0.4), "bark",
                   rot=("x", -22.5), pivot=(x, 8.6, z))
    # baston de corteza con seta y orbe de esporas
    st = m.bone("staff", (6.5, 10.0, 0), AR[2])
    m.cube(st, "haft", (6.05, 9.5, -24.0), (6.95, 10.5, 6.0), "wood", **B)
    m.cube(st, "knot", (5.8, 9.2, -6.0), (7.2, 10.8, -4.0), "bark")
    m.cube(st, "orb", (5.2, 8.2, -28.0), (7.8, 10.8, -25.4), "glow", decor={"all": "puff"})
    shroom(m, st, "staff_cap", 6.5, 10.6, -26.7, 0.6, 2.6)
    for k, (ang, ln) in enumerate(((22.5, 4.0), (-22.5, 3.4))):
        m.cube(st, f"prong{k}", (6.1, 10.0, -26.0), (6.9, 10.8, -26.0 + ln), "wood", rot=("y", ang), pivot=(6.5, 10.4, -24))
    m.ZERO_BONES += ["staff"]

    GM.human_idle(m, arm_r=(-25, 0, 10), arm_l=(-10, 0, -12),
                  extra=lambda a, t, s: (a.rot("staff", t, 55, 0, 0), a.rot("torso", t, 6 + 2 * s, 0, 0),
                                         a.rot("h_head", t, 0, 4 * s - 2, 3 * s)))
    GM.human_walk(m, leg=18, arm=10, bob=1.0, lean=8, length=1.5, arm_r=(-25, 0, 10),
                  extra=lambda a, t, s: a.rot("staff", t, 55, 0, 0))

    def anim(name, length, keys):
        a = m.anim(name, length, "once")
        a.rest(0)
        for t, pose, lin in keys:
            a.pose(t, pose, i="linear" if lin else "catmullrom")
        a.rest(length)
        return a

    anim("attack", 0.7, [(0.15, {"right_arm": (-150, 0, 20), "torso": (-6, 15, 0), "staff": (55, 0, 0)}, False),
                         (0.3, {"right_arm": (-50, 0, -10), "torso": (14, -10, 0), "staff": (0, 0, 0)}, True)])
    anim("swipe", 0.7, [(0.1, {"left_arm": (-90, -60, -20), "torso": (0, -35, 0)}, False),
                        (0.2, {"left_arm": (-90, 50, 0), "torso": (5, 30, 0)}, True)])
    cast = {"right_arm": (-150, 0, 5), "staff": (60, 0, 0), "h_head": (-15, 0, 0), "torso": (-8, 0, 0)}
    anim("cast", 1.0, [(0.3, cast, False), (0.45, {**cast, "right_arm": (-110, 0, 0)}, True),
                       (0.7, {**cast, "right_arm": (-110, 0, 0)}, False)])
    anim("burst", 0.9, [(0.08, {"right_arm": (-160, 0, 20), "left_arm": (-160, 0, -20), "staff": (60, 0, 0)}, False),
                        (0.18, {**GM.KNEEL, "right_arm": (-50, 0, 10), "left_arm": (-50, 0, -10), "torso": (30, 0, 0),
                                "staff": (-20, 0, 0)}, True),
                        (0.5, {**GM.KNEEL, "right_arm": (-50, 0, 10), "left_arm": (-50, 0, -10), "torso": (28, 0, 0),
                               "staff": (-20, 0, 0)}, False)])
    anim("cloud", 1.0, [(0.25, {"torso": (-15, 0, 0), "h_head": (-25, 0, 0), "right_arm": (-30, 0, 40),
                                "left_arm": (-30, 0, -40)}, False),
                        (0.45, {"torso": (20, 0, 0), "h_head": (15, 0, 0), "right_arm": (-70, 0, 20),
                                "left_arm": (-70, 0, -20)}, True)])
    anim("nova", 1.3, [(0.4, {"right_arm": (-70, -40, 0), "left_arm": (-70, 40, 0), "torso": (20, 0, 0),
                              "h_head": (20, 0, 0)}, False),
                       (0.5, {"right_arm": (-40, 0, 80), "left_arm": (-40, 0, -80), "torso": (-18, 0, 0),
                              "h_head": (-30, 0, 0)}, True),
                       (0.9, {"right_arm": (-40, 0, 75), "left_arm": (-40, 0, -75), "torso": (-15, 0, 0)}, False)])
    anim("surge", 1.2, [(0.3, {"right_arm": (-100, 0, 20), "left_arm": (-100, 0, -20), "torso": (15, 0, 0)}, False),
                        (0.4, {"right_arm": (-40, 0, 30), "left_arm": (-40, 0, -30), "torso": (-10, 0, 0)}, True),
                        (0.5, {**GM.KNEEL, "right_arm": (-60, 0, 0), "left_arm": (-60, 0, 0), "torso": (35, 0, 0)}, True),
                        (0.8, {**GM.KNEEL, "right_arm": (-60, 0, 0), "left_arm": (-60, 0, 0), "torso": (33, 0, 0)}, False)])
    sent = {"right_arm": (-175, 0, 5), "staff": (70, 0, 0), "left_arm": (-100, 0, -30), "h_head": (-20, 0, 0)}
    anim("sentence", 1.6, [(0.3, sent, False), (1.1, {**sent, "torso": (-6, 0, 0)}, False),
                           (1.2, {"right_arm": (-90, 0, 0), "staff": (10, 0, 0), "torso": (10, 0, 0)}, True)])
    charge = {"right_arm": (-170, 0, 30), "left_arm": (-170, 0, -30), "staff": (70, 0, 0), "torso": (-16, 0, 0),
              "h_head": (-30, 0, 0)}
    keys = [(0.4, charge, False)] + [(0.6 + 0.2 * k, {**charge, "torso": (-16 + (3 if k % 2 else -3), 0, 0)}, False)
                                      for k in range(4)]
    keys += [(1.5, {**GM.KNEEL, "right_arm": (-50, 0, 10), "left_arm": (-50, 0, -10), "staff": (-20, 0, 0),
                    "torso": (35, 0, 0)}, True),
             (1.9, {**GM.KNEEL, "right_arm": (-50, 0, 10), "left_arm": (-50, 0, -10), "staff": (-20, 0, 0),
                    "torso": (33, 0, 0)}, False)]
    anim("apocalypse", 2.3, keys)
    curl = {**GM.KNEEL, "torso": (45, 0, 0), "h_head": (30, 0, 0), "right_arm": (-60, -40, 20), "left_arm": (-60, 40, -20)}
    anim("cocoon", 1.2, [(0.3, curl, False), (0.55, curl, False),
                         (0.65, {"body": {"p": (0, 0, 0)}, "right_leg": (0, 0, 0), "right_lower_leg": (0, 0, 0),
                                 "left_leg": (0, 0, 0), "left_lower_leg": (0, 0, 0), "torso": (-20, 0, 0),
                                 "h_head": (-30, 0, 0), "right_arm": (-30, 0, 70), "left_arm": (-30, 0, -70)}, True),
                         (0.9, {"torso": (-18, 0, 0), "right_arm": (-30, 0, 65), "left_arm": (-30, 0, -65)}, False)])
    anim("summon", 1.4, [(0.4, {"right_arm": (-170, 0, 10), "staff": (70, 0, 0), "left_arm": (-30, 0, -60),
                                "h_head": (-25, 0, 0)}, False),
                         (1.0, {"right_arm": (-170, 0, 10), "staff": (70, 0, 0), "left_arm": (-30, 0, -60)}, False)])
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-170, 0, 10), "staff": (70, 0, 0), "h_head": (-20, 0, 0)}, length=2.0)
    GM.human_death(m, 2.4)
    m.scale(1.5)
    return m


# ===========================================================================
# ZOMBI HONGO (ZOMBIE)
# ===========================================================================
def build_mush_zombie():
    m = _model("mush_zombie", 6061)

    def head(m, hd):
        AN.default_head(m, hd, face="zombie_face", mat="rot")
        m.cube(hd, "cap", (-4.6, 30.6, -4.6), (4.6, 32.8, 4.6), "red_cap", decor={"all": "white_spots", "down": "gills"})
        m.cube(hd, "cap_top", (-3.2, 32.8, -3.2), (3.2, 34.0, 3.2), "red_cap", decor={"all": "white_spots"})
        m.cube_lr(hd, hd, "cap_droop", (4.2, 29.4, -4.4), (4.9, 31.2, 4.4), "red_cap", rot=("z", 22.5),
                  pivot=(4.5, 31, 0), decor={"all": "white_spots"})

    H = AN.humanoid(m, k=0.95, mats={"skin": "rot", "chest": "leather", "belly": "rot", "thigh": "leather",
                                     "shin": "leather", "foot": "leather"}, head=head)
    torso = H["torso"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    m.cube(torso, "moss", (-4.4, 19.0, -3.0), (4.4, 23.4, 2.8), "moss", decor={"all": "mossy"})
    shroom(m, AL[0], "shoulder1", -7.0, 23.6, 0.2, 1.4, 1.2, mat="red_cap", spots="white_spots")
    shroom(m, AL[0], "shoulder2", -8.0, 23.0, -1.6, 0.9, 0.8, mat="red_cap", tilt=("z", 22.5), spots="white_spots")
    shroom(m, torso, "back1", 1.2, 21.0, 3.0, 1.2, 1.0, mat="red_cap", tilt=("x", -22.5), spots="white_spots")
    sw = m.bone("sword", (6.5, 10.0, 0), AR[2])
    m.cube(sw, "grip", (6.1, 9.5, -2.4), (6.9, 10.5, 2.4), "leather")
    m.cube(sw, "blade", (6.2, 9.0, -14.0), (6.8, 11.0, -2.4), "stone", decor={"all": "blade"})
    m.ZERO_BONES += ["sword"]
    GM.human_idle(m, arm_r=(-60, 0, 8), arm_l=(-75, 0, -6),
                  extra=lambda a, t, s: (a.rot("sword", t, 40, 0, 0), a.rot("torso", t, 10, 0, 0)))
    GM.human_walk(m, leg=18, arm=8, lean=10, length=1.3, arm_r=(-65, 0, 8), arm_l=(-80, 0, -6),
                  extra=lambda a, t, s: a.rot("sword", t, 40, 0, 0))
    a = m.anim("attack", 0.7, "once")
    a.rest(0)
    a.pose(0.15, {"right_arm": (-150, 0, 20), "sword": (40, 0, 0), "torso": (-5, 15, 0)})
    a.pose(0.3, {"right_arm": (-50, 0, -15), "sword": (0, 0, 0), "torso": (15, -15, 0)}, i="linear")
    a.rest(0.7)
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-80, 0, 10), "h_head": (-15, 0, 0)})
    GM.human_death(m)
    return m


# ===========================================================================
# CREEPER ESPORA (CREEPER)
# ===========================================================================
SC_BONES = ["body", "head", "leg_fr", "leg_fl", "leg_br", "leg_bl", "sacs"]


def build_shroom_creeper():
    m = _model("shroom_creeper", 6062)
    root = m.root
    hb = m.bone("hitbox", (0, 13, 0), root)
    m.cube(hb, "hitbox", (-4.5, 0, -4.5), (4.5, 26, 4.5), "hitbox")
    m.bone("tag_name", (0, 32, 0), root)
    body = m.bone("body", (0, 6, 0), root)
    m.cube(body, "torso", (-4, 6, -2), (4, 18, 2), "creeper", decor={"all": "creeper_skin"})
    for name, x, z in (("leg_fr", 2, -4), ("leg_fl", -2, -4), ("leg_br", 2, 4), ("leg_bl", -2, 4)):
        lg = m.bone(name, (x, 6, z / 2), root)
        m.cube(lg, name, (x - 2, 0, z / 2 - 2 + (-1 if z < 0 else 1) * 0.0), (x + 2, 6, z / 2 + 2), "creeper",
               decor={"all": "creeper_skin"})
    hd = m.bone("head", (0, 18, 0), body)
    m.cube(hd, "head", (-4, 18, -4), (4, 26, 4), "creeper", decor={"north": "creeper_face", "all": "creeper_skin"})
    shroom(m, hd, "cap_big", 1.4, 26.0, 0.6, 1.4, 2.8, mat="red_cap", spots="white_spots")
    shroom(m, hd, "cap_small", -2.4, 26.0, -1.4, 0.8, 1.6, mat="red_cap", tilt=("z", 22.5), spots="white_spots")
    shroom(m, body, "cap_side", 4.0, 12.0, 0.4, 0.8, 1.4, mat="red_cap", tilt=("z", -45), spots="white_spots")
    sacs = m.bone("sacs", (0, 12, -2), body)
    for k, (x, y) in enumerate(((-2.0, 14.0), (1.8, 10.6), (-1.2, 8.4))):
        m.cube(sacs, f"sac{k}", (x - 1.3, y - 1.3, -3.2), (x + 1.3, y + 1.3, -1.8), "glow", decor={"all": "puff"})
    m.ZERO_BONES = list(SC_BONES)
    a = m.anim("idle", 2.0, "loop")
    for t, s in ((0, 0), (1.0, 1), (2.0, 0)):
        a.rot("head", t, 0, 6 * s - 3, 0)
        a.scl("sacs", t, 1 + 0.15 * s)
    a = m.anim("walk", 0.8, "loop")
    for t, s in ((0, 1), (0.4, -1), (0.8, 1)):
        a.rot("leg_fr", t, 30 * s, 0, 0)
        a.rot("leg_bl", t, 30 * s, 0, 0)
        a.rot("leg_fl", t, -30 * s, 0, 0)
        a.rot("leg_br", t, -30 * s, 0, 0)
    a = m.anim("prime", 0.9, "once")            # se hincha antes de reventar (TSC_PrimeExplode)
    for k in range(10):
        t = 0.09 * k
        s = 1 + 0.05 * k + (0.06 if k % 2 else 0)
        a.scl("body", t, s, 1 + 0.03 * k, s)
        a.scl("sacs", t, 1 + 0.04 * k)
    a = m.anim("hurt", 0.35, "once")
    a.rest(0, ["head", "body"])
    a.pose(0.08, {"head": (-15, 0, 0), "body": (8, 0, 0)})
    a.rest(0.35, ["head", "body"])
    a = m.anim("spawn", 1.0, "once")
    a.pos("body", 0, 0, -14, 0)
    for n in ("leg_fr", "leg_fl", "leg_br", "leg_bl"):
        a.pos(n, 0, 0, -14, 0)
        a.pos(n, 0.7, 0, 0, 0)
    a.pos("body", 0.7, 0, 0, 0)
    a.rest(1.0)
    a = m.anim("death", 0.6, "hold")
    a.scl("body", 0, 1)
    a.scl("body", 0.3, 1.5)
    a.scl("body", 0.6, 0.05)
    return m


# ===========================================================================
# ESPORA VIVIENTE (SILVERFISH)
# ===========================================================================
def build_living_spore():
    m = _model("living_spore", 6063, atlas=128)
    root = m.root
    hb = m.bone("hitbox", (0, 4, 0), root)
    m.cube(hb, "hitbox", (-3, 0, -3), (3, 6, 3), "hitbox")
    m.bone("tag_name", (0, 12, 0), root)
    body = m.bone("body", (0, 6, 0), root)
    m.cube(body, "core", (-3.2, 3.6, -3.2), (3.2, 9.6, 3.2), "slime", decor={"all": "puff"})
    m.cube(body, "core_w", (-4.0, 4.6, -2.4), (4.0, 8.6, 2.4), "slime", decor={"all": "puff"})
    m.cube(body, "core_d", (-2.4, 4.6, -4.0), (2.4, 8.6, 4.0), "slime", decor={"all": "puff"})
    m.cube(body, "core_h", (-2.4, 2.8, -2.4), (2.4, 10.4, 2.4), "slime", decor={"all": "puff"})
    for k, (x, z) in enumerate(((-1.2, -4.1), (1.4, -4.1))):
        m.cube(body, f"eye{k}", (x - 0.6, 6.6, z - 0.2), (x + 0.6, 7.8, z + 0.2), "white")
    m.cube(body, "mouth", (-1.0, 5.2, -4.2), (1.0, 5.8, -3.9), "cap_dark")
    tend = m.bone("tendrils", (0, 4, 0), body)
    for k in range(4):
        th = 2 * math.pi * (k + 0.5) / 4
        x, z = 2.2 * math.cos(th), 2.2 * math.sin(th)
        m.cube(tend, f"t{k}", (x - 0.3, 0.4, z - 0.3), (x + 0.3, 3.6, z + 0.3), "myc")
        m.cube(tend, f"t{k}_tip", (x - 0.45, 0, z - 0.45), (x + 0.45, 0.6, z + 0.45), "glow")
    shroom(m, body, "top", 0, 10.2, 0, 0.6, 1.4, mat="cap")
    m.ZERO_BONES = ["body", "tendrils"]
    a = m.anim("idle", 1.4, "loop")
    for t, s in ((0, 0), (0.7, 1), (1.4, 0)):
        a.pos("body", t, 0, 1.2 * s, 0)
        a.scl("body", t, 1 + 0.06 * s, 1 - 0.04 * s, 1 + 0.06 * s)
        a.rot("tendrils", t, 0, 30 * s, 0)
    a = m.anim("walk", 0.6, "loop")
    for t, s in ((0, 0), (0.3, 1), (0.6, 0)):
        a.pos("body", t, 0, 2.0 * s, 0)
        a.scl("body", t, 1 - 0.1 * s + 0.05, 1 + 0.1 * s, 1 - 0.1 * s + 0.05)
    a = m.anim("attack", 0.6, "once")           # bocanada de esporas
    a.scl("body", 0, 1)
    a.scl("body", 0.2, 1.3, 0.8, 1.3)
    a.scl("body", 0.35, 0.9)
    a.scl("body", 0.6, 1)
    a = m.anim("hurt", 0.3, "once")
    a.scl("body", 0, 1)
    a.scl("body", 0.08, 0.8, 1.2, 0.8)
    a.scl("body", 0.3, 1)
    a = m.anim("spawn", 0.8, "once")
    a.scl("body", 0, 0.1)
    a.scl("body", 0.5, 1.2)
    a.scl("body", 0.8, 1)
    a = m.anim("death", 0.5, "hold")
    a.scl("body", 0, 1)
    a.scl("body", 0.2, 1.6)
    a.scl("body", 0.5, 0.05)
    return m


# ===========================================================================
# CHARCO TOXICO y NUBE (armor stands)
# ===========================================================================
def build_toxic_zone():
    m = _model("ms_toxic_zone", 6064)
    root = m.root
    pool = m.bone("pool", (0, 0, 0), root)
    for k, (x, z, r) in enumerate(((0, 0, 40), (24, 14, 22), (-26, 10, 20), (10, -28, 20), (-14, -24, 16))):
        m.cube(pool, f"blob{k}", (x - r, 0.05 + k * 0.02, z - r * 0.8), (x + r, 0.3 + k * 0.02, z + r * 0.8),
               "toxic" if k % 2 == 0 else "slime")
    m.cube(pool, "glow", (-14, 0.35, -10), (14, 0.45, 10), "glow")
    a = m.anim("idle", 2.0, "loop")
    rng = random.Random(4)
    for k in range(5):
        b = m.bone(f"shroom{k}", (0, 0, 0), root)
        x, z = rng.uniform(-34, 34), rng.uniform(-26, 26)
        shroom(m, b, f"s{k}", x, 0.2, z, rng.uniform(5.0, 9.0), rng.uniform(3.4, 5.0),
               mat="cap" if k % 2 else "red_cap", spots="spots" if k % 2 else "white_spots")
        for t, s in ((0, 1), (1.0, 1.08), (2.0, 1)):
            a.scl(f"shroom{k}", t, s)
    for t, s in ((0, 1), (1.0, 1.04), (2.0, 1)):
        a.scl("pool", t, s, 1, s)
    a = m.anim("spawn", 0.8, "once")
    a.scl("pool", 0, 0.1, 1, 0.1)
    a.scl("pool", 0.5, 1.06, 1, 1.06)
    a.scl("pool", 0.8, 1, 1, 1)
    for k in range(5):
        a.scl(f"shroom{k}", 0, 0.05)
        a.scl(f"shroom{k}", 0.3 + 0.08 * k, 1.15)
        a.scl(f"shroom{k}", 0.8, 1)
    return m


def build_breath():
    m = _model("ms_breath", 6065, atlas=128)
    root = m.root
    a = m.anim("idle", 3.0, "loop")
    rng = random.Random(8)
    for k in range(7):
        th = 2 * math.pi * k / 7
        r = 0 if k == 0 else 34
        x, z = r * math.cos(th), r * math.sin(th)
        b = m.bone(f"puff{k}", (x, 4, z), root)
        s = rng.uniform(10, 14)
        m.cube(b, f"p{k}", (x - s, 0, z - s), (x + s, s * 0.6, z + s), "fog", decor={"all": "puff"})
        m.cube(b, f"p{k}b", (x - s * 0.6, s * 0.6, z - s * 0.6), (x + s * 0.6, s, z + s * 0.6), "fog", decor={"all": "puff"})
        off = k * 0.4
        for t in (0, 1.0, 2.0, 3.0):
            ph = math.sin(2 * math.pi * (t + off) / 3.0)
            a.scl(f"puff{k}", t, 1 + 0.12 * ph, 1 + 0.2 * ph, 1 + 0.12 * ph)
            a.pos(f"puff{k}", t, 0, 1.5 * ph, 0)
    a = m.anim("spawn", 1.0, "once")
    for k in range(7):
        a.scl(f"puff{k}", 0, 0.05)
        a.scl(f"puff{k}", 0.6 + 0.05 * k, 1.1)
        a.scl(f"puff{k}", 1.0, 1)
    return m


BUILDERS = {"mushlord": build_mushlord, "mush_zombie": build_mush_zombie, "shroom_creeper": build_shroom_creeper,
            "living_spore": build_living_spore, "ms_toxic_zone": build_toxic_zone, "ms_breath": build_breath}
SHOTS = {
    "mushlord": [("rest", 0, -30), ("rest", 0, 150), ("burst", 0.18, -50), ("apocalypse", 0.8, -30)],
    "mush_zombie": [("idle", 0.5, -30), ("rest", 0, 150), ("attack", 0.15, -60), ("attack", 0.3, -60)],
    "shroom_creeper": [("idle", 0.5, -30), ("rest", 0, 150), ("walk", 0.2, -80), ("prime", 0.8, -30)],
    "living_spore": [("idle", 0.7, -30), ("idle", 0.7, 150), ("attack", 0.2, -30), ("walk", 0.3, -80)],
    "ms_toxic_zone": [("idle", 0.2, -30), ("idle", 1.0, -30), ("spawn", 0.3, -30), ("idle", 1.6, 150)],
    "ms_breath": [("idle", 0.2, -30), ("idle", 1.2, -30), ("spawn", 0.4, -30), ("idle", 2.2, 150)],
}
VIEW = {"mushlord": (34, 4.4), "shroom_creeper": (13, 11.0), "living_spore": (6, 22.0), "ms_toxic_zone": (0, 3.0),
        "ms_breath": (8, 3.0)}


def previews(name, m):
    import render_preview as RP
    RP.G = m
    tw, th = m.pack()
    tex = m.paint(tw, th)
    anims = {a.name: a for a in m.ANIMS}
    focus, scale = VIEW.get(name, (18, 8.5))
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
        out = BLUEPRINTS / name / f"{name}.bbmodel"
        out.parent.mkdir(parents=True, exist_ok=True)
        m.build(out)
        print(f"OK {name}: cubos={len(m.CUBES)} huesos={len(m.BONES)} anims={[a.name for a in m.ANIMS]}")
        if "--no-preview" not in sys.argv:
            previews(name, m)


if __name__ == "__main__":
    main()
