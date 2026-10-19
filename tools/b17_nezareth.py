#!/usr/bin/env python3
"""
Boss 17 - NEZARETH y sus subditos (modelos de ModelEngine).

  nezareth       la Tejedora Eterna: torso de mujer palida con tunica gris de seda, rostro con seis
                 ojos rojos, melena negra y corona de pinchos, garras-hoz y carretes de hilo en las
                 manos, sobre un cuerpo de arana gigante (cefalotorax, abdomen con reloj de arena y
                 telarana pintados, hileras y ocho patas en dos tramos)
  nz_puppet      marioneta de seda: munieco de madera con mascara de porcelana y la cruceta con los
                 hilos flotando encima (HUSK)
  nz_spinner     hilandera del destino: tunica con capucha, ojos cosidos, huso y tijeras enormes (VINDICATOR)
  nz_moth        polilla sombria: cuerpo peludo, alas grandes con ojos pintados y antenas (VEX)

Uso: python3 tools/b17_nezareth.py [modelo ...] [--no-preview]
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
import b11_azathoth as AZ  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent / "Modelos/17_Nezareth"
BLUEPRINTS = ROOT / "ModelEngine/blueprints"
PREVIEW = ROOT / "preview"

EYE = (230, 30, 40)
MATS = {
    "chitin": ((34, 30, 40), 5), "chitin_hi": ((70, 62, 80), 6), "pale": ((214, 206, 214), 5), "silk": ((226, 224, 232), 4),
    "silk_dark": ((140, 136, 150), 5), "robe": ((80, 76, 90), 6), "hair": ((20, 16, 24), 4), "eye": (EYE, 2),
    "bone": ((214, 206, 186), 6), "red": ((150, 20, 30), 5), "wood": ((130, 96, 64), 8), "wood_dark": ((80, 58, 40), 7),
    "porcelain": ((236, 232, 226), 3), "iron": ((110, 110, 120), 6), "fur": ((90, 80, 70), 9), "wing": ((120, 104, 90), 6),
    "wing_dark": ((60, 50, 44), 5), "gold": ((200, 160, 70), 7), "hitbox": ((255, 255, 255), 0),
}


def web_decor(m):
    D = m.decor

    @D
    def d_carapace(f):
        if f.name in ("up", "down"):
            return
        for y in range(f.h):
            k = 1.25 - 0.5 * y / max(1, f.h - 1)
            for x in range(f.w):
                f.shade(x, y, k)
        for x in range(f.w):
            f.put(x, 0, (110, 100, 120))

    @D
    def d_webpaint(f):
        """Telarana pintada con reloj de arena rojo en el abdomen."""
        w, h = f.w, f.h
        cx, cy = w // 2, h // 2
        for k in range(8):
            a = 2 * math.pi * k / 8
            for r in range(max(w, h)):
                x, y = round(cx + r * math.cos(a)), round(cy + r * math.sin(a))
                if 0 <= x < w and 0 <= y < h:
                    f.put(x, y, (120, 116, 130))
        for r in range(3, max(w, h), 4):
            for k in range(32):
                a = 2 * math.pi * k / 32
                x, y = round(cx + r * math.cos(a)), round(cy + r * math.sin(a))
                if 0 <= x < w and 0 <= y < h:
                    f.put(x, y, (100, 96, 110))
        if f.name == "up":
            for y in range(-3, 4):
                hw = abs(y) // 1
                f.rect(cx - hw, cy + y, cx + hw + 1, cy + y + 1, (170, 20, 30))

    @D
    def d_six_eyes(f):
        if f.name != "north":
            return
        w = f.w
        for (x, y, s) in ((2, 5, 2), (w - 4, 5, 2), (4, 3, 1), (w - 5, 3, 1), (3, 8, 1), (w - 4, 8, 1)):
            f.rect(x, y, x + s, y + s, EYE)
        f.rect(w // 2 - 2, 11, w // 2 + 2, 12, (90, 20, 30))

    @D
    def d_silk(f):
        for x in range(f.w):
            for y in range(f.h):
                if (x + 2 * y) % 5 == 0:
                    f.shade(x, y, 0.9)
                elif (2 * x + y) % 7 == 0:
                    f.shade(x, y, 1.08)

    @D
    def d_porcelain(f):
        if f.name != "north":
            return
        w = f.w
        for ex in (2, w - 5):
            f.rect(ex, 5, ex + 3, 7, (20, 20, 26))
        f.rect(w // 2 - 2, 10, w // 2 + 2, 11, (150, 20, 30))
        f.put(3, 9, (230, 140, 150))
        f.put(w - 4, 9, (230, 140, 150))
        f.rect(ex - 1, 7, ex, 10, (60, 60, 70))

    @D
    def d_stitched(f):
        if f.name != "north":
            return
        w = f.w
        for ex in (2, w - 6):
            f.rect(ex, 7, ex + 4, 8, (40, 30, 40))
            for i in range(0, 4, 2):
                f.put(ex + i, 6, (40, 30, 40))
                f.put(ex + i, 8, (40, 30, 40))

    @D
    def d_moth_wing(f):
        if f.name not in ("up", "down"):
            return
        w, h = f.w, f.h
        cx, cy = w // 2, h // 2
        for y in range(h):
            for x in range(w):
                if (x * 2 + y) % 6 == 0:
                    f.shade(x, y, 0.8)
        r = max(1, min(w, h) // 4)
        f.rect(cx - r, cy - r, cx + r, cy + r, (230, 200, 120))
        f.rect(cx - r // 2, cy - r // 2, cx + max(1, r // 2), cy + max(1, r // 2), (20, 16, 20))

    @D
    def d_crystal(f):
        for y in range(f.h):
            f.put(0, y, (255, 255, 255))


def _model(name, seed, atlas=256):
    m = Model(name, MATS, seed=seed, atlas_w=atlas)
    m.SHINE |= {"eye", "silk", "porcelain", "gold", "chitin_hi"}
    m.WOOD |= {"wood", "wood_dark"}
    GM.add_common_decor(m)
    RG.norse_decor(m)
    AZ.void_decor(m)
    web_decor(m)
    return m


CA = {"decor": {"all": "carapace"}}
SI = {"decor": {"all": "silk"}}


def spider_leg(m, parent, name, root, side, yaw, up=40, length=(9, 12), w=(1.2, 0.8)):
    """Pata de arana: tramo que sube hacia fuera y tramo que baja hasta el suelo."""
    x0, y0, z0 = root
    sx = 1 if side > 0 else -1
    hip = m.bone(name, root, parent, rotation=(0, yaw * sx, -up * sx))
    L1, L2 = length
    m.cube(hip, name + "_a", (min(x0, x0 + L1 * sx), y0 - w[0], z0 - w[0]), (max(x0, x0 + L1 * sx), y0 + w[0], z0 + w[0]),
           "chitin", **CA)
    m.cube(hip, name + "_joint", (x0 + L1 * sx - 1.2, y0 - 1.2, z0 - 1.2), (x0 + L1 * sx + 1.2, y0 + 1.2, z0 + 1.2), "chitin_hi",
           rot=("y", 45), pivot=(x0 + L1 * sx, y0, z0))
    knee = m.bone(name + "_knee", (x0 + L1 * sx, y0, z0), hip, rotation=(0, 0, (up + 70) * sx))
    m.cube(knee, name + "_b", (min(x0 + L1 * sx, x0 + (L1 + L2) * sx), y0 - w[1], z0 - w[1]),
           (max(x0 + L1 * sx, x0 + (L1 + L2) * sx), y0 + w[1], z0 + w[1]), "chitin", **CA)
    m.cube(knee, name + "_claw", (min(x0 + (L1 + L2) * sx, x0 + (L1 + L2 + 2) * sx), y0 - 0.4, z0 - 0.4),
           (max(x0 + (L1 + L2) * sx, x0 + (L1 + L2 + 2) * sx), y0 + 0.4, z0 + 0.4), "bone")
    return name, name + "_knee"


# ===========================================================================
# NEZARETH
# ===========================================================================
def nz_head(m, hd):
    m.cube(hd, "face", (-3.0, 25.0, -3.2), (3.0, 31.2, 3.0), "pale", decor={"north": "six_eyes"})
    m.cube(hd, "jaw", (-2.4, 24.2, -3.0), (2.4, 25.4, 1.0), "pale")
    for sx in (1, -1):
        m.cube(hd, f"mandible{sx}", (1.4 * sx - 0.35, 22.6, -3.4), (1.4 * sx + 0.35, 25.0, -2.8), "bone",
               rot=("z", 22.5 * sx), pivot=(1.4 * sx, 25, -3.1))
    m.cube(hd, "hair", (-3.6, 22.0, -1.0), (3.6, 31.8, 3.8), "hair", decor={"all": "braid"})
    m.cube(hd, "hair_back", (-3.0, 14.0, 2.6), (3.0, 22.4, 3.8), "hair", rot=("x", 22.5), pivot=(0, 22, 3.2), decor={"all": "braid"})
    for i, (x, h, ang) in enumerate(((-3.0, 4.0, 45), (-1.6, 5.4, 22.5), (0.0, 7.0, 0), (1.6, 5.4, -22.5), (3.0, 4.0, -45))):
        m.cube(hd, f"crown{i}", (x - 0.45, 31.0, -1.5), (x + 0.45, 31.0 + h, -0.6), "chitin_hi", rot=("z", ang) if ang else None,
               pivot=(x, 31, -1))
    m.cube(hd, "crown_gem", (-0.6, 30.6, -3.4), (0.6, 31.8, -2.9), "eye", rot=("z", 45), pivot=(0, 31.2, -3.1))


def build_nezareth():
    m = _model("nezareth", 1717, atlas=512)
    H = AN.humanoid(m, k=1.1, mats={"skin": "pale", "chest": "robe", "belly": "robe", "arm": "pale", "hand": "chitin",
                                     "thigh": "robe", "shin": "robe", "foot": "robe", "pelvis": "chitin"}, head=nz_head)
    legs = {"right_leg", "left_leg", "right_lower_leg", "left_lower_leg"}
    m.CUBES = [c for c in m.CUBES if c.bone.name not in legs]
    for n in legs:
        m.BONES[n].children = [ch for ch in m.BONES[n].children if not hasattr(ch, "mat")]
    torso, waist, body = H["torso"], H["waist"], H["body"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    # tunica de seda y cuello de telarana
    m.cube(torso, "bodice", (-4.4, 15.4, -3.0), (4.4, 22.8, 2.8), "silk_dark", **SI)
    m.cube(torso, "collar", (-5.0, 22.4, -3.2), (5.0, 24.6, 3.2), "chitin_hi", rot=("x", -22.5), pivot=(0, 23.5, 0), **CA)
    for i, ang in enumerate((-45, -22.5, 0, 22.5, 45)):
        m.cube(torso, f"ruff{i}", ((i - 2) * 1.6 - 0.8, 23.4, 2.0), ((i - 2) * 1.6 + 0.8, 29.4, 2.4), "silk",
               rot=("z", ang) if ang else None, pivot=((i - 2) * 0.6, 23.4, 2.2), decor={"all": "webpaint"})
    m.cube(torso, "brooch", (-1.0, 19.4, -3.5), (1.0, 21.4, -3.0), "eye", rot=("z", 45), pivot=(0, 20.4, -3.2))
    for side, sx, arm in (("r", 1, AR), ("l", -1, AL)):
        m.cube(arm[0], f"pad_{side}", (4.4 * sx if sx > 0 else -9.2, 21.8, -3.0), (9.2 if sx > 0 else -4.4, 24.4, 3.0), "chitin_hi",
               rot=("z", -22.5 * sx), pivot=(6.8 * sx, 23.1, 0), **CA)
        m.cube(arm[0], f"pad_spike_{side}", (7.6 * sx - 0.4, 24.0, -0.4), (7.6 * sx + 0.4, 27.4, 0.4), "chitin_hi",
               rot=("z", -22.5 * sx), pivot=(7.6 * sx, 24, 0))
        m.cube(arm[1], f"sleeve_{side}", (4.4 * sx if sx > 0 else -8.6, 11.0, -2.6), (8.6 if sx > 0 else -4.4, 16.0, 2.6), "silk",
               rot=("z", 22.5 * sx), pivot=(6.5 * sx, 16, 0), **SI)
        # garra-hoz
        sk = m.bone(f"sickle_{side}", (6.5 * sx, 9.0, 0), arm[2])
        m.cube(sk, f"sickle_{side}a", (6.5 * sx - 0.5, 1.0, -0.8), (6.5 * sx + 0.5, 9.0, 0.8), "chitin_hi", **CA)
        m.cube(sk, f"sickle_{side}b", (6.5 * sx - 0.4, -2.6, -3.6), (6.5 * sx + 0.4, 1.4, -1.6), "bone", rot=("x", 45),
               pivot=(6.5 * sx, 1.2, -0.8))
        m.cube(sk, f"thread_{side}", (6.5 * sx - 0.15, -14.0, -0.15), (6.5 * sx + 0.15, 1.0, 0.15), "silk")
    # cuerpo de arana
    sp = m.bone("spider", (0, 10, 4), body)
    m.cube(sp, "cephalo", (-5.6, 5.6, -3.0), (5.6, 12.6, 9.0), "chitin", **CA)
    m.cube(sp, "cephalo45", (-4.6, 5.0, -2.0), (4.6, 13.2, 8.0), "chitin_hi", rot=("y", 45), pivot=(0, 9, 3), **CA)
    ab = m.bone("abdomen", (0, 12, 9), sp)
    m.cube(ab, "abdomen", (-8.0, 7.0, 8.0), (8.0, 21.0, 26.0), "chitin", decor={"all": "webpaint"})
    m.cube(ab, "abdomen_x", (-7.0, 6.0, 10.0), (7.0, 22.0, 24.0), "chitin_hi", rot=("x", 45), pivot=(0, 14, 17), **CA)
    m.cube(ab, "abdomen_z", (-9.0, 8.0, 10.0), (9.0, 20.0, 24.0), "chitin", rot=("z", 45), pivot=(0, 14, 17), **CA)
    for sx in (1, -1):
        m.cube(ab, f"spinneret{sx}", (1.0 * sx - 0.6, 9.0, 25.4), (1.0 * sx + 0.6, 11.0, 28.4), "silk", rot=("x", 22.5),
               pivot=(sx, 10, 26))
    m.cube(ab, "silk_trail", (-0.3, 0.0, 27.4), (0.3, 10.0, 28.0), "silk")
    leg_bones = []
    for i, (z, yaw) in enumerate(((-2.0, 40), (1.6, 15), (5.2, -15), (8.6, -40))):
        for side in (1, -1):
            leg_bones.append(spider_leg(m, sp, f"leg{i}{'r' if side > 0 else 'l'}", (5.0 * side, 9.6, z), side, yaw,
                                        up=40, length=(10, 13)))
    m.ZERO_BONES += ["spider", "abdomen", "sickle_r", "sickle_l"]

    def legs_walk(a, length, amp=18):
        for k in range(5):
            t = length * k / 4
            s = math.sin(2 * math.pi * k / 4)
            for i, (hip, knee) in enumerate(leg_bones):
                ph = 1 if (i // 2 + i % 2) % 2 == 0 else -1
                side = 1 if hip.endswith("r") else -1
                yaw = (40, 15, -15, -40)[i // 2]
                a.rot(hip, t, 0, amp * s * ph, -12 * max(0, s * ph) * side)

    def legs_rest(a, t):
        for i, (hip, knee) in enumerate(leg_bones):
            side = 1 if hip.endswith("r") else -1
            yaw = (40, 15, -15, -40)[i // 2]
            a.rot(hip, t, 0, 0, 0)

    a = GM.human_idle(m, arm_r=(-30, 0, 10), arm_l=(-30, 0, -10),
                      extra=lambda a, t, s: (a.rot("abdomen", t, 4 * s - 2, 0, 0), a.rot("torso", t, 4, 0, 0)))
    legs_rest(a, 0)
    legs_rest(a, 2.4)
    a = m.anim("walk", 1.0, "loop")
    for t, s in ((0, 1), (0.5, -1), (1.0, 1)):
        a.rot("torso", t, 6, 4 * s, 0)
        a.rot("right_arm", t, -35, 0, 10)
        a.rot("left_arm", t, -35, 0, -10)
        a.rot("abdomen", t, 0, 5 * s, 0)
    for t, s in ((0, 0), (0.25, 1), (0.5, 0), (0.75, 1), (1.0, 0)):
        a.pos("body", t, 0, 0.6 * s, 0)
    legs_walk(a, 1.0)

    def anim(name, length, keys, legs_up=None):
        a = m.anim(name, length, "once")
        a.rest(0)
        legs_rest(a, 0)
        for t, pose, lin in keys:
            a.pose(t, pose, i="linear" if lin else "catmullrom")
        a.rest(length)
        if legs_up:
            for t, ang in legs_up:
                for i, (hip, knee) in enumerate(leg_bones[:2]):
                    side = 1 if hip.endswith("r") else -1
                    a.rot(hip, t, 0, 0, -(ang - 40) * side)
        legs_rest(a, length)
        return a

    claw_up = {"right_arm": (-150, 0, 30), "left_arm": (-150, 0, -30), "torso": (-10, 0, 0)}
    claw_down = {"right_arm": (-60, 0, -10), "left_arm": (-60, 0, 10), "torso": (25, 0, 0)}
    anim("attack", 0.7, [(0.15, {"right_arm": (-150, 0, 30), "torso": (-6, 15, 0)}, False),
                         (0.3, {"right_arm": (-60, 0, -10), "torso": (18, -12, 0)}, True)])
    anim("smash", 0.8, [(0.15, claw_up, False), (0.28, claw_down, True)], [(0.15, 80), (0.28, 30), (0.6, 40)])
    tug = {"right_arm": (-100, 40, 0), "left_arm": (-100, -40, 0), "torso": (-15, 0, 0), "h_head": (-15, 0, 0),
           "body": {"p": (0, 2, 0)}}
    stomp = {"right_arm": (-40, -30, 0), "left_arm": (-40, 30, 0), "torso": (20, 0, 0), "body": {"p": (0, -2, 0)}}
    anim("tug", 1.2, [(0.25, tug, False), (0.4, stomp, True), (0.8, stomp, False)], [(0.25, 90), (0.4, 20), (0.8, 40)])
    anim("throw", 1.1, [(0.3, {"right_arm": (-175, 0, 30), "left_arm": (-175, 0, -30), "torso": (-20, 0, 0)}, False),
                        (0.5, {"right_arm": (-70, 0, 10), "left_arm": (-70, 0, -10), "torso": (25, 0, 0)}, True)])
    a = anim("barrage", 1.2, [(0.3, {"torso": (30, 0, 0), "h_head": (20, 0, 0)}, False),
                              (0.6, {"torso": (35, 0, 0), "right_arm": (-30, 0, 40), "left_arm": (-30, 0, -40)}, False)])
    a.rot("abdomen", 0, 0, 0, 0)
    a.rot("abdomen", 0.4, -35, 0, 0)
    a.rot("abdomen", 0.7, -35, 0, 0)
    a.rot("abdomen", 1.2, 0, 0, 0)
    spread = {"right_arm": (-30, 0, 75), "left_arm": (-30, 0, -75), "torso": (-20, 0, 0), "h_head": (-30, 0, 0)}
    anim("nova", 0.9, [(0.15, spread, True), (0.5, spread, False)], [(0.15, 70), (0.5, 70), (0.8, 40)])
    weave = {"right_arm": (-90, 60, 0), "left_arm": (-90, -60, 0), "torso": (-5, 0, 0)}
    weave2 = {"right_arm": (-80, 20, 0), "left_arm": (-80, -20, 0), "torso": (-5, 0, 0)}
    anim("weave", 1.4, [(0.2, weave, False), (0.4, weave2, False), (0.6, weave, False), (0.8, weave2, False), (1.1, spread, False)])
    shriek = {"right_arm": (-60, 0, 50), "left_arm": (-60, 0, -50), "torso": (-15, 0, 0), "h_head": (-30, 0, 0),
              "body": {"p": (0, 2, 0)}}
    anim("roar", 1.6, [(0.3, {"torso": (25, 0, 0), "h_head": (15, 0, 0)}, False), (0.5, shriek, True), (1.1, shriek, False)],
         [(0.5, 90), (1.1, 90), (1.4, 40)])
    cocoon = {"right_arm": (-120, -50, 0), "left_arm": (-120, 50, 0), "torso": (25, 0, 0), "h_head": (25, 0, 0),
              "body": {"p": (0, -3, 0)}}
    anim("cocoon", 2.0, [(0.4, cocoon, False), (1.6, cocoon, False)])
    anim("summon", 1.4, [(0.3, weave, False), (0.6, weave2, False), (1.0, shriek, False)])
    anim("phase_change", 1.8, [(0.5, cocoon, False), (0.8, cocoon, False), (1.2, shriek, True), (1.5, shriek, False)],
         [(1.2, 90), (1.5, 90)])
    GM.human_hurt(m)
    a = m.anim("spawn", 2.0, "once")
    a.pos("body", 0, 0, 30, 0)
    a.pose(0, {"torso": (30, 0, 0), "h_head": (30, 0, 0), "right_arm": (-170, 0, 0), "left_arm": (-170, 0, 0)})
    a.pos("body", 1.0, 0, -1, 0)
    a.pos("body", 1.2, 0, 0, 0)
    a.pose(1.4, shriek)
    a.rest(2.0)
    legs_rest(a, 0)
    legs_rest(a, 2.0)
    a = m.anim("death", 2.4, "hold")
    a.rest(0)
    legs_rest(a, 0)
    a.pose(0.5, shriek)
    for i, (hip, knee) in enumerate(leg_bones):
        side = 1 if hip.endswith("r") else -1
        a.rot(hip, 1.6, 0, 0, -50 * side)
        a.rot(knee, 1.6, 0, 0, 80 * side)
    a.pose(1.6, {"torso": (40, 0, 0), "h_head": (30, 0, 0), "right_arm": (20, 0, 40), "left_arm": (20, 0, -40)})
    a.pos("body", 1.6, 0, -4, 0)
    a.pos("body", 2.4, 0, -5, 0)
    m.scale(1.4)
    return m


# ===========================================================================
# MARIONETA DE SEDA (HUSK)
# ===========================================================================
def build_puppet():
    m = _model("nz_puppet", 1718)

    def head(m, hd):
        m.cube(hd, "mask", (-3.0, 25.0, -3.0), (3.0, 31.0, 3.0), "porcelain", decor={"north": "porcelain"})
        m.cube(hd, "crack", (1.0, 27.0, -3.1), (1.4, 30.6, -2.9), "chitin")
        m.cube(hd, "hair", (-3.4, 29.4, -2.4), (3.4, 31.8, 3.4), "hair", decor={"all": "braid"})

    H = AN.humanoid(m, k=0.9, mats={"skin": "wood", "chest": "silk_dark", "belly": "wood", "arm": "wood", "hand": "wood_dark",
                                     "thigh": "wood", "shin": "wood", "foot": "wood_dark", "pelvis": "wood"}, head=head)
    torso = H["torso"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    for side, sx, arm in (("r", 1, AR), ("l", -1, AL)):
        m.cube(arm[1], f"elbow_peg_{side}", (6.5 * sx - 1.0, 16.6, -1.0), (6.5 * sx + 1.0, 18.0, 1.0), "wood_dark", rot=("y", 45),
               pivot=(6.5 * sx, 17.3, 0))
    m.cube(torso, "ruffle", (-4.0, 22.4, -3.0), (4.0, 24.0, 2.8), "silk", **SI)
    m.cube(torso, "buttons", (-0.5, 16.0, -3.2), (0.5, 22.0, -2.8), "red")
    ctrl = m.bone("control", (0, 42, 0), m.root)
    m.cube(ctrl, "bar_x", (-7.0, 41.4, -0.6), (7.0, 42.6, 0.6), "wood_dark")
    m.cube(ctrl, "bar_z", (-0.6, 41.4, -5.0), (0.6, 42.6, 5.0), "wood_dark")
    for i, (x, z, y0) in enumerate(((6.5, 0, 12.0), (-6.5, 0, 12.0), (0, -4.6, 30.0), (0, 4.6, 22.0))):
        m.cube(ctrl, f"string{i}", (x - 0.1, y0, z - 0.1), (x + 0.1, 41.4, z + 0.1), "silk")
    m.ZERO_BONES += ["control"]
    a = GM.human_idle(m, arm_r=(-10, 0, 20), arm_l=(-10, 0, -20),
                      extra=lambda a, t, s: (a.rot("h_head", t, 0, 0, 20 * s - 10), a.rot("control", t, 0, 0, 6 * s - 3)))
    a = GM.human_walk(m, leg=34, arm=30, bob=1.4, extra=lambda a, t, s: (a.rot("h_head", t, 0, 0, 15 * s),
                                                                          a.rot("control", t, 0, 0, 8 * s)))
    a = m.anim("attack", 0.7, "once")
    a.rest(0)
    a.pose(0.15, {"right_arm": (-170, 0, 30), "left_arm": (-170, 0, -30), "h_head": (0, 0, 30), "control": (0, 0, 15)})
    a.pose(0.3, {"right_arm": (-60, 0, -10), "left_arm": (-60, 0, 10), "torso": (25, 0, 0), "control": (0, 0, -10)}, i="linear")
    a.rest(0.7)
    GM.human_hurt(m)
    a = m.anim("spawn", 1.6, "once")
    a.pos("body", 0, 0, 20, 0)
    a.pose(0, {"torso": (40, 0, 0), "h_head": (40, 0, 30), "right_arm": (0, 0, 10), "left_arm": (0, 0, -10)})
    a.pos("body", 0.8, 0, 0, 0)
    a.rest(1.6)
    GM.human_death(m)
    return m


# ===========================================================================
# HILANDERA DEL DESTINO (VINDICATOR)
# ===========================================================================
def build_spinner():
    m = _model("nz_spinner", 1719)

    def head(m, hd):
        AN.default_head(m, hd, face="stitched", mat="pale")
        m.cube(hd, "hood", (-3.8, 24.4, -3.0), (3.8, 32.4, 3.8), "robe", **SI)
        m.cube_lr(hd, hd, "hood_side", (2.8, 24.0, -3.6), (3.9, 31.6, 3.4), "robe", rot=("z", -22.5), pivot=(3.3, 31.6, 0), **SI)
        m.cube(hd, "hood_peak", (-1.0, 31.6, -3.0), (1.0, 34.0, 2.0), "robe", rot=("x", -22.5), pivot=(0, 32.6, 0), **SI)

    H = AN.humanoid(m, k=0.9, mats={"skin": "pale", "chest": "robe", "belly": "robe", "arm": "robe", "hand": "pale",
                                     "thigh": "robe", "shin": "robe", "foot": "chitin", "pelvis": "robe"}, head=head)
    waist = H["waist"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    m.cube(waist, "skirt", (-4.8, 0.4, -3.2), (4.8, 13.4, 3.2), "robe", **SI)
    m.cube_lr(waist, waist, "skirt_flare", (4.2, 0.2, -3.0), (5.2, 8.6, 3.0), "silk_dark", rot=("z", 22.5), pivot=(4.7, 8.6, 0))
    m.cube(waist, "thread_belt", (-5.0, 12.4, -3.4), (5.0, 14.0, 3.4), "silk", **SI)
    sh = m.bone("shears", (6.5, 10.0, 0), AR[2])
    m.cube(sh, "blade_a", (6.2, 9.4, -15.0), (6.8, 10.6, -2.0), "iron", rot=("y", -22.5), pivot=(6.5, 10, -2.5))
    m.cube(sh, "ring_a", (5.6, 8.6, -2.0), (7.4, 11.4, 1.0), "gold")
    m.cube(sh, "pivot_bolt", (5.9, 9.4, -3.0), (7.1, 10.6, -2.0), "chitin_hi")
    m.cube(sh, "blade_b", (6.2, 9.0, -15.0), (6.8, 10.2, -2.0), "iron", rot=("y", 22.5), pivot=(6.5, 10, -2.5))
    sp = m.bone("spindle", (-6.5, 10.0, 0), AL[2])
    m.cube(sp, "spindle", (-6.9, 3.0, -0.4), (-6.1, 15.0, 0.4), "wood")
    m.cube(sp, "whorl", (-8.0, 4.0, -1.5), (-5.0, 5.2, 1.5), "wood_dark", rot=("y", 45), pivot=(-6.5, 4.6, 0))
    m.cube(sp, "yarn", (-7.6, 7.0, -1.1), (-5.4, 11.0, 1.1), "silk", **SI)
    m.ZERO_BONES += ["shears", "spindle"]
    GM.human_idle(m, arm_r=(-25, 0, 8), arm_l=(-40, 0, -8),
                  extra=lambda a, t, s: (a.rot("shears", t, 50, 0, 0), a.rot("spindle", t, 0, 90 * s, 0)))
    GM.human_walk(m, leg=20, arm=10, arm_r=(-30, 0, 8), arm_l=(-40, 0, -8),
                  extra=lambda a, t, s: a.rot("shears", t, 50, 0, 0))
    a = m.anim("attack", 0.7, "once")
    a.rest(0)
    a.pose(0.15, {"right_arm": (-100, 40, 0), "shears": (0, 0, 0), "torso": (-5, 15, 0)})
    a.pose(0.3, {"right_arm": (-90, -40, 0), "shears": (0, 0, 0), "torso": (15, -15, 0)}, i="linear")
    a.rest(0.7)
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-170, 0, 10), "shears": (70, 0, 0), "left_arm": (-150, 0, -10)})
    GM.human_death(m)
    return m


# ===========================================================================
# POLILLA SOMBRIA (VEX)
# ===========================================================================
def build_moth():
    m = _model("nz_moth", 1720, atlas=128)
    root = m.root
    hb = m.bone("hitbox", (0, 8, 0), root)
    m.cube(hb, "hitbox", (-3, 4, -3), (3, 12, 3), "hitbox")
    m.bone("tag_name", (0, 16, 0), root)
    body = m.bone("body", (0, 8, 0), root)
    F = {"decor": {"all": "fur"}}
    m.cube(body, "thorax", (-1.6, 6.4, -2.4), (1.6, 9.6, 1.0), "fur", **F)
    m.cube(body, "abdomen", (-1.2, 5.6, 0.6), (1.2, 8.4, 6.0), "fur", rot=("x", -22.5), pivot=(0, 7.5, 0.8), **F)
    m.cube(body, "head", (-1.2, 7.0, -4.0), (1.2, 9.4, -2.2), "fur", **F)
    m.cube(body, "eyes", (-1.3, 7.8, -4.1), (1.3, 8.8, -3.4), "eye")
    for sx in (1, -1):
        m.cube(body, f"antenna{sx}", (0.6 * sx - 0.15, 9.0, -4.0), (0.6 * sx + 0.15, 12.4, -3.6), "fur", rot=("z", -22.5 * sx),
               pivot=(0.6 * sx, 9, -3.8))
        m.cube(body, f"antenna_f{sx}", (0.6 * sx - 0.6, 10.4, -4.0), (0.6 * sx + 0.6, 12.0, -3.8), "wing", rot=("z", -22.5 * sx),
               pivot=(0.6 * sx, 9, -3.8))
    wings = []
    for side, sx in (("right", 1), ("left", -1)):
        w = m.bone(f"{side}_wing", (1.4 * sx, 9.0, -0.6), body)
        m.cube(w, f"{side}_fore", (min(1.4 * sx, 9.4 * sx), 8.8, -4.0), (max(1.4 * sx, 9.4 * sx), 9.2, 2.0), "wing",
               rot=("y", -22.5 * sx), pivot=(1.4 * sx, 9, -0.6), decor={"all": "moth_wing"})
        m.cube(w, f"{side}_hind", (min(1.4 * sx, 7.0 * sx), 8.7, 0.6), (max(1.4 * sx, 7.0 * sx), 9.1, 6.0), "wing_dark",
               rot=("y", 22.5 * sx), pivot=(1.4 * sx, 9, 0.6), decor={"all": "moth_wing"})
        wings.append(f"{side}_wing")
    m.ZERO_BONES = ["body"] + wings
    for name, length, amp in (("idle", 0.5, 45), ("walk", 0.3, 60)):
        a = m.anim(name, length, "loop")
        for k in range(5):
            t = length * k / 4
            s = math.sin(2 * math.pi * k / 4)
            a.rot("right_wing", t, 0, 0, amp * s)
            a.rot("left_wing", t, 0, 0, -amp * s)
            a.pos("body", t, 0, 0.5 * s, 0)
    a = m.anim("attack", 0.5, "once")
    a.rest(0, ["body"])
    a.pose(0.15, {"body": {"r": (-20, 0, 0), "p": (0, 1, 2)}})
    a.pose(0.3, {"body": {"r": (20, 0, 0), "p": (0, 0, -4)}}, i="linear")
    a.rest(0.5, ["body"])
    a = m.anim("hurt", 0.3, "once")
    a.rot("body", 0, 0, 0, 0)
    a.rot("body", 0.08, -15, 0, 15)
    a.rot("body", 0.3, 0, 0, 0)
    a = m.anim("spawn", 0.8, "once")
    a.scl("body", 0, 0.1)
    a.scl("body", 0.5, 1.2)
    a.scl("body", 0.8, 1)
    a = m.anim("death", 0.8, "hold")
    a.scl("body", 0, 1)
    a.scl("body", 0.8, 1.5, 0.05, 1.5)
    return m


BUILDERS = {"nezareth": build_nezareth, "nz_puppet": build_puppet, "nz_spinner": build_spinner, "nz_moth": build_moth}
SHOTS = {
    "nezareth": [("idle", 0.6, -40), ("rest", 0, 140), ("smash", 0.15, -50), ("walk", 0.25, -70)],
    "nz_puppet": [("idle", 0.5, -30), ("rest", 0, 150), ("attack", 0.15, -60), ("walk", 0.25, -70)],
    "nz_spinner": [("idle", 0.5, -30), ("rest", 0, 150), ("attack", 0.15, -60), ("walk", 0.25, -70)],
    "nz_moth": [("idle", 0.1, -30), ("rest", 0, 150), ("attack", 0.15, -40), ("walk", 0.1, -80)],
}
VIEW = {"nezareth": (28, 3.2), "nz_moth": (9, 13.0), "nz_puppet": (22, 7.5)}
ACTIONS = [("smash", 0.28, -40), ("tug", 0.25, -40), ("tug", 0.45, -40), ("throw", 0.3, -50),
           ("barrage", 0.6, -60), ("nova", 0.3, -30), ("cocoon", 1.0, -40), ("roar", 0.7, -30)]


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
            if name == "nezareth":
                FX.action_sheet(m, ACTIONS, PREVIEW / "nezareth_acciones.png", focus=28, scale=3.2)


if __name__ == "__main__":
    main()
