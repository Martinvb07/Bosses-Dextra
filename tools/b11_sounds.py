#!/usr/bin/env python3
"""
Sonidos propios de AZATHOTH y sus subditos (sintetizados): flautas desafinadas, tambores
sordos del vacio, zumbido cosmico, voces al reves, gorgoteos y estrellas que caen.

  Modelos/DextraBossesPack/assets/dextra/sounds/azathoth/*.ogg  ->  dextra:azathoth.<nombre>
  Demo: Modelos/11_Azathoth/preview/sonidos_demo.mp3

Uso: python3 tools/b11_sounds.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import sndkit  # noqa: E402
from generate_sounds import (AA, OO, SR, bandpass, crack, curve, env, growl, highpass, lowpass,  # noqa: E402
                             mixdown, noise, reverb, rumble, thump, thunder, whoosh)
from b03_sounds import shakuhachi, taiko  # noqa: E402
from b06_sounds import bubbles, squelch, wet_voice  # noqa: E402

BOSS = "azathoth"
DEMO = Path(__file__).resolve().parent.parent / "Modelos/11_Azathoth/preview/sonidos_demo.mp3"
RNG = np.random.default_rng(1111)


def T(dur):
    return np.arange(int(dur * SR)) / SR


def flutes(dur, base=520, count=4):
    """Flautas que no se ponen de acuerdo: tonos cercanos que baten y se desafinan."""
    parts = []
    for k in range(count):
        hz = base * RNG.choice([1, 1.06, 1.12, 1.41, 1.5]) * (1 + RNG.uniform(-0.02, 0.02))
        parts.append((RNG.uniform(0, dur * 0.3), 0.4 * shakuhachi(dur * RNG.uniform(0.6, 0.9), hz, bend=RNG.uniform(-3, 2))))
    return mixdown(*parts)


def drone(dur, hz=41.2):
    t = T(dur)
    x = sum(np.sin(2 * np.pi * hz * r * t + RNG.uniform(0, 6)) * a for r, a in ((1, 1), (1.007, 0.8), (1.5, 0.4), (2.013, 0.3)))
    x *= 1 + 0.3 * np.sin(2 * np.pi * 0.7 * t)
    return x / np.abs(x).max() * curve(len(t), [(0, 0), (0.2, 1), (0.8, 1), (1, 0)])


def void_drums(beats=4, gap=0.5):
    return mixdown(*[(max(0.0, k * gap + RNG.uniform(-0.04, 0.04)), lowpass(taiko(1.0, 80, 34, 0.15), 900)) for k in range(beats)])


def eldritch(dur, f_points, drv=2.4):
    """Voz imposible: gruñido + su copia al reves + gorgoteo."""
    g = growl(dur, f_points, vowel=OO, drv=drv, rough=40, sub=1.0, breath=0.4)
    return mixdown((0, g), (0, 0.5 * g[::-1].copy()), (0, 0.4 * wet_voice(dur, [(p, f * 1.5) for p, f in f_points])))


def stars(dur=1.2, count=10):
    out = np.zeros(int(dur * SR))
    for k in range(count):
        i = int(RNG.uniform(0, dur * 0.7) * SR)
        f = RNG.uniform(1800, 4200)
        tt = T(dur)[: len(out) - i]
        out[i:] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 6) * 0.3
    return out


def az_intro():
    s = mixdown((0, 0.7 * drone(5.0)), (0.3, 0.6 * flutes(3.0)), (1.2, 0.8 * void_drums(4, 0.55)),
                (3.0, eldritch(2.2, [(0, 70), (0.3, 55), (1, 45)])), (3.0, 0.4 * stars(2.0)))
    return reverb(s, 4.0, 0.42)


def az_roar():
    return reverb(mixdown((0, eldritch(2.0, [(0, 80), (0.2, 110), (1, 60)])), (0, 0.4 * drone(2.0, 55))), 3.0, 0.4)


def az_hurt():
    g = mixdown((0, eldritch(0.6, [(0, 120), (0.3, 160), (1, 90)], drv=3.0)), (0, 0.5 * squelch(0.4)))
    return reverb(g * env(len(g), 0.01, len(g) / SR, 1.8, hold=0.1), 1.2, 0.3)


def az_lash():
    return reverb(mixdown((0, 0.7 * whoosh(0.4, 120, 1600)), (0.3, 0.7 * squelch(0.5)), (0.3, 0.5 * thump(0.5, 110, 40))),
                  1.2, 0.25)


def az_blink():
    n = int(0.9 * SR)
    f = curve(n, [(0, 1600), (1, 120)])
    zap = np.sin(2 * np.pi * np.cumsum(f) / SR) * curve(n, [(0, 0), (0.1, 0.6), (1, 0)])
    return reverb(mixdown((0, zap), (0, 0.6 * whoosh(0.6, 200, 4000)[::-1].copy()), (0.5, 0.6 * thump(0.5, 140, 50))), 2.0, 0.4)


def az_pulse():
    return reverb(mixdown((0, 0.6 * drone(1.2, 55)), (0.1, thump(1.0, 90, 30)), (0.1, 0.8 * whoosh(0.9, 80, 1500)),
                          (0.1, 0.4 * stars(0.8))), 2.4, 0.38)


def az_collapse():
    s = mixdown((0, 0.6 * eldritch(0.8, [(0, 100), (1, 140)])), (0.5, thump(1.4, 90, 28)), (0.5, 0.8 * rumble(1.8, 18, 140)),
                (0.5, 0.6 * lowpass(crack(0.5), 4000)), (0.6, 0.5 * bubbles(1.2, 12)))
    return reverb(s, 2.6, 0.36)


def az_gaze():
    n = int(1.4 * SR)
    swell = drone(1.4, 82.4) * curve(n, [(0, 0), (0.35, 1), (0.4, 0.2), (1, 0)])
    return reverb(mixdown((0, swell), (0.1, 0.5 * flutes(0.6, 900, 3)), (0.5, crack(0.3)), (0.5, 0.6 * stars(0.8, 14))),
                  2.4, 0.4)


def az_storm():
    return reverb(mixdown((0, drone(3.0, 36.7)), (0, 0.6 * lowpass(rumble(3.0, 20, 200), 800)), (0.3, 0.5 * flutes(2.4, 380)),
                          (0.5, 0.4 * stars(2.0, 16))), 3.0, 0.42)


def az_warp():
    n = int(1.2 * SR)
    f = curve(n, [(0, 60), (0.4, 400), (1, 60)])
    suck = np.sin(2 * np.pi * np.cumsum(f) / SR) * curve(n, [(0, 0), (0.35, 0.8), (0.4, 0.1), (1, 0)])
    return reverb(mixdown((0, suck), (0, 0.6 * whoosh(0.45, 200, 3000)[::-1].copy()), (0.4, thump(0.8, 120, 30)),
                          (0.4, 0.5 * eldritch(0.8, [(0, 90), (1, 70)]))), 2.4, 0.38)


def az_rift():
    n = int(1.0 * SR)
    tear = bandpass(noise(1.0), 400, 6000) * curve(n, [(0, 0), (0.85, 1), (1, 0)]) ** 2
    s = mixdown((0, 0.6 * tear), (0, 0.5 * drone(1.0, 98)), (0.9, 0.9 * thunder(2.4)), (0.9, thump(1.2, 80, 26)),
                (0.95, 0.5 * eldritch(1.4, [(0, 70), (1, 50)])))
    return reverb(s, 3.2, 0.4)


def az_skyfall():
    return reverb(mixdown((0, stars(1.4, 18)), (0.2, 0.6 * whoosh(0.6, 800, 7000)), (0.7, thump(0.6, 160, 60)),
                          (0.7, 0.5 * crack(0.2))), 2.2, 0.4)


def az_summon():
    s = mixdown((0, 0.7 * void_drums(3, 0.4)), (0.2, 0.7 * bubbles(1.6, 18)), (0.4, 0.5 * flutes(1.8, 440)),
                (0.8, 0.6 * eldritch(1.2, [(0, 90), (1, 110)])))
    return reverb(s, 2.8, 0.4)


def az_phase():
    s = mixdown((0, 0.8 * drone(3.0, 41.2)), (0.4, 0.6 * flutes(2.2, 600, 5)), (1.0, 0.9 * void_drums(3, 0.3)),
                (1.6, eldritch(1.8, [(0, 60), (0.2, 100), (1, 50)])))
    return reverb(s, 3.4, 0.42)


def az_death():
    s = mixdown((0, eldritch(3.0, [(0, 110), (0.4, 70), (1, 30)], drv=2.0)), (0.5, 0.7 * drone(3.0, 30.9)),
                (1.0, 0.5 * flutes(2.4, 300)), (2.0, 0.6 * stars(2.0, 20)), (2.2, 0.8 * thump(1.4, 70, 24)))
    return reverb(s, 4.0, 0.45)


def spawn_gurgle():
    return reverb(mixdown((0, wet_voice(0.8, [(0, 140), (0.5, 110), (1, 90)])), (0, 0.5 * bubbles(0.8, 8))), 1.2, 0.3)


def spawn_lash():
    return reverb(mixdown((0, 0.6 * whoosh(0.3, 200, 2500)), (0.2, 0.7 * squelch(0.4))), 0.8, 0.2)


def piper_tune():
    return reverb(flutes(1.6, 660, 3), 2.0, 0.45)


def piper_curse():
    return reverb(mixdown((0, flutes(1.0, 990, 4)), (0.1, 0.4 * stars(0.8, 6))), 1.6, 0.4)


def larva_chitter():
    out = np.zeros(int(0.8 * SR))
    for k in range(10):
        i = int(k * 0.07 * SR)
        x = bandpass(noise(0.03), 2500, 7000) * env(int(0.03 * SR), 0.001, 0.03, 3)
        out[i:i + len(x)] += x * RNG.uniform(0.4, 1.0)
    return reverb(out, 0.8, 0.2)


def larva_bite():
    return reverb(mixdown((0, 0.6 * crack(0.12)), (0.04, 0.6 * squelch(0.35)), (0.06, 0.4 * larva_chitter()[: int(0.3 * SR)])),
                  0.8, 0.2)


def priest_chant():
    g = growl(1.6, [(0, 110), (0.5, 98), (1, 110)], vowel=AA, drv=1.6, rough=6, sub=0.4, breath=0.2)
    return reverb(mixdown((0, 0.6 * g), (0, 0.4 * drone(1.6, 110))), 2.4, 0.45)


def priest_heal():
    return reverb(mixdown((0, stars(1.2, 12)), (0, 0.5 * drone(1.2, 220))), 2.0, 0.45)


SOUNDS = {
    "intro": (az_intro, 64), "roar": (az_roar, 56), "hurt": (az_hurt, 24), "lash": (az_lash, 24), "blink": (az_blink, 32),
    "pulse": (az_pulse, 40), "collapse": (az_collapse, 48), "gaze": (az_gaze, 40), "storm": (az_storm, 56),
    "warp": (az_warp, 48), "rift": (az_rift, 64), "skyfall": (az_skyfall, 40), "summon": (az_summon, 48),
    "phase": (az_phase, 64), "death": (az_death, 64), "spawn_gurgle": (spawn_gurgle, 16), "spawn_lash": (spawn_lash, 16),
    "piper_tune": (piper_tune, 24), "piper_curse": (piper_curse, 20), "larva_chitter": (larva_chitter, 16),
    "larva_bite": (larva_bite, 16), "priest_chant": (priest_chant, 20), "priest_heal": (priest_heal, 20),
}

if __name__ == "__main__":
    sndkit.build(BOSS, SOUNDS, DEMO)
