#!/usr/bin/env python3
"""
Efectos de los ataques de AZATHOTH (modelos de ModelEngine con animacion "play").

  az_fx_blink      implosion de vacio al teletransportarse y al golpear     (AZ_TeleportStrike)
  az_fx_pulse      onda de entropia de 8 bloques                            (AZ_SandPulse)
  az_fx_collapse   el suelo se deshace: grietas, esquirlas y ola (9 bl.)    (AZ_DesertCollapse)
  az_fx_gaze       ojo gigante que se abre sobre el jugador y lo fulmina    (AZ_EnderGaze)
  az_fx_storm      tormenta de vacio en espiral de 16 bloques               (AZ_Sandstorm)
  az_fx_warp       vortice que arrastra y estalla (10 bloques)              (AZ_SandWarp)
  az_fx_rift       desgarro del espacio y explosion de 12 bloques           (AZ_SandstormRift)
  az_fx_skyfall    estrellas que caen sobre los jugadores                   (AZ_Skyfall)
  az_fx_tentacles  tentaculos que salen del suelo                           (invocaciones)
  az_fx_phase      ojo cosmico y cupula de esquirlas                        (fases e intro)

Uso: python3 tools/b11_fx.py [efecto ...] [--no-preview]
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fxlib as FX  # noqa: E402
import b11_azathoth as AZ  # noqa: E402

MATS = {
    "void": ((34, 16, 54), 5), "void_dark": ((14, 8, 24), 4), "flesh": ((96, 44, 118), 8), "nebula": ((130, 60, 210), 6),
    "pink": ((220, 90, 200), 6), "glow": ((230, 80, 255), 3), "star": ((255, 240, 200), 2), "eye": ((240, 236, 220), 3),
    "pupil": ((10, 4, 16), 2), "white": ((255, 250, 255), 1), "flesh_dark": ((62, 26, 84), 7),
}
SHINE = ("glow", "star", "white", "eye")


def M(name, seed, **kw):
    m = FX.model(name, MATS, seed, shine=SHINE, **kw)
    AZ.void_decor(m)
    return m


def blink():
    m = M("az_fx_blink", 1121)
    a = m.anim("play", 1.0, "once")
    FX.smoke(m, a, n=8, R=12, size=4.0, mats=("void", "void_dark"), drops="glow", t_end=0.9, grow=1.4)
    FX.wave(m, a, n=12, radius=48, mats=("nebula", "glow"), size=1.4, height=1.6, grow=1.6, t_end=0.6, delay=0.1)
    FX.spiral(m, a, prefix="s", n=10, r0=40, r1=2, height=26, mats=("star", "glow"), size=0.8, turns=1.0, t_end=0.6, grow=0.4)
    return m


def pulse():
    m = M("az_fx_pulse", 1122)
    a = m.anim("play", 1.0, "once")
    FX.wave(m, a, prefix="a", n=22, radius=128, mats=("void", "nebula"), size=2.6, height=3, grow=2.0, t_end=0.8)
    FX.wave(m, a, prefix="b", n=14, radius=120, mats=("glow", "star"), size=1.0, height=6, grow=1.4, t_end=0.85, spikes=True,
            tip="white", delay=0.05)
    return m


def collapse():
    m = M("az_fx_collapse", 1123, px=1, atlas=512)
    a = m.anim("play", 1.5, "once")
    FX.circle(m, a, name="cracks", R=144, n=20, mats=("void_dark", "glow"), t_in=0.2, t_hold=1.2, t_end=1.5, turns=0.1)
    FX.crystals_burst(m, a, prefix="c", spec=[(30 * math.cos(k), 30 * math.sin(k), 10 + 3 * (k % 3), 2.4,
                                               ("x", 22.5) if k % 2 else ("z", -22.5)) for k in range(8)],
                      mat="void", tip="glow", t_out=0.15, t_hold=0.5, t_end=0.8, fly=40)
    FX.wave(m, a, n=24, radius=144, mats=("void", "flesh", "nebula"), size=2.8, height=4, grow=2.0, t_end=0.8, delay=0.5)
    return m


def gaze():
    m = M("az_fx_gaze", 1124)
    a = m.anim("play", 1.4, "once")
    e = m.bone("eye", (0, 56, 0), m.root)
    for j, ang in enumerate((0, 45)):
        m.cube(e, f"sclera{j}", (-9, 50, -1), (9, 62, 1), "eye", rot=("z", ang) if ang else None, pivot=(0, 56, 0))
    m.cube(e, "sclera_w", (-12, 52, -1), (12, 60, 1), "eye")
    ir = m.bone("iris", (0, 56, 0), e)
    m.cube(ir, "iris", (-4.6, 51.4, -1.6), (4.6, 60.6, 1.6), "glow", rot=("z", 45), pivot=(0, 56, 0))
    m.cube(ir, "pupil", (-1.4, 51.0, -2.0), (1.4, 61.0, 2.0), "pupil")
    for n, y0, y1 in (("lid_top", 56, 64), ("lid_bot", 48, 56)):
        lb = m.bone(n, (0, 56, 0), e)
        m.cube(lb, n, (-13, y0, -2.4), (13, y1, 2.4), "flesh", decor={"all": "veins"})
    a.scl("eye", 0, 0.3)
    a.scl("eye", 0.2, 1)
    a.scl("lid_top", 0, 1)
    a.scl("lid_bot", 0, 1)
    a.scl("lid_top", 0.25, 1)
    a.scl("lid_bot", 0.25, 1)
    a.scl("lid_top", 0.45, 1, 0.05, 1, i="linear")
    a.scl("lid_bot", 0.45, 1, 0.05, 1, i="linear")
    a.scl("lid_top", 1.0, 1, 0.05, 1)
    a.scl("lid_bot", 1.0, 1, 0.05, 1)
    a.scl("lid_top", 1.2, 1)
    a.scl("lid_bot", 1.2, 1)
    a.scl("iris", 0.45, 1)
    a.scl("iris", 0.55, 1.4)
    a.scl("iris", 0.7, 1)
    a.scl("eye", 1.2, 1)
    a.scl("eye", 1.4, 0.05)
    for k, t in enumerate((0, 0.3, 0.45)):
        a.rot("eye", t, 0, (k - 1) * 20, 0)
    a.rot("eye", 1.4, 0, 0, 0)
    FX.pillar(m, a, name="beam", r=2.5, h=50, mat="glow", core="white", t0=0.48, t_peak=0.55, t_end=0.9, turns=0)
    FX.wave(m, a, n=10, radius=40, mats=("nebula", "glow"), size=1.4, height=1.4, grow=1.6, t_end=0.5, delay=0.5)
    return m


def storm():
    m = M("az_fx_storm", 1125)
    a = m.anim("play", 2.0, "once")
    FX.spiral(m, a, prefix="s", n=30, r0=20, r1=220, height=48, mats=("void", "nebula", "star"), size=1.8, turns=1.4,
              t_end=2.0, grow=1.6)
    FX.spiral(m, a, prefix="t", n=14, r0=10, r1=180, height=30, mats=("glow", "pink"), size=1.0, turns=-1.0, t_end=1.8,
              grow=1.2)
    return m


def warp():
    m = M("az_fx_warp", 1126)
    a = m.anim("play", 1.2, "once")
    FX.spiral(m, a, prefix="s", n=22, r0=160, r1=4, height=20, mats=("void", "nebula", "star"), size=1.6, turns=1.2,
              t_end=0.45, grow=0.2)
    FX.wave(m, a, n=20, radius=160, mats=("glow", "void", "pink"), size=2.4, height=3, grow=2.0, t_end=0.7, delay=0.42)
    return m


def rift():
    m = M("az_fx_rift", 1127)
    a = m.anim("play", 1.8, "once")
    FX.portal(m, a, rx=8, ry=26, y=30, rim=("glow", "void"), core="void_dark", mote="star", length=1.1)
    FX.wave(m, a, prefix="a", n=28, radius=192, mats=("void", "nebula", "glow"), size=3.0, height=5, grow=2.4, t_end=0.8,
            delay=0.9)
    FX.wave(m, a, prefix="b", n=16, radius=180, mats=("glow", "star"), size=1.2, height=8, grow=1.4, t_end=0.8, spikes=True,
            tip="white", delay=0.95)
    return m


def skyfall():
    m = M("az_fx_skyfall", 1128)
    a = m.anim("play", 1.6, "once")
    FX.rain(m, a, n=6, radius=40, h=(6, 10), w=2.4, mat="star", tip="glow", top=150, t_window=0.6, t_end=1.6, seed=11)
    FX.circle(m, a, name="mark", R=36, n=12, mats=("nebula", "glow"), t_in=0.2, t_hold=1.2, t_end=1.6, turns=0.3)
    return m


def tentacles():
    m = M("az_fx_tentacles", 1129)
    a = m.anim("play", 1.8, "once")

    def piece(m, b, x, z, k):
        for i in range(4):
            w = 2.0 - i * 0.4
            m.cube(b, f"tt{k}_{i}", (x - w, i * 5, z - w), (x + w, i * 5 + 5.2, z + w), ("flesh", "void")[i % 2],
                   rot=("x", 22.5) if i % 2 else None, pivot=(x, i * 5, z), decor={"all": "suckers"})
        m.cube(b, f"tt{k}_tip", (x - 0.6, 20, z - 0.6), (x + 0.6, 23, z + 0.6), "glow")

    FX.rise_ring(m, a, n=6, R=36, piece=piece, t_up=0.35, t_hold=1.4, t_end=1.8, depth=26)
    FX.circle(m, a, name="seal", R=44, n=16, mats=("void_dark", "glow"), t_in=0.3, t_hold=1.4, t_end=1.8, turns=0.4)
    return m


def phase():
    m = M("az_fx_phase", 1130)
    a = m.anim("play", 2.6, "once")
    FX.dome(m, a, n=14, R=40, h=26, w=3.0, mat="void", tip="glow", t_charge=1.8, t_end=2.6, burst=140)
    rows = ["..XXXXX..", ".XoooooX.", "XooGGGooX", "XoGGPGGoX", "XooGGGooX", ".XoooooX.", "..XXXXX.."]
    FX.floating_glyph(m, a, "eye_glyph", rows, {"X": "flesh", "o": "eye", "G": "glow", "P": "pupil"}, px=2.4, y=52, t_end=2.4,
                      turns=0.5, ring="star")
    return m


BUILDERS = {"az_fx_blink": blink, "az_fx_pulse": pulse, "az_fx_collapse": collapse, "az_fx_gaze": gaze,
            "az_fx_storm": storm, "az_fx_warp": warp, "az_fx_rift": rift, "az_fx_skyfall": skyfall,
            "az_fx_tentacles": tentacles, "az_fx_phase": phase}
SHOTS = {"az_fx_blink": [0.1, 0.3, 0.5, 0.8], "az_fx_pulse": [0.1, 0.3, 0.5, 0.8], "az_fx_collapse": [0.2, 0.45, 0.7, 1.1],
         "az_fx_gaze": [0.2, 0.45, 0.6, 1.0], "az_fx_storm": [0.3, 0.8, 1.3, 1.8], "az_fx_warp": [0.1, 0.3, 0.5, 0.8],
         "az_fx_rift": [0.3, 0.7, 1.0, 1.4], "az_fx_skyfall": [0.3, 0.6, 0.9, 1.3], "az_fx_tentacles": [0.2, 0.5, 1.0, 1.6],
         "az_fx_phase": [0.4, 1.0, 1.8, 2.3]}
VIEW = {"az_fx_blink": (12, 4.0, -20), "az_fx_pulse": (6, 1.6, -20), "az_fx_collapse": (10, 1.0, -20),
        "az_fx_gaze": (36, 2.8, -20), "az_fx_storm": (16, 0.7, -20), "az_fx_warp": (10, 1.2, -20),
        "az_fx_rift": (28, 0.9, -20), "az_fx_skyfall": (40, 2.2, -20), "az_fx_tentacles": (14, 2.6, -20),
        "az_fx_phase": (30, 2.0, -20)}

if __name__ == "__main__":
    FX.build_all(BUILDERS, AZ.BLUEPRINTS, AZ.PREVIEW / "efectos", SHOTS, VIEW)
