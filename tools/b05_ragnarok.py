#!/usr/bin/env python3
"""
Boss 05 - RAGNAROK y sus subditos (modelos de ModelEngine).

  ragnarok         gigante de hielo vikingo: casco con cuernos curvos y corona de cristales,
                   barba trenzada, manto de piel de lobo, tatuajes de runas que brillan,
                   cristales de hielo en el hombro y gran hacha de hielo
  draugr           vikingo no muerto encorvado, piel azulada y ojos que brillan (ZOMBIE)
  spectral_valkyrie valquiria espectral con alas, casco alado y lanza de hielo (VEX)
  viking_warrior   guerrero vikingo con escudo redondo pintado, hacha y capa de piel (HUSK)

Uso: python3 tools/b05_ragnarok.py [modelo ...] [--no-preview]
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

ROOT = Path(__file__).resolve().parent.parent / "Modelos/05_Ragnarok"
BLUEPRINTS = ROOT / "ModelEngine/blueprints"
PREVIEW = ROOT / "preview"

ICE_GLOW = (150, 240, 255)

MATS = {
    "frost": ((128, 158, 186), 7), "fur": ((222, 226, 232), 9), "fur_grey": ((132, 128, 124), 9),
    "iron": ((88, 92, 100), 5), "chain": ((100, 104, 112), 6), "ice": ((176, 226, 255), 5),
    "ice_dark": ((84, 146, 210), 6), "glow": ((150, 240, 255), 3), "leather": ((92, 60, 36), 7),
    "wood": ((110, 74, 42), 8), "gold": ((214, 168, 60), 8), "beard": ((214, 226, 240), 8),
    "ivory": ((230, 220, 196), 6), "corpse": ((96, 118, 130), 8), "spectral": ((170, 230, 250), 5),
    "spectral_dark": ((90, 160, 200), 6), "tan": ((196, 150, 110), 7), "ginger": ((200, 96, 40), 8),
    "red": ((168, 32, 36), 6), "white": ((236, 232, 222), 4), "skin": ((128, 158, 186), 7),
    "bronze": ((196, 140, 58), 8), "hitbox": ((255, 255, 255), 0),
}


def norse_decor(m):
    D = m.decor

    @D
    def d_tattoo(f):
        """Tatuajes de runas que brillan (lineas cian en zigzag)."""
        if f.name in ("up", "down"):
            return
        rng = random.Random(f.x0 * 5 + f.y0)
        for x0 in range(1, f.w - 1, 4):
            y = rng.randrange(max(1, f.h - 4))
            for k in range(min(4, f.h - y)):
                f.put(x0 + (k % 2), y + k, ICE_GLOW)

    @D
    def d_fur(f):
        rng = random.Random(f.x0 * 3 + f.y0 * 11)
        for y in range(f.h):
            for x in range(f.w):
                r = rng.random()
                if r < 0.25:
                    f.shade(x, y, 0.82)
                elif r < 0.35:
                    f.shade(x, y, 1.1)
        if f.name not in ("up", "down"):
            for x in range(0, f.w, 2):
                f.shade(x, f.h - 1, 0.7)

    @D
    def d_crystal(f):
        for y in range(f.h):
            f.put(0, y, (240, 252, 255))
            if f.w > 2:
                f.put(f.w - 1, y, mul(m.MAT["ice_dark"], 0.9))

    @D
    def d_giant_face(f):
        w = f.w
        for ex in (2, w - 5):
            f.rect(ex, 6, ex + 3, 8, (20, 30, 40))
            f.rect(ex, 6, ex + 3, 7, ICE_GLOW)
        f.rect(1, 5, 6, 6, mul(m.MAT["beard"], 0.8))
        f.rect(w - 6, 5, w - 1, 6, mul(m.MAT["beard"], 0.8))

    @D
    def d_draugr_face(f):
        w = f.w
        for ex in (2, w - 5):
            f.rect(ex, 6, ex + 3, 8, (10, 14, 20))
            f.put(ex + 1, 7, ICE_GLOW)
        f.rect(w // 2 - 2, 11, w // 2 + 2, 12, (20, 26, 30))

    @D
    def d_viking_face(f):
        w = f.w
        for ex in (2, w - 5):
            f.rect(ex, 6, ex + 3, 8, (240, 236, 224))
            f.rect(ex + 1, 6, ex + 2, 8, (60, 100, 150))
        f.rect(1, 5, 6, 6, m.MAT["ginger"])
        f.rect(w - 6, 5, w - 1, 6, m.MAT["ginger"])

    @D
    def d_braid(f):
        for y in range(0, f.h, 2):
            for x in range(f.w):
                f.shade(x, y, 0.8 if (x + y // 2) % 2 else 1.1)

    @D
    def d_knot(f):
        """Nudo nordico en oro."""
        if f.name not in ("north", "south"):
            return
        for y in range(f.h):
            for x in range(f.w):
                if (x + y) % 4 == 0 or (x - y) % 4 == 0:
                    f.put(x, y, m.MAT["gold"])

    @D
    def d_shield_paint(f):
        """Escudo redondo pintado en cuartos rojo/blanco con umbo de hierro."""
        if f.name not in ("east", "west", "north", "south"):
            return
        cx, cy = f.w / 2, f.h / 2
        for y in range(f.h):
            for x in range(f.w):
                q = (x < cx) ^ (y < cy)
                f.put(x, y, m.MAT["red"] if q else m.MAT["white"])
        f.rect(int(cx) - 2, int(cy) - 2, int(cx) + 2, int(cy) + 2, m.MAT["iron"])
        for x in range(f.w):
            f.put(x, 0, m.MAT["iron"])
            f.put(x, f.h - 1, m.MAT["iron"])
        for y in range(f.h):
            f.put(0, y, m.MAT["iron"])
            f.put(f.w - 1, y, m.MAT["iron"])

    @D
    def d_straps(f):
        for y in range(1, f.h, 3):
            for x in range(f.w):
                f.put(x, (y + x) % f.h, m.MAT["leather"])

    @D
    def d_feather(f):
        for x in range(f.w):
            f.put(x, f.h // 2, mul(m.MAT["spectral_dark"], 1.0))
        for y in range(f.h):
            f.put(0, y, (240, 252, 255))

    @D
    def d_chainmail(f):
        for y in range(f.h):
            for x in range(f.w):
                if (x + (y % 2)) % 2 == 0:
                    f.shade(x, y, 0.7)

    @D
    def d_wisp(f):
        for y in range(f.h):
            for x in range(f.w):
                if (x * 3 + y * 5) % 7 == 0:
                    f.shade(x, y, 1.25)
                elif (x + y * 2) % 9 == 0:
                    f.shade(x, y, 0.8)


def _model(name, seed):
    m = Model(name, MATS, seed=seed, atlas_w=256)
    m.SHINE |= {"iron", "gold", "ice", "glow"}
    m.WOOD |= {"wood"}
    GM.add_common_decor(m)
    norse_decor(m)
    return m


F = {"decor": {"all": "fur"}}
C = {"decor": {"all": "crystal"}}


def horns(m, hd, y0=29.4, x0=3.4, segs=((0, 3.4, 1.1), (22.5, 3.2, 0.95), (45, 3.0, 0.75), (45, 2.0, 0.5)),
          mat="ivory", z=-0.4):
    """Cuernos que salen de lado y se curvan hacia arriba."""
    for side, sx in (("r", 1), ("l", -1)):
        x, y = x0 * sx, y0
        for i, (ang, ln, w) in enumerate(segs):
            frm = (x if sx > 0 else x - ln, y - w * 0.7, z - w * 0.8)
            to = (x + ln if sx > 0 else x, y + w * 0.7, z + w * 0.8)
            m.cube(hd, f"horn_{side}{i}", frm, to, mat, rot=("z", ang * sx) if ang else None, pivot=(x, y, z))
            x += sx * ln * math.cos(math.radians(ang))
            y += ln * math.sin(math.radians(ang))


def crystals(m, bone, base, spec, prefix):
    """Racimo de cristales de hielo: spec = [(dx, dz, h, w, (eje, ang))]."""
    bx, by, bz = base
    for i, (dx, dz, h, w, rot) in enumerate(spec):
        m.cube(bone, f"{prefix}{i}", (bx + dx - w, by, bz + dz - w), (bx + dx + w, by + h, bz + dz + w),
               "ice" if i % 2 == 0 else "ice_dark", rot=rot, pivot=(bx + dx, by, bz + dz), **C)
        m.cube(bone, f"{prefix}{i}_tip", (bx + dx - w * 0.5, by + h, bz + dz - w * 0.5),
               (bx + dx + w * 0.5, by + h + w * 1.6, bz + dz + w * 0.5), "glow", rot=rot, pivot=(bx + dx, by, bz + dz))


# ===========================================================================
# RAGNAROK
# ===========================================================================
def rg_head(m, hd):
    AN.default_head(m, hd, face="giant_face", mat="frost")
    m.cube(hd, "helm", (-3.8, 29.4, -3.7), (3.8, 32.4, 3.9), "iron", decor={"all": "knot"})
    m.cube(hd, "helm_top", (-2.8, 32.4, -2.7), (2.8, 33.4, 2.9), "iron")
    m.cube(hd, "helm_band", (-3.9, 29.2, -3.9), (3.9, 30.0, 4.1), "gold")
    m.cube(hd, "nasal", (-0.5, 26.6, -4.6), (0.5, 30.0, -3.7), "iron")
    m.cube_lr(hd, hd, "cheek_guard", (2.8, 25.8, -3.6), (3.9, 29.6, -0.6), "iron")
    horns(m, hd)
    crystals(m, hd, (0, 33.2, 0), [(0, -1.0, 3.6, 0.7, None), (-1.8, 0.2, 2.6, 0.6, ("z", 22.5)),
                                    (1.8, 0.2, 2.8, 0.6, ("z", -22.5)), (0, 1.6, 2.2, 0.5, ("x", -22.5))], "crown")
    # barba larga trenzada y melena
    m.cube(hd, "beard", (-3.0, 21.6, -4.6), (3.0, 26.6, -3.0), "beard", decor={"all": "braid"})
    m.cube(hd, "moustache", (-2.4, 26.2, -4.7), (2.4, 27.0, -3.9), "beard")
    for sx in (1, -1):
        m.cube(hd, f"braid{sx}", (1.3 * sx - 0.7, 16.6, -4.4), (1.3 * sx + 0.7, 21.8, -3.4), "beard", decor={"all": "braid"})
        m.cube(hd, f"braid_ring{sx}", (1.3 * sx - 0.85, 18.0, -4.55), (1.3 * sx + 0.85, 18.8, -3.25), "gold")
    m.cube(hd, "mane", (-3.6, 20.6, 3.0), (3.6, 30.0, 4.4), "beard", decor={"all": "braid"})


def build_ragnarok():
    m = _model("ragnarok", 505)
    H = AN.humanoid(m, k=1.3, mats={"skin": "frost", "chest": "chain", "belly": "chain", "foot": "fur",
                                    "shin": "fur", "thigh": "leather"}, head=rg_head)
    for c in m.CUBES:
        if c.mat == "frost" and c.bone.name.endswith(("arm", "forearm")):
            c.decor["all"] = "tattoo"
        elif c.mat == "chain":
            c.decor.setdefault("all", "chainmail")
        elif c.mat == "fur":
            c.decor.setdefault("all", "fur")
    torso, waist = H["torso"], H["waist"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    RL, LL = H["legs"]["right"], H["legs"]["left"]
    # manto de piel de lobo sobre los hombros
    m.cube(torso, "mantle", (-6.2, 22.8, -1.0), (6.2, 25.4, 4.4), "fur_grey", **F)
    m.cube_lr(torso, torso, "mantle_side", (5.4, 19.6, -3.0), (7.4, 24.8, 4.2), "fur_grey", rot=("z", 22.5),
              pivot=(6.4, 24.8, 0), **F)
    m.cube(torso, "mantle_back", (-6.0, 10.0, 3.6), (6.0, 23.0, 4.6), "fur_grey", rot=("x", 22.5), pivot=(0, 23, 4.1), **F)
    m.cube(torso, "wolf_head", (-2.0, 21.0, 4.2), (2.0, 24.6, 7.2), "fur", **F)
    # correas cruzadas, cinturon con hebilla de runa
    m.cube(torso, "strap1", (-6.6, 19.0, -3.7), (6.6, 20.2, 3.4), "leather", rot=("z", 45), pivot=(0, 19.6, 0))
    m.cube(torso, "strap2", (-6.6, 19.0, -3.75), (6.6, 20.2, 3.45), "leather", rot=("z", -45), pivot=(0, 19.6, 0))
    m.cube(waist, "belt", (-5.2, 13.2, -3.4), (5.2, 15.4, 3.3), "leather")
    m.cube(waist, "buckle", (-1.3, 13.0, -3.8), (1.3, 15.6, -3.3), "gold", decor={"all": "knot"})
    m.cube(waist, "buckle_rune", (-0.5, 13.6, -3.95), (0.5, 15.0, -3.75), "glow")
    # faldon de piel
    m.cube(m.BONES["skirt_front"], "kilt_f", (-4.2, 7.6, -3.8), (4.2, 13.6, -3.0), "fur_grey", **F)
    m.cube(m.BONES["skirt_back"], "kilt_b", (-4.4, 7.6, 3.0), (4.4, 13.6, 3.8), "fur_grey", **F)
    m.cube_lr(waist, waist, "kilt_s", (4.6, 8.2, -3.0), (5.4, 13.6, 3.0), "fur_grey", rot=("z", 22.5),
              pivot=(5.0, 13.6, 0), **F)
    # botas de piel con correas
    m.cube_lr(RL[1], LL[1], "boot_wrap", (0.4, 1.0, -2.6), (4.6, 6.6, 2.4), "fur_grey", **F)
    m.cube_lr(RL[1], LL[1], "boot_strap", (0.3, 3.2, -2.7), (4.7, 3.9, 2.5), "leather")
    m.cube_lr(RL[1], LL[1], "boot_cuff", (0.2, 6.2, -2.8), (4.8, 7.8, 2.6), "fur", **F)
    # brazales y cristales de hielo en el hombro derecho
    m.cube_lr(AR[1], AL[1], "bracer", (4.9, 11.6, -2.0), (8.1, 15.4, 2.0), "leather", decor={"all": "knot"})
    m.cube_lr(AR[0], AL[0], "armband", (4.9, 19.0, -1.9), (8.1, 20.0, 1.9), "gold")
    crystals(m, AR[0], (7.0, 24.0, 0), [(0, 0, 4.2, 0.9, ("z", -22.5)), (0.6, -1.6, 3.0, 0.7, ("x", 22.5)),
                                         (0.6, 1.6, 3.2, 0.7, ("x", -22.5)), (1.6, 0, 2.4, 0.6, ("z", -45))], "shard")
    m.cube(AL[0], "pauldron_l", (-9.2, 21.8, -3.0), (-4.6, 25.0, 3.0), "iron", rot=("z", -22.5), pivot=(-5, 24, 0),
           decor={"all": "knot"})
    # gran hacha de hielo
    ax = m.bone("axe", (6.5, 10.0, 0), AR[2])
    m.cube(ax, "haft", (6.05, 9.5, -26.0), (6.95, 10.5, 4.0), "wood")
    m.cube(ax, "haft_wrap", (5.95, 9.4, -2.0), (7.05, 10.6, 3.0), "leather", decor={"all": "straps"})
    m.cube(ax, "pommel", (5.9, 9.3, 4.0), (7.1, 10.7, 5.0), "gold")
    m.cube(ax, "socket", (5.8, 8.8, -26.0), (7.2, 11.2, -20.0), "iron", decor={"all": "knot"})
    m.cube(ax, "blade", (6.1, 11.2, -27.0), (6.9, 20.0, -19.0), "ice", **C)
    m.cube(ax, "beard_blade", (6.1, 15.0, -30.0), (6.9, 21.6, -26.0), "ice", rot=("x", -22.5), pivot=(6.5, 18, -27),
           **C)
    m.cube(ax, "edge", (6.05, 13.0, -31.0), (6.95, 21.0, -30.0), "glow", rot=("x", -22.5), pivot=(6.5, 18, -27))
    m.cube(ax, "back_spike", (6.2, 4.0, -24.6), (6.8, 8.8, -21.4), "ice_dark", rot=("x", 22.5), pivot=(6.5, 8.8, -23))
    m.ZERO_BONES += ["axe"]

    GM.human_idle(m, arm_r=(-25, 0, 10), arm_l=(-5, 0, -12),
                  extra=lambda a, t, s: (a.rot("axe", t, 60, 0, 0), a.rot("torso", t, 4, 0, 0)))
    GM.human_walk(m, leg=20, arm=10, bob=1.0, lean=6, length=1.4, arm_r=(-25, 0, 10),
                  extra=lambda a, t, s: a.rot("axe", t, 60, 0, 0))

    def swing(name, length, hit, up, down):
        a = m.anim(name, length, "once")
        a.rest(0)
        a.pose(hit * 0.5, up)
        a.pose(hit, down, i="linear")
        a.pose(hit + 0.25, down)
        a.rest(length)
        return a

    swing("attack", 0.7, 0.3, {"right_arm": (-165, 0, 15), "torso": (-8, 15, 0), "axe": (60, 0, 0)},
          {"right_arm": (-50, 0, -10), "torso": (15, -10, 0), "axe": (0, 0, 0)})
    swing("heavy", 0.7, 0.2, {"right_arm": (-90, 70, 30), "torso": (0, 40, 0), "axe": (30, 40, 0)},
          {"right_arm": (-90, -60, -10), "torso": (10, -40, 0), "axe": (30, -30, 0)})
    swing("blow", 1.0, 0.3, {"right_arm": (-175, 0, -10), "left_arm": (-175, 0, 10), "torso": (-15, 0, 0),
                              "axe": (70, 0, 0), "h_head": (-15, 0, 0)},
          {**GM.KNEEL, "right_arm": (-60, 0, -5), "left_arm": (-60, 0, 5), "torso": (35, 0, 0), "axe": (0, 0, 0)})

    a = m.anim("burst", 0.9, "once")           # pisoton y brazos abiertos (inmediato)
    a.rest(0)
    a.pose(0.12, {"right_arm": (-30, 0, 70), "left_arm": (-30, 0, -70), "torso": (-12, 0, 0), "h_head": (-20, 0, 0),
                  "right_leg": (-40, 0, 0), "right_lower_leg": (30, 0, 0)}, i="linear")
    a.pose(0.25, {"right_arm": (-30, 0, 70), "left_arm": (-30, 0, -70), "torso": (-10, 0, 0), "right_leg": (0, 0, 0),
                  "right_lower_leg": (0, 0, 0)}, i="linear")
    a.rest(0.9)

    a = m.anim("storm", 1.2, "once")           # alza el hacha al cielo y la tormenta cae (0.4 s)
    a.rest(0)
    up = {"right_arm": (-178, 0, 5), "axe": (70, 0, 0), "left_arm": (-140, 0, -40), "h_head": (-30, 0, 0),
          "torso": (-12, 0, 0)}
    a.pose(0.35, up)
    a.pose(0.8, up)
    a.rest(1.2)

    a = m.anim("lightning", 1.6, "once")       # brazos al cielo invocando rayos
    a.rest(0)
    call = {"right_arm": (-170, 0, 30), "left_arm": (-170, 0, -30), "axe": (70, 0, 0), "h_head": (-35, 0, 0),
            "torso": (-15, 0, 0)}
    a.pose(0.3, call)
    for k, t in enumerate((0.5, 0.7, 0.9, 1.1)):
        a.pose(t, {**call, "torso": (-15 + (3 if k % 2 else -3), 0, 0)})
    a.rest(1.6)

    a = m.anim("ragnarok", 2.8, "once")        # carga el fin 2 s y golpea el suelo con las dos manos
    a.rest(0)
    charge = {"right_arm": (-175, 0, -10), "left_arm": (-175, 0, 10), "axe": (70, 0, 0), "torso": (-18, 0, 0),
              "h_head": (-30, 0, 0)}
    a.pose(0.5, charge)
    for k, t in enumerate((0.8, 1.1, 1.4, 1.7)):
        a.pose(t, {**charge, "torso": (-18 + (2 if k % 2 else -2), 0, 0)})
    a.pose(2.0, {**GM.KNEEL, "right_arm": (-55, 0, -5), "left_arm": (-55, 0, 5), "axe": (-10, 0, 0),
                 "torso": (38, 0, 0), "h_head": (15, 0, 0)}, i="linear")
    a.pose(2.4, {**GM.KNEEL, "right_arm": (-55, 0, -5), "left_arm": (-55, 0, 5), "axe": (-10, 0, 0), "torso": (35, 0, 0)})
    a.rest(2.8)

    a = m.anim("summon", 1.4, "once")          # golpe al pecho y grito de guerra
    a.rest(0)
    a.pose(0.2, {"left_arm": (-100, 40, -10), "h_head": (10, 0, 0)})
    a.pose(0.35, {"left_arm": (-80, 60, 0), "torso": (5, 0, 0)}, i="linear")
    a.pose(0.7, {"right_arm": (-170, 0, 10), "axe": (70, 0, 0), "left_arm": (-30, 0, -50), "h_head": (-30, 0, 0),
                 "torso": (-12, 0, 0)})
    a.pose(1.1, {"right_arm": (-170, 0, 10), "axe": (70, 0, 0), "left_arm": (-30, 0, -50), "h_head": (-30, 0, 0)})
    a.rest(1.4)

    a = m.anim("phase_change", 1.8, "once")
    a.rest(0)
    kneel = {**GM.KNEEL, "torso": (30, 0, 0), "h_head": (25, 0, 0), "right_arm": (-30, 0, 10), "left_arm": (-30, 0, -10)}
    a.pose(0.5, kneel)
    a.pose(0.8, kneel)
    roar = {"body": {"p": (0, 0, 0)}, "right_leg": (0, 0, 0), "right_lower_leg": (0, 0, 0), "left_leg": (0, 0, 0),
            "left_lower_leg": (0, 0, 0), "torso": (-18, 0, 0), "h_head": (-30, 0, 0), "right_arm": (-30, 0, 65),
            "left_arm": (-30, 0, -65), "axe": (60, 0, 0)}
    a.pose(1.2, roar, i="linear")
    a.pose(1.5, roar)
    a.rest(1.8)

    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-170, 0, 10), "axe": (70, 0, 0), "h_head": (-25, 0, 0)}, length=2.0)
    GM.human_death(m, 2.6)
    m.scale(1.5)
    return m


# ===========================================================================
# DRAUGR (ZOMBIE)
# ===========================================================================
def build_draugr():
    m = _model("draugr", 5051)

    def head(m, hd):
        AN.default_head(m, hd, face="draugr_face", mat="corpse")
        m.cube(hd, "helm", (-3.7, 29.6, -3.6), (3.7, 32.4, 3.8), "iron", decor={"all": "rusty"} if "rusty" in m.DECOR else None)
        m.cube(hd, "nasal", (-0.45, 26.8, -4.5), (0.45, 30.0, -3.6), "iron")
        m.cube(hd, "beard", (-2.6, 22.0, -4.2), (2.6, 25.6, -3.0), "fur_grey", decor={"all": "braid"})
        m.cube(hd, "beard_tail", (-1.0, 19.6, -4.0), (1.0, 22.2, -3.2), "fur_grey", rot=("x", -22.5),
               pivot=(0, 22.2, -3.6))

    H = AN.humanoid(m, k=0.95, mats={"skin": "corpse", "chest": "chain", "belly": "chain", "thigh": "leather",
                                     "shin": "leather", "foot": "leather"}, head=head)
    for c in m.CUBES:
        if c.mat == "chain":
            c.decor.setdefault("all", "chainmail")
    torso, waist = H["torso"], H["waist"]
    AR = H["arms"]["right"]
    m.cube(torso, "rags", (-4.4, 14.6, -3.0), (4.4, 17.2, 2.8), "fur_grey", **F)
    m.cube(m.BONES["skirt_front"], "rag_f", (-3.0, 7.6, -3.0), (3.0, 13.2, -2.5), "fur_grey", **F)
    m.cube(waist, "belt", (-4.2, 13.2, -2.6), (4.2, 14.6, 2.6), "leather")
    ax = m.bone("axe", (6.5, 10.0, 0), AR[2])
    m.cube(ax, "haft", (6.1, 9.5, -12.0), (6.9, 10.5, 3.0), "wood")
    m.cube(ax, "head", (6.15, 10.4, -12.4), (6.85, 15.0, -8.4), "iron")
    m.ZERO_BONES += ["axe"]
    GM.human_idle(m, arm_r=(-35, 0, 10), arm_l=(-20, 0, -10),
                  extra=lambda a, t, s: (a.rot("axe", t, 50, 0, 0), a.rot("torso", t, 18, 0, 0),
                                         a.rot("h_head", t, -14, 6 * s - 3, 5)))
    GM.human_walk(m, leg=16, arm=8, lean=18, length=1.5, arm_r=(-35, 0, 10),
                  extra=lambda a, t, s: a.rot("axe", t, 50, 0, 0))
    a = m.anim("attack", 0.8, "once")
    a.rest(0)
    a.pose(0.2, {"right_arm": (-160, 0, 15), "torso": (5, 10, 0), "axe": (50, 0, 0)})
    a.pose(0.35, {"right_arm": (-50, 0, -10), "torso": (25, -10, 0), "axe": (0, 0, 0)}, i="linear")
    a.rest(0.8)
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-80, 0, 10), "h_head": (-15, 0, 0)})
    GM.human_death(m)
    return m


# ===========================================================================
# VALQUIRIA ESPECTRAL (VEX)
# ===========================================================================
def build_spectral_valkyrie():
    m = _model("spectral_valkyrie", 5052)
    m.SHINE |= {"spectral"}

    def head(m, hd):
        AN.default_head(m, hd, face="draugr_face", mat="spectral")
        m.cube(hd, "helm", (-3.6, 29.4, -3.6), (3.6, 32.2, 3.8), "ice", **C)
        m.cube(hd, "nasal", (-0.45, 27.0, -4.4), (0.45, 29.8, -3.6), "ice")
        for sx in (1, -1):
            m.cube(hd, f"wing{sx}", (3.4 * sx - 0.3, 29.6, -1.0), (3.4 * sx + 0.3, 34.0, 2.6), "white",
                   rot=("z", -22.5 * sx), pivot=(3.4 * sx, 30, 0), decor={"all": "feather"})
        m.cube(hd, "braid", (-0.8, 18.0, 3.2), (0.8, 30.0, 4.4), "beard", decor={"all": "braid"})

    H = AN.humanoid(m, k=0.8, mats={"skin": "spectral", "chest": "ice", "shin": "spectral_dark",
                                     "foot": "spectral_dark"}, head=head)
    torso, waist = H["torso"], H["waist"]
    AR = H["arms"]["right"]
    for c in m.CUBES:
        if c.mat == "spectral_dark":
            c.decor["all"] = "wisp"
    m.cube(waist, "skirt", (-4.0, 6.0, -2.8), (4.0, 14.0, 2.8), "spectral_dark", decor={"all": "wisp"})
    m.cube_lr(waist, waist, "skirt_s", (3.4, 3.6, -2.6), (4.2, 12.0, 2.6), "spectral_dark", rot=("z", 22.5),
              pivot=(3.8, 12, 0), decor={"all": "wisp"})
    for side, sx in (("r", 1), ("l", -1)):
        w = m.bone(f"wing_{side}", (1.6 * sx, 22.0, 3.0), torso, rotation=(0, -20 * sx, 25 * sx))
        for k, (ln, h) in enumerate(((11, 3.2), (9, 3.0), (7, 2.8), (5, 2.6))):
            y1 = 23.6 - k * 2.4
            x0, x1 = (1.6, 1.6 + ln) if sx > 0 else (-1.6 - ln, -1.6)
            m.cube(w, f"feather_{side}{k}", (x0, y1 - h, 3.0 + k * 0.1), (x1, y1, 3.5 + k * 0.1),
                   "white" if k % 2 == 0 else "spectral", decor={"all": "feather"})
    sp = m.bone("spear", (6.5, 10.0, 0), AR[2])
    m.cube(sp, "shaft", (6.15, 9.6, -14.0), (6.85, 10.4, 10.0), "ice_dark")
    m.cube(sp, "point", (6.05, 9.2, -19.0), (6.95, 10.8, -14.0), "glow")
    m.ZERO_BONES += ["spear", "wing_r", "wing_l"]
    float_legs = {"right_leg": (-15, 0, 0), "right_lower_leg": (25, 0, 0), "left_leg": (5, 0, 0),
                  "left_lower_leg": (20, 0, 0)}

    def flap(a, t, s, amp=30):
        a.rot("wing_r", t, 0, -amp * s, 10 * s)
        a.rot("wing_l", t, 0, amp * s, -10 * s)

    a = m.anim("idle", 1.2, "loop")
    for t, s in ((0, 1), (0.6, -1), (1.2, 1)):
        a.pose(t, {**float_legs, "right_arm": (-30, 0, 10), "spear": (40, 0, 0), "torso": (5, 0, 0)})
        a.pos("body", t, 0, 0.8 * s, 0)
        flap(a, t, s)
    a = m.anim("walk", 0.8, "loop")
    for t, s in ((0, 1), (0.4, -1), (0.8, 1)):
        a.pose(t, {"right_leg": (30, 0, 0), "left_leg": (20, 0, 0), "torso": (25, 0, 0), "h_head": (-20, 0, 0),
                   "right_arm": (-60, 0, 10), "spear": (60, 0, 0)})
        a.pos("body", t, 0, 0.5 * s, 0)
        flap(a, t, s, 40)
    a = m.anim("attack", 0.6, "once")
    a.rest(0)
    a.pose(0.12, {"right_arm": (-20, 0, 25), "torso": (-5, 25, 0), "spear": (90, 0, 0)})
    a.pose(0.25, {"right_arm": (-95, 0, -5), "torso": (15, -15, 0), "spear": (0, 0, 0)}, i="linear")
    a.rest(0.6)
    GM.human_hurt(m)
    a = m.anim("spawn", 1.2, "once")
    a.pos("body", 0, 0, 12, 0)
    a.scl("body", 0, 0.2)
    a.pos("body", 0.7, 0, 0, 0)
    a.scl("body", 0.7, 1)
    a.rest(1.2)
    a = m.anim("death", 1.4, "hold")
    a.rest(0)
    a.pose(0.3, {"torso": (-20, 0, 0), "h_head": (-25, 0, 0), "right_arm": (10, 0, 40), "left_arm": (10, 0, -40)})
    a.scl("body", 0.3, 1)
    a.scl("body", 1.4, 0.05, 1.4, 0.05)
    a.pos("body", 1.4, 0, 8, 0)
    return m


# ===========================================================================
# GUERRERO VIKINGO (HUSK)
# ===========================================================================
def build_viking_warrior():
    m = _model("viking_warrior", 5053)

    def head(m, hd):
        AN.default_head(m, hd, face="viking_face", mat="tan")
        m.cube(hd, "helm", (-3.7, 29.6, -3.6), (3.7, 32.6, 3.8), "iron")
        m.cube(hd, "helm_top", (-2.4, 32.6, -2.3), (2.4, 33.4, 2.5), "iron")
        m.cube(hd, "nasal", (-0.45, 26.8, -4.5), (0.45, 30.0, -3.6), "iron")
        m.cube(hd, "beard", (-2.9, 22.0, -4.4), (2.9, 26.6, -3.0), "ginger", decor={"all": "braid"})
        m.cube(hd, "beard_braid", (-0.7, 19.2, -4.2), (0.7, 22.2, -3.4), "ginger", decor={"all": "braid"})
        m.cube(hd, "hair", (-3.4, 23.0, 3.0), (3.4, 30.0, 4.2), "ginger", decor={"all": "braid"})

    H = AN.humanoid(m, k=1.05, mats={"skin": "tan", "chest": "leather", "belly": "leather", "thigh": "leather",
                                     "shin": "fur_grey", "foot": "leather"}, head=head)
    torso, waist = H["torso"], H["waist"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    m.cube(torso, "mail", (-4.8, 16.0, -3.2), (4.8, 23.4, 3.0), "chain", decor={"all": "chainmail"})
    m.cube(torso, "fur_collar", (-5.2, 22.4, -3.4), (5.2, 24.8, 3.6), "fur", **F)
    cp = m.bone("cape", (0, 24, 3.4), torso)
    m.cube(cp, "cape", (-4.8, 8.0, 3.2), (4.8, 24.0, 3.9), "fur_grey", rot=("x", 0), **F)
    m.cube(waist, "belt", (-4.6, 13.0, -2.9), (4.6, 14.8, 2.9), "leather")
    m.cube(waist, "buckle", (-1.0, 12.8, -3.3), (1.0, 15.0, -2.9), "gold")
    m.cube_lr(AR[1], AL[1], "bracer", (5.0, 12.0, -1.9), (8.0, 15.6, 1.9), "leather", decor={"all": "straps"})
    sh = m.bone("shield", (-6.5, 14, -1), AL[1])
    m.cube(sh, "shield", (-9.6, 7.0, -6.0), (-8.6, 19.0, 6.0), "wood", decor={"all": "shield_paint"})
    m.cube(sh, "shield_boss", (-10.4, 11.6, -1.4), (-9.6, 14.4, 1.4), "iron")
    ax = m.bone("axe", (6.5, 10.0, 0), AR[2])
    m.cube(ax, "haft", (6.1, 9.5, -14.0), (6.9, 10.5, 3.0), "wood")
    m.cube(ax, "head", (6.15, 10.4, -15.0), (6.85, 16.0, -10.4), "iron", decor={"all": "blade"})
    m.cube(ax, "beard", (6.15, 13.0, -17.0), (6.85, 16.6, -14.6), "iron", rot=("x", -22.5), pivot=(6.5, 15, -15))
    m.ZERO_BONES += ["axe", "shield", "cape"]
    GM.human_idle(m, arm_r=(-25, 0, 8), arm_l=(-30, 30, -6),
                  extra=lambda a, t, s: (a.rot("axe", t, 40, 0, 0), a.rot("cape", t, 4 * s, 0, 0)))
    GM.human_walk(m, leg=24, arm=10, arm_r=(-30, 0, 8), arm_l=(-35, 30, -6),
                  extra=lambda a, t, s: (a.rot("axe", t, 40, 0, 0), a.rot("cape", t, 8 + 4 * s, 0, 0)))
    a = m.anim("attack", 0.8, "once")          # doble hachazo (0.2 y 0.4 s)
    a.rest(0)
    a.pose(0.1, {"right_arm": (-160, 0, 15), "axe": (50, 0, 0), "torso": (-5, 15, 0)})
    a.pose(0.2, {"right_arm": (-60, 0, -10), "axe": (0, 0, 0), "torso": (12, -10, 0)}, i="linear")
    a.pose(0.3, {"right_arm": (-90, 60, 20), "axe": (20, 30, 0), "torso": (0, 30, 0)})
    a.pose(0.4, {"right_arm": (-90, -50, -10), "axe": (20, -30, 0), "torso": (5, -30, 0)}, i="linear")
    a.rest(0.8)
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-170, 0, 10), "axe": (70, 0, 0), "h_head": (-20, 0, 0)})
    GM.human_death(m)
    return m


BUILDERS = {"ragnarok": build_ragnarok, "draugr": build_draugr, "spectral_valkyrie": build_spectral_valkyrie,
            "viking_warrior": build_viking_warrior}
SHOTS = {
    "ragnarok": [("rest", 0, -30), ("rest", 0, 150), ("blow", 0.15, -60), ("lightning", 0.5, -30)],
    "draugr": [("idle", 0.5, -30), ("rest", 0, 150), ("attack", 0.2, -60), ("attack", 0.35, -60)],
    "spectral_valkyrie": [("idle", 0.3, -30), ("idle", 0.3, 150), ("walk", 0.2, -80), ("attack", 0.25, -60)],
    "viking_warrior": [("rest", 0, -30), ("rest", 0, 150), ("attack", 0.1, -60), ("attack", 0.4, -60)],
}
VIEW = {"ragnarok": (32, 4.6)}


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
