#!/usr/bin/env python3
"""
Sonidos propios de THOR y sus subditos (sintetizados): truenos, chispazos electricos, el
zumbido de Mjolnir, cuerno de guerra, coro del Valhalla y la voz del dios.

  Modelos/DextraBossesPack/assets/dextra/sounds/thor/*.ogg  ->  dextra:thor.<nombre>
  Demo: Modelos/15_Thor/preview/sonidos_demo.mp3

Uso: python3 tools/b15_sounds.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import sndkit  # noqa: E402
from generate_sounds import (AA, OO, SR, bandpass, choir, crack, curve, env, growl, highpass, horn, lowpass,  # noqa: E402
                             mixdown, noise, reverb, rumble, thump, thunder, whoosh)
from b04_sounds import clank  # noqa: E402
from b05_sounds import drums, giant  # noqa: E402

BOSS = "thor"
DEMO = Path(__file__).resolve().parent.parent / "Modelos/15_Thor/preview/sonidos_demo.mp3"
RNG = np.random.default_rng(1515)
NOTES = [73.4, 110.0, 146.8, 174.6]


def T(dur):
    return np.arange(int(dur * SR)) / SR


def zap(dur=0.3):
    """Chispazo: rafagas de ruido agudo cortadas."""
    n = int(dur * SR)
    gate = (RNG.random(n // 200 + 1) < 0.6).repeat(200)[:n]
    return highpass(noise(dur), 2500) * gate * env(n, 0.001, dur, 2.0)


def crackle_bolt(dur=0.6):
    return mixdown((0, crack(0.15)), (0, 0.8 * zap(dur)), (0.02, 0.6 * lowpass(noise(0.3), 300) * env(int(0.3 * SR), 0.001, 0.3, 3)))


def strike(dur=2.4):
    return mixdown((0, crackle_bolt(0.5)), (0.05, thunder(dur)))


def hum(dur, f0=55):
    t = T(dur)
    x = np.sin(2 * np.pi * f0 * t) + 0.5 * np.sin(2 * np.pi * f0 * 2.01 * t) + 0.3 * zap(dur)
    return lowpass(x, 2000) * curve(len(t), [(0, 0), (0.2, 1), (0.8, 1), (1, 0)])


def god(dur, pts, drv=3.0):
    return giant(dur, pts, drv=drv)


def th_intro():
    s = mixdown((0, 0.7 * rumble(5.0, 18, 140)), (0.3, 0.8 * horn(2.4, 73.4)), (1.4, 0.7 * drums(4, 0.35)),
                (2.4, strike(2.6)), (2.6, 0.5 * choir(2.6, NOTES, vowel=AA, attack=0.3)),
                (2.8, god(1.8, [(0, 80), (0.3, 120), (1, 70)])))
    return reverb(s, 3.6, 0.38)


def th_roar():
    return reverb(mixdown((0, god(1.8, [(0, 90), (0.2, 140), (1, 80)])), (0.1, 0.6 * thunder(1.8))), 2.4, 0.32)


def th_hurt():
    g = god(0.5, [(0, 140), (0.3, 180), (1, 110)])
    return reverb(mixdown((0, g * env(len(g), 0.01, 0.5, 1.8, hold=0.1)), (0, 0.4 * zap(0.3))), 1.0, 0.25)


def th_swing():
    return reverb(mixdown((0, 0.6 * whoosh(0.4, 100, 2000)), (0.25, thump(0.6, 120, 40)), (0.25, 0.6 * crackle_bolt(0.4))), 1.2, 0.25)


def th_throw():
    return reverb(mixdown((0, 0.6 * hum(0.5, 70)), (0.2, 0.7 * whoosh(0.4, 200, 3000)), (0.4, strike(1.6))), 2.0, 0.3)


def th_shock():
    n = int(1.0 * SR)
    sweep = np.sin(2 * np.pi * np.cumsum(curve(n, [(0, 1200), (1, 200)])) / SR) * env(n, 0.001, 1.0, 2.0)
    return reverb(mixdown((0, thump(0.8, 110, 35)), (0, 0.6 * sweep), (0, 0.7 * zap(0.7))), 1.8, 0.3)


def th_thunder():
    return reverb(mixdown((0, 0.5 * whoosh(0.4, 100, 800)), (0.2, strike(2.2)), (0.35, 0.6 * crackle_bolt(0.4)),
                          (0.5, 0.6 * crackle_bolt(0.4))), 2.6, 0.35)


def th_absorb():
    s = mixdown((0, 0.6 * hum(1.4, 55)), (0.2, 0.8 * crackle_bolt(0.5)), (0.45, 0.8 * crackle_bolt(0.5)),
                (0.7, 0.8 * crackle_bolt(0.5)), (0.7, 0.6 * god(0.8, [(0, 100), (1, 140)])))
    return reverb(s, 2.2, 0.32)


def th_nova():
    return reverb(mixdown((0, 0.6 * whoosh(0.5, 100, 1500)), (0.45, strike(2.0)), (0.5, thump(1.2, 90, 28)),
                          (0.5, 0.6 * rumble(1.4, 18, 150))), 2.6, 0.35)


def th_surge():
    n = int(0.5 * SR)
    pull = np.sin(2 * np.pi * np.cumsum(curve(n, [(0, 60), (1, 400)])) / SR) * curve(n, [(0, 0), (1, 1)])
    return reverb(mixdown((0, 0.6 * pull), (0, 0.5 * hum(0.5, 80)), (0.5, thump(1.0, 100, 30)), (0.5, 0.7 * crackle_bolt(0.6))),
                  2.0, 0.3)


def th_eruption():
    return reverb(mixdown(*[(t, 0.6 * crackle_bolt(0.4)) for t in (0.0, 0.1, 0.22, 0.35, 0.5)], (0, thunder(2.4)),
                          (0, 0.8 * thump(1.0, 100, 30))), 2.6, 0.35)


def th_judgement():
    s = mixdown((0, 0.6 * horn(1.0, 110.0)), (0.2, 0.6 * hum(1.0, 65)), (1.2, strike(2.4)), (1.2, thump(1.2, 80, 26)))
    return reverb(s, 2.8, 0.35)


def th_ragnarok():
    s = mixdown((0, 0.7 * hum(1.5, 41)), (0, 0.6 * rumble(1.5, 18, 120)), (0.3, 0.6 * horn(1.2, 55.0)),
                (1.5, strike(2.8)), (1.5, thump(1.4, 70, 22)), (1.55, 0.6 * choir(2.0, NOTES, vowel=AA, attack=0.05)))
    return reverb(s, 3.2, 0.4)


def th_summon():
    return reverb(mixdown((0, 0.8 * horn(2.2, 98.0)), (0.3, 0.6 * choir(2.2, NOTES, vowel=AA, attack=0.6)),
                          (0.8, 0.6 * drums(3, 0.3))), 3.0, 0.4)


def th_phase():
    s = mixdown((0, 0.6 * hum(1.2, 55)), (0.5, strike(2.4)), (0.8, god(1.6, [(0, 80), (0.2, 130), (1, 70)])),
                (0.8, 0.5 * choir(2.0, NOTES, vowel=AA, attack=0.2)))
    return reverb(s, 3.0, 0.38)


def th_death():
    s = mixdown((0, god(2.4, [(0, 120), (0.4, 80), (1, 40)], drv=2.4)), (1.0, thunder(3.0)), (1.6, 0.7 * horn(3.0, 55.0)),
                (2.0, 0.5 * choir(3.0, NOTES, vowel=OO, attack=1.0)))
    return reverb(s, 3.8, 0.42)


def einherjar_cry():
    g = growl(0.9, [(0, 140), (0.3, 190), (1, 130)], vowel=AA, drv=2.6, rough=20)
    return reverb(mixdown((0, g * env(len(g), 0.02, 0.9, 1.6, hold=0.3)), (0, 0.4 * choir(0.9, NOTES[1:3], vowel=AA, attack=0.1))),
                  1.6, 0.4)


def einherjar_chop():
    return reverb(mixdown((0, 0.7 * whoosh(0.35, 150, 2000)), (0.25, thump(0.5, 140, 50)), (0.25, 0.5 * clank(0.4, 800))), 1.0, 0.2)


def creeper_hiss():
    n = int(1.0 * SR)
    return reverb(mixdown((0, bandpass(noise(1.0), 2000, 8000) * curve(n, [(0, 0), (1, 1)])), (0.3, 0.6 * zap(0.7))), 1.0, 0.2)


def creeper_boom():
    return reverb(mixdown((0, strike(1.6)), (0, thump(1.0, 100, 30))), 2.0, 0.3)


def spark_buzz():
    return reverb(mixdown((0, 0.5 * hum(0.8, 220)), (0, 0.6 * zap(0.8))), 0.8, 0.2)


def spark_pop():
    return reverb(crackle_bolt(0.4), 1.0, 0.25)


def field_hum():
    return reverb(hum(2.0, 60), 1.6, 0.3)


def cloud_rumble():
    return reverb(mixdown((0, 0.7 * rumble(2.4, 18, 120)), (0.8, 0.6 * crackle_bolt(0.4))), 2.4, 0.35)


SOUNDS = {
    "intro": (th_intro, 64), "roar": (th_roar, 56), "hurt": (th_hurt, 24), "swing": (th_swing, 24), "throw": (th_throw, 48),
    "shock": (th_shock, 40), "thunder": (th_thunder, 56), "absorb": (th_absorb, 48), "nova": (th_nova, 56),
    "surge": (th_surge, 40), "eruption": (th_eruption, 64), "judgement": (th_judgement, 64), "ragnarok": (th_ragnarok, 64),
    "summon": (th_summon, 48), "phase": (th_phase, 56), "death": (th_death, 64), "einherjar_cry": (einherjar_cry, 20),
    "einherjar_chop": (einherjar_chop, 16), "creeper_hiss": (creeper_hiss, 16), "creeper_boom": (creeper_boom, 40),
    "spark_buzz": (spark_buzz, 12), "spark_pop": (spark_pop, 16), "field_hum": (field_hum, 16), "cloud_rumble": (cloud_rumble, 32),
}

if __name__ == "__main__":
    sndkit.build(BOSS, SOUNDS, DEMO)
