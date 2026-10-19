#!/usr/bin/env python3
"""
Efectos de los ataques de RED HAND (modelos de ModelEngine con animacion "play").

  rh_fx_slash      tajo carmesi del mandoble                          (RH_SlashCombo, cada golpe)
  rh_fx_mark       sello de la mano roja girando sobre el marcado     (RH_RedMark)
  rh_fx_shadow     estallido de sombra y sangre                       (RH_ShadowDash, invocaciones)
  rh_fx_hand       mano roja gigante que sale del suelo y se cierra   (RH_HandCrush)
  rh_fx_nova       ola de sangre con pinchos, 9 bloques               (RH_BloodNova)
  rh_fx_execution  circulo de runas que se carga 2 s y estalla        (RH_Execution)
  rh_fx_pillar     columna de sangre                                  (cambios de fase)

Uso: python3 tools/b04_fx.py [efecto ...] [--no-preview]
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
from bbmodel import Model  # noqa: E402
import b04_redhand as RH  # noqa: E402
from b02_fx import spin  # noqa: E402

BLUEPRINTS = RH.BLUEPRINTS
PREVIEW = RH.PREVIEW / "efectos"

FX_MATS = {
    "blood": ((150, 12, 18), 7), "crimson": ((100, 8, 16), 6), "glow": ((255, 64, 52), 3),
    "white": ((255, 230, 220), 2), "black": ((20, 16, 20), 3), "smoke": ((40, 30, 36), 5),
    "iron": ((60, 60, 68), 4),
}


def fx_model(name, seed):
    m = Model(name, FX_MATS, seed=seed, atlas_w=256)
    m.SHINE |= {"glow"}
    RH.gothic_decor(m)
    return m


def build_slash():
    m = fx_model("rh_fx_slash", 501)
    arc = m.bone("arc", (0, 18, -12), m.root, rotation=(0, 0, -20))
    R = 24
    for k in range(13):
        th = math.pi * (0.08 + 0.84 * k / 12)
        x, y = R * math.cos(th), 4 + R * math.sin(th)
        w = 1.4 + 1.8 * math.sin(math.pi * k / 12)
        m.cube(arc, f"a{k}", (x - 1.7, y - w / 2, -12.6), (x + 1.7, y + w / 2, -11.4), "white" if 3 < k < 9 else "glow")
        m.cube(arc, f"t{k}", (x * 0.85 - 1.3, y - 3 - w / 3, -12.4), (x * 0.85 + 1.3, y - 3 + w / 3, -11.6), "blood")
    a = m.anim("play", 0.45, "once")
    a.rot("arc", 0, 0, 80, 0)
    a.rot("arc", 0.1, 0, -30, 0, i="linear")
    a.rot("arc", 0.45, 0, -45, 0)
    a.scl("arc", 0, 0.7, 0.7, 1)
    a.scl("arc", 0.1, 1.1, 1.1, 1)
    a.scl("arc", 0.45, 1.3, 0.05, 1)
    return m


HAND = [
    ".F.F.F.F..",
    ".F.F.F.F..",
    ".F.F.F.F..",
    "PPPPPPPP..",
    "PPPPPPPPT.",
    "PPPPPPPPT.",
    "PPPPPPPP..",
    ".PPPPPP...",
]


def build_mark():
    m = fx_model("rh_fx_mark", 502)
    s = m.bone("sigil", (0, 46, 0), m.root)
    px = 1.6
    w = len(HAND[0])
    for ry, row in enumerate(HAND):
        for rx, ch in enumerate(row):
            if ch == ".":
                continue
            x = (rx - w / 2) * px
            y = 46 + (len(HAND) / 2 - ry) * px
            m.cube(s, f"h{ry}_{rx}", (x, y, -0.5), (x + px, y + px, 0.5), "glow" if ch == "F" else "blood")
    for k in range(12):
        th = 2 * math.pi * k / 12
        x, y = 11 * math.cos(th), 46 + 11 * math.sin(th)
        m.cube(s, f"ring{k}", (x - 0.8, y - 0.8, -0.4), (x + 0.8, y + 0.8, 0.4), "crimson")
    a = m.anim("play", 3.0, "once")
    a.scl("sigil", 0, 0.05)
    a.scl("sigil", 0.3, 1.2)
    a.scl("sigil", 0.45, 1)
    for t, sc in ((1.0, 1.08), (1.5, 1), (2.0, 1.08), (2.6, 1)):
        a.scl("sigil", t, sc)
    a.scl("sigil", 3.0, 0.05)
    spin(a, "sigil", 3.0, 1.0)
    return m


def build_shadow():
    m = fx_model("rh_fx_shadow", 503)
    a = m.anim("play", 1.1, "once")
    pts = [(0, 8, 0)] + [(12 * math.cos(2 * math.pi * k / 7), 4 + (k % 2) * 8, 12 * math.sin(2 * math.pi * k / 7))
                         for k in range(7)]
    for k, (x, y, z) in enumerate(pts):
        b = m.bone(f"puff{k}", (x, y, z), m.root)
        s = 4.5 if k == 0 else 3.4
        m.cube(b, f"puff{k}", (x - s, y - s * 0.8, z - s), (x + s, y + s * 0.8, z + s), "smoke" if k % 2 else "black")
        m.cube(b, f"drop{k}", (x - 0.8, y - s * 0.8 - 2, z - 0.8), (x + 0.8, y - s * 0.8, z + 0.8), "blood")
        a.scl(f"puff{k}", 0, 0.05)
        a.scl(f"puff{k}", 0.03 * k + 0.25, 1.5)
        a.scl(f"puff{k}", 0.7, 1.6)
        a.scl(f"puff{k}", 1.1, 0.05)
        a.pos(f"puff{k}", 1.1, 0, 5, 0)
    return m


def build_hand():
    """Mano roja gigante (unos 4 bloques) con la palma hacia el boss que se cierra en un puno."""
    m = fx_model("rh_fx_hand", 504)
    hand = m.bone("hand", (0, 0, 20), m.root)
    m.cube(hand, "wrist", (-8, 0, 16), (8, 14, 24), "blood", decor={"all": "veins"})
    m.cube(hand, "palm", (-11, 14, 15), (11, 34, 25), "blood", decor={"all": "veins"})
    fingers = []
    for i, x in enumerate((-8.5, -3, 2.5, 8)):
        f1 = m.bone(f"finger{i}", (x, 34, 20), hand)
        m.cube(f1, f"finger{i}", (x - 1.9, 34, 17.8), (x + 1.9, 46 + (i in (1, 2)) * 3, 22.2), "blood", decor={"all": "veins"})
        m.cube(f1, f"knuckle{i}", (x - 2.2, 39, 17.4), (x + 2.2, 41, 22.6), "crimson")
        top = 46 + (i in (1, 2)) * 3
        f2 = m.bone(f"finger{i}_tip", (x, top, 20), f1)
        m.cube(f2, f"finger{i}_tip", (x - 1.6, top, 18.2), (x + 1.6, top + 9, 21.8), "blood", decor={"all": "veins"})
        m.cube(f2, f"claw{i}", (x - 1.1, top + 9, 17.6), (x + 1.1, top + 13, 20.8), "glow", rot=("x", -22.5),
               pivot=(x, top + 9, 20))
        fingers.append(i)
    th = m.bone("thumb", (11, 20, 20), hand)
    m.cube(th, "thumb", (11, 18, 17.8), (16, 30, 22.2), "blood", rot=("z", -22.5), pivot=(11, 20, 20),
           decor={"all": "veins"})
    a = m.anim("play", 1.5, "once")
    a.pos("hand", 0, 0, -70, 0)
    a.pos("hand", 0.25, 0, 2, 0)
    a.pos("hand", 0.35, 0, 0, 0)
    a.pos("hand", 1.0, 0, 0, 0)
    a.pos("hand", 1.5, 0, -70, 0)
    for i in fingers:
        a.rot(f"finger{i}", 0, -15, 0, 0)
        a.rot(f"finger{i}", 0.3, -20, 0, 0)
        a.rot(f"finger{i}", 0.5, 85, 0, 0, i="linear")
        a.rot(f"finger{i}_tip", 0, 0, 0, 0)
        a.rot(f"finger{i}_tip", 0.3, 0, 0, 0)
        a.rot(f"finger{i}_tip", 0.5, 90, 0, 0, i="linear")
    a.rot("thumb", 0.3, 0, 0, 0)
    a.rot("thumb", 0.5, 0, 0, 50, i="linear")
    a.scl("hand", 0.45, 1)
    a.scl("hand", 0.5, 1.08)
    a.scl("hand", 0.6, 1)
    return m


def build_nova():
    m = fx_model("rh_fx_nova", 505)
    a = m.anim("play", 1.0, "once")
    n = 22
    for k in range(n):
        th = 2 * math.pi * k / n
        b = m.bone(f"wave{k}", (0, 0, 0), m.root)
        if k % 2:
            m.cube(b, f"w{k}", (-3, 0, -3), (3, 3, 3), "blood")
            m.cube(b, f"wt{k}", (-2, 3, -2), (2, 5, 2), "crimson")
        else:
            m.cube(b, f"s{k}", (-1.8, 0, -1.8), (1.8, 8, 1.8), "crimson")
            m.cube(b, f"st{k}", (-0.9, 8, -0.9), (0.9, 12, 0.9), "glow")
        for t, r, s in ((0, 10, 0.6), (0.18, 80, 2.2), (0.6, 138, 2.6), (1.0, 144, 0.05)):
            a.pos(f"wave{k}", t, -r * math.cos(th), 0, r * math.sin(th), i="linear" if t else "catmullrom")
            a.scl(f"wave{k}", t, s, s * (1 if t < 1.0 else 0.1), s)
    return m


def build_execution():
    m = fx_model("rh_fx_execution", 506)
    a = m.anim("play", 2.8, "once")
    circ = m.bone("circle", (0, 0, 0), m.root)
    for k in range(20):
        th = 2 * math.pi * k / 20
        x, z = 16 * math.cos(th), 16 * math.sin(th)
        m.cube(circ, f"c{k}", (x - 2.2, 0.1, z - 2.2), (x + 2.2, 0.4, z + 2.2), "glow" if k % 2 else "blood")
    for k in range(5):                              # pentagrama de runas
        th = 2 * math.pi * k / 5 - math.pi / 2
        x, z = 9 * math.cos(th), 9 * math.sin(th)
        m.cube(circ, f"r{k}", (x - 1.4, 0.15, z - 1.4), (x + 1.4, 0.5, z + 1.4), "white")
    m.cube(circ, "cross_x", (-14, 0.1, -0.7), (14, 0.35, 0.7), "crimson")
    m.cube(circ, "cross_z", (-0.7, 0.1, -14), (0.7, 0.35, 14), "crimson")
    a.scl("circle", 0, 0.05, 1, 0.05)
    a.scl("circle", 2.0, 7.0, 1, 7.0, i="linear")     # crece hasta 7 bloques durante la carga
    a.scl("circle", 2.2, 7.6, 1, 7.6)
    a.scl("circle", 2.8, 0.05, 1, 0.05)
    spin(a, "circle", 2.8, 0.6)
    pil = m.bone("pillar", (0, 0, 0), m.root)
    m.cube(pil, "pillar", (-5, 0, -5), (5, 48, 5), "blood")
    m.cube(pil, "pillar_core", (-2.5, 0, -2.5), (2.5, 54, 2.5), "glow")
    a.scl("pillar", 0, 0.01)
    a.scl("pillar", 1.95, 0.01)
    a.scl("pillar", 2.1, 2.2, 1.3, 2.2, i="linear")
    a.scl("pillar", 2.4, 1.6, 1.1, 1.6)
    a.scl("pillar", 2.8, 0.05, 1.4, 0.05)
    return m


def build_pillar():
    m = fx_model("rh_fx_pillar", 507)
    a = m.anim("play", 1.3, "once")
    pil = m.bone("pillar", (0, 0, 0), m.root)
    m.cube(pil, "pillar", (-4, 0, -4), (4, 40, 4), "blood")
    m.cube(pil, "pillar_core", (-2, 0, -2), (2, 46, 2), "glow")
    for k in range(6):
        th = 2 * math.pi * k / 6
        x, z = 7 * math.cos(th), 7 * math.sin(th)
        m.cube(pil, f"drop{k}", (x - 1, 6 + k * 5, z - 1), (x + 1, 9 + k * 5, z + 1), "crimson")
    a.scl("pillar", 0, 0.05, 0.05, 0.05)
    a.scl("pillar", 0.2, 1.4, 1.1, 1.4, i="linear")
    a.scl("pillar", 0.8, 1.1, 1.0, 1.1)
    a.scl("pillar", 1.3, 0.05, 1.3, 0.05)
    spin(a, "pillar", 1.3, 1)
    return m


BUILDERS = {"rh_fx_slash": build_slash, "rh_fx_mark": build_mark, "rh_fx_shadow": build_shadow,
            "rh_fx_hand": build_hand, "rh_fx_nova": build_nova, "rh_fx_execution": build_execution,
            "rh_fx_pillar": build_pillar}
SHOTS = {
    "rh_fx_slash": [0.03, 0.1, 0.25, 0.4], "rh_fx_mark": [0.2, 0.6, 1.5, 2.8],
    "rh_fx_shadow": [0.1, 0.3, 0.7, 1.0], "rh_fx_hand": [0.15, 0.3, 0.5, 1.2],
    "rh_fx_nova": [0.05, 0.2, 0.5, 0.9], "rh_fx_execution": [0.5, 1.5, 2.1, 2.5],
    "rh_fx_pillar": [0.1, 0.3, 0.8, 1.2],
}
VIEW = {"rh_fx_slash": (18, 4.0, -30), "rh_fx_mark": (46, 6.0, -20), "rh_fx_shadow": (8, 5.0, -20),
        "rh_fx_hand": (28, 2.8, 160), "rh_fx_nova": (8, 0.95, -20), "rh_fx_execution": (20, 1.1, -20),
        "rh_fx_pillar": (20, 3.5, -20)}


def previews(name, m):
    import render_preview as RP
    RP.G = m
    tw, th = m.pack()
    tex = m.paint(tw, th)
    a = m.ANIMS[0]
    focus, scale, yaw = VIEW[name]
    frames = []
    for t in SHOTS[name]:
        im = RP.render(tex, a, t, yaw=yaw, pitch=20, size=(300, 300), focus=focus, scale=scale)
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
