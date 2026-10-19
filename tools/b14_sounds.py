#!/usr/bin/env python3
"""
Sonidos propios de SAMHAIN y sus subditos (sintetizados): organo de feria macabra, risa
siniestra, cuervos, campana de medianoche, viento, fuego que crepita y almas.

  Modelos/DextraBossesPack/assets/dextra/sounds/samhain/*.ogg  ->  dextra:samhain.<nombre>
  Demo: Modelos/14_Samhain/preview/sonidos_demo.mp3

Uso: python3 tools/b14_sounds.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import sndkit  # noqa: E402
from generate_sounds import (AA, OO, SR, bandpass, crack, curve, env, growl, highpass, lowpass,  # noqa: E402
                             mixdown, noise, reverb, rumble, thump, thunder, whoosh)
from b02_sounds import wind  # noqa: E402
from b03_sounds import bell, wail  # noqa: E402
from b04_sounds import organ  # noqa: E402
from b06_sounds import creak  # noqa: E402

BOSS = "samhain"
DEMO = Path(__file__).resolve().parent.parent / "Modelos/14_Samhain/preview/sonidos_demo.mp3"
RNG = np.random.default_rng(1414)


def T(dur):
    return np.arange(int(dur * SR)) / SR


def crackle(dur=1.0, density=60):
    n = int(dur * SR)
    x = np.zeros(n)
    for _ in range(int(density * dur)):
        i = RNG.integers(0, n - 200)
        L = RNG.integers(20, 200)
        x[i:i + L] += RNG.standard_normal(L) * np.exp(-np.arange(L) / (L / 5)) * RNG.uniform(0.3, 1)
    return mixdown((0, highpass(x, 1500)), (0, 0.4 * lowpass(noise(dur), 500) * curve(n, [(0, 0), (0.1, 1), (0.9, 1), (1, 0)])))


def cackle(dur=1.4, f0=260):
    """Risa: rafagas de 'ja' que bajan de tono."""
    parts = []
    k, t = 0, 0.0
    while t < dur - 0.15:
        f = f0 * (1.25 - 0.4 * t / dur)
        g = growl(0.13, [(0, f * 1.1), (1, f * 0.9)], vowel=AA, drv=2.2, rough=12, sub=0.3, breath=0.4)
        parts.append((t, g * env(len(g), 0.01, 0.13, 2.0)))
        t += 0.15 + 0.02 * k
        k += 1
    return mixdown(*parts)


def crow(dur=0.5):
    n = int(dur * SR)
    f = curve(n, [(0, 900), (0.3, 1200), (1, 700)])
    x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.5 + bandpass(noise(dur), 1000, 4000)
    return bandpass(x, 600, 3500) * env(n, 0.01, dur, 1.8)


def souls_moan(dur=1.6):
    return mixdown((0, 0.5 * wail(dur, [(0, 400), (0.5, 520), (1, 300)], 5)), (0.2, 0.4 * wail(dur - 0.2, [(0, 600), (1, 380)], 5)))


def sh_intro():
    s = mixdown((0, 0.7 * wind(5.0)), (0.2, 0.8 * bell(3.5, 82.4)), (0.6, 0.5 * crow(0.5)), (1.0, 0.5 * crow(0.5)),
                (1.4, 0.6 * organ(3.0, [110.0, 130.8, 155.6], 0.3)), (2.6, cackle(1.8, 220)), (2.6, 0.6 * crackle(2.0)))
    return reverb(s, 3.6, 0.42)


def sh_roar():
    return reverb(mixdown((0, cackle(1.6, 240)), (0, 0.4 * crackle(1.6)), (0.2, 0.4 * souls_moan(1.4))), 2.4, 0.38)


def sh_hurt():
    g = growl(0.5, [(0, 220), (0.3, 300), (1, 180)], vowel=AA, drv=2.4, rough=14)
    return reverb(mixdown((0, g * env(len(g), 0.01, 0.5, 1.8, hold=0.1)), (0, 0.4 * crackle(0.4))), 1.0, 0.3)


def sh_reap():
    return reverb(mixdown((0, 0.7 * whoosh(0.5, 150, 3000)), (0, 0.5 * crackle(0.5, 80)), (0.25, 0.5 * crack(0.2))), 1.2, 0.25)


def sh_harvest():
    return reverb(mixdown((0, 0.5 * whoosh(0.3, 120, 1500)), (0.3, thump(1.0, 100, 32)), (0.3, 0.6 * crack(0.3)),
                          (0.3, 0.7 * crackle(1.0, 90)), (0.35, 0.5 * rumble(1.0, 20, 140))), 1.8, 0.3)


def sh_burst():
    n = int(1.2 * SR)
    fwoom = lowpass(noise(1.2), 900) * curve(n, [(0, 0), (0.08, 1), (1, 0)]) ** 1.5
    return reverb(mixdown((0, fwoom), (0, 0.6 * crackle(1.2, 100)), (0.05, 0.5 * souls_moan(1.0))), 2.0, 0.35)


def sh_souls():
    return reverb(mixdown((0, 0.6 * wind(2.0, (300, 700))), (0, souls_moan(2.0)), (0.4, 0.7 * thump(0.8, 90, 30))), 2.8, 0.42)


def sh_wisps():
    return reverb(mixdown((0, 0.7 * thunder(2.2)), (0.1, 0.5 * crackle(1.8, 70)), (0.4, 0.4 * cackle(0.8, 340))), 2.6, 0.38)


def sh_last():
    s = mixdown((0, 0.8 * bell(2.4, 65.4)), (0.5, 0.6 * organ(1.6, [65.4, 77.8, 98.0], 0.4)), (0.2, 0.5 * crackle(1.8, 50)),
                (2.0, thunder(2.4)), (2.0, thump(1.4, 80, 25)), (2.0, 0.8 * crackle(1.4, 160)), (2.1, cackle(1.2, 200)))
    return reverb(s, 3.4, 0.42)


def sh_summon():
    return reverb(mixdown((0, 0.6 * creak(1.4, 60)), (0.2, 0.6 * crow(0.5)), (0.5, 0.6 * crow(0.5)),
                          (0.3, 0.6 * organ(1.6, [98.0, 116.5, 146.8], 0.2))), 2.6, 0.4)


def sh_phase():
    s = mixdown((0, 0.8 * bell(3.0, 73.4)), (0.4, 0.7 * organ(2.0, [73.4, 87.3, 110.0, 138.6], 0.1)), (1.2, cackle(1.6, 200)),
                (1.2, 0.6 * crackle(1.6)))
    return reverb(s, 3.2, 0.42)


def sh_death():
    s = mixdown((0, cackle(1.6, 260)), (1.0, souls_moan(2.4)), (1.4, 0.8 * bell(3.6, 55.0)), (1.6, 0.7 * wind(3.0)),
                (2.2, 0.6 * crow(0.5)), (2.6, 0.5 * crow(0.5)))
    return reverb(s, 3.8, 0.45)


def scarecrow_rustle():
    return reverb(mixdown((0, bandpass(noise(0.8), 2000, 7000) * env(int(0.8 * SR), 0.05, 0.8, 1.5) * 0.6),
                          (0, 0.5 * creak(0.8, 80)), (0.3, 0.4 * crow(0.4))), 1.0, 0.25)


def scarecrow_stab():
    return reverb(mixdown((0, 0.6 * whoosh(0.3, 200, 2500)), (0.2, 0.6 * crack(0.15)), (0.2, 0.4 * thump(0.4, 140, 60))), 0.9, 0.2)


def wisp_giggle():
    return reverb(cackle(0.8, 520), 1.6, 0.45)


def wisp_strike():
    return reverb(mixdown((0, 0.6 * whoosh(0.25, 800, 6000)), (0, 0.6 * crackle(0.4, 120))), 0.9, 0.3)


def rider_laugh():
    return reverb(mixdown((0, cackle(1.2, 160)), (0, 0.3 * crackle(1.2))), 1.6, 0.35)


def rider_slash():
    return reverb(mixdown((0, 0.7 * whoosh(0.3, 400, 5000)), (0.2, 0.7 * whoosh(0.3, 400, 5000))), 0.9, 0.2)


SOUNDS = {
    "intro": (sh_intro, 64), "roar": (sh_roar, 48), "hurt": (sh_hurt, 24), "reap": (sh_reap, 24), "harvest": (sh_harvest, 40),
    "burst": (sh_burst, 40), "souls": (sh_souls, 48), "wisps": (sh_wisps, 56), "last_harvest": (sh_last, 64),
    "summon": (sh_summon, 48), "phase": (sh_phase, 56), "death": (sh_death, 64),
    "scarecrow_rustle": (scarecrow_rustle, 16), "scarecrow_stab": (scarecrow_stab, 16), "wisp_giggle": (wisp_giggle, 20),
    "wisp_strike": (wisp_strike, 16), "rider_laugh": (rider_laugh, 20), "rider_slash": (rider_slash, 16),
}

if __name__ == "__main__":
    sndkit.build(BOSS, SOUNDS, DEMO)
