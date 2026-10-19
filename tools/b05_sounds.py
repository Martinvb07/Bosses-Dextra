#!/usr/bin/env python3
"""
Sonidos propios de RAGNAROK y sus subditos (sintetizados): cuerno de guerra (gjallarhorn),
tambores, coro grave, hielo que se rompe, ventisca, truenos y voz de gigante.

  Modelos/DextraBossesPack/assets/dextra/sounds/ragnarok/*.ogg  ->  dextra:ragnarok.<nombre>
  Demo: Modelos/05_Ragnarok/preview/sonidos_demo.mp3

Uso: python3 tools/b05_sounds.py
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import dextra_pack as DP  # noqa: E402
from generate_sounds import (AA, OO, SR, UH, bandpass, choir, crack, curve, debris, env, finish, growl,  # noqa: E402
                             highpass, horn, lowpass, mixdown, noise, reverb, rumble, thump, thunder, to_ogg,
                             whoosh, write_wav)
from b02_sounds import wind  # noqa: E402
from b03_sounds import taiko, wail  # noqa: E402

BOSS = "ragnarok"
DEMO = Path(__file__).resolve().parent.parent / "Modelos/05_Ragnarok/preview/sonidos_demo.mp3"
RNG = np.random.default_rng(505)

D2, A2, D3, F3, A3 = 73.42, 110.0, 146.83, 174.61, 220.0


def T(dur):
    return np.arange(int(dur * SR)) / SR


def shatter(dur=0.9):
    """Hielo que se rompe: chasquido, astillas agudas y tintineo."""
    n = int(dur * SR)
    tinkle = np.zeros(n)
    for k in range(18):
        i = int(RNG.uniform(0, dur * 0.6) * SR)
        f = RNG.uniform(2500, 7000)
        L = min(int(0.12 * SR), n - i)
        tt = np.arange(L) / SR
        tinkle[i:i + L] += np.sin(2 * np.pi * f * tt) * np.exp(-tt * 40) * RNG.uniform(0.2, 0.6)
    return mixdown((0, crack(0.2)), (0, 0.7 * highpass(debris(dur, 120), 1500)), (0.02, 0.5 * tinkle))


def ice_creak(dur=1.0):
    n = int(dur * SR)
    f = curve(n, [(0, 90), (0.5, 140), (1, 70)])
    saw = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (RNG.random(n) < 0.3)
    return bandpass(saw, 200, 2500) * curve(n, [(0, 0), (0.2, 1), (1, 0)])


def giant(dur, f_points, drv=3.0):
    return growl(dur, f_points, vowel=OO, drv=drv, rough=22, sub=1.0)


def drums(beats=4, gap=0.4, big=True):
    return mixdown(*[(k * gap, (0.9 if k % 2 == 0 or not big else 0.6) * taiko(0.9, 100, 42)) for k in range(beats)])


# ---------------------------------------------------------------- boss
def rg_intro():
    s = mixdown((0, 0.5 * wind(5.0, (180, 420))), (0.3, 0.9 * horn(2.6, 87.3, -3)), (0.3, 0.4 * horn(2.6, 130.8, -3)),
                (1.2, 0.45 * choir(3.6, [D2, A2, D3, F3])), (2.6, drums(4, 0.35)), (3.6, 0.9 * thunder(2.6)),
                (3.8, 0.7 * giant(1.8, [(0, 70), (0.2, 95), (1, 50)]) * env(int(1.8 * SR), 0.05, 1.8, 1.5, hold=0.6)))
    return reverb(s, 3.4, 0.3)


def rg_roar():
    g = giant(2.2, [(0, 62), (0.15, 90), (0.6, 82), (1, 48)]) * env(int(2.2 * SR), 0.05, 2.2, 1.4, hold=1.0)
    return reverb(mixdown((0, g), (0, 0.5 * thump(1.4, 80, 30))), 2.6, 0.3)


def rg_hurt():
    g = giant(0.5, [(0, 110), (0.3, 120), (1, 80)], drv=3.4) * env(int(0.5 * SR), 0.01, 0.5, 2.0, hold=0.08)
    return reverb(mixdown((0, g), (0, 0.4 * shatter(0.4))), 0.8, 0.15)


def rg_strike():
    return reverb(mixdown((0, whoosh(0.4, 120, 2000)), (0.2, 0.8 * thump(0.6, 120, 45)), (0.2, 0.7 * shatter(0.7))),
                  1.2, 0.2)


def rg_blow():
    s = mixdown((0, 0.6 * whoosh(0.4, 100, 1500)), (0.3, thump(1.2, 120, 30)), (0.3, crack(0.3)),
                (0.31, shatter(1.2)), (0.3, 0.6 * rumble(1.4, 18, 120)))
    return reverb(s, 2.0, 0.25)


def rg_burst():
    s = mixdown((0, 0.8 * thump(0.9, 140, 40)), (0, shatter(1.2)), (0.05, 0.5 * wind(1.2, (300, 700))))
    return reverb(s, 1.8, 0.25)


def rg_storm():
    s = mixdown((0, 0.7 * wind(2.0, (260, 640))), (0, 0.5 * ice_creak(1.0)),
                *[(0.4 + k * 0.08, 0.35 * shatter(0.6)) for k in range(6)])
    return reverb(s, 2.0, 0.25)


def rg_lightning():
    hum = np.sin(2 * np.pi * 55 * T(1.6)) * 0.4 + bandpass(noise(1.6), 2000, 7000) * 0.2
    hum *= curve(len(hum), [(0, 0), (0.5, 1), (1, 0)])
    s = mixdown((0, hum), (0.5, thunder(2.6)), (0.5, 0.6 * crack(0.4)))
    return reverb(s, 2.6, 0.3)


def rg_ragnarok():
    n = int(2.0 * SR)
    rise = lowpass(noise(2.0), 600) * curve(n, [(0, 0), (1, 1)]) ** 2
    s = mixdown((0, 0.6 * rise), (0, 0.9 * horn(2.0, 73.4, -1)), (0, 0.4 * choir(2.0, [D2, A2, D3], attack=1.2)),
                (0, 0.6 * ice_creak(2.0)), (2.0, thump(2.0, 110, 24)), (2.0, crack(0.5)), (2.0, shatter(2.0)),
                (2.0, 0.8 * thunder(2.8)), (2.0, 0.8 * rumble(2.4, 14, 110)))
    return reverb(s, 3.2, 0.3)


def rg_summon():
    s = mixdown((0, 0.9 * horn(1.8, 98.0, -3)), (0, 0.4 * horn(1.8, 146.8, -3)), (0.9, drums(5, 0.25)))
    return reverb(s, 2.6, 0.3)


def rg_phase():
    s = mixdown((0, 0.5 * choir(2.6, [D2, A2, D3, F3, A3], attack=0.05)), (0.6, thunder(2.4)),
                (1.2, 0.8 * giant(1.4, [(0, 70), (0.3, 105), (1, 60)]) * env(int(1.4 * SR), 0.03, 1.4, 1.5, hold=0.4)))
    return reverb(s, 2.8, 0.3)


def rg_death():
    g = giant(3.0, [(0, 90), (0.3, 80), (1, 34)], drv=2.4) * env(int(3.0 * SR), 0.05, 3.0, 1.8, hold=1.0)
    s = mixdown((0, g), (1.8, shatter(2.0)), (2.2, 0.8 * horn(3.0, 65.4, -1)), (2.4, 0.4 * wind(3.0)))
    return reverb(s, 3.4, 0.32)


# ---------------------------------------------------------------- subditos
def draugr_groan():
    g = growl(1.4, [(0, 90), (0.5, 80), (1, 64)], vowel=UH, drv=2.2, breath=0.6, rough=16)
    return reverb(mixdown((0, g * env(len(g), 0.2, 1.4, 1.5, hold=0.5)), (0, 0.3 * ice_creak(1.2))), 1.4, 0.25)


def draugr_hit():
    return reverb(mixdown((0, 0.6 * whoosh(0.3, 200, 2000)), (0.18, 0.7 * thump(0.4, 140, 60)), (0.18, 0.4 * crack(0.1))),
                  0.8, 0.15)


def valkyrie_cry():
    s = mixdown((0, wail(1.2, [(0, 880), (0.3, 1046), (1, 784)], 6)), (0, 0.3 * shatter(0.6)))
    return reverb(s, 2.2, 0.4)


def valkyrie_strike():
    return reverb(mixdown((0, whoosh(0.25, 800, 7000)), (0.12, 0.5 * shatter(0.4))), 0.9, 0.2)


def viking_shout():
    g = growl(0.9, [(0, 140), (0.2, 180), (1, 130)], vowel=AA, drv=3.0, rough=30)
    return reverb(g * env(len(g), 0.03, 0.9, 1.6, hold=0.4), 1.2, 0.2)


def viking_hit():
    return reverb(mixdown((0, 0.6 * whoosh(0.25, 300, 3000)), (0.15, 0.6 * thump(0.4, 180, 70)),
                          (0.35, 0.5 * whoosh(0.2, 300, 3000)), (0.45, 0.5 * thump(0.3, 160, 70))), 0.9, 0.15)


SOUNDS = {
    "intro": (rg_intro, 64), "roar": (rg_roar, 48), "hurt": (rg_hurt, 24), "strike": (rg_strike, 24),
    "blow": (rg_blow, 32), "burst": (rg_burst, 40), "storm": (rg_storm, 48), "lightning": (rg_lightning, 56),
    "ragnarok": (rg_ragnarok, 64), "summon": (rg_summon, 56), "phase": (rg_phase, 56), "death": (rg_death, 64),
    "draugr_groan": (draugr_groan, 20), "draugr_hit": (draugr_hit, 20), "valkyrie_cry": (valkyrie_cry, 24),
    "valkyrie_strike": (valkyrie_strike, 16), "viking_shout": (viking_shout, 20), "viking_hit": (viking_hit, 20),
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
            print(f"OK dextra:{BOSS}.{name:16s} {len(x) / SR:4.1f} s")
        DP.register_sounds(BOSS, {k: d for k, (_, d) in SOUNDS.items()})
        wav = Path(tmp) / "demo.wav"
        write_wav(wav, np.concatenate(demo))
        DEMO.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-b:a", "128k", str(DEMO)], check=True)
    print("demo ->", DEMO)


if __name__ == "__main__":
    main()
