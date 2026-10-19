#!/usr/bin/env python3
"""
Boss 07 - LADY OF LAMENTS y sus subditos (modelos de ModelEngine).

  lady_of_laments   reina espectral: corona de amatista, velo, cuello gotico en abanico, melena blanca,
                    corse con encaje, mangas acampanadas, vestido en capas con cola, linterna de almas
                    y cetro de cristal; flota
  banshee           banshee que grita, con melena y vestido que acaba en jirones (VEX)
  lament_shadow     sombra del duelo: bestia de humo negro con ojos rosas y pinchos (ENDERMITE)
  tormented_spirit  mascara que llora con jirones y cadenas (ALLAY)
  castle_vindicator verdugo encapuchado con hacha grande y tabardo morado (VINDICATOR)

Uso: python3 tools/b07_lady.py [modelo ...] [--no-preview]
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

ROOT = Path(__file__).resolve().parent.parent / "Modelos/07_LadyOfLaments"
BLUEPRINTS = ROOT / "ModelEngine/blueprints"
PREVIEW = ROOT / "preview"

GLOW = (226, 150, 255)

MATS = {
    "pale": ((214, 206, 226), 5), "gown": ((58, 26, 80), 6), "gown_dark": ((30, 14, 42), 4),
    "lace": ((140, 90, 180), 6), "amethyst": ((170, 100, 230), 6), "amethyst_dark": ((100, 50, 160), 6),
    "glow": ((226, 150, 255), 3), "gold": ((214, 170, 70), 8), "hair": ((232, 228, 240), 6),
    "black": ((18, 14, 22), 3), "smoke": ((40, 30, 50), 5), "chain": ((120, 116, 130), 5),
    "spectral": ((200, 180, 240), 5), "spectral_dark": ((110, 80, 160), 6), "mask": ((236, 232, 226), 3),
    "leather": ((70, 46, 30), 7), "iron": ((96, 96, 106), 5), "wood": ((96, 64, 38), 8), "skin": ((172, 140, 120), 7),
    "purple": ((110, 40, 140), 6), "bronze": ((196, 140, 58), 8), "hitbox": ((255, 255, 255), 0),
}


def gothic_decor(m):
    D = m.decor

    @D
    def d_lady_face(f):
        w = f.w
        for ex in (2, w - 5):
            f.rect(ex, 6, ex + 3, 8, (30, 10, 40))
            f.rect(ex, 6, ex + 3, 7, GLOW)
            for y in range(8, f.h - 2):                 # lagrimas
                f.put(ex + 1, y, (90, 40, 120))
        f.rect(w // 2 - 2, f.h - 3, w // 2 + 2, f.h - 2, (60, 20, 70))

    @D
    def d_lace(f):
        if f.name in ("up", "down"):
            return
        for y in range(f.h):
            for x in range(f.w):
                if (x + y) % 4 == 0 or (x - y) % 4 == 0:
                    f.put(x, y, m.MAT["lace"])

    @D
    def d_gown(f):
        for x in range(0, f.w, 3):
            for y in range(f.h):
                f.shade(x, y, 0.75)
        if f.name not in ("up", "down"):
            for x in range(f.w):
                f.put(x, f.h - 1, m.MAT["lace"])
                if x % 2:
                    f.put(x, f.h - 2, m.MAT["lace"])

    @D
    def d_crystal(f):
        for y in range(f.h):
            f.put(0, y, (250, 230, 255))
            if f.w > 2:
                f.put(f.w - 1, y, m.MAT["amethyst_dark"])

    @D
    def d_wisp(f):
        for y in range(f.h):
            for x in range(f.w):
                if (x * 3 + y * 5) % 7 == 0:
                    f.shade(x, y, 1.25)
                elif (x + y * 2) % 9 == 0:
                    f.shade(x, y, 0.8)

    @D
    def d_hair(f):
        for x in range(0, f.w, 2):
            for y in range(f.h):
                f.shade(x, y, 0.88)

    @D
    def d_banshee_face(f):
        w = f.w
        for ex in (1, w - 4):
            f.rect(ex, 4, ex + 3, 7, (20, 10, 30))
            f.put(ex + 1, 5, GLOW)
        f.rect(w // 2 - 2, 8, w // 2 + 2, f.h - 1, (20, 10, 30))

    @D
    def d_tragedy(f):
        """Mascara de tragedia: ojos y boca hacia abajo, lagrimas."""
        if f.name != "north":
            return
        w, h = f.w, f.h
        dark = (30, 20, 40)
        for ex in (2, w - 5):
            f.rect(ex, 4, ex + 3, 6, dark)
            f.put(ex + 1, 5, GLOW)
            for y in range(6, h - 2):
                f.put(ex + 1, y, (120, 80, 170))
        f.rect(w // 2 - 3, h - 4, w // 2 + 3, h - 3, dark)
        f.put(w // 2 - 4, h - 3, dark)
        f.put(w // 2 + 3, h - 3, dark)

    @D
    def d_hood(f):
        if f.name != "north":
            return
        w = f.w
        for ex in (2, w - 5):
            f.rect(ex, 6, ex + 3, 8, (8, 6, 10))
            f.put(ex + 1, 7, (200, 60, 60))

    @D
    def d_shadow_eyes(f):
        if f.name != "north":
            return
        for ex in (1, f.w - 3):
            f.rect(ex, 2, ex + 2, 3, (255, 120, 210))

    @D
    def d_tabard(f):
        if f.name not in ("north", "south"):
            return
        cx, cy = f.w // 2, min(6, f.h // 2)
        for d in range(3):
            for dx, dy in ((d, 2 - d), (-d, 2 - d), (d, d - 2), (-d, d - 2)):
                f.put(cx + dx, cy + dy, m.MAT["gold"])
        f.put(cx, cy, m.MAT["glow"])


def _model(name, seed, atlas=256):
    m = Model(name, MATS, seed=seed, atlas_w=atlas)
    m.SHINE |= {"amethyst", "gold", "glow", "iron"}
    m.WOOD |= {"wood"}
    GM.add_common_decor(m)
    gothic_decor(m)
    return m


G = {"decor": {"all": "gown"}}
CR = {"decor": {"all": "crystal"}}


def crystal(m, bone, name, x, y, z, h, w, rot=None, mat="amethyst"):
    m.cube(bone, name, (x - w, y, z - w), (x + w, y + h, z + w), mat, rot=rot, pivot=(x, y, z), **CR)
    m.cube(bone, name + "_tip", (x - w * 0.5, y + h, z - w * 0.5), (x + w * 0.5, y + h + w * 1.6, z + w * 0.5), "glow",
           rot=rot, pivot=(x, y, z))


# ===========================================================================
# LADY OF LAMENTS
# ===========================================================================
def lady_head(m, hd):
    m.cube(hd, "face", (-2.9, 25.0, -3.0), (2.9, 31.0, 3.0), "pale", decor={"north": "lady_face"})
    m.cube(hd, "chin", (-2.0, 24.4, -3.0), (2.0, 25.4, 1.0), "pale")
    m.cube(hd, "hair_top", (-3.2, 29.6, -3.2), (3.2, 31.6, 3.4), "hair", decor={"all": "hair"})
    m.cube(hd, "hair_back", (-3.4, 14.0, 2.4), (3.4, 31.0, 3.8), "hair", decor={"all": "hair"})
    m.cube_lr(hd, hd, "hair_side", (2.8, 18.0, -1.6), (3.6, 30.4, 3.0), "hair", rot=("z", 22.5), pivot=(3.2, 30, 0),
              decor={"all": "hair"})
    # corona de amatista
    m.cube(hd, "crown_band", (-3.3, 31.2, -3.3), (3.3, 32.0, 3.5), "gold", decor={"all": "gold_band"} if "gold_band" in m.DECOR else None)
    for i, (x, z, h, rot) in enumerate(((0, -3.2, 4.2, None), (-2.2, -2.6, 3.0, ("z", 22.5)), (2.2, -2.6, 3.0, ("z", -22.5)),
                                        (-3.1, 0.4, 2.4, ("z", 22.5)), (3.1, 0.4, 2.4, ("z", -22.5)), (0, 3.2, 2.6, ("x", 22.5)))):
        crystal(m, hd, f"crown{i}", x, 31.6, z, h, 0.55 if i else 0.75, rot)
    # velo
    m.cube(hd, "veil", (-3.6, 18.0, 3.6), (3.6, 32.0, 4.0), "gown_dark", rot=("x", 22.5), pivot=(0, 32, 3.8),
           decor={"all": "lace"})


def build_lady():
    m = _model("lady_of_laments", 707)
    H = AN.humanoid(m, k=0.95, mats={"skin": "gown", "hand": "pale", "neck": "pale", "foot": "gown_dark"},
                    head=lady_head)
    torso, waist = H["torso"], H["waist"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    for c in m.CUBES:
        if c.mat == "gown":
            c.decor.setdefault("all", "gown")
    # corse con encaje y cuello gotico en abanico
    m.cube(torso, "corset", (-4.2, 15.6, -2.9), (4.2, 22.0, 2.7), "black", decor={"all": "lace"})
    m.cube(torso, "bodice", (-4.6, 21.4, -3.1), (4.6, 23.8, 2.9), "gown", **G)
    m.cube(torso, "brooch", (-0.9, 20.0, -3.3), (0.9, 21.8, -2.8), "glow", **CR)
    for i, (ang, x) in enumerate(((-45, -3.8), (-22.5, -1.9), (0, 0.0), (22.5, 1.9), (45, 3.8))):
        m.cube(torso, f"ruff{i}", (x - 1.2, 23.6, 2.0), (x + 1.2, 31.0, 2.6), "lace", rot=("z", ang) if ang else None,
               pivot=(x * 0.4, 23.6, 2.3), decor={"all": "lace"})
    # mangas acampanadas
    m.cube_lr(AR[1], AL[1], "bell_sleeve", (4.6, 10.0, -2.6), (8.4, 15.0, 2.6), "gown", rot=("z", 22.5),
              pivot=(6.5, 15, 0), **G)
    m.cube_lr(AR[1], AL[1], "sleeve_trim", (4.4, 9.4, -2.8), (8.6, 10.2, 2.8), "lace", rot=("z", 22.5), pivot=(6.5, 15, 0))
    # vestido en tres capas con cola
    m.cube(waist, "gown_hip", (-4.6, 9.0, -3.2), (4.6, 15.0, 3.2), "gown", **G)
    m.cube(waist, "gown_mid", (-5.4, 3.0, -3.9), (5.4, 9.4, 4.0), "gown", **G)
    m.cube(waist, "gown_low", (-6.4, 0.0, -4.7), (6.4, 3.4, 4.9), "gown_dark", **G)
    m.cube_lr(waist, waist, "gown_flare", (5.0, 0.4, -3.8), (5.8, 9.0, 3.8), "gown", rot=("z", 22.5), pivot=(5.4, 9, 0), **G)
    m.cube(m.BONES["skirt_back"], "train", (-4.6, -0.4, 3.6), (4.6, 10.0, 4.4), "gown_dark", rot=("x", 22.5),
           pivot=(0, 10, 4.0), decor={"all": "lace"})
    m.cube(m.BONES["skirt_front"], "apron", (-2.4, 1.0, -4.3), (2.4, 13.0, -3.8), "lace", decor={"all": "lace"})
    # cadenas espectrales en las munecas
    for side, sx, arm in (("r", 1, AR), ("l", -1, AL)):
        for j in range(3):
            m.cube(arm[1], f"chain_{side}{j}", (6.5 * sx - 0.35, 10.4 - j * 1.6, 1.4), (6.5 * sx + 0.35, 11.8 - j * 1.6, 1.9),
                   "chain")
    # cetro de cristal (mano derecha) y linterna de almas (mano izquierda)
    sc = m.bone("scepter", (6.5, 10.0, 0), AR[2])
    m.cube(sc, "shaft", (6.1, 9.6, -16.0), (6.9, 10.4, 4.0), "black")
    m.cube(sc, "cradle", (5.6, 9.1, -17.0), (7.4, 10.9, -15.6), "gold")
    crystal(m, sc, "orb", 6.5, 10.0, -17.0, 0.1, 1.6)
    m.cube(sc, "gem", (5.4, 8.8, -20.6), (7.6, 11.2, -17.4), "amethyst", rot=("x", 45), pivot=(6.5, 10, -19), **CR)
    ln = m.bone("lantern", (-6.5, 9.0, 0), AL[2])
    m.cube(ln, "lantern_chain", (-6.8, 4.6, -0.3), (-6.2, 9.0, 0.3), "chain")
    m.cube(ln, "lantern_cage", (-8.0, 0.6, -1.5), (-5.0, 4.8, 1.5), "black")
    m.cube(ln, "lantern_flame", (-7.6, 1.2, -1.1), (-5.4, 4.2, 1.1), "glow")
    m.cube(ln, "lantern_top", (-7.8, 4.6, -1.3), (-5.2, 5.4, 1.3), "gold")
    m.ZERO_BONES += ["scepter", "lantern"]

    float_legs = {"right_leg": (0, 0, 0), "left_leg": (0, 0, 0)}

    def drift(a, t, s):
        a.rot("lantern", t, 6 * s, 0, 4 * s)
        a.rot("skirt_back", t, 4 + 4 * s, 0, 0)

    GM.human_idle(m, arm_r=(-25, 0, 10), arm_l=(-15, 0, -12),
                  extra=lambda a, t, s: (drift(a, t, s), a.rot("scepter", t, 70, 0, 0), a.pos("body", t, 0, 0.8 * s, 0)))
    a = m.anim("walk", 1.6, "loop")             # se desliza flotando
    for t, s in ((0, 0), (0.8, 1), (1.6, 0)):
        a.pos("body", t, 0, 0.6 * s, 0)
        a.rot("torso", t, 6, 3 * s - 1.5, 0)
        a.rot("right_arm", t, -25, 0, 10)
        a.rot("left_arm", t, -20 + 6 * s, 0, -12)
        a.rot("scepter", t, 70, 0, 0)
        a.rot("skirt_back", t, 14 + 4 * s, 0, 0)
        a.rot("skirt_front", t, -6, 0, 0)
        drift(a, t, s)

    def anim(name, length, keys):
        a = m.anim(name, length, "once")
        a.rest(0)
        for t, pose, lin in keys:
            a.pose(t, pose, i="linear" if lin else "catmullrom")
        a.rest(length)
        return a

    anim("attack", 0.7, [(0.15, {"right_arm": (-150, 0, 20), "scepter": (60, 0, 0), "torso": (-6, 15, 0)}, False),
                         (0.3, {"right_arm": (-60, 0, -15), "scepter": (10, 0, 0), "torso": (12, -12, 0)}, True)])
    scream = {"h_head": (-35, 0, 0), "torso": (-15, 0, 0), "right_arm": (-40, 0, 70), "left_arm": (-40, 0, -70)}
    anim("wail", 1.0, [(0.18, scream, True), (0.6, scream, False)])
    anim("shroud", 1.0, [(0.2, {"left_arm": (-120, -50, 0), "right_arm": (-120, 50, 0), "torso": (10, 0, 0)}, False),
                         (0.4, {"left_arm": (-60, 60, -40), "right_arm": (-60, -60, 40), "torso": (-6, 0, 0)}, True)])
    anim("siphon", 1.0, [(0.2, {"left_arm": (-95, 0, 0), "h_head": (-6, 0, 0)}, False),
                         (0.4, {"left_arm": (-60, 0, -10), "torso": (-8, 0, 0), "h_head": (-15, 0, 0)}, True),
                         (0.7, {"left_arm": (-55, 0, -10), "torso": (-8, 0, 0)}, False)])
    mark = {"right_arm": (-100, 0, 0), "scepter": (10, 0, 0), "h_head": (0, -8, 0)}
    anim("mark", 1.4, [(0.3, mark, False), (1.1, mark, False),
                       (1.2, {"right_arm": (-130, 0, 10), "scepter": (40, 0, 0)}, True)])
    anim("sorrow", 1.0, [(0.3, {"right_arm": (-70, -50, 0), "left_arm": (-70, 50, 0), "h_head": (20, 0, 0),
                                "torso": (15, 0, 0)}, False),
                         (0.5, {"right_arm": (-40, 0, 70), "left_arm": (-40, 0, -70), "h_head": (-25, 0, 0),
                                "torso": (-10, 0, 0)}, True)])
    rise = {"body": {"p": (0, 4, 0)}, "h_head": (-35, 0, 0), "torso": (-15, 0, 0), "right_arm": (-60, 0, 80),
            "left_arm": (-60, 0, -80), "scepter": (40, 0, 0)}
    anim("lament", 1.4, [(0.45, {**rise, "body": {"p": (0, 3, 0)}}, False), (0.6, rise, True), (1.0, rise, False)])
    anim("storm", 1.2, [(0.35, {"right_arm": (-178, 0, 5), "scepter": (75, 0, 0), "h_head": (-30, 0, 0)}, False),
                        (0.8, {"right_arm": (-178, 0, 5), "scepter": (75, 0, 0), "h_head": (-30, 0, 0)}, False)])
    anim("summon", 1.4, [(0.4, {"left_arm": (-170, 0, -10), "lantern": (0, 0, 0), "h_head": (-20, 0, 0)}, False),
                         (1.0, {"left_arm": (-170, 0, -10), "h_head": (-20, 0, 0)}, False)])
    anim("phase_change", 1.8, [(0.5, {"torso": (35, 0, 0), "h_head": (30, 0, 0), "right_arm": (-30, -30, 20),
                                      "left_arm": (-30, 30, -20)}, False),
                               (0.8, {"torso": (35, 0, 0), "h_head": (30, 0, 0)}, False),
                               (1.2, {**scream, "body": {"p": (0, 3, 0)}}, True), (1.5, scream, False)])
    GM.human_hurt(m)
    a = m.anim("spawn", 2.0, "once")             # emerge del suelo envuelta en el vestido
    a.pos("body", 0, 0, -24, 0)
    a.pose(0, {"torso": (30, 0, 0), "h_head": (30, 0, 0), "right_arm": (-20, 0, 10), "left_arm": (-20, 0, -10)})
    a.pos("body", 1.0, 0, 0, 0)
    a.pose(1.4, {**scream, "body": {"p": (0, 2, 0)}})
    a.rest(2.0)
    a = m.anim("death", 2.4, "hold")             # se deshace en el aire
    a.rest(0)
    a.pose(0.5, {**scream, "body": {"p": (0, 4, 0)}})
    a.scl("body", 0.5, 1)
    a.scl("body", 2.4, 0.05, 1.6, 0.05)
    a.pos("body", 2.4, 0, 18, 0)
    m.scale(1.5)
    return m


# ===========================================================================
# BANSHEE (VEX)
# ===========================================================================
def build_banshee():
    m = _model("banshee", 7071)
    root = m.root
    hb = m.bone("hitbox", (0, 14, 0), root)
    m.cube(hb, "hitbox", (-4, 4, -4), (4, 26, 4), "hitbox")
    m.bone("tag_name", (0, 30, 0), root)
    body = m.bone("body", (0, 16, 0), root)
    m.cube(body, "torso", (-2.6, 14, -1.8), (2.6, 21, 2.0), "spectral_dark", decor={"all": "wisp"})
    m.cube(body, "dress", (-3.4, 8, -2.4), (3.4, 14.4, 2.6), "spectral_dark", decor={"all": "wisp"})
    m.cube_lr(body, body, "dress_s", (3.0, 4.6, -2.2), (3.8, 12.0, 2.4), "spectral_dark", rot=("z", 22.5),
              pivot=(3.4, 12, 0), decor={"all": "wisp"})
    t = m.bone("tail", (0, 8, 0), body)
    m.cube(t, "tail", (-2.4, 2.0, -1.6), (2.4, 8.2, 1.8), "spectral_dark", rot=("x", 22.5), pivot=(0, 8, 0), decor={"all": "wisp"})
    hd = m.bone("h_head", (0, 21, 0), body)
    m.cube(hd, "face", (-2.4, 21.2, -2.4), (2.4, 26.0, 2.2), "spectral", decor={"north": "banshee_face"})
    m.cube(hd, "hair", (-2.8, 22.0, 1.6), (2.8, 26.6, 3.0), "hair", decor={"all": "hair"})
    m.cube(hd, "hair_long", (-2.4, 12.0, 2.4), (2.4, 22.4, 3.2), "hair", rot=("x", 22.5), pivot=(0, 22, 2.8), decor={"all": "hair"})
    for side, sx in (("right", 1), ("left", -1)):
        arm = m.bone(f"{side}_arm", (3.2 * sx, 20.4, 0), body)
        m.cube(arm, f"{side}_arm", (2.6 * sx - 0.9, 12.6, -0.9), (2.6 * sx + 0.9, 20.8, 0.9), "spectral")
        m.cube(arm, f"{side}_sleeve", (2.6 * sx - 1.4, 14.0, -1.4), (2.6 * sx + 1.4, 18.0, 1.4), "spectral_dark",
               decor={"all": "wisp"})
    m.ZERO_BONES = ["body", "h_head", "right_arm", "left_arm", "tail"]
    a = m.anim("idle", 1.6, "loop")
    for t, s in ((0, 0), (0.8, 1), (1.6, 0)):
        a.pos("body", t, 0, 0.8 * s, 0)
        a.rot("tail", t, 10 * s, 0, 0)
        a.rot("right_arm", t, -60 + 8 * s, 0, 10)
        a.rot("left_arm", t, -60 - 8 * s, 0, -10)
    a = m.anim("walk", 0.8, "loop")
    for t, s in ((0, 0), (0.4, 1), (0.8, 0)):
        a.rot("body", t, 25, 0, 3 * s)
        a.rot("tail", t, 20 + 10 * s, 0, 0)
        a.rot("right_arm", t, -100, 0, 10)
        a.rot("left_arm", t, -100, 0, -10)
    a = m.anim("attack", 0.6, "once")           # grito
    a.rest(0)
    a.pose(0.2, {"h_head": (-35, 0, 0), "right_arm": (-60, 0, 70), "left_arm": (-60, 0, -70), "body": (-10, 0, 0)})
    a.rest(0.6)
    a = m.anim("hurt", 0.3, "once")
    a.rest(0, ["h_head", "body"])
    a.pose(0.08, {"h_head": (-20, 0, 10), "body": (-10, 0, 0)})
    a.rest(0.3, ["h_head", "body"])
    a = m.anim("spawn", 1.0, "once")
    a.scl("body", 0, 0.1)
    a.scl("body", 0.6, 1.1)
    a.scl("body", 1.0, 1)
    a = m.anim("death", 1.0, "hold")
    a.scl("body", 0, 1)
    a.scl("body", 1.0, 0.05, 1.5, 0.05)
    a.pos("body", 1.0, 0, 8, 0)
    return m


# ===========================================================================
# SOMBRA DEL DUELO (ENDERMITE)
# ===========================================================================
def build_lament_shadow():
    m = _model("lament_shadow", 7072, atlas=128)
    root = m.root
    hb = m.bone("hitbox", (0, 3, 0), root)
    m.cube(hb, "hitbox", (-3, 0, -3), (3, 6, 3), "hitbox")
    m.bone("tag_name", (0, 12, 0), root)
    body = m.bone("body", (0, 5, 0), root)
    m.cube(body, "body", (-2.6, 3.4, -4.4), (2.6, 7.4, 4.0), "smoke", decor={"all": "wisp"})
    for i, z in enumerate((-2.4, 0.0, 2.4)):
        m.cube(body, f"spike{i}", (-0.5, 7.0, z - 0.5), (0.5, 9.6 - i * 0.4, z + 0.5), "black", rot=("x", 22.5), pivot=(0, 7, z))
    hd = m.bone("head", (0, 6, -4.4), body)
    m.cube(hd, "head", (-2.2, 4.2, -8.2), (2.2, 8.0, -4.2), "black", decor={"north": "shadow_eyes"})
    m.cube(hd, "snout", (-1.4, 4.2, -9.6), (1.4, 6.2, -8.0), "black")
    m.cube_lr(hd, hd, "ear", (0.8, 7.6, -6.0), (1.8, 10.0, -5.0), "black", rot=("z", -22.5), pivot=(1.3, 7.6, -5.5))
    for n, x, z in (("leg_fr", 1.8, -3.0), ("leg_fl", -1.8, -3.0), ("leg_br", 1.8, 2.6), ("leg_bl", -1.8, 2.6)):
        lg = m.bone(n, (x, 4.0, z), body)
        m.cube(lg, n, (x - 0.8, 0, z - 0.8), (x + 0.8, 4.2, z + 0.8), "smoke")
    tl = m.bone("tail", (0, 6, 4.0), body)
    m.cube(tl, "tail", (-0.8, 5.2, 4.0), (0.8, 6.8, 9.0), "smoke", rot=("x", -22.5), pivot=(0, 6, 4), decor={"all": "wisp"})
    m.ZERO_BONES = ["body", "head", "leg_fr", "leg_fl", "leg_br", "leg_bl", "tail"]
    a = m.anim("idle", 1.6, "loop")
    for t, s in ((0, 0), (0.8, 1), (1.6, 0)):
        a.pos("body", t, 0, 0.3 * s, 0)
        a.rot("tail", t, 0, 20 * s - 10, 0)
        a.rot("head", t, 5 * s, 0, 0)
    a = m.anim("walk", 0.5, "loop")
    for t, s in ((0, 1), (0.25, -1), (0.5, 1)):
        a.rot("leg_fr", t, 35 * s, 0, 0)
        a.rot("leg_bl", t, 35 * s, 0, 0)
        a.rot("leg_fl", t, -35 * s, 0, 0)
        a.rot("leg_br", t, -35 * s, 0, 0)
        a.rot("tail", t, 0, 15 * s, 0)
    a = m.anim("attack", 0.5, "once")
    a.rest(0)
    a.pose(0.12, {"head": (-25, 0, 0), "body": (-10, 0, 0)})
    a.pose(0.22, {"head": (20, 0, 0), "body": (10, 0, 0)}, i="linear")
    a.rest(0.5)
    a = m.anim("hurt", 0.3, "once")
    a.rest(0, ["head"])
    a.pose(0.08, {"head": (-20, 0, 0)})
    a.rest(0.3, ["head"])
    a = m.anim("spawn", 0.8, "once")
    a.scl("body", 0, 0.1)
    a.scl("body", 0.5, 1.1)
    a.scl("body", 0.8, 1)
    a = m.anim("death", 0.8, "hold")
    a.scl("body", 0, 1)
    a.scl("body", 0.8, 1.5, 0.05, 1.5)
    return m


# ===========================================================================
# ESPIRITU ATORMENTADO (ALLAY)
# ===========================================================================
def build_tormented_spirit():
    m = _model("tormented_spirit", 7073, atlas=128)
    root = m.root
    hb = m.bone("hitbox", (0, 8, 0), root)
    m.cube(hb, "hitbox", (-4, 2, -4), (4, 14, 4), "hitbox")
    m.bone("tag_name", (0, 20, 0), root)
    body = m.bone("body", (0, 8, 0), root)
    m.cube(body, "mask", (-3.0, 7.6, -2.6), (3.0, 14.0, -1.6), "mask", decor={"north": "tragedy"})
    m.cube(body, "mask_brow", (-3.2, 12.6, -2.9), (3.2, 13.4, -1.8), "mask")
    m.cube(body, "hood", (-3.4, 7.0, -1.8), (3.4, 14.6, 2.8), "spectral_dark", decor={"all": "wisp"})
    wisp = m.bone("wisp", (0, 7, 0), body)
    for k, (w, y0, y1) in enumerate(((2.8, 3.6, 7.2), (2.0, 0.8, 3.8), (1.2, -1.6, 1.0))):
        m.cube(wisp, f"w{k}", (-w, y0, -w * 0.8 + 0.4), (w, y1, w * 0.8 + 0.4), "spectral" if k % 2 else "spectral_dark",
               decor={"all": "wisp"})
    for j in range(4):
        m.cube(wisp, f"chain{j}", (2.4, 6.0 - j * 1.6, -0.3), (3.0, 7.4 - j * 1.6, 0.3), "chain")
        m.cube(wisp, f"chain_l{j}", (-3.0, 5.6 - j * 1.6, -0.3), (-2.4, 7.0 - j * 1.6, 0.3), "chain")
    m.ZERO_BONES = ["body", "wisp"]
    a = m.anim("idle", 2.0, "loop")
    for t, s in ((0, 0), (1.0, 1), (2.0, 0)):
        a.pos("body", t, 0, 1.0 * s, 0)
        a.rot("wisp", t, 0, 0, 10 * s - 5)
        a.rot("body", t, 0, 8 * s - 4, 0)
    a = m.anim("walk", 1.0, "loop")
    for t, s in ((0, 0), (0.5, 1), (1.0, 0)):
        a.rot("body", t, 15, 0, 0)
        a.rot("wisp", t, -20, 0, 8 * s - 4)
    a = m.anim("attack", 0.8, "once")           # absorbe vida
    a.scl("body", 0, 1)
    a.scl("body", 0.3, 1.25)
    a.scl("body", 0.8, 1)
    a = m.anim("hurt", 0.3, "once")
    a.rot("body", 0, 0, 0, 0)
    a.rot("body", 0.08, -20, 0, 10)
    a.rot("body", 0.3, 0, 0, 0)
    a = m.anim("spawn", 1.0, "once")
    a.scl("body", 0, 0.1)
    a.scl("body", 0.6, 1.1)
    a.scl("body", 1.0, 1)
    a = m.anim("death", 1.0, "hold")
    a.scl("body", 0, 1)
    a.scl("body", 1.0, 0.05, 1.5, 0.05)
    a.pos("body", 1.0, 0, 8, 0)
    return m


# ===========================================================================
# VERDUGO DEL CASTILLO (VINDICATOR)
# ===========================================================================
def build_castle_vindicator():
    m = _model("castle_vindicator", 7074)

    def head(m, hd):
        m.cube(hd, "hood", (-3.6, 24.6, -3.6), (3.6, 31.6, 3.8), "black", decor={"north": "hood"})
        m.cube(hd, "hood_tip", (-2.4, 31.4, -1.6), (2.4, 34.4, 2.8), "black", rot=("x", 22.5), pivot=(0, 31.4, 0))
        m.cube(hd, "mantle", (-4.6, 23.0, -3.4), (4.6, 25.0, 3.6), "black")

    H = AN.humanoid(m, k=1.1, mats={"skin": "skin", "chest": "leather", "belly": "leather", "thigh": "black",
                                     "shin": "black", "foot": "leather"}, head=head)
    torso, waist = H["torso"], H["waist"]
    AR = H["arms"]["right"]
    m.cube(torso, "tabard", (-3.4, 14.6, -3.4), (3.4, 23.0, -2.8), "purple", decor={"all": "tabard"})
    m.cube(m.BONES["skirt_front"], "tabard_low", (-3.0, 6.4, -3.4), (3.0, 13.4, -2.8), "purple", decor={"all": "tabard"})
    m.cube(waist, "belt", (-4.6, 13.0, -2.8), (4.6, 14.8, 2.8), "leather")
    m.cube_lr(H["arms"]["right"][1], H["arms"]["left"][1], "bracer", (5.0, 12.0, -1.9), (8.0, 15.6, 1.9), "leather")
    ax = m.bone("axe", (6.5, 10.0, 0), AR[2])
    m.cube(ax, "haft", (6.1, 9.5, -22.0), (6.9, 10.5, 4.0), "wood")
    m.cube(ax, "head", (6.1, 6.0, -24.0), (6.9, 16.0, -16.0), "iron", decor={"all": "blade"})
    m.cube(ax, "beard", (6.1, 3.0, -25.0), (6.9, 8.0, -20.0), "iron", rot=("x", 22.5), pivot=(6.5, 6, -20))
    m.ZERO_BONES += ["axe"]
    GM.human_idle(m, arm_r=(-25, 0, 8), extra=lambda a, t, s: a.rot("axe", t, 50, 0, 0))
    GM.human_walk(m, leg=22, arm=10, lean=6, arm_r=(-25, 0, 8), extra=lambda a, t, s: a.rot("axe", t, 50, 0, 0))
    a = m.anim("attack", 0.8, "once")           # hachazo de verdugo (0.35 s)
    a.rest(0)
    a.pose(0.2, {"right_arm": (-175, 0, 0), "left_arm": (-170, 0, 0), "axe": (70, 0, 0), "torso": (-12, 0, 0)})
    a.pose(0.35, {"right_arm": (-60, 0, 0), "left_arm": (-60, 0, 0), "axe": (0, 0, 0), "torso": (25, 0, 0)}, i="linear")
    a.rest(0.8)
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-170, 0, 10), "axe": (70, 0, 0), "h_head": (-15, 0, 0)})
    GM.human_death(m)
    return m


BUILDERS = {"lady_of_laments": build_lady, "banshee": build_banshee, "lament_shadow": build_lament_shadow,
            "tormented_spirit": build_tormented_spirit, "castle_vindicator": build_castle_vindicator}
SHOTS = {
    "lady_of_laments": [("rest", 0, -30), ("rest", 0, 150), ("wail", 0.3, -40), ("lament", 0.6, -30)],
    "banshee": [("idle", 0.4, -30), ("idle", 0.4, 150), ("walk", 0.2, -80), ("attack", 0.2, -30)],
    "lament_shadow": [("idle", 0.4, -30), ("idle", 0.4, 150), ("walk", 0.1, -80), ("attack", 0.12, -60)],
    "tormented_spirit": [("idle", 0.5, -30), ("idle", 0.5, 150), ("idle", 0.5, -90), ("attack", 0.3, -30)],
    "castle_vindicator": [("rest", 0, -30), ("rest", 0, 150), ("attack", 0.2, -60), ("attack", 0.35, -60)],
}
VIEW = {"lady_of_laments": (32, 4.6), "banshee": (16, 9.0), "lament_shadow": (5, 18.0), "tormented_spirit": (10, 14.0)}


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
