#!/usr/bin/env python3
"""
Sonidos propios de KRONOS y sus subditos (sintetizados): tic-tac de relojes, campanadas,
sonidos al reves (el tiempo que retrocede), coro grave, arena que cae, engranajes y la voz
del titan.

  Modelos/DextraBossesPack/assets/dextra/sounds/kronos/*.ogg  ->  dextra:kronos.<nombre>
  Demo: Modelos/10_Kronos/preview/sonidos_demo.mp3

Uso: python3 tools/b10_sounds.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import sndkit  # noqa: E402
from generate_sounds import (AA, OO, SR, bandpass, choir, crack, curve, env, growl, highpass, lowpass,  # noqa: E402
                             mixdown, noise, reverb, rumble, thump, whoosh)
from b03_sounds import bell  # noqa: E402
from b04_sounds import clank, organ  # noqa: E402

BOSS = "kronos"
DEMO = Path(__file__).resolve().parent.parent / "Modelos/10_Kronos/preview/sonidos_demo.mp3"
RNG = np.random.default_rng(1010)
NOTES = [55.0, 65.41, 82.41, 98.0]                       # La menor grave


def T(dur):
    return np.arange(int(dur * SR)) / SR


def tick(hz=2400, dur=0.06):
    t = T(dur)
    return (np.sin(2 * np.pi * hz * t) + 0.5 * np.sin(2 * np.pi * hz * 1.7 * t)) * np.exp(-t * 90) + \
        0.4 * highpass(noise(dur), 3000) * np.exp(-t * 120)


def ticking(dur, rate=4.0, speedup=1.0):
    out = np.zeros(int(dur * SR))
    t, k = 0.0, 0
    while t < dur - 0.07:
        x = tick(2600 if k % 2 else 2000)
        i = int(t * SR)
        out[i:i + len(x)] += x
        t += 1 / (rate * (1 + (speedup - 1) * t / dur))
        k += 1
    return out


def reverse(x):
    return x[::-1].copy()


def sand(dur=1.5):
    n = int(dur * SR)
    grains = (RNG.random(n) < 0.04) * RNG.standard_normal(n)
    return bandpass(grains + 0.3 * noise(dur), 2000, 9000) * curve(n, [(0, 0), (0.1, 1), (0.9, 1), (1, 0)])


def gears(dur=1.2):
    n = int(dur * SR)
    out = np.zeros(n)
    for k in range(int(dur * 14)):
        x = clank(0.15, RNG.uniform(500, 1400)) * 0.3
        i = int(RNG.uniform(0, dur - 0.16) * SR)
        out[i:i + len(x)] += x[: n - i]
    return out + 0.4 * lowpass(rumble(dur, 30, 200), 400)


def titan(dur, f_points, drv=2.6):
    return growl(dur, f_points, vowel=OO, drv=drv, rough=18, sub=1.0, breath=0.35)


def toll(hz=73.4, dur=4.0):
    return bell(dur, hz)


def kr_intro():
    s = mixdown((0, 0.6 * ticking(3.0, 3, 3)), (1.2, 0.6 * reverse(toll(110, 2.0))), (3.0, toll(55, 4.0)),
                (3.0, 0.5 * choir(3.5, NOTES, vowel=OO, attack=0.4)), (3.4, titan(2.0, [(0, 70), (0.3, 90), (1, 60)])))
    return reverb(s, 3.6, 0.38)


def kr_roar():
    return reverb(mixdown((0, titan(2.0, [(0, 80), (0.2, 110), (1, 70)])), (0, 0.4 * choir(2.0, NOTES[:3], vowel=OO, attack=0.2)),
                          (0.2, 0.4 * reverse(whoosh(1.0, 200, 3000)))), 2.6, 0.35)


def kr_hurt():
    g = titan(0.6, [(0, 110), (0.3, 140), (1, 90)], drv=3.0)
    return reverb(g * env(len(g), 0.01, 0.6, 1.8, hold=0.1), 1.0, 0.25)


def kr_swing():
    return reverb(mixdown((0, 0.7 * whoosh(0.5, 150, 3000)), (0.28, 0.5 * clank(0.5, 700)), (0.28, 0.6 * thump(0.6, 120, 45))),
                  1.2, 0.2)


def kr_slam():
    s = mixdown((0, 0.4 * reverse(whoosh(0.4, 200, 3000))), (0.25, thump(1.0, 110, 35)), (0.25, 0.6 * crack(0.3)),
                (0.25, 0.6 * toll(146.8, 1.6)), (0.3, 0.5 * lowpass(rumble(1.0, 20, 150), 600)))
    return reverb(s, 2.0, 0.3)


def kr_quake():
    s = mixdown((0, 0.6 * ticking(0.6, 10)), (0.3, thump(1.4, 100, 30)), (0.3, 0.8 * toll(55, 3.0)),
                (0.3, 0.7 * rumble(1.6, 20, 160)), (0.35, 0.6 * gears(1.2)))
    return reverb(s, 2.6, 0.32)


def kr_time():
    """Rugido del tiempo: todo se ralentiza y suena al reves."""
    n = int(2.4 * SR)
    slow = ticking(2.4, 6, 0.25)
    s = mixdown((0, 0.6 * slow), (0, 0.6 * reverse(toll(98, 2.4))), (0.2, titan(1.8, [(0, 90), (1, 60)])),
                (0.0, 0.4 * choir(2.4, NOTES, vowel=AA, attack=0.6)))
    return reverb(s * curve(n, [(0, 1), (1, 1)]), 3.0, 0.4)


def kr_charge():
    s = mixdown((0, 0.6 * reverse(sand(0.5))), (0.1, 0.6 * titan(0.6, [(0, 100), (1, 140)])), (0.4, whoosh(0.6, 150, 4000)),
                (0.5, thump(0.8, 120, 40)), (0.5, 0.5 * clank(0.4, 800)))
    return reverb(s, 1.8, 0.28)


def kr_hourglass():
    return reverb(mixdown((0, 0.5 * clank(0.5, 1200)), (0.4, 0.6 * thump(0.5, 160, 70)), (0.4, sand(1.4)),
                          (0.4, 0.4 * ticking(1.4, 4))), 1.8, 0.3)


def kr_summon():
    s = mixdown((0, 0.5 * reverse(toll(146.8, 1.6))), (1.4, toll(73.4, 3.0)), (0.6, 0.5 * gears(1.6)),
                (1.0, 0.4 * choir(2.0, NOTES[1:], vowel=OO, attack=0.3)))
    return reverb(s, 3.0, 0.35)


def kr_phase():
    s = mixdown((0, 0.6 * ticking(1.6, 4, 4)), (1.5, toll(55, 3.5)), (1.5, 0.6 * organ(2.4, [55, 82.4, 110], 0.05)),
                (1.6, titan(1.6, [(0, 80), (0.2, 120), (1, 70)])))
    return reverb(s, 3.2, 0.38)


def kr_last():
    s = mixdown((0, 0.7 * ticking(2.0, 1.2, 0.5)), (0, 0.5 * sand(2.0)), (1.6, titan(1.4, [(0, 70), (0.3, 120), (1, 90)])),
                (1.6, 0.7 * thump(1.0, 100, 35)), (1.6, 0.6 * toll(98, 2.0)))
    return reverb(s, 2.8, 0.35)


def kr_death():
    s = mixdown((0, titan(2.6, [(0, 110), (0.3, 80), (1, 40)], drv=2.2)), (0.8, 0.6 * ticking(2.0, 4, 0.2)),
                (2.0, toll(55, 4.0)), (2.0, 0.5 * choir(3.5, NOTES, vowel=OO, attack=1.0)), (2.4, 0.5 * reverse(sand(1.5))))
    return reverb(s, 3.6, 0.42)


def sentinel_wind():
    s = mixdown(*[(k * 0.11, 0.6 * clank(0.12, 1500 + 100 * k)) for k in range(6)], (0.7, 0.5 * ticking(0.8, 8)))
    return reverb(s, 1.0, 0.2)


def sentinel_slash():
    return reverb(mixdown((0, 0.7 * whoosh(0.3, 500, 6000)), (0.2, 0.6 * clank(0.4, 1100))), 0.9, 0.2)


def guardian_grunt():
    g = growl(0.7, [(0, 110), (0.3, 130), (1, 90)], vowel=OO, drv=3.0, rough=24)
    return reverb(mixdown((0, g * env(len(g), 0.02, 0.7, 1.6, hold=0.2)), (0, 0.4 * clank(0.5, 600))), 1.0, 0.25)


def guardian_block():
    return reverb(mixdown((0, clank(0.7, 500)), (0, 0.6 * thump(0.4, 180, 80)), (0.05, 0.4 * gears(0.5))), 1.0, 0.2)


def archer_chime():
    t = T(1.2)
    c = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * 3) for f in (880, 1108, 1318)) * 0.4
    return reverb(mixdown((0, c), (0, 0.3 * sand(1.0))), 1.6, 0.4)


def archer_shot():
    return reverb(mixdown((0, 0.5 * clank(0.2, 1800)), (0.05, 0.7 * whoosh(0.35, 1500, 7000))), 0.8, 0.2)


def devourer_roar():
    g = growl(1.4, [(0, 70), (0.2, 100), (1, 60)], vowel=AA, drv=3.6, rough=30, sub=1.0, breath=0.5)
    return reverb(mixdown((0, g), (0.2, 0.4 * gears(1.0))), 1.8, 0.3)


def devourer_bite():
    return reverb(mixdown((0, 0.5 * whoosh(0.3, 200, 2000)), (0.2, thump(0.6, 140, 50)), (0.22, 0.6 * crack(0.15)),
                          (0.22, 0.4 * clank(0.3, 400))), 1.0, 0.2)


SOUNDS = {
    "intro": (kr_intro, 64), "roar": (kr_roar, 56), "hurt": (kr_hurt, 24), "swing": (kr_swing, 24), "slam": (kr_slam, 40),
    "quake": (kr_quake, 48), "time": (kr_time, 48), "charge": (kr_charge, 40), "hourglass": (kr_hourglass, 32),
    "summon": (kr_summon, 48), "phase": (kr_phase, 56), "last_breath": (kr_last, 56), "death": (kr_death, 64),
    "sentinel_wind": (sentinel_wind, 16), "sentinel_slash": (sentinel_slash, 16), "guardian_grunt": (guardian_grunt, 16),
    "guardian_block": (guardian_block, 16), "archer_chime": (archer_chime, 20), "archer_shot": (archer_shot, 20),
    "devourer_roar": (devourer_roar, 32), "devourer_bite": (devourer_bite, 24),
}

if __name__ == "__main__":
    sndkit.build(BOSS, SOUNDS, DEMO)
