#!/usr/bin/env python3
"""
Sonidos propios de RED HAND y sus subditos (sintetizados): campana de castillo, organo,
coro grave, armadura, mandoble, sangre, cadenas y almas en pena.

  Modelos/DextraBossesPack/assets/dextra/sounds/red_hand/*.ogg  ->  dextra:red_hand.<nombre>
  Demo: Modelos/04_RedHand/preview/sonidos_demo.mp3

Uso: python3 tools/b04_sounds.py
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import dextra_pack as DP  # noqa: E402
from generate_sounds import (AA, OO, SR, UH, bandpass, crack, curve, debris, env, finish, growl,  # noqa: E402
                             highpass, lowpass, mixdown, noise, osc_saw, reverb, rumble, thump, to_ogg,
                             whoosh, write_wav)
from b03_sounds import bell, wail  # noqa: E402

BOSS = "red_hand"
DEMO = Path(__file__).resolve().parent.parent / "Modelos/04_RedHand/preview/sonidos_demo.mp3"
RNG = np.random.default_rng(404)


def T(dur):
    return np.arange(int(dur * SR)) / SR


def organ(dur, notes, attack=0.08):
    """Organo de iglesia: sierras con registros de octava y quinta."""
    n = int(dur * SR)
    out = np.zeros(n)
    for hz in notes:
        for mult, amp in ((0.5, 0.6), (1, 1.0), (1.5, 0.35), (2, 0.5), (4, 0.2)):
            out += amp * osc_saw(np.full(n, hz * mult * (1 + RNG.uniform(-0.002, 0.002))))
    out = lowpass(out, 3200, 2)
    return out / (np.abs(out).max() + 1e-9) * env(n, attack, dur, 1.4, hold=dur * 0.6)


def clank(dur=0.6, base=900):
    """Placa de armadura que choca."""
    t = T(dur)
    ring = sum(np.sin(2 * np.pi * base * r * t) * np.exp(-t * d) for r, d in ((1, 10), (1.63, 14), (2.41, 18), (3.7, 25)))
    return mixdown((0, 0.5 * ring), (0, 0.5 * crack(0.08)))


def stomp():
    return mixdown((0, thump(0.7, 90, 38)), (0, 0.4 * clank(0.5, 420)))


def splat(dur=0.5):
    """Sangre salpicando: ruido grave con burbujas."""
    n = int(dur * SR)
    x = lowpass(noise(dur), 1400) * env(n, 0.005, dur, 3)
    bub = np.zeros(n)
    for k in range(10):
        i = int(RNG.uniform(0, dur * 0.7) * SR)
        f = RNG.uniform(250, 700)
        L = int(0.05 * SR)
        tt = np.arange(min(L, n - i)) / SR
        bub[i:i + len(tt)] += np.sin(2 * np.pi * f * (1 + 6 * tt) * tt) * np.exp(-tt * 60)
    return mixdown((0, x), (0, 0.5 * bub))


def heavy_swing(dur=0.5):
    return mixdown((0, whoosh(dur, 120, 1800)), (dur * 0.6, 0.3 * clank(0.4, 1300)))


def chains(dur=1.2, count=10):
    out = np.zeros(int(dur * SR))
    for k in range(count):
        i = int(RNG.uniform(0, dur * 0.85) * SR)
        c = clank(0.25, RNG.uniform(1800, 3200)) * RNG.uniform(0.3, 0.6)
        out[i:i + len(c)] += c[: len(out) - i]
    return out


def demon(dur, f_points, drv=3.4):
    return growl(dur, f_points, vowel=OO, drv=drv, rough=30, sub=0.9)


def heartbeat(beats=3, gap=0.75):
    return mixdown(*[(k * gap + d, a * thump(0.35, 70, 40)) for k in range(beats) for d, a in ((0, 0.9), (0.18, 0.6))])


# ---------------------------------------------------------------- boss
def rh_intro():
    s = mixdown((0, 0.9 * bell(4.5, 82.4)), (1.5, 0.9 * bell(4.5, 73.4)), (0.4, 0.5 * organ(4.0, [73.4, 87.3, 110.0])),
                (3.0, stomp()), (3.6, stomp()),
                (3.6, 0.7 * demon(1.8, [(0, 80), (0.2, 100), (1, 50)]) * env(int(1.8 * SR), 0.05, 1.8, 1.5, hold=0.6)))
    return reverb(s, 3.4, 0.3)


def rh_roar():
    g = demon(2.0, [(0, 70), (0.15, 105), (0.6, 92), (1, 55)]) * env(int(2.0 * SR), 0.05, 2.0, 1.4, hold=0.9)
    return reverb(mixdown((0, g), (0, 0.5 * thump(1.2, 90, 32))), 2.4, 0.3)


def rh_hurt():
    g = demon(0.45, [(0, 120), (0.3, 130), (1, 90)], drv=3.8) * env(int(0.45 * SR), 0.01, 0.45, 2.0, hold=0.08)
    return reverb(mixdown((0, g), (0, 0.6 * clank(0.4, 700))), 0.8, 0.15)


def rh_slash():
    return reverb(heavy_swing(0.45), 1.0, 0.18)


def rh_mark():
    s = mixdown((0, 0.9 * heartbeat(3)), (0, 0.4 * wail(2.2, [(0, 420), (0.5, 380), (1, 300)])),
                (0, 0.3 * organ(2.2, [146.8, 155.6], attack=0.4)))
    return reverb(s, 2.0, 0.3)


def rh_dash():
    n = int(0.6 * SR)
    sink = lowpass(noise(0.6), 900) * curve(n, [(0, 0), (0.4, 1), (1, 0)])
    return reverb(mixdown((0, sink), (0.1, 0.5 * whoosh(0.5, 100, 1500)), (0.35, 0.4 * splat(0.4))), 1.2, 0.25)


def rh_crush():
    s = mixdown((0, 0.6 * heavy_swing(0.5)), (0.5, thump(1.4, 120, 30)), (0.5, 0.8 * crack(0.3)),
                (0.52, 0.7 * debris(1.6, 120)), (0.5, 0.6 * splat(0.8)), (0.5, 0.6 * rumble(1.6, 18, 120)))
    return reverb(s, 2.2, 0.25)


def rh_nova():
    n = int(0.45 * SR)
    swell = bandpass(noise(0.45), 300, 3000) * curve(n, [(0, 0), (1, 1)]) ** 2
    s = mixdown((0, 0.6 * swell), (0.4, thump(1.2, 110, 34)), (0.4, splat(1.0)), (0.4, 0.5 * organ(1.6, [73.4, 77.8], 0.02)))
    return reverb(s, 2.2, 0.28)


def rh_pools():
    return reverb(mixdown((0, 0.5 * whoosh(0.3, 200, 2000)), (0.15, splat(0.6)), (0.35, 0.6 * splat(0.5))), 1.2, 0.2)


def rh_execution():
    n = int(2.0 * SR)
    rise = osc_saw(curve(n, [(0, 40), (1, 180)])) * curve(n, [(0, 0), (1, 1)]) ** 2
    rise = lowpass(rise, 1500, 2)
    s = mixdown((0, 0.5 * rise), (0, 0.5 * organ(2.0, [73.4, 103.8], 1.2)), (0, 0.6 * heartbeat(4, 0.45)),
                (2.0, 1.0 * thump(1.8, 100, 26)), (2.0, crack(0.4)), (2.0, splat(1.2)), (2.0, 0.8 * rumble(2.0, 16, 130)),
                (2.0, 0.6 * bell(3.0, 65.4)))
    return reverb(s, 3.0, 0.3)


def rh_summon():
    s = mixdown((0, 0.8 * chains(1.4, 12)), (0.2, 0.8 * bell(3.2, 98.0)), (0.6, 0.4 * wail(1.6, [(0, 300), (1, 220)])))
    return reverb(s, 2.6, 0.3)


def rh_phase():
    s = mixdown((0, 0.7 * organ(2.4, [73.4, 87.3, 103.8, 146.8], 0.03)), (1.2, stomp()),
                (1.2, 0.8 * demon(1.4, [(0, 80), (0.3, 115), (1, 70)]) * env(int(1.4 * SR), 0.03, 1.4, 1.5, hold=0.5)))
    return reverb(s, 2.8, 0.3)


def rh_death():
    g = demon(2.8, [(0, 100), (0.3, 85), (1, 38)], drv=2.6) * env(int(2.8 * SR), 0.05, 2.8, 1.8, hold=1.0)
    s = mixdown((0, g), (1.6, clank(0.8, 500)), (1.9, clank(0.8, 380)), (2.2, stomp()), (2.2, 0.8 * bell(5.0, 61.7)))
    return reverb(s, 3.4, 0.32)


# ---------------------------------------------------------------- subditos
def squire_groan():
    g = growl(1.2, [(0, 110), (0.5, 96), (1, 80)], vowel=UH, drv=2.4, breath=0.5, rough=20)
    return reverb(g * env(len(g), 0.15, 1.2, 1.5, hold=0.4), 1.2, 0.2)


def squire_hit():
    return reverb(mixdown((0, 0.6 * whoosh(0.25, 400, 3000)), (0.15, 0.6 * clank(0.4, 1600))), 0.8, 0.15)


def knight_clank():
    return reverb(mixdown((0, stomp()), (0.25, 0.5 * clank(0.4, 1100))), 1.0, 0.18)


def knight_bash():
    return reverb(mixdown((0, thump(0.5, 160, 70)), (0, 0.7 * clank(0.5, 640)), (0.2, 0.5 * whoosh(0.2, 600, 4000))), 0.9, 0.15)


def soul_wail():
    return reverb(mixdown((0, wail(1.6, [(0, 600), (0.4, 760), (1, 420)], 7)), (0, 0.4 * chains(1.4, 6))), 2.0, 0.4)


def soul_hit():
    return reverb(mixdown((0, 0.6 * wail(0.5, [(0, 900), (1, 500)], 14)), (0, 0.4 * whoosh(0.3, 800, 5000))), 1.0, 0.3)


def pool_bubble():
    return reverb(splat(1.2) * 0.8, 0.8, 0.15)


SOUNDS = {
    "intro": (rh_intro, 64), "roar": (rh_roar, 48), "hurt": (rh_hurt, 24), "slash": (rh_slash, 24),
    "mark": (rh_mark, 32), "dash": (rh_dash, 32), "crush": (rh_crush, 48), "nova": (rh_nova, 48),
    "pools": (rh_pools, 32), "execution": (rh_execution, 64), "summon": (rh_summon, 56), "phase": (rh_phase, 56),
    "death": (rh_death, 64), "squire_groan": (squire_groan, 20), "squire_hit": (squire_hit, 20),
    "knight_clank": (knight_clank, 20), "knight_bash": (knight_bash, 20), "soul_wail": (soul_wail, 24),
    "soul_hit": (soul_hit, 16), "pool_bubble": (pool_bubble, 12),
}


def main():
    DP.ensure_pack()
    out_dir = DP.sound_dir(BOSS)
    demo = []
    with tempfile.TemporaryDirectory() as tmp:
        for name, (fn, _) in SOUNDS.items():
            x = finish(fn())
            wav = Path(tmp) / f"{name}.wav"
            write_wav(wav, x)
            to_ogg(wav, out_dir / f"{name}.ogg")
            demo += [x, np.zeros(int(0.6 * SR))]
            print(f"OK dextra:{BOSS}.{name:14s} {len(x) / SR:4.1f} s")
        DP.register_sounds(BOSS, {k: d for k, (_, d) in SOUNDS.items()})
        wav = Path(tmp) / "demo.wav"
        write_wav(wav, np.concatenate(demo))
        DEMO.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-b:a", "128k", str(DEMO)], check=True)
    print("demo ->", DEMO)


if __name__ == "__main__":
    main()
