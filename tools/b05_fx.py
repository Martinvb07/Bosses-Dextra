#!/usr/bin/env python3
"""
Efectos de los ataques de RAGNAROK (modelos de ModelEngine con animacion "play").

  rg_fx_shatter  racimo de cristales de hielo que brota delante y estalla  (HeavyStrike, DevastatingBlow)
  rg_fx_burst    anillo de pinchos de hielo que se expande 7 bloques       (Ragnarok_FreezeBurst)
  rg_fx_icefall  lluvia de carambanos gigantes en 9 bloques                (Ragnarok_IceStorm)
  rg_fx_runes    circulo de piedras runicas que se alzan, con un rayo      (LightningStorm, invocaciones, fases)
  rg_fx_end      cupula de hielo que crece 2 s y revienta a 12 bloques     (Ragnarok_RunOrDie)

Uso: python3 tools/b05_fx.py [efecto ...] [--no-preview]
"""
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
from bbmodel import Model  # noqa: E402
import b05_ragnarok as RG  # noqa: E402
from b02_fx import spin  # noqa: E402

BLUEPRINTS = RG.BLUEPRINTS
PREVIEW = RG.PREVIEW / "efectos"

FX_MATS = {
    "ice": ((176, 226, 255), 5), "ice_dark": ((84, 146, 210), 6), "glow": ((150, 240, 255), 3),
    "white": ((240, 250, 255), 2), "frost": ((210, 236, 250), 4), "stone": ((96, 100, 108), 8),
    "bolt": ((230, 245, 255), 2),
}


def fx_model(name, seed):
    m = Model(name, FX_MATS, seed=seed, atlas_w=256)
    m.SHINE |= {"ice", "glow", "bolt"}
    RG.norse_decor(m)
    return m


def crystal(m, bone, name, x, y, z, h, w, rot=None):
    m.cube(bone, name, (x - w, y, z - w), (x + w, y + h, z + w), "ice", rot=rot, pivot=(x, y, z), decor={"all": "crystal"})
    m.cube(bone, name + "_tip", (x - w * 0.5, y + h, z - w * 0.5), (x + w * 0.5, y + h + w * 1.8, z + w * 0.5), "glow",
           rot=rot, pivot=(x, y, z))


def build_shatter():
    m = fx_model("rg_fx_shatter", 601)
    a = m.anim("play", 1.0, "once")
    spec = [(0, -26, 16, 3.0, None), (-7, -22, 11, 2.4, ("z", 22.5)), (7, -22, 12, 2.4, ("z", -22.5)),
            (-4, -32, 9, 2.0, ("x", -22.5)), (5, -31, 10, 2.0, ("x", -22.5)), (0, -17, 7, 1.8, ("x", 22.5))]
    for k, (x, z, h, w, rot) in enumerate(spec):
        b = m.bone(f"c{k}", (x, 0, z), m.root)
        crystal(m, b, f"c{k}", x, 0, z, h, w, rot)
        a.scl(f"c{k}", 0, 0.05)
        a.scl(f"c{k}", 0.12 + 0.02 * k, 1.15)
        a.scl(f"c{k}", 0.25, 1)
        a.scl(f"c{k}", 0.65, 1)
        a.scl(f"c{k}", 1.0, 0.05)
        ang = math.atan2(z + 20, x if x else 0.01)
        a.pos(f"c{k}", 0.65, 0, 0, 0)
        a.pos(f"c{k}", 1.0, -10 * math.cos(ang), 6, 10 * math.sin(ang))
    return m


def build_burst():
    m = fx_model("rg_fx_burst", 602)
    a = m.anim("play", 1.0, "once")
    n = 18
    for k in range(n):
        th = 2 * math.pi * k / n
        b = m.bone(f"s{k}", (0, 0, 0), m.root)
        crystal(m, b, f"s{k}", 0, 0, 0, 7 + (k % 3) * 2, 1.6, ("x", -22.5) if k % 2 else None)
        for t, r, s in ((0, 8, 0.4), (0.15, 70, 1.8), (0.55, 108, 2.2), (1.0, 112, 0.05)):
            a.pos(f"s{k}", t, -r * math.cos(th), 0, r * math.sin(th), i="linear" if t else "catmullrom")
            a.scl(f"s{k}", t, s)
        a.rot(f"s{k}", 0, 0, -math.degrees(th) - 90, 0)
    return m


def build_icefall():
    m = fx_model("rg_fx_icefall", 603)
    rng = random.Random(9)
    a = m.anim("play", 1.6, "once")
    for k in range(16):
        r = 20 + rng.uniform(0, 120)
        th = rng.uniform(0, 2 * math.pi)
        x, z = r * math.cos(th), r * math.sin(th)
        b = m.bone(f"ic{k}", (x, 0, z), m.root)
        h = rng.uniform(10, 16)
        m.cube(b, f"ic{k}", (x - 3.0, 4.5, z - 3.0), (x + 3.0, 4.5 + h * 1.6, z + 3.0), "ice", decor={"all": "crystal"})
        m.cube(b, f"ic{k}_mid", (x - 2.0, 1.8, z - 2.0), (x + 2.0, 4.5, z + 2.0), "ice_dark")
        m.cube(b, f"ic{k}_tip", (x - 1.0, 0, z - 1.0), (x + 1.0, 1.8, z + 1.0), "glow")
        d = rng.uniform(0, 0.5)
        a.pos(f"ic{k}", 0, 0, 120, 0)
        a.pos(f"ic{k}", d, 0, 120, 0)
        a.pos(f"ic{k}", d + 0.35, 0, -2, 0, i="linear")
        a.pos(f"ic{k}", 1.6, 0, -3, 0)
        a.scl(f"ic{k}", d + 0.35, 1)
        a.scl(f"ic{k}", d + 0.45, 1.6, 0.4, 1.6)
        a.scl(f"ic{k}", 1.6, 0.05)
    cloud = m.bone("cloud", (0, 120, 0), m.root)
    for k in range(10):
        th = 2 * math.pi * k / 10
        x, z = 60 * math.cos(th), 60 * math.sin(th)
        m.cube(cloud, f"cl{k}", (x - 12, 120, z - 12), (x + 12, 125, z + 12), "frost")
        m.cube(cloud, f"cl{k}b", (x - 7, 125, z - 7), (x + 7, 128, z + 7), "white")
    spin(a, "cloud", 1.6, 0.4)
    a.scl("cloud", 0, 0.05, 1, 0.05)
    a.scl("cloud", 0.3, 1)
    a.scl("cloud", 1.3, 1)
    a.scl("cloud", 1.6, 0.05, 1, 0.05)
    return m


RUNES = ["1.1|111|.1.", "11.|1.1|11.", "111|.1.|.1.", "1..|11.|1.1", "1.1|.1.|1.1", ".1.|111|.1."]


def build_runes():
    m = fx_model("rg_fx_runes", 604)
    a = m.anim("play", 1.8, "once")
    for k in range(8):
        th = 2 * math.pi * k / 8
        x, z = 40 * math.cos(th), 40 * math.sin(th)
        b = m.bone(f"stone{k}", (x, 0, z), m.root, rotation=(0, -math.degrees(th) - 90, 0))
        m.cube(b, f"stone{k}", (x - 3, 0, z - 1.5), (x + 3, 13, z + 1.5), "stone")
        rows = RUNES[k % len(RUNES)].split("|")
        for ry, row in enumerate(rows):
            for rx, ch in enumerate(row):
                if ch == "1":
                    m.cube(b, f"r{k}_{ry}_{rx}", (x - 1.8 + rx * 1.2, 9 - ry * 1.6, z - 1.7), (x - 0.8 + rx * 1.2, 10.2 - ry * 1.6, z - 1.4),
                           "glow")
        a.pos(f"stone{k}", 0, 0, -16, 0)
        a.pos(f"stone{k}", 0.25 + 0.03 * k, 0, 1, 0)
        a.pos(f"stone{k}", 0.4 + 0.03 * k, 0, 0, 0)
        a.pos(f"stone{k}", 1.4, 0, 0, 0)
        a.pos(f"stone{k}", 1.8, 0, -16, 0)
    ring = m.bone("ring", (0, 0, 0), m.root)
    for k in range(24):
        th = 2 * math.pi * k / 24
        m.cube(ring, f"g{k}", (40 * math.cos(th) - 1.6, 0.1, 40 * math.sin(th) - 1.6),
               (40 * math.cos(th) + 1.6, 0.4, 40 * math.sin(th) + 1.6), "glow")
    a.scl("ring", 0, 0.05, 1, 0.05)
    a.scl("ring", 0.3, 1)
    a.scl("ring", 1.5, 1)
    a.scl("ring", 1.8, 0.05, 1, 0.05)
    spin(a, "ring", 1.8, 0.3)
    bolt = m.bone("bolt", (0, 0, 0), m.root)
    x = 0
    for k in range(8):
        dx = 3 if k % 2 else -3
        m.cube(bolt, f"b{k}", (min(x, x + dx) - 1, 90 - (k + 1) * 11, -1), (max(x, x + dx) + 1, 90 - k * 11, 1), "bolt")
        x += dx
    for t, s in ((0, 0.01), (0.5, 0.01), (0.55, 1.2), (0.65, 0.9), (0.75, 1.2), (0.9, 0.01), (1.8, 0.01)):
        a.scl("bolt", t, s, 1, s, i="linear")
    return m


def build_end():
    m = fx_model("rg_fx_end", 605)
    a = m.anim("play", 2.8, "once")
    n = 16
    for k in range(n):
        th = 2 * math.pi * k / n
        b = m.bone(f"d{k}", (0, 0, 0), m.root)
        R = 40
        x, z = R * math.cos(th), R * math.sin(th)
        tilt = ("x", -22.5) if k % 2 else ("z", 22.5)
        crystal(m, b, f"d{k}", x, 0, z, 18 + (k % 3) * 6, 3.0, tilt)
        a.scl(f"d{k}", 0, 0.05)
        a.scl(f"d{k}", 2.0, 1.0, i="linear")                      # crece durante la carga
        a.scl(f"d{k}", 2.1, 1.2)
        a.pos(f"d{k}", 2.0, 0, 0, 0)
        a.pos(f"d{k}", 2.8, -150 * math.cos(th), 20, 150 * math.sin(th), i="linear")   # sale disparado a 12 bloques
        a.scl(f"d{k}", 2.8, 0.2)
    core = m.bone("core", (0, 0, 0), m.root)
    crystal(m, core, "core", 0, 0, 0, 40, 5.0)
    a.scl("core", 0, 0.05)
    a.scl("core", 1.95, 0.05)
    a.scl("core", 2.1, 1.5, 1.2, 1.5)
    a.scl("core", 2.8, 0.05, 1.6, 0.05)
    return m


BUILDERS = {"rg_fx_shatter": build_shatter, "rg_fx_burst": build_burst, "rg_fx_icefall": build_icefall,
            "rg_fx_runes": build_runes, "rg_fx_end": build_end}
SHOTS = {
    "rg_fx_shatter": [0.08, 0.2, 0.6, 0.9], "rg_fx_burst": [0.05, 0.2, 0.5, 0.9],
    "rg_fx_icefall": [0.2, 0.45, 0.7, 1.2], "rg_fx_runes": [0.2, 0.45, 0.6, 1.2], "rg_fx_end": [0.6, 1.6, 2.1, 2.5],
}
VIEW = {"rg_fx_shatter": (8, 4.0, -150), "rg_fx_burst": (8, 1.1, -20), "rg_fx_icefall": (50, 0.9, -20),
        "rg_fx_runes": (30, 2.0, -20), "rg_fx_end": (20, 0.95, -20)}


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
