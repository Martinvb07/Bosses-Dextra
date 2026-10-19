#!/usr/bin/env python3
"""
Efectos de los ataques de MUSHLORD (modelos de ModelEngine con animacion "play").

  ms_fx_swipe     zarpazo verde con gotas toxicas                      (Mushlord_ToxicSwipe)
  ms_fx_bolt      bomba de esporas que cae sobre el objetivo y revienta (Mushlord_SporeBolt)
  ms_fx_bloom     anillo de setas que brotan del suelo                 (SporeBurst, FungalBloom, invocaciones)
  ms_fx_nova      ola de esporas verde que se expande 8 bloques        (Mushlord_MycotoxinNova, ToxicCloud)
  ms_fx_roots     raices que salen del suelo y se cierran              (Mushlord_PlagueSurge)
  ms_fx_sentence  circulo de setas que crece y estalla en una seta gigante (Mushlord_GardenSentence)
  ms_fx_eruption  hongo nuclear toxico                                 (CorruptionEruption, PlagueApocalypse)
  ms_fx_cocoon    capullo de micelio que envuelve al boss y revienta   (Mushlord_TransitionCocoon)

Uso: python3 tools/b06_fx.py [efecto ...] [--no-preview]
"""
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
from bbmodel import Model  # noqa: E402
import b06_mushlord as MS  # noqa: E402
from b02_fx import spin  # noqa: E402

BLUEPRINTS = MS.BLUEPRINTS
PREVIEW = MS.PREVIEW / "efectos"

FX_MATS = {k: v for k, v in MS.MATS.items()}
FX_MATS.update({"spore": ((170, 230, 120), 6), "toxic_dark": ((40, 96, 36), 6)})


def fx_model(name, seed, px=2, atlas=256):
    m = Model(name, FX_MATS, seed=seed, atlas_w=atlas, px=px)
    m.SHINE |= {"glow", "cap", "slime"}
    MS.fungal_decor(m)
    return m


def build_swipe():
    m = fx_model("ms_fx_swipe", 701)
    arc = m.bone("arc", (0, 16, -10), m.root, rotation=(0, 0, 25))
    R = 18
    for k in range(11):
        th = math.pi * (0.1 + 0.8 * k / 10)
        x, y = R * math.cos(th), 2 + R * math.sin(th)
        w = 1.2 + 1.6 * math.sin(math.pi * k / 10)
        m.cube(arc, f"a{k}", (x - 1.5, y - w / 2, -10.6), (x + 1.5, y + w / 2, -9.4), "glow" if 3 < k < 8 else "slime")
        m.cube(arc, f"d{k}", (x * 0.9 - 0.5, y - 2 - w, -10.3), (x * 0.9 + 0.5, y - w / 2, -9.7), "toxic")
    a = m.anim("play", 0.5, "once")
    a.rot("arc", 0, 0, -70, 0)
    a.rot("arc", 0.12, 0, 40, 0, i="linear")
    a.rot("arc", 0.5, 0, 55, 0)
    a.scl("arc", 0, 0.7, 0.7, 1)
    a.scl("arc", 0.12, 1.1, 1.1, 1)
    a.scl("arc", 0.5, 1.3, 0.05, 1)
    return m


def build_bolt():
    m = fx_model("ms_fx_bolt", 702)
    a = m.anim("play", 1.1, "once")
    orb = m.bone("orb", (0, 40, 0), m.root)
    m.cube(orb, "orb", (-3.5, 36.5, -3.5), (3.5, 43.5, 3.5), "glow", decor={"all": "puff"})
    m.cube(orb, "orb_w", (-4.4, 37.6, -2.4), (4.4, 42.4, 2.4), "slime", decor={"all": "puff"})
    m.cube(orb, "orb_d", (-2.4, 37.6, -4.4), (2.4, 42.4, 4.4), "slime", decor={"all": "puff"})
    a.pos("orb", 0, 0, 30, 0)
    a.pos("orb", 0.4, 0, -36, 0, i="linear")
    a.scl("orb", 0, 0.5)
    a.scl("orb", 0.4, 1)
    a.scl("orb", 0.45, 1.6, 0.4, 1.6)
    a.scl("orb", 0.55, 0.05)
    for k in range(10):
        th = 2 * math.pi * k / 10
        b = m.bone(f"puff{k}", (0, 3, 0), m.root)
        m.cube(b, f"p{k}", (-3, 0, -3), (3, 4, 3), "spore" if k % 2 else "fog", decor={"all": "puff"})
        a.scl(f"puff{k}", 0, 0.01)
        a.scl(f"puff{k}", 0.42, 0.01)
        a.scl(f"puff{k}", 0.6, 1.6)
        a.scl(f"puff{k}", 1.1, 0.05)
        a.pos(f"puff{k}", 0.42, 0, 0, 0)
        a.pos(f"puff{k}", 1.1, -40 * math.cos(th), 8, 40 * math.sin(th))
    return m


def build_bloom():
    m = fx_model("ms_fx_bloom", 703)
    a = m.anim("play", 1.4, "once")
    rng = random.Random(5)
    for k in range(12):
        th = 2 * math.pi * k / 12
        r = 40 + (k % 2) * 40
        x, z = r * math.cos(th), r * math.sin(th)
        b = m.bone(f"s{k}", (x, 0, z), m.root)
        MS.shroom(m, b, f"s{k}", x, 0, z, rng.uniform(6, 11), rng.uniform(4, 6.5),
                  mat="cap" if k % 2 else "red_cap", spots="spots" if k % 2 else "white_spots")
        d = 0.04 * k
        a.scl(f"s{k}", 0, 0.05)
        a.scl(f"s{k}", d + 0.18, 1.25)
        a.scl(f"s{k}", d + 0.3, 1)
        a.scl(f"s{k}", 1.0, 1)
        a.scl(f"s{k}", 1.4, 0.05)
    return m


def build_nova():
    m = fx_model("ms_fx_nova", 704)
    a = m.anim("play", 1.1, "once")
    n = 20
    for k in range(n):
        th = 2 * math.pi * k / n
        b = m.bone(f"w{k}", (0, 0, 0), m.root)
        m.cube(b, f"w{k}", (-3, 0, -3), (3, 4, 3), "spore" if k % 2 else "fog", decor={"all": "puff"})
        m.cube(b, f"w{k}t", (-2, 4, -2), (2, 6.5, 2), "glow")
        for t, r, s in ((0, 10, 0.5), (0.2, 70, 2.0), (0.6, 124, 2.6), (1.1, 128, 0.05)):
            a.pos(f"w{k}", t, -r * math.cos(th), 0, r * math.sin(th), i="linear" if t else "catmullrom")
            a.scl(f"w{k}", t, s, s * (1 if t < 1.1 else 0.1), s)
    return m


def build_roots():
    m = fx_model("ms_fx_roots", 705)
    a = m.anim("play", 1.4, "once")
    for k in range(10):
        th = 2 * math.pi * k / 10
        r = 64 + (k % 2) * 30
        x, z = r * math.cos(th), r * math.sin(th)
        b = m.bone(f"r{k}", (x, 0, z), m.root, rotation=(0, -math.degrees(th) + 90, 0))
        m.cube(b, f"r{k}a", (x - 2.2, 0, z - 2.2), (x + 2.2, 14, z + 2.2), "bark", decor={"all": "bark"})
        tip = m.bone(f"r{k}_tip", (x, 14, z), b)
        m.cube(tip, f"r{k}b", (x - 1.6, 14, z - 1.6), (x + 1.6, 24, z + 1.6), "bark", decor={"all": "bark"})
        m.cube(tip, f"r{k}c", (x - 0.9, 24, z - 0.9), (x + 0.9, 29, z + 0.9), "glow")
        a.pos(f"r{k}", 0, 0, -30, 0)
        a.pos(f"r{k}", 0.2, 0, 2, 0)
        a.pos(f"r{k}", 0.3, 0, 0, 0)
        a.pos(f"r{k}", 1.0, 0, 0, 0)
        a.pos(f"r{k}", 1.4, 0, -30, 0)
        a.rot(f"r{k}_tip", 0.3, 0, 0, 0)
        a.rot(f"r{k}_tip", 0.5, 70, 0, 0, i="linear")           # se cierran hacia el centro
        a.rot(f"r{k}_tip", 1.0, 70, 0, 0)
    return m


def build_sentence():
    m = fx_model("ms_fx_sentence", 706)
    a = m.anim("play", 1.9, "once")
    ring = m.bone("ring", (0, 0, 0), m.root)
    for k in range(12):
        th = 2 * math.pi * k / 12
        x, z = 64 * math.cos(th), 64 * math.sin(th)
        MS.shroom(m, ring, f"rs{k}", x, 0, z, 3.0, 2.2, mat="cap" if k % 2 else "red_cap",
                  spots="spots" if k % 2 else "white_spots")
    for k in range(24):
        th = 2 * math.pi * k / 24
        m.cube(ring, f"g{k}", (64 * math.cos(th) - 1.5, 0.1, 64 * math.sin(th) - 1.5),
               (64 * math.cos(th) + 1.5, 0.4, 64 * math.sin(th) + 1.5), "glow")
    a.scl("ring", 0, 0.05, 1, 0.05)
    a.scl("ring", 0.4, 1)
    a.scl("ring", 1.5, 1)
    a.scl("ring", 1.9, 0.05, 1, 0.05)
    spin(a, "ring", 1.9, 0.4)
    big = m.bone("big", (0, 0, 0), m.root)
    MS.shroom(m, big, "giant", 0, 0, 0, 30, 20, mat="cap")
    a.scl("big", 0, 0.01)
    a.scl("big", 1.15, 0.01)
    a.scl("big", 1.25, 1.2, i="linear")
    a.scl("big", 1.4, 1)
    a.scl("big", 1.6, 1)
    a.scl("big", 1.9, 0.05)
    return m


def build_eruption():
    m = fx_model("ms_fx_eruption", 707, px=1, atlas=512)
    a = m.anim("play", 1.8, "once")
    stem = m.bone("stem", (0, 0, 0), m.root)
    m.cube(stem, "stem", (-8, 0, -8), (8, 50, 8), "fog", decor={"all": "puff"})
    m.cube(stem, "stem_core", (-4, 0, -4), (4, 54, 4), "glow")
    cap = m.bone("cap", (0, 50, 0), m.root)
    for k, (r, y0, y1, mat) in enumerate(((32, 48, 58, "toxic"), (26, 58, 66, "spore"), (17, 66, 73, "fog"), (9, 73, 77, "glow"))):
        for j, rot in enumerate((None, ("y", 45))):
            m.cube(cap, f"cap{k}_{j}", (-r, y0, -r), (r, y1, r), mat, rot=rot, pivot=(0, y0, 0), decor={"all": "puff"})
    base = m.bone("base", (0, 0, 0), m.root)
    for j, rot in enumerate((None, ("y", 45))):
        m.cube(base, f"base{j}", (-34, 0, -34), (34, 6, 34), "toxic", rot=rot, pivot=(0, 0, 0), decor={"all": "puff"})
        m.cube(base, f"base_top{j}", (-22, 6, -22), (22, 11, 22), "spore", rot=rot, pivot=(0, 6, 0), decor={"all": "puff"})
    for b in ("stem", "cap", "base"):
        a.scl(b, 0, 0.05)
    a.scl("stem", 0.3, 1, 1.1, 1)
    a.pos("cap", 0, 0, -48, 0)
    a.pos("cap", 0.4, 0, 0, 0)
    a.scl("cap", 0.4, 1.2)
    a.scl("cap", 1.2, 1.5)
    a.scl("base", 0.3, 1.6, 1, 1.6)
    a.scl("base", 1.2, 2.2, 1, 2.2)
    for b in ("stem", "cap", "base"):
        a.scl(b, 1.8, 0.05)
    spin(a, "cap", 1.8, 0.25)
    return m


def build_cocoon():
    m = fx_model("ms_fx_cocoon", 708)
    a = m.anim("play", 1.2, "once")
    for k in range(8):
        th = 2 * math.pi * k / 8
        x, z = 22 * math.cos(th), 22 * math.sin(th)
        b = m.bone(f"shell{k}", (x, 0, z), m.root, rotation=(0, -math.degrees(th) + 90, 0))
        m.cube(b, f"shell{k}", (x - 6, 0, z - 1.5), (x + 6, 60, z + 1.5), "myc", decor={"all": "mossy"})
        m.cube(b, f"vein{k}", (x - 0.8, 4, z - 1.8), (x + 0.8, 56, z - 1.4), "glow")
        a.rot(f"shell{k}", 0, -60, 0, 0)
        a.rot(f"shell{k}", 0.4, -18, 0, 0)
        a.rot(f"shell{k}", 0.6, -18, 0, 0)
        a.rot(f"shell{k}", 0.75, -80, 0, 0, i="linear")       # revienta hacia fuera
        a.scl(f"shell{k}", 0, 0.05)
        a.scl(f"shell{k}", 0.4, 1)
        a.scl(f"shell{k}", 0.9, 1)
        a.scl(f"shell{k}", 1.2, 0.05)
    return m


BUILDERS = {"ms_fx_swipe": build_swipe, "ms_fx_bolt": build_bolt, "ms_fx_bloom": build_bloom, "ms_fx_nova": build_nova,
            "ms_fx_roots": build_roots, "ms_fx_sentence": build_sentence, "ms_fx_eruption": build_eruption,
            "ms_fx_cocoon": build_cocoon}
SHOTS = {
    "ms_fx_swipe": [0.05, 0.12, 0.3, 0.45], "ms_fx_bolt": [0.15, 0.4, 0.6, 0.9], "ms_fx_bloom": [0.1, 0.3, 0.8, 1.3],
    "ms_fx_nova": [0.05, 0.2, 0.5, 0.9], "ms_fx_roots": [0.15, 0.3, 0.5, 1.2], "ms_fx_sentence": [0.4, 1.0, 1.3, 1.6],
    "ms_fx_eruption": [0.2, 0.5, 1.0, 1.6], "ms_fx_cocoon": [0.2, 0.5, 0.75, 1.0],
}
VIEW = {"ms_fx_swipe": (16, 5.0, -30), "ms_fx_bolt": (20, 4.0, -20), "ms_fx_bloom": (10, 1.8, -20),
        "ms_fx_nova": (8, 1.0, -20), "ms_fx_roots": (14, 1.5, -20), "ms_fx_sentence": (20, 1.6, -20),
        "ms_fx_eruption": (50, 1.2, -20), "ms_fx_cocoon": (30, 2.4, -20)}


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
