#!/usr/bin/env python3
"""
Efectos de los ataques de OLD ENDER (modelos de ModelEngine con animacion propia).

Cada efecto es un mob invisible (armor stand marcador) que lleva el modelo, reproduce
la animacion "play" y se borra solo. Se invocan desde las skills con summon{}.

  oe_fx_portal     portal del vacio que se abre y se cierra    (OD_TeleportStrike, OD_SandWarp)
  oe_fx_shockwave  onda de arena que se expande por el suelo   (OD_SandPulse, OD_SandstormRift)
  oe_fx_collapse   anillo de pinchos de arenisca que brotan    (OD_DesertCollapse, OD_SandstormRift)
  oe_fx_eye        ojo de Horus gigante sobre el objetivo      (OD_EnderGaze)
  oe_fx_tornado    remolino de arena                           (OD_Sandstorm, OD_SandstormRift)

Uso: python3 tools/b02_fx.py [efecto ...] [--no-preview]
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
from bbmodel import Model  # noqa: E402
import b02_oldender as OE  # noqa: E402

BLUEPRINTS = OE.BLUEPRINTS
PREVIEW = OE.PREVIEW / "efectos"

FX_MATS = {
    "void": ((24, 10, 40), 4), "purple": ((170, 70, 235), 6), "glow": ((235, 190, 255), 3),
    "sand": ((222, 196, 130), 10), "sandstone": ((200, 166, 104), 10), "dust": ((236, 220, 170), 6),
    "gold": ((232, 178, 52), 8), "lapis": ((40, 72, 168), 6), "white": ((250, 246, 230), 2),
    "turquoise": ((60, 168, 160), 6),
}


def fx_model(name, seed):
    m = Model(name, FX_MATS, seed=seed, atlas_w=256)
    m.SHINE |= {"gold", "glow"}
    OE.egypt_decor(m)
    return m


def spin(a, bone, length, turns, axis="y", step=0.1):
    """Giro continuo (keyframes lineales para que no oscile)."""
    n = max(2, round(length / step))
    for i in range(n + 1):
        t = length * i / n
        ang = 360 * turns * i / n
        a.rot(bone, t, *(ang if ax == axis else 0 for ax in "xyz"), i="linear")


# --------------------------------------------------------------------------- portal
def build_portal():
    m = fx_model("oe_fx_portal", 301)
    root = m.root
    p = m.bone("portal", (0, 18, 0), root)
    # marco ovalado de 18 bloques de vacio con vetas moradas
    for k in range(18):
        th = 2 * math.pi * k / 18
        x, y = 9 * math.cos(th), 13 * math.sin(th)
        mat = "purple" if k % 3 == 0 else "void"
        m.cube(p, f"rim{k}", (x - 1.8, 18 + y - 1.8, -1.2), (x + 1.8, 18 + y + 1.8, 1.2), mat,
               decor={"all": "void" if mat == "void" else "orb"})
    core = m.bone("core", (0, 18, 0), p)
    m.cube(core, "core", (-7, 7, -0.3), (7, 29, 0.3), "void", decor={"all": "void"})
    m.cube(core, "core_glow", (-4, 11, -0.5), (4, 25, 0.5), "purple", decor={"all": "void"})
    sw = m.bone("swirl", (0, 18, 0), p)
    for k in range(6):
        th = 2 * math.pi * k / 6
        x, y = 4.5 * math.cos(th), 6.5 * math.sin(th)
        m.cube(sw, f"mote{k}", (x - 0.8, 18 + y - 0.8, -0.8), (x + 0.8, 18 + y + 0.8, 0.8), "glow")
    a = m.anim("play", 1.2, "once")
    a.scl("portal", 0, 0.05, 0.05, 1)
    a.scl("portal", 0.25, 1.15, 1.15, 1)
    a.scl("portal", 0.35, 1)
    a.scl("portal", 0.9, 1)
    a.scl("portal", 1.2, 0.05, 1.3, 1)
    spin(a, "swirl", 1.2, 1.5, "z")
    for t, s in ((0, 1), (0.3, 1.25), (0.6, 0.9), (0.9, 1.2), (1.2, 1)):
        a.scl("core", t, s, s, 1)
    return m


# --------------------------------------------------------------------------- onda
def build_shockwave():
    m = fx_model("oe_fx_shockwave", 302)
    root = m.root
    n = 22
    a = m.anim("play", 0.9, "once")
    for k in range(n):
        th = 2 * math.pi * k / n
        b = m.bone(f"chunk{k}", (0, 1, 0), root)
        mat = ("sand", "dust", "sandstone")[k % 3]
        m.cube(b, f"chunk{k}", (-3, 0, -3), (3, 3.5, 3), mat, decor={"all": "sandstone"})
        m.cube(b, f"puff{k}", (-2, 3.5, -2), (2, 6, 2), "dust")
        r0, r1 = 8, 128                     # de medio bloque a 8 bloques (radio de OD_SandPulse)
        for t, r, s in ((0, r0, 0.8), (0.15, r0 + (r1 - r0) * 0.45, 2.2), (0.55, r1 * 0.95, 3.2), (0.9, r1, 2.5)):
            # en ModelEngine/Blockbench el eje X de las posiciones va invertido
            a.pos(f"chunk{k}", t, -r * math.cos(th), 0, r * math.sin(th), i="linear" if t else "catmullrom")
            a.scl(f"chunk{k}", t, s, s if t < 0.9 else 0.05, s)
        a.rot(f"chunk{k}", 0, 0, -math.degrees(th), 0)
        a.rot(f"chunk{k}", 0.9, 0, -math.degrees(th) + 90, 0)
    return m


# --------------------------------------------------------------------------- pinchos
def build_collapse():
    m = fx_model("oe_fx_collapse", 303)
    root = m.root
    a = m.anim("play", 1.8, "once")
    spikes = [(48, k, 6) for k in range(6)] + [(104, k, 9) for k in range(9)]   # dos anillos: 3 y 6.5 bloques
    for k, (R, j, n) in enumerate(spikes):
        th = 2 * math.pi * (j + 0.5 * (R > 60)) / n
        x, z = R * math.cos(th), R * math.sin(th)
        b = m.bone(f"spike{k}", (x, 0, z), root, rotation=(0, -math.degrees(th), 0))
        h = 1.3 + 0.3 * (k % 3)
        m.cube(b, f"base{k}", (x - 5, 0, z - 5), (x + 5, 9 * h, z + 5), "sandstone", decor={"all": "sandstone"})
        m.cube(b, f"mid{k}", (x - 3.5, 9 * h, z - 3.5), (x + 3.5, 18 * h, z + 3.5), "sandstone",
               decor={"all": "sandstone"})
        m.cube(b, f"tip{k}", (x - 1.8, 18 * h, z - 1.8), (x + 1.8, 26 * h, z + 1.8), "sand")
        m.cube(b, f"rune{k}", (x - 1, 6 * h, z - 5.3), (x + 1, 12 * h, z - 4.9), "purple")
        delay = 0.0 if R < 60 else 0.12
        a.pos(f"spike{k}", 0, 0, -34, 0)
        a.pos(f"spike{k}", delay, 0, -34, 0)
        a.pos(f"spike{k}", delay + 0.14, 0, 3, 0, i="linear")
        a.pos(f"spike{k}", delay + 0.25, 0, 0, 0)
        a.pos(f"spike{k}", 1.3, 0, 0, 0)
        a.pos(f"spike{k}", 1.8, 0, -34, 0)
    c = m.bone("crack", (0, 0, 0), root)
    for k, ang in enumerate((0, 45, 0, -45)):          # 8 grietas en estrella (4 cubos que se cruzan)
        if k == 2:
            m.cube(c, f"crack{k}", (-36, 0.05, -0.8), (36, 0.35, 0.8), "purple")
        else:
            m.cube(c, f"crack{k}", (-0.8, 0.05, -36), (0.8, 0.35, 36), "purple",
                   **({"rot": ("y", ang), "pivot": (0, 0, 0)} if ang else {}))
    a.scl("crack", 0, 0.01)
    a.scl("crack", 0.2, 1)
    a.scl("crack", 1.4, 1)
    a.scl("crack", 1.8, 0.01)
    return m


# --------------------------------------------------------------------------- ojo
EYE = [
    "...LLLLLLLLLLLLLLLLL......",
    ".LLLLLLLLLLLLLLLLLLLLLL...",
    "......................LL..",
    "......GGGGGGGGG........L..",
    "....GGG.......GGG.........",
    "...G...WWPPPWW...GGGGGGGGG",
    "..G...WWPPDPPWW..GGGGGGGGG",
    "...G...WWPPPWW...G........",
    "....GGG.......GGG.........",
    "......GGGGGGGGG...........",
    ".......G.....G............",
    ".......G......G...........",
    ".......G.......G..........",
    ".......G........G...GG....",
    "......GG.........G.G..G...",
    ".....GG...........G...G...",
    "....GG.............GGG....",
]


def build_eye():
    m = fx_model("oe_fx_eye", 304)
    root = m.root
    px = 1.25                                       # tamano de cada "pixel" del sprite
    w, h = len(EYE[0]), len(EYE)
    up = 40                                         # flota 2.5 bloques sobre el objetivo
    eye = m.bone("eye", (0, up + h * px / 2, 0), root)
    pupil = m.bone("pupil", (0, up + h * px - 6 * px - px / 2, 0), eye)
    mats = {"L": "lapis", "G": "gold", "W": "white", "P": "purple", "D": "void"}
    for ry, row in enumerate(EYE):
        x = 0
        while x < w:
            ch = row[x]
            if ch == ".":
                x += 1
                continue
            x1 = x
            while x1 < w and row[x1] == ch:
                x1 += 1
            y0 = up + (h - 1 - ry) * px
            bone = pupil if ch in "PD" else eye
            depth = 1.2 if ch in "PD" else 0.8
            m.cube(bone, f"e{ry}_{x}", ((x - w / 2) * px, y0, -depth), ((x1 - w / 2) * px, y0 + px, depth),
                   mats[ch], decor={"all": "orb"} if ch == "P" else None)
            x = x1
    a = m.anim("play", 1.3, "once")
    a.scl("eye", 0, 0.05, 0.05, 0.05)
    a.scl("eye", 0.3, 1.15)
    a.scl("eye", 0.4, 1)
    a.scl("eye", 1.0, 1)
    a.scl("eye", 1.3, 1.2, 0.02, 1)
    for t, s in ((0, 1), (0.35, 1), (0.5, 1.7), (0.65, 1.1), (1.3, 1)):
        a.scl("pupil", t, s)
    for t, y in ((0, 0), (0.65, 1.5), (1.3, 0.5)):
        a.pos("eye", t, 0, y, 0)
    return m


# --------------------------------------------------------------------------- remolino
def build_tornado():
    m = fx_model("oe_fx_tornado", 305)
    root = m.root
    a = m.anim("play", 3.0, "once")
    tw = m.bone("twister", (0, 0, 0), root)
    for j in range(6):
        ring = m.bone(f"ring{j}", (0, 0, 0), tw)
        y = 2 + j * 9
        R = 6 + j * 3.2
        n = 6 + j
        for k in range(n):
            th = 2 * math.pi * k / n + j * 0.5
            x, z = R * math.cos(th), R * math.sin(th)
            s = 1.6 + j * 0.25
            mat = ("sand", "dust", "sandstone")[(k + j) % 3]
            m.cube(ring, f"r{j}_{k}", (x - s, y - s * 0.7, z - s), (x + s, y + s * 0.7, z + s), mat)
        spin(a, f"ring{j}", 3.0, 3.5 - j * 0.35)
    m.cube(tw, "eye_of_storm", (-1.5, 0, -1.5), (1.5, 50, 1.5), "purple", decor={"all": "void"})
    a.scl("twister", 0, 0.1, 0.05, 0.1)
    a.scl("twister", 0.35, 1.1)
    a.scl("twister", 0.5, 1)
    a.scl("twister", 2.6, 1)
    a.scl("twister", 3.0, 1.6, 0.05, 1.6)
    return m


BUILDERS = {"oe_fx_portal": build_portal, "oe_fx_shockwave": build_shockwave, "oe_fx_collapse": build_collapse,
            "oe_fx_eye": build_eye, "oe_fx_tornado": build_tornado}
SHOTS = {
    "oe_fx_portal": [0.1, 0.35, 0.7, 1.1],
    "oe_fx_shockwave": [0.05, 0.15, 0.4, 0.8],
    "oe_fx_collapse": [0.08, 0.3, 1.0, 1.6],
    "oe_fx_eye": [0.15, 0.4, 0.5, 1.2],
    "oe_fx_tornado": [0.2, 0.8, 1.6, 2.8],
}
VIEW = {"oe_fx_portal": (18, 7.0, -25), "oe_fx_shockwave": (6, 1.1, -20), "oe_fx_collapse": (14, 1.9, -20),
        "oe_fx_eye": (51, 9.0, -15), "oe_fx_tornado": (26, 4.5, -20)}


def previews(name, m):
    import render_preview as RP
    RP.G = m
    tw, th = m.pack()
    tex = m.paint(tw, th)
    a = m.ANIMS[0]
    focus, scale, yaw = VIEW[name]
    frames = []
    for t in SHOTS[name]:
        im = RP.render(tex, a, t, yaw=yaw, pitch=25, size=(300, 300), focus=focus, scale=scale)
        ImageDraw.Draw(im).text((8, 8), f"{name}  {t:g}s", fill=(230, 230, 230))
        frames.append(im)
    sheet = Image.new("RGB", (300 * len(frames), 300))
    for i, f in enumerate(frames):
        sheet.paste(f, (i * 300, 0))
    PREVIEW.mkdir(parents=True, exist_ok=True)
    sheet.save(PREVIEW / f"{name}.png")


def main():
    only = [x for x in sys.argv[1:] if not x.startswith("--")]
    for name, fn in BUILDERS.items():
        if only and name not in only:
            continue
        m = fn()
        out = BLUEPRINTS / name / f"{name}.bbmodel"
        out.parent.mkdir(parents=True, exist_ok=True)
        m.build(out)
        print(f"OK {name}: cubos={len(m.CUBES)} huesos={len(m.BONES)}")
        if "--no-preview" not in sys.argv:
            previews(name, m)


if __name__ == "__main__":
    main()
