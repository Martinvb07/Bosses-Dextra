#!/usr/bin/env python3
"""
Boss 08 - YETI y sus subditos (modelos de ModelEngine).

  yeti              bestia del invierno: mechones de pelo blanco en capas, cara y manos azul hielo,
                    cejas pesadas, colmillos, cuernos cortos, carambanos en el pelo y brazos largos
  frost_brute       troll de escarcha azul con pinchos de hielo en la espalda y garrote de hielo (HUSK)
  glacier_raider    asaltante con capucha de piel, gafas de hueso y hacha de cristal (VINDICATOR)
  blizzard_spirit   espiritu de ventisca con mascara de hielo y cola de nieve (VEX)

Uso: python3 tools/b08_yeti.py [modelo ...] [--no-preview]
"""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from bbmodel import Model, mul  # noqa: E402
import anatomy as AN  # noqa: E402
import generate_minions as GM  # noqa: E402
import fxlib as FX  # noqa: E402
import b05_ragnarok as RG  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent / "Modelos/08_Yeti"
BLUEPRINTS = ROOT / "ModelEngine/blueprints"
PREVIEW = ROOT / "preview"

ICE_GLOW = (150, 240, 255)
MATS = {
    "fur": ((232, 236, 242), 9), "fur_shade": ((190, 200, 214), 9), "iceskin": ((120, 160, 200), 6),
    "ice": ((176, 226, 255), 5), "ice_dark": ((84, 146, 210), 6), "glow": ((150, 240, 255), 3),
    "horn": ((210, 200, 180), 6), "fang": ((245, 240, 230), 3), "mouth": ((40, 30, 50), 3),
    "troll": ((90, 130, 170), 8), "leather": ((92, 60, 36), 7), "furbrown": ((140, 110, 80), 9),
    "bone": ((220, 212, 190), 6), "wood": ((100, 70, 44), 8), "skin": ((120, 160, 200), 6),
    "spectral": ((200, 230, 250), 5), "spectral_dark": ((120, 170, 220), 6), "bronze": ((196, 140, 58), 8),
    "hitbox": ((255, 255, 255), 0),
}


def yeti_decor(m):
    D = m.decor

    @D
    def d_shag(f):
        """Pelo largo: mechones verticales y puntas oscuras abajo."""
        rng = random.Random(f.x0 * 7 + f.y0)
        for x in range(f.w):
            ln = rng.randint(1, 3)
            for y in range(f.h):
                if (x + rng.randint(0, 1)) % 3 == 0:
                    f.shade(x, y, 0.88)
            if f.name not in ("up", "down"):
                for y in range(f.h - ln, f.h):
                    f.shade(x, y, 0.8)

    @D
    def d_yeti_face(f):
        w = f.w
        for ex in (2, w - 5):
            f.rect(ex, 3, ex + 3, 5, (20, 30, 50))
            f.rect(ex, 3, ex + 3, 4, ICE_GLOW)
        f.rect(w // 2 - 1, 5, w // 2 + 1, 7, (70, 100, 140))

    @D
    def d_crystal(f):
        for y in range(f.h):
            f.put(0, y, (240, 252, 255))

    @D
    def d_troll_face(f):
        w = f.w
        for ex in (2, w - 5):
            f.rect(ex, 6, ex + 3, 8, (10, 20, 40))
            f.put(ex + 1, 7, ICE_GLOW)
        f.rect(w // 2 - 3, 11, w // 2 + 3, 12, (30, 40, 60))
        f.put(w // 2 - 3, 10, (245, 240, 230))
        f.put(w // 2 + 2, 10, (245, 240, 230))

    @D
    def d_goggles(f):
        if f.name != "north":
            return
        w = f.w
        f.rect(0, 5, w, 6, (60, 40, 30))
        for ex in (2, w - 5):
            f.rect(ex, 4, ex + 3, 7, (220, 212, 190))
            f.rect(ex + 1, 5, ex + 2, 6, (60, 140, 200))

    @D
    def d_wisp(f):
        for y in range(f.h):
            for x in range(f.w):
                if (x * 3 + y * 5) % 7 == 0:
                    f.shade(x, y, 1.2)


def _model(name, seed, atlas=256):
    m = Model(name, MATS, seed=seed, atlas_w=atlas)
    m.SHINE |= {"ice", "glow"}
    m.WOOD |= {"wood"}
    GM.add_common_decor(m)
    RG.norse_decor(m)
    yeti_decor(m)
    return m


SH = {"decor": {"all": "shag"}}


def tuft(m, bone, name, x, y, z, w, h, d, rot=None, mat="fur"):
    m.cube(bone, name, (x - w, y - h, z - d), (x + w, y, z + d), mat, rot=rot, pivot=(x, y, z), **SH)


# ===========================================================================
# YETI
# ===========================================================================
def yeti_head(m, hd):
    m.cube(hd, "skull", (-3.6, 25.0, -3.4), (3.6, 32.0, 3.8), "fur", **SH)
    m.cube(hd, "face", (-2.8, 24.6, -4.0), (2.8, 30.0, -3.2), "iceskin", decor={"north": "yeti_face"})
    m.cube(hd, "brow", (-3.4, 29.4, -4.8), (3.4, 31.0, -3.4), "fur", rot=("x", 22.5), pivot=(0, 30.6, -3.6), **SH)
    m.cube(hd, "muzzle", (-2.2, 24.0, -5.2), (2.2, 26.8, -3.4), "iceskin")
    m.cube(hd, "mouth", (-1.8, 24.2, -5.3), (1.8, 25.0, -4.6), "mouth")
    m.cube(hd, "jaw", (-2.6, 22.8, -4.8), (2.6, 24.4, 1.0), "iceskin")
    for sx in (1, -1):
        m.cube(hd, f"tusk{sx}", (1.5 * sx - 0.4, 23.4, -5.2), (1.5 * sx + 0.4, 26.4, -4.4), "fang", rot=("x", 22.5),
               pivot=(1.5 * sx, 24, -4.8))
    RG.horns(m, hd, y0=30.6, x0=3.2, segs=((0, 1.8, 0.9), (22.5, 1.8, 0.75), (45, 1.6, 0.55)), mat="horn", z=0.6)
    tuft(m, hd, "mane", 0, 32.6, 2.0, 3.8, 9.0, 1.8, ("x", 22.5))
    tuft(m, hd, "cheek_r", 3.6, 29.0, -1.0, 0.9, 5.0, 2.6, ("z", 22.5))
    tuft(m, hd, "cheek_l", -3.6, 29.0, -1.0, 0.9, 5.0, 2.6, ("z", -22.5))


def build_yeti():
    m = _model("yeti", 808)
    H = AN.humanoid(m, k=1.45, mats={"skin": "fur", "hand": "iceskin", "foot": "iceskin"}, head=yeti_head)
    for c in m.CUBES:
        if c.mat == "fur":
            c.decor.setdefault("all", "shag")
    torso, waist = H["torso"], H["waist"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    RL, LL = H["legs"]["right"], H["legs"]["left"]
    # mechones en capas (pecho, hombros, brazos, piernas y espalda)
    tuft(m, torso, "chest_tuft", 0, 24.0, -3.2, 5.6, 6.0, 1.2, ("x", -22.5))
    tuft(m, torso, "belly_tuft", 0, 18.2, -3.0, 4.6, 5.0, 1.0, ("x", -22.5), mat="fur_shade")
    tuft(m, torso, "back_tuft", 0, 25.0, 3.6, 5.8, 10.0, 1.4, ("x", 22.5))
    for i, (x, z) in enumerate(((-2.4, 3.8), (2.6, 3.6), (0, 4.4))):
        RG.crystals(m, torso, (x, 22.0 - i * 2, z), [(0, 0, 2.6 + i, 0.6, ("x", 22.5))], f"back_ice{i}")
    for side, sx, (arm, fore, hand) in (("r", 1, AR), ("l", -1, AL)):
        tuft(m, arm, f"shoulder_{side}", 7.0 * sx, 26.4, 0, 3.4, 4.0, 3.2, ("z", -22.5 * sx))
        tuft(m, fore, f"forearm_{side}", 7.6 * sx, 17.0, 0, 1.4, 5.6, 2.4, ("z", 22.5 * sx))
        for k, z in enumerate((-1.4, 0.0, 1.4)):
            m.cube(hand, f"claw_{side}{k}", (6.5 * sx - 0.45, 6.4, z - 0.45), (6.5 * sx + 0.45, 8.8, z + 0.45), "fang",
                   rot=("x", -22.5), pivot=(6.5 * sx, 8.8, z))
    for side, sx, (leg, low) in (("r", 1, RL), ("l", -1, LL)):
        tuft(m, leg, f"hip_{side}", 2.8 * sx, 14.4, 0, 3.0, 5.6, 3.0, ("z", 22.5 * sx))
        tuft(m, low, f"shin_{side}", 2.5 * sx, 7.6, 0, 2.8, 4.4, 2.8, ("z", 22.5 * sx), mat="fur_shade")
    m.cube(waist, "hip_fur", (-5.6, 9.6, -3.6), (5.6, 15.6, 3.6), "fur", **SH)

    hunch = lambda a, t, s: (a.rot("torso", t, 22 + 2 * s, 0, 0), a.rot("h_head", t, -18, 4 * s - 2, 0))  # noqa: E731
    GM.human_idle(m, arm_r=(-10, 0, 14), arm_l=(-10, 0, -14), extra=hunch)
    GM.human_walk(m, leg=22, arm=26, bob=1.4, lean=24, length=1.4,
                  extra=lambda a, t, s: a.rot("h_head", t, -20, 3 * s, 0))

    def anim(name, length, keys):
        a = m.anim(name, length, "once")
        a.rest(0)
        for t, pose, lin in keys:
            a.pose(t, pose, i="linear" if lin else "catmullrom")
        a.rest(length)
        return a

    anim("attack", 0.7, [(0.15, {"right_arm": (-160, 0, 20), "torso": (5, 15, 0)}, False),
                         (0.3, {"right_arm": (-50, 0, -10), "torso": (30, -12, 0)}, True)])
    anim("smash", 0.8, [(0.15, {"right_arm": (-175, 0, -10), "left_arm": (-175, 0, 10), "torso": (-10, 0, 0),
                                "h_head": (-20, 0, 0)}, False),
                        (0.28, {"right_arm": (-60, 0, -5), "left_arm": (-60, 0, 5), "torso": (40, 0, 0)}, True)])
    slam = {**GM.KNEEL, "right_arm": (-55, 0, -10), "left_arm": (-55, 0, 10), "torso": (45, 0, 0), "h_head": (-10, 0, 0)}
    anim("shatter", 1.2, [(0.25, {"right_arm": (-175, 0, -10), "left_arm": (-175, 0, 10), "torso": (-15, 0, 0),
                                  "body": {"p": (0, 3, 0)}}, False),
                          (0.4, slam, True), (0.8, slam, False)])
    anim("throw", 1.1, [(0.3, {"right_arm": (-175, 0, 30), "left_arm": (-175, 0, -30), "torso": (-20, 0, 0),
                               "h_head": (-25, 0, 0)}, False),
                        (0.5, {"right_arm": (-70, 0, 10), "left_arm": (-70, 0, -10), "torso": (25, 0, 0)}, True)])
    anim("nova", 0.9, [(0.15, {"right_arm": (-30, 0, 75), "left_arm": (-30, 0, -75), "torso": (-20, 0, 0),
                               "h_head": (-35, 0, 0)}, True),
                       (0.5, {"right_arm": (-30, 0, 70), "left_arm": (-30, 0, -70), "torso": (-18, 0, 0)}, False)])
    roar = {"right_arm": (-60, 0, 50), "left_arm": (-60, 0, -50), "torso": (-12, 0, 0), "h_head": (-12, 0, 0)}
    anim("roar", 1.6, [(0.3, {"torso": (30, 0, 0), "h_head": (10, 0, 0)}, False), (0.5, roar, True), (1.1, roar, False)])
    beat = {"right_arm": (-90, 60, 0), "left_arm": (-90, -60, 0), "torso": (-10, 0, 0), "h_head": (-25, 0, 0)}
    anim("summon", 1.4, [(0.2, beat, False), (0.3, {**beat, "right_arm": (-80, 30, 0), "left_arm": (-80, -30, 0)}, True),
                         (0.45, beat, False), (0.55, {**beat, "right_arm": (-80, 30, 0), "left_arm": (-80, -30, 0)}, True),
                         (1.0, roar, False)])
    anim("phase_change", 1.8, [(0.5, {**GM.KNEEL, "torso": (40, 0, 0), "h_head": (20, 0, 0)}, False),
                               (0.8, {**GM.KNEEL, "torso": (40, 0, 0)}, False), (1.2, roar, True), (1.5, roar, False)])
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-60, 0, 50), "left_arm": (-60, 0, -50), "h_head": (-35, 0, 0)}, length=2.0)
    GM.human_death(m, 2.4)
    m.scale(1.45)
    return m


# ===========================================================================
# BRUTO DE ESCARCHA (HUSK)
# ===========================================================================
def build_frost_brute():
    m = _model("frost_brute", 8081)

    def head(m, hd):
        AN.default_head(m, hd, face="troll_face", mat="troll")
        m.cube(hd, "brow", (-3.4, 28.8, -4.4), (3.4, 30.0, -3.2), "troll", rot=("x", 22.5), pivot=(0, 29.6, -3.6))
        RG.crystals(m, hd, (0, 31.6, 0), [(-1.6, 0, 2.4, 0.6, ("z", 22.5)), (1.6, 0, 2.6, 0.6, ("z", -22.5))], "head_ice")

    H = AN.humanoid(m, k=1.2, mats={"skin": "troll", "chest": "troll", "thigh": "furbrown", "pelvis": "furbrown"},
                    head=head)
    torso = H["torso"]
    AR = H["arms"]["right"]
    for i, (x, y) in enumerate(((-2.2, 22.0), (2.0, 21.0), (0, 18.0))):
        RG.crystals(m, torso, (x, y, 3.0), [(0, 0, 3.0, 0.8, ("x", 22.5))], f"spike{i}")
    m.cube(torso, "pelt", (-5.6, 21.6, -3.4), (5.6, 24.6, 3.6), "furbrown", decor={"all": "fur"})
    cl = m.bone("club", (6.5, 10.0, 0), AR[2])
    m.cube(cl, "handle", (6.1, 9.5, -8.0), (6.9, 10.5, 3.0), "wood")
    m.cube(cl, "head", (5.0, 8.0, -18.0), (8.0, 12.0, -8.0), "ice", decor={"all": "crystal"})
    m.cube(cl, "spikes", (4.6, 7.6, -16.0), (8.4, 12.4, -14.0), "ice_dark")
    m.ZERO_BONES += ["club"]
    GM.human_idle(m, arm_r=(-25, 0, 12), arm_l=(-5, 0, -14),
                  extra=lambda a, t, s: (a.rot("club", t, 50, 0, 0), a.rot("torso", t, 14, 0, 0)))
    GM.human_walk(m, leg=20, arm=12, lean=14, length=1.3, arm_r=(-30, 0, 12), extra=lambda a, t, s: a.rot("club", t, 50, 0, 0))
    a = m.anim("attack", 0.8, "once")
    a.rest(0)
    a.pose(0.2, {"right_arm": (-170, 0, 10), "club": (60, 0, 0), "torso": (-8, 10, 0)})
    a.pose(0.35, {"right_arm": (-50, 0, -10), "club": (0, 0, 0), "torso": (25, -10, 0)}, i="linear")
    a.rest(0.8)
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-170, 0, 10), "club": (60, 0, 0)})
    GM.human_death(m)
    return m


# ===========================================================================
# ASALTANTE GLACIAR (VINDICATOR)
# ===========================================================================
def build_glacier_raider():
    m = _model("glacier_raider", 8082)

    def head(m, hd):
        AN.default_head(m, hd, face="goggles", mat="iceskin")
        m.cube(hd, "hood", (-3.8, 27.4, -3.0), (3.8, 32.6, 4.0), "fur", **SH)
        m.cube(hd, "hood_rim", (-4.0, 26.0, -3.6), (4.0, 32.4, -2.8), "fur_shade", **SH)
        m.cube(hd, "scarf", (-3.4, 23.4, -4.0), (3.4, 26.2, 3.4), "furbrown", decor={"all": "fur"})

    H = AN.humanoid(m, k=1.0, mats={"skin": "iceskin", "chest": "furbrown", "belly": "leather", "arm": "furbrown",
                                     "thigh": "leather", "shin": "fur", "foot": "leather"}, head=head)
    torso, waist = H["torso"], H["waist"]
    AR = H["arms"]["right"]
    m.cube(torso, "fur_vest", (-4.8, 16.0, -3.2), (4.8, 23.6, 3.0), "fur", **SH)
    m.cube(waist, "belt", (-4.4, 13.2, -2.8), (4.4, 14.8, 2.8), "leather")
    m.cube(m.BONES["skirt_front"], "kilt", (-3.4, 8.0, -3.2), (3.4, 13.4, -2.6), "fur_shade", **SH)
    ax = m.bone("axe", (6.5, 10.0, 0), AR[2])
    m.cube(ax, "haft", (6.1, 9.5, -16.0), (6.9, 10.5, 3.0), "bone")
    RG.crystals(m, ax, (6.5, 10.0, -16.0), [(0, -1.0, 6.0, 1.2, ("x", -22.5)), (0, 0.6, 4.4, 1.0, None)], "blade")
    m.ZERO_BONES += ["axe"]
    GM.human_idle(m, arm_r=(-25, 0, 8), extra=lambda a, t, s: a.rot("axe", t, 50, 0, 0))
    GM.human_walk(m, leg=24, arm=12, arm_r=(-30, 0, 8), extra=lambda a, t, s: a.rot("axe", t, 50, 0, 0))
    a = m.anim("attack", 0.7, "once")
    a.rest(0)
    a.pose(0.15, {"right_arm": (-150, 0, 20), "axe": (40, 0, 0), "torso": (-5, 15, 0)})
    a.pose(0.3, {"right_arm": (-50, 0, -15), "axe": (0, 0, 0), "torso": (15, -15, 0)}, i="linear")
    a.rest(0.7)
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-170, 0, 10), "axe": (70, 0, 0), "h_head": (-15, 0, 0)})
    GM.human_death(m)
    return m


# ===========================================================================
# ESPIRITU DE VENTISCA (VEX)
# ===========================================================================
def build_blizzard_spirit():
    m = _model("blizzard_spirit", 8083, atlas=128)
    root = m.root
    hb = m.bone("hitbox", (0, 14, 0), root)
    m.cube(hb, "hitbox", (-4, 4, -4), (4, 24, 4), "hitbox")
    m.bone("tag_name", (0, 28, 0), root)
    body = m.bone("body", (0, 14, 0), root)
    hd = m.bone("head", (0, 20.5, 0), body)
    m.cube(hd, "mask", (-2.4, 17.6, -3.0), (2.4, 23.0, -2.0), "ice", decor={"north": "troll_face", "all": "crystal"})
    m.cube(hd, "chin", (-1.4, 16.4, -2.8), (1.4, 17.8, -2.0), "ice", rot=("x", -22.5), pivot=(0, 17.6, -2.4))
    for sx in (1, -1):
        m.cube(hd, f"hood{sx}", (2.0 * sx - 0.5, 17.0, -2.6), (2.0 * sx + 0.5, 23.4, 2.4), "spectral_dark",
               rot=("z", -22.5 * sx), pivot=(2.0 * sx, 23.0, 0), decor={"all": "wisp"})
    m.cube(hd, "hood_top", (-2.2, 22.6, -2.6), (2.2, 23.8, 3.0), "spectral", rot=("x", 22.5), pivot=(0, 23.2, 0),
           decor={"all": "wisp"})
    RG.crystals(m, hd, (0, 23.4, -0.6), [(-1.6, 0, 2.6, 0.5, ("z", 22.5)), (0, 0, 3.6, 0.6, None),
                                         (1.6, 0, 2.6, 0.5, ("z", -22.5))], "crown")
    # pecho que se afina hacia la cola, con picos de escarcha en los hombros
    m.cube(body, "chest", (-3.2, 15.6, -2.0), (3.2, 20.0, 2.4), "spectral", decor={"all": "wisp"})
    m.cube(body, "chest45", (-2.6, 15.8, -2.6), (2.6, 19.6, 3.0), "spectral_dark", rot=("y", 45), pivot=(0, 18, 0.2),
           decor={"all": "wisp"})
    for sx in (1, -1):
        m.cube(body, f"pauldron{sx}", (3.0 * sx - 1.4, 18.6, -1.6), (3.0 * sx + 1.4, 20.4, 2.0), "ice",
               rot=("z", -22.5 * sx), pivot=(3.0 * sx, 19.6, 0), decor={"all": "crystal"})
        RG.crystals(m, body, (3.6 * sx, 20.2, 0.4), [(0, 0, 2.2, 0.45, ("z", -45 * sx))], f"spk{sx}")
    sw = m.bone("swirl", (0, 12, 0.2), body)
    tiers = ((2.6, 12.0, 16.0), (2.0, 8.6, 12.4), (1.4, 5.4, 9.0), (0.8, 2.6, 5.8))
    for k, (w, y0, y1) in enumerate(tiers):
        for j, ang in enumerate((0, 45)):
            m.cube(sw, f"tail{k}_{j}", (-w, y0, -w + 0.2), (w, y1, w + 0.2), "spectral_dark" if (k + j) % 2 else "spectral",
                   rot=("y", ang) if ang else None, pivot=(0, y0, 0.2), decor={"all": "wisp"})
    for k, sx in enumerate((1, -1, 0)):
        m.cube(sw, f"ribbon{k}", (1.6 * sx - 0.3, 3.0 + k * 2, 2.0), (1.6 * sx + 0.3, 9.0 + k * 2, 2.6), "spectral",
               rot=("x", 45), pivot=(1.6 * sx, 9.0 + k * 2, 2.2), decor={"all": "wisp"})
    for side, sx in (("right", 1), ("left", -1)):
        arm = m.bone(f"{side}_arm", (3.8 * sx, 19.4, 0), body)
        m.cube(arm, f"{side}_upper", (3.8 * sx - 0.8, 15.4, -0.8), (3.8 * sx + 0.8, 19.8, 0.8), "spectral",
               decor={"all": "wisp"})
        fo = m.bone(f"{side}_fore", (3.8 * sx, 15.6, 0), arm)
        m.cube(fo, f"{side}_fore", (3.8 * sx - 0.6, 11.4, -0.6), (3.8 * sx + 0.6, 15.8, 0.6), "spectral_dark",
               decor={"all": "wisp"})
        m.cube(fo, f"{side}_cuff", (3.8 * sx - 0.9, 13.6, -0.9), (3.8 * sx + 0.9, 15.2, 0.9), "ice", rot=("y", 45),
               pivot=(3.8 * sx, 14.4, 0), decor={"all": "crystal"})
        for k in range(3):
            x = 3.8 * sx + (k - 1) * 0.55
            m.cube(fo, f"{side}_claw{k}", (x - 0.2, 8.6, -0.25), (x + 0.2, 11.6, 0.25), "ice",
                   rot=("z", (k - 1) * 22.5), pivot=(x, 11.6, 0))
    m.ZERO_BONES = ["body", "head", "swirl", "right_arm", "left_arm", "right_fore", "left_fore"]
    a = m.anim("idle", 1.4, "loop")
    for k in range(9):
        t = 1.4 * k / 8
        a.rot("swirl", t, 0, 45 * k, 0, i="linear")
    for t, s in ((0, 0), (0.7, 1), (1.4, 0)):
        a.pos("body", t, 0, 0.8 * s, 0)
        a.rot("right_arm", t, -40 + 8 * s, 0, 20)
        a.rot("left_arm", t, -40 - 8 * s, 0, -20)
        a.rot("right_fore", t, -30 - 10 * s, 0, 0)
        a.rot("left_fore", t, -30 - 10 * s, 0, 0)
        a.rot("head", t, 5 * s, 6 * s - 3, 0)
    a = m.anim("walk", 0.8, "loop")
    for k in range(9):
        a.rot("swirl", 0.8 * k / 8, 0, 45 * k, 0, i="linear")
    for t, s in ((0, 0), (0.4, 1), (0.8, 0)):
        a.rot("body", t, 22, 0, 3 * s)
        a.rot("right_arm", t, -90, 0, 15)
        a.rot("left_arm", t, -90, 0, -15)
    a = m.anim("attack", 0.6, "once")
    a.rest(0, ["right_arm", "left_arm", "body"])
    a.pose(0.12, {"right_arm": (-150, 0, 30), "left_arm": (-150, 0, -30)})
    a.pose(0.25, {"right_arm": (-70, 0, 0), "left_arm": (-70, 0, 0), "body": (15, 0, 0)}, i="linear")
    a.rest(0.6, ["right_arm", "left_arm", "body"])
    a = m.anim("hurt", 0.3, "once")
    a.rot("body", 0, 0, 0, 0)
    a.rot("body", 0.08, -15, 0, 10)
    a.rot("body", 0.3, 0, 0, 0)
    a = m.anim("spawn", 1.0, "once")
    a.scl("body", 0, 0.1)
    a.scl("body", 0.6, 1.1)
    a.scl("body", 1.0, 1)
    a = m.anim("death", 1.0, "hold")
    a.scl("body", 0, 1)
    a.scl("body", 1.0, 1.6, 0.05, 1.6)
    return m


BUILDERS = {"yeti": build_yeti, "frost_brute": build_frost_brute, "glacier_raider": build_glacier_raider,
            "blizzard_spirit": build_blizzard_spirit}
SHOTS = {
    "yeti": [("idle", 0.5, -30), ("rest", 0, 150), ("smash", 0.15, -50), ("roar", 0.6, -30)],
    "frost_brute": [("idle", 0.5, -30), ("rest", 0, 150), ("attack", 0.2, -60), ("attack", 0.35, -60)],
    "glacier_raider": [("rest", 0, -30), ("rest", 0, 150), ("attack", 0.15, -60), ("attack", 0.3, -60)],
    "blizzard_spirit": [("idle", 0.4, -30), ("idle", 0.4, 150), ("walk", 0.2, -80), ("attack", 0.25, -40)],
}
VIEW = {"yeti": (30, 4.4), "blizzard_spirit": (16, 10.0)}
ACTIONS = [("shatter", 0.2, -40), ("shatter", 0.5, -40), ("throw", 0.3, -60), ("nova", 0.4, -20),
           ("roar", 0.7, -30), ("summon", 0.3, -30), ("phase_change", 0.7, -40), ("death", 2.0, -60)]


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
            if name == "yeti":
                import fxlib
                fxlib.action_sheet(m, ACTIONS, PREVIEW / "yeti_acciones.png", focus=30, scale=4.4)


if __name__ == "__main__":
    main()
