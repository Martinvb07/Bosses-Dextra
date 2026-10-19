#!/usr/bin/env python3
"""
Sonidos propios del YETI y sus subditos (sintetizados): rugidos graves de bestia, hielo que se
rompe, ventisca que aulla, golpes contra el suelo y rocas de hielo.

  Modelos/DextraBossesPack/assets/dextra/sounds/yeti/*.ogg  ->  dextra:yeti.<nombre>
  Demo: Modelos/08_Yeti/preview/sonidos_demo.mp3

Uso: python3 tools/b08_sounds.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import sndkit  # noqa: E402
from generate_sounds import (AA, OO, SR, bandpass, crack, curve, debris, env, growl, highpass, lowpass,  # noqa: E402
                             mixdown, noise, reverb, rumble, thump, whoosh)
from b02_sounds import wind  # noqa: E402
from b05_sounds import ice_creak, shatter  # noqa: E402

BOSS = "yeti"
DEMO = Path(__file__).resolve().parent.parent / "Modelos/08_Yeti/preview/sonidos_demo.mp3"


def beast(dur, f_points, drv=3.4, vowel=OO, rough=26):
    return growl(dur, f_points, vowel=vowel, drv=drv, rough=rough, sub=1.0, breath=0.45)


def chuff(dur=0.5):
    n = int(dur * SR)
    return bandpass(noise(dur), 200, 1600) * curve(n, [(0, 0), (0.1, 1), (1, 0)]) ** 2


def boulder(dur=1.0):
    return mixdown((0, thump(dur, 90, 32)), (0, 0.7 * rumble(dur * 0.8, 20, 160)), (0, 0.6 * lowpass(debris(dur, 60), 2500)))


def blizzard(dur=3.0):
    return mixdown((0, wind(dur, (260, 620))), (0.2, 0.4 * wind(dur - 0.2, (400, 900))),
                   (0, 0.3 * highpass(noise(dur), 4000) * curve(int(dur * SR), [(0, 0), (0.3, 1), (1, 0)])))


def yt_intro():
    s = mixdown((0, 0.6 * blizzard(3.0)), (0.6, 0.8 * ice_creak(1.2)), (1.4, beast(2.4, [(0, 90), (0.3, 120), (1, 70)])),
                (1.4, 0.8 * thump(1.2, 80, 30)), (1.8, 0.5 * shatter(1.0)))
    return reverb(s, 3.0, 0.35)


def yt_roar():
    s = mixdown((0, 0.4 * chuff(0.4)), (0.3, beast(2.0, [(0, 100), (0.2, 140), (0.7, 120), (1, 80)])),
                (0.3, 0.4 * wind(1.6, (300, 700))))
    return reverb(s, 2.4, 0.3)


def yt_hurt():
    g = beast(0.6, [(0, 150), (0.3, 180), (1, 110)], drv=3.0, vowel=AA)
    return reverb(g * env(len(g), 0.01, 0.6, 1.8, hold=0.1), 0.9, 0.2)


def yt_smash():
    return reverb(mixdown((0, 0.5 * whoosh(0.4, 120, 1500)), (0.28, thump(0.9, 110, 38)), (0.28, 0.8 * shatter(0.8))),
                  1.6, 0.25)


def yt_shatter():
    s = mixdown((0, 0.5 * beast(0.8, [(0, 110), (1, 150)])), (0.4, thump(1.2, 100, 30)), (0.4, 0.7 * rumble(1.4, 20, 150)),
                (0.45, shatter(1.2)), (0.6, 0.6 * ice_creak(1.0)))
    return reverb(s, 2.2, 0.3)


def yt_throw():
    s = mixdown((0, 0.6 * ice_creak(0.6)), (0.1, 0.5 * beast(0.6, [(0, 120), (1, 160)])), (0.5, 0.7 * whoosh(0.5, 150, 1800)),
                (0.95, boulder(1.0)), (0.95, 0.7 * shatter(0.8)))
    return reverb(s, 1.8, 0.25)


def yt_barrage():
    s = mixdown((0, 0.6 * whoosh(0.8, 100, 1200)), *[(0.5 + 0.15 * k, (0.8 - 0.08 * k) * boulder(0.8)) for k in range(5)],
                (0.6, 0.6 * shatter(1.2)))
    return reverb(s, 2.2, 0.3)


def yt_nova():
    n = int(1.2 * SR)
    hiss = highpass(noise(1.2), 3000) * curve(n, [(0, 1), (0.15, 0.8), (1, 0)])
    return reverb(mixdown((0, crack(0.3)), (0, 0.7 * hiss), (0, 0.8 * shatter(1.0)), (0.05, 0.5 * whoosh(0.8, 300, 4000))),
                  2.0, 0.35)


def yt_blizzard():
    return reverb(mixdown((0, blizzard(3.4)), (0.4, 0.4 * beast(1.4, [(0, 90), (1, 120)]))), 2.4, 0.3)


def yt_summon():
    s = mixdown((0, beast(1.2, [(0, 120), (0.5, 160), (1, 120)])), (0.2, 0.7 * thump(0.6, 100, 40)),
                (0.5, 0.7 * thump(0.6, 100, 40)), (0.6, 0.5 * blizzard(1.6)))
    return reverb(s, 2.2, 0.3)


def yt_phase():
    s = mixdown((0, 0.8 * ice_creak(1.4)), (0.8, thump(1.0, 90, 30)), (1.2, beast(1.8, [(0, 90), (0.2, 150), (1, 80)])),
                (1.2, 0.6 * blizzard(2.0)))
    return reverb(s, 2.8, 0.35)


def yt_shield():
    n = int(2.4 * SR)
    hum = np.sin(2 * np.pi * 220 * np.arange(n) / SR) * curve(n, [(0, 0), (0.8, 0.4), (1, 0)])
    return reverb(mixdown((0, 0.6 * ice_creak(2.0)), (0, 0.4 * hum), (2.2, shatter(1.0))), 2.4, 0.35)


def yt_death():
    s = mixdown((0, beast(2.6, [(0, 130), (0.3, 100), (1, 50)], drv=2.6)), (1.4, thump(1.4, 80, 28)),
                (1.5, 0.8 * shatter(1.6)), (1.6, 0.6 * wind(2.4, (200, 400))))
    return reverb(s, 3.2, 0.38)


def brute_grunt():
    g = growl(0.6, [(0, 110), (0.3, 140), (1, 90)], vowel=OO, drv=3.2, rough=30)
    return reverb(g * env(len(g), 0.02, 0.6, 1.8, hold=0.2), 0.9, 0.2)


def brute_maul():
    return reverb(mixdown((0, 0.6 * whoosh(0.4, 100, 1400)), (0.35, thump(0.6, 120, 40)), (0.35, 0.6 * shatter(0.5))), 1.0,
                  0.2)


def raider_shout():
    g = growl(0.7, [(0, 160), (0.4, 210), (1, 150)], vowel=AA, drv=2.8, rough=24)
    return reverb(g * env(len(g), 0.02, 0.7, 1.6, hold=0.25), 1.0, 0.2)


def raider_cleave():
    return reverb(mixdown((0, 0.8 * whoosh(0.35, 400, 5000)), (0.2, 0.7 * shatter(0.5))), 1.0, 0.2)


def spirit_howl():
    return reverb(mixdown((0, wind(1.4, (500, 1100))), (0, 0.3 * highpass(noise(1.4), 5000) * 0.3)), 1.8, 0.4)


def spirit_claw():
    return reverb(mixdown((0, 0.6 * whoosh(0.25, 800, 6000)), (0.1, 0.6 * shatter(0.4))), 0.8, 0.25)


SOUNDS = {
    "intro": (yt_intro, 64), "roar": (yt_roar, 56), "hurt": (yt_hurt, 24), "smash": (yt_smash, 32),
    "shatter": (yt_shatter, 48), "throw": (yt_throw, 40), "barrage": (yt_barrage, 48), "nova": (yt_nova, 40),
    "blizzard": (yt_blizzard, 56), "summon": (yt_summon, 48), "phase": (yt_phase, 56), "shield": (yt_shield, 48),
    "death": (yt_death, 64), "brute_grunt": (brute_grunt, 16), "brute_maul": (brute_maul, 16),
    "raider_shout": (raider_shout, 16), "raider_cleave": (raider_cleave, 16), "spirit_howl": (spirit_howl, 20),
    "spirit_claw": (spirit_claw, 16),
}

if __name__ == "__main__":
    sndkit.build(BOSS, SOUNDS, DEMO)
