#!/usr/bin/env python3
"""
Boss 12 - LEVIATAN y sus subditos (modelos de ModelEngine).

  leviatan        rey del abismo: torso con escamas y coraza de coral, cabeza de dragon marino con
                  hocico largo, mandibula, aletas y corona de coral, aleta dorsal, aletas en los
                  antebrazos, cola de serpiente marina en lugar de piernas y tridente con perla
  lv_drowned      ahogado del abismo: marinero con algas, percebes, caparazon de tortuga y sable (DROWNED)
  lv_tide         espiritu de la marea: medusa luminosa con campana y tentaculos (ALLAY)
  lv_eel          anguila espectral: serpiente larga voladora con aletas (VEX)

Uso: python3 tools/b12_leviatan.py [modelo ...] [--no-preview]
"""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from bbmodel import Model  # noqa: E402
import anatomy as AN  # noqa: E402
import generate_minions as GM  # noqa: E402
import fxlib as FX  # noqa: E402
import b05_ragnarok as RG  # noqa: E402
import b11_azathoth as AZ  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent / "Modelos/12_Leviatan"
BLUEPRINTS = ROOT / "ModelEngine/blueprints"
PREVIEW = ROOT / "preview"

GLOW = (90, 255, 230)
MATS = {
    "scale": ((40, 110, 130), 8), "scale_dark": ((20, 60, 80), 7), "belly": ((150, 200, 190), 6), "fin": ((60, 170, 180), 6),
    "fin_dark": ((30, 100, 120), 6), "coral": ((230, 90, 110), 7), "coral_dark": ((150, 50, 80), 6), "gold": ((214, 176, 70), 7),
    "pearl": ((240, 240, 255), 3), "glow": (GLOW, 3), "teeth": ((236, 232, 214), 4), "mouth": ((60, 10, 30), 4),
    "skin": ((110, 150, 140), 7), "cloth": ((70, 80, 70), 8), "cloth_dark": ((40, 50, 46), 7), "kelp": ((50, 110, 50), 8),
    "shell": ((110, 120, 60), 7), "barnacle": ((200, 200, 180), 5), "iron": ((110, 120, 130), 6), "leather": ((92, 60, 36), 7),
    "jelly": ((120, 200, 255), 4), "jelly_dark": ((60, 120, 200), 5), "spectral": ((150, 240, 230), 5),
    "spectral_dark": ((60, 160, 170), 6), "ice": ((120, 230, 220), 5), "ice_dark": ((40, 140, 150), 6), "bone": ((214, 206, 186), 6),
    "hitbox": ((255, 255, 255), 0),
}


def sea_decor(m):
    D = m.decor

    @D
    def d_scales(f):
        for y in range(f.h):
            for x in range(f.w):
                if (x + (y // 2) * 2) % 4 == 0 and y % 2 == 0:
                    f.shade(x, y, 1.25)
                elif (x + (y // 2) * 2) % 4 == 2 and y % 2 == 1:
                    f.shade(x, y, 0.78)

    @D
    def d_fin(f):
        for x in range(0, f.w, 2):
            for y in range(f.h):
                f.shade(x, y, 0.8)
        for x in range(f.w):
            f.put(x, 0, (150, 240, 230))

    @D
    def d_coral(f):
        rng = random.Random(f.x0 + 5 * f.y0)
        for _ in range(max(1, f.w * f.h // 8)):
            f.shade(rng.randrange(f.w), rng.randrange(f.h), rng.choice((0.7, 1.3)))

    @D
    def d_sea_eyes(f):
        if f.name not in ("east", "west", "north"):
            return
        w, h = f.w, f.h
        if f.name == "north":
            for ex in (1, w - 4):
                f.rect(ex, 1, ex + 3, 3, (10, 30, 40))
                f.rect(ex + 1, 1, ex + 2, 2, GLOW)
        else:
            f.rect(1, 1, 4, 3, (10, 30, 40))
            f.put(2, 1, GLOW)

    @D
    def d_drowned_face(f):
        if f.name != "north":
            return
        w = f.w
        for ex in (2, w - 6):
            f.rect(ex, 6, ex + 4, 8, (20, 30, 30))
            f.rect(ex + 1, 6, ex + 3, 7, GLOW)
        f.rect(w // 2 - 3, 11, w // 2 + 3, 13, (30, 30, 30))
        for x in range(w // 2 - 3, w // 2 + 3, 2):
            f.put(x, 11, (220, 220, 200))

    @D
    def d_kelp(f):
        for x in range(0, f.w, 2):
            for y in range(f.h):
                if (y + x) % 3 == 0:
                    f.shade(x, y, 0.75)

    @D
    def d_barnacles(f):
        rng = random.Random(f.x0 * 3 + f.y0)
        for _ in range(max(1, f.w * f.h // 18)):
            x, y = rng.randrange(f.w), rng.randrange(f.h)
            f.put(x, y, (210, 210, 190))
            f.put(x + 1, y, (150, 150, 130))

    @D
    def d_jelly(f):
        for y in range(f.h):
            for x in range(f.w):
                if (x * 2 + y * 3) % 7 == 0:
                    f.shade(x, y, 1.3)

    @D
    def d_crystal(f):
        for y in range(f.h):
            f.put(0, y, (240, 255, 255))

    @D
    def d_wisp(f):
        for y in range(f.h):
            for x in range(f.w):
                if (x * 3 + y * 5) % 7 == 0:
                    f.shade(x, y, 1.2)


def _model(name, seed, atlas=256):
    m = Model(name, MATS, seed=seed, atlas_w=atlas)
    m.SHINE |= {"gold", "pearl", "glow", "jelly", "ice"}
    GM.add_common_decor(m)
    RG.norse_decor(m)
    AZ.void_decor(m)
    sea_decor(m)
    return m


SC = {"decor": {"all": "scales"}}
FN = {"decor": {"all": "fin"}}
CO = {"decor": {"all": "coral"}}


def coral_branch(m, bone, name, x, y, z, h, w=0.6, side=1, mat="coral"):
    """Rama de coral: tronco y dos brazos inclinados."""
    m.cube(bone, name, (x - w, y, z - w), (x + w, y + h, z + w), mat, **CO)
    m.cube(bone, name + "a", (x - w * 0.8, y + h * 0.4, z - w * 0.8), (x + w * 0.8, y + h * 0.9, z + w * 0.8), mat,
           rot=("z", -45 * side), pivot=(x, y + h * 0.4, z), **CO)
    m.cube(bone, name + "b", (x - w * 0.7, y + h * 0.55, z - w * 0.7), (x + w * 0.7, y + h * 1.05, z + w * 0.7), "coral_dark",
           rot=("z", 22.5 * side), pivot=(x, y + h * 0.55, z), **CO)


# ===========================================================================
# LEVIATAN
# ===========================================================================
def lv_head(m, hd):
    m.cube(hd, "skull", (-3.2, 25.0, -3.6), (3.2, 30.6, 3.2), "scale", **SC)
    m.cube(hd, "brow", (-3.4, 29.0, -4.6), (3.4, 30.8, -2.6), "scale_dark", rot=("x", 22.5), pivot=(0, 30, -3.6))
    m.cube(hd, "snout", (-2.2, 25.4, -9.0), (2.2, 28.8, -3.4), "scale", decor={"north": "sea_eyes", "all": "scales"})
    m.cube(hd, "snout_ridge", (-0.8, 28.4, -8.6), (0.8, 29.6, -3.0), "scale_dark", rot=("x", -22.5), pivot=(0, 29, -3.4))
    m.cube(hd, "upper_teeth", (-2.0, 24.8, -8.8), (2.0, 25.6, -3.8), "teeth")
    m.cube(hd, "eyes", (-3.3, 27.4, -5.2), (3.3, 28.6, -3.4), "glow")
    jw = m.bone("jaw", (0, 25.4, -2.8), hd)
    m.cube(jw, "jaw", (-2.0, 23.4, -8.4), (2.0, 25.4, -2.8), "belly", **SC)
    m.cube(jw, "lower_teeth", (-1.8, 25.2, -8.2), (1.8, 26.0, -4.0), "teeth")
    m.cube(jw, "jaw_mouth", (-1.6, 25.3, -7.8), (1.6, 25.5, -3.0), "mouth")
    for sx in (1, -1):
        m.cube(hd, f"gill_fin{sx}", (3.0 * sx - 0.3, 24.6, -2.6), (3.0 * sx + 0.3, 30.0, 2.6), "fin",
               rot=("y", 22.5 * sx), pivot=(3.0 * sx, 27, 2.6), **FN)
        m.cube(hd, f"ear_fin{sx}", (3.2 * sx - 0.25, 27.0, -0.6), (3.2 * sx + 0.25, 31.4, 4.4), "fin_dark",
               rot=("z", -22.5 * sx), pivot=(3.2 * sx, 28, 2), **FN)
    for i, (x, h, sd) in enumerate(((-2.4, 4.0, 1), (-0.8, 5.4, -1), (0.8, 5.0, 1), (2.4, 3.6, -1))):
        coral_branch(m, hd, f"crown{i}", x, 30.4, -1.0 + (i % 2), h, 0.5, sd)
    m.cube(hd, "crown_band", (-3.4, 30.0, -3.4), (3.4, 31.0, 3.0), "gold", decor={"all": "gold_band"} if "gold_band" in m.DECOR else {})
    m.cube(hd, "crown_pearl", (-0.7, 30.4, -3.9), (0.7, 31.8, -3.3), "pearl")


def build_leviatan():
    m = _model("leviatan", 1212, atlas=512)
    H = AN.humanoid(m, k=1.3, mats={"skin": "scale", "chest": "scale", "belly": "belly", "arm": "scale", "hand": "scale_dark",
                                     "thigh": "scale", "shin": "scale", "foot": "scale", "pelvis": "scale"}, head=lv_head)
    legs = {"right_leg", "left_leg", "right_lower_leg", "left_lower_leg"}
    m.CUBES = [c for c in m.CUBES if c.bone.name not in legs]
    for n in legs:                                         # sin piernas: la cola las sustituye
        m.BONES[n].children = [ch for ch in m.BONES[n].children if not hasattr(ch, "mat")]
    for c in m.CUBES:
        if c.mat == "scale":
            c.decor.setdefault("all", "scales")
    torso, waist, body = H["torso"], H["waist"], H["body"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    # coraza de coral, perla y hombreras
    m.cube(torso, "breastplate", (-4.8, 19.4, -4.2), (4.8, 23.8, -3.4), "coral_dark", **CO)
    m.cube(torso, "pearl", (-1.1, 20.2, -4.6), (1.1, 22.4, -4.0), "pearl", rot=("z", 45), pivot=(0, 21.3, -4.3))
    m.cube(torso, "belly_plates", (-3.4, 15.0, -3.5), (3.4, 18.6, -2.8), "belly", **SC)
    for side, sx, arm in (("r", 1, AR), ("l", -1, AL)):
        coral_branch(m, arm[0], f"pauldron_coral_{side}", 7.4 * sx, 24.0, 0, 4.0, 0.6, sx)
        m.cube(arm[0], f"pauldron_{side}", (4.2 * sx if sx > 0 else -10.2, 21.8, -3.4), (10.2 if sx > 0 else -4.2, 24.8, 3.4),
               "scale_dark", rot=("z", -22.5 * sx), pivot=(7.2 * sx, 23.3, 0), **SC)
        m.cube(arm[1], f"arm_fin_{side}", (8.0 * sx - 0.25, 11.0, -1.0), (8.0 * sx + 0.25, 17.0, 4.0), "fin",
               rot=("z", -22.5 * sx), pivot=(8.0 * sx, 17, 1.5), **FN)
        m.cube(arm[1], f"bracer_{side}", (4.7 * sx if sx > 0 else -8.3, 12.0, -2.2), (8.3 if sx > 0 else -4.7, 14.6, 2.2), "gold")
        for k, z in enumerate((-1.0, 0.0, 1.0)):
            m.cube(arm[2], f"claw_{side}{k}", (6.5 * sx - 0.3, 6.8, z - 0.3), (6.5 * sx + 0.3, 9.0, z + 0.3), "teeth",
                   rot=("x", -22.5), pivot=(6.5 * sx, 9, z))
    # aleta dorsal
    for i, (y, h) in enumerate(((23.0, 5.0), (19.8, 6.0), (16.6, 4.6))):
        m.cube(torso, f"dorsal{i}", (-0.3, y, 3.0), (0.3, y + h, 7.0), "fin", rot=("x", 22.5), pivot=(0, y, 3.4), **FN)
        m.cube(torso, f"dorsal_spine{i}", (-0.5, y, 3.2), (0.5, y + h + 1.2, 4.0), "scale_dark", rot=("x", 22.5),
               pivot=(0, y, 3.4))
    # faldon de escamas y cola de serpiente marina
    m.cube(waist, "hip_scales", (-5.4, 9.6, -3.6), (5.4, 14.6, 3.6), "scale_dark", **SC)
    m.cube(m.BONES["skirt_front"], "loin", (-3.0, 6.0, -4.2), (3.0, 13.6, -3.6), "fin", **FN)
    tail = []
    prev = waist
    segs = [((0, 9.6, 0.4), 4.6, 8.0, "down"), ((0, 1.6, 1.6), 4.0, 7.0, "back"), ((0, 1.6, 8.6), 3.4, 7.0, "back"),
            ((0, 1.6, 15.6), 2.8, 6.4, "back"), ((0, 1.6, 22.0), 2.0, 6.0, "back"), ((0, 1.6, 28.0), 1.4, 5.0, "back")]
    for i, ((x, y, z), w, L, kind) in enumerate(segs):
        b = m.bone(f"tail{i}", (x, y, z), prev)
        if kind == "down":
            m.cube(b, f"tail{i}", (-w, y - L, z - w * 0.8), (w, y + 1.0, z + w * 0.8), "scale", **SC)
            m.cube(b, f"tail{i}_belly", (-w * 0.7, y - L, z - w * 0.8 - 0.4), (w * 0.7, y, z - w * 0.8), "belly")
        else:
            m.cube(b, f"tail{i}", (-w, y - 1.6, z), (w, y - 1.6 + w * 1.5, z + L + 0.3), "scale", **SC)
            m.cube(b, f"tail{i}_fin", (-0.25, y - 1.6 + w * 1.5, z + 0.5), (0.25, y + w * 1.5 + 0.6, z + L - 0.5), "fin", **FN)
        tail.append(f"tail{i}")
        prev = b
    tb = m.bone("tail_fin", (0, 2.0, 33.0), prev)
    for sx in (1, -1):
        m.cube(tb, f"fluke{sx}", (min(0, 5 * sx), 0.8, 32.6), (max(0, 5 * sx), 1.6, 38.0), "fin", rot=("y", -22.5 * sx),
               pivot=(0, 1.2, 33), **FN)
    tail.append("tail_fin")
    # tridente
    tr = m.bone("trident", (6.5, 10.0, 0), AR[2])
    m.cube(tr, "shaft", (6.05, 9.55, -26.0), (6.95, 10.45, 9.0), "gold")
    m.cube(tr, "guard", (4.4, 9.4, -26.6), (8.6, 10.6, -25.6), "gold")
    for i, dx in enumerate((-1.8, 0.0, 1.8)):
        L = 6.0 if dx == 0 else 4.8
        m.cube(tr, f"prong{i}", (6.5 + dx - 0.4, 9.6, -26.4 - L), (6.5 + dx + 0.4, 10.4, -26.2), "gold")
        m.cube(tr, f"tip{i}", (6.5 + dx - 0.6, 9.4, -27.6 - L), (6.5 + dx + 0.6, 10.6, -26.0 - L), "glow", rot=("y", 45),
               pivot=(6.5 + dx, 10, -26.8 - L))
    m.cube(tr, "trident_pearl", (5.7, 9.2, -25.4), (7.3, 10.8, -23.8), "pearl")
    m.ZERO_BONES += tail + ["jaw", "trident"]

    def slither(a, length, amp=10, speed=1.0):
        steps = 8
        for k in range(steps + 1):
            t = length * k / steps
            for i, b in enumerate(tail[1:]):
                a.rot(b, t, 0, amp * (0.6 + 0.15 * i) * math.sin(2 * math.pi * k / steps * speed + i * 0.9), 0)

    def idle_x(a, t, s):
        a.rot("trident", t, -80, 0, 0)
        a.rot("jaw", t, 6 * s, 0, 0)

    a = GM.human_idle(m, arm_r=(-20, 0, 10), arm_l=(-15, 0, -14), extra=idle_x)
    slither(a, 2.4, 6)
    a = m.anim("walk", 1.2, "loop")
    for t, s in ((0, 1), (0.6, -1), (1.2, 1)):
        a.rot("torso", t, 8, 6 * s, 0)
        a.rot("h_head", t, -6, -4 * s, 0)
        a.rot("right_arm", t, -25, 0, 10)
        a.rot("left_arm", t, -10 + 15 * s, 0, -14)
        a.rot("trident", t, -80, 0, 0)
        a.rot("body", t, 0, -5 * s, 0)
    slither(a, 1.2, 18)

    def anim(name, length, keys, tail_amp=8):
        a = m.anim(name, length, "once")
        a.rest(0)
        for t, pose, lin in keys:
            a.pose(t, pose, i="linear" if lin else "catmullrom")
        a.rest(length)
        slither(a, length, tail_amp)
        return a

    anim("attack", 0.7, [(0.15, {"right_arm": (-160, 0, 15), "trident": (-90, 0, 0), "torso": (-8, 15, 0)}, False),
                         (0.3, {"right_arm": (-70, 0, -5), "trident": (-90, 0, 0), "torso": (20, -10, 0), "jaw": (30, 0, 0)},
                          True)])
    anim("curse", 1.0, [(0.25, {"left_arm": (-100, 0, -10), "jaw": (35, 0, 0), "h_head": (-10, 0, 0)}, False),
                        (0.45, {"left_arm": (-80, 0, -30), "jaw": (10, 0, 0), "torso": (-5, 10, 0)}, True)])
    lunge = {"right_arm": (-90, 0, 0), "trident": (-90, 0, 0), "torso": (30, 0, 0), "h_head": (-25, 0, 0), "jaw": (40, 0, 0),
             "body": {"p": (0, 2, -6)}}
    anim("lunge", 1.0, [(0.2, {"torso": (-10, 0, 0), "right_arm": (-120, 0, 20), "trident": (-90, 0, 0),
                               "body": {"p": (0, -2, 2)}}, False), (0.6, lunge, True), (0.75, lunge, False)], 20)
    whirl = {"right_arm": (-60, 0, 70), "left_arm": (-60, 0, -70), "trident": (-90, 0, 0), "h_head": (-20, 0, 0)}
    a = anim("whirlpool", 1.4, [(0.2, whirl, False), (1.0, whirl, False)], 16)
    FX.spin(a, "body", 1.2, 1)
    a.rot("body", 1.4, 0, 0, 0)
    anim("veil", 1.0, [(0.3, {"right_arm": (-100, -40, 0), "left_arm": (-100, 40, 0), "torso": (20, 0, 0),
                              "h_head": (20, 0, 0)}, False), (0.7, {"torso": (20, 0, 0)}, False)])
    nova = {"right_arm": (-175, 0, 5), "trident": (-90, 0, 0), "left_arm": (-120, 0, -40), "h_head": (-35, 0, 0),
            "jaw": (45, 0, 0), "body": {"p": (0, 3, 0)}}
    anim("nova", 1.3, [(0.35, nova, False), (0.5, {**nova, "right_arm": (-60, 0, 0), "body": {"p": (0, -1, 0)},
                                                   "torso": (30, 0, 0)}, True),
                       (0.9, {"right_arm": (-60, 0, 0), "trident": (-90, 0, 0), "torso": (30, 0, 0)}, False)], 20)
    anim("summon", 1.4, [(0.4, {**nova, "body": {"p": (0, 0, 0)}}, False), (1.0, nova, False)], 14)
    roar = {"right_arm": (-50, 0, 60), "left_arm": (-50, 0, -60), "trident": (-90, 0, 0), "h_head": (-40, 0, 0),
            "jaw": (50, 0, 0), "torso": (-15, 0, 0)}
    anim("phase_change", 1.8, [(0.5, {"torso": (40, 0, 0), "h_head": (25, 0, 0), "body": {"p": (0, -3, 0)}}, False),
                               (0.8, {"torso": (40, 0, 0), "h_head": (25, 0, 0), "body": {"p": (0, -3, 0)}}, False),
                               (1.2, roar, True), (1.5, roar, False)], 20)
    GM.human_hurt(m)
    a = m.anim("spawn", 2.0, "once")
    a.pos("body", 0, 0, -30, 0)
    a.pose(0, {"torso": (30, 0, 0), "h_head": (30, 0, 0)})
    a.pos("body", 1.0, 0, 2, 0)
    a.pos("body", 1.2, 0, 0, 0)
    a.pose(1.4, roar)
    a.rest(2.0)
    slither(a, 2.0, 20)
    a = m.anim("death", 2.4, "hold")
    a.rest(0)
    a.pose(0.5, roar)
    a.pose(1.4, {"torso": (40, 0, 20), "h_head": (30, 0, 0), "right_arm": (20, 0, 40), "left_arm": (20, 0, -40)})
    a.pos("body", 1.4, 0, -2, 0)
    a.pos("body", 2.4, 0, -28, 0)
    m.scale(1.45)
    return m


# ===========================================================================
# AHOGADO DEL ABISMO (DROWNED)
# ===========================================================================
def build_drowned():
    m = _model("lv_drowned", 1213)

    def head(m, hd):
        AN.default_head(m, hd, face="drowned_face", mat="skin")
        m.cube(hd, "shell", (-3.8, 29.0, -3.6), (3.8, 31.6, 3.8), "shell", decor={"all": "scales"})
        m.cube(hd, "shell_top", (-2.8, 31.0, -2.6), (2.8, 32.4, 2.8), "shell", rot=("y", 45), pivot=(0, 31.7, 0))
        for i, (x, z, ln) in enumerate(((-3.0, 2.0, 7.0), (0.0, 3.4, 8.5), (3.0, 2.0, 6.0), (-3.4, -1.0, 5.0), (3.4, -1.0, 4.4))):
            m.cube(hd, f"kelp{i}", (x - 0.5, 29.0 - ln, z - 0.4), (x + 0.5, 29.4, z + 0.4), "kelp", decor={"all": "kelp"},
                   rot=("x", 22.5) if i == 1 else None, pivot=(x, 29, z))

    H = AN.humanoid(m, k=1.0, mats={"skin": "skin", "chest": "cloth", "belly": "cloth", "arm": "skin", "thigh": "cloth_dark",
                                     "shin": "skin", "foot": "skin", "pelvis": "cloth_dark"}, head=head)
    for c in m.CUBES:
        if c.mat in ("cloth", "skin"):
            c.decor.setdefault("all", "barnacles")
    torso = H["torso"]
    AR = H["arms"]["right"]
    m.cube(torso, "rag", (-4.4, 15.0, -3.0), (4.4, 20.6, -2.4), "cloth_dark", rot=("z", 22.5), pivot=(0, 18, -2.7))
    m.cube(torso, "kelp_sash", (-0.6, 13.0, -3.2), (0.6, 24.0, -2.6), "kelp", rot=("z", -22.5), pivot=(0, 18, -2.9))
    m.cube(m.BONES["skirt_front"], "tatter", (-3.0, 8.0, -2.8), (3.0, 13.4, -2.3), "cloth_dark")
    sw = m.bone("sword", (6.5, 10.0, 0), AR[2])
    m.cube(sw, "grip", (6.1, 9.5, -2.0), (6.9, 10.5, 2.0), "leather")
    m.cube(sw, "guard", (5.6, 9.0, -2.8), (7.4, 11.0, -2.0), "iron")
    m.cube(sw, "blade", (6.2, 9.0, -13.0), (6.8, 11.4, -2.8), "iron", decor={"all": "barnacles"})
    m.cube(sw, "blade_tip", (6.25, 9.6, -15.0), (6.75, 11.4, -12.6), "iron", rot=("x", -22.5), pivot=(6.5, 10, -13))
    m.ZERO_BONES += ["sword"]
    GM.human_idle(m, arm_r=(-25, 0, 8), arm_l=(-60, 0, -8), extra=lambda a, t, s: (a.rot("sword", t, 50, 0, 0),
                                                                                    a.rot("torso", t, 10, 0, 0)))
    GM.human_walk(m, leg=22, arm=12, lean=10, arm_r=(-30, 0, 8), arm_l=(-80, 0, -8),
                  extra=lambda a, t, s: a.rot("sword", t, 50, 0, 0))
    a = m.anim("attack", 0.7, "once")
    a.rest(0)
    a.pose(0.15, {"right_arm": (-150, 0, 20), "sword": (40, 0, 0), "torso": (-5, 15, 0)})
    a.pose(0.3, {"right_arm": (-50, 0, -15), "sword": (0, 0, 0), "torso": (15, -15, 0)}, i="linear")
    a.rest(0.7)
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-60, 0, 40), "left_arm": (-60, 0, -40), "h_head": (-25, 0, 0)})
    GM.human_death(m)
    return m


# ===========================================================================
# ESPIRITU DE LA MAREA (ALLAY): medusa
# ===========================================================================
def build_tide():
    m = _model("lv_tide", 1214, atlas=128)
    root = m.root
    hb = m.bone("hitbox", (0, 6, 0), root)
    m.cube(hb, "hitbox", (-3, 2, -3), (3, 12, 3), "hitbox")
    m.bone("tag_name", (0, 16, 0), root)
    body = m.bone("body", (0, 9, 0), root)
    J = {"decor": {"all": "jelly"}}
    m.cube(body, "bell", (-3.6, 8.6, -3.6), (3.6, 12.4, 3.6), "jelly", **J)
    m.cube(body, "bell45", (-3.2, 8.4, -3.2), (3.2, 12.0, 3.2), "jelly_dark", rot=("y", 45), pivot=(0, 10, 0), **J)
    m.cube(body, "bell_top", (-2.4, 12.0, -2.4), (2.4, 13.8, 2.4), "jelly", rot=("y", 45), pivot=(0, 13, 0), **J)
    m.cube(body, "core", (-1.4, 9.4, -1.4), (1.4, 12.0, 1.4), "glow")
    m.cube(body, "rim", (-4.0, 8.2, -4.0), (4.0, 9.0, 4.0), "jelly_dark", **J)
    m.cube(body, "face", (-1.8, 10.0, -3.9), (1.8, 11.6, -3.5), "jelly", decor={"north": "sea_eyes"})
    tents = []
    for k in range(6):
        a = 2 * math.pi * k / 6
        x, z = 2.6 * math.cos(a), 2.6 * math.sin(a)
        tents.append(AZ.tentacle(m, body, f"t{k}_", (x, 8.4, z), n=3, L=2.2, w0=0.45, mats=("jelly", "spectral"), tip="glow"))
    m.ZERO_BONES = ["body"] + sum(tents, [])
    a = m.anim("idle", 1.6, "loop")
    for t, s in ((0, 0), (0.8, 1), (1.6, 0)):
        a.pos("body", t, 0, 1.0 * s, 0)
        a.scl("body", t, 1 + 0.08 * s, 1 - 0.08 * s, 1 + 0.08 * s)
    for k, bs in enumerate(tents):
        AZ.wave(a, bs, 1.6, 16, "x", k)
    a = m.anim("walk", 1.0, "loop")
    a.rot("body", 0, 15, 0, 0)
    a.rot("body", 1.0, 15, 0, 0)
    for k, bs in enumerate(tents):
        AZ.wave(a, bs, 1.0, 22, "x", k)
    a = m.anim("attack", 0.8, "once")
    a.scl("body", 0, 1)
    a.scl("body", 0.25, 1.35, 0.8, 1.35)
    a.scl("body", 0.45, 0.9, 1.15, 0.9)
    a.scl("body", 0.8, 1)
    a = m.anim("hurt", 0.3, "once")
    a.rot("body", 0, 0, 0, 0)
    a.rot("body", 0.08, -15, 0, 10)
    a.rot("body", 0.3, 0, 0, 0)
    a = m.anim("spawn", 1.0, "once")
    a.scl("body", 0, 0.1)
    a.scl("body", 0.6, 1.15)
    a.scl("body", 1.0, 1)
    a = m.anim("death", 1.0, "hold")
    a.scl("body", 0, 1)
    a.scl("body", 1.0, 1.8, 0.05, 1.8)
    return m


# ===========================================================================
# ANGUILA ESPECTRAL (VEX)
# ===========================================================================
def build_eel():
    m = _model("lv_eel", 1215, atlas=128)
    root = m.root
    hb = m.bone("hitbox", (0, 8, 0), root)
    m.cube(hb, "hitbox", (-3, 4, -6), (3, 12, 6), "hitbox")
    m.bone("tag_name", (0, 16, 0), root)
    body = m.bone("body", (0, 8, 0), root)
    W = {"decor": {"all": "wisp"}}
    hd = m.bone("head", (0, 8, -6), body)
    m.cube(hd, "head", (-1.8, 6.4, -11.0), (1.8, 9.6, -6.0), "spectral", decor={"north": "sea_eyes", "all": "wisp"})
    m.cube(hd, "snout", (-1.2, 6.6, -12.6), (1.2, 8.6, -10.8), "spectral_dark")
    jw = m.bone("eel_jaw", (0, 7.0, -6.4), hd)
    m.cube(jw, "jaw", (-1.4, 5.6, -11.8), (1.4, 7.0, -6.4), "spectral_dark")
    m.cube(jw, "fangs", (-1.0, 6.9, -11.6), (1.0, 7.6, -10.6), "teeth")
    for sx in (1, -1):
        m.cube(hd, f"gill{sx}", (1.8 * sx - 0.2, 6.6, -7.4), (1.8 * sx + 0.2, 9.4, -5.2), "glow", rot=("y", 22.5 * sx),
               pivot=(1.8 * sx, 8, -6.4))
    segs = []
    prev = body
    for i in range(6):
        z0 = -6.0 + i * 3.4
        w = 1.6 - i * 0.18
        b = m.bone(f"eel{i}", (0, 8, z0), prev)
        m.cube(b, f"eel{i}", (-w, 8 - w, z0), (w, 8 + w, z0 + 3.6), "spectral" if i % 2 == 0 else "spectral_dark", **W)
        m.cube(b, f"eel{i}_fin", (-0.2, 8 + w - 0.2, z0 + 0.2), (0.2, 8 + w + 1.6, z0 + 3.4), "glow" if i % 2 else "fin", **FN)
        segs.append(f"eel{i}")
        prev = b
    tf = m.bone("eel_tail", (0, 8, 14.4), prev)
    m.cube(tf, "eel_tail", (-0.2, 5.4, 14.4), (0.2, 10.6, 18.6), "fin", rot=("x", 22.5), pivot=(0, 8, 14.4), **FN)
    segs.append("eel_tail")
    m.ZERO_BONES = ["body", "head", "eel_jaw"] + segs

    def swim(a, length, amp):
        for k in range(9):
            t = length * k / 8
            for i, b in enumerate(segs):
                a.rot(b, t, 0, amp * math.sin(2 * math.pi * k / 8 + i * 0.9), 0)
            a.rot("head", t, 0, -amp * 0.6 * math.sin(2 * math.pi * k / 8 - 0.9), 0)

    a = m.anim("idle", 1.6, "loop")
    swim(a, 1.6, 14)
    for t, s in ((0, 0), (0.8, 1), (1.6, 0)):
        a.pos("body", t, 0, 0.8 * s, 0)
    a = m.anim("walk", 0.8, "loop")
    swim(a, 0.8, 24)
    a = m.anim("attack", 0.6, "once")
    a.rest(0)
    a.pose(0.15, {"head": (-20, 0, 0), "eel_jaw": (45, 0, 0), "body": {"p": (0, 0, 3)}})
    a.pose(0.3, {"head": (10, 0, 0), "eel_jaw": (0, 0, 0), "body": {"p": (0, 0, -6)}}, i="linear")
    a.rest(0.6)
    a = m.anim("hurt", 0.3, "once")
    a.rest(0, ["head"])
    a.pose(0.08, {"head": (-20, 20, 0)})
    a.rest(0.3, ["head"])
    a = m.anim("spawn", 1.0, "once")
    a.scl("body", 0, 0.1)
    a.scl("body", 0.6, 1.1)
    a.scl("body", 1.0, 1)
    a = m.anim("death", 1.0, "hold")
    a.scl("body", 0, 1)
    a.scl("body", 1.0, 1.6, 0.05, 1.6)
    return m


BUILDERS = {"leviatan": build_leviatan, "lv_drowned": build_drowned, "lv_tide": build_tide, "lv_eel": build_eel}
SHOTS = {
    "leviatan": [("idle", 0.6, -30), ("rest", 0, 150), ("attack", 0.15, -60), ("walk", 0.3, -80)],
    "lv_drowned": [("idle", 0.5, -30), ("rest", 0, 150), ("attack", 0.15, -60), ("walk", 0.25, -70)],
    "lv_tide": [("idle", 0.4, -30), ("rest", 0, 150), ("attack", 0.25, -40), ("walk", 0.2, -80)],
    "lv_eel": [("idle", 0.4, -40), ("rest", 0, 140), ("attack", 0.15, -70), ("walk", 0.2, -90)],
}
VIEW = {"leviatan": (30, 3.4), "lv_tide": (9, 14.0), "lv_eel": (8, 9.0)}
ACTIONS = [("curse", 0.45, -30), ("lunge", 0.6, -60), ("whirlpool", 0.6, -30), ("veil", 0.5, -30),
           ("nova", 0.35, -30), ("nova", 0.5, -30), ("summon", 0.6, -30), ("phase_change", 1.3, -30)]


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
            if name == "leviatan":
                FX.action_sheet(m, ACTIONS, PREVIEW / "leviatan_acciones.png", focus=30, scale=3.4)


if __name__ == "__main__":
    main()
