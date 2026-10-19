#!/usr/bin/env python3
"""
Sonidos propios de LADY OF LAMENTS y sus subditos (sintetizados): coro soprano, lamentos,
campanillas de amatista, organo, susurros, latidos y truenos.

  Modelos/DextraBossesPack/assets/dextra/sounds/lady_of_laments/*.ogg  ->  dextra:lady_of_laments.<nombre>
  Demo: Modelos/07_LadyOfLaments/preview/sonidos_demo.mp3

Uso: python3 tools/b07_sounds.py
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import dextra_pack as DP  # noqa: E402
from generate_sounds import (AA, OO, SR, bandpass, choir, crack, curve, env, finish, growl, lowpass,  # noqa: E402
                             mixdown, noise, reverb, rumble, thump, thunder, to_ogg, whoosh, write_wav)
from b03_sounds import bell, wail  # noqa: E402
from b04_sounds import heartbeat, organ, clank  # noqa: E402

BOSS = "lady_of_laments"
DEMO = Path(__file__).resolve().parent.parent / "Modelos/07_LadyOfLaments/preview/sonidos_demo.mp3"
RNG = np.random.default_rng(707)
NOTES = [293.66, 349.23, 440.0, 523.25, 587.33]          # Re menor


def T(dur):
    return np.arange(int(dur * SR)) / SR


def chime(dur=1.6, count=6, base=1200):
    out = np.zeros(int(dur * SR))
    for k in range(count):
        i = int(RNG.uniform(0, dur * 0.5) * SR)
        f = base * RNG.choice([1, 1.25, 1.5, 2, 2.5])
        t = T(dur)[: len(out) - i]
        out[i:] += sum(np.sin(2 * np.pi * f * r * t) * np.exp(-t * (4 + 3 * r)) for r in (1, 2.76)) * 0.4
    return out


def whisper(dur=1.4):
    n = int(dur * SR)
    x = bandpass(noise(dur), 1500, 6000)
    return x * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 3.3 * T(dur)))) * curve(n, [(0, 0), (0.2, 1), (1, 0)])


def soprano(dur, notes, attack=0.4):
    return choir(dur, notes, vowel=AA, attack=attack, vib=6.0)


def ll_intro():
    s = mixdown((0, 0.8 * bell(4.0, 110.0)), (0.3, 0.6 * whisper(2.0)), (0.6, 0.5 * soprano(4.0, NOTES[:3])),
                (1.2, 0.5 * chime(2.0, 8)), (2.6, 0.9 * wail(2.2, [(0, 700), (0.3, 980), (1, 520)], 6)),
                (2.6, 0.5 * organ(2.4, [73.4, 87.3, 110.0], 0.1)))
    return reverb(s, 3.4, 0.4)


def ll_roar():
    return reverb(mixdown((0, wail(2.0, [(0, 600), (0.2, 1100), (1, 500)], 7)), (0, 0.4 * soprano(2.0, NOTES[1:4], 0.1))),
                  2.6, 0.4)


def ll_hurt():
    return reverb(wail(0.5, [(0, 900), (0.4, 1100), (1, 700)], 12) * env(int(0.5 * SR), 0.01, 0.5, 2, hold=0.1), 1.0, 0.3)


def ll_wail():
    s = mixdown((0, wail(1.6, [(0, 800), (0.2, 1300), (1, 600)], 9)), (0, 0.4 * soprano(1.6, NOTES[2:5], 0.05)),
                (0.1, 0.4 * whoosh(1.0, 300, 3000)))
    return reverb(s, 2.4, 0.4)


def ll_shroud():
    n = int(1.6 * SR)
    dark = lowpass(noise(1.6), 600) * curve(n, [(0, 0), (0.3, 1), (1, 0)])
    return reverb(mixdown((0, dark), (0, 0.6 * whisper(1.6)), (0.4, 0.5 * organ(1.2, [73.4, 77.8], 0.05))), 2.4, 0.4)


def ll_siphon():
    n = int(1.4 * SR)
    f = curve(n, [(0, 300), (1, 1400)])
    rise = np.sin(2 * np.pi * np.cumsum(f) / SR) * curve(n, [(0, 0), (0.8, 0.6), (1, 0)])
    return reverb(mixdown((0, rise), (0, 0.5 * whisper(1.4)), (0.4, 0.4 * chime(1.0, 5, 1600))), 2.0, 0.4)


def ll_mark():
    s = mixdown((0, 0.8 * heartbeat(3, 0.4)), (0, 0.5 * chime(1.2, 6)), (1.2, crack(0.3)), (1.2, 0.7 * chime(1.4, 12, 900)),
                (1.2, 0.6 * thump(0.8, 120, 50)))
    return reverb(s, 2.2, 0.35)


def ll_sorrow():
    s = mixdown((0, 0.5 * soprano(1.2, [NOTES[0], NOTES[1]], 0.3)), (0.5, crack(0.3)), (0.5, chime(1.2, 14, 1000)),
                (0.5, 0.5 * thump(0.6, 140, 50)))
    return reverb(s, 2.0, 0.35)


def ll_lament():
    n = int(0.6 * SR)
    swell = bandpass(noise(0.6), 400, 4000) * curve(n, [(0, 0), (1, 1)]) ** 2
    s = mixdown((0, 0.5 * swell), (0, 0.5 * soprano(2.4, NOTES, 0.3)),
                (0.55, wail(2.0, [(0, 600), (0.15, 1200), (1, 400)], 8)), (0.6, thump(1.4, 100, 30)),
                (0.6, 0.6 * rumble(1.6, 18, 140)))
    return reverb(s, 3.0, 0.4)


def ll_storm():
    return reverb(mixdown((0, 0.6 * thunder(2.4)), (0.5, 0.5 * chime(1.4, 10, 1400)), (1.0, 0.6 * crack(0.4))), 2.6, 0.35)


def ll_summon():
    s = mixdown((0, 0.8 * bell(3.0, 146.8)), (0.2, 0.5 * soprano(2.4, NOTES[:3], 0.5)), (0.4, 0.5 * whisper(1.6)),
                (0.8, 0.4 * chime(1.6, 8)))
    return reverb(s, 3.0, 0.4)


def ll_phase():
    s = mixdown((0, 0.6 * organ(2.4, [73.4, 87.3, 110.0, 146.8], 0.03)), (1.2, wail(1.6, [(0, 700), (0.2, 1200), (1, 500)], 7)),
                (1.2, 0.5 * thunder(2.0)))
    return reverb(s, 3.0, 0.4)


def ll_death():
    s = mixdown((0, wail(3.0, [(0, 900), (0.3, 700), (1, 220)], 5)), (0.5, 0.5 * soprano(3.0, NOTES[:3], 1.0)),
                (2.0, 0.6 * chime(2.4, 16, 1000)), (2.0, 0.6 * bell(4.0, 98.0)))
    return reverb(s, 3.6, 0.42)


def banshee_scream():
    return reverb(wail(0.9, [(0, 1000), (0.2, 1500), (1, 800)], 14), 1.6, 0.4)


def banshee_hit():
    return reverb(mixdown((0, 0.6 * wail(0.4, [(0, 1200), (1, 700)], 16)), (0, 0.4 * whoosh(0.3, 800, 5000))), 1.0, 0.3)


def shadow_growl():
    g = growl(0.8, [(0, 140), (0.5, 120), (1, 100)], vowel=OO, drv=3.0, rough=40, breath=0.6)
    return reverb(lowpass(g, 2000) * env(len(g), 0.05, 0.8, 1.6, hold=0.3), 1.0, 0.25)


def shadow_bite():
    return reverb(mixdown((0, 0.5 * whoosh(0.2, 400, 4000)), (0.12, 0.6 * crack(0.12)), (0.12, 0.4 * thump(0.3, 200, 90))),
                  0.6, 0.15)


def spirit_moan():
    return reverb(mixdown((0, 0.6 * wail(1.4, [(0, 400), (0.5, 330), (1, 280)], 5)), (0, 0.3 * chime(1.0, 4, 800))), 2.2, 0.45)


def spirit_drain():
    n = int(1.0 * SR)
    f = curve(n, [(0, 900), (1, 300)])
    down = np.sin(2 * np.pi * np.cumsum(f) / SR) * curve(n, [(0, 0), (0.2, 0.6), (1, 0)])
    return reverb(mixdown((0, down), (0, 0.4 * whisper(1.0))), 1.6, 0.35)


def vindicator_grunt():
    g = growl(0.6, [(0, 130), (0.3, 160), (1, 110)], vowel=AA, drv=3.0, rough=28)
    return reverb(g * env(len(g), 0.02, 0.6, 1.8, hold=0.2), 0.9, 0.2)


def vindicator_chop():
    return reverb(mixdown((0, 0.7 * whoosh(0.4, 120, 1800)), (0.35, thump(0.6, 140, 45)), (0.35, 0.5 * clank(0.4, 900))),
                  1.0, 0.2)


SOUNDS = {
    "intro": (ll_intro, 64), "roar": (ll_roar, 48), "hurt": (ll_hurt, 24), "wail": (ll_wail, 40), "shroud": (ll_shroud, 32),
    "siphon": (ll_siphon, 32), "mark": (ll_mark, 32), "sorrow": (ll_sorrow, 32), "lament": (ll_lament, 64),
    "storm": (ll_storm, 56), "summon": (ll_summon, 56), "phase": (ll_phase, 56), "death": (ll_death, 64),
    "banshee_scream": (banshee_scream, 24), "banshee_hit": (banshee_hit, 16), "shadow_growl": (shadow_growl, 16),
    "shadow_bite": (shadow_bite, 16), "spirit_moan": (spirit_moan, 20), "spirit_drain": (spirit_drain, 20),
    "vindicator_grunt": (vindicator_grunt, 20), "vindicator_chop": (vindicator_chop, 20),
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
