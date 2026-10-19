#!/usr/bin/env python3
"""
Efectos de los ataques de KUKULKAN (modelos de ModelEngine con animacion "play").

  kk_fx_screech   ondas doradas del chillido de la serpiente (7 bloques)   (KK_Wail, KK_EchoOfGrief)
  kk_fx_eclipse   sol negro y sombra del eclipse (4 bloques)               (KK_ShroudOfNight)
  kk_fx_siphon    plumas que suben en espiral desde el jugador             (KK_SpiritSiphon)
  kk_fx_altar     piedra del sol bajo el elegido que estalla a los 1.2 s   (KK_GriefMark)
  kk_fx_venom     anillo de colmillos de jade a los 0.5 s (5 bloques)      (KK_SharedSorrow)
  kk_fx_solar     columna de luz del eclipse y ola a los 0.6 s (12 bl.)    (KK_MassLament)
  kk_fx_sunrays   rayos de sol que caen a los 0.5 y 1.0 s (10 bloques)     (KK_StormOfSorrow)
  kk_fx_serpents  serpientes emplumadas que salen del suelo                (KK_ShadowHunt, invocaciones)
  kk_fx_pyramid   escalones de piramide que suben y disco solar            (fases e intro)

Uso: python3 tools/b16_fx.py [efecto ...] [--no-preview]
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fxlib as FX  # noqa: E402
import b16_kukulkan as KK  # noqa: E402

MATS = {
    "sun": ((255, 210, 80), 3), "glow": ((255, 240, 150), 2), "gold": ((225, 180, 60), 7), "jade": ((60, 190, 140), 5),
    "feather": ((40, 180, 90), 7), "feather_red": ((200, 50, 40), 6), "feather_blue": ((40, 130, 200), 6),
    "feather_dark": ((20, 110, 70), 6), "scale": ((50, 140, 80), 8), "stone": ((150, 140, 120), 7),
    "stone_dark": ((110, 100, 86), 7), "black": ((16, 10, 14), 3), "shadow": ((40, 30, 50), 5), "white": ((255, 250, 230), 1),
    "teeth": ((240, 236, 220), 4),
}
SHINE = ("sun", "glow", "gold", "jade", "white")


def M(name, seed, **kw):
    m = FX.model(name, MATS, seed, shine=SHINE, **kw)
    KK.aztec_decor(m)
    return m


def screech():
    m = M("kk_fx_screech", 1621)
    a = m.anim("play", 1.2, "once")
    for j, p in enumerate("abc"):
        FX.wave(m, a, prefix=p, n=16, radius=112, mats=("sun", "feather"), size=2.0, height=1.8, grow=2.2, t_end=0.8,
                delay=0.15 * j)
    return m


def eclipse():
    m = M("kk_fx_eclipse", 1622)
    a = m.anim("play", 1.4, "once")
    b = m.bone("disc", (0, 40, 0), m.root)
    for j, (ax, ang) in enumerate(((None, 0), ("z", 45))):
        m.cube(b, f"black{j}", (-8, 32, -0.6), (8, 48, 0.6), "black", rot=(ax, ang) if ax else None, pivot=(0, 40, 0))
    import b10_kronos as KR
    KR.ring(m, b, "corona", 0, 40, -0.4, 0.4, 12, "glow", n=16, t=1.6)
    a.scl("disc", 0, 0.05)
    a.scl("disc", 0.3, 1.1)
    a.scl("disc", 0.4, 1)
    a.scl("disc", 1.1, 1)
    a.scl("disc", 1.4, 0.05)
    FX.spin(a, "disc", 1.4, 0.5)
    FX.smoke(m, a, n=8, R=30, size=6, mats=("shadow", "black"), drops="sun", t_end=1.3, grow=1.4)
    return m


def siphon():
    m = M("kk_fx_siphon", 1623)
    a = m.anim("play", 1.4, "once")
    FX.spiral(m, a, n=18, r0=40, r1=3, height=46, mats=("feather", "feather_red", "sun"), size=1.3, turns=1.3, t_end=1.4,
              grow=0.6)
    return m


def altar():
    m = M("kk_fx_altar", 1624, px=1, atlas=512)
    a = m.anim("play", 1.8, "once")
    b = m.bone("stone", (0, 0, 0), m.root)
    for j, (ax, ang) in enumerate(((None, 0), ("y", 45))):
        m.cube(b, f"disc{j}", (-30, 0.2, -30), (30, 1.0, 30), "stone", rot=(ax, ang) if ax else None, pivot=(0, 0.6, 0),
               decor={"all": "stepfret"})
    m.cube(b, "face", (-10, 1.0, -10), (10, 1.8, 10), "sun", rot=("y", 45), pivot=(0, 1.4, 0), decor={"all": "sun_face"})
    for k in range(8):
        th = 2 * math.pi * k / 8
        x, z = 24 * math.cos(th), 24 * math.sin(th)
        m.cube(b, f"glyph{k}", (x - 3, 1.0, z - 3), (x + 3, 2.0, z + 3), "jade" if k % 2 else "gold", rot=("y", 45),
               pivot=(x, 1.5, z))
    a.scl("stone", 0, 0.05, 1, 0.05)
    a.scl("stone", 0.3, 1.1, 1, 1.1)
    a.scl("stone", 0.4, 1)
    a.scl("stone", 1.2, 1)
    a.scl("stone", 1.3, 0.05, 1, 0.05)
    FX.spin(a, "stone", 1.2, 0.3)
    FX.pillar(m, a, r=6, h=60, mat="sun", core="white", t0=1.15, t_peak=1.25, t_end=1.7, bits="gold", turns=0)
    FX.wave(m, a, n=16, radius=64, mats=("sun", "jade"), size=1.8, height=4, grow=1.8, t_end=0.5, delay=1.2)
    return m


def venom():
    m = M("kk_fx_venom", 1625)
    a = m.anim("play", 1.2, "once")
    FX.wave(m, a, n=20, radius=80, mats=("jade", "teeth"), size=1.8, height=6, grow=2.0, t_end=0.6, spikes=True, tip="white",
            delay=0.5)
    FX.circle(m, a, name="ring", R=72, n=16, mats=("jade", "feather_dark"), t_in=0.3, t_hold=0.9, t_end=1.2, turns=0.4)
    return m


def solar():
    m = M("kk_fx_solar", 1626)
    a = m.anim("play", 1.8, "once")
    FX.pillar(m, a, r=8, h=80, mat="sun", core="white", t_peak=0.6, t_end=1.4, bits="gold", turns=1)
    FX.wave(m, a, prefix="a", n=30, radius=192, mats=("sun", "gold", "glow"), size=3.0, height=5, grow=2.6, t_end=0.9, delay=0.6)
    FX.wave(m, a, prefix="b", n=16, radius=180, mats=("feather", "jade"), size=1.4, height=8, grow=1.4, t_end=0.9,
            spikes=True, tip="white", delay=0.65)
    return m


def sunrays():
    m = M("kk_fx_sunrays", 1627)
    a = m.anim("play", 1.6, "once")
    import random
    rng = random.Random(16)
    for i in range(12):
        r = rng.uniform(16, 160)
        th = rng.uniform(0, 6.28)
        x, z = r * math.cos(th), r * math.sin(th)
        t0 = 0.5 if i % 2 == 0 else 1.0
        n = f"beam{i}"
        b = m.bone(n, (x, 0, z), m.root)
        m.cube(b, n, (x - 2.0, 0, z - 2.0), (x + 2.0, 90, z + 2.0), "sun")
        m.cube(b, n + "c", (x - 0.8, 0, z - 0.8), (x + 0.8, 92, z + 0.8), "white")
        a.scl(n, 0, 0.01)
        a.scl(n, t0 - 0.05, 0.01)
        a.scl(n, t0, 1.4, 1, 1.4, i="linear")
        a.scl(n, t0 + 0.25, 0.01, 1, 0.01)
    FX.circle(m, a, name="mark", R=160, n=20, mats=("sun", "gold"), t_in=0.3, t_hold=1.3, t_end=1.6, turns=0.2)
    return m


def serpents():
    m = M("kk_fx_serpents", 1628)
    a = m.anim("play", 1.8, "once")

    def piece(m, b, x, z, k):
        for i in range(4):
            w = 1.6 - i * 0.25
            ang = 22.5 if i % 2 else -22.5
            m.cube(b, f"sp{k}_{i}", (x - w, i * 4.4, z - w), (x + w, i * 4.4 + 4.8, z + w), "scale" if i % 2 else "feather",
                   rot=("x", ang), pivot=(x, i * 4.4, z), decor={"all": "scales"})
        m.cube(b, f"sp{k}_head", (x - 1.6, 17, z - 3.4), (x + 1.6, 19.6, z + 1.0), "scale", decor={"all": "scales"})
        m.cube(b, f"sp{k}_crest", (x - 0.4, 19.4, z - 1.6), (x + 0.4, 23.4, z - 0.6), "feather_red", decor={"all": "feather"})

    FX.rise_ring(m, a, n=5, R=30, piece=piece, t_up=0.35, t_hold=1.4, t_end=1.8, depth=26)
    FX.circle(m, a, name="ring", R=40, n=14, mats=("jade", "gold"), t_in=0.3, t_hold=1.4, t_end=1.8, turns=0.4)
    return m


def pyramid():
    m = M("kk_fx_pyramid", 1629)
    a = m.anim("play", 2.4, "once")

    def step(m, b, x, z, k):
        m.cube(b, f"st{k}", (x - 6, 0, z - 6), (x + 6, 8 + (k % 2) * 3, z + 6), "stone" if k % 2 else "stone_dark",
               decor={"all": "stepfret"})
        m.cube(b, f"st_top{k}", (x - 4, 8 + (k % 2) * 3, z - 4), (x + 4, 12 + (k % 2) * 3, z + 4), "gold", decor={"all": "stepfret"})

    FX.rise_ring(m, a, n=8, R=52, piece=step, t_up=0.4, t_hold=2.0, t_end=2.4, depth=16, face_out=False)
    rows = ["..YYY..", ".YGGGY.", "YGJJJGY", "YGJSJGY", "YGJJJGY", ".YGGGY.", "..YYY.."]
    FX.floating_glyph(m, a, "sun", rows, {"Y": "sun", "G": "gold", "J": "jade", "S": "white"}, px=2.6, y=56, t_end=2.3,
                      turns=0.6, ring="glow")
    return m


BUILDERS = {"kk_fx_screech": screech, "kk_fx_eclipse": eclipse, "kk_fx_siphon": siphon, "kk_fx_altar": altar,
            "kk_fx_venom": venom, "kk_fx_solar": solar, "kk_fx_sunrays": sunrays, "kk_fx_serpents": serpents,
            "kk_fx_pyramid": pyramid}
SHOTS = {"kk_fx_screech": [0.1, 0.3, 0.6, 0.9], "kk_fx_eclipse": [0.2, 0.5, 0.9, 1.2], "kk_fx_siphon": [0.2, 0.6, 1.0, 1.3],
         "kk_fx_altar": [0.3, 0.9, 1.25, 1.5], "kk_fx_venom": [0.3, 0.55, 0.8, 1.0], "kk_fx_solar": [0.3, 0.7, 1.0, 1.3],
         "kk_fx_sunrays": [0.3, 0.52, 1.02, 1.3], "kk_fx_serpents": [0.2, 0.5, 1.0, 1.6], "kk_fx_pyramid": [0.3, 0.8, 1.5, 2.1]}
VIEW = {"kk_fx_screech": (6, 1.6, -20), "kk_fx_eclipse": (30, 2.4, -20), "kk_fx_siphon": (20, 3.0, -20),
        "kk_fx_altar": (14, 1.8, -20), "kk_fx_venom": (8, 2.0, -20), "kk_fx_solar": (30, 0.8, -20),
        "kk_fx_sunrays": (40, 0.9, -20), "kk_fx_serpents": (12, 2.4, -20), "kk_fx_pyramid": (24, 1.6, -20)}

if __name__ == "__main__":
    FX.build_all(BUILDERS, KK.BLUEPRINTS, KK.PREVIEW / "efectos", SHOTS, VIEW)
