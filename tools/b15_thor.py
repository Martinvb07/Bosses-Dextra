#!/usr/bin/env python3
"""
Boss 15 - THOR y sus subditos (modelos de ModelEngine).

  thor           Dios del Trueno: corpulento, barba y melena rojas trenzadas, casco con alas,
                 coraza con nudos nordicos y runas que brillan, cinturon de fuerza (Megingjord),
                 capa roja, guanteletes de hierro y Mjolnir con rayos que chisporrotean
  th_einherjar   guerrero del Valhalla: espectral dorado, casco con cuernos cortos, escudo y hacha (ZOMBIE)
  th_creeper     creeper de tormenta: cuerpo con franjas de rayo, pararrayos de cobre y nubecita (CREEPER)
  th_spark       chispa viviente: bola de rayos con patitas de electricidad (SILVERFISH)
  th_field       campo estatico: placa de cobre en el suelo con bobinas y arcos (ARMOR_STAND)
  th_cloud       nube de tormenta: nube flotante con rayos que caen (ARMOR_STAND)

Uso: python3 tools/b15_thor.py [modelo ...] [--no-preview]
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

ROOT = Path(__file__).resolve().parent.parent / "Modelos/15_Thor"
BLUEPRINTS = ROOT / "ModelEngine/blueprints"
PREVIEW = ROOT / "preview"

BOLT = (140, 230, 255)
MATS = {
    "tan": ((214, 168, 130), 6), "ginger": ((190, 70, 30), 8), "iron": ((120, 124, 136), 6), "iron_dark": ((70, 74, 86), 6),
    "steel": ((170, 176, 190), 5), "gold": ((220, 180, 70), 7), "leather": ((92, 60, 36), 7), "cape": ((170, 30, 30), 6),
    "cape_dark": ((110, 20, 20), 5), "fur": ((120, 96, 70), 9), "wing": ((235, 235, 240), 4), "bolt": (BOLT, 2),
    "bolt_core": ((250, 255, 255), 1), "rune": ((120, 220, 255), 3), "wood": ((100, 70, 44), 8), "spectral": ((255, 220, 120), 4),
    "spectral_dark": ((190, 140, 60), 5), "creeper": ((70, 120, 150), 7), "creeper_dark": ((40, 70, 100), 6),
    "red": ((60, 110, 200), 6), "white": ((240, 220, 150), 5), "copper": ((200, 110, 70), 6), "copper_dark": ((120, 70, 50), 6), "cloud": ((90, 96, 110), 6), "cloud_hi": ((150, 156, 170), 6),
    "hitbox": ((255, 255, 255), 0),
}


def storm_decor(m):
    D = m.decor

    @D
    def d_plate_rune(f):
        if f.name in ("up", "down"):
            return
        for y in range(f.h):
            k = 1.25 - 0.5 * y / max(1, f.h - 1)
            for x in range(f.w):
                f.shade(x, y, k)
        if f.w > 5 and f.h > 5:
            cx = f.w // 2
            for y in range(2, f.h - 2):
                f.put(cx, y, (120, 220, 255))
            f.put(cx - 1, 3, (120, 220, 255))
            f.put(cx + 1, 5, (120, 220, 255))

    @D
    def d_lightning(f):
        x = f.w // 2
        for y in range(f.h):
            f.put(x, y, (250, 255, 255))
            x += 1 if (y // 2) % 2 == 0 else -1
            x = max(0, min(f.w - 1, x))

    @D
    def d_creeper_face(f):
        if f.name != "north":
            return
        w = f.w
        dark = (10, 20, 30)
        f.rect(1, 2, 4, 5, dark)
        f.rect(w - 4, 2, w - 1, 5, dark)
        f.rect(w // 2 - 1, 5, w // 2 + 1, 8, dark)
        f.rect(w // 2 - 2, 7, w // 2 - 1, 10, dark)
        f.rect(w // 2 + 1, 7, w // 2 + 2, 10, dark)
        f.put(2, 3, BOLT)
        f.put(w - 3, 3, BOLT)

    @D
    def d_spark_eyes(f):
        if f.name != "north":
            return
        f.rect(1, 1, 3, 3, (20, 40, 80))
        f.rect(f.w - 3, 1, f.w - 1, 3, (20, 40, 80))

    @D
    def d_crystal(f):
        for y in range(f.h):
            f.put(0, y, (250, 255, 255))


def _model(name, seed, atlas=256):
    m = Model(name, MATS, seed=seed, atlas_w=atlas)
    m.SHINE |= {"iron", "steel", "gold", "bolt", "bolt_core", "rune", "copper", "wing"}
    m.WOOD |= {"wood"}
    GM.add_common_decor(m)
    RG.norse_decor(m)
    storm_decor(m)
    return m


PR = {"decor": {"all": "plate_rune"}}
BR = {"decor": {"all": "braid"}}
KN = {"decor": {"all": "knot"}}


def zigzag(m, bone, name, x, y_top, z, length, seg=4.0, w=0.6, mat="bolt"):
    """Rayo en zigzag hacia abajo (tramos inclinados alternos)."""
    y = y_top
    for i in range(int(length / seg)):
        ang = 22.5 if i % 2 == 0 else -22.5
        dx = seg * 0.38 * (1 if i % 2 == 0 else -1)
        m.cube(bone, f"{name}{i}", (x - w, y - seg, z - w), (x + w, y, z + w), mat, rot=("z", ang), pivot=(x, y, z),
               decor={"all": "lightning"})
        x += dx
        y -= seg * 0.92


# ===========================================================================
# THOR
# ===========================================================================
def thor_head(m, hd):
    AN.default_head(m, hd, face="viking_face", mat="tan")
    m.cube(hd, "helm", (-3.8, 29.4, -3.8), (3.8, 32.4, 3.9), "steel", decor={"all": "knot"})
    m.cube(hd, "helm_dome", (-2.8, 32.0, -2.8), (2.8, 33.6, 2.9), "steel", rot=("y", 45), pivot=(0, 32.6, 0))
    m.cube(hd, "helm_band", (-3.9, 29.2, -4.0), (3.9, 30.0, 4.0), "gold")
    m.cube(hd, "nasal", (-0.5, 26.6, -4.6), (0.5, 30.0, -3.8), "steel")
    for sx in (1, -1):                                           # alas del casco
        for i, (ln, ang) in enumerate(((5.0, 22.5), (4.4, 45), (3.4, 45))):
            y = 30.4 + i * 1.1
            m.cube(hd, f"wing{sx}{i}", (min(3.6 * sx, (3.6 + 0.4) * sx), y, -0.4 - i * 0.2),
                   (max(3.6 * sx, (3.6 + 0.4) * sx), y + ln, 0.6 + i * 1.4), "wing", rot=("z", -ang * sx),
                   pivot=(3.8 * sx, y, 0), decor={"all": "feather"})
    m.cube(hd, "beard", (-3.2, 21.0, -4.6), (3.2, 26.6, -3.0), "ginger", **BR)
    m.cube(hd, "beard_low", (-2.4, 18.0, -4.8), (2.4, 21.4, -3.4), "ginger", rot=("x", -22.5), pivot=(0, 21.4, -4.1), **BR)
    for sx in (1, -1):
        m.cube(hd, f"braid{sx}", (1.6 * sx - 0.6, 15.6, -4.8), (1.6 * sx + 0.6, 19.0, -4.0), "ginger", **BR)
        m.cube(hd, f"braid_ring{sx}", (1.6 * sx - 0.7, 16.0, -4.9), (1.6 * sx + 0.7, 16.8, -3.9), "gold")
    m.cube(hd, "moustache", (-2.8, 25.2, -4.8), (2.8, 26.4, -3.8), "ginger", **BR)
    m.cube(hd, "mane", (-3.8, 21.0, 2.4), (3.8, 30.0, 4.6), "ginger", **BR)
    m.cube_lr(hd, hd, "mane_side", (3.4, 22.0, -1.0), (4.4, 29.0, 3.4), "ginger", rot=("z", 22.5), pivot=(3.9, 29, 1), **BR)


def build_thor():
    m = _model("thor", 1515, atlas=512)
    H = AN.humanoid(m, k=1.35, mats={"skin": "tan", "chest": "iron", "belly": "leather", "arm": "tan", "hand": "iron_dark",
                                      "thigh": "leather", "shin": "iron", "foot": "leather", "pelvis": "leather"},
                    head=thor_head)
    for c in m.CUBES:
        if c.mat == "iron" and not c.decor:
            c.decor["all"] = "plate_rune"
        elif c.mat == "tan" and c.bone.name.endswith("arm"):
            c.decor.setdefault("all", "tattoo")
    torso, waist = H["torso"], H["waist"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    m.cube(torso, "breast", (-5.4, 18.4, -4.4), (5.4, 24.0, -3.6), "iron", **PR)
    m.cube(torso, "rune_disc", (-1.4, 20.0, -4.8), (1.4, 22.8, -4.2), "rune", rot=("z", 45), pivot=(0, 21.4, -4.5))
    m.cube(torso, "fur_collar", (-6.0, 22.8, -4.0), (6.0, 25.4, 4.2), "fur", decor={"all": "fur"})
    m.cube(waist, "megingjord", (-6.2, 13.2, -4.0), (6.2, 15.6, 4.0), "gold", **KN)
    m.cube(waist, "buckle", (-1.6, 12.8, -4.4), (1.6, 16.0, -3.9), "rune", rot=("z", 45), pivot=(0, 14.4, -4.1))
    m.cube(m.BONES["skirt_front"], "tasset", (-3.4, 6.6, -4.0), (3.4, 13.4, -3.4), "leather", decor={"all": "straps"})
    m.cube(m.BONES["skirt_back"], "tasset_b", (-4.0, 6.6, 3.4), (4.0, 13.4, 4.0), "iron_dark",
           decor={"all": "chainmail"})
    for side, sx, arm in (("r", 1, AR), ("l", -1, AL)):
        x0, x1 = (4.2, 10.8) if sx > 0 else (-10.8, -4.2)
        m.cube(arm[0], f"pauldron_{side}", (x0, 22.4, -3.8), (x1, 26.0, 3.8), "iron", rot=("z", -22.5 * sx),
               pivot=(7.5 * sx, 24.2, 0), **PR)
        m.cube(arm[0], f"pauldron_fur_{side}", (x0, 25.4, -3.4), (x1, 26.8, 3.4), "fur", rot=("z", -22.5 * sx),
               pivot=(7.5 * sx, 24.2, 0), decor={"all": "fur"})
        m.cube(arm[1], f"gauntlet_{side}", (4.4 * sx if sx > 0 else -8.6, 11.6, -2.4), (8.6 if sx > 0 else -4.4, 15.6, 2.4),
               "iron_dark", **PR)
    cape = m.bone("cape", (0, 24.5, 3.8), torso, rotation=(6, 0, 0))
    m.cube(cape, "cape", (-6.0, 1.0, 3.8), (6.0, 24.5, 4.6), "cape", decor={"all": "knot"})
    m.cube(cape, "cape_in", (-5.8, 1.4, 3.5), (5.8, 24.2, 3.8), "cape_dark")
    for sx in (1, -1):
        m.cube(torso, f"clasp{sx}", (4.2 * sx - 1.0, 22.6, -4.6), (4.2 * sx + 1.0, 24.6, -4.0), "gold", rot=("z", 45),
               pivot=(4.2 * sx, 23.6, -4.3))
    # Mjolnir
    hm = m.bone("hammer", (6.5, 10.0, 0), AR[2])
    m.cube(hm, "handle", (6.0, 9.5, -12.0), (7.0, 10.5, 2.4), "leather", decor={"all": "straps"})
    m.cube(hm, "pommel", (5.7, 9.2, 2.4), (7.3, 10.8, 3.6), "steel")
    m.cube(hm, "loop", (6.2, 8.0, 3.4), (6.8, 9.6, 5.2), "leather")
    m.cube(hm, "head", (4.4, 6.2, -17.6), (8.6, 13.8, -12.0), "steel", **KN)
    m.cube(hm, "head_face_a", (4.0, 5.8, -16.8), (9.0, 14.2, -12.8), "iron", rot=("z", 45), pivot=(6.5, 10, -14.8))
    m.cube(hm, "head_rune", (4.2, 8.8, -15.6), (8.8, 11.2, -13.6), "rune")
    zig = m.bone("hammer_bolts", (6.5, 10, -14.8), hm)
    zigzag(m, zig, "hb_a", 6.5, 17.0, -14.8, 8, seg=3.0, w=0.35)
    zigzag(m, zig, "hb_b", 9.2, 12.0, -16.0, 6, seg=2.6, w=0.3)
    m.ZERO_BONES += ["hammer", "cape", "hammer_bolts"]

    def crackle(a, length, k=1.0):
        for i in range(9):
            t = length * i / 8
            s = 0.05 if (i % 3 == 1 and k < 2) else 1.0 + 0.2 * (i % 2)
            a.scl("hammer_bolts", t, s, s, s, i="linear")

    a = GM.human_idle(m, arm_r=(-25, 0, 12), arm_l=(-10, 0, -12),
                      extra=lambda a, t, s: (a.rot("hammer", t, 40, 0, 0), a.rot("cape", t, 3 * s, 0, 0)))
    crackle(a, 2.4)
    a = GM.human_walk(m, leg=22, arm=14, lean=6, length=1.2, arm_r=(-30, 0, 12),
                      extra=lambda a, t, s: (a.rot("hammer", t, 40, 0, 0), a.rot("cape", t, 12 + 4 * s, 0, 0)))
    crackle(a, 1.2)

    def anim(name, length, keys, k=1.0):
        a = m.anim(name, length, "once")
        a.rest(0)
        for t, pose, lin in keys:
            a.pose(t, pose, i="linear" if lin else "catmullrom")
        a.rest(length)
        crackle(a, length, k)
        return a

    up = {"right_arm": (-170, 0, 10), "hammer": (60, 0, 0), "torso": (-8, 12, 0)}
    down = {"right_arm": (-55, 0, -10), "hammer": (0, 0, 0), "torso": (22, -12, 0)}
    anim("attack", 0.7, [(0.15, up, False), (0.3, down, True)])
    swing_a = {"right_arm": (-90, 80, 0), "hammer": (0, 0, 0), "torso": (5, 40, 0)}
    swing_b = {"right_arm": (-90, -70, 0), "hammer": (0, 0, 0), "torso": (5, -40, 0)}
    anim("swing", 0.7, [(0.12, swing_a, False), (0.28, swing_b, True)])
    anim("throw", 1.0, [(0.25, {"right_arm": (-170, 0, 20), "hammer": (80, 0, 0), "torso": (-15, 20, 0), "left_arm": (-60, 0, -20)},
                         False), (0.4, {"right_arm": (-80, 0, -10), "hammer": (0, 0, 0), "torso": (20, -15, 0),
                                        "left_arm": (-30, 0, -20)}, True)], 2)
    slam = {**GM.KNEEL, "right_arm": (-50, 0, -10), "hammer": (-10, 0, 0), "torso": (35, 0, 0)}
    anim("slam", 1.0, [(0.12, {**up, "body": {"p": (0, 3, 0)}}, False), (0.25, slam, True), (0.55, slam, False)], 2)
    call = {"right_arm": (-178, 0, 5), "hammer": (90, 0, 0), "left_arm": (-40, 0, -50), "h_head": (-30, 0, 0)}
    anim("call", 1.4, [(0.3, call, False), (1.0, call, False)], 3)
    absorb = {"right_arm": (-60, 0, 70), "left_arm": (-60, 0, -70), "hammer": (60, 0, 0), "h_head": (-35, 0, 0),
              "torso": (-12, 0, 0), "body": {"p": (0, 2, 0)}}
    anim("absorb", 1.2, [(0.3, absorb, False), (0.9, absorb, False)], 3)
    anim("nova", 1.2, [(0.2, {**up, "right_arm": (-175, 0, -5), "left_arm": (-175, 0, 20), "body": {"p": (0, 6, 0)}}, False),
                       (0.5, slam, True), (0.8, slam, False)], 3)
    pull = {"right_arm": (-90, 0, 0), "hammer": (90, 0, 0), "left_arm": (-90, 0, 0), "torso": (-8, 0, 0)}
    anim("surge", 1.1, [(0.2, pull, False), (0.45, {**pull, "torso": (-15, 0, 0), "body": {"p": (0, 0, 2)}}, False),
                        (0.5, slam, True), (0.8, slam, False)], 3)
    anim("eruption", 1.0, [(0.1, absorb, False), (0.2, {**absorb, "body": {"p": (0, 4, 0)}}, True), (0.6, absorb, False)], 3)
    anim("judgement", 1.6, [(0.3, {"right_arm": (-110, 0, 0), "hammer": (90, 0, 0), "h_head": (0, 0, 0)}, False),
                            (1.0, {"right_arm": (-110, 0, 0), "hammer": (90, 0, 0)}, False),
                            (1.2, {"right_arm": (-60, 0, 0), "hammer": (0, 0, 0), "torso": (15, 0, 0)}, True)], 3)
    channel = {**GM.KNEEL, "right_arm": (-178, 0, 5), "hammer": (90, 0, 0), "left_arm": (-178, 0, -5), "h_head": (-30, 0, 0)}
    anim("ragnarok", 2.2, [(0.3, channel, False), (1.45, channel, False), (1.55, slam, True), (1.9, slam, False)], 3)
    anim("summon", 1.4, [(0.35, call, False), (1.0, call, False)], 3)
    anim("phase_change", 1.8, [(0.4, {**GM.KNEEL, "torso": (35, 0, 0), "h_head": (25, 0, 0)}, False),
                               (0.6, {**GM.KNEEL, "torso": (35, 0, 0), "h_head": (25, 0, 0)}, False),
                               (0.8, absorb, True), (1.4, call, False)], 3)
    GM.human_hurt(m)
    a = GM.human_spawn(m, call, length=2.0)
    crackle(a, 2.0, 3)
    GM.human_death(m, 2.4)
    m.scale(1.5)
    return m


# ===========================================================================
# EINHERJAR (ZOMBIE)
# ===========================================================================
def build_einherjar():
    m = _model("th_einherjar", 1516)

    def head(m, hd):
        AN.default_head(m, hd, face="draugr_face", mat="spectral")
        m.cube(hd, "helm", (-3.7, 29.4, -3.7), (3.7, 32.4, 3.8), "gold", **KN)
        m.cube(hd, "nasal", (-0.45, 26.6, -4.5), (0.45, 30.0, -3.6), "gold")
        for sx in (1, -1):
            m.cube(hd, f"horn{sx}", (3.4 * sx - 0.6, 30.4, -0.6), (3.4 * sx + 0.6, 33.6, 0.6), "wing", rot=("z", -22.5 * sx),
                   pivot=(3.4 * sx, 30.4, 0))
        m.cube(hd, "beard", (-2.8, 21.6, -4.4), (2.8, 26.4, -3.0), "spectral_dark", **BR)

    H = AN.humanoid(m, k=1.05, mats={"skin": "spectral", "chest": "gold", "belly": "spectral_dark", "arm": "spectral",
                                      "hand": "spectral_dark", "thigh": "spectral_dark", "shin": "gold", "foot": "spectral_dark"},
                    head=head)
    torso = H["torso"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    m.cube(torso, "mail", (-4.8, 15.8, -3.2), (4.8, 23.4, 3.0), "spectral_dark", decor={"all": "chainmail"})
    sh = m.bone("shield", (-6.5, 14, -1), AL[1])
    m.cube(sh, "shield", (-9.6, 7.0, -6.0), (-8.6, 19.0, 6.0), "spectral", decor={"all": "shield_paint"})
    m.cube(sh, "shield45", (-9.5, 8.0, -5.0), (-8.7, 18.0, 5.0), "spectral_dark", rot=("x", 45), pivot=(-9.1, 13, 0))
    m.cube(sh, "shield_boss", (-10.4, 11.6, -1.4), (-9.6, 14.4, 1.4), "gold")
    ax = m.bone("axe", (6.5, 10.0, 0), AR[2])
    m.cube(ax, "haft", (6.1, 9.5, -14.0), (6.9, 10.5, 3.0), "spectral_dark")
    m.cube(ax, "head", (6.15, 10.4, -15.0), (6.85, 16.0, -10.4), "gold", decor={"all": "blade"})
    m.cube(ax, "edge", (6.2, 11.4, -15.6), (6.8, 16.4, -14.6), "bolt")
    m.ZERO_BONES += ["axe", "shield"]
    GM.human_idle(m, arm_r=(-25, 0, 8), arm_l=(-30, 30, -6), extra=lambda a, t, s: a.rot("axe", t, 40, 0, 0))
    GM.human_walk(m, leg=24, arm=10, arm_r=(-30, 0, 8), arm_l=(-35, 30, -6), extra=lambda a, t, s: a.rot("axe", t, 40, 0, 0))
    a = m.anim("attack", 0.7, "once")
    a.rest(0)
    a.pose(0.15, {"right_arm": (-160, 0, 15), "axe": (50, 0, 0), "torso": (-5, 15, 0), "left_arm": (-30, 30, -6)})
    a.pose(0.3, {"right_arm": (-60, 0, -10), "axe": (0, 0, 0), "torso": (12, -10, 0), "left_arm": (-30, 30, -6)}, i="linear")
    a.rest(0.7)
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-170, 0, 10), "axe": (70, 0, 0), "left_arm": (-80, 50, 0)})
    GM.human_death(m)
    return m


# ===========================================================================
# CREEPER DE TORMENTA (CREEPER)
# ===========================================================================
def build_storm_creeper():
    m = _model("th_creeper", 1517, atlas=128)
    root = m.root
    hb = m.bone("hitbox", (0, 13, 0), root)
    m.cube(hb, "hitbox", (-4, 0, -4), (4, 26, 4), "hitbox")
    m.bone("tag_name", (0, 30, 0), root)
    body = m.bone("body", (0, 6, 0), root)
    C = {"decor": {"all": "lightning"}}
    m.cube(body, "torso", (-3.6, 6.0, -2.2), (3.6, 18.0, 2.2), "creeper", **C)
    m.cube(body, "torso45", (-3.0, 6.4, -2.6), (3.0, 17.6, 2.6), "creeper_dark", rot=("y", 45), pivot=(0, 12, 0))
    hd = m.bone("head", (0, 18, 0), body)
    m.cube(hd, "head", (-4.0, 18.0, -4.0), (4.0, 26.0, 4.0), "creeper", decor={"north": "creeper_face", "all": "lightning"})
    for i, (x, z, h) in enumerate(((-2.4, 1.6, 5.0), (2.0, -1.2, 4.0), (0.4, 2.6, 6.0))):
        m.cube(hd, f"rod{i}", (x - 0.35, 26.0, z - 0.35), (x + 0.35, 26.0 + h, z + 0.35), "copper")
        m.cube(hd, f"rod_tip{i}", (x - 0.6, 26.0 + h, z - 0.6), (x + 0.6, 27.0 + h, z + 0.6), "bolt", rot=("y", 45),
               pivot=(x, 26.5 + h, z))
    cl = m.bone("mini_cloud", (0, 34, 0), hd)
    for i, (x, z, s) in enumerate(((0, 0, 3.0), (-2.6, 0.6, 2.2), (2.4, -0.6, 2.4))):
        m.cube(cl, f"puff{i}", (x - s, 33 - s * 0.6, z - s), (x + s, 33 + s * 0.6, z + s), "cloud_hi" if i else "cloud")
    zigzag(m, cl, "zap", 0.5, 31.0, 0, 4, seg=2.0, w=0.25)
    legs = []
    for n, x, z in (("leg_fr", 2.0, -3.0), ("leg_fl", -2.0, -3.0), ("leg_br", 2.0, 3.0), ("leg_bl", -2.0, 3.0)):
        lg = m.bone(n, (x, 6.0, z), root)
        m.cube(lg, n, (x - 2.0, 0, z - 2.0), (x + 2.0, 6.0, z + 2.0), "creeper_dark")
        legs.append(n)
    m.ZERO_BONES = ["body", "head", "mini_cloud"] + legs
    a = m.anim("idle", 2.0, "loop")
    for t, s in ((0, 0), (1.0, 1), (2.0, 0)):
        a.rot("head", t, 0, 6 * s - 3, 0)
        a.pos("mini_cloud", t, 0, 0.6 * s, 0)
    FX.spin(a, "mini_cloud", 2.0, 0.5)
    a = m.anim("walk", 0.8, "loop")
    for t, s in ((0, 1), (0.4, -1), (0.8, 1)):
        a.rot("leg_fr", t, 30 * s, 0, 0)
        a.rot("leg_bl", t, 30 * s, 0, 0)
        a.rot("leg_fl", t, -30 * s, 0, 0)
        a.rot("leg_br", t, -30 * s, 0, 0)
    a = m.anim("attack", 1.0, "once")                       # se hincha antes de estallar
    for i in range(9):
        t = i / 8
        s = 1 + 0.25 * t + 0.08 * (i % 2)
        a.scl("body", t, s, 1 + 0.12 * t, s)
    a = m.anim("hurt", 0.3, "once")
    a.rest(0, ["head"])
    a.pose(0.08, {"head": (-15, 10, 0)})
    a.rest(0.3, ["head"])
    a = m.anim("spawn", 1.0, "once")
    a.pos("body", 0, 0, -20, 0)
    a.pos("body", 0.8, 0, 0, 0)
    a.rest(1.0)
    a = m.anim("death", 0.6, "hold")
    a.scl("body", 0, 1)
    a.scl("body", 0.3, 1.4)
    a.scl("body", 0.6, 0.05)
    return m


# ===========================================================================
# CHISPA VIVIENTE (SILVERFISH)
# ===========================================================================
def build_spark():
    m = _model("th_spark", 1518, atlas=128)
    root = m.root
    hb = m.bone("hitbox", (0, 3, 0), root)
    m.cube(hb, "hitbox", (-3, 0, -3), (3, 6, 3), "hitbox")
    m.bone("tag_name", (0, 10, 0), root)
    body = m.bone("body", (0, 3.4, 0), root)
    for j, (ax, ang) in enumerate(((None, 0), ("y", 45), ("x", 45))):
        m.cube(body, f"orb{j}", (-2.2, 1.2, -2.2), (2.2, 5.6, 2.2), "bolt" if j != 1 else "rune",
               rot=(ax, ang) if ax else None, pivot=(0, 3.4, 0), decor={"north": "spark_eyes"} if j == 0 else {})
    m.cube(body, "core", (-1.2, 2.2, -1.2), (1.2, 4.6, 1.2), "bolt_core")
    arcs = m.bone("arcs", (0, 3.4, 0), body)
    for k in range(6):
        a = 2 * math.pi * k / 6
        x, z = 3.4 * math.cos(a), 3.4 * math.sin(a)
        m.cube(arcs, f"leg{k}", (x - 0.25, 0, z - 0.25), (x + 0.25, 3.4, z + 0.25), "bolt", rot=("x", 22.5) if k % 2 else ("z", 22.5),
               pivot=(x, 3.4, z), decor={"all": "lightning"})
    m.ZERO_BONES = ["body", "arcs"]
    a = m.anim("idle", 1.0, "loop")
    FX.spin(a, "arcs", 1.0, 1)
    for i in range(5):
        a.scl("body", i / 4, 1 + 0.1 * (i % 2))
    a = m.anim("walk", 0.5, "loop")
    FX.spin(a, "arcs", 0.5, 1)
    for i in range(5):
        a.pos("body", 0.5 * i / 4, 0, 0.8 * (i % 2), 0)
    a = m.anim("attack", 0.5, "once")
    a.scl("body", 0, 1)
    a.scl("body", 0.15, 1.6)
    a.scl("body", 0.5, 1)
    a = m.anim("hurt", 0.3, "once")
    a.scl("body", 0, 1)
    a.scl("body", 0.1, 0.7)
    a.scl("body", 0.3, 1)
    a = m.anim("spawn", 0.6, "once")
    a.scl("body", 0, 0.1)
    a.scl("body", 0.4, 1.3)
    a.scl("body", 0.6, 1)
    a = m.anim("death", 0.6, "hold")
    a.scl("body", 0, 1)
    a.scl("body", 0.2, 1.8)
    a.scl("body", 0.6, 0.05)
    return m


# ===========================================================================
# CAMPO ESTATICO y NUBE DE TORMENTA (ARMOR_STAND)
# ===========================================================================
def build_field():
    m = _model("th_field", 1519)
    root = m.root
    m.bone("hitbox", (0, 0, 0), root)
    plate = m.bone("plate", (0, 0, 0), root)
    m.cube(plate, "plate", (-20, 0.1, -20), (20, 0.5, 20), "copper_dark", rot=("y", 45), pivot=(0, 0.3, 0),
           decor={"all": "lightning"})
    m.cube(plate, "plate2", (-16, 0.2, -16), (16, 0.6, 16), "copper", decor={"all": "lightning"})
    arcs = m.bone("arcs", (0, 0, 0), root)
    for k in range(4):
        a = 2 * math.pi * k / 4 + math.pi / 4
        x, z = 22 * math.cos(a), 22 * math.sin(a)
        m.cube(plate, f"coil{k}", (x - 1.6, 0, z - 1.6), (x + 1.6, 7, z + 1.6), "copper")
        m.cube(plate, f"coil_top{k}", (x - 2.0, 7, z - 2.0), (x + 2.0, 8.4, z + 2.0), "rune", rot=("y", 45), pivot=(x, 7.7, z))
        zigzag(m, arcs, f"arc{k}", x * 0.5, 7.5, z * 0.5, 7, seg=2.4, w=0.3)
    m.ZERO_BONES = ["plate", "arcs"]
    a = m.anim("idle", 1.0, "loop")
    for i in range(9):
        t = i / 8
        s = 1.0 if i % 3 else 0.05
        a.scl("arcs", t, s, s, s, i="linear")
        a.rot("arcs", t, 0, 40 * i, 0, i="linear")
    a = m.anim("spawn", 0.6, "once")
    a.scl("plate", 0, 0.05, 1, 0.05)
    a.scl("plate", 0.5, 1.1, 1, 1.1)
    a.scl("plate", 0.6, 1)
    return m


def build_cloud():
    m = _model("th_cloud", 1520)
    root = m.root
    m.bone("hitbox", (0, 0, 0), root)
    cloud = m.bone("cloud", (0, 48, 0), root)
    for i, (x, z, s, y) in enumerate(((0, 0, 9, 48), (-10, 4, 7, 46), (10, -3, 7.5, 47), (4, 10, 6, 46), (-5, -9, 6, 47),
                                      (-14, -6, 5, 45), (14, 8, 5, 45))):
        m.cube(cloud, f"puff{i}", (x - s, y - s * 0.55, z - s), (x + s, y + s * 0.55, z + s), "cloud" if i % 2 else "cloud_hi")
    bolts = m.bone("bolts", (0, 42, 0), cloud)
    for k, (x, z) in enumerate(((-6, 2), (5, -4), (1, 7))):
        zigzag(m, bolts, f"bolt{k}", x, 42, z, 40, seg=6, w=0.6)
    m.ZERO_BONES = ["cloud", "bolts"]
    a = m.anim("idle", 1.6, "loop")
    for i in range(9):
        t = 1.6 * i / 8
        s = 1.0 if i in (2, 3, 6) else 0.02
        a.scl("bolts", t, s, s, s, i="linear")
        a.rot("bolts", t, 0, 70 * i, 0, i="linear")
    for t, s in ((0, 0), (0.8, 1), (1.6, 0)):
        a.pos("cloud", t, 0, 1.2 * s, 0)
    a = m.anim("spawn", 0.8, "once")
    a.scl("cloud", 0, 0.1)
    a.scl("cloud", 0.7, 1.1)
    a.scl("cloud", 0.8, 1)
    return m


BUILDERS = {"thor": build_thor, "th_einherjar": build_einherjar, "th_creeper": build_storm_creeper, "th_spark": build_spark,
            "th_field": build_field, "th_cloud": build_cloud}
SHOTS = {
    "thor": [("idle", 0.6, -30), ("rest", 0, 150), ("attack", 0.15, -50), ("call", 0.6, -30)],
    "th_einherjar": [("idle", 0.5, -30), ("rest", 0, 150), ("attack", 0.15, -60), ("walk", 0.25, -70)],
    "th_creeper": [("idle", 0.5, -30), ("rest", 0, 150), ("attack", 0.8, -40), ("walk", 0.2, -80)],
    "th_spark": [("idle", 0.2, -30), ("rest", 0, 150), ("attack", 0.15, -40), ("walk", 0.2, -80)],
    "th_field": [("idle", 0.0, -30), ("idle", 0.25, -30), ("idle", 0.5, -30), ("spawn", 0.3, -30)],
    "th_cloud": [("idle", 0.0, -30), ("idle", 0.5, -30), ("idle", 0.7, -30), ("spawn", 0.4, -30)],
}
VIEW = {"thor": (32, 4.0), "th_spark": (4, 16.0), "th_field": (4, 4.0), "th_cloud": (26, 3.4), "th_creeper": (14, 9.0)}
ACTIONS = [("swing", 0.28, -40), ("throw", 0.4, -50), ("slam", 0.25, -40), ("absorb", 0.5, -30),
           ("nova", 0.2, -40), ("judgement", 0.6, -40), ("ragnarok", 1.0, -40), ("phase_change", 1.0, -30)]


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
            if name == "thor":
                FX.action_sheet(m, ACTIONS, PREVIEW / "thor_acciones.png", focus=32, scale=4.0)


if __name__ == "__main__":
    main()
