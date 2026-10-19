#!/usr/bin/env python3
"""
Efectos de los ataques de SAMHAIN (modelos de ModelEngine con animacion "play").

  sh_fx_reap      media luna de fuego de la guadana                        (SH_HeavyStrike)
  sh_fx_harvest   golpe de cosecha: grietas y llamas a los 0.3 s (4 bl.)   (SH_DevastatingBlow)
  sh_fx_burst     anillo de fuego de animas de 7 bloques                   (SH_FreezeBurst)
  sh_fx_souls     tormenta de almas en espiral y ola a los 0.4 s (9 bl.)   (SH_IceStorm)
  sh_fx_wisps     lluvia de fuegos fatuos durante 1 s (12 bloques)         (SH_LightningStorm)
  sh_fx_moon      luna de calabaza que crece 2 s y estalla (12 bloques)    (SH_RunOrDie)
  sh_fx_graves    calabazas y lapidas que salen del suelo                  (invocaciones)
  sh_fx_phase     circulo de velas y columna de fuego de almas             (fases e intro)

Uso: python3 tools/b14_fx.py [efecto ...] [--no-preview]
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fxlib as FX  # noqa: E402
import b14_samhain as SH  # noqa: E402

MATS = {
    "fire": ((255, 170, 40), 3), "flame": ((255, 220, 120), 2), "ember": ((200, 70, 10), 5), "soul": ((90, 220, 255), 3),
    "soul_dark": ((40, 120, 170), 4), "pumpkin": ((230, 120, 20), 8), "pumpkin_dark": ((170, 80, 10), 7), "stem": ((80, 110, 40), 7),
    "leaf": ((70, 130, 40), 8), "stone": ((110, 110, 115), 7), "dirt": ((60, 40, 30), 6), "candle": ((235, 225, 200), 4),
    "white": ((255, 255, 240), 1),
}
SHINE = ("fire", "flame", "soul", "white")


def M(name, seed, **kw):
    m = FX.model(name, MATS, seed, shine=SHINE, **kw)
    SH.harvest_decor(m)
    return m


def reap():
    m = M("sh_fx_reap", 1421)
    a = m.anim("play", 0.6, "once")
    FX.arc(m, a, name="arc", R=34, mats=("fire", "flame"), trail="ember", tilt=8, y=16, z=-14, length=0.5, sweep=(70, -60))
    return m


def harvest():
    m = M("sh_fx_harvest", 1422)
    a = m.anim("play", 1.2, "once")
    FX.shifted(m, a, 0.3, lambda m, t: (
        FX.circle(m, t, name="crack", R=56, n=12, mats=("dirt", "ember"), t_in=0.1, t_hold=0.6, t_end=0.9, turns=0, grow=1.3),
        FX.wave(m, t, n=14, radius=64, mats=("fire", "flame"), size=1.8, height=6, grow=1.8, t_end=0.6, spikes=True,
                tip="white")))
    return m


def burst():
    m = M("sh_fx_burst", 1423)
    a = m.anim("play", 1.0, "once")
    FX.wave(m, a, prefix="a", n=24, radius=112, mats=("fire", "ember"), size=2.4, height=5, grow=2.0, t_end=0.8, tip="flame")
    FX.wave(m, a, prefix="b", n=14, radius=104, mats=("soul", "soul_dark"), size=1.2, height=7, grow=1.4, t_end=0.85,
            spikes=True, tip="white", delay=0.06)
    return m


def souls():
    m = M("sh_fx_souls", 1424)
    a = m.anim("play", 1.6, "once")
    FX.spiral(m, a, prefix="s", n=22, r0=20, r1=150, height=40, mats=("soul", "fire", "white"), size=1.4, turns=1.2,
              t_end=1.4, grow=1.4)
    FX.wave(m, a, n=24, radius=144, mats=("soul", "soul_dark", "fire"), size=2.4, height=4, grow=2.0, t_end=0.8, delay=0.4)
    return m


def wisps():
    m = M("sh_fx_wisps", 1425)
    a = m.anim("play", 1.8, "once")
    FX.rain(m, a, n=14, radius=192, h=(8, 12), w=3.6, mat="fire", tip="soul", top=140, t_window=1.1, t_end=1.8, seed=14)
    return m


def moon():
    m = M("sh_fx_moon", 1426, px=1, atlas=1024)
    a = m.anim("play", 2.8, "once")
    b = m.bone("moon", (0, 60, 0), m.root)
    for j, (ax, ang) in enumerate(((None, 0), ("y", 45), ("x", 45))):
        m.cube(b, f"moon{j}", (-22, 40, -22), (22, 80, 22), "pumpkin" if j != 1 else "pumpkin_dark",
               rot=(ax, ang) if ax else None, pivot=(0, 60, 0), decor={"north": "jack", "all": "pumpkin"} if j == 0 else
               {"all": "pumpkin"})
    m.cube(b, "moon_stem", (-3, 79, -3), (3, 90, 3), "stem", rot=("z", -22.5), pivot=(0, 80, 0))
    m.cube(b, "moon_leaf", (2, 80, -7), (18, 82, 6), "leaf", rot=("z", 22.5), pivot=(2, 81, 0))
    FX.spin(a, "moon", 2.0, 1)
    a.scl("moon", 0, 0.05)
    a.scl("moon", 1.9, 1.0, i="linear")
    a.scl("moon", 2.0, 1.3)
    a.scl("moon", 2.08, 0.05)
    a.scl("moon", 2.8, 0.05)
    FX.circle(m, a, name="ring", R=180, n=28, mats=("fire", "ember"), t_in=0.4, t_hold=2.0, t_end=2.2, turns=0.3)
    FX.wave(m, a, n=30, radius=192, mats=("fire", "pumpkin", "flame"), size=3.0, height=6, grow=2.4, t_end=0.7, delay=2.0)
    return m


def graves():
    m = M("sh_fx_graves", 1427)
    a = m.anim("play", 1.8, "once")

    def piece(m, b, x, z, k):
        if k % 2:
            m.cube(b, f"stone{k}", (x - 3, 0, z - 1), (x + 3, 9, z + 1), "stone")
            m.cube(b, f"stone_top{k}", (x - 2.2, 7.6, z - 1), (x + 2.2, 11.2, z + 1), "stone", rot=("z", 45), pivot=(x, 9, z))
        else:
            m.cube(b, f"pk{k}", (x - 3.4, 0, z - 3.4), (x + 3.4, 5.4, z + 3.4), "pumpkin", decor={"all": "pumpkin"})
            m.cube(b, f"pk_glow{k}", (x - 2.4, 1, z - 3.5), (x + 2.4, 3.6, z - 3.3), "fire")
            m.cube(b, f"pk_stem{k}", (x - 0.5, 5.2, z - 0.5), (x + 0.5, 7.2, z + 0.5), "stem")

    FX.rise_ring(m, a, n=6, R=40, piece=piece, t_up=0.35, t_hold=1.4, t_end=1.8, depth=14)
    FX.smoke(m, a, n=6, R=24, size=3.0, mats=("soul", "soul_dark"), t_end=1.4, grow=1.1)
    return m


def phase():
    m = M("sh_fx_phase", 1428)
    a = m.anim("play", 2.2, "once")

    def candle(m, b, x, z, k):
        m.cube(b, f"candle{k}", (x - 1.2, 0, z - 1.2), (x + 1.2, 6 + (k % 3) * 2, z + 1.2), "candle")
        m.cube(b, f"candle_fl{k}", (x - 0.8, 6 + (k % 3) * 2, z - 0.8), (x + 0.8, 8.6 + (k % 3) * 2, z + 0.8), "flame",
               rot=("y", 45), pivot=(x, 7, z))

    FX.circle(m, a, name="ring", R=48, n=16, mats=("ember", "fire"), t_in=0.3, t_hold=1.8, t_end=2.2, turns=0.3, items=candle)
    FX.pillar(m, a, r=5, h=60, mat="soul", core="white", t0=0.2, t_peak=0.5, t_end=1.6, bits="fire", turns=1)
    return m


BUILDERS = {"sh_fx_reap": reap, "sh_fx_harvest": harvest, "sh_fx_burst": burst, "sh_fx_souls": souls, "sh_fx_wisps": wisps,
            "sh_fx_moon": moon, "sh_fx_graves": graves, "sh_fx_phase": phase}
SHOTS = {"sh_fx_reap": [0.05, 0.15, 0.3, 0.45], "sh_fx_harvest": [0.2, 0.4, 0.6, 0.9], "sh_fx_burst": [0.1, 0.3, 0.5, 0.8],
         "sh_fx_souls": [0.3, 0.6, 0.9, 1.3], "sh_fx_wisps": [0.3, 0.7, 1.1, 1.5], "sh_fx_moon": [0.6, 1.5, 2.0, 2.3],
         "sh_fx_graves": [0.2, 0.5, 1.0, 1.6], "sh_fx_phase": [0.3, 0.8, 1.4, 2.0]}
VIEW = {"sh_fx_reap": (16, 3.6, -20), "sh_fx_harvest": (8, 2.6, -20), "sh_fx_burst": (8, 1.4, -20),
        "sh_fx_souls": (16, 1.0, -20), "sh_fx_wisps": (30, 0.8, -20), "sh_fx_moon": (40, 0.8, -20),
        "sh_fx_graves": (8, 2.6, -20), "sh_fx_phase": (24, 1.8, -20)}

if __name__ == "__main__":
    FX.build_all(BUILDERS, SH.BLUEPRINTS, SH.PREVIEW / "efectos", SHOTS, VIEW)
