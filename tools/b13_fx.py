#!/usr/bin/env python3
"""
Efectos de los ataques de XYLAR (modelos de ModelEngine con animacion "play").

  xy_fx_combo     tres tajos de energia (0, 0.3 y 0.6 s)                    (XY_SlashCombo)
  xy_fx_mark      orbita de estrellas y constelacion sobre el marcado       (XY_RedMark)
  xy_fx_dash      estallido de estrellas al desaparecer/aparecer            (XY_ShadowDash)
  xy_fx_crush     la gravedad aspira y aplasta a los 0.5 s (7 bloques)      (XY_HandCrush)
  xy_fx_nova      nova galactica de 9 bloques a los 0.4 s                   (XY_BloodNova)
  xy_fx_horizon   agujero negro que crece 2 s y estalla (7 bloques)         (XY_Execution)
  xy_fx_meteor    capsulas que caen desde la orbita                         (XY_SummonSquires, invocaciones)
  xy_fx_phase     constelacion y cupula de cristales                        (fases e intro)
  (el pozo gravitatorio es el modelo xy_well, en b13_xylar.py)

Uso: python3 tools/b13_fx.py [efecto ...] [--no-preview]
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fxlib as FX  # noqa: E402
import b13_xylar as XY  # noqa: E402

MATS = {
    "energy": ((255, 170, 255), 2), "glow": ((255, 90, 255), 3), "star": ((255, 240, 220), 2), "void": ((10, 6, 18), 3),
    "violet": ((150, 60, 200), 6), "armor": ((36, 26, 50), 5), "white": ((255, 255, 255), 1), "nebula": ((120, 30, 110), 5),
}
SHINE = ("energy", "glow", "star", "white")


def M(name, seed, **kw):
    m = FX.model(name, MATS, seed, shine=SHINE, **kw)
    XY.star_decor(m)
    return m


def combo():
    m = M("xy_fx_combo", 1321)
    a = m.anim("play", 1.2, "once")
    for i, (dt, tilt, sweep) in enumerate(((0.0, 20, (-80, 40)), (0.3, -25, (60, -60)), (0.6, 70, (-70, 50)))):
        FX.shifted(m, a, dt, lambda m, t, i=i, tilt=tilt, sweep=sweep: FX.arc(
            m, t, name=f"arc{i}", R=26, mats=("energy", "glow"), trail="violet", tilt=tilt, y=18, z=-14, length=0.45,
            sweep=sweep))
    return m


def mark():
    m = M("xy_fx_mark", 1322)
    a = m.anim("play", 3.0, "once")
    FX.circle(m, a, name="orbit", R=24, n=12, mats=("glow", "star"), t_in=0.3, t_hold=2.6, t_end=3.0, turns=1.0)
    rows = ["...X...", "..XGX..", "XXGSGXX", ".XGSGX.", "..XGX..", ".X...X."]
    FX.floating_glyph(m, a, "star", rows, {"X": "violet", "G": "glow", "S": "white"}, px=1.8, y=44, t_end=3.0, turns=1.5,
                      ring="star")
    return m


def dash():
    m = M("xy_fx_dash", 1323)
    a = m.anim("play", 0.9, "once")
    FX.smoke(m, a, n=8, R=12, size=3.4, mats=("void", "nebula"), drops="glow", t_end=0.8, grow=1.3)
    FX.wave(m, a, n=14, radius=48, mats=("star", "glow"), size=1.0, height=4, grow=1.4, t_end=0.6, spikes=True, tip="white")
    return m


def crush():
    m = M("xy_fx_crush", 1324)
    a = m.anim("play", 1.2, "once")
    FX.spiral(m, a, prefix="s", n=22, r0=160, r1=4, height=16, mats=("violet", "star", "glow"), size=1.6, turns=1.0,
              t_end=0.5, grow=0.2)
    FX.wave(m, a, n=22, radius=112, mats=("void", "glow"), size=2.4, height=4, grow=2.0, t_end=0.6, spikes=True,
            tip="energy", delay=0.5)
    return m


def nova():
    m = M("xy_fx_nova", 1325)
    a = m.anim("play", 1.4, "once")
    FX.pillar(m, a, r=4, h=56, mat="glow", core="white", t_peak=0.4, t_end=1.0, bits="star", turns=1)
    FX.wave(m, a, prefix="a", n=26, radius=144, mats=("glow", "violet"), size=2.6, height=4, grow=2.2, t_end=0.8, delay=0.4)
    FX.wave(m, a, prefix="b", n=14, radius=136, mats=("star", "energy"), size=1.0, height=8, grow=1.4, t_end=0.85,
            spikes=True, tip="white", delay=0.45)
    return m


def horizon():
    m = M("xy_fx_horizon", 1326)
    a = m.anim("play", 2.8, "once")
    b = m.bone("hole", (0, 24, 0), m.root)
    for j, (ax, ang) in enumerate(((None, 0), ("y", 45), ("x", 45), ("z", 45))):
        m.cube(b, f"hole{j}", (-7, 17, -7), (7, 31, 7), "void", rot=(ax, ang) if ax else None, pivot=(0, 24, 0))
    ring = m.bone("ring", (0, 24, 0), b, rotation=(20, 0, 0))
    import b10_kronos as KR
    KR.ring(m, ring, "acc", 0, 24, -0.6, 0.6, 14, "glow", n=16, t=1.6)
    FX.spin(a, "ring", 2.0, 3, "z")
    a.scl("hole", 0, 0.05)
    a.scl("hole", 1.9, 1.0, i="linear")
    a.scl("hole", 2.0, 1.3)
    a.scl("hole", 2.1, 0.05)
    a.scl("hole", 2.8, 0.05)
    FX.spiral(m, a, prefix="s", n=18, r0=120, r1=6, height=30, mats=("star", "violet"), size=1.2, turns=2.0, t_end=1.9,
              grow=0.3)
    FX.wave(m, a, n=24, radius=112, mats=("glow", "energy", "void"), size=2.8, height=5, grow=2.2, t_end=0.7, delay=2.0)
    return m


def meteor():
    m = M("xy_fx_meteor", 1327)
    a = m.anim("play", 1.6, "once")
    FX.rain(m, a, n=3, radius=96, h=(12, 16), w=4.0, mat="armor", tip="glow", top=180, t_window=0.4, t_end=1.6, seed=13)
    FX.wave(m, a, n=14, radius=64, mats=("star", "violet"), size=1.6, height=2, grow=1.6, t_end=0.6, delay=0.6)
    return m


def phase():
    m = M("xy_fx_phase", 1328)
    a = m.anim("play", 2.4, "once")
    FX.dome(m, a, n=14, R=42, h=26, w=3.0, mat="violet", tip="energy", t_charge=1.7, t_end=2.4, burst=150)
    FX.circle(m, a, name="const", R=56, n=14, mats=("star", "glow"), t_in=0.3, t_hold=2.0, t_end=2.4, turns=0.6)
    return m


BUILDERS = {"xy_fx_combo": combo, "xy_fx_mark": mark, "xy_fx_dash": dash, "xy_fx_crush": crush, "xy_fx_nova": nova,
            "xy_fx_horizon": horizon, "xy_fx_meteor": meteor, "xy_fx_phase": phase}
SHOTS = {"xy_fx_combo": [0.1, 0.4, 0.7, 0.9], "xy_fx_mark": [0.4, 1.2, 2.0, 2.8], "xy_fx_dash": [0.1, 0.3, 0.5, 0.7],
         "xy_fx_crush": [0.15, 0.4, 0.6, 0.9], "xy_fx_nova": [0.3, 0.5, 0.8, 1.1], "xy_fx_horizon": [0.6, 1.5, 2.0, 2.3],
         "xy_fx_meteor": [0.2, 0.45, 0.7, 1.2], "xy_fx_phase": [0.4, 1.0, 1.7, 2.1]}
VIEW = {"xy_fx_combo": (16, 4.0, -20), "xy_fx_mark": (30, 3.0, -20), "xy_fx_dash": (10, 3.6, -20),
        "xy_fx_crush": (10, 1.2, -20), "xy_fx_nova": (20, 1.0, -20), "xy_fx_horizon": (24, 1.6, -20),
        "xy_fx_meteor": (40, 1.6, -20), "xy_fx_phase": (20, 1.8, -20)}

if __name__ == "__main__":
    FX.build_all(BUILDERS, XY.BLUEPRINTS, XY.PREVIEW / "efectos", SHOTS, VIEW)
