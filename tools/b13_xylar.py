#!/usr/bin/env python3
"""
Boss 13 - XYLAR y sus subditos (modelos de ModelEngine).

  xylar          Senor Galactico: armadura de metal estelar negra y magenta con vetas de energia,
                 yelmo con visor brillante y corona de cristales, agujero negro en el pecho,
                 hombreras con fragmentos de estrellas en orbita, capa de cielo estrellado y
                 espadon de energia
  xy_soldier     soldado estelar: armadura con casco de cupula, visor y espada de energia (ZOMBIE)
  xy_knight      caballero del vacio: armadura negra con cuernos, escudo con estrella y espadon (WITHER_SKELETON)
  xy_shard       fragmento estelar: racimo de cristales con nucleo y alas de cristal (VEX)
  xy_well        pozo gravitatorio: disco negro con aro de acrecion que gira (ARMOR_STAND del pozo)

Uso: python3 tools/b13_xylar.py [modelo ...] [--no-preview]
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from bbmodel import Model  # noqa: E402
import anatomy as AN  # noqa: E402
import generate_minions as GM  # noqa: E402
import fxlib as FX  # noqa: E402
import b05_ragnarok as RG  # noqa: E402
import b10_kronos as KR  # noqa: E402
import b11_azathoth as AZ  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent / "Modelos/13_Xylar"
BLUEPRINTS = ROOT / "ModelEngine/blueprints"
PREVIEW = ROOT / "preview"

GLOW = (255, 90, 255)
MATS = {
    "armor": ((36, 26, 50), 5), "armor_hi": ((80, 60, 110), 6), "trim": ((230, 80, 220), 5), "glow": (GLOW, 3),
    "star": ((255, 240, 220), 2), "void": ((10, 6, 18), 3), "cape": ((40, 20, 70), 5), "cape_in": ((120, 30, 110), 5),
    "silver": ((190, 190, 210), 5), "ice": ((240, 150, 255), 5), "ice_dark": ((150, 60, 200), 6), "skin": ((60, 40, 70), 5),
    "energy": ((255, 170, 255), 2), "steel": ((120, 120, 140), 6), "hitbox": ((255, 255, 255), 0),
}


def star_decor(m):
    D = m.decor

    @D
    def d_star_plate(f):
        """Placa de metal estelar: degradado, filo magenta y vetas de energia."""
        if f.name in ("up", "down"):
            return
        for y in range(f.h):
            k = 1.3 - 0.6 * y / max(1, f.h - 1)
            for x in range(f.w):
                f.shade(x, y, k)
        for x in range(f.w):
            f.put(x, 0, (240, 120, 230))
        if f.w > 5:
            for y in range(1, f.h - 1):
                if (y // 2) % 2 == 0:
                    f.put(f.w // 2, y, (255, 90, 255))

    @D
    def d_visor(f):
        if f.name != "north":
            return
        w = f.w
        f.rect(1, 6, w - 1, 8, (10, 6, 18))
        f.rect(2, 6, w - 2, 7, GLOW)
        f.rect(w // 2 - 1, 8, w // 2 + 1, 12, (10, 6, 18))

    @D
    def d_dome_visor(f):
        if f.name != "north":
            return
        w, h = f.w, f.h
        f.rect(1, 3, w - 1, h - 3, (30, 10, 40))
        f.rect(2, 4, w - 2, 6, (255, 140, 255))

    @D
    def d_star_emblem(f):
        if f.name not in ("east", "west"):
            return
        w, h = f.w, f.h
        cx, cy = w // 2, h // 2
        for i in range(-3, 4):
            f.put(cx + i, cy, GLOW)
            f.put(cx, cy + i, GLOW)
        for i in (-1, 1):
            f.put(cx + i, cy + i, (255, 240, 220))
            f.put(cx + i, cy - i, (255, 240, 220))

    @D
    def d_crystal(f):
        for y in range(f.h):
            f.put(0, y, (255, 230, 255))


def _model(name, seed, atlas=256):
    m = Model(name, MATS, seed=seed, atlas_w=atlas)
    m.SHINE |= {"trim", "glow", "silver", "ice", "energy", "armor_hi"}
    GM.add_common_decor(m)
    RG.norse_decor(m)
    AZ.void_decor(m)
    star_decor(m)
    return m


SP = {"decor": {"all": "star_plate"}}
CS = {"decor": {"all": "cosmic"}}


def energy_blade(m, bone, name, x, y, z0, length, w=1.2):
    """Hoja de energia a lo largo de -Z con nucleo brillante y punta."""
    m.cube(bone, name, (x - 0.45, y - w, z0 - length), (x + 0.45, y + w, z0), "energy")
    m.cube(bone, name + "_core", (x - 0.25, y - w * 0.4, z0 - length + 0.5), (x + 0.25, y + w * 0.4, z0 - 0.5), "star")
    m.cube(bone, name + "_tip", (x - 0.4, y - w * 0.7, z0 - length - 1.6), (x + 0.4, y + w * 0.7, z0 - length + 0.2), "energy",
           rot=("x", 45), pivot=(x, y, z0 - length))


# ===========================================================================
# XYLAR
# ===========================================================================
def xylar_head(m, hd):
    m.cube(hd, "helm", (-3.4, 24.8, -3.6), (3.4, 31.6, 3.4), "armor", decor={"north": "visor", "all": "star_plate"})
    m.cube(hd, "helm45", (-2.8, 25.2, -3.0), (2.8, 31.8, 3.0), "armor_hi", rot=("y", 45), pivot=(0, 28, 0), **SP)
    m.cube(hd, "jaw_guard", (-2.8, 24.0, -4.2), (2.8, 26.4, -2.6), "armor", rot=("x", -22.5), pivot=(0, 26, -3.4), **SP)
    m.cube(hd, "crest", (-0.6, 30.4, -4.0), (0.6, 33.2, 3.6), "trim")
    m.cube_lr(hd, hd, "cheek_fin", (3.0, 26.0, -2.4), (4.0, 31.0, 2.4), "trim", rot=("y", 22.5), pivot=(3.5, 28, 0))
    spec = [(-2.6, 0, 4.0, 0.6, ("z", 45)), (-1.4, 0, 5.4, 0.7, ("z", 22.5)), (0, 0, 7.0, 0.8, None),
            (1.4, 0, 5.4, 0.7, ("z", -22.5)), (2.6, 0, 4.0, 0.6, ("z", -45))]
    RG.crystals(m, hd, (0, 31.4, 0.8), spec, "crown")


def build_xylar():
    m = _model("xylar", 1313, atlas=512)
    H = AN.humanoid(m, k=1.25, mats={"skin": "armor", "chest": "armor", "belly": "armor_hi", "arm": "armor",
                                      "hand": "armor_hi", "thigh": "armor", "shin": "armor", "foot": "armor_hi",
                                      "pelvis": "armor"}, head=xylar_head)
    for c in m.CUBES:
        if c.mat in ("armor", "armor_hi") and not c.decor:
            c.decor["all"] = "star_plate"
    torso, waist = H["torso"], H["waist"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    RL, LL = H["legs"]["right"], H["legs"]["left"]
    # agujero negro en el pecho con aro de energia
    core = m.bone("core", (0, 21.0, -4.2), torso)
    m.cube(core, "core", (-1.6, 19.4, -4.9), (1.6, 22.6, -4.1), "void")
    KR.ring(m, core, "core_ring", 0, 21.0, -4.6, -4.0, 2.6, "glow", n=8, t=0.6)
    m.cube(torso, "chest_v", (-4.6, 19.0, -4.2), (4.6, 24.0, -3.4), "armor_hi", **SP)
    m.cube(torso, "abs_trim", (-3.6, 15.4, -3.4), (3.6, 16.4, -2.8), "trim")
    # hombreras en capas con fragmentos de estrellas en orbita
    for side, sx, arm in (("r", 1, AR), ("l", -1, AL)):
        x0, x1 = (4.0, 10.6) if sx > 0 else (-10.6, -4.0)
        m.cube(arm[0], f"pauldron_{side}", (x0, 22.2, -3.8), (x1, 25.6, 3.8), "armor", rot=("z", -22.5 * sx),
               pivot=(7.3 * sx, 24, 0), **SP)
        m.cube(arm[0], f"pauldron2_{side}", (x0 + 0.6 * sx, 20.0, -3.4), (x1 + 0.6 * sx, 22.6, 3.4), "armor_hi",
               rot=("z", -22.5 * sx), pivot=(7.6 * sx, 21, 0), **SP)
        m.cube(arm[0], f"pauldron_trim_{side}", (x0, 25.4, -3.9), (x1, 26.0, 3.9), "trim", rot=("z", -22.5 * sx),
               pivot=(7.3 * sx, 24, 0))
        RG.crystals(m, arm[0], (8.0 * sx, 25.4, 0), [(0, -1.2, 3.0, 0.5, ("z", -22.5 * sx)), (0, 1.2, 2.2, 0.4, ("z", -45 * sx))],
                    f"pc_{side}")
        orb = m.bone(f"orbit_{side}", (7.5 * sx, 27.0, 0), arm[0])
        for k in range(3):
            a = 2 * math.pi * k / 3
            x, z = 7.5 * sx + 4.6 * math.cos(a), 4.6 * math.sin(a)
            m.cube(orb, f"orbit_{side}{k}", (x - 0.7, 26.3, z - 0.7), (x + 0.7, 27.7, z + 0.7), "star" if k else "glow",
                   rot=("y", 45), pivot=(x, 27, z))
        m.cube(arm[1], f"gauntlet_{side}", (4.6 * sx if sx > 0 else -8.4, 11.6, -2.2), (8.4 if sx > 0 else -4.6, 15.4, 2.2),
               "armor_hi", **SP)
        m.cube(arm[1], f"gauntlet_fin_{side}", (8.0 * sx - 0.3, 11.6, -0.4), (8.0 * sx + 0.3, 16.4, 0.4), "trim",
               rot=("z", -22.5 * sx), pivot=(8 * sx, 14, 0))
    # faldon, grebas y rodilleras
    m.cube(m.BONES["skirt_front"], "tasset", (-3.4, 6.4, -3.6), (3.4, 13.4, -3.0), "armor_hi", **SP)
    m.cube(m.BONES["skirt_back"], "tasset_b", (-3.6, 6.0, 3.0), (3.6, 13.4, 3.6), "armor_hi", rot=("x", 22.5),
           pivot=(0, 13, 3.3), **SP)
    m.cube_lr(waist, waist, "hip_plate", (4.4, 8.4, -3.0), (5.4, 13.6, 3.0), "armor", rot=("z", 22.5), pivot=(4.9, 13.6, 0), **SP)
    m.cube_lr(RL[0], LL[0], "knee", (1.0, 6.6, -3.0), (4.0, 9.0, -1.6), "trim", rot=("x", -22.5), pivot=(2.5, 8, -2.3))
    # capa de cielo estrellado
    cape = m.bone("cape", (0, 24, 3.6), torso, rotation=(6, 0, 0))
    m.cube(cape, "cape", (-5.6, 2.0, 3.6), (5.6, 24.0, 4.3), "cape", **CS)
    m.cube(cape, "cape_lining", (-5.4, 2.4, 3.3), (5.4, 23.6, 3.6), "cape_in")
    m.cube_lr(cape, cape, "cape_tail", (2.0, -1.0, 3.7), (5.6, 3.0, 4.2), "cape", rot=("z", 22.5), pivot=(3.8, 3, 4), **CS)
    # espadon de energia
    sw = m.bone("sword", (6.5, 10.0, 0), AR[2])
    m.cube(sw, "grip", (6.05, 9.55, -2.6), (6.95, 10.45, 4.0), "silver")
    m.cube(sw, "pommel", (5.8, 9.3, 4.0), (7.2, 10.7, 5.4), "glow", rot=("z", 45), pivot=(6.5, 10, 4.7))
    m.cube(sw, "guard", (3.6, 9.0, -3.4), (9.4, 11.0, -2.6), "armor_hi", **SP)
    for sx in (1, -1):
        m.cube(sw, f"guard_tip{sx}", (6.5 + 3.0 * sx - 0.6, 9.4, -3.6), (6.5 + 3.0 * sx + 0.6, 10.6, -2.4), "trim",
               rot=("z", 45), pivot=(6.5 + 3.0 * sx, 10, -3))
    energy_blade(m, sw, "blade", 6.5, 10.0, -3.4, 24, 1.4)
    m.ZERO_BONES += ["sword", "cape", "core", "orbit_r", "orbit_l"]

    def orbits(a, length, speed=1.0):
        FX.spin(a, "orbit_r", length, speed)
        FX.spin(a, "orbit_l", length, -speed)
        FX.spin(a, "core", length, 2 * speed, "z")

    a = GM.human_idle(m, arm_r=(-25, 0, 10), arm_l=(-10, 0, -10),
                      extra=lambda a, t, s: (a.rot("sword", t, -70, 0, 0), a.rot("cape", t, 3 * s, 0, 0)))
    orbits(a, 2.4)
    a = GM.human_walk(m, leg=22, arm=12, lean=6, length=1.2, arm_r=(-30, 0, 10),
                      extra=lambda a, t, s: (a.rot("sword", t, -70, 0, 0), a.rot("cape", t, 12 + 4 * s, 0, 0)))
    orbits(a, 1.2)

    def anim(name, length, keys, speed=None):
        a = m.anim(name, length, "once")
        a.rest(0)
        for t, pose, lin in keys:
            a.pose(t, pose, i="linear" if lin else "catmullrom")
        a.rest(length)
        orbits(a, length, speed or 1.0)
        return a

    up = {"right_arm": (-160, 0, 20), "sword": (-100, 0, 0), "torso": (-6, 18, 0)}
    down = {"right_arm": (-60, 0, -15), "sword": (-30, 0, 0), "torso": (18, -18, 0)}
    anim("attack", 0.7, [(0.15, up, False), (0.3, down, True)])
    side_a = {"right_arm": (-90, 70, 0), "sword": (-80, 0, 0), "torso": (5, 35, 0)}
    side_b = {"right_arm": (-90, -70, 0), "sword": (-80, 0, 0), "torso": (5, -35, 0)}
    anim("combo", 1.0, [(0.0, side_a, True), (0.1, side_b, True), (0.25, up, False), (0.35, down, True),
                        (0.5, side_b, False), (0.62, side_a, True)])
    anim("mark", 1.0, [(0.25, {"left_arm": (-100, 0, -5), "h_head": (-5, -10, 0)}, False),
                       (0.7, {"left_arm": (-100, 0, -5), "h_head": (-5, -10, 0)}, False)], 2)
    a = anim("dash", 0.9, [(0.2, {"torso": (25, 0, 0), "right_arm": (-60, 60, 0), "sword": (-80, 0, 0),
                                  "body": {"p": (0, -2, 0)}}, False)])
    a.scl("body", 0, 1)
    a.scl("body", 0.3, 1)
    a.scl("body", 0.4, 0.05, 1.4, 0.05)
    a.scl("body", 0.5, 0.05, 1.4, 0.05)
    a.scl("body", 0.6, 1)
    anim("pools", 1.2, [(0.3, {"left_arm": (-175, 0, -10), "body": {"p": (0, 2, 0)}}, False),
                        (0.5, {**GM.KNEEL, "left_arm": (-50, 0, -5), "torso": (35, 0, 0)}, True),
                        (0.8, {**GM.KNEEL, "left_arm": (-50, 0, -5), "torso": (35, 0, 0)}, False)])
    grab = {"right_arm": (-90, -30, 0), "left_arm": (-90, 30, 0), "sword": (-80, 0, 0), "torso": (-5, 0, 0)}
    crush = {"right_arm": (-60, 30, -20), "left_arm": (-60, -30, 20), "sword": (-80, 0, 0), "torso": (25, 0, 0),
             "body": {"p": (0, -2, 0)}}
    anim("crush", 1.1, [(0.2, grab, False), (0.4, {**grab, "torso": (-12, 0, 0)}, False), (0.5, crush, True),
                        (0.8, crush, False)], 3)
    charge = {"right_arm": (-30, 0, 70), "left_arm": (-30, 0, -70), "sword": (-80, 0, 0), "h_head": (-25, 0, 0),
              "torso": (-10, 0, 0), "body": {"p": (0, 2, 0)}}
    anim("nova", 1.2, [(0.3, {"right_arm": (-60, -60, 0), "left_arm": (-60, 60, 0), "torso": (20, 0, 0)}, False),
                       (0.4, charge, True), (0.8, charge, False)], 3)
    channel = {**GM.KNEEL, "right_arm": (-60, 0, 0), "sword": (-150, 0, 0), "left_arm": (-150, 0, -30),
               "h_head": (-30, 0, 0), "torso": (5, 0, 0)}
    anim("horizon", 2.6, [(0.4, channel, False), (1.95, channel, False), (2.05, charge, True), (2.3, charge, False)], -4)
    raise_ = {"right_arm": (-178, 0, 5), "sword": (-90, 0, 0), "left_arm": (-60, 0, -60), "h_head": (-25, 0, 0)}
    anim("summon", 1.4, [(0.35, raise_, False), (1.0, raise_, False)], 3)
    anim("phase_change", 1.8, [(0.5, {**GM.KNEEL, "torso": (40, 0, 0), "h_head": (25, 0, 0), "right_arm": (-60, 0, 0),
                                      "sword": (-150, 0, 0)}, False),
                               (0.8, {**GM.KNEEL, "torso": (40, 0, 0), "h_head": (25, 0, 0), "right_arm": (-60, 0, 0),
                                      "sword": (-150, 0, 0)}, False),
                               (1.2, charge, True), (1.5, charge, False)], 4)
    GM.human_hurt(m)
    a = GM.human_spawn(m, raise_, length=2.0)
    orbits(a, 2.0, 2)
    GM.human_death(m, 2.4)
    m.scale(1.5)
    return m


# ===========================================================================
# SOLDADO ESTELAR (ZOMBIE)
# ===========================================================================
def build_soldier():
    m = _model("xy_soldier", 1314)

    def head(m, hd):
        m.cube(hd, "dome", (-3.4, 24.8, -3.4), (3.4, 31.2, 3.4), "silver", decor={"north": "dome_visor"})
        m.cube(hd, "dome45", (-2.8, 25.4, -2.8), (2.8, 31.8, 2.8), "silver", rot=("y", 45), pivot=(0, 28, 0))
        m.cube(hd, "dome_top", (-2.4, 31.0, -2.4), (2.4, 32.6, 2.4), "armor_hi", rot=("x", 22.5), pivot=(0, 31.6, 0), **SP)
        m.cube(hd, "antenna", (2.4, 30.0, 1.0), (3.0, 35.0, 1.6), "trim", rot=("z", -22.5), pivot=(2.7, 30, 1.3))
        m.cube(hd, "antenna_tip", (3.6, 34.0, 0.8), (4.6, 35.0, 1.8), "glow")

    H = AN.humanoid(m, k=1.0, mats={"skin": "armor", "chest": "silver", "belly": "armor", "arm": "armor", "hand": "armor_hi",
                                     "thigh": "armor", "shin": "silver", "foot": "armor_hi", "pelvis": "armor"}, head=head)
    for c in m.CUBES:
        if c.mat == "armor" and not c.decor:
            c.decor["all"] = "star_plate"
    torso = H["torso"]
    AR = H["arms"]["right"]
    m.cube(torso, "chest_stripe", (-0.8, 15.4, -3.3), (0.8, 23.8, -2.7), "trim")
    m.cube(torso, "pack", (-3.0, 16.4, 2.6), (3.0, 23.0, 4.4), "armor_hi", **SP)
    m.cube_lr(torso, torso, "thruster", (1.4, 15.0, 3.4), (2.8, 17.0, 4.8), "glow")
    m.cube_lr(AR[0], H["arms"]["left"][0], "pad", (4.4, 21.8, -2.4), (8.6, 24.4, 2.4), "silver", rot=("z", -22.5),
              pivot=(6.5, 23, 0))
    sw = m.bone("sword", (6.5, 10.0, 0), AR[2])
    m.cube(sw, "grip", (6.1, 9.5, -2.2), (6.9, 10.5, 2.0), "silver")
    m.cube(sw, "guard", (5.4, 9.2, -2.8), (7.6, 10.8, -2.2), "trim")
    energy_blade(m, sw, "blade", 6.5, 10.0, -2.8, 11, 0.9)
    m.ZERO_BONES += ["sword"]
    GM.human_idle(m, arm_r=(-25, 0, 8), extra=lambda a, t, s: a.rot("sword", t, 50, 0, 0))
    GM.human_walk(m, leg=24, arm=12, arm_r=(-30, 0, 8), extra=lambda a, t, s: a.rot("sword", t, 50, 0, 0))
    a = m.anim("attack", 0.7, "once")
    a.rest(0)
    a.pose(0.15, {"right_arm": (-150, 0, 20), "sword": (40, 0, 0), "torso": (-5, 15, 0)})
    a.pose(0.3, {"right_arm": (-50, 0, -15), "sword": (0, 0, 0), "torso": (15, -15, 0)}, i="linear")
    a.rest(0.7)
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-170, 0, 10), "sword": (70, 0, 0)})
    GM.human_death(m)
    return m


# ===========================================================================
# CABALLERO DEL VACIO (WITHER_SKELETON)
# ===========================================================================
def build_knight():
    m = _model("xy_knight", 1315)

    def head(m, hd):
        m.cube(hd, "helm", (-3.6, 24.6, -3.6), (3.6, 32.0, 3.6), "void", decor={"north": "visor", "all": "cosmic"})
        m.cube(hd, "helm_ridge", (-0.6, 30.6, -4.0), (0.6, 33.4, 3.6), "armor_hi")
        for sx in (1, -1):
            for i, (y0, h, ang) in enumerate(((29.0, 3.0, 22.5), (31.6, 3.0, 45))):
                m.cube(hd, f"horn{sx}{i}", (3.4 * sx - 0.7 + (1.6 * i * sx), y0, -0.7), (3.4 * sx + 0.7 + (1.6 * i * sx), y0 + h, 0.7),
                       "silver" if i else "armor_hi", rot=("z", -ang * sx), pivot=(3.4 * sx + 1.6 * i * sx, y0, 0))

    H = AN.humanoid(m, k=1.15, mats={"skin": "void", "chest": "armor", "belly": "void", "arm": "armor", "hand": "void",
                                      "thigh": "void", "shin": "armor", "foot": "void", "pelvis": "void"}, head=head)
    for c in m.CUBES:
        if c.mat == "armor" and not c.decor:
            c.decor["all"] = "star_plate"
        elif c.mat == "void" and not c.decor:
            c.decor["all"] = "cosmic"
    torso = H["torso"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    m.cube_lr(AR[0], AL[0], "pauldron", (4.0, 21.8, -3.4), (10.2, 25.4, 3.4), "armor", rot=("z", -22.5), pivot=(7.1, 23.6, 0),
              **SP)
    m.cube_lr(AR[0], AL[0], "spike", (7.4, 24.6, -0.5), (8.4, 28.6, 0.5), "silver", rot=("z", -22.5), pivot=(7.9, 24.6, 0))
    m.cube(m.BONES["skirt_front"], "tabard", (-2.8, 2.0, -3.4), (2.8, 13.4, -2.8), "cape", **CS)
    sh = m.bone("shield", (-8.4, 15.0, 0), AL[1])
    m.cube(sh, "shield", (-9.6, 7.0, -4.4), (-8.6, 20.0, 4.4), "void", decor={"all": "star_emblem"})
    m.cube(sh, "shield_tip", (-9.5, 4.6, -3.0), (-8.7, 9.0, 3.0), "void", rot=("x", 45), pivot=(-9.1, 7, 0))
    m.cube(sh, "shield_rim", (-9.8, 19.6, -4.6), (-8.4, 20.6, 4.6), "trim")
    sw = m.bone("sword", (6.5, 10.0, 0), AR[2])
    m.cube(sw, "grip", (6.1, 9.5, -2.6), (6.9, 10.5, 3.0), "silver")
    m.cube(sw, "guard", (4.4, 9.0, -3.4), (8.6, 11.0, -2.6), "armor_hi")
    m.cube(sw, "blade", (6.15, 8.8, -19.0), (6.85, 11.2, -3.4), "void", **CS)
    m.cube(sw, "blade_edge", (6.2, 8.4, -19.0), (6.8, 8.9, -3.4), "glow")
    m.ZERO_BONES += ["sword", "shield"]
    extra = lambda a, t, s: a.rot("sword", t, 50, 0, 0)  # noqa: E731
    GM.human_idle(m, arm_r=(-25, 0, 10), arm_l=(-35, 25, -6), extra=extra)
    GM.human_walk(m, leg=20, arm=10, lean=6, arm_r=(-30, 0, 10), arm_l=(-35, 25, -6), extra=extra)
    a = m.anim("attack", 0.8, "once")
    a.rest(0)
    a.pose(0.2, {"right_arm": (-170, 0, 10), "sword": (60, 0, 0), "torso": (-8, 10, 0), "left_arm": (-35, 25, -6)})
    a.pose(0.35, {"right_arm": (-50, 0, -10), "sword": (0, 0, 0), "torso": (25, -10, 0), "left_arm": (-35, 25, -6)}, i="linear")
    a.rest(0.8)
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-170, 0, 10), "sword": (70, 0, 0), "left_arm": (-80, 50, 0)})
    GM.human_death(m)
    return m


# ===========================================================================
# FRAGMENTO ESTELAR (VEX)
# ===========================================================================
def build_shard():
    m = _model("xy_shard", 1316, atlas=128)
    root = m.root
    hb = m.bone("hitbox", (0, 8, 0), root)
    m.cube(hb, "hitbox", (-3, 3, -3), (3, 13, 3), "hitbox")
    m.bone("tag_name", (0, 17, 0), root)
    body = m.bone("body", (0, 8, 0), root)
    m.cube(body, "core", (-1.6, 7.0, -1.6), (1.6, 10.2, 1.6), "glow", rot=("y", 45), pivot=(0, 8.6, 0))
    RG.crystals(m, body, (0, 8.6, 0), [(0, 0, 5.0, 1.0, None), (-1.2, 0.6, 3.6, 0.7, ("z", 45)), (1.2, -0.6, 3.6, 0.7, ("z", -45)),
                                       (0.6, 1.2, 3.0, 0.6, ("x", 45)), (-0.6, -1.2, 3.0, 0.6, ("x", -45))], "up")
    m.cube(body, "under", (-0.9, 3.0, -0.9), (0.9, 7.2, 0.9), "ice_dark", rot=("y", 45), pivot=(0, 5, 0), decor={"all": "crystal"})
    m.cube(body, "under_tip", (-0.5, 1.6, -0.5), (0.5, 3.2, 0.5), "ice", rot=("y", 45), pivot=(0, 2.4, 0))
    wings = []
    for side, sx in (("right", 1), ("left", -1)):
        w = m.bone(f"{side}_wing", (1.4 * sx, 9.0, 0.8), body)
        for i, (ln, ang) in enumerate(((5.0, 22.5), (3.8, 45))):
            m.cube(w, f"{side}_wing{i}", (min(1.4 * sx, (1.4 + ln) * sx), 8.6 + i, 0.6),
                   (max(1.4 * sx, (1.4 + ln) * sx), 9.4 + i, 1.2), "ice", rot=("z", ang * sx), pivot=(1.4 * sx, 9, 0.9),
                   decor={"all": "crystal"})
        wings.append(f"{side}_wing")
    m.ZERO_BONES = ["body"] + wings
    a = m.anim("idle", 1.6, "loop")
    for t, s in ((0, 0), (0.8, 1), (1.6, 0)):
        a.pos("body", t, 0, 0.8 * s, 0)
    FX.spin(a, "body", 1.6, 0.5)
    for k in range(5):
        t = 1.6 * k / 4
        a.rot("right_wing", t, 0, 0, 25 * (k % 2))
        a.rot("left_wing", t, 0, 0, -25 * (k % 2))
    a = m.anim("walk", 0.8, "loop")
    FX.spin(a, "body", 0.8, 1)
    a = m.anim("attack", 0.6, "once")
    a.scl("body", 0, 1)
    a.scl("body", 0.15, 1.3)
    a.scl("body", 0.3, 0.9)
    a.scl("body", 0.6, 1)
    a.pos("body", 0, 0, 0, 0)
    a.pos("body", 0.25, 0, 0, -5, i="linear")
    a.pos("body", 0.6, 0, 0, 0)
    a = m.anim("hurt", 0.3, "once")
    a.rot("body", 0, 0, 0, 0)
    a.rot("body", 0.08, -15, 0, 15)
    a.rot("body", 0.3, 0, 0, 0)
    a = m.anim("spawn", 1.0, "once")
    a.scl("body", 0, 0.1)
    a.scl("body", 0.6, 1.2)
    a.scl("body", 1.0, 1)
    a = m.anim("death", 1.0, "hold")
    a.scl("body", 0, 1)
    a.scl("body", 0.3, 1.4)
    a.scl("body", 1.0, 0.05)
    return m


# ===========================================================================
# POZO GRAVITATORIO (ARMOR_STAND)
# ===========================================================================
def build_well():
    m = _model("xy_well", 1317)
    root = m.root
    m.bone("hitbox", (0, 0, 0), root)
    disk = m.bone("disk", (0, 0.2, 0), root)
    m.cube(disk, "hole", (-14, 0.1, -14), (14, 0.4, 14), "void", rot=("y", 45), pivot=(0, 0.2, 0))
    m.cube(disk, "hole2", (-14, 0.15, -14), (14, 0.45, 14), "void")
    for k in range(16):
        a = 2 * math.pi * k / 16
        r = 22
        x, z = r * math.cos(a), r * math.sin(a)
        m.cube(disk, f"acc{k}", (x - 3, 0.2, z - 3), (x + 3, 0.9, z + 3), "glow" if k % 2 else "ice_dark", rot=("y", 45),
               pivot=(x, 0.5, z))
    inner = m.bone("inner", (0, 0.4, 0), root)
    for k in range(10):
        a = 2 * math.pi * k / 10
        r = 30 + (k % 3) * 4
        x, z = r * math.cos(a), r * math.sin(a)
        m.cube(inner, f"dust{k}", (x - 1, 0.4, z - 1), (x + 1, 2.4, z + 1), "star" if k % 2 else "ice", rot=("y", 45),
               pivot=(x, 1.4, z))
    m.ZERO_BONES = ["disk", "inner"]
    a = m.anim("idle", 2.0, "loop")
    FX.spin(a, "disk", 2.0, -1)
    FX.spin(a, "inner", 2.0, 0.5)
    for t, s in ((0, 0), (1.0, 1), (2.0, 0)):
        a.scl("disk", t, 1 + 0.06 * s, 1, 1 + 0.06 * s)
    a = m.anim("spawn", 0.8, "once")
    a.scl("disk", 0, 0.05, 1, 0.05)
    a.scl("disk", 0.6, 1.1, 1, 1.1)
    a.scl("disk", 0.8, 1)
    a.scl("inner", 0, 0.05, 1, 0.05)
    a.scl("inner", 0.8, 1)
    return m


BUILDERS = {"xylar": build_xylar, "xy_soldier": build_soldier, "xy_knight": build_knight, "xy_shard": build_shard,
            "xy_well": build_well}
SHOTS = {
    "xylar": [("idle", 0.6, -30), ("rest", 0, 150), ("attack", 0.15, -50), ("nova", 0.6, -30)],
    "xy_soldier": [("idle", 0.5, -30), ("rest", 0, 150), ("attack", 0.15, -60), ("walk", 0.25, -70)],
    "xy_knight": [("idle", 0.5, -30), ("rest", 0, 150), ("attack", 0.2, -60), ("walk", 0.25, -70)],
    "xy_shard": [("idle", 0.4, -30), ("rest", 0, 150), ("attack", 0.15, -40), ("walk", 0.2, -80)],
    "xy_well": [("idle", 0.2, -30), ("idle", 0.8, -30), ("spawn", 0.3, -30), ("spawn", 0.7, -30)],
}
VIEW = {"xylar": (32, 4.3), "xy_shard": (8, 13.0), "xy_well": (2, 3.0)}
ACTIONS = [("combo", 0.1, -40), ("combo", 0.35, -40), ("mark", 0.5, -30), ("pools", 0.5, -40),
           ("crush", 0.5, -30), ("nova", 0.5, -30), ("horizon", 1.0, -40), ("phase_change", 1.3, -30)]


def previews(name, m):
    import render_preview as RP
    from PIL import Image, ImageDraw
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
    sheet = Image.new("RGB", (340 * len(frames), 420))
    for i, f in enumerate(frames):
        sheet.paste(f, (i * 340, 0))
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
            if name == "xylar":
                FX.action_sheet(m, ACTIONS, PREVIEW / "xylar_acciones.png", focus=32, scale=4.2)


if __name__ == "__main__":
    main()
