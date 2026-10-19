#!/usr/bin/env python3
"""
Sonidos propios de NEZARETH y sus subditos (sintetizados): patas de arana que repiquetean,
hilos que se tensan y chasquean, seda que se desgarra, susurros, una caja de musica
desafinada y el chillido de la reina.

  Modelos/DextraBossesPack/assets/dextra/sounds/nezareth/*.ogg  ->  dextra:nezareth.<nombre>
  Demo: Modelos/17_Nezareth/preview/sonidos_demo.mp3

Uso: python3 tools/b17_sounds.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import sndkit  # noqa: E402
from generate_sounds import (AA, OO, SR, bandpass, crack, curve, env, growl, highpass, lowpass,  # noqa: E402
                             mixdown, noise, reverb, rumble, thump, whoosh)
from b03_sounds import wail  # noqa: E402
from b04_sounds import clank  # noqa: E402
from b07_sounds import whisper  # noqa: E402

BOSS = "nezareth"
DEMO = Path(__file__).resolve().parent.parent / "Modelos/17_Nezareth/preview/sonidos_demo.mp3"
RNG = np.random.default_rng(1717)


def T(dur):
    return np.arange(int(dur * SR)) / SR


def skitter(dur=1.0, rate=22):
    """Patas de arana: clics secos muy seguidos."""
    out = np.zeros(int(dur * SR))
    for k in range(int(dur * rate)):
        i = int((k / rate + RNG.uniform(0, 0.01)) * SR)
        x = bandpass(noise(0.015), 1500, 6000) * env(int(0.015 * SR), 0.0005, 0.015, 3)
        out[i:i + len(x)] += x[: len(out) - i] * RNG.uniform(0.4, 1.0)
    return out


def string_snap(hz=180, dur=0.8):
    """Hilo tenso que se suelta: cuerda pulsada grave con chasquido."""
    t = T(dur)
    x = sum(np.sin(2 * np.pi * hz * k * t) * np.exp(-t * (3 + 2 * k)) / k for k in (1, 2, 3, 5))
    return mixdown((0, 0.7 * x), (0, 0.5 * crack(0.05)))


def stretch(dur=0.6, f0=120, f1=420):
    n = int(dur * SR)
    f = curve(n, [(0, f0), (1, f1)])
    saw = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (RNG.random(n) < 0.35)
    return bandpass(saw, 300, 3000) * curve(n, [(0, 0), (0.3, 1), (1, 1)])


def tear(dur=0.6):
    n = int(dur * SR)
    return bandpass(noise(dur), 800, 6000) * (RNG.random(n) < 0.5) * env(n, 0.01, dur, 1.6)


def music_box(dur=2.0, notes=(784, 740, 659, 622, 587)):
    out = np.zeros(int(dur * SR))
    for k, f in enumerate(notes):
        i = int(k * dur / len(notes) * SR)
        tt = T(dur)[: len(out) - i]
        out[i:] += (np.sin(2 * np.pi * f * 0.99 * tt) + 0.4 * np.sin(2 * np.pi * f * 3.01 * tt)) * np.exp(-tt * 3) * 0.4
    return out


def queen(dur, pts, drv=2.6):
    g = growl(dur, pts, vowel=AA, drv=drv, rough=30, sub=0.6, breath=0.6)
    return mixdown((0, g), (0, 0.4 * whisper(dur)))


def nz_intro():
    s = mixdown((0, 0.6 * music_box(2.4)), (0.4, 0.6 * whisper(2.0)), (1.6, 0.8 * skitter(1.6, 26)), (2.4, 0.8 * stretch(0.8)),
                (3.1, string_snap(140, 1.2)), (3.2, queen(1.8, [(0, 300), (0.3, 420), (1, 220)])))
    return reverb(s, 3.4, 0.4)


def nz_roar():
    return reverb(mixdown((0, queen(1.6, [(0, 320), (0.2, 480), (1, 260)])), (0, 0.5 * wail(1.6, [(0, 900), (0.3, 1300), (1, 600)], 10)),
                          (0.1, 0.4 * skitter(1.0))), 2.4, 0.38)


def nz_hurt():
    g = queen(0.5, [(0, 360), (0.3, 480), (1, 300)])
    return reverb(g * env(len(g), 0.01, 0.5, 1.8, hold=0.1), 1.0, 0.3)


def nz_claw():
    return reverb(mixdown((0, 0.6 * whoosh(0.3, 500, 5000)), (0.2, 0.6 * clank(0.3, 1500)), (0.22, 0.4 * tear(0.3))), 1.0, 0.25)


def nz_tug():
    s = mixdown((0, stretch(0.4, 100, 500)), (0.4, string_snap(110, 1.0)), (0.4, thump(1.0, 100, 32)),
                (0.45, 0.6 * skitter(0.6)), (0.5, 0.5 * rumble(1.0, 20, 140)))
    return reverb(s, 2.0, 0.32)


def nz_smash():
    return reverb(mixdown((0, 0.5 * whoosh(0.3, 300, 3000)), (0.25, thump(0.8, 120, 40)), (0.25, 0.7 * clank(0.4, 1200)),
                          (0.3, 0.6 * whoosh(0.3, 300, 3000))), 1.4, 0.25)


def nz_cocoon():
    return reverb(mixdown((0, 0.6 * stretch(0.5, 200, 600)), (0.1, 0.6 * whoosh(0.4, 200, 2000)), (0.5, thump(0.6, 130, 50)),
                          (0.5, 0.5 * tear(0.4))), 1.8, 0.3)


def nz_rain():
    return reverb(mixdown(*[(0.3 + 0.08 * k, 0.6 * thump(0.4, 140, 55)) for k in range(6)], (0, 0.6 * stretch(0.6)),
                          (0.3, 0.5 * tear(0.8))), 2.0, 0.32)


def nz_web():
    return reverb(mixdown((0, string_snap(220, 1.0)), (0, string_snap(330, 1.0)), (0.02, 0.6 * tear(0.5)),
                          (0, 0.5 * whoosh(0.6, 400, 4000))), 2.0, 0.35)


def nz_silk():
    return reverb(mixdown((0, 0.6 * whisper(2.6)), (0, 0.6 * lowpass(noise(2.6), 1200) * curve(int(2.6 * SR), [(0, 0), (0.3, 1), (1, 0)])),
                          (0.3, 0.5 * music_box(2.0, (523, 494, 466, 440)))), 2.8, 0.42)


def nz_shield():
    return reverb(mixdown((0, 0.7 * stretch(2.2, 80, 300)), (0, 0.4 * whisper(2.2)), (2.3, tear(0.8)), (2.3, string_snap(160, 0.8))),
                  2.4, 0.38)


def nz_summon():
    return reverb(mixdown((0, 0.6 * music_box(1.6, (659, 698, 622))), (0.2, 0.7 * skitter(1.2, 30)), (0.6, 0.6 * stretch(0.6))),
                  2.4, 0.4)


def nz_phase():
    s = mixdown((0, 0.7 * stretch(1.2, 80, 400)), (1.2, string_snap(100, 1.4)), (1.2, queen(1.6, [(0, 280), (0.2, 460), (1, 240)])),
                (1.2, 0.6 * skitter(1.2)))
    return reverb(s, 3.0, 0.4)


def nz_death():
    s = mixdown((0, queen(2.4, [(0, 400), (0.4, 260), (1, 120)], drv=2.0)), (0.6, 0.8 * skitter(2.0, 14)),
                (1.6, 0.6 * music_box(2.4, (587, 554, 523, 494, 466))), (2.0, string_snap(90, 1.6)))
    return reverb(s, 3.6, 0.45)


def puppet_creak():
    n = int(0.8 * SR)
    f = curve(n, [(0, 80), (0.5, 140), (1, 70)])
    c = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (RNG.random(n) < 0.3)
    return reverb(mixdown((0, bandpass(c, 200, 2000) * curve(n, [(0, 0), (0.2, 1), (1, 0)])), (0.3, 0.5 * music_box(0.6, (880, 830)))),
                  1.0, 0.3)


def puppet_hit():
    return reverb(mixdown((0, 0.6 * whoosh(0.3, 200, 2000)), (0.2, 0.7 * clank(0.3, 600)), (0.2, 0.4 * crack(0.1))), 0.9, 0.2)


def spinner_hum():
    g = growl(1.2, [(0, 196), (0.5, 185), (1, 196)], vowel=OO, drv=1.4, rough=4, sub=0.2, breath=0.3)
    return reverb(mixdown((0, 0.6 * g), (0, 0.4 * whisper(1.2))), 2.0, 0.45)


def spinner_snip():
    return reverb(mixdown((0, 0.6 * clank(0.2, 2400)), (0.12, 0.8 * clank(0.25, 2800)), (0.12, 0.4 * tear(0.2))), 0.9, 0.25)


def moth_flutter():
    out = np.zeros(int(0.8 * SR))
    for k in range(16):
        i = int(k * 0.05 * SR)
        x = lowpass(noise(0.04), 800) * env(int(0.04 * SR), 0.005, 0.04, 2)
        out[i:i + len(x)] += x[: len(out) - i]
    return reverb(out, 1.0, 0.3)


def moth_bite():
    return reverb(mixdown((0, 0.5 * moth_flutter()[: int(0.3 * SR)]), (0.15, 0.6 * crack(0.08))), 0.8, 0.25)


SOUNDS = {
    "intro": (nz_intro, 64), "roar": (nz_roar, 56), "hurt": (nz_hurt, 24), "claw": (nz_claw, 24), "tug": (nz_tug, 48),
    "smash": (nz_smash, 32), "cocoon": (nz_cocoon, 40), "rain": (nz_rain, 48), "web": (nz_web, 40), "silk": (nz_silk, 56),
    "shield": (nz_shield, 48), "summon": (nz_summon, 48), "phase": (nz_phase, 56), "death": (nz_death, 64),
    "puppet_creak": (puppet_creak, 16), "puppet_hit": (puppet_hit, 16), "spinner_hum": (spinner_hum, 20),
    "spinner_snip": (spinner_snip, 16), "moth_flutter": (moth_flutter, 16), "moth_bite": (moth_bite, 16),
}

if __name__ == "__main__":
    sndkit.build(BOSS, SOUNDS, DEMO)
