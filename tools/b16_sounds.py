#!/usr/bin/env python3
"""
Sonidos propios de KUKULKAN y sus subditos (sintetizados): caracola, huehuetl (tambor),
silbato de la muerte, sonajas, siseo de serpiente, aleteo de plumas y cantos de quetzal.

  Modelos/DextraBossesPack/assets/dextra/sounds/kukulkan/*.ogg  ->  dextra:kukulkan.<nombre>
  Demo: Modelos/16_Kukulkan/preview/sonidos_demo.mp3

Uso: python3 tools/b16_sounds.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import sndkit  # noqa: E402
from generate_sounds import (AA, OO, SR, bandpass, choir, crack, curve, env, growl, highpass, horn, lowpass,  # noqa: E402
                             mixdown, noise, reverb, rumble, thump, thunder, whoosh)
from b03_sounds import taiko, wail  # noqa: E402
from b06_sounds import bubbles  # noqa: E402

BOSS = "kukulkan"
DEMO = Path(__file__).resolve().parent.parent / "Modelos/16_Kukulkan/preview/sonidos_demo.mp3"
RNG = np.random.default_rng(1616)


def T(dur):
    return np.arange(int(dur * SR)) / SR


def conch(dur=2.0, hz=146.8):
    return horn(dur, hz, bend=-1.0)


def huehuetl(beats=4, gap=0.32):
    return mixdown(*[(k * gap, (1.0 if k % 2 == 0 else 0.7) * taiko(0.8, 130, 55, 0.4)) for k in range(beats)])


def death_whistle(dur=1.4):
    """Silbato de la muerte: ruido muy agudo con un tono que sube y baja, como un grito."""
    n = int(dur * SR)
    f = curve(n, [(0, 900), (0.3, 1700), (0.7, 1400), (1, 800)])
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR)
    air = bandpass(noise(dur), 900, 4000)
    return (0.5 * tone + 0.8 * air * (0.6 + 0.4 * tone)) * curve(n, [(0, 0), (0.1, 1), (0.8, 0.9), (1, 0)])


def rattle(dur=1.0, rate=18):
    out = np.zeros(int(dur * SR))
    for k in range(int(dur * rate)):
        i = int(k / rate * SR)
        x = bandpass(noise(0.03), 3000, 9000) * env(int(0.03 * SR), 0.001, 0.03, 3)
        out[i:i + len(x)] += x[: len(out) - i] * (0.6 + 0.4 * (k % 2))
    return out


def hiss(dur=1.0):
    n = int(dur * SR)
    return bandpass(noise(dur), 3000, 9000) * curve(n, [(0, 0), (0.15, 1), (0.85, 0.8), (1, 0)])


def wings(dur=0.8, flaps=3):
    return mixdown(*[(k * dur / flaps, 0.6 * whoosh(dur / flaps, 150, 1500)) for k in range(flaps)])


def serpent_voice(dur, pts):
    g = growl(dur, pts, vowel=AA, drv=2.8, rough=26, sub=0.8, breath=0.6)
    return mixdown((0, g), (0, 0.5 * hiss(dur)))


def bird(dur=0.6, f0=2400):
    n = int(dur * SR)
    f = curve(n, [(0, f0), (0.3, f0 * 1.4), (0.5, f0 * 0.9), (1, f0 * 1.2)])
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.01, dur, 2.0, hold=dur * 0.2)


def kk_intro():
    s = mixdown((0, 0.8 * conch(2.4, 110.0)), (1.0, 0.8 * huehuetl(6, 0.3)), (1.4, 0.4 * rattle(2.0)),
                (2.8, death_whistle(1.6)), (3.0, serpent_voice(1.8, [(0, 90), (0.3, 130), (1, 70)])), (3.0, 0.6 * wings(1.2, 4)))
    return reverb(s, 3.6, 0.4)


def kk_roar():
    return reverb(mixdown((0, serpent_voice(1.8, [(0, 100), (0.2, 150), (1, 80)])), (0, 0.6 * wings(1.0, 3))), 2.4, 0.35)


def kk_hurt():
    g = serpent_voice(0.5, [(0, 160), (0.3, 200), (1, 120)])
    return reverb(g * env(len(g), 0.01, 0.5, 1.8, hold=0.1), 1.0, 0.25)


def kk_strike():
    return reverb(mixdown((0, 0.6 * hiss(0.3)), (0.05, 0.6 * whoosh(0.35, 200, 3000)), (0.3, 0.6 * thump(0.5, 140, 50))), 1.0, 0.25)


def kk_screech():
    return reverb(mixdown((0, death_whistle(1.2)), (0, 0.6 * wail(1.2, [(0, 900), (0.2, 1400), (1, 600)], 10)),
                          (0, 0.5 * wings(0.8, 3))), 2.2, 0.4)


def kk_eclipse():
    n = int(1.6 * SR)
    dark = lowpass(noise(1.6), 500) * curve(n, [(0, 0), (0.3, 1), (1, 0)])
    return reverb(mixdown((0, dark), (0, 0.6 * conch(1.6, 73.4)), (0.3, 0.4 * hiss(1.2))), 2.6, 0.4)


def kk_siphon():
    n = int(1.4 * SR)
    rise = np.sin(2 * np.pi * np.cumsum(curve(n, [(0, 300), (1, 1400)])) / SR) * curve(n, [(0, 0), (0.8, 0.6), (1, 0)])
    return reverb(mixdown((0, rise), (0, 0.5 * wings(1.2, 4)), (0.2, 0.4 * rattle(1.0))), 2.0, 0.4)


def kk_altar():
    s = mixdown((0, 0.8 * huehuetl(4, 0.3)), (0, 0.4 * rattle(1.2)), (1.2, thump(1.0, 110, 35)), (1.2, 0.7 * crack(0.3)),
                (1.2, 0.6 * conch(1.4, 110.0)))
    return reverb(s, 2.4, 0.38)


def kk_venom():
    return reverb(mixdown((0, 0.8 * hiss(0.6)), (0.5, 0.6 * crack(0.2)), (0.5, 0.6 * thump(0.5, 140, 50)),
                          (0.5, 0.5 * bubbles(0.6, 10))), 1.6, 0.3)


def kk_solar():
    s = mixdown((0, 0.6 * death_whistle(0.8)), (0.2, 0.7 * conch(1.6, 98.0)), (0.6, thump(1.4, 90, 28)),
                (0.6, 0.6 * rumble(1.6, 18, 140)), (0.6, 0.5 * choir(1.8, [196.0, 246.9, 293.7], vowel=AA, attack=0.05)))
    return reverb(s, 3.0, 0.4)


def kk_sunrays():
    return reverb(mixdown((0, 0.5 * conch(1.0, 146.8)), (0.5, 0.8 * thunder(1.6)), (1.0, 0.7 * thunder(1.4))), 2.6, 0.35)


def kk_summon():
    return reverb(mixdown((0, 0.7 * conch(1.8, 110.0)), (0.3, 0.7 * huehuetl(4, 0.28)), (0.6, 0.5 * wings(1.0, 4)),
                          (0.8, 0.4 * bird(0.6))), 2.6, 0.4)


def kk_phase():
    s = mixdown((0, 0.8 * huehuetl(6, 0.22)), (0.6, 0.6 * rattle(1.4)), (1.2, death_whistle(1.4)),
                (1.2, serpent_voice(1.6, [(0, 90), (0.2, 140), (1, 70)])))
    return reverb(s, 3.2, 0.4)


def kk_death():
    s = mixdown((0, serpent_voice(2.6, [(0, 130), (0.4, 90), (1, 40)])), (0.8, 0.6 * death_whistle(2.0)),
                (1.6, 0.8 * conch(3.0, 73.4)), (2.2, 0.6 * wings(1.4, 5)))
    return reverb(s, 3.8, 0.45)


def quetzal_call():
    return reverb(mixdown((0, 0.6 * bird(0.5, 2200)), (0.5, 0.6 * bird(0.6, 1800)), (0, 0.4 * wings(0.8, 3))), 1.6, 0.35)


def quetzal_peck():
    return reverb(mixdown((0, 0.5 * wings(0.3, 1)), (0.15, 0.6 * crack(0.08)), (0.15, 0.4 * bird(0.2, 3000))), 0.8, 0.2)


def serpent_hiss():
    return reverb(mixdown((0, hiss(0.9)), (0.2, 0.4 * rattle(0.6, 24))), 0.9, 0.2)


def serpent_bite():
    return reverb(mixdown((0, 0.5 * hiss(0.2)), (0.1, 0.7 * crack(0.12)), (0.1, 0.4 * thump(0.3, 180, 80))), 0.7, 0.2)


def offering_chant():
    return reverb(mixdown((0, 0.5 * choir(1.6, [220.0, 277.2], vowel=OO, attack=0.4)), (0, 0.4 * rattle(1.4, 10))), 2.2, 0.45)


def offering_drain():
    n = int(1.0 * SR)
    down = np.sin(2 * np.pi * np.cumsum(curve(n, [(0, 900), (1, 300)])) / SR) * curve(n, [(0, 0), (0.2, 0.6), (1, 0)])
    return reverb(mixdown((0, down), (0, 0.3 * rattle(1.0))), 1.6, 0.35)


def jaguar_roar():
    g = growl(1.0, [(0, 120), (0.3, 170), (1, 90)], vowel=AA, drv=3.4, rough=34, sub=0.9, breath=0.5)
    return reverb(g * env(len(g), 0.02, 1.0, 1.6, hold=0.3), 1.4, 0.3)


def jaguar_slash():
    return reverb(mixdown((0, 0.7 * whoosh(0.35, 200, 3000)), (0.25, 0.6 * crack(0.15)), (0.4, 0.6 * whoosh(0.3, 200, 3000)),
                          (0.6, 0.5 * crack(0.12))), 1.0, 0.2)


SOUNDS = {
    "intro": (kk_intro, 64), "roar": (kk_roar, 56), "hurt": (kk_hurt, 24), "strike": (kk_strike, 24), "screech": (kk_screech, 40),
    "eclipse": (kk_eclipse, 40), "siphon": (kk_siphon, 32), "altar": (kk_altar, 40), "venom": (kk_venom, 32),
    "solar": (kk_solar, 64), "sunrays": (kk_sunrays, 56), "summon": (kk_summon, 48), "phase": (kk_phase, 56),
    "death": (kk_death, 64), "quetzal_call": (quetzal_call, 24), "quetzal_peck": (quetzal_peck, 16),
    "serpent_hiss": (serpent_hiss, 16), "serpent_bite": (serpent_bite, 16), "offering_chant": (offering_chant, 20),
    "offering_drain": (offering_drain, 16), "jaguar_roar": (jaguar_roar, 24), "jaguar_slash": (jaguar_slash, 16),
}

if __name__ == "__main__":
    sndkit.build(BOSS, SOUNDS, DEMO)
