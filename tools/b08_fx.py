#!/usr/bin/env python3
"""
Efectos de los ataques del YETI (modelos de ModelEngine con animacion "play").

  yt_fx_shatter   grietas y ola de pinchos de hielo de 7 bloques           (Yeti_GroundShatter)
  yt_fx_smash     racimo de cristales que revienta delante del Yeti        (Yeti_IceSmash)
  yt_fx_rock      roca de hielo que cae sobre el objetivo                  (Yeti_IceRockThrow)
  yt_fx_barrage   lluvia de rocas de hielo en 9 bloques                    (Yeti_IceRockBarrage)
  yt_fx_nova      ola de nieve y escarcha de 7 bloques                     (Yeti_FrostNova)
  yt_fx_blizzard  remolino de ventisca alrededor del Yeti                  (Yeti_IntenseBlizzard)
  yt_fx_roar      anillos de nieve que salen del rugido                    (Yeti_Roar)
  yt_fx_shield    cupula de hielo de la fase 3 (escudo de subditos)         (Yeti_Phase3_Check)
  yt_fx_snow      estallido de nieve de las invocaciones                   (invocaciones)

Uso: python3 tools/b08_fx.py [efecto ...] [--no-preview]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fxlib as FX  # noqa: E402
import b08_yeti as YT  # noqa: E402

MATS = {
    "ice": ((150, 210, 245), 6), "ice_dark": ((70, 130, 200), 6), "glow": ((215, 245, 255), 3),
    "snow": ((238, 244, 250), 3), "snow_shade": ((196, 210, 226), 4), "rock": ((110, 130, 150), 6),
    "crack": ((40, 70, 110), 4), "white": ((255, 255, 255), 1),
}
SHINE = ("ice", "glow", "white")


def M(name, seed, **kw):
    return FX.model(name, MATS, seed, shine=SHINE, **kw)


def shatter():
    m = M("yt_fx_shatter", 811)
    a = m.anim("play", 1.4, "once")
    FX.circle(m, a, name="cracks", R=60, n=16, mats=("crack", "ice_dark"), t_in=0.15, t_hold=1.1, t_end=1.4, turns=0.0,
              grow=1.9)
    FX.wave(m, a, n=22, radius=112, mats=("ice", "ice_dark"), size=2.2, height=7, grow=2.0, t_end=0.9, spikes=True,
            tip="glow", delay=0.25)
    return m


def smash():
    m = M("yt_fx_smash", 812)
    a = m.anim("play", 1.1, "once")
    FX.crystals_burst(m, a, spec=[(0, -10, 20, 3.4, None), (-7, -6, 14, 2.6, ("z", 22.5)), (7, -6, 15, 2.6, ("z", -22.5)),
                                  (-4, -16, 12, 2.2, ("x", -22.5)), (5, -15, 13, 2.2, ("x", -22.5)),
                                  (0, -2, 10, 2.0, ("x", 22.5))],
                      mat="ice", tip="glow", t_out=0.08, t_hold=0.6, t_end=1.0, fly=18)
    FX.smoke(m, a, n=6, R=12, size=3.5, mats=("snow", "snow_shade"), t_end=1.0, grow=1.3)
    return m


def boulder(m, b, x=0, y=0, z=0, s=1.0, name="rock"):
    m.cube(b, name, (x - 6 * s, y, z - 6 * s), (x + 6 * s, y + 11 * s, z + 6 * s), "ice", decor={"all": "crystal"})
    m.cube(b, name + "45", (x - 5 * s, y + 1 * s, z - 5 * s), (x + 5 * s, y + 10 * s, z + 5 * s), "ice_dark",
           rot=("y", 45), pivot=(x, y, z), decor={"all": "crystal"})
    m.cube(b, name + "x", (x - 4 * s, y - 1 * s, z - 6.6 * s), (x + 4 * s, y + 9 * s, z + 6.6 * s), "rock",
           rot=("x", 22.5), pivot=(x, y + 5 * s, z))
    m.cube(b, name + "top", (x - 2.5 * s, y + 10 * s, z - 2.5 * s), (x + 2.5 * s, y + 13 * s, z + 2.5 * s), "glow")


def rock():
    m = M("yt_fx_rock", 813)
    a = m.anim("play", 1.4, "once")
    b = m.bone("boulder", (0, 0, 0), m.root)
    boulder(m, b)
    a.pos("boulder", 0, 0, 90, 0)
    a.pos("boulder", 0.55, 0, 0, 0, i="linear")
    a.pos("boulder", 1.4, 0, -8, 0)
    a.rot("boulder", 0, 0, 0, 0)
    a.rot("boulder", 0.55, 60, 30, 0, i="linear")
    a.scl("boulder", 0.55, 1)
    a.scl("boulder", 0.65, 1.25, 0.7, 1.25)
    a.scl("boulder", 1.0, 1)
    a.scl("boulder", 1.4, 0.05)
    FX.wave(m, a, n=12, radius=48, mats=("ice", "snow"), size=1.6, height=4, grow=1.6, t_end=0.6, spikes=True, tip="glow",
            delay=0.55)
    return m


def barrage():
    m = M("yt_fx_barrage", 814, px=1, atlas=512)
    a = m.anim("play", 1.8, "once")
    FX.rain(m, a, n=12, radius=144, h=(14, 20), w=6.5, mat="ice", tip="rock", top=130, t_window=0.55, t_end=1.8, seed=8)
    FX.circle(m, a, name="mark", R=144, n=24, mats=("ice_dark", "glow"), t_in=0.2, t_hold=1.4, t_end=1.8, turns=0.2)
    return m


def nova():
    m = M("yt_fx_nova", 815)
    a = m.anim("play", 1.1, "once")
    FX.wave(m, a, prefix="a", n=24, radius=112, mats=("snow", "snow_shade"), size=2.6, height=3.0, grow=2.4, t_end=0.8)
    FX.wave(m, a, prefix="b", n=16, radius=104, mats=("ice", "glow"), size=1.4, height=5.0, grow=1.8, t_end=0.9,
            spikes=True, tip="white", delay=0.1)
    return m


def blizzard():
    m = M("yt_fx_blizzard", 816)
    a = m.anim("play", 2.2, "once")
    FX.spiral(m, a, prefix="s", n=30, r0=20, r1=180, height=50, mats=("snow", "snow_shade", "white"), size=1.6, turns=1.6,
              t_end=2.2, grow=1.8)
    FX.spiral(m, a, prefix="i", n=12, r0=10, r1=140, height=30, mats=("ice", "glow"), size=1.0, turns=-1.2, t_end=2.0,
              grow=1.2)
    FX.smoke(m, a, n=8, R=30, size=7, mats=("snow", "snow_shade"), t_end=2.0, grow=1.7)
    return m


def roar():
    m = M("yt_fx_roar", 817)
    a = m.anim("play", 1.2, "once")
    for j, p in enumerate("abc"):
        FX.wave(m, a, prefix=p, n=14, radius=80, mats=("snow", "white"), size=1.8, height=1.6, grow=2.0, t_end=0.7,
                delay=0.18 * j)
    return m


def shield():
    m = M("yt_fx_shield", 818)
    a = m.anim("play", 3.0, "once")
    FX.dome(m, a, n=14, R=34, h=30, w=3.2, mat="ice", tip="glow", t_charge=2.3, t_end=3.0, burst=110)
    FX.circle(m, a, name="seal", R=40, n=18, mats=("ice_dark", "glow"), t_in=0.4, t_hold=2.4, t_end=3.0, turns=0.5)
    return m


def snow():
    m = M("yt_fx_snow", 819)
    a = m.anim("play", 1.2, "once")
    FX.smoke(m, a, n=8, R=16, size=4.5, mats=("snow", "snow_shade"), drops="ice", t_end=1.2, grow=1.5)
    FX.pillar(m, a, r=3, h=36, mat="snow", core="glow", t_peak=0.25, t_end=1.0, bits="ice", turns=1)
    return m


BUILDERS = {"yt_fx_shatter": shatter, "yt_fx_smash": smash, "yt_fx_rock": rock, "yt_fx_barrage": barrage,
            "yt_fx_nova": nova, "yt_fx_blizzard": blizzard, "yt_fx_roar": roar, "yt_fx_shield": shield,
            "yt_fx_snow": snow}
SHOTS = {"yt_fx_shatter": [0.1, 0.4, 0.7, 1.1], "yt_fx_smash": [0.1, 0.3, 0.7, 0.9], "yt_fx_rock": [0.3, 0.56, 0.75, 1.1],
         "yt_fx_barrage": [0.3, 0.6, 0.9, 1.4], "yt_fx_nova": [0.1, 0.3, 0.6, 0.85], "yt_fx_blizzard": [0.3, 0.8, 1.4, 1.9],
         "yt_fx_roar": [0.15, 0.35, 0.6, 0.9], "yt_fx_shield": [0.5, 1.5, 2.3, 2.7], "yt_fx_snow": [0.15, 0.4, 0.7, 1.0]}
VIEW = {"yt_fx_shatter": (8, 1.6, -20), "yt_fx_smash": (12, 4.0, -20), "yt_fx_rock": (30, 2.4, -20),
        "yt_fx_barrage": (40, 0.9, -20), "yt_fx_nova": (6, 1.6, -20), "yt_fx_blizzard": (16, 0.9, -20),
        "yt_fx_roar": (6, 2.0, -20), "yt_fx_shield": (14, 2.4, -20), "yt_fx_snow": (16, 3.0, -20)}

if __name__ == "__main__":
    FX.build_all(BUILDERS, YT.BLUEPRINTS, YT.PREVIEW / "efectos", SHOTS, VIEW)
