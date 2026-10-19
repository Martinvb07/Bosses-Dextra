#!/usr/bin/env python3
"""
Efectos de los ataques de THOR (modelos de ModelEngine con animacion "play").

  th_fx_swing      media luna electrica del martillazo                    (TH_ToxicSwipe)
  th_fx_bolt       rayo que cae sobre el jugador a los 0.4 s              (TH_SporeBolt)
  th_fx_shock      anillo de descarga de 7 bloques                        (TH_SporeBurst)
  th_fx_thunder    trueno: nube que revienta sobre Thor (6 bloques)       (TH_ToxicCloud)
  th_fx_absorb     rayos que caen sobre el propio Thor                    (TH_FungalBloom, cambios de fase)
  th_fx_nova       nova de trueno a los 0.5 s (8 bloques)                 (TH_MycotoxinNova, TH_PlagueSurge)
  th_fx_eruption   lluvia de rayos y ola electrica (9 bloques)            (TH_CorruptionEruption)
  th_fx_judgement  circulo de Mjolnir y rayo gigante a los 1.2 s          (TH_GardenSentence)
  th_fx_ragnarok   cupula de tormenta que estalla a los 1.5 s (10 bl.)    (TH_PlagueApocalypse)
  th_fx_valhalla   columna de luz dorada del Valhalla                     (invocaciones e intro)
  (el campo estatico y la nube de tormenta son los modelos th_field y th_cloud)

Uso: python3 tools/b15_fx.py [efecto ...] [--no-preview]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fxlib as FX  # noqa: E402
import b15_thor as TH  # noqa: E402

MATS = {
    "bolt": ((140, 230, 255), 2), "core": ((250, 255, 255), 1), "blue": ((60, 120, 220), 5), "cloud": ((90, 96, 110), 6),
    "cloud_hi": ((150, 156, 170), 6), "gold": ((255, 210, 100), 4), "gold_dark": ((200, 150, 60), 5), "white": ((255, 255, 255), 1),
    "stone": ((110, 110, 120), 6),
}
SHINE = ("bolt", "core", "gold", "white")


def M(name, seed, **kw):
    m = FX.model(name, MATS, seed, shine=SHINE, **kw)
    TH.storm_decor(m)
    return m


def strike(m, a, name, t0, x=0, z=0, top=80, w=1.4, t_hold=0.25, ring=True):
    """Rayo que cae del cielo en t0: aparece de golpe, parpadea y se apaga."""
    b = m.bone(name, (x, 0, z), m.root)
    TH.zigzag(m, b, name + "_z", x, top, z, top, seg=8, w=w, mat="bolt")
    TH.zigzag(m, b, name + "_c", x, top, z, top, seg=8, w=w * 0.45, mat="core")
    a.scl(name, 0, 0.01)
    if t0 > 0.02:
        a.scl(name, round(t0 - 0.02, 3), 0.01)
    a.scl(name, t0, 1, i="linear")
    a.scl(name, t0 + t_hold * 0.4, 0.3, 1, 0.3, i="linear")
    a.scl(name, t0 + t_hold * 0.6, 1.2, 1, 1.2, i="linear")
    a.scl(name, t0 + t_hold, 0.01, 1, 0.01)
    if ring:
        FX.wave(m, a, prefix=name + "w", n=10, radius=40, mats=("bolt", "white"), size=1.2, height=1.6, grow=1.4, t_end=0.5,
                delay=t0)


def swing():
    m = M("th_fx_swing", 1521)
    a = m.anim("play", 0.6, "once")
    FX.arc(m, a, name="arc", R=34, mats=("bolt", "core"), trail="blue", tilt=8, y=16, z=-14, length=0.5, sweep=(70, -60))
    return m


def bolt():
    m = M("th_fx_bolt", 1522)
    a = m.anim("play", 1.0, "once")
    FX.circle(m, a, name="mark", R=20, n=10, mats=("blue", "bolt"), t_in=0.2, t_hold=0.5, t_end=0.8, turns=0.6)
    strike(m, a, "s", 0.4, top=96)
    return m


def shock():
    m = M("th_fx_shock", 1523)
    a = m.anim("play", 0.9, "once")
    FX.wave(m, a, prefix="a", n=22, radius=112, mats=("bolt", "blue"), size=2.0, height=3, grow=1.8, t_end=0.7)
    FX.wave(m, a, prefix="b", n=12, radius=104, mats=("core", "bolt"), size=0.8, height=8, grow=1.2, t_end=0.75, spikes=True,
            tip="white", delay=0.05)
    return m


def thunder():
    m = M("th_fx_thunder", 1524)
    a = m.anim("play", 1.4, "once")
    FX.smoke(m, a, prefix="c", n=8, R=22, size=7, mats=("cloud", "cloud_hi"), t_end=1.3, grow=1.4)
    for i, (x, z) in enumerate(((20, 10), (-24, 6), (6, -26))):
        strike(m, a, f"s{i}", 0.2 + 0.15 * i, x, z, top=70, w=1.0, ring=False)
    FX.wave(m, a, n=18, radius=96, mats=("bolt", "cloud_hi"), size=1.8, height=2, grow=1.6, t_end=0.7, delay=0.2)
    return m


def absorb():
    m = M("th_fx_absorb", 1525)
    a = m.anim("play", 1.2, "once")
    for i, (x, z, t) in enumerate(((0, 0, 0.2), (3, 2, 0.45), (-3, -1, 0.7))):
        strike(m, a, f"s{i}", t, x, z, top=100, w=1.6, ring=(i == 0))
    FX.spiral(m, a, prefix="p", n=12, r0=40, r1=4, height=36, mats=("bolt", "core"), size=0.8, turns=1.2, t_end=1.0, grow=0.4)
    return m


def nova():
    m = M("th_fx_nova", 1526)
    a = m.anim("play", 1.3, "once")
    strike(m, a, "s", 0.45, top=110, w=2.2, ring=False)
    FX.wave(m, a, prefix="a", n=26, radius=128, mats=("bolt", "blue", "white"), size=2.6, height=4, grow=2.0, t_end=0.7,
            delay=0.5)
    FX.wave(m, a, prefix="b", n=14, radius=120, mats=("core", "bolt"), size=1.0, height=9, grow=1.3, t_end=0.75, spikes=True,
            tip="white", delay=0.55)
    return m


def eruption():
    m = M("th_fx_eruption", 1527)
    a = m.anim("play", 1.4, "once")
    import random
    rng = random.Random(15)
    for i in range(7):
        r = rng.uniform(20, 140)
        th = rng.uniform(0, 6.28)
        import math
        strike(m, a, f"s{i}", rng.uniform(0.0, 0.5), r * math.cos(th), r * math.sin(th), top=90, w=1.1, ring=False)
    FX.wave(m, a, n=26, radius=144, mats=("bolt", "blue", "cloud_hi"), size=2.6, height=3, grow=2.0, t_end=0.8)
    return m


def judgement():
    m = M("th_fx_judgement", 1528, px=1, atlas=512)
    a = m.anim("play", 1.8, "once")
    FX.circle(m, a, name="ring", R=64, n=16, mats=("gold", "bolt"), t_in=0.3, t_hold=1.2, t_end=1.5, turns=0.8)
    rows = [".XXXXX.", ".XGGGX.", ".XGGGX.", "...X...", "...X...", "...G..."]
    FX.floating_glyph(m, a, "mjolnir", rows, {"X": "stone", "G": "gold"}, px=2.4, y=60, t_end=1.3, turns=1.0, ring="bolt")
    strike(m, a, "s", 1.2, top=120, w=3.2)
    return m


def ragnarok():
    m = M("th_fx_ragnarok", 1529)
    a = m.anim("play", 2.2, "once")
    FX.dome(m, a, n=16, R=50, h=30, w=2.6, mat="bolt", tip="core", t_charge=1.5, t_end=2.2, burst=160)
    FX.smoke(m, a, prefix="c", n=8, R=40, size=10, mats=("cloud", "cloud_hi"), t_end=2.0, grow=1.3)
    for i in range(4):
        import math
        th = 1.57 * i
        strike(m, a, f"s{i}", 1.5, 60 * math.cos(th), 60 * math.sin(th), top=100, w=1.6, ring=False)
    FX.wave(m, a, n=30, radius=160, mats=("bolt", "white", "blue"), size=3.0, height=5, grow=2.4, t_end=0.7, delay=1.5)
    return m


def valhalla():
    m = M("th_fx_valhalla", 1530)
    a = m.anim("play", 1.8, "once")
    FX.pillar(m, a, r=8, h=70, mat="gold", core="white", t_peak=0.3, t_end=1.6, bits="gold_dark", turns=0.5)
    FX.circle(m, a, name="ring", R=36, n=14, mats=("gold", "gold_dark"), t_in=0.3, t_hold=1.4, t_end=1.8, turns=0.4)
    return m


BUILDERS = {"th_fx_swing": swing, "th_fx_bolt": bolt, "th_fx_shock": shock, "th_fx_thunder": thunder, "th_fx_absorb": absorb,
            "th_fx_nova": nova, "th_fx_eruption": eruption, "th_fx_judgement": judgement, "th_fx_ragnarok": ragnarok,
            "th_fx_valhalla": valhalla}
SHOTS = {"th_fx_swing": [0.05, 0.15, 0.3, 0.45], "th_fx_bolt": [0.2, 0.42, 0.5, 0.7], "th_fx_shock": [0.1, 0.3, 0.5, 0.7],
         "th_fx_thunder": [0.2, 0.4, 0.7, 1.1], "th_fx_absorb": [0.22, 0.47, 0.72, 1.0], "th_fx_nova": [0.3, 0.47, 0.7, 1.0],
         "th_fx_eruption": [0.1, 0.3, 0.5, 0.8], "th_fx_judgement": [0.4, 1.0, 1.22, 1.4], "th_fx_ragnarok": [0.6, 1.4, 1.55, 1.8],
         "th_fx_valhalla": [0.2, 0.5, 1.0, 1.5]}
VIEW = {"th_fx_swing": (16, 3.6, -20), "th_fx_bolt": (40, 2.0, -20), "th_fx_shock": (8, 1.6, -20),
        "th_fx_thunder": (30, 1.4, -20), "th_fx_absorb": (40, 1.8, -20), "th_fx_nova": (40, 1.0, -20),
        "th_fx_eruption": (40, 0.9, -20), "th_fx_judgement": (50, 1.2, -20), "th_fx_ragnarok": (40, 0.9, -20),
        "th_fx_valhalla": (30, 1.6, -20)}

if __name__ == "__main__":
    FX.build_all(BUILDERS, TH.BLUEPRINTS, TH.PREVIEW / "efectos", SHOTS, VIEW)
