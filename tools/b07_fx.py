#!/usr/bin/env python3
"""
Efectos de los ataques de LADY OF LAMENTS (modelos de ModelEngine con animacion "play").

  ll_fx_wail     ondas de sonido moradas que se expanden 7 bloques        (LL_Wail, LL_EchoOfGrief)
  ll_fx_shroud   cupula de oscuridad alrededor de la reina                (LL_ShroudOfNight)
  ll_fx_siphon   almas que suben en espiral desde el jugador              (LL_SpiritSiphon, TormentedSpirit)
  ll_fx_mark     circulo de amatistas que estalla bajo el marcado         (LL_GriefMark)
  ll_fx_sorrow   anillo de pinchos de amatista                            (LL_SharedSorrow)
  ll_fx_lament   lamento masivo: grito que sube y ola de 12 bloques       (LL_MassLament)
  ll_fx_storm    rayos de amatista que caen del cielo                     (LL_StormOfSorrow)
  ll_fx_mirror   espejo espectral que se abre                             (invocaciones y fases)

Uso: python3 tools/b07_fx.py [efecto ...] [--no-preview]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fxlib as FX  # noqa: E402
import b07_lady as LL  # noqa: E402

MATS = {
    "amethyst": ((170, 100, 230), 6), "amethyst_dark": ((100, 50, 160), 6), "glow": ((226, 150, 255), 3),
    "spectral": ((200, 180, 240), 5), "dark": ((30, 14, 42), 4), "smoke": ((50, 30, 64), 5), "white": ((250, 240, 255), 2),
    "black": ((18, 14, 22), 3),
}
SHINE = ("amethyst", "glow", "white")


def M(name, seed):
    return FX.model(name, MATS, seed, shine=SHINE)


def wail():
    m = M("ll_fx_wail", 801)
    a = m.anim("play", 1.3, "once")
    for j, p in enumerate("abc"):
        FX.wave(m, a, prefix=p, n=16, radius=112, mats=("amethyst", "glow"), size=2.2, height=2.0, grow=2.4, t_end=0.9,
                delay=0.15 * j)
    return m


def shroud():
    m = M("ll_fx_shroud", 802)
    a = m.anim("play", 1.4, "once")
    FX.smoke(m, a, n=10, R=34, size=8, mats=("dark", "smoke"), drops="glow", t_end=1.4, grow=1.6)
    return m


def siphon():
    m = M("ll_fx_siphon", 803)
    a = m.anim("play", 1.4, "once")
    FX.spiral(m, a, n=18, r0=40, r1=3, height=46, mats=("glow", "spectral", "white"), size=1.3, turns=1.3, t_end=1.4,
              grow=0.6)
    return m


def mark():
    m = M("ll_fx_mark", 804)
    a = m.anim("play", 1.8, "once")

    def shard(m, b, x, z, k):
        m.cube(b, f"sh{k}", (x - 1.2, 0, z - 1.2), (x + 1.2, 6, z + 1.2), "amethyst", decor={"all": "crystal"})

    FX.circle(m, a, R=56, n=20, mats=("glow", "amethyst"), t_in=0.3, t_hold=1.3, t_end=1.8, turns=0.4, items=shard)
    FX.crystals_burst(m, a, spec=[(0, 0, 22, 4.0, None), (-8, 6, 14, 3.0, ("z", 22.5)), (8, 6, 15, 3.0, ("z", -22.5)),
                                  (0, -9, 13, 2.8, ("x", -22.5)), (0, 10, 12, 2.6, ("x", 22.5))],
                      mat="amethyst", tip="glow", t_out=1.15, t_hold=1.5, t_end=1.8, fly=24)
    return m


def sorrow():
    m = M("ll_fx_sorrow", 805)
    a = m.anim("play", 1.0, "once")
    FX.wave(m, a, n=20, radius=80, mats=("amethyst", "amethyst_dark"), size=2.0, height=6, grow=2.2, t_end=1.0,
            spikes=True, tip="glow")
    return m


def lament():
    m = M("ll_fx_lament", 806)
    a = m.anim("play", 1.6, "once")
    FX.pillar(m, a, r=5, h=60, mat="spectral", core="glow", t_peak=0.6, t_end=1.4, bits="amethyst", turns=1.5)
    FX.wave(m, a, n=30, radius=192, mats=("spectral", "amethyst", "glow"), size=3.0, height=5, grow=2.8, t_end=1.0,
            delay=0.55)
    return m


def storm():
    m = M("ll_fx_storm", 807)
    a = m.anim("play", 1.8, "once")
    FX.rain(m, a, n=14, radius=160, h=(30, 44), w=1.6, mat="glow", tip="white", top=140, t_window=0.9, t_end=1.8)
    return m


def mirror():
    m = M("ll_fx_mirror", 808)
    a = m.anim("play", 1.6, "once")
    FX.portal(m, a, rx=11, ry=17, y=22, rim=("black", "amethyst"), core="spectral", mote="glow", length=1.6)
    return m


BUILDERS = {"ll_fx_wail": wail, "ll_fx_shroud": shroud, "ll_fx_siphon": siphon, "ll_fx_mark": mark,
            "ll_fx_sorrow": sorrow, "ll_fx_lament": lament, "ll_fx_storm": storm, "ll_fx_mirror": mirror}
SHOTS = {"ll_fx_wail": [0.1, 0.3, 0.6, 0.9], "ll_fx_shroud": [0.2, 0.5, 0.9, 1.2], "ll_fx_siphon": [0.2, 0.6, 1.0, 1.3],
         "ll_fx_mark": [0.4, 1.0, 1.25, 1.6], "ll_fx_sorrow": [0.05, 0.2, 0.5, 0.9], "ll_fx_lament": [0.3, 0.6, 0.9, 1.3],
         "ll_fx_storm": [0.3, 0.6, 0.9, 1.4], "ll_fx_mirror": [0.2, 0.5, 1.0, 1.5]}
VIEW = {"ll_fx_wail": (6, 1.2, -20), "ll_fx_shroud": (10, 3.0, -20), "ll_fx_siphon": (20, 3.0, -20),
        "ll_fx_mark": (10, 2.0, -20), "ll_fx_sorrow": (8, 1.6, -20), "ll_fx_lament": (20, 0.8, -20),
        "ll_fx_storm": (40, 0.9, -20), "ll_fx_mirror": (22, 6.0, -25)}

if __name__ == "__main__":
    FX.build_all(BUILDERS, LL.BLUEPRINTS, LL.PREVIEW / "efectos", SHOTS, VIEW)
