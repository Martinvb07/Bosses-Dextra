#!/usr/bin/env python3
"""
Boss 03 - BAAL y sus subditos (modelos de ModelEngine).

  baal            espiritu samurai demoniaco del Templo Sakura: kabuto con cuernos dorados,
                  mascara oni, o-yoroi lacado, sode, hakama, nodachi y estandarte sashimono
  undead_samurai  samurai esqueleto con jingasa, armadura rota y katana mellada (WITHER_SKELETON)
  yokai           espiritu kitsune: mascara de zorro, cuerpo de llama y tres colas (ALLAY)
  shadow_ninja    ninja de sombra con bufanda roja y piernas de humo (VEX)

Uso: python3 tools/b03_baal.py [modelo ...] [--no-preview]
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

ROOT = Path(__file__).resolve().parent.parent / "Modelos/03_Baal"
BLUEPRINTS = ROOT / "ModelEngine/blueprints"
PREVIEW = ROOT / "preview"

PINK_GLOW = (255, 150, 220)
GOLD_HI = (255, 230, 140)

MATS = {
    "lacquer": ((30, 24, 34), 4), "red": ((168, 30, 42), 7), "gold": ((226, 176, 60), 8),
    "spirit": ((206, 182, 240), 6), "purple": ((86, 40, 118), 7), "pink": ((240, 132, 196), 7),
    "sakura": ((255, 186, 214), 5), "steel": ((206, 210, 222), 4), "wrap": ((42, 30, 54), 5),
    "glow": ((255, 176, 232), 3), "white": ((240, 236, 226), 4), "wood": ((92, 54, 32), 8),
    "bone": ((222, 212, 186), 8), "rust": ((122, 60, 40), 10), "straw": ((176, 140, 80), 10),
    "shadow": ((26, 22, 32), 4), "smoke": ((58, 48, 74), 6), "flame": ((150, 90, 240), 6),
    "blue": ((90, 150, 255), 6), "skin": ((206, 182, 240), 6), "leather": ((60, 40, 30), 6),
    "bronze": ((196, 140, 58), 8), "hitbox": ((255, 255, 255), 0),
}


def japan_decor(m):
    D = m.decor

    @D
    def d_lamellar(f):
        """Placas de laca en filas con cordones rojos (odoshi)."""
        for y in range(f.h):
            if y % 3 == 2:
                for x in range(f.w):
                    f.shade(x, y, 0.55)
            if y % 6 == 1:
                for x in range(2, f.w, 5):
                    f.put(x, y, mul(m.MAT["red"], 0.8))
        for x in range(f.w):
            f.put(x, 0, mul(m.MAT["gold"], 0.9))

    @D
    def d_gold_band(f):
        for x in range(f.w):
            f.put(x, 0, GOLD_HI)
        for x in range(1, f.w, 3):
            f.put(x, f.h // 2, m.MAT["red"])

    @D
    def d_orb(f):
        f.rect(0, 0, f.w, f.h, mul(m.MAT["blue"], 0.7))
        f.rect(1, 1, f.w - 1, f.h - 1, (190, 220, 255))
        f.put(1, 1, (255, 255, 255))

    @D
    def d_suji(f):
        for x in range(1, f.w, 3):
            for y in range(f.h):
                f.put(x, y, mul(m.MAT["gold"], 0.85))

    @D
    def d_oni_face(f):
        w = f.w
        dark = (30, 8, 12)
        for ex in (1, w - 5):                     # ojos rasgados encendidos
            f.rect(ex, 3, ex + 4, 5, dark)
            f.rect(ex + 1, 3, ex + 3, 4, PINK_GLOW)
        f.rect(1, 1, 5, 2, dark)                  # cejas fruncidas
        f.rect(w - 5, 1, w - 1, 2, dark)
        f.rect(2, f.h - 4, w - 2, f.h - 2, dark)  # boca con colmillos
        for x in (3, w - 4):
            f.put(x, f.h - 4, (250, 246, 230))
            f.put(x, f.h - 3, (250, 246, 230))

    @D
    def d_sakura(f):
        """Flor de cerezo (mon) en el centro de la cara."""
        if f.name in ("up", "down"):
            return
        cx, cy = f.w // 2, f.h // 2
        for dx, dy in ((0, -2), (2, -1), (1, 2), (-1, 2), (-2, -1)):
            f.rect(cx + dx - 1, cy + dy - 1, cx + dx + 1, cy + dy + 1, (255, 236, 244))
        f.put(cx, cy, m.MAT["gold"])
        f.put(cx - 1, cy, (230, 90, 150))

    @D
    def d_pleats(f):
        for x in range(0, f.w, 3):
            for y in range(f.h):
                f.shade(x, y, 0.75)

    @D
    def d_blade(f):
        if f.name in ("east", "west"):
            for x in range(f.w):
                f.put(x, f.h - 1, (255, 255, 255))
                if (x // 3) % 2:
                    f.put(x, f.h - 2, (236, 240, 250))

    @D
    def d_tsuka(f):
        for x in range(f.w):
            for y in range(f.h):
                if (x + y) % 4 < 2:
                    f.put(x, y, (220, 214, 200))

    @D
    def d_skull_face(f):
        w = f.w
        for ex in (1, w - 5):
            f.rect(ex, 3, ex + 4, 7, (20, 14, 18))
            f.put(ex + 2, 5, (190, 110, 255))
        f.rect(w // 2 - 1, 7, w // 2 + 1, 9, (40, 30, 30))
        for x in range(2, w - 2, 2):
            f.put(x, f.h - 2, (40, 30, 30))

    @D
    def d_ribs(f):
        if f.name not in ("north", "south"):
            return
        for y in range(1, f.h, 2):
            for x in range(f.w):
                f.put(x, y, (40, 30, 34))
        for y in range(f.h):
            f.put(f.w // 2, y, m.MAT["bone"])

    @D
    def d_rusty(f):
        rng = random.Random(f.x0 * 7 + f.y0)
        for _ in range(f.w * f.h // 5):
            f.put(rng.randrange(f.w), rng.randrange(f.h), mul(m.MAT["rust"], rng.uniform(0.8, 1.2)))
        for y in range(2, f.h, 3):
            for x in range(f.w):
                f.shade(x, y, 0.6)

    @D
    def d_fox_mask(f):
        w = f.w
        red = (210, 30, 50)
        for ex in (1, w - 4):                   # ojos rasgados
            f.rect(ex, 3, ex + 3, 4, (20, 10, 20))
            f.put(ex + 1, 3, PINK_GLOW)
        for x in range(w):                       # marcas rojas
            if x in (0, 1, w - 2, w - 1):
                f.put(x, 1, red)
                f.put(x, 6, red)
        f.rect(w // 2 - 1, 0, w // 2 + 1, 2, red)

    @D
    def d_ear_in(f):
        if f.name == "north":
            f.rect(1, 1, f.w - 1, f.h, (210, 30, 50))

    @D
    def d_ninja_eyes(f):
        w = f.w
        f.rect(0, 4, w, 7, (14, 12, 18))
        for ex in (2, w - 5):
            f.rect(ex, 5, ex + 3, 6, PINK_GLOW)

    @D
    def d_wisp(f):
        for y in range(f.h):
            for x in range(f.w):
                if (x * 3 + y * 5) % 7 == 0:
                    f.shade(x, y, 1.25)

    @D
    def d_ofuda(f):
        if f.name in ("north", "south"):
            for y in range(1, f.h - 1, 2):
                f.put(f.w // 2, y, (170, 20, 30))


def _model(name, seed, extra=None):
    m = Model(name, {**MATS, **(extra or {})}, seed=seed, atlas_w=256)
    m.SHINE |= {"gold", "steel", "lacquer"}
    m.WOOD |= {"wood"}
    GM.add_common_decor(m)
    japan_decor(m)
    return m


L = {"decor": {"all": "lamellar"}}


# ===========================================================================
# BAAL
# ===========================================================================
def baal_head(m, hd):
    m.cube(hd, "skull", (-3.2, 25.2, -3.0), (3.2, 30.8, 3.3), "spirit")
    # mascara oni (menpo) con mejillas en angulo, cejas, nariz y mandibula con colmillos
    m.cube(hd, "mask", (-2.9, 24.8, -3.9), (2.9, 30.0, -3.1), "red", decor={"north": "oni_face"})
    m.cube_lr(hd, hd, "cheek", (2.4, 24.8, -3.7), (3.6, 29.2, -1.4), "red", rot=("y", -22.5), pivot=(2.6, 27, -3.2))
    m.cube(hd, "brow", (-3.1, 28.6, -4.5), (3.1, 29.5, -3.7), "red", rot=("x", 22.5), pivot=(0, 29.5, -3.9))
    m.cube_lr(hd, hd, "brow_horn", (2.2, 29.0, -4.4), (3.0, 31.4, -3.6), "white", rot=("z", -22.5), pivot=(2.6, 29.2, -4))
    m.cube(hd, "nose", (-0.7, 26.8, -4.6), (0.7, 28.6, -3.8), "red")
    m.cube(hd, "nostrils", (-1.2, 26.6, -4.5), (1.2, 27.4, -3.8), "red")
    m.cube(hd, "chin", (-2.4, 23.8, -4.4), (2.4, 25.2, -3.0), "lacquer", rot=("x", -22.5), pivot=(0, 25, -3.4))
    for sx in (1, -1):
        m.cube(hd, f"fang{sx}", (1.3 * sx - 0.35, 24.4, -4.7), (1.3 * sx + 0.35, 26.0, -4.2), "white")
    m.cube(hd, "beard", (-1.6, 22.4, -4.2), (1.6, 24.2, -3.4), "white", rot=("x", -22.5), pivot=(0, 24.2, -3.8))
    # kabuto: cupula en tres pisos y visera inclinada
    m.cube(hd, "bowl", (-3.9, 30.0, -3.8), (3.9, 32.0, 3.9), "lacquer", decor={"all": "suji"})
    m.cube(hd, "bowl_mid", (-3.4, 32.0, -3.3), (3.4, 33.2, 3.4), "lacquer", decor={"all": "suji"})
    m.cube(hd, "bowl_top", (-2.5, 33.2, -2.4), (2.5, 34.0, 2.5), "lacquer", decor={"all": "suji"})
    m.cube(hd, "tehen", (-0.8, 34.0, -0.8), (0.8, 34.7, 0.8), "gold")
    m.cube(hd, "visor", (-4.0, 29.6, -5.2), (4.0, 30.4, -3.6), "lacquer", rot=("x", -22.5), pivot=(0, 30.2, -3.6),
           decor={"north": "gold_band"})
    # shikoro (cubrenuca) en dos laminas que se abren
    m.cube(hd, "shikoro", (-4.4, 26.4, 3.0), (4.4, 30.4, 4.0), "lacquer", rot=("x", 22.5), pivot=(0, 30.4, 3.5), **L)
    m.cube(hd, "shikoro2", (-5.0, 23.8, 4.4), (5.0, 27.0, 5.2), "lacquer", rot=("x", 45), pivot=(0, 27, 4.8), **L)
    m.cube_lr(hd, hd, "shikoro_side", (3.5, 26.2, -2.4), (4.3, 30.4, 3.4), "lacquer", rot=("z", -22.5),
              pivot=(3.9, 30.4, 0), **L)
    m.cube_lr(hd, hd, "shikoro_side2", (4.5, 23.6, -2.0), (5.3, 27.0, 3.8), "lacquer", rot=("z", -45),
              pivot=(4.9, 27, 0), **L)
    m.cube_lr(hd, hd, "fukigaeshi", (3.7, 28.8, -4.4), (5.9, 31.2, -3.4), "lacquer", rot=("y", -45),
              pivot=(3.7, 30, -3.9), decor={"all": "gold_band"})
    # kuwagata: cuernos dorados que se curvan hacia fuera (tres tramos)
    segs = [(0, 3.0), (-22.5, 3.4), (-45, 3.2)]
    x, y = 1.1, 31.0
    for i, (ang, ln) in enumerate(segs):
        m.cube_lr(hd, hd, f"horn{i}", (x - 0.45, y - 0.2, -4.7), (x + 0.45, y + ln, -4.0), "gold",
                  rot=("z", ang) if ang else None, pivot=(x, y, -4.35))
        x += ln * math.sin(math.radians(-ang))
        y += ln * math.cos(math.radians(-ang))
    m.cube(hd, "mon", (-1.2, 30.6, -5.0), (1.2, 33.0, -4.4), "pink", decor={"north": "sakura"})


def build_baal():
    m = _model("baal", 303)
    H = AN.humanoid(m, k=1.1, mats={"skin": "purple", "hand": "spirit", "foot": "lacquer", "neck": "spirit"},
                    head=baal_head)
    torso, waist, body = H["torso"], H["waist"], H["body"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    RL, LL = H["legs"]["right"], H["legs"]["left"]
    for c in m.CUBES:
        if c.mat == "purple":
            c.decor.setdefault("all", "pleats")
    # hakama ancho que se abre hacia abajo
    m.cube_lr(RL[0], LL[0], "hakama_up", (0.0, 7.6, -2.8), (5.0, 13.8, 2.8), "purple", decor={"all": "pleats"})
    m.cube_lr(RL[1], LL[1], "hakama_low", (0.0, 1.2, -3.1), (5.0, 7.8, 2.9), "purple", decor={"all": "pleats"})
    m.cube_lr(RL[1], LL[1], "hakama_flare", (4.6, 0.6, -3.2), (5.4, 7.6, 3.0), "purple", rot=("z", 22.5),
              pivot=(5.0, 7.6, 0), decor={"all": "pleats"})
    m.cube_lr(RL[1], LL[1], "hakama_front", (0.2, 0.8, -3.6), (4.8, 7.4, -3.0), "purple", rot=("x", -22.5),
              pivot=(2.5, 7.4, -3.2), decor={"all": "pleats"})
    m.cube_lr(RL[0], LL[0], "haidate", (0.4, 8.4, -3.4), (4.6, 12.4, -2.8), "lacquer", rot=("x", -22.5),
              pivot=(2.5, 12.4, -3.1), **L)
    # do (coraza) en V: ancha arriba, estrecha en la cintura, con esquinas biseladas
    m.cube(torso, "do", (-5.2, 19.6, -3.5), (5.2, 23.6, 3.3), "lacquer", **L)
    m.cube(torso, "do_low", (-4.4, 16.4, -3.2), (4.4, 19.8, 3.0), "lacquer", **L)
    m.cube_lr(torso, torso, "do_bevel", (4.4, 19.6, -3.4), (5.8, 23.4, -1.2), "lacquer", rot=("y", -22.5),
              pivot=(4.8, 21.5, -3.0), **L)
    m.cube(torso, "do_trim", (-5.4, 22.7, -3.7), (5.4, 23.9, 3.5), "gold", decor={"all": "gold_band"})
    m.cube(torso, "do_mon", (-1.4, 19.4, -3.9), (1.4, 22.0, -3.5), "pink", decor={"all": "sakura"})
    m.cube_lr(torso, torso, "watagami", (1.0, 23.4, -2.8), (4.4, 24.4, 2.8), "lacquer", rot=("z", -22.5),
              pivot=(1.0, 23.9, 0), decor={"all": "gold_band"})
    m.cube(waist, "obi", (-4.6, 13.4, -2.9), (4.6, 15.4, 2.9), "pink")
    m.cube(waist, "obi_knot", (-1.2, 12.6, -3.5), (1.2, 15.0, -2.9), "pink", rot=("z", 22.5))
    m.cube(waist, "obi_tail", (-0.6, 9.0, -3.4), (0.6, 12.8, -3.0), "pink", rot=("z", -22.5), pivot=(0, 12.8, -3.2))
    # kusazuri: faldones de placas en dos pisos que se abren
    for bone, z0, z1, zr in ((m.BONES["skirt_front"], -3.6, -3.0, -22.5), (m.BONES["skirt_back"], 3.0, 3.6, 22.5)):
        nm = "f" if z0 < 0 else "b"
        m.cube(bone, f"kusazuri_{nm}", (-3.4, 10.0, z0), (3.4, 13.6, z1), "lacquer", **L)
        m.cube(bone, f"kusazuri_{nm}2", (-3.6, 6.6, z0), (3.6, 10.2, z1), "lacquer", rot=("x", zr / 1),
               pivot=(0, 10.1, (z0 + z1) / 2), **L)
    m.cube_lr(waist, waist, "kusazuri_s", (4.2, 9.6, -2.8), (4.9, 13.6, 2.8), "lacquer", rot=("z", 22.5),
              pivot=(4.5, 13.6, 0), **L)
    m.cube_lr(waist, waist, "kusazuri_s2", (5.6, 6.6, -2.8), (6.3, 10.0, 2.8), "lacquer", rot=("z", 45),
              pivot=(5.9, 10.0, 0), **L)
    # sode curvas (dos laminas), kote y manos espectrales
    m.cube_lr(AR[0], AL[0], "sode_cap", (5.4, 23.8, -3.2), (9.0, 25.0, 3.2), "gold", rot=("z", 22.5),
              pivot=(5.4, 24.4, 0), decor={"all": "gold_band"})
    m.cube_lr(AR[0], AL[0], "sode", (8.4, 19.6, -3.2), (9.3, 24.4, 3.2), "lacquer", rot=("z", 22.5),
              pivot=(8.8, 24.4, 0), **L)
    m.cube_lr(AR[0], AL[0], "sode_low", (10.1, 15.6, -3.0), (11.0, 20.4, 3.0), "lacquer", rot=("z", 45),
              pivot=(10.5, 20.4, 0), **L)
    m.cube_lr(AR[1], AL[1], "kote", (4.9, 12.2, -1.9), (8.1, 16.8, 1.9), "lacquer", decor={"all": "suji"})
    m.cube_lr(AR[1], AL[1], "kote_guard", (4.7, 15.8, -2.2), (8.3, 17.4, 2.2), "gold", decor={"all": "gold_band"})
    # haori espectral (capa corta) que ondea
    cp = m.bone("cape", (0, 23.6, 3.4), torso)
    m.cube(cp, "cape", (-5.0, 15.0, 3.3), (5.0, 23.6, 3.9), "glow", decor={"all": "wisp"})
    m.cube(cp, "cape_low", (-5.4, 8.2, 3.3), (5.4, 15.2, 3.9), "glow", rot=("x", 22.5), pivot=(0, 15.1, 3.6),
           decor={"all": "wisp"})
    # cintas de espiritu a la espalda
    for side, sx in (("r", 1), ("l", -1)):
        rb = m.bone(f"ribbon_{side}", (2.2 * sx, 23, 3.2), torso)
        m.cube(rb, f"ribbon_{side}", (2.2 * sx - 0.7, 8, 3.2), (2.2 * sx + 0.7, 23, 3.6), "glow",
               rot=("x", 22.5), pivot=(2.2 * sx, 23, 3.4), decor={"all": "wisp"})
    # sashimono (estandarte) con el mon de sakura
    bn = m.bone("banner", (0, 22, 3.8), torso)
    m.cube(bn, "pole", (-0.35, 16, 3.6), (0.35, 46, 4.3), "wood")
    m.cube(bn, "crossbar", (-3.8, 45.4, 3.6), (3.8, 46.0, 4.3), "wood")
    m.cube(bn, "flag", (-3.6, 33.0, 4.3), (3.6, 45.4, 4.6), "pink", decor={"south": "sakura", "north": "sakura"})
    m.cube(bn, "flag_hem", (-3.6, 32.4, 4.3), (3.6, 33.0, 4.6), "gold")
    # nodachi en la mano derecha y saya en la cadera izquierda
    kt = m.bone("katana", (6.5, 10.0, 0), AR[2])
    m.cube(kt, "tsuka", (6.05, 9.5, -4.0), (6.95, 10.5, 3.4), "wrap", decor={"all": "tsuka"})
    m.cube(kt, "kashira", (5.95, 9.4, 3.4), (7.05, 10.6, 3.9), "gold")
    m.cube(kt, "tsuba", (5.2, 8.2, -4.6), (7.8, 11.8, -4.0), "gold")
    m.cube(kt, "blade", (6.3, 9.0, -28.0), (6.7, 10.8, -4.6), "steel", decor={"all": "blade"})
    m.cube(kt, "blade_tip", (6.3, 9.6, -30.0), (6.7, 10.8, -28.0), "steel")
    m.cube(kt, "blade_glow", (6.25, 8.8, -27.0), (6.75, 9.1, -5.0), "glow")
    m.cube(waist, "saya", (-5.6, 11.4, -2.0), (-4.8, 12.6, 14.0), "lacquer", rot=("x", -22.5),
           pivot=(-5.2, 12, -1), decor={"all": "gold_band"})
    m.ZERO_BONES += ["katana", "banner", "ribbon_r", "ribbon_l", "cape"]

    def sway(a, t, s):
        a.rot("cape", t, 6 * s, 0, 0)
        a.rot("banner", t, 0, 3 * s - 1.5, 2 * s)
        a.rot("ribbon_r", t, 8 * s, 0, 4 * s)
        a.rot("ribbon_l", t, 4 + 6 * s, 0, -4 * s)

    GM.human_idle(m, arm_r=(-20, 0, 8), arm_l=(0, 0, -6),
                  extra=lambda a, t, s: (sway(a, t, s), a.rot("katana", t, 25, 0, 0)))
    GM.human_walk(m, leg=24, arm=10, bob=0.6, lean=6, arm_r=(-25, 0, 8),
                  extra=lambda a, t, s: (sway(a, t, s), a.rot("katana", t, 25, 0, 0)))

    a = m.anim("attack", 0.7, "once")          # tajo diagonal (impacto 0.3 s)
    a.rest(0)
    a.pose(0.15, {"right_arm": (-160, 0, 25), "torso": (-6, 25, 0), "katana": (40, 0, 0), "h_head": (0, -10, 0)})
    a.pose(0.3, {"right_arm": (-45, 0, -35), "torso": (12, -28, 0), "katana": (-10, 0, 0)}, i="linear")
    a.rest(0.7)

    a = m.anim("curse", 1.0, "once")           # maldicion con ofuda (impacto 0.4 s)
    a.rest(0)
    a.pose(0.25, {"left_arm": (-120, 15, -10), "torso": (-4, -18, 0), "h_head": (-6, -12, 0)})
    a.pose(0.4, {"left_arm": (-88, 0, 0), "torso": (6, -10, 0), "h_head": (4, -6, 0)}, i="linear")
    a.pose(0.7, {"left_arm": (-90, 0, 0), "torso": (6, -10, 0)})
    a.rest(1.0)

    a = m.anim("dash_slash", 1.0, "once")      # embestida con tajo (impacto 0.6 s)
    a.rest(0)
    a.pose(0.2, {"body": {"p": (0, -2, 0)}, "torso": (25, 0, 0), "right_arm": (30, 0, 30), "katana": (60, 0, 0),
                 "right_leg": (-30, 0, 0), "right_lower_leg": (40, 0, 0), "left_leg": (20, 0, 0)})
    a.pose(0.45, {"body": {"p": (0, 0, 0)}, "torso": (30, 0, 0), "right_arm": (-60, 0, 10), "katana": (30, 0, 0),
                  "right_leg": (-40, 0, 0), "left_leg": (30, 0, 0)})
    a.pose(0.6, {"torso": (15, -30, 0), "right_arm": (-100, 0, -45), "katana": (-10, 0, 0),
                 "right_leg": (-20, 0, 0), "left_leg": (15, 0, 0)}, i="linear")
    a.rest(1.0)

    a = m.anim("hex", 1.2, "once")             # giro con petalos (impacto 0.5 s)
    a.rest(0)
    a.pose(0.2, {"right_arm": (-170, 0, 10), "left_arm": (-20, 0, -40), "h_head": (-15, 0, 0)})
    for t, ang in ((0.25, 0), (0.33, 120), (0.42, 240), (0.5, 360)):
        a.rot("body", t, 0, ang, 0, i="linear")
    a.pose(0.5, {"right_arm": (-90, 0, 70), "left_arm": (-90, 0, -70), "h_head": (0, 0, 0)}, i="linear")
    a.pose(0.8, {"right_arm": (-85, 0, 60), "left_arm": (-85, 0, -60)})
    a.rest(1.2)
    a.rot("body", 1.2, 0, 360, 0)

    a = m.anim("nova", 1.4, "once")            # clava la nodachi en el suelo (impacto 0.6 s)
    a.rest(0)
    a.pose(0.35, {"right_arm": (-165, 0, 15), "left_arm": (-165, 0, -15), "katana": (70, 0, 0),
                  "h_head": (-20, 0, 0), "torso": (-8, 0, 0)})
    a.pose(0.6, {**GM.KNEEL, "right_arm": (-55, 0, -5), "left_arm": (-55, 0, 5), "katana": (-70, 0, 0),
                 "torso": (30, 0, 0), "h_head": (10, 0, 0)}, i="linear")
    a.pose(1.0, {**GM.KNEEL, "right_arm": (-55, 0, -5), "left_arm": (-55, 0, 5), "katana": (-70, 0, 0),
                 "torso": (28, 0, 0), "h_head": (-10, 0, 0)})
    a.rest(1.4)

    a = m.anim("veil", 0.8, "once")            # se envuelve en sombras
    a.rest(0)
    a.pose(0.25, {"left_arm": (-110, -40, 0), "torso": (5, 20, 0), "h_head": (10, 15, 0)})
    a.pose(0.5, {"left_arm": (-60, 50, 0), "torso": (5, -20, 0), "h_head": (5, -10, 0)})
    a.rest(0.8)

    a = m.anim("summon", 1.4, "once")          # alza la nodachi al cielo
    a.rest(0)
    pose = {"right_arm": (-178, 0, 0), "katana": (75, 0, 0), "left_arm": (-30, 0, -60), "h_head": (-25, 0, 0),
            "torso": (-10, 0, 0)}
    a.pose(0.4, pose)
    a.pose(1.0, pose)
    a.rest(1.4)

    a = m.anim("phase_change", 1.8, "once")    # se arrodilla y se levanta furioso
    a.rest(0)
    kneel = {**GM.KNEEL, "torso": (30, 0, 0), "h_head": (25, 0, 0), "right_arm": (-30, 0, 10), "left_arm": (-30, 0, -10)}
    a.pose(0.5, kneel)
    a.pose(0.8, kneel)
    roar = {"body": {"p": (0, 0, 0)}, "right_leg": (0, 0, 0), "right_lower_leg": (0, 0, 0), "left_leg": (0, 0, 0),
            "left_lower_leg": (0, 0, 0), "torso": (-15, 0, 0), "h_head": (-25, 0, 0), "right_arm": (-30, 0, 65),
            "left_arm": (-30, 0, -65), "katana": (40, 0, 0)}
    a.pose(1.2, roar, i="linear")
    a.pose(1.5, roar)
    a.rest(1.8)

    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-170, 0, 10), "katana": (70, 0, 0), "h_head": (-20, 0, 0)}, length=2.0)
    GM.human_death(m, 2.4)
    m.scale(1.45)
    return m


# ===========================================================================
# SAMURAI NO MUERTO (WITHER_SKELETON)
# ===========================================================================
def build_undead_samurai():
    m = _model("undead_samurai", 3031)

    def head(m, hd):
        m.cube(hd, "skull", (-3.0, 25.6, -3.0), (3.0, 31.0, 3.2), "bone", decor={"north": "skull_face"})
        m.cube(hd, "jaw", (-2.4, 24.4, -3.1), (2.4, 25.8, 1.0), "bone")
        m.cube(hd, "brim", (-6.6, 30.8, -6.6), (6.6, 31.5, 6.6), "straw", decor={"all": "pleats"})
        m.cube(hd, "hat_mid", (-4.6, 31.5, -4.6), (4.6, 32.4, 4.6), "straw", decor={"all": "pleats"})
        m.cube(hd, "hat_top", (-2.6, 32.4, -2.6), (2.6, 33.2, 2.6), "straw")
        m.cube(hd, "hat_knob", (-0.8, 33.2, -0.8), (0.8, 33.8, 0.8), "red")
        m.cube(hd, "chinstrap", (-3.1, 24.8, -0.4), (3.1, 25.4, 0.4), "red")

    H = AN.humanoid(m, k=0.9, mats={"skin": "bone", "chest": "bone", "belly": "bone", "foot": "lacquer"}, head=head)
    for c in m.CUBES:
        if c.name in ("ribs", "chest"):
            c.decor["all"] = "ribs"
    torso, waist = H["torso"], H["waist"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    RL, LL = H["legs"]["right"], H["legs"]["left"]
    m.cube(torso, "do_half", (-4.6, 15.2, -3.0), (4.6, 18.8, 2.9), "red", decor={"all": "rusty"})
    m.cube(torso, "strap", (-5.0, 18.0, -3.0), (5.0, 19.0, 2.9), "lacquer", rot=("z", 45), pivot=(0, 20, 0))
    m.cube(AL[0], "sode", (-8.9, 17.6, -2.8), (-8.1, 23.8, 2.8), "red", rot=("z", -22.5), pivot=(-8.5, 23.8, 0),
           decor={"all": "rusty"})
    m.cube(waist, "sash", (-4.5, 13.0, -2.6), (4.5, 15.0, 2.6), "red")
    m.cube(waist, "sash_end", (2.0, 7.5, -2.9), (3.2, 13.2, -2.5), "red", rot=("z", 22.5))
    m.cube_lr(RL[0], LL[0], "hakama", (0.0, 8.0, -2.4), (5.0, 13.6, 2.4), "smoke", decor={"all": "pleats"})
    m.cube_lr(RL[1], LL[1], "hakama_low", (-0.2, 3.0, -2.8), (5.2, 8.2, 2.6), "smoke", decor={"all": "pleats"})
    kt = m.bone("katana", (6.5, 10.0, 0), AR[2])
    m.cube(kt, "tsuka", (6.1, 9.5, -3.4), (6.9, 10.5, 2.8), "wrap", decor={"all": "tsuka"})
    m.cube(kt, "tsuba", (5.4, 8.6, -4.0), (7.6, 11.4, -3.4), "rust")
    m.cube(kt, "blade", (6.3, 9.1, -18.0), (6.7, 10.6, -4.0), "steel", decor={"all": "blade"})
    m.cube(kt, "chip", (6.3, 9.9, -19.5), (6.7, 10.6, -18.0), "steel")
    m.ZERO_BONES += ["katana"]
    GM.human_idle(m, arm_r=(-25, 0, 8), extra=lambda a, t, s: (a.rot("katana", t, 30, 0, 0),
                                                              a.rot("torso", t, 8, 0, 0)))
    GM.human_walk(m, leg=22, arm=12, lean=8, arm_r=(-30, 0, 8), extra=lambda a, t, s: a.rot("katana", t, 30, 0, 0))
    a = m.anim("attack", 0.7, "once")          # tajo (impacto 0.3 s)
    a.rest(0)
    a.pose(0.15, {"right_arm": (-150, 0, 20), "torso": (-6, 20, 0), "katana": (40, 0, 0)})
    a.pose(0.3, {"right_arm": (-50, 0, -30), "torso": (12, -22, 0), "katana": (0, 0, 0)}, i="linear")
    a.rest(0.7)
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-60, 0, 10), "katana": (20, 0, 0), "h_head": (-10, 0, 0)})
    GM.human_death(m)
    return m


# ===========================================================================
# YOKAI (ALLAY): espiritu kitsune
# ===========================================================================
YK_BONES = ["body", "h_head", "flame", "orbit"] + [f"tail{i}" for i in range(3)] + [f"tail{i}_tip" for i in range(3)]


def build_yokai():
    m = _model("yokai", 3032)
    m.SHINE |= {"flame", "glow"}
    root = m.root
    hb = m.bone("hitbox", (0, 8, 0), root)
    m.cube(hb, "hitbox", (-4, 2, -4), (4, 14, 4), "hitbox")
    m.bone("tag_name", (0, 20, 0), root)
    body = m.bone("body", (0, 8, 0), root)
    hd = m.bone("h_head", (0, 10, 0), body)
    m.cube(hd, "mask", (-3.0, 8.0, -3.0), (3.0, 13.0, 2.0), "white", decor={"north": "fox_mask"})
    m.cube(hd, "snout", (-1.4, 8.2, -5.0), (1.4, 10.4, -3.0), "white")
    m.cube(hd, "snout_tip", (-0.9, 8.3, -7.0), (0.9, 9.8, -4.9), "white")
    m.cube(hd, "nose", (-0.6, 9.2, -7.4), (0.6, 9.9, -6.9), "shadow")
    m.cube(hd, "snout_mark", (-0.4, 10.4, -4.8), (0.4, 10.7, -3.2), "red")
    m.cube(hd, "cheek_r", (2.6, 8.2, -2.6), (3.6, 10.0, 0.6), "white", rot=("y", -22.5), pivot=(2.6, 9, 0))
    m.cube(hd, "cheek_l", (-3.6, 8.2, -2.6), (-2.6, 10.0, 0.6), "white", rot=("y", 22.5), pivot=(-2.6, 9, 0))
    m.cube_lr(hd, hd, "ear", (0.8, 12.8, -1.2), (3.0, 14.8, 0.4), "white", decor={"all": "ear_in"},
              rot=("z", -22.5), pivot=(1.9, 12.9, -0.4))
    m.cube_lr(hd, hd, "ear_tip", (1.4, 14.8, -1.0), (2.4, 16.0, 0.2), "white", rot=("z", -22.5),
              pivot=(1.9, 12.9, -0.4))
    m.cube(hd, "hood", (-2.6, 9.0, 1.8), (2.6, 12.6, 3.0), "flame", decor={"all": "wisp"})
    fl = m.bone("flame", (0, 7, 0), body)
    m.cube(fl, "flame1", (-2.2, 4.6, -1.8), (2.2, 8.4, 2.2), "flame", decor={"all": "wisp"})
    m.cube(fl, "flame2", (-1.5, 2.2, -1.2), (1.5, 4.8, 1.6), "flame", decor={"all": "wisp"})
    m.cube(fl, "flame3", (-1.0, 0.2, -0.8), (1.0, 1.9, 1.4), "blue")
    m.cube(fl, "flame_core", (-1.0, 5.2, -2.1), (1.0, 7.0, -1.7), "glow")
    orb = m.bone("orbit", (0, 9, 0), body)
    for i, (x, z) in enumerate(((5, 0), (-5, 0))):
        m.cube(orb, f"hitodama{i}", (x - 0.8, 8.2, z - 0.8), (x + 0.8, 9.8, z + 0.8), "blue", decor={"all": "orb"})
    for i, ang in enumerate((-35, 0, 35)):
        t = m.bone(f"tail{i}", (0, 6, 2.4), body, rotation=(-45, ang, 0))
        m.cube(t, f"tail{i}", (-1.6, 4.4, 2.4), (1.6, 7.6, 7.6), "flame", decor={"all": "wisp"})
        tt = m.bone(f"tail{i}_tip", (0, 6, 7.6), t, rotation=(-20, 0, 0))
        m.cube(tt, f"tail{i}_tip", (-1.9, 4.2, 7.6), (1.9, 7.8, 11.2), "flame", decor={"all": "wisp"})
        m.cube(tt, f"tail{i}_end", (-1.4, 4.6, 11.2), (1.4, 7.4, 13.2), "white")
    m.ZERO_BONES = list(YK_BONES)

    def tails(a, t, s, amp=12):
        for i in range(3):
            ph = (s if i % 2 else -s)
            a.rot(f"tail{i}", t, amp * ph, 0, 0)
            a.rot(f"tail{i}_tip", t, -amp * 1.3 * ph, 0, 0)

    def orbit(a, length):
        n = 8
        for k in range(n + 1):
            a.rot("orbit", length * k / n, 0, 360 * k / n, 0, i="linear")

    a = m.anim("idle", 2.0, "loop")
    for t, s in ((0, 0), (0.5, 1), (1.0, 0), (1.5, -1), (2.0, 0)):
        a.pos("body", t, 0, 0.8 * s, 0)
        a.rot("h_head", t, 3 * s, 5 * s, 0)
        a.rot("flame", t, 0, 0, 6 * s)
        tails(a, t, s)
    orbit(a, 2.0)
    a = m.anim("walk", 1.0, "loop")
    for t, s in ((0, 0), (0.25, 1), (0.5, 0), (0.75, -1), (1.0, 0)):
        a.pos("body", t, 0, 0.6 * s, 0)
        a.rot("body", t, 12, 0, 4 * s)
        a.rot("flame", t, -15, 0, 0)
        tails(a, t, s, 18)
    orbit(a, 1.0)
    a = m.anim("attack", 0.9, "once")          # maldicion: la mascara se inclina y las colas se abren (0.4 s)
    a.rest(0)
    a.pose(0.25, {"h_head": (-20, 0, 15), "tail0": (-40, -20, 0), "tail1": (-50, 0, 0), "tail2": (-40, 20, 0)})
    a.pose(0.4, {"h_head": (15, 0, -10), "tail0": (20, -30, 0), "tail1": (25, 0, 0), "tail2": (20, 30, 0)},
           i="linear")
    a.rest(0.9)
    a = m.anim("hurt", 0.35, "once")
    a.rest(0, ["h_head", "body"])
    a.pose(0.08, {"h_head": (-20, 0, 10), "body": (10, 0, 0)})
    a.rest(0.35, ["h_head", "body"])
    a = m.anim("spawn", 1.2, "once")
    a.scl("body", 0, 0.05)
    a.rot("body", 0, 0, -360, 0)
    a.scl("body", 0.7, 1.15)
    a.rot("body", 0.7, 0, 0, 0)
    a.scl("body", 0.9, 1)
    a.rest(1.2)
    a = m.anim("death", 1.2, "hold")
    a.rest(0)
    a.scl("body", 0, 1)
    for k in range(5):
        a.rot("body", 1.2 * k / 4, 0, 180 * k, 0, i="linear")
    a.scl("body", 1.0, 0.1)
    a.pos("body", 1.2, 0, -4, 0)
    return m


# ===========================================================================
# NINJA DE SOMBRA (VEX)
# ===========================================================================
def build_shadow_ninja():
    m = _model("shadow_ninja", 3033)

    def head(m, hd):
        m.cube(hd, "hood", (-3.3, 25.0, -3.3), (3.3, 31.6, 3.5), "shadow", decor={"north": "ninja_eyes"})
        m.cube(hd, "brow", (-3.4, 28.8, -3.7), (3.4, 29.4, -3.2), "shadow")
        m.cube(hd, "knot", (-0.9, 29.2, 3.4), (0.9, 30.6, 4.4), "red")
        m.cube(hd, "knot_tail", (-0.4, 26.0, 4.0), (0.4, 29.4, 4.6), "red", rot=("x", 22.5), pivot=(0, 29.4, 4.3))

    H = AN.humanoid(m, k=0.85, mats={"skin": "shadow", "shin": "smoke", "foot": "smoke"}, head=head)
    torso, waist = H["torso"], H["waist"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    RL, LL = H["legs"]["right"], H["legs"]["left"]
    m.cube(torso, "wrap", (-4.0, 19.0, -2.6), (4.0, 20.0, 2.5), "smoke", rot=("z", 22.5))
    m.cube(waist, "belt", (-4.0, 13.4, -2.4), (4.0, 14.8, 2.4), "red")
    m.cube(torso, "shuriken", (-1.2, 18.8, 2.6), (1.2, 21.2, 3.0), "steel", rot=("z", 45), pivot=(0, 20, 2.8))
    m.cube_lr(AR[1], AL[1], "tekko", (5.0, 12.0, -1.6), (7.9, 13.6, 1.6), "red")
    for side, (bone, low) in (("r", RL), ("l", LL)):
        m.cube(low, f"smoke_{side}", ((1.4 if side == "r" else -3.6), -2.5, -1.0), ((3.6 if side == "r" else -1.4), 1.0, 1.2),
               "smoke", decor={"all": "wisp"})
    sc = m.bone("scarf", (0, 24, 2.6), torso)
    m.cube(sc, "scarf_ring", (-2.0, 23.2, -1.8), (2.0, 24.6, 2.8), "red")
    m.cube(sc, "scarf", (-1.0, 22.6, 2.6), (1.0, 23.6, 16.0), "red", rot=("x", 22.5), pivot=(0, 23.6, 2.6))
    tn = m.bone("tanto", (6.5, 10.0, 0), AR[2])
    m.cube(tn, "grip", (6.1, 9.5, -2.6), (6.9, 10.5, 2.2), "wrap", decor={"all": "tsuka"})
    m.cube(tn, "blade", (6.3, 9.2, -9.0), (6.7, 10.6, -2.6), "steel", decor={"all": "blade"})
    m.ZERO_BONES += ["scarf", "tanto"]
    float_legs = {"right_leg": (-25, 0, 0), "right_lower_leg": (45, 0, 0), "left_leg": (-5, 0, 0),
                  "left_lower_leg": (30, 0, 0)}
    a = m.anim("idle", 2.0, "loop")
    for t, s in ((0, 0), (1.0, 1), (2.0, 0)):
        a.pose(t, {**float_legs, "right_arm": (-30 + 5 * s, 0, 10), "left_arm": (-10, 0, -15 - 4 * s),
                   "torso": (8, 0, 0), "scarf": (6 * s, 8 * s - 4, 0), "tanto": (40, 0, 0)})
        a.pos("body", t, 0, 0.6 * s, 0)
    a = m.anim("walk", 0.8, "loop")             # vuela inclinado hacia delante
    for t, s in ((0, 0), (0.4, 1), (0.8, 0)):
        a.pose(t, {"right_leg": (35, 0, 0), "right_lower_leg": (30, 0, 0), "left_leg": (25, 0, 0),
                   "left_lower_leg": (40, 0, 0), "torso": (30, 0, 0), "h_head": (-25, 0, 0),
                   "right_arm": (30, 0, 15), "left_arm": (30, 0, -15), "scarf": (-15 + 10 * s, 6 * s, 0),
                   "tanto": (60, 0, 0)})
        a.pos("body", t, 0, 0.5 * s, 0)
    a = m.anim("attack", 0.6, "once")           # punalada (impacto 0.25 s)
    a.rest(0)
    a.pose(0.12, {"right_arm": (-30, 0, 30), "torso": (-5, 25, 0), "tanto": (80, 0, 0)})
    a.pose(0.25, {"right_arm": (-95, 0, -5), "torso": (15, -15, 0), "tanto": (0, 0, 0)}, i="linear")
    a.rest(0.6)
    GM.human_hurt(m)
    a = m.anim("spawn", 1.2, "once")            # sale del humo
    a.pos("body", 0, 0, -10, 0)
    a.scl("body", 0, 0.3)
    a.pos("body", 0.7, 0, 0, 0)
    a.scl("body", 0.7, 1)
    a.pose(0.7, float_legs)
    a.rest(1.2)
    a = m.anim("death", 1.4, "hold")            # se deshace en humo
    a.rest(0)
    a.pose(0.3, {"torso": (-20, 0, 0), "h_head": (-25, 0, 0), "right_arm": (10, 0, 40), "left_arm": (10, 0, -40)})
    a.scl("body", 0.3, 1)
    a.scl("body", 1.4, 0.05, 1.4, 0.05)
    a.pos("body", 1.4, 0, -6, 0)
    return m


BUILDERS = {"baal": build_baal, "undead_samurai": build_undead_samurai, "yokai": build_yokai,
            "shadow_ninja": build_shadow_ninja}
SHOTS = {
    "baal": [("rest", 0, -30), ("rest", 0, 150), ("attack", 0.15, -60), ("nova", 0.6, -40)],
    "undead_samurai": [("rest", 0, -30), ("rest", 0, 150), ("attack", 0.15, -60), ("attack", 0.3, -60)],
    "yokai": [("idle", 0.5, -30), ("idle", 0.5, -100), ("idle", 0.5, 150), ("attack", 0.25, -40)],
    "shadow_ninja": [("idle", 0.5, -30), ("walk", 0.3, -80), ("rest", 0, 150), ("attack", 0.25, -60)],
}
VIEW = {"baal": (34, 5.0), "yokai": (8, 14.0)}


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
