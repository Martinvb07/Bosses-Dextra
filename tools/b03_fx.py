#!/usr/bin/env python3
"""
Efectos de los ataques de BAAL (modelos de ModelEngine con animacion "play").

  bl_fx_seal    circulo de ofuda (talismanes) que gira y se cierra sobre el objetivo  (Baal_SpiritCurse)
  bl_fx_slash   media luna de luz rosa: el tajo de la nodachi                         (Baal_ShadowStep)
  bl_fx_petals  tormenta de petalos de sakura en espiral, 7 bloques                   (Baal_SakuraHex)
  bl_fx_nova    anillo de llamas de alma que se expande 8 bloques                     (Baal_SpiritNova)
  bl_fx_torii   torii rojo espectral que sale del suelo                               (invocaciones y fases)
  bl_fx_smoke   cupula de humo de sombra                                              (Baal_ShadowVeil)

Uso: python3 tools/b03_fx.py [efecto ...] [--no-preview]
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
from bbmodel import Model  # noqa: E402
import b03_baal as BL  # noqa: E402
from b02_fx import spin  # noqa: E402

BLUEPRINTS = BL.BLUEPRINTS
PREVIEW = BL.PREVIEW / "efectos"

FX_MATS = {
    "paper": ((246, 240, 222), 3), "red": ((196, 30, 44), 6), "purple": ((150, 70, 220), 6),
    "glow": ((255, 176, 232), 3), "pink": ((255, 160, 210), 6), "sakura": ((255, 205, 225), 5),
    "white": ((255, 250, 252), 2), "soul": ((90, 220, 255), 6), "soul_dark": ((40, 120, 200), 6),
    "lacquer": ((30, 24, 34), 4), "gold": ((226, 176, 60), 8), "smoke": ((40, 32, 52), 5),
    "smoke2": ((70, 58, 90), 6),
}


def fx_model(name, seed):
    m = Model(name, FX_MATS, seed=seed, atlas_w=256)
    m.SHINE |= {"gold", "glow", "soul"}
    BL.japan_decor(m)
    return m


def build_seal():
    m = fx_model("bl_fx_seal", 401)
    root = m.root
    ring = m.bone("ring", (0, 0, 0), root)
    for k in range(8):
        th = 2 * math.pi * k / 8
        x, z = 20 * math.cos(th), 20 * math.sin(th)
        m.cube(ring, f"ofuda{k}", (x - 1.6, 4, z - 0.25), (x + 1.6, 13, z + 0.25), "paper", decor={"all": "ofuda"})
    sig = m.bone("sigil", (0, 0, 0), root)
    for k in range(16):
        th = 2 * math.pi * k / 16
        x, z = 16 * math.cos(th), 16 * math.sin(th)
        m.cube(sig, f"sig{k}", (x - 2, 0.1, z - 2), (x + 2, 0.4, z + 2), "purple" if k % 2 else "glow")
    m.cube(sig, "sig_x", (-14, 0.1, -0.8), (14, 0.4, 0.8), "purple")
    m.cube(sig, "sig_z", (-0.8, 0.1, -14), (0.8, 0.4, 14), "purple")
    m.cube(sig, "sig_d1", (-12, 0.1, -0.8), (12, 0.4, 0.8), "glow", rot=("y", 45), pivot=(0, 0, 0))
    m.cube(sig, "sig_d2", (-12, 0.1, -0.8), (12, 0.4, 0.8), "glow", rot=("y", -45), pivot=(0, 0, 0))
    a = m.anim("play", 1.1, "once")
    spin(a, "ring", 1.1, 1.2)
    a.scl("ring", 0, 1.6, 0.05, 1.6)
    a.scl("ring", 0.2, 1.3, 1, 1.3)
    a.scl("ring", 0.4, 0.4, 1.2, 0.4, i="linear")
    a.scl("ring", 0.55, 1.8, 0.3, 1.8)
    a.scl("ring", 1.1, 2.2, 0.02, 2.2)
    for t, y in ((0, 0), (0.4, 6), (1.1, 10)):
        a.pos("ring", t, 0, y, 0)
    a.scl("sigil", 0, 0.05)
    a.scl("sigil", 0.25, 1.1)
    a.scl("sigil", 0.4, 1)
    a.scl("sigil", 0.8, 1.3)
    a.scl("sigil", 1.1, 0.05)
    spin(a, "sigil", 1.1, -0.5)
    return m


def build_slash():
    m = fx_model("bl_fx_slash", 402)
    root = m.root
    arc = m.bone("arc", (0, 18, -12), root, rotation=(0, 0, 35))
    R = 26
    for k in range(15):
        th = math.pi * (0.05 + 0.9 * k / 14)
        x, y = R * math.cos(th), 18 + R * math.sin(th) - 14
        w = 1.6 + 1.6 * math.sin(math.pi * k / 14)
        m.cube(arc, f"a{k}", (x - 1.8, y - w / 2, -12.6), (x + 1.8, y + w / 2, -11.4), "white" if 4 < k < 10 else "pink")
        m.cube(arc, f"t{k}", (x * 0.86 - 1.4, y - 3 - w / 3, -12.4), (x * 0.86 + 1.4, y - 3 + w / 3, -11.6), "glow")
    a = m.anim("play", 0.6, "once")
    a.rot("arc", 0, 0, 0, -70)
    a.rot("arc", 0.12, 0, 0, 25, i="linear")
    a.rot("arc", 0.6, 0, 0, 40)
    a.scl("arc", 0, 0.6, 0.6, 1)
    a.scl("arc", 0.12, 1.1, 1.1, 1)
    a.scl("arc", 0.35, 1.2, 1.2, 1)
    a.scl("arc", 0.6, 1.4, 0.05, 1)
    return m


def build_petals():
    m = fx_model("bl_fx_petals", 403)
    root = m.root
    a = m.anim("play", 1.6, "once")
    n = 26
    for k in range(n):
        b = m.bone(f"petal{k}", (0, 0, 0), root)
        mat = ("pink", "sakura", "white")[k % 3]
        m.cube(b, f"p{k}", (-1.6, -0.3, -1.1), (1.6, 0.3, 1.1), mat)
        m.cube(b, f"q{k}", (-1.1, -0.3, -1.6), (1.1, 0.3, 1.6), mat)
        th0 = 2 * math.pi * k / n
        h = 6 + (k % 4) * 7
        steps = 8
        for i in range(steps + 1):
            t = 1.6 * i / steps
            r = 8 + 104 * (i / steps) ** 0.8                      # espiral hasta 7 bloques
            th = th0 + 2.2 * i / steps
            y = h * math.sin(math.pi * min(1, i / steps * 1.2))
            a.pos(f"petal{k}", t, -r * math.cos(th), y, r * math.sin(th), i="linear")
            a.rot(f"petal{k}", t, 70 * i * ((k % 2) * 2 - 1), 90 * i, 0, i="linear")
            sc = 1.6 + 2.6 * (i / steps) if i < steps else 0.05
            a.scl(f"petal{k}", t, sc, i="linear")
    return m


def build_nova():
    m = fx_model("bl_fx_nova", 404)
    root = m.root
    a = m.anim("play", 1.1, "once")
    n = 14
    for k in range(n):
        th = 2 * math.pi * k / n
        b = m.bone(f"flame{k}", (0, 0, 0), root)
        h = 10 + (k % 3) * 4
        m.cube(b, f"f{k}_base", (-2.2, 0, -2.2), (2.2, h * 0.5, 2.2), "soul_dark")
        m.cube(b, f"f{k}_mid", (-1.5, h * 0.5, -1.5), (1.5, h * 0.85, 1.5), "soul")
        m.cube(b, f"f{k}_tip", (-0.7, h * 0.85, -0.7), (0.7, h * 1.1, 0.7), "white")
        for t, r, s in ((0, 10, 0.6), (0.2, 70, 2.2), (0.6, 124, 2.6), (1.1, 132, 0.05)):
            a.pos(f"flame{k}", t, -r * math.cos(th), 0, r * math.sin(th), i="linear" if t else "catmullrom")
            a.scl(f"flame{k}", t, s, s * (1.0 if t < 1.1 else 0.1), s)
    core = m.bone("core", (0, 0, 0), root)
    m.cube(core, "pillar", (-3, 0, -3), (3, 40, 3), "soul")
    m.cube(core, "pillar_in", (-1.5, 0, -1.5), (1.5, 44, 1.5), "white")
    a.scl("core", 0, 0.2, 0.05, 0.2)
    a.scl("core", 0.15, 1.3, 1.0, 1.3)
    a.scl("core", 0.5, 0.6, 1.2, 0.6)
    a.scl("core", 1.1, 0.05, 1.5, 0.05)
    return m


def build_torii():
    m = fx_model("bl_fx_torii", 405)
    root = m.root
    g = m.bone("gate", (0, 0, 24), root)
    for sx in (1, -1):
        m.cube(g, f"hashira{sx}", (13 * sx - 1.6, 0, 22.4), (13 * sx + 1.6, 38, 25.6), "red")
        m.cube(g, f"base{sx}", (13 * sx - 2.2, 0, 21.8), (13 * sx + 2.2, 3, 26.2), "lacquer")
    m.cube(g, "nuki", (-17, 29, 23.2), (17, 31.5, 24.8), "red")
    m.cube(g, "kasagi", (-20, 36, 22.6), (20, 38.5, 25.4), "lacquer")
    m.cube(g, "shimaki", (-19, 34, 22.8), (19, 36, 25.2), "red")
    m.cube_lr(g, g, "kasagi_end", (17, 37, 22.6), (22, 39.5, 25.4), "lacquer", rot=("z", 22.5), pivot=(17, 38, 24))
    m.cube(g, "gakuzuka", (-1.4, 31.5, 23.4), (1.4, 34, 24.6), "red")
    m.cube(g, "gaku", (-2.2, 30.4, 22.9), (2.2, 34.6, 23.4), "gold", decor={"north": "sakura"})
    m.cube(g, "shimenawa", (-10, 26, 23.6), (10, 27.4, 24.4), "paper")
    for x in (-6, 0, 6):
        m.cube(g, f"shide{x}", (x - 0.8, 22, 23.8), (x + 0.8, 26, 24.2), "paper")
    a = m.anim("play", 2.2, "once")
    a.pos("gate", 0, 0, -40, 0)
    a.pos("gate", 0.6, 0, 1, 0)
    a.pos("gate", 0.75, 0, 0, 0)
    a.pos("gate", 1.7, 0, 0, 0)
    a.pos("gate", 2.2, 0, -40, 0)
    return m


def build_smoke():
    m = fx_model("bl_fx_smoke", 406)
    root = m.root
    a = m.anim("play", 1.4, "once")
    pts = [(0, 6, 0)] + [(16 * math.cos(2 * math.pi * k / 8), 4 + (k % 2) * 6, 16 * math.sin(2 * math.pi * k / 8))
                         for k in range(8)] + [(0, 20, 0)]
    for k, (x, y, z) in enumerate(pts):
        b = m.bone(f"puff{k}", (x, y, z), root)
        s = 5 if k in (0, len(pts) - 1) else 4
        m.cube(b, f"puff{k}", (x - s, y - s * 0.8, z - s), (x + s, y + s * 0.8, z + s), "smoke" if k % 2 else "smoke2")
        m.cube(b, f"puff{k}b", (x - s * 0.6, y + s * 0.4, z - s * 0.6), (x + s * 0.6, y + s * 1.2, z + s * 0.6), "smoke2")
        d = 0.04 * k
        a.scl(f"puff{k}", 0, 0.05)
        a.scl(f"puff{k}", d + 0.3, 1.4)
        a.scl(f"puff{k}", 0.9, 1.6)
        a.scl(f"puff{k}", 1.4, 0.05)
        a.pos(f"puff{k}", 1.4, 0, 6, 0)
    return m


BUILDERS = {"bl_fx_seal": build_seal, "bl_fx_slash": build_slash, "bl_fx_petals": build_petals,
            "bl_fx_nova": build_nova, "bl_fx_torii": build_torii, "bl_fx_smoke": build_smoke}
SHOTS = {
    "bl_fx_seal": [0.1, 0.3, 0.45, 0.8], "bl_fx_slash": [0.05, 0.12, 0.3, 0.5],
    "bl_fx_petals": [0.1, 0.4, 0.9, 1.4], "bl_fx_nova": [0.1, 0.2, 0.5, 0.9],
    "bl_fx_torii": [0.3, 0.75, 1.5, 2.0], "bl_fx_smoke": [0.15, 0.4, 0.9, 1.2],
}
VIEW = {"bl_fx_seal": (6, 5.0, -20), "bl_fx_slash": (14, 4.0, -30), "bl_fx_petals": (10, 1.1, -20),
        "bl_fx_nova": (8, 1.0, -20), "bl_fx_torii": (20, 4.0, 160), "bl_fx_smoke": (10, 4.0, -20)}


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
