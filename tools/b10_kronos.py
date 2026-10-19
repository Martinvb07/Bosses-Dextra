#!/usr/bin/env python3
"""
Boss 10 - KRONOS y sus subditos (modelos de ModelEngine).

  kronos            titan del tiempo: barba larga, corona de agujas de reloj, aureola de reloj con
                    manecillas que giran, peto de oro con esfera, hombreras inclinadas, tunica en capas,
                    engranajes en la espalda, reloj de arena en la cadera y guadana
  kr_sentinel       centinela de cuerda: armadura de bronce, casco-esfera, llave de cuerda en la
                    espalda, espada y reloj de bolsillo (ZOMBIE)
  kr_guardian       guardian de las eras: armadura pesada de hierro y oro, escudo-engranaje y hacha (ZOMBIE)
  kr_archer         saetero del ocaso: capucha, capa de atardecer, arco y carcaj (SKELETON)
  kr_devourer       devorador de eras: bestia enorme a cuatro patas con mandibula, cuernos y un
                    engranaje incrustado en el lomo (RAVAGER)

Uso: python3 tools/b10_kronos.py [modelo ...] [--no-preview]
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

ROOT = Path(__file__).resolve().parent.parent / "Modelos/10_Kronos"
BLUEPRINTS = ROOT / "ModelEngine/blueprints"
PREVIEW = ROOT / "preview"

GLOW = (214, 140, 255)
MATS = {
    "robe": ((78, 34, 120), 7), "robe_dark": ((44, 20, 70), 6), "gold": ((214, 170, 64), 7), "gold_dark": ((150, 110, 40), 6),
    "skin": ((176, 160, 176), 6), "beard": ((222, 222, 232), 7), "glow": (GLOW, 3), "sand": ((236, 200, 120), 6),
    "glass": ((200, 226, 255), 3), "dial": ((240, 230, 200), 3), "iron": ((70, 70, 88), 6), "iron_hi": ((130, 130, 150), 6),
    "bronze": ((190, 130, 60), 7), "bronze_dark": ((120, 80, 40), 6), "black": ((22, 16, 30), 3), "leather": ((92, 60, 36), 7),
    "wood": ((100, 70, 44), 8), "dusk": ((200, 90, 50), 7), "dusk_dark": ((120, 50, 40), 6), "bone": ((220, 212, 190), 6),
    "hide": ((70, 56, 84), 9), "hide_dark": ((44, 34, 56), 8), "horn": ((210, 200, 180), 6), "fang": ((245, 240, 230), 3),
    "mouth": ((60, 20, 40), 3), "ice": ((196, 140, 245), 5), "ice_dark": ((112, 60, 176), 6),
    "hitbox": ((255, 255, 255), 0),
}


def time_decor(m):
    D = m.decor

    @D
    def d_clock(f):
        """Esfera de reloj: marcas de las horas y dos manecillas."""
        if f.name != "north":
            return
        w, h = f.w, f.h
        cx, cy = w // 2, h // 2
        r = min(w, h) / 2 - 1
        for k in range(12):
            a = 2 * math.pi * k / 12
            f.put(round(cx + r * math.sin(a)) - (1 if k > 6 else 0), round(cy - r * math.cos(a)), (60, 30, 90))
        for i in range(int(r * 0.8)):
            f.put(cx, cy - i, (30, 20, 40))
        for i in range(int(r * 0.55)):
            f.put(cx + i, cy, (30, 20, 40))
        f.put(cx, cy, (200, 60, 60))

    @D
    def d_kronos_face(f):
        if f.name != "north":
            return
        w = f.w
        f.rect(1, 4, w - 1, 6, (110, 96, 112))              # cejas pesadas
        for ex in (2, w - 6):
            f.rect(ex, 6, ex + 4, 8, (30, 10, 40))
            f.rect(ex + 1, 6, ex + 3, 7, GLOW)
        f.rect(w // 2 - 1, 7, w // 2 + 1, 11, (150, 134, 150))
        for y in range(1, 4):                                # arrugas
            f.put(4 + y, y, (140, 126, 142))
            f.put(w - 5 - y, y, (140, 126, 142))

    @D
    def d_beard(f):
        for y in range(f.h):
            for x in range(f.w):
                if (x * 2 + y) % 4 == 0:
                    f.shade(x, y, 0.84)

    @D
    def d_robe(f):
        """Tunica: ribete de oro abajo y bordado de arena."""
        if f.name in ("up", "down"):
            return
        for x in range(f.w):
            f.put(x, f.h - 1, (214, 170, 64))
            if f.h > 4:
                f.put(x, f.h - 2, (150, 110, 40))
        for x in range(2, f.w, 5):
            for y in range(f.h - 2):
                f.shade(x, y, 0.8)
                f.shade(x + 1, y, 1.12)

    @D
    def d_engraved(f):
        """Oro grabado: bandas y remaches."""
        if f.name in ("up", "down"):
            return
        for x in range(f.w):
            f.put(x, 1, (250, 220, 130))
            f.put(x, f.h - 2, (120, 84, 30))
        for x in range(2, f.w - 1, 4):
            f.put(x, f.h // 2, (250, 230, 160))

    @D
    def d_gear(f):
        if f.name not in ("north", "south"):
            return
        w, h = f.w, f.h
        f.rect(w // 2 - 1, h // 2 - 1, w // 2 + 1, h // 2 + 1, (60, 40, 20))
        for x in range(w):
            f.put(x, 0, (250, 220, 130))

    @D
    def d_crystal(f):
        for y in range(f.h):
            f.put(0, y, (250, 240, 255))

    @D
    def d_clock_helm(f):
        if f.name != "north":
            return
        w, h = f.w, f.h
        cx, cy = w // 2, h // 2 + 1
        r = min(w, h) / 2 - 2
        for k in range(12):
            a = 2 * math.pi * k / 12
            f.put(round(cx + r * math.sin(a)), round(cy - r * math.cos(a)), (60, 40, 20))
        f.rect(cx - 4, cy - 1, cx - 1, cy + 1, (255, 200, 90))
        f.rect(cx + 1, cy - 1, cx + 4, cy + 1, (255, 200, 90))
        for i in range(int(r * 0.7)):
            f.put(cx, cy - 1 - i, (40, 30, 20))

    @D
    def d_slit(f):
        if f.name != "north":
            return
        w = f.w
        f.rect(1, 6, w - 1, 8, (12, 8, 16))
        f.rect(w // 2 - 1, 8, w // 2 + 1, 13, (12, 8, 16))
        f.rect(3, 6, 5, 7, GLOW)
        f.rect(w - 5, 6, w - 3, 7, GLOW)

    @D
    def d_hood_face(f):
        if f.name != "north":
            return
        w, h = f.w, f.h
        f.rect(1, 2, w - 1, h - 1, (16, 10, 20))
        for ex in (3, w - 6):
            f.rect(ex, h // 2 - 1, ex + 3, h // 2 + 1, (255, 160, 80))

    @D
    def d_beast_eyes(f):
        if f.name != "north":
            return
        w = f.w
        for ex in (2, w - 6):
            f.rect(ex, 3, ex + 4, 6, (20, 10, 30))
            f.rect(ex + 1, 4, ex + 3, 5, GLOW)

    @D
    def d_hide(f):
        for y in range(f.h):
            for x in range(f.w):
                if (x + 3 * y) % 7 == 0:
                    f.shade(x, y, 0.82)
                elif (2 * x + y) % 11 == 0:
                    f.shade(x, y, 1.15)


def _model(name, seed, atlas=256):
    m = Model(name, MATS, seed=seed, atlas_w=atlas)
    m.SHINE |= {"gold", "gold_dark", "iron_hi", "bronze", "glow", "glass", "ice"}
    m.WOOD |= {"wood"}
    GM.add_common_decor(m)
    RG.norse_decor(m)
    time_decor(m)
    return m


EN = {"decor": {"all": "engraved"}}
RB = {"decor": {"all": "robe"}}


def gear(m, bone, name, cx, cy, z0, z1, r, mat="gold", teeth=8):
    """Engranaje en el plano XY: disco octogonal + dientes."""
    m.cube(bone, name, (cx - r * 0.72, cy - r * 0.72, z0), (cx + r * 0.72, cy + r * 0.72, z1), mat, decor={"all": "gear"})
    m.cube(bone, name + "45", (cx - r * 0.72, cy - r * 0.72, z0 + 0.05), (cx + r * 0.72, cy + r * 0.72, z1 - 0.05), mat,
           rot=("z", 45), pivot=(cx, cy, (z0 + z1) / 2))
    for k in range(teeth):
        a = 2 * math.pi * k / teeth
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        rot = ("z", 45) if k % 2 else None
        m.cube(bone, f"{name}t{k}", (x - 0.5, y - 0.5, z0 + 0.1), (x + 0.5, y + 0.5, z1 - 0.1), mat, rot=rot, pivot=(x, y, z0))


def ring(m, bone, name, cx, cy, z0, z1, R, mat, n=16, t=0.7):
    """Aro en el plano XY hecho de n tramos tangentes (giros de 22.5 grados)."""
    L = 2 * math.pi * R / n * 0.56
    for k in range(n):
        a = 360 * k / n
        x, y = cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))
        th = (a + 90) % 180
        th = th - 180 if th >= 90 else th
        if abs(th) <= 45:
            frm, to = (x - L, y - t / 2, z0), (x + L, y + t / 2, z1)
        else:
            th = th - 90 if th > 0 else th + 90
            frm, to = (x - t / 2, y - L, z0), (x + t / 2, y + L, z1)
        m.cube(bone, f"{name}{k}", frm, to, mat, rot=("z", th) if th else None, pivot=(x, y, (z0 + z1) / 2))


def hourglass(m, bone, name, x, y, z, s=1.0):
    """Reloj de arena: tapas de oro, dos ampollas de cristal en rombo y arena."""
    m.cube(bone, name + "_top", (x - 1.5 * s, y + 4.2 * s, z - 1.5 * s), (x + 1.5 * s, y + 4.8 * s, z + 1.5 * s), "gold")
    m.cube(bone, name + "_bot", (x - 1.5 * s, y, z - 1.5 * s), (x + 1.5 * s, y + 0.6 * s, z + 1.5 * s), "gold")
    for k, (y0, y1) in enumerate(((0.6, 2.4), (2.4, 4.2))):
        m.cube(bone, f"{name}_g{k}", (x - 0.9 * s, y + y0 * s, z - 0.9 * s), (x + 0.9 * s, y + y1 * s, z + 0.9 * s), "glass",
               rot=("y", 45), pivot=(x, y, z))
    m.cube(bone, name + "_sand", (x - 0.6 * s, y + 0.6 * s, z - 0.6 * s), (x + 0.6 * s, y + 1.6 * s, z + 0.6 * s), "sand")
    for sx in (1, -1):
        m.cube(bone, f"{name}_post{sx}", (x + 1.2 * s * sx - 0.25 * s, y + 0.6 * s, z - 0.25 * s),
               (x + 1.2 * s * sx + 0.25 * s, y + 4.2 * s, z + 0.25 * s), "gold_dark")


# ===========================================================================
# KRONOS
# ===========================================================================
def kronos_head(m, hd):
    m.cube(hd, "skull", (-3.4, 25.0, -3.4), (3.4, 31.6, 3.4), "skin", decor={"north": "kronos_face"})
    m.cube(hd, "brow", (-3.6, 29.6, -4.2), (3.6, 30.8, -3.0), "skin", rot=("x", 22.5), pivot=(0, 30.2, -3.4))
    m.cube(hd, "nose", (-0.7, 26.8, -4.2), (0.7, 29.2, -3.3), "skin")
    m.cube(hd, "hair_back", (-3.8, 23.0, 1.0), (3.8, 31.0, 4.0), "beard", decor={"all": "beard"})
    m.cube_lr(hd, hd, "hair_side", (3.2, 24.0, -2.0), (4.2, 30.4, 3.0), "beard", decor={"all": "beard"})
    # barba larga que se afina en capas
    m.cube(hd, "moustache", (-2.6, 25.6, -4.4), (2.6, 26.8, -3.2), "beard", decor={"all": "beard"})
    m.cube(hd, "beard0", (-3.4, 21.6, -4.6), (3.4, 26.0, -2.6), "beard", decor={"all": "beard"})
    m.cube(hd, "beard1", (-2.6, 17.8, -5.0), (2.6, 22.0, -3.6), "beard", rot=("x", -22.5), pivot=(0, 22, -4.2),
           decor={"all": "beard"})
    m.cube(hd, "beard2", (-1.6, 14.6, -5.4), (1.6, 18.4, -4.2), "beard", rot=("x", -22.5), pivot=(0, 22, -4.2),
           decor={"all": "beard"})
    m.cube_lr(hd, hd, "beard_side", (2.2, 21.4, -4.4), (3.6, 26.0, -1.6), "beard", rot=("z", 22.5), pivot=(3.4, 26, -3),
              decor={"all": "beard"})
    # corona de agujas de reloj
    m.cube(hd, "crown", (-3.8, 30.4, -3.8), (3.8, 31.8, 3.8), "gold", **EN)
    for i, (x, h, ang) in enumerate(((-3.0, 3.0, 22.5), (-1.5, 4.2, 0), (0.0, 6.0, 0), (1.5, 4.2, 0), (3.0, 3.0, -22.5))):
        m.cube(hd, f"crown_hand{i}", (x - 0.45, 31.6, -3.9), (x + 0.45, 31.6 + h, -3.1), "gold", rot=("z", ang) if ang else None,
               pivot=(x, 31.6, -3.5))
    m.cube(hd, "crown_gem", (-0.7, 32.2, -4.2), (0.7, 33.6, -3.6), "glow", rot=("z", 45), pivot=(0, 32.9, -3.9))
    for sx in (1, -1):
        m.cube(hd, f"crown_back{sx}", (2.2 * sx - 0.4, 31.6, 2.6), (2.2 * sx + 0.4, 34.4, 3.4), "gold",
               rot=("z", -22.5 * sx), pivot=(2.2 * sx, 31.6, 3))


def build_kronos():
    m = _model("kronos", 1010)
    H = AN.humanoid(m, k=1.3, mats={"chest": "gold", "belly": "robe", "arm": "robe", "hand": "skin", "thigh": "robe",
                                     "shin": "robe_dark", "foot": "gold", "pelvis": "robe", "neck": "skin"},
                    head=kronos_head)
    for c in m.CUBES:
        if c.mat == "gold":
            c.decor.setdefault("all", "engraved")
    torso, waist, body = H["torso"], H["waist"], H["body"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    RL, LL = H["legs"]["right"], H["legs"]["left"]

    # peto con esfera de reloj
    m.cube(torso, "dial_frame", (-2.9, 18.2, -4.7), (2.9, 24.0, -4.1), "gold", rot=("z", 45), pivot=(0, 21.1, -4.4), **EN)
    m.cube(torso, "dial", (-2.6, 18.5, -4.9), (2.6, 23.7, -4.3), "dial", decor={"all": "clock"})
    m.cube(torso, "sash", (-5.6, 15.4, -4.3), (5.6, 16.8, 4.0), "robe_dark", rot=("z", 22.5), pivot=(0, 16, 0))
    # hombreras inclinadas en dos capas con puas
    m.cube_lr(AR[0], AL[0], "pauldron", (4.2, 22.4, -3.6), (10.2, 25.4, 3.6), "gold", rot=("z", -22.5), pivot=(7.2, 24, 0), **EN)
    m.cube_lr(AR[0], AL[0], "pauldron2", (5.6, 20.2, -3.2), (10.4, 22.6, 3.2), "gold_dark", rot=("z", -22.5),
              pivot=(8.0, 21.4, 0), **EN)
    m.cube_lr(AR[0], AL[0], "pauldron_spike", (7.4, 25.0, -0.5), (8.4, 28.6, 0.5), "gold", rot=("z", -22.5),
              pivot=(7.9, 25, 0))
    m.cube_lr(AR[0], AL[0], "sleeve", (4.0, 15.6, -2.8), (9.0, 21.0, 2.8), "robe", **RB)
    m.cube_lr(AR[1], AL[1], "bracer", (4.6, 11.8, -2.3), (8.4, 15.8, 2.3), "gold", **EN)
    m.cube_lr(AR[1], AL[1], "bracer_gem", (6.0, 13.2, -2.6), (7.0, 14.4, -2.2), "glow")
    # tunica en capas
    m.cube(waist, "belt", (-6.0, 13.4, -4.0), (6.0, 15.2, 4.0), "gold", **EN)
    hourglass(m, waist, "buckle", 0, 13.0, -4.4, 0.55)
    m.cube(waist, "robe_hip", (-6.2, 6.0, -4.2), (6.2, 13.6, 4.2), "robe", **RB)
    m.cube_lr(waist, waist, "robe_flare", (5.6, 0.6, -4.0), (6.6, 9.6, 4.0), "robe", rot=("z", 22.5), pivot=(6.1, 9.6, 0), **RB)
    m.cube(m.BONES["skirt_front"], "tabard", (-3.0, 0.4, -4.9), (3.0, 13.0, -4.3), "robe_dark", **RB)
    m.cube(m.BONES["skirt_front"], "tabard_trim", (-0.7, 0.6, -5.1), (0.7, 12.4, -4.8), "gold")
    m.cube(m.BONES["skirt_back"], "robe_back", (-5.6, 0.4, 4.0), (5.6, 13.0, 4.8), "robe", rot=("x", 22.5),
           pivot=(0, 13, 4.4), **RB)
    m.cube_lr(RL[1], LL[1], "greave", (0.6, 1.0, -2.4), (4.4, 6.0, 2.0), "gold", **EN)
    # reloj de arena colgando de la cadera izquierda
    hg = m.bone("hourglass", (-6.6, 13.0, 0), waist)
    m.cube(hg, "hg_chain", (-6.9, 11.0, -0.3), (-6.3, 13.4, 0.3), "gold_dark")
    hourglass(m, hg, "hg", -6.6, 5.8, 0, 1.25)
    # capa, engranajes en la espalda y aureola de reloj
    cape = m.bone("cape", (0, 24, 3.8), torso, rotation=(6, 0, 0))
    m.cube(cape, "cape", (-5.4, 3.0, 3.8), (5.4, 24.0, 4.5), "robe_dark", **RB)
    m.cube_lr(cape, cape, "cape_edge", (5.0, 4.0, 3.6), (5.8, 23.6, 4.6), "gold")
    for n, (x, y, r, z) in (("gear_a", (-2.6, 19.0, 3.4, 4.6)), ("gear_b", (3.0, 14.2, 2.4, 4.7)), ("gear_c", (2.4, 22.4, 1.6, 4.8))):
        g = m.bone(n, (x, y, z), torso)
        gear(m, g, n, x, y, z, z + 0.9, r, mat="gold" if n != "gear_b" else "bronze")
    halo = m.bone("halo", (0, 30, 6.0), torso)
    ring(m, halo, "halo_ring", 0, 30, 5.7, 6.3, 8.0, "gold", n=16)
    for k in range(12):
        a = 2 * math.pi * k / 12
        x, y = 8.0 * math.cos(a), 30 + 8.0 * math.sin(a)
        s = 1.0 if k % 3 == 0 else 0.6
        m.cube(halo, f"halo{k}", (x - s, y - s, 5.5), (x + s, y + s, 6.5), "glow" if k % 3 == 0 else "gold_dark",
               rot=("z", 45), pivot=(x, y, 6))
    hl = m.bone("hand_long", (0, 30, 6.0), halo)
    m.cube(hl, "hand_long", (-0.35, 30, 5.4), (0.35, 37.0, 6.6), "gold")
    m.cube(hl, "hand_long_tip", (-0.8, 36.0, 5.5), (0.8, 37.6, 6.5), "gold", rot=("z", 45), pivot=(0, 36.8, 6))
    hs = m.bone("hand_short", (0, 30, 6.0), halo)
    m.cube(hs, "hand_short", (0, 29.65, 5.5), (5.0, 30.35, 6.5), "gold_dark")
    m.cube(halo, "halo_hub", (-0.9, 29.1, 5.3), (0.9, 30.9, 6.7), "glow")
    # guadana
    sc = m.bone("scythe", (6.5, 10.0, 0), AR[2])
    m.cube(sc, "shaft", (6.05, 9.55, -28.0), (6.95, 10.45, 7.0), "black")
    for i, z in enumerate((-20.0, -8.0, 4.0)):
        m.cube(sc, f"shaft_ring{i}", (5.8, 9.3, z - 0.5), (7.2, 10.7, z + 0.5), "gold")
    gear(m, sc, "scythe_gear", 6.5, 10.0, -28.6, -27.6, 1.8, teeth=6)
    blade = [((3.6, 10.6), -27.6, None), ((-0.6, 4.2), -27.2, ("x", -22.5)), ((-4.4, 0.0), -26.0, ("x", -45))]
    for i, ((y0, y1), z, rot) in enumerate(blade):
        w = 1.4 - i * 0.3
        m.cube(sc, f"blade{i}", (6.2, y0, z - w), (6.8, y1, z + w), "iron_hi", rot=rot, pivot=(6.5, y1, z))
        m.cube(sc, f"edge{i}", (6.25, y0, z - w - 0.6), (6.75, y1, z - w), "glow", rot=rot, pivot=(6.5, y1, z))
    m.ZERO_BONES += ["scythe", "hourglass", "cape", "halo", "hand_long", "hand_short", "gear_a", "gear_b", "gear_c"]

    def ticking(a, length, speed=1.0):
        FX.spin(a, "hand_long", length, -1 * speed, "z")
        FX.spin(a, "hand_short", length, -speed / 12, "z")
        FX.spin(a, "gear_a", length, 0.5 * speed, "z")
        FX.spin(a, "gear_b", length, -0.7 * speed, "z")
        FX.spin(a, "gear_c", length, -1.0 * speed, "z")

    a = GM.human_idle(m, arm_r=(-20, 0, 10), arm_l=(-8, 0, -10),
                      extra=lambda a, t, s: (a.rot("scythe", t, -80, 0, 0), a.rot("hourglass", t, 0, 0, 4 * s - 2),
                                             a.rot("cape", t, 3 * s, 0, 0), a.pos("halo", t, 0, 0.5 * s, 0)))
    ticking(a, 2.4)
    a = GM.human_walk(m, leg=20, arm=10, lean=6, length=1.4, arm_r=(-25, 0, 10),
                      extra=lambda a, t, s: (a.rot("scythe", t, -80, 0, 0), a.rot("cape", t, 10 + 3 * s, 0, 0),
                                             a.rot("hourglass", t, 0, 0, 8 * s)))
    ticking(a, 1.4)

    def anim(name, length, keys, speed=None):
        a = m.anim(name, length, "once")
        a.rest(0)
        for t, pose, lin in keys:
            a.pose(t, pose, i="linear" if lin else "catmullrom")
        a.rest(length)
        if speed:
            ticking(a, length, speed)
        return a

    anim("attack", 0.7, [(0.15, {"right_arm": (-165, 0, 15), "scythe": (-100, 0, 0), "torso": (-6, 15, 0)}, False),
                         (0.3, {"right_arm": (-55, 0, -10), "scythe": (-20, 0, 0), "torso": (18, -15, 0)}, True)])
    up = {"right_arm": (-175, 0, -5), "left_arm": (-175, 0, 20), "scythe": (-90, 0, 0), "torso": (-12, 0, 0),
          "h_head": (-15, 0, 0)}
    anim("slam", 0.9, [(0.12, up, False), (0.25, {"right_arm": (-45, 0, -10), "left_arm": (-50, 0, 20), "scythe": (10, 0, 0),
                                                   "torso": (35, 0, 0), "h_head": (-10, 0, 0)}, True),
                       (0.55, {"right_arm": (-45, 0, -10), "left_arm": (-50, 0, 20), "scythe": (10, 0, 0),
                               "torso": (35, 0, 0)}, False)])
    plant = {**GM.KNEEL, "right_arm": (-70, 0, -5), "left_arm": (-60, 0, 25), "scythe": (150, 0, 0), "torso": (25, 0, 0),
             "h_head": (-15, 0, 0)}
    anim("quake", 1.3, [(0.15, {**up, "body": {"p": (0, 4, 0)}}, False), (0.3, plant, True), (0.9, plant, False)], speed=2)
    spread = {"right_arm": (-50, 0, 70), "left_arm": (-50, 0, -70), "torso": (-15, 0, 0), "h_head": (-25, 0, 0),
              "scythe": (-80, 0, 0)}
    anim("roar", 1.6, [(0.3, {"torso": (20, 0, 0), "h_head": (15, 0, 0)}, False), (0.5, spread, True), (1.2, spread, False)],
         speed=-3)
    crouch = {"right_arm": (-60, 70, 0), "scythe": (-60, 0, 0), "torso": (25, 30, 0), "right_leg": (-30, 0, 0),
              "right_lower_leg": (40, 0, 0), "body": {"p": (0, -2, 0)}}
    anim("charge", 1.0, [(0.25, crouch, False),
                         (0.5, {"right_arm": (-90, -80, 0), "scythe": (-60, 0, 0), "torso": (15, -40, 0)}, True),
                         (0.7, {"right_arm": (-90, -80, 0), "scythe": (-60, 0, 0), "torso": (15, -40, 0)}, False)])
    anim("antirun", 1.0, [(0.2, {"left_arm": (-95, 0, 0), "h_head": (-5, 0, 0)}, False),
                          (0.45, {"left_arm": (-55, 0, -25), "torso": (-10, 15, 0), "h_head": (-10, 0, 0)}, True),
                          (0.7, {"left_arm": (-55, 0, -25), "torso": (-10, 15, 0)}, False)], speed=-2)
    raise_ = {"right_arm": (-178, 0, 5), "scythe": (-90, 0, 0), "left_arm": (-60, 0, -60), "h_head": (-25, 0, 0)}
    anim("summon", 1.4, [(0.35, raise_, False), (1.0, raise_, False)], speed=3)
    anim("phase_change", 1.8, [(0.5, {**GM.KNEEL, "torso": (40, 0, 0), "h_head": (25, 0, 0), "scythe": (150, 0, 0),
                                      "right_arm": (-60, 0, 0)}, False),
                               (0.8, {**GM.KNEEL, "torso": (40, 0, 0), "h_head": (25, 0, 0), "scythe": (150, 0, 0),
                                      "right_arm": (-60, 0, 0)}, False),
                               (1.2, spread, True), (1.5, spread, False)], speed=4)
    anim("last_breath", 2.0, [(0.4, {**GM.KNEEL, "torso": (35, 0, 0), "h_head": (35, 0, 0), "scythe": (150, 0, 0),
                                     "right_arm": (-60, 0, 0), "left_arm": (-20, 0, -10)}, False),
                              (1.2, {**GM.KNEEL, "torso": (30, 0, 0), "h_head": (30, 0, 0), "scythe": (150, 0, 0),
                                     "right_arm": (-60, 0, 0)}, False),
                              (1.5, raise_, True)], speed=-6)
    GM.human_hurt(m)
    a = GM.human_spawn(m, raise_, length=2.0)
    ticking(a, 2.0, 3)
    a = GM.human_death(m, 2.4)
    a.pos("halo", 0, 0, 0, 0)
    a.pos("halo", 1.0, 0, -6, 2)
    a.scl("halo", 0, 1)
    a.scl("halo", 1.6, 0.05)
    m.scale(1.5)
    return m


# ===========================================================================
# CENTINELA DEL RELOJ (ZOMBIE)
# ===========================================================================
def build_sentinel():
    m = _model("kr_sentinel", 1011)

    def head(m, hd):
        m.cube(hd, "helm", (-3.4, 24.8, -3.4), (3.4, 31.4, 3.6), "bronze", **EN)
        m.cube(hd, "helm45", (-2.7, 25.0, -2.6), (2.7, 31.8, 2.8), "bronze_dark", rot=("y", 45), pivot=(0, 28, 0.1))
        m.cube(hd, "helm_dome", (-2.8, 31.0, -2.8), (2.8, 32.4, 3.0), "bronze", rot=("x", 22.5), pivot=(0, 31.5, 0))
        m.cube(hd, "visor", (-2.6, 25.4, -4.0), (2.6, 30.6, -3.4), "dial", decor={"north": "clock_helm"})
        m.cube(hd, "helm_rim", (-3.8, 24.6, -3.8), (3.8, 25.6, 4.0), "bronze_dark")
        gear(m, hd, "crest", 0, 33.2, -0.5, 0.5, 1.8, mat="gold", teeth=6)
        m.cube_lr(hd, hd, "cheek", (2.8, 24.2, -3.8), (3.8, 28.0, -1.0), "bronze", rot=("y", 22.5), pivot=(3.3, 26, -2.4))

    H = AN.humanoid(m, k=1.0, mats={"skin": "bronze_dark", "chest": "bronze", "belly": "iron", "arm": "bronze",
                                     "hand": "iron", "thigh": "iron", "shin": "bronze", "foot": "iron", "pelvis": "iron"},
                    head=head)
    torso, waist = H["torso"], H["waist"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    m.cube(torso, "plate", (-4.0, 18.6, -3.2), (4.0, 23.4, -2.6), "bronze", **EN)
    gear(m, torso, "chest_gear", 0, 21.0, -3.6, -3.0, 1.6, mat="gold", teeth=6)
    m.cube_lr(AR[0], AL[0], "pauldron", (4.4, 21.8, -2.6), (8.8, 24.6, 2.6), "bronze", rot=("z", -22.5), pivot=(6.6, 23.2, 0),
              **EN)
    m.cube(m.BONES["skirt_front"], "tasset", (-3.2, 8.6, -3.0), (3.2, 13.4, -2.4), "bronze", **EN)
    m.cube(m.BONES["skirt_back"], "tasset_b", (-3.2, 8.6, 2.4), (3.2, 13.4, 3.0), "bronze", **EN)
    key = m.bone("windup", (0, 20.0, 3.2), torso)
    m.cube(key, "key_shaft", (-0.4, 19.6, 3.0), (0.4, 20.4, 6.0), "gold")
    m.cube(key, "key_bow", (-2.6, 18.8, 6.0), (2.6, 21.2, 6.8), "gold", **EN)
    m.cube_lr(key, key, "key_loop", (1.6, 17.6, 6.0), (2.8, 22.4, 6.8), "gold", rot=("z", 22.5), pivot=(2.2, 20, 6.4))
    sw = m.bone("sword", (6.5, 10.0, 0), AR[2])
    m.cube(sw, "grip", (6.1, 9.5, -2.2), (6.9, 10.5, 2.0), "leather")
    m.cube(sw, "guard", (5.0, 9.4, -2.8), (8.0, 10.6, -2.2), "gold", rot=("y", 22.5), pivot=(6.5, 10, -2.5))
    m.cube(sw, "blade", (6.2, 9.2, -15.0), (6.8, 10.8, -2.8), "iron_hi")
    m.cube(sw, "tip", (6.25, 9.5, -16.4), (6.75, 10.5, -14.6), "iron_hi", rot=("x", 45), pivot=(6.5, 10, -15.4))
    ck = m.bone("pocket_clock", (-6.5, 10.0, 0), AL[2])
    m.cube(ck, "pclock", (-8.0, 7.6, -2.4), (-5.0, 10.6, -1.8), "dial", decor={"all": "clock"})
    m.cube(ck, "pclock_rim", (-8.2, 7.4, -1.8), (-4.8, 10.8, -1.4), "gold", rot=("z", 45), pivot=(-6.5, 9.1, -1.6))
    m.ZERO_BONES += ["sword", "pocket_clock", "windup"]

    def extra(a, t, s):
        a.rot("sword", t, 50, 0, 0)

    a = GM.human_idle(m, arm_r=(-25, 0, 8), arm_l=(-30, 0, -8), extra=extra)
    FX.spin(a, "windup", 2.4, 1, "z")
    a = GM.human_walk(m, leg=24, arm=12, arm_r=(-30, 0, 8), arm_l=(-30, 0, -8), extra=extra)
    FX.spin(a, "windup", 1.0, 1, "z")
    a = m.anim("attack", 0.7, "once")
    a.rest(0)
    a.pose(0.15, {"right_arm": (-150, 0, 20), "sword": (40, 0, 0), "torso": (-5, 15, 0)})
    a.pose(0.3, {"right_arm": (-50, 0, -15), "sword": (0, 0, 0), "torso": (15, -15, 0)}, i="linear")
    a.rest(0.7)
    GM.human_hurt(m)
    a = GM.human_spawn(m, {"right_arm": (-170, 0, 10), "sword": (70, 0, 0), "left_arm": (-100, 0, -10)})
    FX.spin(a, "windup", 1.6, 2, "z")
    GM.human_death(m)
    return m


# ===========================================================================
# GUARDIAN DE LAS ERAS (ZOMBIE)
# ===========================================================================
def build_guardian():
    m = _model("kr_guardian", 1012)

    def head(m, hd):
        m.cube(hd, "helm", (-3.6, 24.6, -3.6), (3.6, 32.0, 3.8), "iron", decor={"north": "slit"})
        m.cube(hd, "helm_top", (-3.0, 31.6, -3.2), (3.0, 33.0, 3.4), "iron_hi", rot=("x", 22.5), pivot=(0, 32, 0))
        m.cube(hd, "crest", (-0.5, 31.6, -3.6), (0.5, 35.4, 3.6), "gold")
        hourglass(m, hd, "hg", 0, 27.6, -4.0, 0.45)
        m.cube_lr(hd, hd, "wing", (3.4, 27.0, -0.6), (4.4, 33.0, 0.6), "gold", rot=("z", -22.5), pivot=(3.9, 27, 0))

    H = AN.humanoid(m, k=1.25, mats={"skin": "iron", "chest": "iron", "belly": "iron_hi", "arm": "iron", "hand": "iron_hi",
                                      "thigh": "robe_dark", "shin": "iron", "foot": "iron_hi", "pelvis": "robe_dark"},
                    head=head)
    torso, waist = H["torso"], H["waist"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    m.cube(torso, "breast", (-5.0, 18.0, -3.9), (5.0, 23.8, -3.2), "iron", decor={"all": "plate"} if "plate" in m.DECOR else EN["decor"])
    m.cube(torso, "trim", (-5.2, 17.6, -4.0), (5.2, 18.4, 3.6), "gold")
    m.cube_lr(AR[0], AL[0], "pauldron", (4.0, 22.0, -3.6), (10.4, 26.0, 3.6), "iron", rot=("z", -22.5), pivot=(7.2, 24, 0), **EN)
    m.cube_lr(AR[0], AL[0], "pauldron_rim", (4.4, 21.6, -3.8), (10.6, 22.4, 3.8), "gold", rot=("z", -22.5), pivot=(7.2, 24, 0))
    m.cube(m.BONES["skirt_front"], "tabard", (-3.0, 3.0, -3.6), (3.0, 13.4, -3.0), "robe", **RB)
    m.cube(m.BONES["skirt_back"], "tabard_b", (-3.6, 3.0, 3.0), (3.6, 13.4, 3.6), "robe", rot=("x", 22.5), pivot=(0, 13, 3.3),
           **RB)
    sh = m.bone("shield", (-8.6, 15.0, 0), AL[1])
    m.cube(sh, "shield_disc", (-9.8, 8.4, -5.0), (-8.8, 19.6, 5.0), "iron", decor={"all": "engraved"})
    m.cube(sh, "shield_disc45", (-9.7, 9.0, -4.4), (-8.9, 19.0, 4.4), "iron_hi", rot=("x", 45), pivot=(-9.3, 14, 0))
    for k in range(8):
        a = 2 * math.pi * k / 8
        y, z = 14 + 6.4 * math.cos(a), 6.4 * math.sin(a)
        m.cube(sh, f"shield_tooth{k}", (-9.7, y - 0.9, z - 0.9), (-8.9, y + 0.9, z + 0.9), "gold", rot=("x", 45),
               pivot=(-9.3, y, z))
    m.cube(sh, "shield_boss", (-10.4, 12.6, -1.4), (-9.6, 15.4, 1.4), "dial", decor={"all": "clock"})
    ax = m.bone("axe", (6.5, 10.0, 0), AR[2])
    m.cube(ax, "haft", (6.1, 9.5, -18.0), (6.9, 10.5, 3.0), "wood")
    m.cube(ax, "head", (6.0, 4.6, -18.6), (7.0, 10.0, -13.6), "iron_hi", rot=("x", -22.5), pivot=(6.5, 10, -16))
    m.cube(ax, "edge", (6.1, 3.4, -19.4), (6.9, 5.4, -12.8), "glow", rot=("x", -22.5), pivot=(6.5, 10, -16))
    m.cube(ax, "spike", (6.1, 10.0, -17.0), (6.9, 13.0, -15.6), "gold", rot=("x", 22.5), pivot=(6.5, 10, -16.3))
    m.ZERO_BONES += ["axe", "shield"]
    extra = lambda a, t, s: a.rot("axe", t, 55, 0, 0)  # noqa: E731
    GM.human_idle(m, arm_r=(-25, 0, 10), arm_l=(-35, 25, -6), extra=extra)
    GM.human_walk(m, leg=20, arm=10, lean=6, arm_r=(-30, 0, 10), arm_l=(-35, 25, -6), extra=extra)
    a = m.anim("attack", 0.8, "once")
    a.rest(0)
    a.pose(0.2, {"right_arm": (-170, 0, 10), "axe": (60, 0, 0), "torso": (-8, 10, 0), "left_arm": (-35, 25, -6)})
    a.pose(0.35, {"right_arm": (-50, 0, -10), "axe": (0, 0, 0), "torso": (25, -10, 0), "left_arm": (-35, 25, -6)}, i="linear")
    a.rest(0.8)
    a = m.anim("block", 0.8, "once")
    a.rest(0)
    a.pose(0.15, {"left_arm": (-80, 50, 0), "torso": (5, -10, 0)})
    a.pose(0.6, {"left_arm": (-80, 50, 0), "torso": (5, -10, 0)})
    a.rest(0.8)
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-170, 0, 10), "axe": (70, 0, 0), "left_arm": (-80, 50, 0)})
    GM.human_death(m)
    return m


# ===========================================================================
# SAETERO DEL OCASO (SKELETON)
# ===========================================================================
def build_archer():
    m = _model("kr_archer", 1013)

    def head(m, hd):
        m.cube(hd, "face", (-2.8, 25.0, -2.8), (2.8, 30.8, 2.8), "black", decor={"north": "hood_face"})
        m.cube(hd, "hood_back", (-3.2, 24.4, -1.0), (3.2, 30.8, 3.6), "dusk_dark", decor={"all": "beard"})
        m.cube_lr(hd, hd, "hood_side", (2.6, 24.2, -3.4), (3.7, 31.4, 3.4), "dusk", rot=("z", -22.5), pivot=(3.1, 31.4, 0),
                  decor={"all": "beard"})
        m.cube(hd, "hood_top", (-2.0, 30.2, -3.6), (2.0, 32.2, 3.2), "dusk", rot=("x", 22.5), pivot=(0, 31.2, -0.2),
               decor={"all": "beard"})
        m.cube(hd, "hood_peak", (-1.0, 31.6, -4.2), (1.0, 33.6, -2.2), "dusk_dark", rot=("x", -45), pivot=(0, 32.6, -3.2))
        for sx in (1, -1):
            m.cube(hd, f"eye{sx}", (1.2 * sx - 0.6, 27.4, -3.0), (1.2 * sx + 0.6, 28.2, -2.7), "sand")
        m.cube(hd, "hood_tip", (-1.6, 29.0, 3.0), (1.6, 31.0, 7.0), "dusk_dark", rot=("x", -22.5), pivot=(0, 30, 3))

    H = AN.humanoid(m, k=0.85, mats={"skin": "bone", "chest": "leather", "belly": "dusk_dark", "arm": "dusk_dark",
                                      "hand": "bone", "thigh": "dusk_dark", "shin": "leather", "foot": "leather",
                                      "pelvis": "leather"}, head=head)
    torso, waist = H["torso"], H["waist"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    m.cube(torso, "mantle", (-4.6, 20.4, -3.0), (4.6, 24.2, 3.0), "dusk", decor={"all": "robe"})
    m.cube_lr(torso, torso, "mantle_drape", (3.2, 19.0, -3.2), (5.0, 24.0, 3.2), "dusk", rot=("z", 22.5), pivot=(4.2, 24, 0),
              **RB)
    cl = m.bone("cloak", (0, 23.6, 2.8), torso)
    m.cube(cl, "cloak", (-4.4, 3.0, 2.8), (4.4, 23.6, 3.4), "dusk_dark", rot=("x", 22.5), pivot=(0, 23.6, 3.1), **RB)
    q = m.bone("quiver", (0, 18, 3.4), torso)
    m.cube(q, "quiver", (-1.4, 12.0, 3.4), (1.4, 22.0, 5.6), "leather", rot=("z", 22.5), pivot=(0, 17, 4.5))
    for i, x in enumerate((-0.7, 0.0, 0.7)):
        m.cube(q, f"arrow{i}", (x - 0.25, 21.6, 4.2), (x + 0.25, 24.6, 4.8), "glow" if i == 1 else "sand",
               rot=("z", 22.5), pivot=(0, 17, 4.5))
    m.cube(m.BONES["skirt_front"], "flap", (-2.6, 7.0, -2.8), (2.6, 13.2, -2.3), "dusk", **RB)
    bw = m.bone("bow", (-6.5, 10.0, 0), AL[2])
    segs = [((-6.9, -6.1), (10.0, 16.0), -1.2, ("x", 22.5)), ((-6.9, -6.1), (4.0, 10.0), -1.2, ("x", -22.5))]
    for i, ((x0, x1), (y0, y1), z, rot) in enumerate(segs):
        m.cube(bw, f"limb{i}", (x0, y0, z - 0.5), (x1, y1, z + 0.5), "wood", rot=rot, pivot=(-6.5, 10, z))
    m.cube(bw, "bow_grip", (-7.0, 8.8, -1.8), (-6.0, 11.2, -0.6), "gold")
    m.cube(bw, "string", (-6.6, 4.6, 0.6), (-6.4, 15.4, 0.8), "dial")
    for sy, yy in ((1, 15.6), (-1, 4.4)):
        m.cube(bw, f"tip{sy}", (-6.9, yy - 0.6, -2.8), (-6.1, yy + 0.6, -1.6), "glow")
    m.ZERO_BONES += ["bow", "cloak", "quiver"]
    GM.human_idle(m, arm_l=(-20, 0, -8), extra=lambda a, t, s: a.rot("cloak", t, 4 * s, 0, 0))
    GM.human_walk(m, leg=26, arm=16, extra=lambda a, t, s: a.rot("cloak", t, 10 + 4 * s, 0, 0))
    a = m.anim("attack", 0.9, "once")
    draw = {"left_arm": (-90, 0, 0), "right_arm": (-90, 0, -20), "torso": (0, 20, 0), "bow": (0, 0, 0)}
    a.rest(0)
    a.pose(0.25, draw)
    a.pose(0.5, {**draw, "right_arm": (-90, 30, -10)})
    a.pose(0.55, draw, i="linear")
    a.rest(0.9)
    GM.human_hurt(m)
    GM.human_spawn(m, {"left_arm": (-90, 0, 0), "right_arm": (-90, 0, -20)})
    GM.human_death(m)
    return m


# ===========================================================================
# DEVORADOR DE ERAS (RAVAGER)
# ===========================================================================
def build_devourer():
    m = _model("kr_devourer", 1014)
    root = m.root
    hb = m.bone("hitbox", (0, 18, 0), root)
    m.cube(hb, "hitbox", (-10, 0, -12), (10, 34, 12), "hitbox")
    m.bone("tag_name", (0, 42, 0), root)
    body = m.bone("body", (0, 20, 0), root)
    H = {"decor": {"all": "hide"}}
    m.cube(body, "barrel", (-8.0, 15.0, -10.0), (8.0, 29.0, 9.0), "hide", **H)
    m.cube(body, "barrel45", (-6.6, 14.0, -9.0), (6.6, 30.0, 8.0), "hide_dark", rot=("z", 45), pivot=(0, 22, 0), **H)
    m.cube(body, "hump", (-9.0, 22.0, -12.0), (9.0, 32.0, -1.0), "hide", rot=("x", -22.5), pivot=(0, 27, -6), **H)
    m.cube(body, "belly", (-6.0, 13.0, -7.0), (6.0, 16.0, 7.0), "hide_dark", **H)
    m.cube(body, "rump", (-7.0, 17.0, 6.0), (7.0, 27.0, 12.0), "hide", rot=("x", 22.5), pivot=(0, 22, 8), **H)
    # placas de armadura con numeros y engranaje incrustado
    for i, (z, ang) in enumerate(((-7.0, -22.5), (-1.0, 0), (5.0, 22.5))):
        m.cube(body, f"plate{i}", (-6.4, 29.0, z - 2.6), (6.4, 31.0, z + 2.6), "gold_dark", rot=("x", ang) if ang else None,
               pivot=(0, 30, z), **EN)
    g = m.bone("back_gear", (0, 34.0, -1.0), body)
    gear(m, g, "back_gear", 0, 34.0, -1.6, -0.4, 4.0, mat="gold", teeth=10)
    m.cube(g, "back_gear_dial", (-2.4, 31.6, -1.8), (2.4, 36.4, -1.4), "dial", decor={"all": "clock"})
    for i, (x, z) in enumerate(((-5.0, -4.0), (5.0, -4.0), (-5.0, 3.0), (5.0, 3.0))):
        RG.crystals(m, body, (x, 29.0, z), [(0, 0, 4.0, 0.8, ("z", 22.5 if x < 0 else -22.5))], f"spike{i}")
    # cabeza con mandibula, cuernos y ojos
    hd = m.bone("head", (0, 24.0, -11.0), body)
    m.cube(hd, "skull", (-6.0, 19.0, -24.0), (6.0, 29.0, -11.0), "hide", decor={"north": "beast_eyes", "all": "hide"})
    m.cube(hd, "brow", (-6.4, 26.0, -24.8), (6.4, 28.4, -20.0), "hide_dark", rot=("x", 22.5), pivot=(0, 27, -22))
    m.cube(hd, "snout", (-4.4, 18.4, -28.0), (4.4, 24.0, -23.0), "hide", **H)
    m.cube(hd, "nose", (-2.6, 22.6, -28.6), (2.6, 24.6, -26.6), "hide_dark")
    for sx in (1, -1):
        hn = [(4.6 * sx, 26.0, -16.0, (5.6 * sx, 27.2, -12.0)), ]
        m.cube(hd, f"horn_a{sx}", (5.0 * sx - 1.4, 25.4, -18.0), (5.0 * sx + 1.4, 28.2, -12.0), "horn",
               rot=("y", 22.5 * sx), pivot=(5.0 * sx, 26.8, -15))
        m.cube(hd, f"horn_b{sx}", (6.4 * sx - 1.1, 25.8, -12.6), (6.4 * sx + 1.1, 27.8, -6.6), "horn",
               rot=("x", -22.5), pivot=(6.4 * sx, 26.8, -12.6))
        m.cube(hd, f"horn_c{sx}", (6.8 * sx - 0.7, 27.2, -7.4), (6.8 * sx + 0.7, 28.8, -3.0), "horn",
               rot=("x", -45), pivot=(6.8 * sx, 27.8, -7.4))
        del hn
    jw = m.bone("jaw", (0, 19.0, -12.0), hd)
    m.cube(jw, "jaw", (-5.0, 14.6, -27.0), (5.0, 19.0, -12.0), "hide_dark", **H)
    m.cube(jw, "mouth", (-4.2, 18.8, -26.4), (4.2, 19.4, -13.0), "mouth")
    for i, x in enumerate((-3.6, -1.2, 1.2, 3.6)):
        m.cube(jw, f"tooth{i}", (x - 0.5, 19.0, -26.6), (x + 0.5, 21.4, -25.6), "fang")
    for sx in (1, -1):
        m.cube(jw, f"tusk{sx}", (4.0 * sx - 0.6, 18.6, -27.4), (4.0 * sx + 0.6, 23.4, -26.2), "fang", rot=("z", -22.5 * sx),
               pivot=(4.0 * sx, 19, -26.8))
    # patas en dos tramos con pezunas
    legs = (("leg_fr", 6.0, -7.0), ("leg_fl", -6.0, -7.0), ("leg_br", 6.0, 6.0), ("leg_bl", -6.0, 6.0))
    for n, x, z in legs:
        up = m.bone(n, (x, 18.0, z), body)
        m.cube(up, n + "_thigh", (x - 3.0, 9.0, z - 3.2), (x + 3.0, 19.0, z + 3.2), "hide", **H)
        lo = m.bone(n + "_low", (x, 9.0, z), up)
        m.cube(lo, n + "_shin", (x - 2.2, 2.0, z - 2.4), (x + 2.2, 9.4, z + 2.4), "hide_dark", **H)
        m.cube(lo, n + "_hoof", (x - 2.6, 0.0, z - 3.0), (x + 2.6, 2.4, z + 2.6), "black")
        m.cube(lo, n + "_band", (x - 2.5, 7.0, z - 2.7), (x + 2.5, 8.4, z + 2.7), "gold", **EN)
    tl = m.bone("tail", (0, 24.0, 11.0), body)
    m.cube(tl, "tail", (-1.2, 22.0, 11.0), (1.2, 25.0, 18.0), "hide", rot=("x", -22.5), pivot=(0, 24, 11))
    hourglass(m, tl, "tail_hg", 0, 18.0, 18.6, 0.9)
    m.ZERO_BONES = ["body", "head", "jaw", "tail", "back_gear"] + [n for n, _, _ in legs] + [n + "_low" for n, _, _ in legs]

    a = m.anim("idle", 2.0, "loop")
    for t, s in ((0, 0), (1.0, 1), (2.0, 0)):
        a.pos("body", t, 0, -0.5 * s, 0)
        a.rot("head", t, 4 * s, 0, 0)
        a.rot("jaw", t, 6 * s, 0, 0)
        a.rot("tail", t, 0, 15 * s - 7, 0)
    FX.spin(a, "back_gear", 2.0, 0.5, "z")
    a = m.anim("walk", 1.0, "loop")
    for t, s in ((0, 1), (0.5, -1), (1.0, 1)):
        a.rot("leg_fr", t, 25 * s, 0, 0)
        a.rot("leg_bl", t, 25 * s, 0, 0)
        a.rot("leg_fl", t, -25 * s, 0, 0)
        a.rot("leg_br", t, -25 * s, 0, 0)
        a.rot("tail", t, 0, 12 * s, 0)
        a.rot("head", t, 3 * s, 4 * s, 0)
    for t, s in ((0, 0), (0.25, 1), (0.5, 0), (0.75, 1), (1.0, 0)):
        a.pos("body", t, 0, -0.8 * s, 0)
        for n in ("leg_fr_low", "leg_fl_low", "leg_br_low", "leg_bl_low"):
            a.rot(n, t, 20 * s, 0, 0)
    FX.spin(a, "back_gear", 1.0, 0.5, "z")
    a = m.anim("attack", 0.9, "once")                     # embestida con la cabeza y mordisco
    a.rest(0)
    a.pose(0.25, {"head": (-25, 0, 0), "jaw": (35, 0, 0), "body": {"r": (-8, 0, 0), "p": (0, 0, 3)}})
    a.pose(0.45, {"head": (25, 0, 0), "jaw": (0, 0, 0), "body": {"r": (8, 0, 0), "p": (0, 0, -8)}}, i="linear")
    a.rest(0.9)
    a = m.anim("roar", 1.4, "once")
    a.rest(0)
    a.pose(0.3, {"head": (-35, 0, 0), "jaw": (45, 0, 0), "body": (-10, 0, 0), "leg_fr": (-25, 0, 0), "leg_fl": (-25, 0, 0)})
    a.pose(1.0, {"head": (-35, 0, 0), "jaw": (45, 0, 0), "body": (-10, 0, 0), "leg_fr": (-25, 0, 0), "leg_fl": (-25, 0, 0)})
    a.rest(1.4)
    a = m.anim("hurt", 0.35, "once")
    a.rest(0, ["head", "body"])
    a.pose(0.1, {"head": (-15, 10, 0), "body": (0, 0, 5)})
    a.rest(0.35, ["head", "body"])
    a = m.anim("spawn", 1.6, "once")
    a.pos("body", 0, 0, -26, 0)
    a.pos("body", 0.8, 0, 2, 0)
    a.pos("body", 1.0, 0, 0, 0)
    a.pose(1.1, {"head": (-35, 0, 0), "jaw": (45, 0, 0)})
    a.rest(1.6)
    a = m.anim("death", 1.8, "hold")
    a.rest(0)
    a.pose(0.4, {"head": (-30, 0, 0), "jaw": (40, 0, 0)})
    a.rot("root", 0.6, 0, 0, 0)
    a.rot("root", 1.2, 0, 0, 85, i="linear")
    a.rot("root", 1.8, 0, 0, 82)
    a.pose(1.2, {"head": (20, 0, 0), "jaw": (20, 0, 0), "leg_fr": (-30, 0, 0), "leg_br": (30, 0, 0)})
    return m


BUILDERS = {"kronos": build_kronos, "kr_sentinel": build_sentinel, "kr_guardian": build_guardian,
            "kr_archer": build_archer, "kr_devourer": build_devourer}
SHOTS = {
    "kronos": [("idle", 0.5, -30), ("rest", 0, 150), ("attack", 0.15, -50), ("summon", 0.6, -30)],
    "kr_sentinel": [("idle", 0.5, -30), ("rest", 0, 150), ("attack", 0.15, -60), ("attack", 0.3, -60)],
    "kr_guardian": [("idle", 0.5, -30), ("rest", 0, 150), ("attack", 0.2, -60), ("block", 0.3, -40)],
    "kr_archer": [("idle", 0.5, -30), ("rest", 0, 150), ("attack", 0.4, -60), ("walk", 0.25, -80)],
    "kr_devourer": [("idle", 0.5, -40), ("rest", 0, 140), ("attack", 0.25, -70), ("walk", 0.25, -90)],
}
VIEW = {"kronos": (32, 4.0), "kr_devourer": (22, 5.5), "kr_guardian": (20, 7.5)}
ACTIONS = [("slam", 0.12, -40), ("slam", 0.3, -40), ("quake", 0.4, -40), ("roar", 0.7, -30),
           ("charge", 0.5, -40), ("antirun", 0.4, -30), ("phase_change", 0.7, -40), ("last_breath", 0.8, -40)]


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
            if name == "kronos":
                FX.action_sheet(m, ACTIONS, PREVIEW / "kronos_acciones.png", focus=32, scale=4.0)


if __name__ == "__main__":
    main()
