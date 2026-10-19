#!/usr/bin/env python3
"""
Sonidos propios de LEVIATAN y sus subditos (sintetizados): canto de ballena, olas, burbujas,
salpicaduras, cuerno del abismo y rugido de dragon marino.

  Modelos/DextraBossesPack/assets/dextra/sounds/leviatan/*.ogg  ->  dextra:leviatan.<nombre>
  Demo: Modelos/12_Leviatan/preview/sonidos_demo.mp3

Uso: python3 tools/b12_sounds.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import sndkit  # noqa: E402
from generate_sounds import (AA, OO, SR, bandpass, brown, crack, curve, env, growl, horn, lowpass,  # noqa: E402
                             mixdown, noise, reverb, rumble, thump, whoosh)
from b06_sounds import bubbles, squelch, wet_voice  # noqa: E402

BOSS = "leviatan"
DEMO = Path(__file__).resolve().parent.parent / "Modelos/12_Leviatan/preview/sonidos_demo.mp3"
RNG = np.random.default_rng(1212)


def T(dur):
    return np.arange(int(dur * SR)) / SR


def whale(dur, pts):
    n = int(dur * SR)
    f = curve(n, pts)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.2 * np.sin(3 * ph)
    return lowpass(x, 1800) * curve(n, [(0, 0), (0.15, 1), (0.8, 0.9), (1, 0)])


def waves(dur):
    n = int(dur * SR)
    x = lowpass(brown(dur), 900, 2) * 2 + 0.3 * bandpass(noise(dur), 800, 5000)
    sw = 0.5 + 0.5 * np.sin(2 * np.pi * 0.35 * T(dur) - 1.5)
    return x * sw * curve(n, [(0, 0), (0.1, 1), (0.9, 1), (1, 0)])


def splash(dur=0.8):
    n = int(dur * SR)
    return mixdown((0, bandpass(noise(dur), 500, 7000) * env(n, 0.005, dur, 3)), (0, 0.6 * bubbles(dur, 10)),
                   (0, 0.6 * thump(0.4, 140, 60)))


def sea_roar(dur, pts, drv=3.2):
    g = growl(dur, pts, vowel=OO, drv=drv, rough=22, sub=1.0, breath=0.5)
    return mixdown((0, g), (0, 0.4 * wet_voice(dur, [(p, f * 1.3) for p, f in pts])))


def lv_intro():
    s = mixdown((0, 0.8 * waves(5.0)), (0.3, 0.7 * whale(2.5, [(0, 200), (0.5, 340), (1, 160)])),
                (1.8, 0.7 * horn(2.4, 73.4)), (2.6, sea_roar(2.0, [(0, 80), (0.3, 110), (1, 60)])), (2.6, 0.8 * splash(1.0)))
    return reverb(s, 3.6, 0.4)


def lv_roar():
    return reverb(mixdown((0, sea_roar(2.0, [(0, 90), (0.2, 130), (1, 70)])), (0, 0.5 * bubbles(1.6, 14))), 2.6, 0.35)


def lv_hurt():
    g = sea_roar(0.6, [(0, 140), (0.3, 180), (1, 110)])
    return reverb(g * env(len(g), 0.01, 0.6, 1.8, hold=0.1), 1.0, 0.25)


def lv_stab():
    return reverb(mixdown((0, 0.7 * whoosh(0.35, 300, 4000)), (0.25, 0.6 * crack(0.15)), (0.25, 0.5 * splash(0.5))), 1.2, 0.25)


def lv_curse():
    return reverb(mixdown((0, 0.6 * whale(1.4, [(0, 500), (1, 220)])), (0, 0.6 * bubbles(1.4, 20)),
                          (0.2, 0.5 * whoosh(1.0, 300, 3000))), 2.4, 0.4)


def lv_splash():
    return reverb(mixdown((0, 0.6 * whoosh(0.4, 200, 3000)), (0.1, splash(1.0))), 1.6, 0.3)


def lv_whirlpool():
    n = int(2.0 * SR)
    swirl = bandpass(noise(2.0), 200, 1500) * (0.6 + 0.4 * np.sin(2 * np.pi * np.cumsum(curve(n, [(0, 1), (1, 6)])) / SR))
    return reverb(mixdown((0, swirl * curve(n, [(0, 0), (0.2, 1), (1, 0)])), (0, 0.6 * lowpass(rumble(2.0, 20, 140), 400)),
                          (0.2, 0.5 * bubbles(1.6, 20))), 2.4, 0.38)


def lv_ink():
    return reverb(mixdown((0, 0.8 * squelch(0.5)), (0.1, 0.6 * lowpass(noise(1.2), 600) * env(int(1.2 * SR), 0.1, 1.2, 1.5)),
                          (0.1, 0.5 * bubbles(1.2, 12))), 2.0, 0.4)


def lv_tsunami():
    s = mixdown((0, 0.6 * whoosh(0.5, 100, 1200)), (0.3, waves(2.4)), (0.3, thump(1.2, 90, 30)), (0.3, 0.9 * splash(1.2)),
                (0.35, 0.6 * rumble(1.6, 18, 150)))
    return reverb(s, 2.8, 0.38)


def lv_summon():
    return reverb(mixdown((0, 0.7 * horn(2.0, 98.0)), (0.3, 0.6 * whale(1.8, [(0, 300), (0.6, 420), (1, 260)])),
                          (0.6, 0.6 * splash(1.0))), 3.0, 0.4)


def lv_phase():
    s = mixdown((0, 0.7 * waves(3.0)), (0.6, 0.8 * horn(2.2, 55.0)), (1.2, sea_roar(1.8, [(0, 70), (0.2, 120), (1, 60)])),
                (1.2, 0.8 * splash(1.2)))
    return reverb(s, 3.2, 0.4)


def lv_death():
    s = mixdown((0, sea_roar(2.6, [(0, 120), (0.4, 80), (1, 40)], drv=2.4)),
                (1.0, 0.8 * whale(3.0, [(0, 300), (0.5, 200), (1, 90)])), (1.5, 0.8 * waves(3.0)), (2.2, 0.7 * bubbles(2.0, 24)))
    return reverb(s, 3.8, 0.45)


def drowned_groan():
    g = growl(0.9, [(0, 120), (0.5, 100), (1, 85)], vowel=AA, drv=2.6, rough=26)
    return reverb(mixdown((0, g * env(len(g), 0.05, 0.9, 1.6, hold=0.3)), (0, 0.4 * bubbles(0.8, 8))), 1.2, 0.3)


def drowned_slash():
    return reverb(mixdown((0, 0.7 * whoosh(0.3, 500, 6000)), (0.2, 0.5 * squelch(0.3))), 0.9, 0.2)


def tide_chime():
    t = T(1.4)
    c = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * 3) for f in (660, 990, 1320)) * 0.4
    return reverb(mixdown((0, c), (0, 0.4 * bubbles(1.0, 10))), 2.0, 0.45)


def tide_pulse():
    return reverb(mixdown((0, 0.6 * whale(0.8, [(0, 600), (1, 900)])), (0, 0.4 * bubbles(0.6, 10))), 1.4, 0.4)


def eel_hiss():
    n = int(0.8 * SR)
    return reverb(bandpass(noise(0.8), 2500, 8000) * curve(n, [(0, 0), (0.2, 1), (1, 0)]) + 0.4 * whale(0.8, [(0, 800), (1, 500)]),
                  1.2, 0.3)


def eel_bite():
    return reverb(mixdown((0, 0.5 * whoosh(0.25, 600, 5000)), (0.15, 0.7 * crack(0.12)), (0.15, 0.5 * squelch(0.3))), 0.8, 0.2)


SOUNDS = {
    "intro": (lv_intro, 64), "roar": (lv_roar, 56), "hurt": (lv_hurt, 24), "stab": (lv_stab, 24), "curse": (lv_curse, 32),
    "splash": (lv_splash, 32), "whirlpool": (lv_whirlpool, 40), "ink": (lv_ink, 32), "tsunami": (lv_tsunami, 48),
    "summon": (lv_summon, 48), "phase": (lv_phase, 56), "death": (lv_death, 64), "drowned_groan": (drowned_groan, 16),
    "drowned_slash": (drowned_slash, 16), "tide_chime": (tide_chime, 20), "tide_pulse": (tide_pulse, 16),
    "eel_hiss": (eel_hiss, 16), "eel_bite": (eel_bite, 16),
}

if __name__ == "__main__":
    sndkit.build(BOSS, SOUNDS, DEMO)
