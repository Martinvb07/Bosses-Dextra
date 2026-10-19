#!/usr/bin/env python3
"""
Boss 04 - RED HAND y sus subditos (modelos de ModelEngine).

  red_hand        caballero oscuro caido: yelmo con visor en T encendido, corona rota y cuernos,
                  armadura negra con sangre, hombreras con pinchos, capa carmesi hecha jirones,
                  mandoble de runas rojas y un guantelete rojo gigante en la mano izquierda
  fallen_squire   escudero no muerto con capelina, gambeson y tabardo del castillo (ZOMBIE)
  corrupt_knight  caballero esqueleto con bacinete de hocico, escudo de la mano roja (WITHER_SKELETON)
  condemned_soul  alma en pena encapuchada con cadenas y cola de espectro (VEX)
  rh_blood_pool   charco de sangre que burbujea (RH_BloodPool)

Uso: python3 tools/b04_redhand.py [modelo ...] [--no-preview]
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

ROOT = Path(__file__).resolve().parent.parent / "Modelos/04_RedHand"
BLUEPRINTS = ROOT / "ModelEngine/blueprints"
PREVIEW = ROOT / "preview"

RED_GLOW = (255, 60, 50)

MATS = {
    "iron": ((50, 50, 58), 5), "iron_hi": ((96, 96, 108), 5), "black": ((18, 16, 20), 3),
    "blood": ((140, 12, 18), 7), "glow": ((255, 64, 52), 3), "crimson": ((104, 10, 20), 7),
    "brass": ((150, 108, 48), 8), "leather": ((70, 44, 28), 7), "chain": ((92, 92, 100), 6),
    "bone": ((206, 198, 176), 7), "bone_black": ((48, 44, 46), 5), "rust": ((112, 56, 34), 10),
    "flesh": ((112, 126, 98), 8), "gambeson": ((150, 136, 110), 8), "red": ((168, 24, 30), 6),
    "ghost": ((150, 220, 214), 6), "ghost_dark": ((40, 78, 92), 6), "skin": ((50, 50, 58), 5),
    "wood": ((92, 60, 36), 8), "bronze": ((150, 108, 48), 8), "hitbox": ((255, 255, 255), 0),
}


def gothic_decor(m):
    D = m.decor

    @D
    def d_plate(f):
        """Placa pulida: degradado (claro arriba, oscuro abajo), brillo, filo carmesi y remaches."""
        if f.name in ("up", "down"):
            return
        for y in range(f.h):
            k = 1.35 - 0.7 * y / max(1, f.h - 1)
            for x in range(f.w):
                f.shade(x, y, k)
        for x in range(f.w):
            f.put(x, 0, (150, 150, 165))
            if f.h > 3:
                f.put(x, f.h - 1, (150, 16, 24))
        if f.w > 5 and f.h > 4:
            for x in (1, f.w - 2):
                f.put(x, 2, (210, 170, 90))
        if f.w > 6:
            for y in range(1, f.h - 1):
                f.put(f.w // 2 - 1, y, mul(f.get(f.w // 2 - 1, y), 1.25))

    @D
    def d_visor(f):
        w, h = f.w, f.h
        f.rect(1, 5, w - 1, 7, (10, 8, 10))
        f.rect(w // 2 - 1, 5, w // 2 + 1, h - 2, (10, 8, 10))
        f.rect(2, 5, w - 2, 6, RED_GLOW)
        f.rect(w // 2 - 1, 7, w // 2 + 1, h - 4, (200, 30, 30))
        for y in range(h - 3, h):
            for x in range(1, w - 1, 2):
                f.put(x, y, (24, 20, 24))

    @D
    def d_visor_half(f):
        f.rect(0, 5, f.w, 6, RED_GLOW)
        f.rect(0, 4, f.w, 5, (10, 8, 10))
        f.rect(0, 6, f.w, 7, (10, 8, 10))
        for y in range(f.h - 4, f.h - 1, 2):
            for x in range(1, f.w, 2):
                f.put(x, y, (24, 20, 24))

    @D
    def d_runes(f):
        if f.name in ("east", "west"):
            for x in range(1, f.w - 1, 4):
                f.put(x, f.h // 2, RED_GLOW)
                f.put(x + 1, f.h // 2 - 1, (200, 30, 30))
            for x in range(f.w):
                f.put(x, f.h - 1, (150, 150, 160))

    @D
    def d_veins(f):
        rng = random.Random(f.x0 + f.y0 * 3)
        for _ in range(f.w * f.h // 10):
            x, y = rng.randrange(f.w), rng.randrange(f.h)
            f.put(x, y, RED_GLOW if rng.random() < 0.4 else (200, 30, 30))

    @D
    def d_tatter(f):
        if f.name in ("north", "south"):
            rng = random.Random(f.x0)
            for x in range(f.w):
                cut = rng.randint(0, 3)
                for y in range(f.h - cut, f.h):
                    f.shade(x, y, 0.35)
            for x in range(0, f.w, 5):
                for y in range(f.h):
                    f.shade(x, y, 0.8)

    @D
    def d_chainmail(f):
        for y in range(f.h):
            for x in range(f.w):
                if (x + (y % 2)) % 2 == 0:
                    f.shade(x, y, 0.7)

    @D
    def d_handsigil(f):
        """Mano roja pintada (escudo y tabardo)."""
        if f.name not in ("north", "south"):
            return
        cx, cy = f.w // 2, f.h // 2 + 1
        col = (190, 20, 26)
        f.rect(cx - 2, cy - 1, cx + 2, cy + 3, col)
        for k, dx in enumerate((-2, -1, 0, 1)):
            f.rect(cx + dx, cy - 4 + (k in (0, 3)), cx + dx + 1, cy - 1, col)
        f.rect(cx + 2, cy, cx + 3, cy + 2, col)

    @D
    def d_rusty(f):
        rng = random.Random(f.x0 * 7 + f.y0)
        for _ in range(f.w * f.h // 5):
            f.put(rng.randrange(f.w), rng.randrange(f.h), mul(m.MAT["rust"], rng.uniform(0.8, 1.2)))
        for y in range(2, f.h, 3):
            for x in range(f.w):
                f.shade(x, y, 0.6)

    @D
    def d_quilt(f):
        for y in range(0, f.h, 3):
            for x in range(f.w):
                f.shade(x, y, 0.8)
        for x in range(0, f.w, 3):
            for y in range(f.h):
                f.shade(x, y, 0.85)

    @D
    def d_zombie_face(f):
        w = f.w
        for ex in (2, w - 5):
            f.rect(ex, 6, ex + 3, 8, (16, 12, 10))
            f.put(ex + 1, 7, (240, 220, 60))
        f.rect(w // 2 - 3, 11, w // 2 + 3, 12, (40, 20, 16))

    @D
    def d_skull_face(f):
        w = f.w
        for ex in (1, w - 5):
            f.rect(ex, 3, ex + 4, 7, (14, 10, 12))
            f.put(ex + 2, 5, RED_GLOW)
        f.rect(w // 2 - 1, 7, w // 2 + 1, 9, (20, 14, 16))
        for x in range(2, w - 2, 2):
            f.put(x, f.h - 2, (20, 14, 16))

    @D
    def d_wisp(f):
        for y in range(f.h):
            for x in range(f.w):
                if (x * 3 + y * 5) % 7 == 0:
                    f.shade(x, y, 1.25)
                elif (x + y * 2) % 9 == 0:
                    f.shade(x, y, 0.8)

    @D
    def d_gem(f):
        f.rect(0, 0, f.w, f.h, (120, 10, 14))
        f.rect(1, 1, f.w - 1, f.h - 1, RED_GLOW)
        f.put(1, 1, (255, 220, 210))

    @D
    def d_gold_band(f):
        for x in range(f.w):
            f.put(x, 0, (220, 180, 100))
        for x in range(1, f.w, 3):
            f.put(x, f.h // 2, (120, 10, 14))


def _model(name, seed, extra=None):
    m = Model(name, {**MATS, **(extra or {})}, seed=seed, atlas_w=256)
    m.SHINE |= {"iron", "iron_hi", "brass", "glow"}
    m.WOOD |= {"wood"}
    GM.add_common_decor(m)
    gothic_decor(m)
    return m


P = {"decor": {"all": "plate"}}


# ===========================================================================
# RED HAND
# ===========================================================================
def rh_head(m, hd):
    # yelmo con frente en punta (proa) y visor en T encendido
    m.cube(hd, "helm", (-3.2, 24.8, -3.0), (3.2, 31.6, 3.6), "iron", **P)
    m.cube_lr(hd, hd, "faceplate", (0.0, 24.6, -4.6), (3.6, 31.0, -3.4), "iron", rot=("y", -22.5),
              pivot=(0.0, 28, -4.6), decor={"north": "visor_half", "all": "plate"})
    m.cube(hd, "prow", (-0.5, 24.4, -5.1), (0.5, 31.6, -4.2), "iron_hi")
    m.cube(hd, "helm_top", (-2.6, 31.6, -2.6), (2.6, 32.8, 3.0), "iron", rot=("x", 22.5), pivot=(0, 31.6, 0), **P)
    m.cube(hd, "crest", (-0.5, 31.8, -3.4), (0.5, 34.6, 3.2), "crimson")
    m.cube(hd, "gorget", (-3.9, 23.2, -3.6), (3.9, 25.0, 3.7), "iron", **P)
    # corona rota de pinchos
    m.cube(hd, "crown", (-3.4, 31.2, -3.4), (3.4, 32.0, 3.7), "brass", decor={"all": "gold_band"})
    for i, (x, z, h) in enumerate(((-2.8, -3.0, 2.2), (0, -3.4, 3.4), (2.8, -3.0, 2.2), (-3.1, 0.2, 1.6),
                                    (3.1, 0.2, 1.6))):
        rot = ("z", -22.5 if x > 0 else 22.5) if abs(x) > abs(z) else ("x", 22.5)
        m.cube(hd, f"crown_spike{i}", (x - 0.45, 31.8, z - 0.45), (x + 0.45, 31.8 + h * 0.6, z + 0.45), "brass",
               rot=rot, pivot=(x, 31.8, z))
        m.cube(hd, f"crown_tip{i}", (x - 0.25, 31.8 + h * 0.6, z - 0.25), (x + 0.25, 31.8 + h, z + 0.25), "brass",
               rot=rot, pivot=(x, 31.8, z))
    m.cube(hd, "crown_gem", (-0.6, 31.3, -3.8), (0.6, 32.3, -3.4), "glow", decor={"all": "gem"})
    # cuernos grandes: salen de lado, se curvan hacia arriba y hacia delante
    for side, sx in (("r", 1), ("l", -1)):
        segs = [((3.0, 28.6, -0.4), (3.0 + 3.6 * sx, 0.0), ("z", 0), 1.0),
                (None, None, ("z", -22.5 * sx), 0.85), (None, None, ("z", -45 * sx), 0.65)]
        x, y = 3.0 * sx, 28.6
        for i, (ang, w) in enumerate(((0.0, 1.0), (22.5, 0.85), (45.0, 0.65))):
            ln = 3.2
            frm = (x if sx > 0 else x - ln, y - w * 0.7, -1.2 + i * -0.6)
            to = (x + ln if sx > 0 else x, y + w * 0.7, 0.2 + i * -0.6)
            m.cube(hd, f"horn_{side}{i}", frm, to, "black" if i < 2 else "bone",
                   rot=("z", ang * sx) if ang else None, pivot=(x, y, -0.5))
            x += sx * ln * math.cos(math.radians(ang))
            y += ln * math.sin(math.radians(ang))


def build_red_hand():
    m = _model("red_hand", 404)
    H = AN.humanoid(m, k=1.1, mats={"skin": "black", "foot": "iron", "hand": "iron", "belly": "chain"},
                    head=rh_head)
    torso, waist = H["torso"], H["waist"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    RL, LL = H["legs"]["right"], H["legs"]["left"]
    # peto en V: pecho ancho, laminas que se estrechan hacia la cintura
    m.cube(torso, "breastplate", (-5.6, 20.6, -3.8), (5.6, 24.0, 3.4), "iron", **P)
    m.cube_lr(torso, torso, "breast_wing", (3.6, 20.4, -4.4), (5.9, 23.8, -1.8), "iron", rot=("y", -22.5),
              pivot=(4.6, 22, -3.9), **P)
    m.cube(torso, "breast_prow", (-0.45, 17.6, -4.6), (0.45, 24.0, -3.9), "iron_hi")
    for i, (w, y) in enumerate(((4.8, 18.8), (4.2, 17.2), (3.8, 15.6))):
        m.cube(torso, f"lame{i}", (-w, y, -3.6 + i * 0.2), (w, y + 1.9, 3.1 - i * 0.2), "iron", **P)
    m.cube(torso, "heart_gem", (-0.9, 21.6, -4.5), (0.9, 23.4, -3.9), "glow", decor={"all": "gem"})
    m.cube(torso, "backplate", (-5.0, 17.0, 3.0), (5.0, 23.8, 3.8), "iron", **P)
    # faldar y faldones que se abren
    m.cube(waist, "fauld", (-4.6, 13.0, -3.1), (4.6, 15.6, 2.9), "iron", **P)
    m.cube(m.BONES["skirt_front"], "tabard", (-2.4, 4.0, -3.5), (2.4, 13.4, -3.0), "crimson",
           decor={"north": "handsigil", "all": "tatter"})
    m.cube(m.BONES["skirt_back"], "mail_b", (-3.8, 7.0, 2.8), (3.8, 13.0, 3.3), "chain", decor={"all": "chainmail"})
    m.cube_lr(waist, waist, "tasset", (2.6, 8.6, -3.4), (5.0, 13.4, -2.6), "iron", rot=("x", -22.5),
              pivot=(3.8, 13.4, -3.0), **P)
    m.cube_lr(waist, waist, "tasset_side", (4.4, 8.4, -2.6), (5.1, 13.4, 2.6), "iron", rot=("z", 22.5),
              pivot=(4.7, 13.4, 0), **P)
    # piernas: quijotes, rodilleras con pincho, grebas con arista y escarpes en punta
    m.cube_lr(RL[0], LL[0], "cuisse", (0.5, 9.0, -2.5), (4.5, 13.8, 2.3), "iron", **P)
    m.cube_lr(RL[0], LL[0], "poleyn", (1.0, 6.6, -3.0), (4.0, 9.4, -1.4), "iron_hi", rot=("x", -22.5),
              pivot=(2.5, 8, -2.2))
    m.cube_lr(RL[0], LL[0], "knee_spike", (2.1, 7.4, -4.8), (2.9, 8.4, -2.8), "black", rot=("x", -22.5),
              pivot=(2.5, 7.9, -3))
    m.cube_lr(RL[1], LL[1], "greave", (0.9, 1.6, -2.4), (4.1, 7.2, 2.0), "iron", **P)
    m.cube_lr(RL[1], LL[1], "greave_ridge", (2.15, 1.6, -2.8), (2.85, 7.2, -2.2), "iron_hi")
    m.cube_lr(RL[1], LL[1], "sabaton", (1.0, 0.0, -5.0), (4.0, 1.2, -3.0), "iron", rot=("x", 22.5),
              pivot=(2.5, 0.6, -3.0))
    # hombreras enormes en tres laminas con pinchos curvos
    for i, (ang, y0, y1, x0) in enumerate(((0, 23.4, 26.2, 4.4), (22.5, 21.2, 24.2, 8.2), (45, 18.8, 21.6, 10.0))):
        m.cube_lr(AR[0], AL[0], f"pauldron{i}", (x0, y0, -3.4 + i * 0.2), (x0 + (5.6 if i == 0 else 1.2), y1, 3.4 - i * 0.2),
                  "iron", rot=("z", ang) if ang else None, pivot=(x0, y1, 0), **P)
    for i, z in enumerate((-2.0, 0.2, 2.2)):
        h = 3.6 if i == 1 else 2.6
        m.cube_lr(AR[0], AL[0], f"spike{i}", (6.4, 26.0, z - 0.5), (7.4, 26.0 + h, z + 0.5), "black",
                  rot=("z", -22.5), pivot=(6.9, 26.0, z))
        m.cube_lr(AR[0], AL[0], f"spike_tip{i}", (6.6, 26.0 + h, z - 0.3), (7.2, 27.6 + h, z + 0.3), "black",
                  rot=("z", -45), pivot=(6.9, 26.0, z))
    m.cube(AR[1], "vambrace_r", (5.0, 12.4, -1.9), (8.0, 16.8, 1.9), "iron", **P)
    m.cube(AR[1], "couter_r", (5.2, 16.2, -0.6), (8.0, 18.2, 2.8), "iron_hi", rot=("x", 22.5), pivot=(6.5, 17.2, 1))
    m.cube(AR[2], "gauntlet_r", (5.2, 9.2, -1.6), (7.8, 11.8, 1.6), "iron", **P)
    # LA MANO ROJA: guantelete gigante con garras curvas y venas encendidas
    m.cube(AL[1], "red_vambrace", (-9.0, 11.4, -2.8), (-4.0, 17.4, 2.8), "blood", decor={"all": "veins"})
    m.cube(AL[1], "red_cuff", (-9.4, 16.4, -3.2), (-3.6, 17.8, 3.2), "black")
    for i, z in enumerate((-1.8, 0.0, 1.8)):
        m.cube(AL[1], f"red_spike{i}", (-10.6, 13.0 + i * 1.2, z - 0.45), (-8.8, 14.0 + i * 1.2, z + 0.45), "black",
               rot=("z", 22.5), pivot=(-9.0, 13.5 + i * 1.2, z))
    m.cube(AL[2], "red_palm", (-9.2, 7.4, -2.8), (-3.8, 12.0, 2.8), "blood", decor={"all": "veins"})
    m.cube(AL[2], "red_knuckles", (-9.4, 7.0, -3.2), (-3.6, 8.4, -1.8), "black")
    for i, z in enumerate((-2.1, -0.7, 0.7, 2.1)):
        m.cube(AL[2], f"claw{i}", (-7.2, 4.4, z - 0.55), (-5.8, 7.6, z + 0.55), "blood", rot=("x", -22.5),
               pivot=(-6.5, 7.6, z))
        m.cube(AL[2], f"claw_tip{i}", (-6.9, 1.4, z - 0.35), (-6.1, 4.8, z + 0.35), "glow", rot=("x", -45),
               pivot=(-6.5, 5.0, z - 1.3))
    m.cube(AL[2], "red_thumb", (-4.4, 7.8, -3.4), (-3.2, 11.0, -1.9), "blood", rot=("z", -22.5), pivot=(-3.8, 11, -2.6))
    # capa carmesi larga en tres tramos que se abren hacia atras
    cp = m.bone("cape", (0, 24.2, 3.8), torso)
    m.cube(cp, "cape", (-6.0, 15.0, 3.7), (6.0, 24.4, 4.3), "crimson", decor={"all": "wisp"})
    m.cube(cp, "cape_mid", (-6.4, 6.0, 3.7), (6.4, 15.2, 4.3), "crimson", decor={"all": "wisp"})
    m.cube(cp, "cape_low", (-6.8, -0.6, 3.7), (6.8, 6.2, 4.3), "crimson", rot=("x", 22.5), pivot=(0, 6.1, 4.0),
           decor={"all": "tatter"})
    m.cube(cp, "cape_collar", (-5.6, 23.4, 2.6), (5.6, 25.6, 4.4), "black")
    m.cube_lr(torso, torso, "cape_clasp", (3.4, 22.8, -4.0), (4.8, 24.2, -3.6), "brass")
    # mandoble con runas
    sw = m.bone("sword", (6.5, 10.0, 0), AR[2])
    m.cube(sw, "grip", (6.1, 9.5, -3.2), (6.9, 10.5, 4.2), "leather")
    m.cube(sw, "pommel", (5.9, 9.2, 4.2), (7.1, 10.8, 5.2), "glow", decor={"all": "gem"})
    m.cube(sw, "guard", (3.4, 9.3, -3.8), (9.6, 10.7, -3.1), "iron_hi")
    m.cube_lr(sw, sw, "guard_tip", (9.2, 7.8, -3.8), (9.9, 9.6, -3.1), "iron_hi")
    m.cube(sw, "blade", (6.2, 8.3, -34.0), (6.8, 11.7, -3.8), "black", decor={"all": "runes"})
    m.cube(sw, "blade_tip", (6.2, 9.0, -37.0), (6.8, 11.0, -34.0), "black")
    m.cube(sw, "blade_edge", (6.15, 8.1, -33.0), (6.85, 8.4, -5.0), "glow")
    m.ZERO_BONES += ["sword", "cape"]

    def sway(a, t, s):
        a.rot("cape", t, 5 * s, 0, 0)

    GM.human_idle(m, arm_r=(-25, 0, 8), arm_l=(-10, 0, -10),
                  extra=lambda a, t, s: (sway(a, t, s), a.rot("sword", t, 30, 0, 0), a.rot("torso", t, 4, 0, 0)))
    GM.human_walk(m, leg=20, arm=10, bob=0.9, lean=6, arm_r=(-25, 0, 8),
                  extra=lambda a, t, s: (sway(a, t, s), a.rot("sword", t, 30, 0, 0)))

    a = m.anim("attack", 0.7, "once")          # tajo horizontal (0.3 s)
    a.rest(0)
    a.pose(0.15, {"right_arm": (-90, 60, 20), "torso": (0, 35, 0), "sword": (0, 30, 0)})
    a.pose(0.3, {"right_arm": (-90, -50, -10), "torso": (8, -35, 0), "sword": (0, -20, 0)}, i="linear")
    a.rest(0.7)

    a = m.anim("slash_combo", 1.1, "once")     # tres tajos (0.1, 0.4 y 0.7 s)
    a.rest(0)
    a.pose(0.1, {"right_arm": (-100, -50, -10), "torso": (8, -30, 0), "sword": (0, -20, 0)}, i="linear")
    a.pose(0.25, {"right_arm": (-150, 30, 20), "torso": (-5, 20, 0), "sword": (40, 0, 0)})
    a.pose(0.4, {"right_arm": (-40, 0, -20), "torso": (15, -10, 0), "sword": (-10, 0, 0)}, i="linear")
    a.pose(0.55, {"right_arm": (-90, -60, 0), "torso": (0, -30, 0), "sword": (0, -30, 0)})
    a.pose(0.7, {"right_arm": (-90, 60, 10), "torso": (5, 35, 0), "sword": (0, 30, 0)}, i="linear")
    a.rest(1.1)

    a = m.anim("mark", 0.9, "once")            # señala con la mano roja (0.3 s)
    a.rest(0)
    a.pose(0.3, {"left_arm": (-95, 0, 0), "torso": (2, -20, 0), "h_head": (0, -10, 0)}, i="linear")
    a.pose(0.6, {"left_arm": (-95, 0, 0), "torso": (2, -20, 0)})
    a.rest(0.9)

    a = m.anim("dash", 0.6, "once")            # se agacha y se hunde en las sombras (0.4 s)
    a.rest(0)
    a.pose(0.3, {**GM.KNEEL, "torso": (35, 0, 0), "right_arm": (20, 0, 20), "left_arm": (20, 0, -20)})
    a.pos("body", 0.45, 0, -12, 0)
    a.pos("body", 0.6, 0, 0, 0)
    a.rest(0.6, ["torso", "right_arm", "left_arm", "right_leg", "left_leg", "right_lower_leg", "left_lower_leg"])

    a = m.anim("crush", 1.3, "once")           # alza la mano roja y aplasta el suelo (0.5 s)
    a.rest(0)
    a.pose(0.25, {"left_arm": (-175, 0, -10), "torso": (-12, -10, 0), "h_head": (-15, 0, 0)})
    a.pose(0.5, {**GM.KNEEL, "left_arm": (-60, 0, 0), "torso": (35, -10, 0), "h_head": (10, 0, 0),
                 "right_arm": (-20, 0, 20)}, i="linear")
    a.pose(0.9, {**GM.KNEEL, "left_arm": (-60, 0, 0), "torso": (32, -10, 0), "right_arm": (-20, 0, 20)})
    a.rest(1.3)

    a = m.anim("nova", 1.1, "once")            # recoge sangre y la libera (0.4 s)
    a.rest(0)
    a.pose(0.25, {"right_arm": (-60, -40, 0), "left_arm": (-60, 40, 0), "torso": (15, 0, 0), "h_head": (15, 0, 0)})
    a.pose(0.4, {"right_arm": (-40, 0, 80), "left_arm": (-40, 0, -80), "torso": (-15, 0, 0), "h_head": (-25, 0, 0)},
           i="linear")
    a.pose(0.7, {"right_arm": (-40, 0, 75), "left_arm": (-40, 0, -75), "torso": (-12, 0, 0)})
    a.rest(1.1)

    a = m.anim("pools", 0.8, "once")           # lanza sangre con la mano roja
    a.rest(0)
    a.pose(0.15, {"left_arm": (-60, 60, -20), "torso": (0, 25, 0)})
    a.pose(0.3, {"left_arm": (-80, -50, -10), "torso": (8, -25, 0)}, i="linear")
    a.rest(0.8)

    a = m.anim("execution", 2.6, "once")       # carga el mandoble con las dos manos y lo hunde (2.0 s)
    a.rest(0)
    up = {"right_arm": (-170, 0, -15), "left_arm": (-170, 0, 15), "sword": (70, 0, 0), "torso": (-15, 0, 0),
          "h_head": (-20, 0, 0)}
    a.pose(0.5, up)
    for k, t in enumerate((0.8, 1.1, 1.4, 1.7)):
        a.pose(t, {**up, "torso": (-15 + (2 if k % 2 else -2), 0, 0)})
    a.pose(2.0, {**GM.KNEEL, "right_arm": (-60, 0, -10), "left_arm": (-60, 0, 10), "sword": (-70, 0, 0),
                 "torso": (35, 0, 0), "h_head": (15, 0, 0)}, i="linear")
    a.pose(2.3, {**GM.KNEEL, "right_arm": (-60, 0, -10), "left_arm": (-60, 0, 10), "sword": (-70, 0, 0),
                 "torso": (33, 0, 0)})
    a.rest(2.6)

    a = m.anim("summon", 1.4, "once")          # clava la espada y alza la mano roja
    a.rest(0)
    pose = {"right_arm": (-40, 0, 10), "sword": (-50, 0, 0), "left_arm": (-175, 0, -5), "h_head": (-20, 0, 0),
            "torso": (-8, 0, 0)}
    a.pose(0.4, pose)
    a.pose(1.0, pose)
    a.rest(1.4)

    a = m.anim("phase_change", 1.8, "once")
    a.rest(0)
    kneel = {**GM.KNEEL, "torso": (30, 0, 0), "h_head": (25, 0, 0), "right_arm": (-30, 0, 10), "left_arm": (-30, 0, -10)}
    a.pose(0.5, kneel)
    a.pose(0.8, kneel)
    roar = {"body": {"p": (0, 0, 0)}, "right_leg": (0, 0, 0), "right_lower_leg": (0, 0, 0), "left_leg": (0, 0, 0),
            "left_lower_leg": (0, 0, 0), "torso": (-18, 0, 0), "h_head": (-28, 0, 0), "right_arm": (-30, 0, 60),
            "left_arm": (-30, 0, -60), "sword": (40, 0, 0)}
    a.pose(1.2, roar, i="linear")
    a.pose(1.5, roar)
    a.rest(1.8)

    GM.human_hurt(m)
    GM.human_spawn(m, {"left_arm": (-170, 0, -10), "h_head": (-20, 0, 0)}, length=2.0)
    GM.human_death(m, 2.4)
    m.scale(1.45)
    return m


# ===========================================================================
# ESCUDERO CAIDO (ZOMBIE)
# ===========================================================================
def build_fallen_squire():
    m = _model("fallen_squire", 4041)

    def head(m, hd):
        AN.default_head(m, hd, face="zombie_face", mat="flesh")
        m.cube(hd, "hat_dome", (-3.6, 30.6, -3.6), (3.6, 32.8, 3.8), "iron", **P)
        m.cube(hd, "hat_brim", (-5.6, 30.0, -5.6), (5.6, 30.8, 5.8), "iron", rot=("x", 0), **P)
        m.cube(hd, "hat_top", (-1.6, 32.8, -1.6), (1.6, 33.4, 1.8), "iron_hi")
        m.cube(hd, "coif", (-3.7, 24.8, -1.0), (3.7, 30.2, 3.9), "chain", decor={"all": "chainmail"})

    H = AN.humanoid(m, k=0.95, mats={"skin": "flesh", "chest": "gambeson", "belly": "gambeson", "arm": "gambeson",
                                     "thigh": "leather", "shin": "leather", "foot": "leather"}, head=head)
    for c in m.CUBES:
        if c.mat == "gambeson":
            c.decor.setdefault("all", "quilt")
    torso, waist = H["torso"], H["waist"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    m.cube(torso, "tabard", (-3.4, 14.6, -3.4), (3.4, 23.4, -2.8), "red", decor={"all": "handsigil"})
    m.cube(m.BONES["skirt_front"], "tabard_low", (-3.0, 7.0, -3.2), (3.0, 13.4, -2.7), "red", decor={"all": "tatter"})
    m.cube(m.BONES["skirt_back"], "tabard_back", (-3.2, 7.4, 2.7), (3.2, 13.4, 3.2), "red", decor={"all": "tatter"})
    m.cube(waist, "belt", (-4.4, 13.2, -2.6), (4.4, 14.6, 2.6), "leather")
    sw = m.bone("sword", (6.5, 10.0, 0), AR[2])
    m.cube(sw, "grip", (6.1, 9.5, -2.6), (6.9, 10.5, 2.4), "leather")
    m.cube(sw, "guard", (4.8, 9.3, -3.2), (8.2, 10.7, -2.6), "rust")
    m.cube(sw, "blade", (6.25, 8.9, -17.0), (6.75, 11.1, -3.2), "iron_hi", decor={"all": "blade"})
    m.ZERO_BONES += ["sword"]
    GM.human_idle(m, arm_r=(-40, 0, 8), arm_l=(-60, 0, -6),
                  extra=lambda a, t, s: (a.rot("sword", t, 40, 0, 0), a.rot("torso", t, 10, 0, 0),
                                         a.rot("h_head", t, -6, 6 * s - 3, 6)))
    GM.human_walk(m, leg=18, arm=8, lean=12, length=1.3, arm_r=(-45, 0, 8), arm_l=(-65, 0, -6),
                  extra=lambda a, t, s: a.rot("sword", t, 40, 0, 0))
    a = m.anim("attack", 0.7, "once")
    a.rest(0)
    a.pose(0.15, {"right_arm": (-150, 0, 20), "torso": (-5, 15, 0), "sword": (40, 0, 0)})
    a.pose(0.3, {"right_arm": (-50, 0, -20), "torso": (15, -15, 0), "sword": (0, 0, 0)}, i="linear")
    a.rest(0.7)
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-60, 0, 10), "h_head": (-10, 0, 0)})
    GM.human_death(m)
    return m


# ===========================================================================
# CABALLERO CORRUPTO (WITHER_SKELETON)
# ===========================================================================
def build_corrupt_knight():
    m = _model("corrupt_knight", 4042)

    def head(m, hd):
        m.cube(hd, "skull", (-3.0, 25.4, -2.8), (3.0, 30.4, 3.0), "bone_black", decor={"north": "skull_face"})
        m.cube(hd, "bascinet", (-3.5, 27.0, -3.2), (3.5, 32.0, 3.6), "iron", **P)
        m.cube(hd, "bascinet_top", (-2.4, 32.0, -2.0), (2.4, 33.6, 2.6), "iron", rot=("x", 22.5), pivot=(0, 32, 0), **P)
        m.cube(hd, "snout", (-2.0, 25.4, -5.6), (2.0, 29.8, -3.0), "iron", rot=("x", -22.5), pivot=(0, 27.6, -3.2),
               decor={"north": "visor", "all": "plate"})
        m.cube(hd, "aventail", (-3.8, 23.4, -2.6), (3.8, 27.2, 3.8), "chain", decor={"all": "chainmail"})

    H = AN.humanoid(m, k=1.0, mats={"skin": "bone_black", "chest": "bone_black", "foot": "iron"}, head=head)
    torso, waist = H["torso"], H["waist"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    RL, LL = H["legs"]["right"], H["legs"]["left"]
    m.cube(torso, "cuirass", (-4.8, 16.6, -3.3), (4.8, 23.6, 3.1), "iron", decor={"all": "rusty"})
    m.cube(waist, "mail", (-4.4, 8.0, -2.8), (4.4, 15.0, 2.8), "chain", decor={"all": "chainmail"})
    m.cube_lr(AR[0], AL[0], "pauldron", (4.6, 22.0, -2.8), (9.0, 25.0, 2.8), "iron", rot=("z", 22.5),
              pivot=(5.0, 24, 0), decor={"all": "rusty"})
    m.cube_lr(RL[1], LL[1], "greave", (0.8, 1.4, -2.2), (4.2, 7.2, 2.0), "iron", decor={"all": "rusty"})
    sh = m.bone("shield", (-6.5, 14, -1), AL[1])
    m.cube(sh, "shield", (-9.4, 6.0, -5.0), (-8.6, 18.0, 4.0), "black", decor={"west": "handsigil", "all": "plate"})
    m.cube(sh, "shield_tip", (-9.4, 3.6, -3.0), (-8.6, 6.2, 2.0), "black", **P)
    m.cube(sh, "shield_rim", (-9.6, 17.4, -5.2), (-8.4, 18.4, 4.2), "brass")
    sw = m.bone("sword", (6.5, 10.0, 0), AR[2])
    m.cube(sw, "grip", (6.1, 9.5, -2.8), (6.9, 10.5, 2.8), "leather")
    m.cube(sw, "guard", (4.4, 9.3, -3.4), (8.6, 10.7, -2.8), "iron_hi")
    m.cube(sw, "blade", (6.25, 8.8, -21.0), (6.75, 11.2, -3.4), "iron_hi", decor={"all": "blade"})
    m.ZERO_BONES += ["sword", "shield"]
    GM.human_idle(m, arm_r=(-25, 0, 8), arm_l=(-30, 30, -6),
                  extra=lambda a, t, s: a.rot("sword", t, 30, 0, 0))
    GM.human_walk(m, leg=22, arm=10, arm_r=(-30, 0, 8), arm_l=(-35, 30, -6),
                  extra=lambda a, t, s: a.rot("sword", t, 30, 0, 0))
    a = m.anim("attack", 0.8, "once")          # golpe de escudo y estocada (0.35 s)
    a.rest(0)
    a.pose(0.15, {"left_arm": (-80, 10, -6), "right_arm": (10, 0, 20), "torso": (0, 20, 0), "sword": (20, 0, 0)})
    a.pose(0.35, {"left_arm": (-40, 30, -6), "right_arm": (-95, 0, 0), "torso": (10, -20, 0), "sword": (0, 0, 0)},
           i="linear")
    a.rest(0.8)
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-60, 0, 10), "left_arm": (-40, 30, -6)})
    GM.human_death(m)
    return m


# ===========================================================================
# ALMA CONDENADA (VEX)
# ===========================================================================
CS_BONES = ["body", "h_head", "right_arm", "left_arm", "tail0", "tail1", "tail2", "chains"]


def build_condemned_soul():
    m = _model("condemned_soul", 4043)
    m.SHINE |= {"ghost"}
    root = m.root
    hb = m.bone("hitbox", (0, 14, 0), root)
    m.cube(hb, "hitbox", (-4, 4, -4), (4, 26, 4), "hitbox")
    m.bone("tag_name", (0, 30, 0), root)
    body = m.bone("body", (0, 16, 0), root)
    m.cube(body, "robe", (-3.2, 14, -2.2), (3.2, 21, 2.4), "ghost_dark", decor={"all": "wisp"})
    m.cube_lr(body, body, "robe_flare", (2.6, 10.6, -2.2), (3.4, 15.2, 2.4), "ghost_dark", rot=("z", 22.5),
              pivot=(3.0, 15.2, 0), decor={"all": "wisp"})
    m.cube(body, "robe_low", (-2.8, 10.6, -2.0), (2.8, 14.2, 2.2), "ghost_dark", decor={"all": "wisp"})
    m.cube(body, "ribs", (-2.4, 15, -2.6), (2.4, 20, -2.3), "ghost", decor={"all": "ribs"} if "ribs" in m.DECOR else None)
    hd = m.bone("h_head", (0, 21, 0), body)
    m.cube(hd, "skull", (-2.6, 21.2, -2.6), (2.6, 26.0, 2.4), "ghost", decor={"north": "skull_face"})
    m.cube(hd, "hood", (-3.4, 21.0, -2.0), (3.4, 27.4, 3.4), "ghost_dark", decor={"all": "wisp"})
    m.cube(hd, "hood_tip", (-1.6, 26.6, 1.0), (1.6, 28.4, 4.4), "ghost_dark", rot=("x", 22.5), pivot=(0, 27, 2))
    for side, sx in (("right", 1), ("left", -1)):
        arm = m.bone(f"{side}_arm", (3.8 * sx, 20, 0), body)
        m.cube(arm, f"{side}_sleeve", (3.0 * sx - 1.2, 15.0, -1.4), (3.0 * sx + 1.2, 20.4, 1.4), "ghost_dark",
               decor={"all": "wisp"})
        m.cube(arm, f"{side}_hand", (3.0 * sx - 0.8, 12.4, -1.0), (3.0 * sx + 0.8, 15.2, 0.8), "ghost")
        for k in range(3):
            m.cube(arm, f"{side}_finger{k}", (3.0 * sx - 0.7 + k * 0.6, 10.6, -0.9), (3.0 * sx - 0.3 + k * 0.6, 12.6, -0.5),
                   "ghost")
    prev = body
    for k in range(3):
        y = 12 - k * 3.6
        t = m.bone(f"tail{k}", (0, y, 0.4 * k), prev, rotation=(-22.5 if k else -10, 0, 0))
        w = 2.8 - k * 0.9
        m.cube(t, f"tail{k}", (-w, y - 4.0, -w * 0.7 + 0.4 * k), (w, y + 0.2, w * 0.7 + 0.4 * k), "ghost_dark",
               decor={"all": "wisp"})
        prev = t
    ch = m.bone("chains", (0, 13, 0), body)
    for i, (x, z) in enumerate(((-2.8, -1.0), (2.6, 0.8))):
        for j in range(4):
            m.cube(ch, f"chain{i}_{j}", (x - 0.4, 11.0 - j * 1.8, z - 0.25 + (j % 2) * 0.1),
                   (x + 0.4, 12.4 - j * 1.8, z + 0.25), "chain")
    m.ZERO_BONES = list(CS_BONES)

    def wave(a, t, s, amp=10):
        a.rot("tail0", t, amp * s, 0, 0)
        a.rot("tail1", t, -amp * 1.2 * s, 0, 0)
        a.rot("tail2", t, amp * 1.4 * s, 0, 0)
        a.rot("chains", t, 0, 0, 6 * s)

    a = m.anim("idle", 2.0, "loop")
    for t, s in ((0, 0), (0.5, 1), (1.0, 0), (1.5, -1), (2.0, 0)):
        a.pos("body", t, 0, 0.8 * s, 0)
        a.rot("right_arm", t, -30 + 6 * s, 0, 10)
        a.rot("left_arm", t, -30 - 6 * s, 0, -10)
        a.rot("h_head", t, 4 * s, 6 * s, 0)
        wave(a, t, s)
    a = m.anim("walk", 1.0, "loop")
    for t, s in ((0, 0), (0.25, 1), (0.5, 0), (0.75, -1), (1.0, 0)):
        a.rot("body", t, 20, 0, 4 * s)
        a.pos("body", t, 0, 0.6 * s, 0)
        a.rot("right_arm", t, -70, 0, 10)
        a.rot("left_arm", t, -70, 0, -10)
        wave(a, t, s, 16)
    a = m.anim("attack", 0.7, "once")          # se abalanza con las manos (0.3 s)
    a.rest(0)
    a.pose(0.15, {"right_arm": (-150, 0, 30), "left_arm": (-150, 0, -30), "h_head": (-20, 0, 0)})
    a.pose(0.3, {"right_arm": (-80, 0, 0), "left_arm": (-80, 0, 0), "h_head": (10, 0, 0), "body": (20, 0, 0)},
           i="linear")
    a.rest(0.7)
    a = m.anim("hurt", 0.35, "once")
    a.rest(0, ["h_head", "body"])
    a.pose(0.08, {"h_head": (-20, 0, 10), "body": (-10, 0, 0)})
    a.rest(0.35, ["h_head", "body"])
    a = m.anim("spawn", 1.2, "once")
    a.pos("body", 0, 0, -12, 0)
    a.scl("body", 0, 0.2)
    a.pos("body", 0.8, 0, 0, 0)
    a.scl("body", 0.8, 1)
    a.rest(1.2)
    a = m.anim("death", 1.2, "hold")
    a.rest(0)
    a.pose(0.3, {"h_head": (-30, 0, 0), "right_arm": (-160, 0, 40), "left_arm": (-160, 0, -40)})
    a.scl("body", 0.3, 1)
    a.scl("body", 1.2, 0.05, 1.6, 0.05)
    a.pos("body", 1.2, 0, 6, 0)
    return m


# ===========================================================================
# CHARCO DE SANGRE (RH_BloodPool)
# ===========================================================================
def build_blood_pool():
    m = _model("rh_blood_pool", 4044)
    root = m.root
    pool = m.bone("pool", (0, 0, 0), root)
    rng = random.Random(7)
    for k, (x, z, r) in enumerate(((0, 0, 30), (18, 10, 18), (-20, 8, 16), (8, -22, 16), (-12, -18, 14), (24, -10, 12))):
        m.cube(pool, f"blob{k}", (x - r, 0.05 + k * 0.02, z - r * 0.8), (x + r, 0.35 + k * 0.02, z + r * 0.8),
               "blood" if k % 2 == 0 else "crimson")
    m.cube(pool, "glow_core", (-10, 0.4, -8), (10, 0.5, 8), "glow")
    a = m.anim("idle", 2.0, "loop")
    for k in range(6):
        b = m.bone(f"bubble{k}", (0, 0, 0), root)
        x, z = rng.uniform(-22, 22), rng.uniform(-18, 18)
        m.cube(b, f"bubble{k}", (x - 1.4, 0.2, z - 1.4), (x + 1.4, 2.6, z + 1.4), "blood")
        off = k / 6 * 2.0
        for t in (0, 0.5, 1.0, 1.5, 2.0):
            ph = ((t + off) % 2.0) / 2.0
            a.scl(f"bubble{k}", t, 0.3 + 0.9 * ph if ph < 0.85 else 0.05, i="linear")
            a.pos(f"bubble{k}", t, 0, ph * 2, 0, i="linear")
    for t, s in ((0, 1), (1.0, 1.04), (2.0, 1)):
        a.scl("pool", t, s, 1, s)
    a = m.anim("spawn", 0.6, "once")
    a.scl("pool", 0, 0.1, 1, 0.1)
    a.scl("pool", 0.4, 1.08, 1, 1.08)
    a.scl("pool", 0.6, 1, 1, 1)
    return m


BUILDERS = {"red_hand": build_red_hand, "fallen_squire": build_fallen_squire, "corrupt_knight": build_corrupt_knight,
            "condemned_soul": build_condemned_soul, "rh_blood_pool": build_blood_pool}
SHOTS = {
    "red_hand": [("rest", 0, -30), ("rest", 0, 150), ("crush", 0.25, -50), ("execution", 0.6, -30)],
    "fallen_squire": [("idle", 0.5, -30), ("rest", 0, 150), ("attack", 0.15, -60), ("attack", 0.3, -60)],
    "corrupt_knight": [("rest", 0, -30), ("rest", 0, 150), ("attack", 0.15, -60), ("attack", 0.35, -60)],
    "condemned_soul": [("idle", 0.5, -30), ("idle", 0.5, -100), ("rest", 0, 150), ("attack", 0.3, -50)],
    "rh_blood_pool": [("idle", 0.2, -30), ("idle", 0.9, -30), ("spawn", 0.2, -30), ("idle", 1.6, -30)],
}
VIEW = {"red_hand": (30, 6.2), "condemned_soul": (16, 9.0), "rh_blood_pool": (0, 3.5)}


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
