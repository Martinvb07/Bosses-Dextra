#!/usr/bin/env python3
"""
Boss 14 - SAMHAIN y sus subditos (modelos de ModelEngine).

  samhain        Senor de las Animas: cabeza de calabaza tallada que arde por dentro (tallo, hojas,
                 enredaderas y llamas que salen de la cabeza), cuerpo flaco con tunica negra y
                 naranja hecha jirones, paja que asoma por mangas y cuello, velas en los hombros,
                 faroles de almas en la cintura y guadana de cosecha
  sh_scarecrow   espantapajaros maldito: arpillera remendada, paja, calabaza tallada, sombrero y horca (ZOMBIE)
  sh_wisp        fuego fatuo: bola de fuego con carita y llamas que suben (VEX)
  sh_rider       jinete sin cabeza: armadura oscura, capa, llamas en el cuello, espada y calabaza en la mano (HUSK)

Uso: python3 tools/b14_samhain.py [modelo ...] [--no-preview]
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

ROOT = Path(__file__).resolve().parent.parent / "Modelos/14_Samhain"
BLUEPRINTS = ROOT / "ModelEngine/blueprints"
PREVIEW = ROOT / "preview"

FIRE = (255, 170, 40)
MATS = {
    "pumpkin": ((230, 120, 20), 8), "pumpkin_dark": ((170, 80, 10), 7), "stem": ((80, 110, 40), 7), "leaf": ((70, 130, 40), 8),
    "robe": ((30, 22, 26), 5), "robe_or": ((200, 90, 20), 7), "straw": ((220, 190, 90), 9), "wood": ((90, 62, 40), 8),
    "fire": (FIRE, 3), "flame": ((255, 220, 120), 2), "soul": ((90, 220, 255), 3), "candle": ((235, 225, 200), 4),
    "iron": ((70, 70, 80), 6), "iron_hi": ((130, 130, 140), 6), "burlap": ((150, 120, 80), 9), "burlap_dark": ((110, 86, 56), 8),
    "skin": ((80, 70, 60), 6), "cloth": ((60, 40, 50), 7), "hat": ((40, 34, 30), 6), "leather": ((92, 60, 36), 7),
    "bone": ((214, 206, 186), 6), "hitbox": ((255, 255, 255), 0),
}


def harvest_decor(m):
    D = m.decor

    @D
    def d_pumpkin(f):
        """Gajos de la calabaza: franjas verticales."""
        for x in range(f.w):
            if x % 4 == 0:
                for y in range(f.h):
                    f.shade(x, y, 0.78)
            elif x % 4 == 2:
                for y in range(f.h):
                    f.shade(x, y, 1.1)

    @D
    def d_jack(f):
        """Cara tallada que brilla por dentro."""
        if f.name != "north":
            return
        w, h = f.w, f.h
        lit = (255, 210, 80)
        for ex in (2, w - 6):                       # ojos triangulares
            for y in range(4):
                f.rect(ex + (3 - y) // 2, 4 + y, ex + 4 - (3 - y) // 2, 5 + y, lit)
        f.rect(w // 2 - 1, 8, w // 2 + 1, 10, lit)  # nariz
        for x in range(3, w - 3):                   # sonrisa con dientes
            yy = 12 + (1 if 5 < x < w - 6 else 0)
            f.put(x, yy, lit)
            if x % 3 != 0:
                f.put(x, yy + 1, lit)

    @D
    def d_tatter(f):
        if f.name in ("up", "down"):
            return
        rng = random.Random(f.x0 + 7 * f.y0)
        for x in range(f.w):
            cut = rng.randint(0, 3)
            for y in range(f.h - cut, f.h):
                f.shade(x, y, 0.55)
        for x in range(0, f.w, 3):
            for y in range(f.h - 4):
                f.shade(x, y, 0.85)

    @D
    def d_straw(f):
        for x in range(f.w):
            for y in range(f.h):
                if (x * 3 + y) % 4 == 0:
                    f.shade(x, y, 0.8)
                elif (x + y * 2) % 7 == 0:
                    f.shade(x, y, 1.2)

    @D
    def d_burlap(f):
        for y in range(f.h):
            for x in range(f.w):
                if (x + y) % 2 == 0:
                    f.shade(x, y, 0.9)
        if f.name == "north" and f.w > 6:
            f.rect(1, 1, 4, 4, (110, 70, 50))

    @D
    def d_flame(f):
        for y in range(f.h):
            k = 1.3 - 0.5 * y / max(1, f.h - 1)
            for x in range(f.w):
                f.shade(x, y, k)

    @D
    def d_wisp_face(f):
        if f.name != "north":
            return
        w = f.w
        f.rect(1, 2, 3, 4, (60, 20, 0))
        f.rect(w - 3, 2, w - 1, 4, (60, 20, 0))
        f.rect(w // 2 - 1, 5, w // 2 + 1, 6, (60, 20, 0))

    @D
    def d_crystal(f):
        for y in range(f.h):
            f.put(0, y, (255, 240, 200))


def _model(name, seed, atlas=256):
    m = Model(name, MATS, seed=seed, atlas_w=atlas)
    m.SHINE |= {"fire", "flame", "soul", "iron_hi"}
    m.WOOD |= {"wood"}
    GM.add_common_decor(m)
    RG.norse_decor(m)
    harvest_decor(m)
    return m


PK = {"decor": {"all": "pumpkin"}}
TT = {"decor": {"all": "tatter"}}
STW = {"decor": {"all": "straw"}}
FL = {"decor": {"all": "flame"}}


def pumpkin_head(m, hd, y0=24.6, s=1.0, jack=True, name="pk"):
    """Calabaza achatada (dos cubos cruzados), cara tallada, tallo y hojas."""
    w, h = 4.0 * s, 6.4 * s
    m.cube(hd, name, (-w, y0, -w * 0.95), (w, y0 + h, w * 0.95), "pumpkin",
           decor={"north": "jack", "all": "pumpkin"} if jack else PK)
    m.cube(hd, name + "_45", (-w * 0.64, y0 + 0.3, -w * 0.64), (w * 0.64, y0 + h + 0.2, w * 0.64), "pumpkin_dark", rot=("y", 45),
           pivot=(0, y0 + h / 2, 0), **PK)
    m.cube(hd, name + "_stem", (-0.6 * s, y0 + h - 0.2, -0.6 * s), (0.6 * s, y0 + h + 2.2 * s, 0.6 * s), "stem",
           rot=("z", -22.5), pivot=(0, y0 + h, 0))
    m.cube(hd, name + "_leaf", (0.4 * s, y0 + h + 0.2, -1.4 * s), (3.0 * s, y0 + h + 0.6, 1.0 * s), "leaf", rot=("z", 22.5),
           pivot=(0.4 * s, y0 + h + 0.4, 0))


# ===========================================================================
# SAMHAIN
# ===========================================================================
def build_samhain():
    m = _model("samhain", 1414, atlas=512)

    def head(m, hd):
        pumpkin_head(m, hd, 24.6, 1.12)
        for i, (x, z, h) in enumerate(((-1.6, 0.6, 4.0), (0.6, -0.4, 5.4), (2.0, 1.0, 3.2))):   # llamas en la cabeza
            fb = m.bone(f"head_flame{i}", (x, 32.2, z), hd)
            m.cube(fb, f"head_flame{i}", (x - 0.7, 31.6, z - 0.7), (x + 0.7, 31.6 + h, z + 0.7), "fire", rot=("y", 45),
                   pivot=(x, 32, z), **FL)
            m.cube(fb, f"head_flame{i}t", (x - 0.4, 31.6 + h, z - 0.4), (x + 0.4, 32.6 + h, z + 0.4), "flame")
        for sx in (1, -1):                                                                     # enredaderas
            m.cube(hd, f"vine{sx}", (3.8 * sx - 0.3, 22.0, -1.0), (3.8 * sx + 0.3, 29.0, -0.4), "leaf", rot=("z", 22.5 * sx),
                   pivot=(3.8 * sx, 29, -0.7))

    H = AN.humanoid(m, k=0.95, mats={"skin": "robe", "chest": "robe", "belly": "robe", "arm": "robe", "hand": "bone",
                                      "thigh": "robe", "shin": "robe", "foot": "wood", "pelvis": "robe"}, head=head)
    for c in m.CUBES:
        if c.mat == "robe" and not c.decor:
            c.decor["all"] = "tatter"
    torso, waist = H["torso"], H["waist"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    # cuello de paja, capucha abierta y tunica en capas
    for i, ang in enumerate((-45, -22.5, 0, 22.5, 45)):
        m.cube(torso, f"straw_collar{i}", (-0.6 + (i - 2) * 1.2, 22.6, -2.8), (0.6 + (i - 2) * 1.2, 26.6, -2.2), "straw",
               rot=("z", ang) if ang else None, pivot=((i - 2) * 1.2, 23, -2.5), **STW)
    m.cube(torso, "hood", (-4.6, 21.6, 1.0), (4.6, 30.0, 3.8), "robe", rot=("x", -22.5), pivot=(0, 22, 2.4), **TT)
    m.cube(torso, "sash", (-4.4, 15.0, -3.0), (4.4, 16.6, 2.8), "robe_or", **TT)
    m.cube(torso, "chest_wrap", (-4.0, 17.0, -3.0), (4.0, 22.0, -2.4), "robe_or", rot=("z", 22.5), pivot=(0, 19.5, -2.7), **TT)
    m.cube(waist, "robe_hip", (-5.0, 4.0, -3.4), (5.0, 13.6, 3.4), "robe", **TT)
    m.cube_lr(waist, waist, "robe_flare", (4.4, -0.4, -3.4), (5.4, 8.0, 3.4), "robe", rot=("z", 22.5), pivot=(4.9, 8, 0), **TT)
    m.cube(m.BONES["skirt_front"], "front_rag", (-2.6, -0.6, -4.0), (2.6, 13.0, -3.4), "robe_or", **TT)
    m.cube(m.BONES["skirt_back"], "back_rag", (-4.4, -1.0, 3.4), (4.4, 13.0, 4.0), "robe", rot=("x", 22.5), pivot=(0, 13, 3.7), **TT)
    # paja en las munecas, velas en los hombros
    for side, sx, arm in (("r", 1, AR), ("l", -1, AL)):
        for k, ang in enumerate((-22.5, 0, 22.5)):
            m.cube(arm[1], f"wrist_straw_{side}{k}", (6.5 * sx - 0.4 + (k - 1) * 0.8, 9.6, -0.4), (6.5 * sx + 0.4 + (k - 1) * 0.8, 12.6, 0.4),
                   "straw", rot=("z", ang) if ang else None, pivot=(6.5 * sx, 12, 0), **STW)
        m.cube(arm[1], f"sleeve_{side}", (4.4 * sx if sx > 0 else -8.6, 11.6, -2.6), (8.6 if sx > 0 else -4.4, 16.0, 2.6),
               "robe", rot=("z", 22.5 * sx), pivot=(6.5 * sx, 16, 0), **TT)
        for k, (dx, h) in enumerate(((-1.0, 3.0), (0.8, 4.2))):
            x = 7.0 * sx + dx
            m.cube(arm[0], f"candle_{side}{k}", (x - 0.5, 24.0, -0.5 + k), (x + 0.5, 24.0 + h, 0.5 + k), "candle")
            m.cube(arm[0], f"candle_fl_{side}{k}", (x - 0.35, 24.0 + h, -0.35 + k), (x + 0.35, 25.4 + h, 0.35 + k), "flame",
                   rot=("y", 45), pivot=(x, 24.5 + h, k))
        m.cube(arm[0], f"pad_{side}", (4.6 * sx if sx > 0 else -9.0, 22.0, -2.8), (9.0 if sx > 0 else -4.6, 24.2, 2.8), "robe_or",
               rot=("z", -22.5 * sx), pivot=(6.8 * sx, 23, 0), **TT)
    # faroles de almas en la cintura
    lanterns = []
    for sx in (1, -1):
        lb = m.bone(f"lantern{sx}", (4.8 * sx, 13.0, -1.6), waist)
        m.cube(lb, f"lantern_chain{sx}", (4.8 * sx - 0.2, 10.6, -1.8), (4.8 * sx + 0.2, 13.0, -1.4), "iron")
        m.cube(lb, f"lantern{sx}", (4.8 * sx - 1.2, 7.4, -2.8), (4.8 * sx + 1.2, 10.8, -0.4), "iron")
        m.cube(lb, f"lantern_soul{sx}", (4.8 * sx - 0.9, 7.8, -3.0), (4.8 * sx + 0.9, 10.4, -0.2), "soul")
        lanterns.append(f"lantern{sx}")
    # guadana de cosecha
    sc = m.bone("scythe", (6.5, 10.0, 0), AR[2])
    m.cube(sc, "shaft", (6.05, 9.55, -26.0), (6.95, 10.45, 7.0), "wood")
    for i, z in enumerate((-18.0, -6.0)):
        m.cube(sc, f"wrap{i}", (5.85, 9.35, z - 0.6), (7.15, 10.65, z + 0.6), "robe_or")
    blade = [((3.4, 10.6), -26.6, None), ((-0.8, 4.0), -26.2, ("x", -22.5)), ((-4.8, -0.2), -25.0, ("x", -45))]
    for i, ((y0, y1), z, rot) in enumerate(blade):
        w = 1.5 - i * 0.3
        m.cube(sc, f"blade{i}", (6.2, y0, z - w), (6.8, y1, z + w), "iron_hi", rot=rot, pivot=(6.5, y1, z))
        m.cube(sc, f"edge{i}", (6.25, y0, z - w - 0.6), (6.75, y1, z - w), "fire", rot=rot, pivot=(6.5, y1, z))
    m.ZERO_BONES += ["scythe", "head_flame0", "head_flame1", "head_flame2"] + lanterns

    def flicker(a, length, k=1.0):
        steps = 8
        for i in range(steps + 1):
            t = length * i / steps
            for j in range(3):
                s = 1 + 0.25 * k * math.sin(2 * math.pi * i / steps * 2 + j * 2)
                a.scl(f"head_flame{j}", t, 1, s, 1)

    a = GM.human_idle(m, arm_r=(-20, 0, 10), arm_l=(-10, 0, -10),
                      extra=lambda a, t, s: (a.rot("scythe", t, -80, 0, 0), a.rot("lantern1", t, 8 * s - 4, 0, 0),
                                             a.rot("lantern-1", t, 4 - 8 * s, 0, 0), a.rot("torso", t, 8, 0, 0),
                                             a.rot("h_head", t, -6, 0, 8 * s - 4)))
    flicker(a, 2.4)
    a = GM.human_walk(m, leg=20, arm=10, lean=10, length=1.3, arm_r=(-25, 0, 10),
                      extra=lambda a, t, s: (a.rot("scythe", t, -80, 0, 0), a.rot("lantern1", t, 14 * s, 0, 0),
                                             a.rot("lantern-1", t, -14 * s, 0, 0)))
    flicker(a, 1.3)

    def anim(name, length, keys, fl=1.0):
        a = m.anim(name, length, "once")
        a.rest(0)
        for t, pose, lin in keys:
            a.pose(t, pose, i="linear" if lin else "catmullrom")
        a.rest(length)
        flicker(a, length, fl)
        return a

    anim("attack", 0.7, [(0.15, {"right_arm": (-160, 0, 20), "scythe": (-100, 0, 0), "torso": (-6, 15, 0)}, False),
                         (0.3, {"right_arm": (-55, 0, -10), "scythe": (-20, 0, 0), "torso": (18, -15, 0)}, True)])
    reap_a = {"right_arm": (-90, 80, 0), "scythe": (-80, 0, 0), "torso": (5, 40, 0)}
    reap_b = {"right_arm": (-90, -80, 0), "scythe": (-80, 0, 0), "torso": (5, -40, 0)}
    anim("reap", 0.8, [(0.15, reap_a, False), (0.3, reap_b, True)])
    up = {"right_arm": (-175, 0, -5), "left_arm": (-175, 0, 20), "scythe": (-90, 0, 0), "torso": (-12, 0, 0)}
    slam = {"right_arm": (-45, 0, -10), "left_arm": (-50, 0, 20), "scythe": (10, 0, 0), "torso": (35, 0, 0)}
    anim("harvest", 1.0, [(0.15, up, False), (0.3, slam, True), (0.6, slam, False)], 2)
    flare = {"right_arm": (-40, 0, 70), "left_arm": (-40, 0, -70), "scythe": (-80, 0, 0), "h_head": (-20, 0, 0),
             "torso": (-10, 0, 0)}
    anim("burst", 0.9, [(0.1, {"torso": (20, 0, 0), "right_arm": (-30, -40, 0), "left_arm": (-30, 40, 0)}, False),
                        (0.2, flare, True), (0.5, flare, False)], 3)
    spin_pose = {"right_arm": (-90, 0, 80), "left_arm": (-90, 0, -80), "scythe": (-80, 0, 0)}
    a = anim("storm", 1.3, [(0.2, spin_pose, False), (0.9, spin_pose, False)], 3)
    FX.spin(a, "body", 0.9, 2)
    a.rot("body", 1.3, 0, 0, 0)
    call = {"right_arm": (-178, 0, 5), "scythe": (-90, 0, 0), "left_arm": (-150, 0, -30), "h_head": (-30, 0, 0)}
    anim("call", 1.4, [(0.3, call, False), (1.1, call, False)], 3)
    channel = {**GM.KNEEL, "right_arm": (-60, 0, 0), "scythe": (150, 0, 0), "left_arm": (-150, 0, -30), "h_head": (-25, 0, 0)}
    anim("last_harvest", 2.6, [(0.4, channel, False), (1.95, channel, False), (2.05, flare, True), (2.3, flare, False)], 5)
    anim("summon", 1.4, [(0.35, call, False), (1.0, call, False)], 2)
    anim("phase_change", 1.8, [(0.5, {**GM.KNEEL, "torso": (40, 0, 0), "h_head": (25, 0, 0)}, False),
                               (0.8, {**GM.KNEEL, "torso": (40, 0, 0), "h_head": (25, 0, 0)}, False),
                               (1.2, flare, True), (1.5, flare, False)], 4)
    GM.human_hurt(m)
    a = GM.human_spawn(m, call, length=2.0)
    flicker(a, 2.0, 2)
    GM.human_death(m, 2.4)
    m.scale(1.5)
    return m


# ===========================================================================
# ESPANTAPAJAROS MALDITO (ZOMBIE)
# ===========================================================================
def build_scarecrow():
    m = _model("sh_scarecrow", 1415)

    def head(m, hd):
        pumpkin_head(m, hd, 24.8, 0.95)
        m.cube(hd, "hat_brim", (-5.6, 30.4, -5.6), (5.6, 31.2, 5.6), "hat")
        m.cube(hd, "hat_top", (-2.6, 31.0, -2.6), (2.6, 35.0, 2.6), "hat", rot=("x", -22.5), pivot=(0, 31, 0))
        m.cube(hd, "hat_tip", (-1.4, 34.0, 0.6), (1.4, 36.0, 3.4), "hat", rot=("x", -45), pivot=(0, 34.5, 1.5))

    H = AN.humanoid(m, k=0.9, mats={"skin": "burlap", "chest": "cloth", "belly": "burlap", "arm": "cloth", "hand": "straw",
                                     "thigh": "burlap_dark", "shin": "burlap_dark", "foot": "straw", "pelvis": "burlap"}, head=head)
    for c in m.CUBES:
        if c.mat in ("burlap", "burlap_dark", "cloth") and not c.decor:
            c.decor["all"] = "burlap"
    torso = H["torso"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    m.cube(torso, "patch", (-2.4, 17.0, -3.0), (0.4, 19.6, -2.6), "robe_or")
    m.cube(torso, "rope", (-4.0, 14.8, -2.6), (4.0, 15.6, 2.6), "straw")
    for side, sx, arm in (("r", 1, AR), ("l", -1, AL)):
        for k, ang in enumerate((-45, -22.5, 0, 22.5)):
            m.cube(arm[1], f"straw_{side}{k}", (6.5 * sx - 0.3 + (k - 1.5) * 0.6, 8.6, -0.3), (6.5 * sx + 0.3 + (k - 1.5) * 0.6, 12.0, 0.3),
                   "straw", rot=("z", ang) if ang else None, pivot=(6.5 * sx, 11.6, 0), **STW)
    for k, ang in enumerate((-22.5, 0, 22.5)):
        m.cube(torso, f"neck_straw{k}", (-0.4 + (k - 1), 22.8, -2.0), (0.4 + (k - 1), 26.0, -1.4), "straw",
               rot=("z", ang) if ang else None, pivot=(k - 1, 23, -1.7), **STW)
    fk = m.bone("fork", (6.5, 10.0, 0), AR[2])
    m.cube(fk, "fork_shaft", (6.1, 9.6, -18.0), (6.9, 10.4, 6.0), "wood")
    m.cube(fk, "fork_bar", (4.6, 9.6, -18.6), (8.4, 10.4, -17.8), "iron")
    for i, dx in enumerate((-1.6, 0.0, 1.6)):
        m.cube(fk, f"tine{i}", (6.5 + dx - 0.3, 9.7, -22.6), (6.5 + dx + 0.3, 10.3, -18.4), "iron_hi")
    m.ZERO_BONES += ["fork"]
    GM.human_idle(m, arm_r=(-25, 0, 8), arm_l=(0, 0, -70), extra=lambda a, t, s: (a.rot("fork", t, -60, 0, 0),
                                                                                    a.rot("h_head", t, 0, 0, 15 + 4 * s)))
    GM.human_walk(m, leg=18, arm=8, lean=4, arm_r=(-30, 0, 8), arm_l=(0, 0, -70),
                  extra=lambda a, t, s: (a.rot("fork", t, -60, 0, 0), a.rot("h_head", t, 0, 0, 15)))
    a = m.anim("attack", 0.7, "once")
    a.rest(0)
    a.pose(0.15, {"right_arm": (-120, 0, 10), "fork": (-30, 0, 0), "torso": (-8, 0, 0)})
    a.pose(0.3, {"right_arm": (-80, 0, 0), "fork": (0, 0, 0), "torso": (20, 0, 0), "body": {"p": (0, 0, -2)}}, i="linear")
    a.rest(0.7)
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-170, 0, 10), "fork": (-90, 0, 0), "left_arm": (0, 0, -80)})
    GM.human_death(m)
    return m


# ===========================================================================
# FUEGO FATUO (VEX)
# ===========================================================================
def build_wisp():
    m = _model("sh_wisp", 1416, atlas=128)
    root = m.root
    hb = m.bone("hitbox", (0, 8, 0), root)
    m.cube(hb, "hitbox", (-3, 4, -3), (3, 12, 3), "hitbox")
    m.bone("tag_name", (0, 16, 0), root)
    body = m.bone("body", (0, 8, 0), root)
    m.cube(body, "core", (-2.4, 5.8, -2.4), (2.4, 10.6, 2.4), "fire", decor={"north": "wisp_face", "all": "flame"})
    m.cube(body, "core45", (-2.0, 6.2, -2.0), (2.0, 10.2, 2.0), "flame", rot=("y", 45), pivot=(0, 8.2, 0))
    m.cube(body, "corex", (-2.0, 6.4, -2.0), (2.0, 10.0, 2.0), "fire", rot=("x", 45), pivot=(0, 8.2, 0), **FL)
    flames = []
    for k, (x, z, h) in enumerate(((0, 0, 5.0), (-1.4, 0.8, 3.4), (1.4, -0.6, 3.8), (0.4, 1.6, 2.8))):
        fb = m.bone(f"flame{k}", (x, 10.2, z), body)
        m.cube(fb, f"flame{k}", (x - 0.8, 10.0, z - 0.8), (x + 0.8, 10.0 + h, z + 0.8), "fire" if k else "flame", rot=("y", 45),
               pivot=(x, 10, z), **FL)
        flames.append(f"flame{k}")
    tl = m.bone("trail", (0, 6.0, 1.0), body)
    m.cube(tl, "trail", (-1.0, 4.6, 1.0), (1.0, 6.4, 4.0), "fire", rot=("x", 22.5), pivot=(0, 6, 1), **FL)
    m.cube(tl, "trail2", (-0.5, 4.0, 3.6), (0.5, 5.2, 6.4), "flame", rot=("x", 22.5), pivot=(0, 6, 1))
    m.ZERO_BONES = ["body", "trail"] + flames
    a = m.anim("idle", 1.2, "loop")
    for i in range(7):
        t = 1.2 * i / 6
        a.pos("body", t, 0, 0.8 * math.sin(2 * math.pi * i / 6), 0)
        for k, f in enumerate(flames):
            a.scl(f, t, 1, 1 + 0.3 * math.sin(2 * math.pi * i / 6 * 2 + k), 1)
        a.rot("trail", t, 0, 15 * math.sin(2 * math.pi * i / 6), 0)
    a = m.anim("walk", 0.6, "loop")
    a.rot("body", 0, 20, 0, 0)
    a.rot("body", 0.6, 20, 0, 0)
    for i in range(5):
        a.rot("trail", 0.6 * i / 4, 20, 25 * math.sin(2 * math.pi * i / 4), 0)
    a = m.anim("attack", 0.5, "once")
    a.scl("body", 0, 1)
    a.scl("body", 0.15, 1.4)
    a.scl("body", 0.3, 0.9)
    a.scl("body", 0.5, 1)
    a = m.anim("hurt", 0.3, "once")
    a.rot("body", 0, 0, 0, 0)
    a.rot("body", 0.08, -15, 0, 15)
    a.rot("body", 0.3, 0, 0, 0)
    a = m.anim("spawn", 0.8, "once")
    a.scl("body", 0, 0.1)
    a.scl("body", 0.5, 1.3)
    a.scl("body", 0.8, 1)
    a = m.anim("death", 0.8, "hold")
    a.scl("body", 0, 1)
    a.scl("body", 0.3, 1.5)
    a.scl("body", 0.8, 0.05)
    return m


# ===========================================================================
# JINETE SIN CABEZA (HUSK)
# ===========================================================================
def build_rider():
    m = _model("sh_rider", 1417)

    def head(m, hd):
        for k, (x, z, h) in enumerate(((0, 0, 4.0), (-1.0, 0.6, 2.8), (1.0, -0.4, 3.2))):
            fb = m.bone(f"neck_flame{k}", (x, 24.8, z), hd)
            m.cube(fb, f"neck_flame{k}", (x - 0.8, 24.6, z - 0.8), (x + 0.8, 24.6 + h, z + 0.8), "fire", rot=("y", 45),
                   pivot=(x, 24.6, z), **FL)
        m.cube(hd, "collar", (-2.6, 23.6, -2.6), (2.6, 25.4, 2.6), "iron_hi")

    H = AN.humanoid(m, k=1.1, mats={"skin": "iron", "chest": "iron", "belly": "leather", "arm": "iron", "hand": "leather",
                                     "thigh": "leather", "shin": "iron", "foot": "leather", "pelvis": "leather"}, head=head)
    torso = H["torso"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    m.cube_lr(AR[0], AL[0], "pauldron", (4.2, 21.8, -3.2), (9.4, 24.8, 3.2), "iron_hi", rot=("z", -22.5), pivot=(6.8, 23.3, 0))
    m.cube(torso, "breast", (-4.6, 18.4, -3.6), (4.6, 23.6, -3.0), "iron_hi")
    cape = m.bone("cape", (0, 24, 3.2), torso, rotation=(10, 0, 0))
    m.cube(cape, "cape", (-5.2, 2.0, 3.2), (5.2, 24.0, 3.8), "robe", **TT)
    m.cube(cape, "cape_in", (-5.0, 2.4, 2.9), (5.0, 23.6, 3.2), "robe_or")
    sw = m.bone("sword", (6.5, 10.0, 0), AR[2])
    m.cube(sw, "grip", (6.1, 9.5, -2.2), (6.9, 10.5, 2.0), "leather")
    m.cube(sw, "guard", (4.8, 9.2, -2.8), (8.2, 10.8, -2.2), "iron")
    m.cube(sw, "blade", (6.2, 9.0, -16.0), (6.8, 11.0, -2.8), "iron_hi")
    m.cube(sw, "blade_tip", (6.25, 9.3, -17.6), (6.75, 10.7, -15.6), "iron_hi", rot=("x", 45), pivot=(6.5, 10, -16.6))
    pk = m.bone("held_pumpkin", (-6.5, 9.0, -1.0), AL[2])
    pumpkin_head(m, pk, 4.6, 0.6, name="held")
    for c in m.CUBES:
        if c.name.startswith("held"):
            for i in (0, 2):
                c.frm[i] += -6.5 if i == 0 else -1.6
                c.to[i] += -6.5 if i == 0 else -1.6
            c.pivot[0] += -6.5
            c.pivot[2] += -1.6
    m.ZERO_BONES += ["sword", "cape", "held_pumpkin", "neck_flame0", "neck_flame1", "neck_flame2"]
    GM.human_idle(m, arm_r=(-25, 0, 8), arm_l=(-50, 0, -10),
                  extra=lambda a, t, s: (a.rot("sword", t, 50, 0, 0), a.rot("cape", t, 4 * s, 0, 0)))
    GM.human_walk(m, leg=24, arm=10, lean=6, arm_r=(-30, 0, 8), arm_l=(-50, 0, -10),
                  extra=lambda a, t, s: (a.rot("sword", t, 50, 0, 0), a.rot("cape", t, 14 + 4 * s, 0, 0)))
    a = m.anim("attack", 0.7, "once")
    a.rest(0)
    a.pose(0.1, {"right_arm": (-150, 0, 20), "sword": (40, 0, 0), "torso": (-5, 15, 0), "left_arm": (-50, 0, -10)})
    a.pose(0.2, {"right_arm": (-50, 0, -15), "sword": (0, 0, 0), "torso": (15, -15, 0), "left_arm": (-50, 0, -10)}, i="linear")
    a.pose(0.3, {"right_arm": (-90, -60, 0), "sword": (0, 0, 0), "torso": (5, 20, 0), "left_arm": (-50, 0, -10)})
    a.pose(0.4, {"right_arm": (-90, 60, 0), "sword": (0, 0, 0), "torso": (5, -20, 0), "left_arm": (-50, 0, -10)}, i="linear")
    a.rest(0.7)
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-170, 0, 10), "sword": (70, 0, 0), "left_arm": (-150, 0, -10)})
    GM.human_death(m)
    return m


BUILDERS = {"samhain": build_samhain, "sh_scarecrow": build_scarecrow, "sh_wisp": build_wisp, "sh_rider": build_rider}
SHOTS = {
    "samhain": [("idle", 0.6, -30), ("rest", 0, 150), ("attack", 0.15, -50), ("call", 0.6, -30)],
    "sh_scarecrow": [("idle", 0.5, -30), ("rest", 0, 150), ("attack", 0.3, -60), ("walk", 0.25, -70)],
    "sh_wisp": [("idle", 0.4, -30), ("rest", 0, 150), ("attack", 0.15, -40), ("walk", 0.2, -80)],
    "sh_rider": [("idle", 0.5, -30), ("rest", 0, 150), ("attack", 0.1, -60), ("walk", 0.25, -70)],
}
VIEW = {"samhain": (32, 4.2), "sh_wisp": (9, 14.0)}
ACTIONS = [("reap", 0.3, -40), ("harvest", 0.3, -40), ("burst", 0.3, -30), ("storm", 0.5, -30),
           ("call", 0.6, -30), ("last_harvest", 1.0, -40), ("summon", 0.6, -30), ("phase_change", 1.3, -30)]


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
            if name == "samhain":
                FX.action_sheet(m, ACTIONS, PREVIEW / "samhain_acciones.png", focus=32, scale=4.2)


if __name__ == "__main__":
    main()
