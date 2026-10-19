#!/usr/bin/env python3
"""
Efectos de los ataques de LEVIATAN (modelos de ModelEngine con animacion "play").

  lv_fx_curse      remolino de agua y almas que sube por el jugador        (LV_SpiritCurse)
  lv_fx_splash     geiser y salpicadura al saltar y al caer                (LV_ShadowStep)
  lv_fx_whirlpool  remolino de 7 bloques que arrastra al fondo             (LV_SakuraHex)
  lv_fx_ink        nube de tinta del abismo                                (LV_ShadowVeil)
  lv_fx_tsunami    ola gigante de 8 bloques con pinchos de agua            (LV_SpiritNova)
  lv_fx_coral      corales que brotan del suelo en anillo                  (invocaciones)
  lv_fx_phase      columna de agua y cupula de coral que estalla           (fases e intro)

Uso: python3 tools/b12_fx.py [efecto ...] [--no-preview]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fxlib as FX  # noqa: E402
import b12_leviatan as LV  # noqa: E402

MATS = {
    "water": ((60, 160, 220), 5), "water_dark": ((30, 90, 160), 5), "foam": ((230, 250, 255), 2), "glow": ((90, 255, 230), 3),
    "ink": ((14, 20, 40), 4), "ink2": ((30, 40, 70), 5), "coral": ((230, 90, 110), 7), "coral_dark": ((150, 50, 80), 6),
    "pearl": ((240, 240, 255), 3), "soul": ((150, 240, 230), 4), "white": ((255, 255, 255), 1),
}
SHINE = ("water", "glow", "foam", "white", "pearl")


def M(name, seed, **kw):
    m = FX.model(name, MATS, seed, shine=SHINE, **kw)
    LV.sea_decor(m)
    return m


def curse():
    m = M("lv_fx_curse", 1221)
    a = m.anim("play", 1.4, "once")
    FX.spiral(m, a, prefix="s", n=18, r0=26, r1=4, height=44, mats=("water", "foam", "soul"), size=1.4, turns=1.5,
              t_end=1.3, grow=0.6)
    FX.circle(m, a, name="ring", R=24, n=12, mats=("water_dark", "glow"), t_in=0.2, t_hold=1.0, t_end=1.4, turns=-0.6)
    return m


def splash():
    m = M("lv_fx_splash", 1222)
    a = m.anim("play", 1.1, "once")
    FX.pillar(m, a, r=4, h=40, mat="water", core="foam", t_peak=0.15, t_end=0.8, bits="foam", turns=0.5)
    FX.wave(m, a, n=14, radius=56, mats=("water", "foam"), size=1.8, height=3, grow=1.8, t_end=0.7, spikes=True, tip="white")
    return m


def whirlpool():
    m = M("lv_fx_whirlpool", 1223, px=1, atlas=512)
    a = m.anim("play", 1.6, "once")
    FX.spiral(m, a, prefix="a", n=24, r0=112, r1=6, height=6, mats=("water", "water_dark", "foam"), size=2.2, turns=1.6,
              t_end=1.4, grow=0.4)
    FX.circle(m, a, name="eddy", R=112, n=24, mats=("water_dark", "foam"), t_in=0.2, t_hold=1.3, t_end=1.6, turns=-1.2)
    FX.circle(m, a, name="eddy2", R=60, n=14, mats=("water", "glow"), t_in=0.25, t_hold=1.3, t_end=1.6, turns=1.5)
    return m


def ink():
    m = M("lv_fx_ink", 1224)
    a = m.anim("play", 1.6, "once")
    FX.smoke(m, a, n=10, R=20, size=6, mats=("ink", "ink2"), drops="glow", t_end=1.6, grow=1.6)
    return m


def tsunami():
    m = M("lv_fx_tsunami", 1225)
    a = m.anim("play", 1.3, "once")
    FX.wave(m, a, prefix="w", n=26, radius=128, mats=("water", "water_dark"), size=3.0, height=9, grow=2.0, t_end=0.9,
            tip="foam")
    FX.wave(m, a, prefix="s", n=16, radius=120, mats=("glow", "foam"), size=1.2, height=7, grow=1.4, t_end=0.95, spikes=True,
            tip="white", delay=0.08)
    FX.pillar(m, a, r=5, h=50, mat="water", core="glow", t_peak=0.2, t_end=0.9, bits="foam", turns=1)
    return m


def coral():
    m = M("lv_fx_coral", 1226)
    a = m.anim("play", 1.8, "once")

    def piece(m, b, x, z, k):
        LV.coral_branch(m, b, f"cb{k}", x, 0, z, 12 + (k % 3) * 3, 1.2, 1 if k % 2 else -1)

    FX.rise_ring(m, a, n=7, R=40, piece=piece, t_up=0.35, t_hold=1.4, t_end=1.8, depth=22)
    FX.wave(m, a, n=12, radius=48, mats=("water", "foam"), size=1.6, height=2, grow=1.6, t_end=0.6)
    return m


def phase():
    m = M("lv_fx_phase", 1227)
    a = m.anim("play", 2.4, "once")
    FX.pillar(m, a, r=7, h=64, mat="water", core="glow", t_peak=0.4, t_end=1.6, bits="pearl", turns=-1)
    FX.dome(m, a, n=12, R=44, h=26, w=3.0, mat="coral", tip="pearl", t_charge=1.7, t_end=2.4, burst=140)
    return m


BUILDERS = {"lv_fx_curse": curse, "lv_fx_splash": splash, "lv_fx_whirlpool": whirlpool, "lv_fx_ink": ink,
            "lv_fx_tsunami": tsunami, "lv_fx_coral": coral, "lv_fx_phase": phase}
SHOTS = {"lv_fx_curse": [0.2, 0.6, 1.0, 1.3], "lv_fx_splash": [0.05, 0.15, 0.4, 0.7],
         "lv_fx_whirlpool": [0.2, 0.6, 1.0, 1.4], "lv_fx_ink": [0.2, 0.6, 1.0, 1.4], "lv_fx_tsunami": [0.1, 0.3, 0.6, 0.9],
         "lv_fx_coral": [0.2, 0.5, 1.0, 1.6], "lv_fx_phase": [0.3, 0.9, 1.6, 2.1]}
VIEW = {"lv_fx_curse": (22, 3.0, -20), "lv_fx_splash": (16, 3.0, -20), "lv_fx_whirlpool": (6, 1.3, -20),
        "lv_fx_ink": (12, 3.0, -20), "lv_fx_tsunami": (14, 1.3, -20), "lv_fx_coral": (12, 2.6, -20),
        "lv_fx_phase": (26, 1.6, -20)}

if __name__ == "__main__":
    FX.build_all(BUILDERS, LV.BLUEPRINTS, LV.PREVIEW / "efectos", SHOTS, VIEW)
