#!/usr/bin/env python3
"""
Boss 16 - KUKULKAN y sus subditos (modelos de ModelEngine).

  kukulkan       la Serpiente Emplumada: cabeza de serpiente con colmillos y plumas, penacho de
                 plumas de quetzal en abanico, disco solar a la espalda, collar y orejeras de jade
                 y oro, pechera escalonada, alas de plumas que se abren, cola de serpiente con
                 escamas y plumas en lugar de piernas, y baston solar
  kk_quetzal     quetzal espectral: pajaro verde con cola larga y alas que aletean (VEX)
  kk_serpent     sierpe solar: serpiente pequena con cresta de plumas (ENDERMITE)
  kk_offering    espiritu de la ofrenda: mascara de jade y oro con plumas y humo de copal (ALLAY)
  kk_jaguar      guerrero jaguar: casco de cabeza de jaguar, piel con manchas, macuahuitl y chimalli (VINDICATOR)

Uso: python3 tools/b16_kukulkan.py [modelo ...] [--no-preview]
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

ROOT = Path(__file__).resolve().parent.parent / "Modelos/16_Kukulkan"
BLUEPRINTS = ROOT / "ModelEngine/blueprints"
PREVIEW = ROOT / "preview"

SUN = (255, 210, 80)
MATS = {
    "scale": ((50, 140, 80), 8), "scale_dark": ((26, 80, 50), 7), "belly": ((220, 200, 120), 6), "feather": ((40, 180, 90), 7),
    "feather_dark": ((20, 110, 70), 6), "feather_red": ((200, 50, 40), 6), "feather_blue": ((40, 130, 200), 6),
    "jade": ((60, 190, 140), 5), "gold": ((225, 180, 60), 7), "sun": (SUN, 3), "teeth": ((240, 236, 220), 4),
    "mouth": ((120, 20, 30), 4), "stone": ((150, 140, 120), 7), "wood": ((100, 70, 44), 8), "obsidian": ((30, 20, 40), 3),
    "pelt": ((220, 160, 60), 8), "skin": ((150, 100, 70), 6), "cloth": ((230, 220, 190), 6), "copal": ((200, 200, 210), 6),
    "glow": ((255, 240, 150), 2), "red": ((180, 40, 40), 6), "white": ((240, 230, 200), 5), "hitbox": ((255, 255, 255), 0),
}


def aztec_decor(m):
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
    def d_feather(f):
        """Pluma: raquis claro en el centro y barbas en diagonal; punta mas oscura."""
        cx = f.w // 2
        for y in range(f.h):
            f.put(cx, y, (240, 240, 200))
            for x in range(f.w):
                if (x + y) % 3 == 0 and x != cx:
                    f.shade(x, y, 0.82)
        for y in range(max(0, f.h - 2), f.h):
            for x in range(f.w):
                f.shade(x, y, 0.6)

    @D
    def d_stepfret(f):
        """Greca escalonada mexica."""
        if f.name in ("up", "down"):
            return
        for x in range(f.w):
            f.put(x, 0, (225, 180, 60))
            f.put(x, f.h - 1, (225, 180, 60))
            k = x % 6
            y = 1 + (k if k < 3 else 5 - k)
            if y < f.h - 1:
                f.put(x, y, (60, 190, 140))

    @D
    def d_serpent_eyes(f):
        if f.name not in ("east", "west"):
            return
        f.rect(1, 1, 4, 3, (20, 10, 10))
        f.put(2, 1, SUN)
        f.put(3, 1, SUN)

    @D
    def d_sun_face(f):
        if f.name not in ("north", "south"):
            return
        w, h = f.w, f.h
        cx, cy = w // 2, h // 2
        for ex in (cx - 3, cx + 2):
            f.rect(ex, cy - 2, ex + 1, cy, (120, 60, 20))
        f.rect(cx - 2, cy + 2, cx + 2, cy + 3, (180, 40, 40))
        for k in range(16):
            a = 2 * math.pi * k / 16
            r = min(w, h) / 2 - 1
            f.put(round(cx + r * math.cos(a)), round(cy + r * math.sin(a)), (200, 120, 30))

    @D
    def d_spots(f):
        for y in range(1, f.h, 3):
            for x in range((y // 3) % 2 * 2, f.w, 4):
                f.rect(x, y, x + 2, y + 2, (60, 40, 20))
                f.put(x + 1, y + 1, (160, 100, 40))

    @D
    def d_jaguar_face(f):
        if f.name != "north":
            return
        w = f.w
        f.rect(1, 1, w - 1, 4, (60, 40, 20))
        for ex in (2, w - 5):
            f.rect(ex, 5, ex + 3, 7, (20, 15, 10))
            f.put(ex + 1, 5, SUN)
        f.rect(w // 2 - 2, 10, w // 2 + 2, 12, (100, 30, 30))

    @D
    def d_mask(f):
        if f.name != "north":
            return
        w, h = f.w, f.h
        for ex in (2, w - 5):
            f.rect(ex, h // 3, ex + 3, h // 3 + 2, (10, 40, 30))
            f.put(ex + 1, h // 3, (240, 230, 200))
        f.rect(w // 2 - 2, h * 2 // 3, w // 2 + 2, h * 2 // 3 + 2, (225, 180, 60))
        for x in range(0, w, 2):
            f.put(x, 0, (225, 180, 60))

    @D
    def d_obsidian(f):
        for x in range(0, f.w, 3):
            for y in range(f.h):
                f.put(x, y, (60, 50, 80))


def _model(name, seed, atlas=256):
    m = Model(name, MATS, seed=seed, atlas_w=atlas)
    m.SHINE |= {"gold", "jade", "sun", "glow", "obsidian"}
    m.WOOD |= {"wood"}
    GM.add_common_decor(m)
    RG.norse_decor(m)
    AZ.void_decor(m)
    aztec_decor(m)
    return m


SC = {"decor": {"all": "scales"}}
FE = {"decor": {"all": "feather"}}
SF = {"decor": {"all": "stepfret"}}


def plume(m, bone, name, x, y, z, length, w=0.9, ang=0.0, axis="z", mat="feather", tip="feather_blue"):
    """Pluma larga: tallo y punta de otro color, inclinada ang grados (multiplo de 22.5)."""
    rot = (axis, ang) if ang else None
    m.cube(bone, name, (x - w, y, z - 0.3), (x + w, y + length, z + 0.3), mat, rot=rot, pivot=(x, y, z), **FE)
    m.cube(bone, name + "_tip", (x - w * 0.8, y + length, z - 0.25), (x + w * 0.8, y + length + 2.0, z + 0.25), tip, rot=rot,
           pivot=(x, y, z), **FE)


def wing(m, parent, side, sx, root, span=1.0):
    """Ala de plumas: tres capas de plumas inclinadas desde la raiz."""
    x0, y0, z0 = root
    b = m.bone(f"{side}_wing", root, parent)
    m.cube(b, f"{side}_wing_arm", (min(x0, x0 + 9 * sx * span), y0 - 1.0, z0 - 0.6), (max(x0, x0 + 9 * sx * span), y0 + 1.0, z0 + 0.6),
           "feather_dark", rot=("z", 22.5 * sx), pivot=root, **FE)
    for i in range(6):
        x = x0 + sx * (1.6 + i * 1.6) * span
        ln = (9 + i * 1.6) * span
        ang = -22.5 * sx if i < 3 else -45 * sx
        mat = ("feather", "feather_dark", "feather_blue")[i % 3]
        m.cube(b, f"{side}_wf{i}", (x - 0.8, y0 - ln + 2 + i * 0.8, z0 - 0.3), (x + 0.8, y0 + 2 + i * 0.8, z0 + 0.3), mat,
               rot=("z", ang), pivot=(x, y0 + 2 + i * 0.8, z0), **FE)
    for i in range(5):
        x = x0 + sx * (1.2 + i * 1.8) * span
        m.cube(b, f"{side}_wc{i}", (x - 0.9 * span, y0 - 4 * span, z0 - 0.5), (x + 0.9 * span, y0 + 1.8 * span, z0 + 0.1),
               "feather_red", rot=("z", -22.5 * sx), pivot=(x, y0 + span, z0), **FE)
    return f"{side}_wing"


# ===========================================================================
# KUKULKAN
# ===========================================================================
def kk_head(m, hd):
    m.cube(hd, "skull", (-3.0, 25.0, -3.4), (3.0, 30.2, 3.0), "scale", **SC)
    m.cube(hd, "snout", (-2.2, 25.4, -9.2), (2.2, 28.8, -3.2), "scale", decor={"all": "scales", "east": "serpent_eyes",
                                                                             "west": "serpent_eyes"})
    m.cube(hd, "brow", (-2.6, 28.0, -7.0), (2.6, 29.6, -2.6), "scale_dark", rot=("x", -22.5), pivot=(0, 28.8, -3.0))
    m.cube(hd, "eyes", (-2.4, 27.2, -6.4), (2.4, 28.2, -5.0), "sun")
    m.cube(hd, "upper_fangs", (-1.8, 24.4, -8.8), (1.8, 25.6, -7.8), "teeth")
    jw = m.bone("jaw", (0, 25.4, -2.8), hd)
    m.cube(jw, "jaw", (-2.0, 23.4, -8.6), (2.0, 25.4, -2.8), "belly", **SC)
    m.cube(jw, "jaw_mouth", (-1.6, 25.3, -8.0), (1.6, 25.5, -3.0), "mouth")
    m.cube(jw, "tongue", (-0.3, 24.8, -11.0), (0.3, 25.2, -8.0), "red")
    for sx in (1, -1):
        m.cube(jw, f"fang{sx}", (1.4 * sx - 0.35, 24.6, -8.6), (1.4 * sx + 0.35, 26.6, -8.0), "teeth")
        m.cube(hd, f"earspool{sx}", (3.0 * sx - 0.4, 26.0, -1.2), (3.0 * sx + 0.4, 28.4, 1.2), "jade")
        m.cube(hd, f"earspool_ring{sx}", (3.1 * sx - 0.3, 25.6, -1.6), (3.1 * sx + 0.3, 28.8, 1.6), "gold", rot=("x", 45),
               pivot=(3.1 * sx, 27.2, 0))
        for i in range(3):                                     # plumas en las mejillas
            plume(m, hd, f"cheek{sx}{i}", 3.0 * sx, 24.6, -2.0 + i * 1.4, 3.6 - i * 0.4, 0.5, -45 * sx if i else -22.5 * sx)
    # penacho de plumas de quetzal en abanico
    m.cube(hd, "band", (-3.4, 29.8, -3.6), (3.4, 31.0, 3.2), "gold", **SF)
    m.cube(hd, "band_jade", (-1.0, 30.0, -3.9), (1.0, 31.6, -3.4), "jade")
    for i, ang in enumerate((-45, -22.5, 0, 22.5, 45)):
        for j, (dz, ln, mat, tip) in enumerate(((1.2, 12.0, "feather", "feather_blue"), (2.0, 9.0, "feather_red", "gold"))):
            plume(m, hd, f"crest{i}{j}", (i - 2) * 1.0, 30.4, dz, ln, 0.9, ang, "z", mat, tip)


def build_kukulkan():
    m = _model("kukulkan", 1616, atlas=512)
    H = AN.humanoid(m, k=1.2, mats={"skin": "scale", "chest": "scale", "belly": "belly", "arm": "scale", "hand": "scale_dark",
                                     "thigh": "scale", "shin": "scale", "foot": "scale", "pelvis": "scale"}, head=kk_head)
    legs = {"right_leg", "left_leg", "right_lower_leg", "left_lower_leg"}
    m.CUBES = [c for c in m.CUBES if c.bone.name not in legs]
    for n in legs:
        m.BONES[n].children = [ch for ch in m.BONES[n].children if not hasattr(ch, "mat")]
    for c in m.CUBES:
        if c.mat == "scale":
            c.decor.setdefault("all", "scales")
    torso, waist = H["torso"], H["waist"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    # collar y pectoral escalonado de jade y oro
    m.cube(torso, "collar", (-5.2, 21.8, -4.2), (5.2, 24.4, 3.8), "jade", rot=("x", -22.5), pivot=(0, 23, 0), **SF)
    m.cube(torso, "pectoral", (-4.2, 17.4, -3.9), (4.2, 21.8, -3.2), "gold", **SF)
    m.cube(torso, "pectoral_sun", (-1.6, 18.0, -4.4), (1.6, 21.2, -3.8), "sun", rot=("z", 45), pivot=(0, 19.6, -4.1))
    m.cube(waist, "loincloth_belt", (-5.4, 12.6, -3.6), (5.4, 14.8, 3.6), "gold", **SF)
    m.cube(m.BONES["skirt_front"], "loincloth", (-2.8, 4.0, -4.0), (2.8, 13.0, -3.4), "cloth", **SF)
    for side, sx, arm in (("r", 1, AR), ("l", -1, AL)):
        m.cube(arm[0], f"pauldron_{side}", (4.4 * sx if sx > 0 else -9.4, 22.0, -3.2), (9.4 if sx > 0 else -4.4, 24.6, 3.2),
               "gold", rot=("z", -22.5 * sx), pivot=(6.9 * sx, 23.3, 0), **SF)
        for i in range(3):
            plume(m, arm[0], f"shoulder_plume_{side}{i}", 8.6 * sx, 21.0, -1.6 + i * 1.6, 4.0, 0.6, -45 * sx)
        m.cube(arm[1], f"bracer_{side}", (4.8 * sx if sx > 0 else -8.2, 12.0, -2.2), (8.2 if sx > 0 else -4.8, 14.8, 2.2), "jade",
               **SF)
    # disco solar a la espalda y alas de plumas
    sun = m.bone("sun_disc", (0, 27, 5.6), torso)
    KR.ring(m, sun, "sun_ring", 0, 27, 5.2, 6.0, 9.0, "gold", n=16, t=1.6)
    KR.ring(m, sun, "sun_ring2", 0, 27, 5.4, 5.8, 6.0, "jade", n=16, t=1.0)
    m.cube(sun, "sun_core", (-2.6, 24.4, 5.3), (2.6, 29.6, 5.9), "sun", rot=("z", 45), pivot=(0, 27, 5.6))
    for k in range(16):
        a = 2 * math.pi * k / 16
        r0 = 10.0
        ln = 4.0 if k % 2 == 0 else 2.4
        x, y = (r0 + ln / 2) * math.cos(a), 27 + (r0 + ln / 2) * math.sin(a)
        ang = (math.degrees(a) + 90) % 180
        ang = ang - 180 if ang >= 90 else ang
        snap = round(ang / 22.5) * 22.5
        if abs(snap) <= 45:
            frm, to = (x - 0.7, y - ln / 2, 5.4), (x + 0.7, y + ln / 2, 5.8)
            rot = -snap + 0.0
        else:
            snap = snap - 90 if snap > 0 else snap + 90
            frm, to = (x - ln / 2, y - 0.7, 5.4), (x + ln / 2, y + 0.7, 5.8)
            rot = -snap + 0.0
        rot = max(-45, min(45, rot))
        m.cube(sun, f"ray{k}", frm, to, "glow" if k % 2 == 0 else "sun", rot=("z", rot) if rot else None, pivot=(x, y, 5.6))
    wings = [wing(m, torso, "right", 1, (3.0, 23.0, 4.6), 1.5), wing(m, torso, "left", -1, (-3.0, 23.0, 4.6), 1.5)]
    # cola de serpiente
    tail, prev = [], waist
    segs = [((0, 9.6, 0.4), 4.4, 8.0, "down"), ((0, 1.6, 1.6), 3.8, 7.0, "back"), ((0, 1.6, 8.6), 3.2, 7.0, "back"),
            ((0, 1.6, 15.6), 2.6, 6.4, "back"), ((0, 1.6, 22.0), 2.0, 6.0, "back"), ((0, 1.6, 28.0), 1.4, 5.0, "back")]
    for i, ((x, y, z), w, L, kind) in enumerate(segs):
        b = m.bone(f"tail{i}", (x, y, z), prev)
        if kind == "down":
            m.cube(b, f"tail{i}", (-w, y - L, z - w * 0.8), (w, y + 1.0, z + w * 0.8), "scale", **SC)
            m.cube(b, f"tail{i}_belly", (-w * 0.7, y - L, z - w * 0.8 - 0.4), (w * 0.7, y, z - w * 0.8), "belly")
        else:
            m.cube(b, f"tail{i}", (-w, y - 1.6, z), (w, y - 1.6 + w * 1.5, z + L + 0.3), "scale", **SC)
            plume(m, b, f"tail{i}_plume", 0, y - 1.6 + w * 1.5, z + L * 0.5, 2.8 - i * 0.3, 0.5, -22.5, "x")
        tail.append(f"tail{i}")
        prev = b
    tb = m.bone("tail_fan", (0, 2.0, 33.0), prev)
    for i, ang in enumerate((-45, -22.5, 0, 22.5, 45)):
        plume(m, tb, f"tail_fan{i}", 0, 1.6, 33.0, 8.0, 0.8, ang, "y", ("feather", "feather_blue", "feather_red")[i % 3], "gold")
    tail.append("tail_fan")
    # baston solar
    st = m.bone("staff", (6.5, 10.0, 0), AR[2])
    m.cube(st, "shaft", (6.05, 9.55, -18.0), (6.95, 10.45, 8.0), "wood")
    m.cube(st, "wrap", (5.8, 9.3, -4.0), (7.2, 10.7, -1.0), "jade")
    m.cube(st, "staff_sun", (5.9, 6.0, -25.0), (7.1, 14.0, -17.0), "sun", decor={"all": "sun_face"})
    m.cube(st, "staff_sun45", (6.0, 6.6, -24.4), (7.0, 13.4, -17.6), "gold", rot=("x", 45), pivot=(6.5, 10, -21))
    for i, ang in enumerate((-22.5, 0, 22.5)):
        plume(m, st, f"staff_plume{i}", 6.5 + (i - 1) * 0.8, 10.0, -17.0, 4.0, 0.5, ang)
    m.ZERO_BONES += tail + wings + ["jaw", "staff", "sun_disc"]

    def slither(a, length, amp=10):
        for k in range(9):
            t = length * k / 8
            for i, b in enumerate(tail[1:]):
                a.rot(b, t, 0, amp * (0.6 + 0.15 * i) * math.sin(2 * math.pi * k / 8 + i * 0.9), 0)

    def flap(a, length, amp=10, base=0):
        for k in range(5):
            t = length * k / 4
            s = math.sin(2 * math.pi * k / 4)
            a.rot("right_wing", t, 0, -base - amp * s, base * 0.4)
            a.rot("left_wing", t, 0, base + amp * s, -base * 0.4)

    def idle_x(a, t, s):
        a.rot("staff", t, -80, 0, 0)
        a.rot("jaw", t, 6 * s, 0, 0)

    a = GM.human_idle(m, arm_r=(-20, 0, 10), arm_l=(-15, 0, -14), extra=idle_x)
    slither(a, 2.4, 6)
    flap(a, 2.4, 6)
    FX.spin(a, "sun_disc", 2.4, 0.25, "z")
    a = m.anim("walk", 1.2, "loop")
    for t, s in ((0, 1), (0.6, -1), (1.2, 1)):
        a.rot("torso", t, 8, 6 * s, 0)
        a.rot("right_arm", t, -25, 0, 10)
        a.rot("left_arm", t, -10 + 15 * s, 0, -14)
        a.rot("staff", t, -80, 0, 0)
    slither(a, 1.2, 18)
    flap(a, 1.2, 10)

    def anim(name, length, keys, wings_open=0, tail_amp=8, spin=0.0):
        a = m.anim(name, length, "once")
        a.rest(0)
        for t, pose, lin in keys:
            a.pose(t, pose, i="linear" if lin else "catmullrom")
        a.rest(length)
        slither(a, length, tail_amp)
        flap(a, length, 14 if wings_open else 6, wings_open)
        if spin:
            FX.spin(a, "sun_disc", length, spin, "z")
        return a

    anim("attack", 0.7, [(0.15, {"right_arm": (-160, 0, 15), "staff": (-90, 0, 0), "torso": (-8, 15, 0)}, False),
                         (0.3, {"right_arm": (-70, 0, -5), "staff": (-60, 0, 0), "torso": (20, -10, 0), "jaw": (30, 0, 0)},
                          True)])
    screech = {"h_head": (-35, 0, 0), "jaw": (50, 0, 0), "torso": (-15, 0, 0), "right_arm": (-40, 0, 60),
               "left_arm": (-40, 0, -60), "staff": (-80, 0, 0)}
    anim("screech", 1.0, [(0.18, screech, True), (0.6, screech, False)], 40, 14)
    wrap = {"right_arm": (-110, -50, 0), "left_arm": (-110, 50, 0), "torso": (20, 0, 0), "h_head": (20, 0, 0)}
    a = anim("eclipse", 1.0, [(0.3, wrap, False), (0.7, wrap, False)])
    for k in range(5):
        t = k / 4
        a.rot("right_wing", t, 0, 60 if 0 < k < 4 else 0, 0)
        a.rot("left_wing", t, 0, -60 if 0 < k < 4 else 0, 0)
    anim("siphon", 1.0, [(0.2, {"left_arm": (-95, 0, 0), "jaw": (30, 0, 0)}, False),
                         (0.4, {"left_arm": (-60, 0, -10), "torso": (-8, 0, 0), "jaw": (40, 0, 0)}, True),
                         (0.7, {"left_arm": (-55, 0, -10), "torso": (-8, 0, 0)}, False)], 20)
    point = {"right_arm": (-100, 0, 0), "staff": (-10, 0, 0), "h_head": (0, -8, 0)}
    anim("mark", 1.4, [(0.3, point, False), (1.1, point, False),
                       (1.2, {"right_arm": (-130, 0, 10), "staff": (-40, 0, 0)}, True)], 0, 8, 1.0)
    anim("venom", 1.0, [(0.3, {"h_head": (25, 0, 0), "jaw": (20, 0, 0), "torso": (20, 0, 0)}, False),
                        (0.5, {**screech, "h_head": (-10, 0, 0)}, True)], 30, 20)
    rise = {**screech, "body": {"p": (0, 5, 0)}, "staff": (-170, 0, 0), "right_arm": (-170, 0, 0)}
    anim("solar", 1.4, [(0.45, {**rise, "body": {"p": (0, 3, 0)}}, False), (0.6, rise, True), (1.0, rise, False)], 50, 20, 2.0)
    call = {"right_arm": (-178, 0, 5), "staff": (-90, 0, 0), "left_arm": (-60, 0, -60), "h_head": (-25, 0, 0)}
    anim("storm", 1.4, [(0.3, call, False), (1.1, call, False)], 30, 10, 3.0)
    anim("summon", 1.4, [(0.35, call, False), (1.0, call, False)], 30, 10, 1.0)
    anim("phase_change", 1.8, [(0.5, {"torso": (40, 0, 0), "h_head": (25, 0, 0), "body": {"p": (0, -3, 0)}}, False),
                               (0.8, {"torso": (40, 0, 0), "h_head": (25, 0, 0), "body": {"p": (0, -3, 0)}}, False),
                               (1.2, screech, True), (1.5, screech, False)], 50, 20, 3.0)
    GM.human_hurt(m)
    a = m.anim("spawn", 2.0, "once")
    a.pos("body", 0, 0, -30, 0)
    a.pose(0, {"torso": (30, 0, 0), "h_head": (30, 0, 0)})
    a.pos("body", 1.0, 0, 2, 0)
    a.pos("body", 1.2, 0, 0, 0)
    a.pose(1.4, screech)
    a.rest(2.0)
    slither(a, 2.0, 20)
    flap(a, 2.0, 20, 40)
    a = m.anim("death", 2.4, "hold")
    a.rest(0)
    a.pose(0.5, screech)
    a.pose(1.4, {"torso": (40, 0, 20), "h_head": (30, 0, 0), "right_arm": (20, 0, 40), "left_arm": (20, 0, -40)})
    a.pos("body", 1.4, 0, -2, 0)
    a.pos("body", 2.4, 0, -28, 0)
    m.scale(1.45)
    return m


# ===========================================================================
# QUETZAL ESPECTRAL (VEX)
# ===========================================================================
def build_quetzal():
    m = _model("kk_quetzal", 1617, atlas=128)
    root = m.root
    hb = m.bone("hitbox", (0, 8, 0), root)
    m.cube(hb, "hitbox", (-3, 4, -3), (3, 12, 3), "hitbox")
    m.bone("tag_name", (0, 16, 0), root)
    body = m.bone("body", (0, 8, 0), root)
    m.cube(body, "breast", (-1.8, 6.0, -2.6), (1.8, 9.6, 1.6), "feather_red", **FE)
    m.cube(body, "back", (-2.0, 7.6, -2.2), (2.0, 10.4, 2.6), "feather", **FE)
    hd = m.bone("head", (0, 10, -2.0), body)
    m.cube(hd, "head", (-1.4, 9.6, -4.4), (1.4, 12.4, -1.6), "feather", decor={"all": "feather", "east": "serpent_eyes",
                                                                                "west": "serpent_eyes"})
    m.cube(hd, "beak", (-0.5, 10.4, -5.6), (0.5, 11.2, -4.2), "gold", rot=("x", 22.5), pivot=(0, 10.8, -4.4))
    m.cube(hd, "crest", (-0.4, 12.0, -3.8), (0.4, 13.6, -1.0), "feather_dark", rot=("x", 22.5), pivot=(0, 12, -2))
    tl = m.bone("tail", (0, 8, 2.4), body)
    for i, dx in enumerate((-0.6, 0.6)):
        m.cube(tl, f"tail{i}", (dx - 0.5, 7.6, 2.4), (dx + 0.5, 8.2, 14.0 - i * 2), "feather", rot=("x", -22.5),
               pivot=(dx, 8, 2.4), **FE)
    wings = [wing(m, body, "right", 1, (1.6, 9.4, 0.2), 0.35), wing(m, body, "left", -1, (-1.6, 9.4, 0.2), 0.35)]
    m.ZERO_BONES = ["body", "head", "tail"] + wings
    a = m.anim("idle", 0.6, "loop")
    for k in range(5):
        t = 0.6 * k / 4
        s = math.sin(2 * math.pi * k / 4)
        a.rot("right_wing", t, 0, 0, 40 * s)
        a.rot("left_wing", t, 0, 0, -40 * s)
        a.pos("body", t, 0, 0.6 * s, 0)
        a.rot("tail", t, 6 * s, 0, 0)
    a = m.anim("walk", 0.4, "loop")
    for k in range(5):
        t = 0.4 * k / 4
        s = math.sin(2 * math.pi * k / 4)
        a.rot("right_wing", t, 0, 0, 55 * s)
        a.rot("left_wing", t, 0, 0, -55 * s)
        a.rot("body", t, 15, 0, 0)
    a = m.anim("attack", 0.5, "once")
    a.rest(0, ["body", "head"])
    a.pose(0.15, {"head": (-30, 0, 0), "body": {"r": (-10, 0, 0), "p": (0, 1, 2)}})
    a.pose(0.3, {"head": (20, 0, 0), "body": {"r": (20, 0, 0), "p": (0, 0, -4)}}, i="linear")
    a.rest(0.5, ["body", "head"])
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


# ===========================================================================
# SIERPE SOLAR (ENDERMITE)
# ===========================================================================
def build_serpent():
    m = _model("kk_serpent", 1618, atlas=128)
    root = m.root
    hb = m.bone("hitbox", (0, 2, 0), root)
    m.cube(hb, "hitbox", (-2, 0, -4), (2, 4, 4), "hitbox")
    m.bone("tag_name", (0, 8, 0), root)
    body = m.bone("body", (0, 1.4, 0), root)
    hd = m.bone("head", (0, 2, -3), body)
    m.cube(hd, "head", (-1.4, 0.4, -6.4), (1.4, 3.0, -3.0), "scale", decor={"all": "scales", "east": "serpent_eyes",
                                                                           "west": "serpent_eyes"})
    m.cube(hd, "fangs", (-1.0, 0.0, -6.2), (1.0, 0.6, -5.4), "teeth")
    for i, ang in enumerate((-22.5, 0, 22.5)):
        plume(m, hd, f"crest{i}", (i - 1) * 0.6, 2.8, -4.2, 2.6, 0.4, ang, "z", ("feather", "feather_red", "feather")[i], "gold")
    segs = []
    prev = body
    for i in range(5):
        z0 = -3.0 + i * 2.4
        w = 1.2 - i * 0.15
        b = m.bone(f"seg{i}", (0, 1.4, z0), prev)
        m.cube(b, f"seg{i}", (-w, 1.4 - w, z0), (w, 1.4 + w, z0 + 2.6), "scale" if i % 2 == 0 else "scale_dark", **SC)
        segs.append(f"seg{i}")
        prev = b
    m.ZERO_BONES = ["body", "head"] + segs
    for name, length, amp in (("idle", 1.2, 10), ("walk", 0.5, 24)):
        a = m.anim(name, length, "loop")
        for k in range(9):
            t = length * k / 8
            for i, b in enumerate(segs):
                a.rot(b, t, 0, amp * math.sin(2 * math.pi * k / 8 + i), 0)
            a.rot("head", t, 0, -amp * 0.5 * math.sin(2 * math.pi * k / 8 - 1), 0)
    a = m.anim("attack", 0.5, "once")
    a.rest(0)
    a.pose(0.15, {"head": (-35, 0, 0), "body": {"p": (0, 1.5, 1)}})
    a.pose(0.3, {"head": (15, 0, 0), "body": {"p": (0, 0, -3)}}, i="linear")
    a.rest(0.5)
    a = m.anim("hurt", 0.3, "once")
    a.rest(0, ["head"])
    a.pose(0.08, {"head": (-20, 20, 0)})
    a.rest(0.3, ["head"])
    a = m.anim("spawn", 0.8, "once")
    a.pos("body", 0, 0, -6, 0)
    a.pos("body", 0.6, 0, 0, 0)
    a = m.anim("death", 0.8, "hold")
    a.rot("root", 0, 0, 0, 0)
    a.rot("root", 0.6, 0, 0, 170, i="linear")
    return m


# ===========================================================================
# ESPIRITU DE LA OFRENDA (ALLAY)
# ===========================================================================
def build_offering():
    m = _model("kk_offering", 1619, atlas=128)
    root = m.root
    hb = m.bone("hitbox", (0, 6, 0), root)
    m.cube(hb, "hitbox", (-3, 2, -3), (3, 12, 3), "hitbox")
    m.bone("tag_name", (0, 16, 0), root)
    body = m.bone("body", (0, 8, 0), root)
    m.cube(body, "mask", (-2.8, 6.0, -1.6), (2.8, 12.0, -0.6), "jade", decor={"north": "mask", "all": "stepfret"})
    m.cube(body, "mask_rim", (-3.2, 5.6, -0.8), (3.2, 12.4, 0.0), "gold", **SF)
    m.cube(body, "nose", (-0.6, 8.0, -2.4), (0.6, 10.0, -1.4), "jade", rot=("x", -22.5), pivot=(0, 10, -1.6))
    for i, ang in enumerate((-45, -22.5, 0, 22.5, 45)):
        plume(m, body, f"halo{i}", (i - 2) * 1.0, 11.6, 0.2, 5.0, 0.6, ang, "z", ("feather", "feather_red", "feather_blue",
                                                                              "feather_red", "feather")[i], "gold")
    sm = m.bone("smoke", (0, 4, 0), body)
    for i, (x, y, s) in enumerate(((0, 4.4, 1.6), (0.8, 2.4, 1.2), (-0.6, 0.6, 0.9))):
        m.cube(sm, f"copal{i}", (x - s, y - s * 0.8, -s), (x + s, y + s * 0.8, s), "copal", decor={"all": "wisp"})
    m.ZERO_BONES = ["body", "smoke"]
    a = m.anim("idle", 1.6, "loop")
    for t, s in ((0, 0), (0.8, 1), (1.6, 0)):
        a.pos("body", t, 0, 0.8 * s, 0)
        a.rot("body", t, 0, 10 * s - 5, 0)
    FX.spin(a, "smoke", 1.6, 1)
    a = m.anim("walk", 1.0, "loop")
    a.rot("body", 0, 10, 0, 0)
    a.rot("body", 1.0, 10, 0, 0)
    FX.spin(a, "smoke", 1.0, 1)
    a = m.anim("attack", 0.8, "once")
    a.scl("body", 0, 1)
    a.scl("body", 0.3, 1.3)
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
    a.scl("body", 1.0, 1.6, 0.05, 1.6)
    return m


# ===========================================================================
# GUERRERO JAGUAR (VINDICATOR)
# ===========================================================================
def build_jaguar():
    m = _model("kk_jaguar", 1620)

    def head(m, hd):
        AN.default_head(m, hd, face="jaguar_face", mat="skin")
        m.cube(hd, "pelt_head", (-3.8, 29.0, -3.4), (3.8, 33.0, 4.0), "pelt", decor={"all": "spots"})
        m.cube(hd, "upper_jaw", (-3.6, 30.0, -6.4), (3.6, 32.6, -3.0), "pelt", rot=("x", -22.5), pivot=(0, 30, -3.2),
               decor={"all": "spots", "north": "jaguar_face"})
        m.cube(hd, "jag_fangs", (-2.8, 28.8, -6.0), (2.8, 30.2, -5.2), "teeth", rot=("x", -22.5), pivot=(0, 30, -3.2))
        m.cube(hd, "lower_jaw", (-3.2, 23.6, -4.2), (3.2, 25.0, 2.0), "pelt", decor={"all": "spots"})
        for sx in (1, -1):
            m.cube(hd, f"ear{sx}", (2.6 * sx - 0.8, 32.6, -0.8), (2.6 * sx + 0.8, 34.4, 0.6), "pelt")
        for i, ang in enumerate((-22.5, 0, 22.5)):
            plume(m, hd, f"plume{i}", (i - 1) * 1.2, 32.6, 2.4, 6.0, 0.6, ang, "z", "feather", "feather_red")

    H = AN.humanoid(m, k=1.05, mats={"skin": "skin", "chest": "pelt", "belly": "cloth", "arm": "skin", "hand": "skin",
                                      "thigh": "pelt", "shin": "skin", "foot": "pelt", "pelvis": "cloth"}, head=head)
    for c in m.CUBES:
        if c.mat == "pelt" and not c.decor:
            c.decor["all"] = "spots"
    torso, waist = H["torso"], H["waist"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    m.cube(waist, "belt", (-4.6, 12.8, -2.9), (4.6, 14.6, 2.9), "red", **SF)
    m.cube(m.BONES["skirt_front"], "maxtlatl", (-2.4, 6.0, -3.0), (2.4, 13.0, -2.5), "cloth", **SF)
    sh = m.bone("shield", (-6.5, 14, -1), AL[1])
    m.cube(sh, "shield", (-9.6, 8.6, -4.6), (-8.6, 18.4, 4.6), "red", decor={"all": "stepfret"})
    m.cube(sh, "shield45", (-9.5, 9.2, -4.0), (-8.7, 17.8, 4.0), "gold", rot=("x", 45), pivot=(-9.1, 13.5, 0))
    for i in range(4):
        m.cube(sh, f"shield_feather{i}", (-9.4, 6.0, -3.0 + i * 2), (-8.8, 9.0, -2.0 + i * 2), "feather", **FE)
    mc = m.bone("macuahuitl", (6.5, 10.0, 0), AR[2])
    m.cube(mc, "club", (5.9, 9.0, -15.0), (7.1, 11.0, 2.0), "wood")
    for i in range(6):
        z = -14.0 + i * 2.2
        for sy in (1, -1):
            m.cube(mc, f"blade{i}{sy}", (6.1, 10.0 + sy * 1.0 - 0.6, z - 0.7), (6.9, 10.0 + sy * 2.2, z + 0.7), "obsidian",
                   rot=("x", 45), pivot=(6.5, 10 + sy * 1.4, z), decor={"all": "obsidian"})
    m.ZERO_BONES += ["macuahuitl", "shield"]
    GM.human_idle(m, arm_r=(-25, 0, 8), arm_l=(-30, 30, -6), extra=lambda a, t, s: (a.rot("macuahuitl", t, 50, 0, 0),
                                                                                      a.rot("torso", t, 8, 0, 0)))
    GM.human_walk(m, leg=26, arm=12, lean=10, arm_r=(-30, 0, 8), arm_l=(-35, 30, -6),
                  extra=lambda a, t, s: a.rot("macuahuitl", t, 50, 0, 0))
    a = m.anim("attack", 0.8, "once")
    a.rest(0)
    a.pose(0.2, {"right_arm": (-170, 0, 10), "macuahuitl": (60, 0, 0), "torso": (-8, 10, 0)})
    a.pose(0.35, {"right_arm": (-50, 0, -10), "macuahuitl": (0, 0, 0), "torso": (25, -10, 0)}, i="linear")
    a.pose(0.5, {"right_arm": (-90, -60, 0), "macuahuitl": (0, 0, 0), "torso": (5, 20, 0)})
    a.rest(0.8)
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-170, 0, 10), "macuahuitl": (70, 0, 0), "h_head": (-25, 0, 0)})
    GM.human_death(m)
    return m


BUILDERS = {"kukulkan": build_kukulkan, "kk_quetzal": build_quetzal, "kk_serpent": build_serpent, "kk_offering": build_offering,
            "kk_jaguar": build_jaguar}
SHOTS = {
    "kukulkan": [("idle", 0.6, -30), ("rest", 0, 150), ("screech", 0.4, -30), ("solar", 0.8, -30)],
    "kk_quetzal": [("idle", 0.15, -30), ("rest", 0, 150), ("attack", 0.15, -60), ("walk", 0.1, -80)],
    "kk_serpent": [("idle", 0.3, -40), ("rest", 0, 140), ("attack", 0.15, -70), ("walk", 0.2, -90)],
    "kk_offering": [("idle", 0.4, -30), ("rest", 0, 150), ("attack", 0.3, -40), ("walk", 0.2, -80)],
    "kk_jaguar": [("idle", 0.5, -30), ("rest", 0, 150), ("attack", 0.2, -60), ("walk", 0.25, -70)],
}
VIEW = {"kukulkan": (32, 3.6), "kk_quetzal": (9, 13.0), "kk_serpent": (3, 18.0), "kk_offering": (9, 13.0)}
ACTIONS = [("screech", 0.4, -30), ("eclipse", 0.5, -30), ("siphon", 0.5, -40), ("mark", 0.6, -40),
           ("venom", 0.5, -30), ("solar", 0.8, -30), ("storm", 0.6, -30), ("phase_change", 1.3, -30)]


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
            if name == "kukulkan":
                FX.action_sheet(m, ACTIONS, PREVIEW / "kukulkan_acciones.png", focus=32, scale=3.6)


if __name__ == "__main__":
    main()
