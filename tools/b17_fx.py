#!/usr/bin/env python3
"""
Efectos de los ataques de NEZARETH (modelos de ModelEngine con animacion "play").

  nz_fx_tug        telarana en el suelo que se tensa y revienta a los 0.4 s (7 bl.)  (NZ_GroundShatter)
  nz_fx_slash      dos tajos de las garras-hoz                                   (NZ_IceSmash)
  nz_fx_cocoon     capullo de seda que cae sobre el jugador a los 0.5 s          (NZ_IceRockThrow)
  nz_fx_rain       lluvia de capullos en 9 bloques                               (NZ_IceRockBarrage)
  nz_fx_web        red que estalla desde Nezareth (7 bloques)                    (NZ_FrostNova)
  nz_fx_silkstorm  tormenta de hilos en espiral (14 bloques)                     (NZ_IntenseBlizzard)
  nz_fx_shriek     anillos del chillido                                          (NZ_Roar)
  nz_fx_shield     capullo-escudo alrededor de Nezareth (fase 3)                 (NZ_Phase3_Check)
  nz_fx_weave      hilos que bajan del cielo y capullos que se abren             (invocaciones, intro, fases)

Uso: python3 tools/b17_fx.py [efecto ...] [--no-preview]
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fxlib as FX  # noqa: E402
import b17_nezareth as NZ  # noqa: E402

MATS = {
    "silk": ((226, 224, 232), 4), "silk_dark": ((140, 136, 150), 5), "chitin": ((34, 30, 40), 5), "red": ((200, 30, 40), 4),
    "shadow": ((40, 36, 48), 5), "white": ((255, 255, 255), 1), "crack": ((60, 50, 60), 4),
}
SHINE = ("silk", "white", "red")


def M(name, seed, **kw):
    m = FX.model(name, MATS, seed, shine=SHINE, **kw)
    NZ.web_decor(m)
    return m


def web_disc(m, bone, name, R, y=0.2, t=0.5, mat="silk", rings=3):
    """Telarana tumbada: 8 radios y anillos de tramos tangentes."""
    for j, ang in enumerate((0, 45, -45)):
        m.cube(bone, f"{name}_s{j}", (-R, y, -t / 2), (R, y + 0.3, t / 2), mat, rot=("y", ang) if ang else None, pivot=(0, y, 0))
    m.cube(bone, f"{name}_s3", (-t / 2, y, -R), (t / 2, y + 0.3, R), mat)
    for k in range(1, rings + 1):
        r = R * k / rings
        n = 16
        L = math.pi * r / n * 1.1
        for i in range(n):
            a = 2 * math.pi * i / n
            x, z = r * math.cos(a), r * math.sin(a)
            th = (math.degrees(a) + 90) % 180
            th = th - 180 if th >= 90 else th
            if abs(th) <= 45:
                frm, to = (x - L, y, z - t / 2), (x + L, y + 0.3, z + t / 2)
            else:
                th = th - 90 if th > 0 else th + 90
                frm, to = (x - t / 2, y, z - L), (x + t / 2, y + 0.3, z + L)
            snap = round(th / 22.5) * 22.5
            m.cube(bone, f"{name}_r{k}_{i}", frm, to, mat, rot=("y", -snap) if snap else None, pivot=(x, y, z))


def cocoon(m, bone, name, x=0, y=0, z=0, s=1.0):
    m.cube(bone, name, (x - 4 * s, y, z - 4 * s), (x + 4 * s, y + 12 * s, z + 4 * s), "silk", decor={"all": "silk"})
    m.cube(bone, name + "45", (x - 3.4 * s, y - 1 * s, z - 3.4 * s), (x + 3.4 * s, y + 13 * s, z + 3.4 * s), "silk_dark",
           rot=("y", 45), pivot=(x, y + 6 * s, z), decor={"all": "silk"})
    m.cube(bone, name + "_tip", (x - 1.6 * s, y + 12 * s, z - 1.6 * s), (x + 1.6 * s, y + 15 * s, z + 1.6 * s), "silk",
           rot=("y", 45), pivot=(x, y + 13 * s, z))
    m.cube(bone, name + "_eye", (x - 1 * s, y + 6 * s, z - 4.3 * s), (x + 1 * s, y + 7 * s, z - 3.9 * s), "red")


def tug():
    m = M("nz_fx_tug", 1721)
    a = m.anim("play", 1.4, "once")
    b = m.bone("web", (0, 0, 0), m.root)
    web_disc(m, b, "w", 112)
    a.scl("web", 0, 0.05, 1, 0.05)
    a.scl("web", 0.25, 1.05, 1, 1.05)
    a.scl("web", 0.38, 0.8, 1, 0.8, i="linear")
    a.scl("web", 0.45, 1.2, 1, 1.2)
    a.scl("web", 1.4, 0.05, 1, 0.05)
    FX.wave(m, a, n=20, radius=112, mats=("silk", "crack"), size=2.0, height=5, grow=1.8, t_end=0.7, spikes=True, tip="white",
            delay=0.4)
    return m


def slash():
    m = M("nz_fx_slash", 1722)
    a = m.anim("play", 0.7, "once")
    FX.arc(m, a, name="a", R=24, mats=("silk", "red"), trail="silk_dark", tilt=45, y=16, z=-12, length=0.45, sweep=(-70, 30))
    FX.arc(m, a, name="b", R=24, mats=("silk", "red"), trail="silk_dark", tilt=-45, y=16, z=-12, length=0.45, sweep=(70, -30))
    return m


def cocoon_fx():
    m = M("nz_fx_cocoon", 1723)
    a = m.anim("play", 1.6, "once")
    b = m.bone("pod", (0, 0, 0), m.root)
    cocoon(m, b, "pod", s=1.1)
    thread = m.bone("thread", (0, 0, 0), m.root)
    m.cube(thread, "thread", (-0.25, 14, -0.25), (0.25, 100, 0.25), "silk")
    a.pos("pod", 0, 0, 90, 0)
    a.pos("pod", 0.5, 0, 0, 0, i="linear")
    a.scl("pod", 0.5, 1)
    a.scl("pod", 0.6, 1.25, 0.7, 1.25)
    a.scl("pod", 0.75, 1)
    a.scl("pod", 1.3, 1)
    a.scl("pod", 1.6, 0.05)
    a.scl("thread", 0, 1, 0.05, 1)
    a.scl("thread", 0.5, 1)
    a.scl("thread", 0.8, 0.05)
    FX.wave(m, a, n=12, radius=48, mats=("silk", "silk_dark"), size=1.6, height=2, grow=1.6, t_end=0.6, delay=0.5)
    return m


def rain():
    m = M("nz_fx_rain", 1724)
    a = m.anim("play", 1.8, "once")
    import random
    rng = random.Random(17)
    for i in range(8):
        r = rng.uniform(16, 140)
        th = rng.uniform(0, 6.28)
        x, z = r * math.cos(th), r * math.sin(th)
        n = f"pod{i}"
        b = m.bone(n, (x, 0, z), m.root)
        cocoon(m, b, n, x, 0, z, 0.8)
        d = rng.uniform(0.0, 0.3)
        a.pos(n, 0, 0, 120, 0)
        a.pos(n, d, 0, 120, 0)
        a.pos(n, d + 0.3, 0, 0, 0, i="linear")
        a.scl(n, d + 0.3, 1)
        a.scl(n, d + 0.4, 1.3, 0.6, 1.3)
        a.scl(n, 1.4, 1)
        a.scl(n, 1.8, 0.05)
    web = m.bone("web", (0, 0, 0), m.root)
    web_disc(m, web, "w", 144, mat="silk_dark")
    a.scl("web", 0, 0.05, 1, 0.05)
    a.scl("web", 0.3, 1)
    a.scl("web", 1.5, 1)
    a.scl("web", 1.8, 0.05, 1, 0.05)
    return m


def web():
    m = M("nz_fx_web", 1725)
    a = m.anim("play", 1.1, "once")
    b = m.bone("web", (0, 1, 0), m.root)
    web_disc(m, b, "w", 112, y=1.2, rings=4)
    a.scl("web", 0, 0.05, 1, 0.05)
    a.scl("web", 0.25, 1.1, 1, 1.1, i="linear")
    a.scl("web", 0.8, 1)
    a.scl("web", 1.1, 0.05, 1, 0.05)
    FX.wave(m, a, n=16, radius=112, mats=("silk", "red"), size=1.2, height=4, grow=1.4, t_end=0.6, spikes=True, tip="white")
    return m


def silkstorm():
    m = M("nz_fx_silkstorm", 1726)
    a = m.anim("play", 2.2, "once")
    FX.spiral(m, a, prefix="s", n=30, r0=20, r1=220, height=50, mats=("silk", "silk_dark", "white"), size=1.4, turns=1.6,
              t_end=2.2, grow=1.6)
    FX.smoke(m, a, n=8, R=30, size=7, mats=("silk", "shadow"), t_end=2.0, grow=1.6)
    return m


def shriek():
    m = M("nz_fx_shriek", 1727)
    a = m.anim("play", 1.2, "once")
    for j, p in enumerate("abc"):
        FX.wave(m, a, prefix=p, n=14, radius=80, mats=("shadow", "red"), size=1.8, height=1.6, grow=2.0, t_end=0.7, delay=0.18 * j)
    return m


def shield():
    m = M("nz_fx_shield", 1728)
    a = m.anim("play", 3.0, "once")
    FX.dome(m, a, n=16, R=34, h=34, w=3.0, mat="silk", tip="silk_dark", t_charge=2.4, t_end=3.0, burst=100)
    b = m.bone("web", (0, 0, 0), m.root)
    web_disc(m, b, "w", 48)
    a.scl("web", 0, 0.05, 1, 0.05)
    a.scl("web", 0.4, 1)
    a.scl("web", 2.6, 1)
    a.scl("web", 3.0, 0.05, 1, 0.05)
    return m


def weave():
    m = M("nz_fx_weave", 1729)
    a = m.anim("play", 2.0, "once")

    def piece(m, b, x, z, k):
        cocoon(m, b, f"c{k}", x, 0, z, 0.7)
        m.cube(b, f"t{k}", (x - 0.2, 10, z - 0.2), (x + 0.2, 70, z + 0.2), "silk")

    FX.rise_ring(m, a, n=5, R=36, piece=piece, t_up=0.4, t_hold=1.5, t_end=2.0, depth=-60, face_out=False)
    b = m.bone("web", (0, 0, 0), m.root)
    web_disc(m, b, "w", 52, mat="silk_dark")
    a.scl("web", 0, 0.05, 1, 0.05)
    a.scl("web", 0.4, 1)
    a.scl("web", 1.7, 1)
    a.scl("web", 2.0, 0.05, 1, 0.05)
    return m


BUILDERS = {"nz_fx_tug": tug, "nz_fx_slash": slash, "nz_fx_cocoon": cocoon_fx, "nz_fx_rain": rain, "nz_fx_web": web,
            "nz_fx_silkstorm": silkstorm, "nz_fx_shriek": shriek, "nz_fx_shield": shield, "nz_fx_weave": weave}
SHOTS = {"nz_fx_tug": [0.2, 0.38, 0.5, 0.9], "nz_fx_slash": [0.05, 0.12, 0.25, 0.4], "nz_fx_cocoon": [0.3, 0.55, 0.8, 1.3],
         "nz_fx_rain": [0.2, 0.45, 0.8, 1.4], "nz_fx_web": [0.1, 0.25, 0.5, 0.9], "nz_fx_silkstorm": [0.3, 0.8, 1.4, 1.9],
         "nz_fx_shriek": [0.15, 0.35, 0.6, 0.9], "nz_fx_shield": [0.5, 1.5, 2.3, 2.7], "nz_fx_weave": [0.2, 0.5, 1.2, 1.8]}
VIEW = {"nz_fx_tug": (6, 1.4, -20), "nz_fx_slash": (16, 4.0, -20), "nz_fx_cocoon": (30, 2.4, -20),
        "nz_fx_rain": (30, 1.0, -20), "nz_fx_web": (6, 1.4, -20), "nz_fx_silkstorm": (16, 0.7, -20),
        "nz_fx_shriek": (6, 2.0, -20), "nz_fx_shield": (16, 2.2, -20), "nz_fx_weave": (24, 1.8, -20)}

if __name__ == "__main__":
    FX.build_all(BUILDERS, NZ.BLUEPRINTS, NZ.PREVIEW / "efectos", SHOTS, VIEW)
