#!/usr/bin/env python3
"""
Efectos de los ataques de KRONOS (modelos de ModelEngine con animacion "play").

  kr_fx_slam       grieta y anillo de cristales de tiempo de 5 bloques           (KR_Slam)
  kr_fx_quake      esfera de reloj gigante en el suelo y ola de pinchos (8 bl.)  (KR_Quake)
  kr_fx_roar       reloj fantasma que sube y gira hacia atras con arena          (KR_RugidoDelTiempo)
  kr_fx_charge     tajo en media luna de la guadana                              (KR_Charge)
  kr_fx_hourglass  reloj de arena que cae sobre el que huye                      (KR_AntiRun)
  kr_fx_phase      engranajes que salen del suelo y aro de reloj                 (fases e intro)
  kr_fx_rift       grieta en el tiempo de la que salen los subditos              (invocaciones)
  kr_fx_sand       columna de arena y ola del ultimo aliento                     (KR_LastBreath)

Uso: python3 tools/b10_fx.py [efecto ...] [--no-preview]
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fxlib as FX  # noqa: E402
import b10_kronos as KR  # noqa: E402

MATS = {
    "gold": ((214, 170, 64), 6), "gold_dark": ((150, 110, 40), 6), "glow": ((214, 140, 255), 3),
    "violet": ((120, 60, 190), 6), "violet_dark": ((60, 26, 100), 5), "sand": ((236, 200, 120), 6),
    "sand_dark": ((190, 150, 80), 6), "glass": ((200, 226, 255), 3), "dial": ((240, 230, 200), 3),
    "white": ((255, 250, 240), 1), "black": ((22, 16, 30), 3),
}
SHINE = ("gold", "glow", "glass", "white")


def M(name, seed, **kw):
    m = FX.model(name, MATS, seed, shine=SHINE, **kw)
    KR.time_decor(m)
    return m


def clock_face(m, a, name, R, t_in, t_hold, t_end, spin=-1.0, y=0.2, ticks="gold", rim="gold_dark", hands="glow"):
    """Esfera de reloj tumbada en el suelo: aro, 12 marcas y dos manecillas que giran."""
    b = m.bone(name, (0, y, 0), m.root)
    n = 24
    for k in range(n):
        th = 2 * math.pi * k / n
        x, z = R * math.cos(th), R * math.sin(th)
        L = math.pi * R / n * 1.1
        rot = ("y", 45) if k % 2 else None
        m.cube(b, f"{name}r{k}", (x - L * 0.6, y, z - L * 0.6), (x + L * 0.6, y + 0.4, z + L * 0.6), rim, rot=rot,
               pivot=(x, y, z))
    for k in range(12):
        th = 2 * math.pi * k / 12
        x, z = R * 0.82 * math.cos(th), R * 0.82 * math.sin(th)
        big = k % 3 == 0
        s = R * (0.07 if big else 0.04)
        m.cube(b, f"{name}t{k}", (x - s, y, z - s), (x + s, y + (2.5 if big else 1.2), z + s), ticks if not big else "glow")
    for hn, ln, w in (("long", R * 0.75, R * 0.04), ("short", R * 0.5, R * 0.06)):
        h = m.bone(f"{name}_{hn}", (0, y, 0), b)
        m.cube(h, f"{name}_{hn}", (-w, y, -ln), (w, y + 0.8, 0), hands)
        m.cube(h, f"{name}_{hn}_tip", (-w * 2, y, -ln - w * 2), (w * 2, y + 0.8, -ln + w * 2), hands, rot=("y", 45),
               pivot=(0, y, -ln))
        FX.spin(a, f"{name}_{hn}", t_end, spin * (1 if hn == "long" else 1 / 12))
    m.cube(b, f"{name}_hub", (-R * 0.08, y, -R * 0.08), (R * 0.08, y + 1.2, R * 0.08), "white")
    a.scl(name, 0, 0.05, 1, 0.05)
    a.scl(name, t_in, 1.08, 1, 1.08)
    a.scl(name, t_in + 0.1, 1)
    a.scl(name, t_hold, 1)
    a.scl(name, t_end, 0.05, 1, 0.05)
    return b


def slam():
    m = M("kr_fx_slam", 1021)
    a = m.anim("play", 1.0, "once")
    FX.circle(m, a, name="crack", R=60, n=14, mats=("violet_dark", "violet"), t_in=0.1, t_hold=0.7, t_end=1.0, turns=0,
              grow=1.4)
    FX.wave(m, a, n=16, radius=80, mats=("violet", "glow"), size=1.8, height=5, grow=1.8, t_end=0.7, spikes=True, tip="white")
    return m


def quake():
    m = M("kr_fx_quake", 1022)
    a = m.anim("play", 1.4, "once")
    clock_face(m, a, "dial", 128, 0.25, 1.0, 1.4, spin=2.0)
    FX.wave(m, a, n=24, radius=128, mats=("violet", "gold"), size=2.4, height=7, grow=1.9, t_end=0.8, spikes=True,
            tip="glow", delay=0.3)
    return m


def roar():
    m = M("kr_fx_roar", 1023)
    a = m.anim("play", 1.8, "once")
    b = m.bone("ghost", (0, 30, 0), m.root)
    import b10_kronos
    b10_kronos.ring(m, b, "ring", 0, 30, -0.4, 0.4, 22, "glow", n=16, t=1.4)
    for k in range(12):
        th = 2 * math.pi * k / 12
        x, y = 18 * math.cos(th), 30 + 18 * math.sin(th)
        s = 1.6 if k % 3 == 0 else 0.9
        m.cube(b, f"num{k}", (x - s, y - s, -0.5), (x + s, y + s, 0.5), "gold" if k % 3 else "white", rot=("z", 45),
               pivot=(x, y, 0))
    for hn, ln, w in (("hl", 16, 0.6), ("hs", 10, 0.9)):
        h = m.bone(hn, (0, 30, 0), b)
        m.cube(h, hn, (-w, 30, -0.6), (w, 30 + ln, 0.6), "gold")
        FX.spin(a, hn, 1.8, 2.0 if hn == "hl" else 0.5, "z")
    a.scl("ghost", 0, 0.05)
    a.scl("ghost", 0.3, 1.1)
    a.scl("ghost", 0.45, 1)
    a.scl("ghost", 1.4, 1.15)
    a.scl("ghost", 1.8, 0.05)
    a.pos("ghost", 0, 0, -20, 0)
    a.pos("ghost", 0.4, 0, 0, 0)
    a.pos("ghost", 1.8, 0, 14, 0)
    for k in range(9):
        a.rot("ghost", 1.8 * k / 8, 0, 45 * k, 0, i="linear")
    FX.spiral(m, a, prefix="s", n=20, r0=10, r1=110, height=40, mats=("sand", "sand_dark", "glow"), size=1.2, turns=-1.2,
              t_end=1.7, grow=1.4)
    return m


def charge():
    m = M("kr_fx_charge", 1024)
    a = m.anim("play", 0.6, "once")
    FX.arc(m, a, name="arc", R=40, mats=("glow", "violet"), trail="gold", tilt=10, y=16, z=-16, length=0.5, sweep=(-80, 40))
    FX.wave(m, a, n=10, radius=56, mats=("violet", "sand"), size=1.6, height=2, grow=1.6, t_end=0.5, delay=0.05)
    return m


def hourglass_fx():
    m = M("kr_fx_hourglass", 1025)
    a = m.anim("play", 2.0, "once")
    b = m.bone("hg", (0, 40, 0), m.root)
    s = 3.0
    m.cube(b, "top", (-4.5 * s / 3 * 2, 52, -3 * s / 1.5), (4.5 * s / 3 * 2, 54, 3 * s / 1.5), "gold")
    m.cube(b, "bot", (-4.5 * s / 3 * 2, 28, -3 * s / 1.5), (4.5 * s / 3 * 2, 30, 3 * s / 1.5), "gold")
    tiers = [(30, 34, 5.4), (34, 38, 4.0), (38, 41, 2.2)]
    tiers += [(82 - y1, 82 - y0, w) for y0, y1, w in tiers]
    sand_t = m.bone("sand_top", (0, 41, 0), b)
    sand_b = m.bone("sand_bot", (0, 30, 0), b)
    for k, (y0, y1, w) in enumerate(tiers):
        for j, ang in enumerate((0, 45)):
            rot = ("y", ang) if ang else None
            m.cube(b, f"g{k}{j}", (-w, y0, -w), (w, y1, w), "glass", rot=rot, pivot=(0, 40, 0))
            sb = sand_b if k < 3 else sand_t
            m.cube(sb, f"s{k}{j}", (-w - 0.2, y0 - 0.1, -w - 0.2), (w + 0.2, y1 + 0.1, w + 0.2),
                   "sand_dark" if k < 3 else "sand", rot=rot, pivot=(0, 40, 0))
    for sx in (1, -1):
        for sz in (1, -1):
            m.cube(b, f"post{sx}{sz}", (5.8 * sx - 0.6, 30, 5.8 * sz - 0.6), (5.8 * sx + 0.6, 52, 5.8 * sz + 0.6), "gold_dark")
    stream = m.bone("stream", (0, 41, 0), b)
    m.cube(stream, "stream", (-0.5, 30, -0.5), (0.5, 41, 0.5), "sand")
    a.pos("hg", 0, 0, 40, 0)
    a.pos("hg", 0.4, 0, -2, 0, i="linear")
    a.pos("hg", 0.5, 0, 0, 0)
    a.scl("hg", 0, 0.6)
    a.scl("hg", 0.4, 1)
    a.scl("hg", 1.6, 1)
    a.scl("hg", 2.0, 0.05)
    a.scl("sand_top", 0.4, 1)
    a.scl("sand_top", 1.6, 1, 0.05, 1, i="linear")
    a.scl("sand_bot", 0.4, 1, 0.05, 1)
    a.scl("sand_bot", 1.6, 1, i="linear")
    a.scl("stream", 0.4, 1)
    a.scl("stream", 1.6, 1)
    a.scl("stream", 1.7, 0.05)
    FX.wave(m, a, n=10, radius=40, mats=("sand", "gold"), size=1.4, height=1.6, grow=1.4, t_end=0.5, delay=0.42)
    return m


def phase():
    m = M("kr_fx_phase", 1026)
    a = m.anim("play", 2.2, "once")

    def piece(m, b, x, z, k):
        r = 9 if k % 2 else 7
        cx, cy = x, r + 1
        import b10_kronos
        b10_kronos.gear(m, b, f"gear{k}", cx, cy, z - 0.8, z + 0.8, r, mat="gold" if k % 2 else "gold_dark", teeth=8)

    FX.rise_ring(m, a, n=6, R=56, piece=piece, t_up=0.35, t_hold=1.8, t_end=2.2, depth=30)
    clock_face(m, a, "dial", 72, 0.3, 1.8, 2.2, spin=-3.0)
    FX.pillar(m, a, r=5, h=60, mat="violet", core="glow", t0=0.2, t_peak=0.5, t_end=1.6, bits="gold", turns=-1)
    return m


def rift():
    m = M("kr_fx_rift", 1027)
    a = m.anim("play", 1.6, "once")
    FX.portal(m, a, rx=12, ry=18, y=22, rim=("gold", "violet"), core="violet_dark", mote="glow", length=1.6)
    FX.smoke(m, a, n=6, R=16, size=2.0, mats=("violet", "sand"), t_end=1.4, grow=1.0)
    return m


def sand():
    m = M("kr_fx_sand", 1028)
    a = m.anim("play", 1.6, "once")
    FX.pillar(m, a, r=6, h=56, mat="sand", core="glow", t_peak=0.25, t_end=1.3, bits="gold", turns=1.5)
    FX.wave(m, a, n=20, radius=96, mats=("sand", "sand_dark", "gold"), size=2.6, height=3, grow=2.2, t_end=0.9, delay=0.1)
    return m


BUILDERS = {"kr_fx_slam": slam, "kr_fx_quake": quake, "kr_fx_roar": roar, "kr_fx_charge": charge,
            "kr_fx_hourglass": hourglass_fx, "kr_fx_phase": phase, "kr_fx_rift": rift, "kr_fx_sand": sand}
SHOTS = {"kr_fx_slam": [0.05, 0.2, 0.5, 0.8], "kr_fx_quake": [0.2, 0.4, 0.7, 1.1], "kr_fx_roar": [0.3, 0.7, 1.2, 1.6],
         "kr_fx_charge": [0.05, 0.15, 0.3, 0.45], "kr_fx_hourglass": [0.3, 0.6, 1.2, 1.8], "kr_fx_phase": [0.3, 0.8, 1.4, 2.0],
         "kr_fx_rift": [0.2, 0.5, 1.0, 1.4], "kr_fx_sand": [0.15, 0.4, 0.8, 1.2]}
VIEW = {"kr_fx_slam": (6, 2.0, -20), "kr_fx_quake": (8, 1.0, -20), "kr_fx_roar": (30, 1.6, -20),
        "kr_fx_charge": (14, 2.6, -20), "kr_fx_hourglass": (40, 2.6, -20), "kr_fx_phase": (20, 1.6, -20),
        "kr_fx_rift": (22, 5.0, -25), "kr_fx_sand": (20, 1.4, -20)}

if __name__ == "__main__":
    FX.build_all(BUILDERS, KR.BLUEPRINTS, KR.PREVIEW / "efectos", SHOTS, VIEW)
