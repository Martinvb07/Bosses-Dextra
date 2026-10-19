#!/usr/bin/env python3
"""
Sonidos propios de MUSHLORD y sus subditos (sintetizados): voz humeda de hongo, esporas que
revientan, chapoteos, burbujas, madera y raices que crujen y un coro inquietante.

  Modelos/DextraBossesPack/assets/dextra/sounds/mushlord/*.ogg  ->  dextra:mushlord.<nombre>
  Demo: Modelos/06_Mushlord/preview/sonidos_demo.mp3

Uso: python3 tools/b06_sounds.py
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import dextra_pack as DP  # noqa: E402
from generate_sounds import (OO, SR, UH, bandpass, choir, crack, curve, debris, env, finish, growl,  # noqa: E402
                             highpass, lowpass, mixdown, noise, reverb, rumble, thump, to_ogg, whoosh, write_wav)
from b04_sounds import splat  # noqa: E402

BOSS = "mushlord"
DEMO = Path(__file__).resolve().parent.parent / "Modelos/06_Mushlord/preview/sonidos_demo.mp3"
RNG = np.random.default_rng(606)


def T(dur):
    return np.arange(int(dur * SR)) / SR


def puff(dur=0.4, lo=300, hi=3000):
    """Espora que revienta: soplo suave con ataque blando."""
    n = int(dur * SR)
    return bandpass(noise(dur), lo, hi) * env(n, 0.01, dur, 2.5)


def squelch(dur=0.5):
    n = int(dur * SR)
    f = curve(n, [(0, 200), (0.3, 90), (1, 60)])
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.005, dur, 3)
    return mixdown((0, 0.6 * tone), (0, splat(dur)))


def bubbles(dur=1.5, count=14):
    n = int(dur * SR)
    out = np.zeros(n)
    for k in range(count):
        i = int(RNG.uniform(0, dur * 0.85) * SR)
        f0 = RNG.uniform(180, 520)
        L = min(int(0.09 * SR), n - i)
        tt = np.arange(L) / SR
        out[i:i + L] += np.sin(2 * np.pi * f0 * (1 + 8 * tt) * tt) * np.exp(-tt * 45) * RNG.uniform(0.4, 0.9)
    return out


def creak(dur=1.0, f0=70):
    """Madera / raices que crujen."""
    n = int(dur * SR)
    f = curve(n, [(0, f0), (0.5, f0 * 1.6), (1, f0 * 0.9)])
    clicks = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (RNG.random(n) < 0.25)
    return bandpass(clicks, 150, 1800) * curve(n, [(0, 0), (0.2, 1), (1, 0)])


def wet_voice(dur, f_points, drv=2.6):
    g = growl(dur, f_points, vowel=UH, drv=drv, rough=14, sub=0.8, breath=0.5)
    return lowpass(g, 2600, 2)


def eerie(dur, notes, attack=0.6):
    return choir(dur, notes, vowel=OO, attack=attack)


# ---------------------------------------------------------------- boss
def ms_intro():
    s = mixdown((0, 0.5 * eerie(4.5, [98.0, 103.8, 146.8, 155.6])), (0.3, 0.6 * bubbles(3.0, 30)),
                (1.0, 0.6 * creak(2.0, 60)), (2.6, squelch(0.8)), (2.8, 0.8 * thump(1.4, 80, 32)),
                (2.8, 0.7 * wet_voice(1.8, [(0, 70), (0.2, 90), (1, 50)]) * env(int(1.8 * SR), 0.05, 1.8, 1.5, hold=0.6)))
    return reverb(s, 3.0, 0.32)


def ms_roar():
    g = wet_voice(2.0, [(0, 70), (0.15, 100), (0.6, 90), (1, 55)]) * env(int(2.0 * SR), 0.05, 2.0, 1.4, hold=0.9)
    return reverb(mixdown((0, g), (0, 0.5 * bubbles(1.6, 12))), 2.4, 0.3)


def ms_hurt():
    g = wet_voice(0.45, [(0, 120), (0.3, 130), (1, 90)], drv=3.0) * env(int(0.45 * SR), 0.01, 0.45, 2.0, hold=0.08)
    return reverb(mixdown((0, g), (0, 0.5 * squelch(0.4))), 0.8, 0.15)


def ms_swipe():
    return reverb(mixdown((0, whoosh(0.35, 200, 2500)), (0.15, squelch(0.5))), 1.0, 0.18)


def ms_bolt():
    n = int(0.4 * SR)
    fall = bandpass(noise(0.4), 500, 4000) * curve(n, [(0, 0), (1, 1)])
    return reverb(mixdown((0, 0.5 * fall), (0.4, squelch(0.6)), (0.4, puff(0.8, 200, 2500))), 1.4, 0.25)


def ms_burst():
    s = mixdown((0, thump(0.8, 120, 42)), (0, squelch(0.7)), *[(0.05 + k * 0.05, 0.5 * puff(0.5)) for k in range(6)])
    return reverb(s, 1.6, 0.25)


def ms_cloud():
    n = int(1.6 * SR)
    hiss = bandpass(noise(1.6), 400, 5000) * curve(n, [(0, 0), (0.3, 1), (1, 0)])
    return reverb(mixdown((0, hiss), (0, 0.4 * bubbles(1.4, 10)), (0.1, 0.4 * wet_voice(1.0, [(0, 90), (1, 70)]))),
                  2.0, 0.3)


def ms_nova():
    n = int(0.5 * SR)
    swell = bandpass(noise(0.5), 300, 3000) * curve(n, [(0, 0), (1, 1)]) ** 2
    s = mixdown((0, 0.6 * swell), (0.5, thump(1.2, 110, 34)), (0.5, squelch(1.0)), (0.5, 0.8 * puff(1.6, 200, 4000)),
                (0.5, 0.5 * eerie(1.6, [146.8, 155.6, 207.7], attack=0.02)))
    return reverb(s, 2.2, 0.3)


def ms_surge():
    s = mixdown((0, creak(1.0, 50)), (0, 0.6 * rumble(1.2, 20, 140)), (0.5, thump(1.0, 120, 36)),
                (0.5, 0.7 * debris(1.2, 80)))
    return reverb(s, 1.8, 0.25)


def ms_sentence():
    n = int(1.2 * SR)
    rise = np.sin(2 * np.pi * np.cumsum(curve(n, [(0, 220), (1, 660)])) / SR) * curve(n, [(0, 0), (1, 0.6)])
    s = mixdown((0, rise), (0, 0.5 * bubbles(1.2, 16)), (1.2, thump(1.2, 110, 30)), (1.2, squelch(1.0)),
                (1.2, 0.8 * puff(1.4, 150, 3000)))
    return reverb(s, 2.2, 0.3)


def ms_eruption():
    s = mixdown((0, thump(1.8, 110, 24)), (0, crack(0.4)), (0, squelch(1.4)), (0.05, puff(2.4, 100, 3500)),
                (0, 0.8 * rumble(2.4, 14, 110)), (0.2, 0.6 * bubbles(2.0, 24)))
    return reverb(s, 3.0, 0.3)


def ms_cocoon():
    s = mixdown((0, 0.7 * creak(0.6, 80)), (0, 0.5 * bubbles(0.6, 8)), (0.6, squelch(0.8)), (0.6, 0.7 * crack(0.25)),
                (0.6, 0.5 * eerie(1.4, [98.0, 146.8, 196.0], attack=0.02)))
    return reverb(s, 2.2, 0.3)


def ms_summon():
    s = mixdown((0, 0.5 * eerie(2.4, [98.0, 103.8, 146.8])), (0.2, creak(1.4, 60)), (0.4, 0.7 * bubbles(1.6, 18)),
                *[(0.6 + k * 0.15, 0.4 * puff(0.4)) for k in range(5)])
    return reverb(s, 2.6, 0.3)


def ms_death():
    g = wet_voice(2.6, [(0, 90), (0.3, 80), (1, 36)], drv=2.2) * env(int(2.6 * SR), 0.05, 2.6, 1.8, hold=0.9)
    s = mixdown((0, g), (1.4, squelch(1.2)), (1.6, puff(2.4, 150, 3000)), (1.8, 0.5 * eerie(3.0, [98.0, 146.8], 1.0)))
    return reverb(s, 3.4, 0.32)


# ---------------------------------------------------------------- subditos
def zombie_groan():
    g = growl(1.3, [(0, 100), (0.5, 88), (1, 72)], vowel=UH, drv=2.2, breath=0.5, rough=16)
    return reverb(mixdown((0, g * env(len(g), 0.15, 1.3, 1.5, hold=0.4)), (0.3, 0.3 * bubbles(0.8, 5))), 1.2, 0.2)


def zombie_hit():
    return reverb(mixdown((0, 0.6 * whoosh(0.25, 300, 2500)), (0.15, squelch(0.4))), 0.8, 0.15)


def creeper_swell():
    n = int(0.9 * SR)
    hiss = bandpass(noise(0.9), 1500, 7000) * curve(n, [(0, 0.2), (1, 1)])
    return reverb(mixdown((0, hiss), (0, 0.6 * bubbles(0.9, 14))), 0.8, 0.15)


def creeper_pop():
    return reverb(mixdown((0, thump(1.0, 130, 40)), (0, crack(0.2)), (0, squelch(0.8)), (0.02, puff(1.6, 150, 3500))),
                  2.0, 0.25)


def spore_squeak():
    n = int(0.3 * SR)
    f = curve(n, [(0, 1200), (0.5, 1700), (1, 1000)])
    return reverb(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.01, 0.3, 2) * 0.6, 0.6, 0.2)


def spore_pop():
    return reverb(mixdown((0, puff(0.6, 300, 4000)), (0, 0.4 * squelch(0.3))), 1.0, 0.2)


def zone_bubble():
    return reverb(bubbles(1.6, 18), 0.8, 0.15)


SOUNDS = {
    "intro": (ms_intro, 64), "roar": (ms_roar, 48), "hurt": (ms_hurt, 24), "swipe": (ms_swipe, 24),
    "bolt": (ms_bolt, 32), "burst": (ms_burst, 40), "cloud": (ms_cloud, 40), "nova": (ms_nova, 48),
    "surge": (ms_surge, 48), "sentence": (ms_sentence, 40), "eruption": (ms_eruption, 64), "cocoon": (ms_cocoon, 48),
    "summon": (ms_summon, 56), "death": (ms_death, 64), "zombie_groan": (zombie_groan, 20),
    "zombie_hit": (zombie_hit, 20), "creeper_swell": (creeper_swell, 20), "creeper_pop": (creeper_pop, 32),
    "spore_squeak": (spore_squeak, 16), "spore_pop": (spore_pop, 16), "zone_bubble": (zone_bubble, 12),
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
