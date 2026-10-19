#!/usr/bin/env python3
"""
Sonidos propios de XYLAR y sus subditos (sintetizados): zumbido de espada de energia,
laseres, coro espacial, gravedad que aspira, supernova y armadura de metal estelar.

  Modelos/DextraBossesPack/assets/dextra/sounds/xylar/*.ogg  ->  dextra:xylar.<nombre>
  Demo: Modelos/13_Xylar/preview/sonidos_demo.mp3

Uso: python3 tools/b13_sounds.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import sndkit  # noqa: E402
from generate_sounds import (AA, OO, SR, bandpass, choir, crack, curve, env, growl, highpass, lowpass,  # noqa: E402
                             mixdown, noise, reverb, rumble, thump, thunder, whoosh)
from b04_sounds import clank  # noqa: E402
from b11_sounds import drone, stars  # noqa: E402

BOSS = "xylar"
DEMO = Path(__file__).resolve().parent.parent / "Modelos/13_Xylar/preview/sonidos_demo.mp3"
NOTES = [69.3, 103.8, 138.6, 164.8]


def T(dur):
    return np.arange(int(dur * SR)) / SR


def saber(dur, f0=110, swing=False):
    n = int(dur * SR)
    t = T(dur)
    f = f0 * (1 + (0.3 * np.sin(np.pi * np.clip(t / dur, 0, 1)) if swing else 0))
    ph = 2 * np.pi * np.cumsum(np.full(n, 1.0) * f) / SR
    x = np.sign(np.sin(ph)) * 0.4 + np.sin(2 * ph) * 0.4 + 0.2 * bandpass(noise(dur), 2000, 6000)
    return lowpass(x, 3000) * curve(n, [(0, 0), (0.1, 1), (0.85, 1), (1, 0)])


def zap(dur=0.35, f0=2400, f1=200):
    n = int(dur * SR)
    f = curve(n, [(0, f0), (1, f1)])
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, dur, 2.0)


def warp_rise(dur, f0=60, f1=900):
    n = int(dur * SR)
    f = curve(n, [(0, f0), (1, f1)])
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.4 * np.sin(4 * np.pi * np.cumsum(f) / SR)) * curve(n, [(0, 0), (1, 1)])


def knight_voice(dur, pts):
    return growl(dur, pts, vowel=OO, drv=2.8, rough=18, sub=1.0, breath=0.3)


def xy_intro():
    s = mixdown((0, 0.7 * drone(5.0, 34.6)), (0.4, 0.6 * choir(4.0, NOTES, vowel=AA, attack=1.0)), (1.6, 0.6 * warp_rise(1.4)),
                (3.0, thump(1.4, 90, 30)), (3.0, 0.7 * thunder(2.0)), (3.0, 0.5 * stars(2.0, 20)),
                (3.2, knight_voice(1.6, [(0, 80), (0.3, 110), (1, 70)])))
    return reverb(s, 3.8, 0.4)


def xy_roar():
    return reverb(mixdown((0, knight_voice(1.8, [(0, 90), (0.2, 130), (1, 70)])), (0, 0.5 * saber(1.8, 90))), 2.4, 0.35)


def xy_hurt():
    g = knight_voice(0.5, [(0, 140), (0.3, 170), (1, 100)])
    return reverb(mixdown((0, g * env(len(g), 0.01, 0.5, 1.8, hold=0.1)), (0, 0.5 * clank(0.4, 700))), 1.0, 0.25)


def xy_swing():
    return reverb(mixdown((0, saber(0.5, 120, True)), (0.2, 0.5 * zap(0.2, 3000, 800))), 1.0, 0.25)


def xy_combo():
    return reverb(mixdown(*[(k * 0.3, saber(0.4, 110 + 15 * k, True)) for k in range(3)],
                          *[(0.15 + k * 0.3, 0.4 * zap(0.15, 3200, 900)) for k in range(3)]), 1.4, 0.3)


def xy_mark():
    return reverb(mixdown((0, stars(1.6, 14)), (0, 0.5 * choir(1.6, NOTES[2:], vowel=AA, attack=0.2)), (0.1, 0.5 * zap(0.6, 600, 2400))),
                  2.4, 0.4)


def xy_dash():
    return reverb(mixdown((0, 0.6 * warp_rise(0.4, 200, 2000)), (0.4, zap(0.4, 2600, 100)), (0.45, 0.6 * thump(0.4, 160, 60))),
                  1.6, 0.35)


def xy_crush():
    n = int(1.2 * SR)
    suck = lowpass(noise(1.2), 900) * curve(n, [(0, 0), (0.4, 1), (0.42, 0), (1, 0)])
    return reverb(mixdown((0, 0.8 * suck), (0, 0.5 * warp_rise(0.5, 40, 300)), (0.5, thump(1.0, 80, 26)),
                          (0.5, 0.7 * crack(0.4)), (0.5, 0.6 * rumble(1.2, 18, 140))), 2.2, 0.35)


def xy_nova():
    return reverb(mixdown((0, 0.7 * warp_rise(0.4, 100, 1600)), (0.4, thunder(2.2)), (0.4, 0.8 * thump(1.0, 100, 30)),
                          (0.45, 0.5 * stars(1.4, 24))), 3.0, 0.38)


def xy_horizon():
    s = mixdown((0, 0.8 * warp_rise(2.0, 30, 200)), (0, 0.7 * drone(2.0, 27.5)), (0.3, 0.5 * choir(1.7, NOTES[:2], vowel=OO, attack=1.0)),
                (2.0, thunder(2.4)), (2.0, thump(1.4, 70, 22)))
    return reverb(s, 3.2, 0.4)


def xy_pools():
    return reverb(mixdown((0, 0.6 * warp_rise(0.5, 300, 60)), (0.4, 0.8 * thump(0.8, 120, 40)), (0.4, 0.6 * drone(1.2, 41.2))),
                  2.2, 0.35)


def xy_meteor():
    n = int(0.8 * SR)
    fall = bandpass(noise(0.8), 300, 4000) * curve(n, [(0, 0), (1, 1)])
    return reverb(mixdown((0, fall), (0.75, thump(1.0, 100, 30)), (0.75, 0.7 * crack(0.3)), (0.8, 0.6 * clank(0.6, 500))),
                  2.2, 0.35)


def xy_summon():
    return reverb(mixdown((0, 0.6 * choir(2.0, NOTES, vowel=AA, attack=0.5)), (0.2, xy_meteor())), 2.6, 0.38)


def xy_phase():
    s = mixdown((0, 0.7 * warp_rise(1.4, 60, 1200)), (1.3, thunder(2.4)), (1.3, 0.7 * choir(2.4, NOTES, vowel=AA, attack=0.2)),
                (1.4, knight_voice(1.4, [(0, 80), (0.2, 120), (1, 70)])))
    return reverb(s, 3.2, 0.4)


def xy_death():
    s = mixdown((0, knight_voice(2.4, [(0, 120), (0.4, 80), (1, 40)])), (0.6, 0.7 * saber(2.0, 90)[::-1].copy()),
                (1.6, thunder(3.0)), (1.8, 0.6 * stars(2.4, 28)), (1.8, 0.5 * choir(3.0, NOTES, vowel=OO, attack=1.0)))
    return reverb(s, 3.8, 0.45)


def soldier_radio():
    n = int(0.8 * SR)
    beeps = sum(np.sin(2 * np.pi * f * T(0.8)) * ((T(0.8) > a) & (T(0.8) < a + 0.08)) for f, a in ((1400, 0), (1800, 0.15), (1200, 0.3)))
    return reverb(mixdown((0, 0.4 * beeps), (0.3, 0.5 * bandpass(noise(0.5), 1000, 4000) * env(int(0.5 * SR), 0.01, 0.5, 2))), 0.8, 0.2)


def soldier_slash():
    return reverb(mixdown((0, 0.8 * saber(0.35, 160, True)), (0.15, 0.4 * zap(0.15))), 0.8, 0.2)


def knight_growl():
    g = knight_voice(0.9, [(0, 90), (0.4, 110), (1, 80)])
    return reverb(mixdown((0, g * env(len(g), 0.05, 0.9, 1.6, hold=0.3)), (0, 0.4 * clank(0.6, 400))), 1.2, 0.3)


def knight_strike():
    return reverb(mixdown((0, 0.7 * whoosh(0.4, 100, 1500)), (0.3, thump(0.6, 120, 40)), (0.3, 0.6 * clank(0.5, 600))), 1.0, 0.2)


def shard_chime():
    t = T(1.2)
    c = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * 4) for f in (1046, 1568, 2093)) * 0.4
    return reverb(c, 1.6, 0.45)


def shard_hit():
    return reverb(mixdown((0, 0.6 * zap(0.25, 3000, 1200)), (0, 0.5 * highpass(crack(0.15), 3000))), 0.8, 0.3)


def well_hum():
    return reverb(mixdown((0, drone(2.0, 41.2)), (0, 0.4 * warp_rise(2.0, 80, 40))), 2.0, 0.35)


SOUNDS = {
    "intro": (xy_intro, 64), "roar": (xy_roar, 48), "hurt": (xy_hurt, 24), "swing": (xy_swing, 24), "combo": (xy_combo, 32),
    "mark": (xy_mark, 32), "dash": (xy_dash, 32), "crush": (xy_crush, 48), "nova": (xy_nova, 56), "horizon": (xy_horizon, 64),
    "pools": (xy_pools, 40), "meteor": (xy_meteor, 48), "summon": (xy_summon, 48), "phase": (xy_phase, 56),
    "death": (xy_death, 64), "soldier_radio": (soldier_radio, 16), "soldier_slash": (soldier_slash, 16),
    "knight_growl": (knight_growl, 16), "knight_strike": (knight_strike, 16), "shard_chime": (shard_chime, 20),
    "shard_hit": (shard_hit, 16), "well_hum": (well_hum, 16),
}

if __name__ == "__main__":
    sndkit.build(BOSS, SOUNDS, DEMO)
