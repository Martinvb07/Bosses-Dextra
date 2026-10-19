#!/usr/bin/env python3
"""
Sonidos propios de BAAL y sus subditos (sintetizados): koto, taiko, shakuhachi,
campana de templo, katana, espiritus y voz de oni.

  Modelos/DextraBossesPack/assets/dextra/sounds/baal/*.ogg  ->  dextra:baal.<nombre>
  Demo: Modelos/03_Baal/preview/sonidos_demo.mp3

Uso: python3 tools/b03_sounds.py
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import dextra_pack as DP  # noqa: E402
from generate_sounds import (OO, SR, UH, bandpass, crack, curve, env, finish, growl, highpass,  # noqa: E402
                             jitter, lowpass, mixdown, noise, reverb, rumble, thump, to_ogg, whoosh,
                             write_wav)

BOSS = "baal"
DEMO = Path(__file__).resolve().parent.parent / "Modelos/03_Baal/preview/sonidos_demo.mp3"
RNG = np.random.default_rng(303)

# escala In (miyako-bushi) sobre Re: Re, Mib, Sol, La, Sib
IN = [293.66, 311.13, 392.0, 440.0, 466.16, 587.33, 622.25, 783.99]


def T(dur):
    return np.arange(int(dur * SR)) / SR


# ---------------------------------------------------------------- instrumentos
def koto(hz, dur=1.6, bright=0.5, bend=0.0):
    """Cuerda pulsada (Karplus-Strong) con un pequeno 'oshide' (subida de tono)."""
    n = int(dur * SR)
    period = int(SR / hz)
    buf = RNG.uniform(-1, 1, period) * np.hanning(period) ** 0.3
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % period]
        nxt = (i + 1) % period
        buf[i % period] = 0.996 * (bright * buf[i % period] + (1 - bright) * buf[nxt])
    if bend:
        idx = np.arange(n) * (1 + bend * np.clip(np.arange(n) / SR - 0.15, 0, 0.2) / 0.2 * 0.059)
        out = np.interp(np.clip(idx, 0, n - 1), np.arange(n), out)
    return highpass(out, 120) * env(n, 0.002, dur, 2.0)


def taiko(dur=1.2, f_hi=120, f_lo=48, skin=0.35):
    n = int(dur * SR)
    body = thump(dur, f_hi, f_lo)
    hit = bandpass(noise(0.08), 300, 3000) * env(int(0.08 * SR), 0.001, 0.08, 4)
    out = mixdown((0, body), (0, skin * hit))
    return out[:n]


def shakuhachi(dur, hz, bend=-1.5, breath=0.5):
    """Flauta de bambu: tono con mucho soplo y caidas de tono (meri)."""
    n = int(dur * SR)
    semis = curve(n, [(0, bend), (0.12, 0), (0.7, 0), (0.85, -0.8), (1, -1.5)])
    f = hz * 2 ** (semis / 12) * (1 + 0.007 * np.sin(2 * np.pi * 5.2 * T(dur)))
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(2 * np.pi * np.cumsum(2 * f) / SR)
    air = bandpass(noise(dur), hz * 1.2, hz * 8) * breath * (0.6 + 0.4 * jitter(n, 0.5, 3000))
    return (tone * 0.8 + air) * env(n, 0.15, dur, 1.4, hold=dur * 0.5)


def bell(dur=5.0, hz=110.0):
    """Campana de templo (bonsho): parciales inarmonicos que decaen lento, con batido."""
    t = T(dur)
    out = np.zeros(len(t))
    for ratio, amp, dec in ((0.5, 0.8, 0.5), (1.0, 1.0, 0.7), (1.19, 0.6, 0.9), (1.56, 0.5, 1.2),
                            (2.0, 0.4, 1.6), (2.51, 0.3, 2.2), (3.01, 0.2, 3.0)):
        f = hz * ratio
        out += amp * np.sin(2 * np.pi * f * t) * (1 + 0.15 * np.sin(2 * np.pi * 1.3 * t)) * np.exp(-t * dec)
    strike = lowpass(noise(0.05), 800) * env(int(0.05 * SR), 0.001, 0.05, 3)
    return mixdown((0, out / np.abs(out).max()), (0, 0.6 * strike))


def shing(dur=1.0, hz=3200):
    """Katana: anillo metalico agudo."""
    t = T(dur)
    ring = sum(np.sin(2 * np.pi * hz * r * t) * np.exp(-t * d) for r, d in ((1, 4), (1.47, 6), (2.13, 9), (2.9, 12)))
    scrape = bandpass(noise(0.25), 3000, 9000) * np.linspace(1, 0, int(0.25 * SR))
    return mixdown((0, 0.5 * scrape), (0.05, 0.4 * ring))


def wail(dur, f_points, rough=6):
    """Lamento de fantasma (onryo): tono que se arrastra con vibrato y soplo."""
    n = int(dur * SR)
    f = curve(n, f_points) * (1 + 0.02 * np.sin(2 * np.pi * rough * T(dur)))
    v = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.4 * np.sin(2 * np.pi * np.cumsum(1.5 * f) / SR)
    v += bandpass(noise(dur), 600, 4000) * 0.35
    return v * curve(n, [(0, 0), (0.2, 1), (0.8, 0.8), (1, 0)])


def chimes(dur=1.6, count=7):
    out = np.zeros(int(dur * SR))
    for k in range(count):
        i = int(RNG.uniform(0, dur * 0.6) * SR)
        f = RNG.choice(IN) * 4
        t = T(dur)[: len(out) - i]
        out[i:] += np.sin(2 * np.pi * f * t) * np.exp(-t * 5) * 0.5
    return out


def oni(dur, f_points, drv=3.2):
    return growl(dur, f_points, vowel=OO, drv=drv, rough=24, sub=0.8)


def arpeggio(notes, gap=0.09, dur=1.4):
    return mixdown(*[(i * gap, 0.6 * koto(hz, dur)) for i, hz in enumerate(notes)])


# ---------------------------------------------------------------- boss
def bl_intro():
    s = mixdown((0, 0.9 * bell(5.0, 98.0)), (0.6, 0.45 * shakuhachi(2.2, 587.33)), (2.2, arpeggio(IN[:6], 0.08)),
                (3.0, 0.9 * taiko()), (3.35, 0.7 * taiko(1.0, 140, 60)), (3.7, 1.0 * taiko(1.4, 110, 40)),
                (3.7, 0.7 * oni(1.6, [(0, 70), (0.2, 95), (1, 55)]) * env(int(1.6 * SR), 0.05, 1.6, 1.5, hold=0.5)))
    return reverb(s, 3.2, 0.3)


def bl_roar():
    g = oni(1.8, [(0, 80), (0.15, 110), (0.6, 100), (1, 62)]) * env(int(1.8 * SR), 0.05, 1.8, 1.4, hold=0.8)
    return reverb(mixdown((0, g), (0, 0.6 * taiko(1.2, 100, 40))), 2.2, 0.28)


def bl_hurt():
    g = oni(0.45, [(0, 140), (0.3, 150), (1, 100)], drv=3.6)
    return reverb(g * env(len(g), 0.01, 0.45, 2.0, hold=0.08), 0.8, 0.15)


def bl_slash():
    return reverb(mixdown((0, 0.9 * whoosh(0.35, 500, 6000)), (0.12, 0.8 * shing(0.9))), 1.2, 0.22)


def bl_curse():
    s = mixdown((0, 0.6 * wail(1.4, [(0, 520), (0.5, 640), (1, 380)])), (0, 0.4 * chimes(1.4, 5)),
                (0.38, 0.6 * koto(IN[1] / 2, 1.2, 0.3, bend=1)))
    return reverb(s, 2.0, 0.35)


def bl_step():
    puff = bandpass(noise(0.4), 200, 2500) * env(int(0.4 * SR), 0.01, 0.4, 2)
    return reverb(mixdown((0, 0.7 * puff), (0.05, 0.7 * whoosh(0.5, 300, 3000)), (0.55, 0.6 * taiko(0.6, 160, 60))),
                  1.2, 0.2)


def bl_hex():
    n = int(1.8 * SR)
    wind = bandpass(noise(1.8), 800, 6000) * curve(n, [(0, 0), (0.3, 1), (1, 0)])
    s = mixdown((0, 0.4 * wind), (0, arpeggio([IN[i % 8] for i in (0, 2, 3, 5, 6, 7, 6, 5)], 0.06, 1.2)),
                (0.5, 0.8 * taiko(0.9, 130, 50)), (0.5, 0.4 * chimes(1.2, 9)))
    return reverb(s, 2.2, 0.3)


def bl_nova():
    n = int(1.2 * SR)
    swell = bandpass(noise(1.2), 400, 5000) * curve(n, [(0, 0), (1, 1)]) ** 2
    s = mixdown((0, 0.6 * swell), (0, 0.4 * wail(1.2, [(0, 300), (1, 900)])), (0.6, taiko(1.6, 110, 34)),
                (0.6, 0.7 * crack(0.3)), (0.6, 0.6 * bell(2.5, 147.0)), (0.6, 0.5 * rumble(1.6, 20, 140)))
    return reverb(s, 2.6, 0.3)


def bl_veil():
    n = int(1.2 * SR)
    dark = lowpass(noise(1.2), 900) * curve(n, [(0, 0), (0.3, 1), (1, 0)])
    return reverb(mixdown((0, dark), (0.1, 0.5 * whoosh(0.8, 150, 1500)), (0.2, 0.3 * wail(0.9, [(0, 300), (1, 200)]))),
                  1.8, 0.35)


def bl_summon():
    roll = mixdown(*[(i * 0.11, (0.4 + 0.06 * i) * taiko(0.6, 140, 55)) for i in range(9)])
    s = mixdown((0, roll), (1.0, 0.8 * bell(3.0, 130.8)), (1.0, 0.4 * shakuhachi(1.6, 440.0)))
    return reverb(s, 2.6, 0.3)


def bl_phase():
    s = mixdown((0, 0.6 * bell(3.5, 98.0)), (0.5, arpeggio(IN[::-1], 0.05, 1.0)), (1.2, taiko(1.4, 110, 36)),
                (1.2, 0.8 * oni(1.2, [(0, 90), (0.3, 120), (1, 70)]) * env(int(1.2 * SR), 0.03, 1.2, 1.5, hold=0.4)))
    return reverb(s, 2.8, 0.3)


def bl_death():
    g = oni(2.6, [(0, 100), (0.3, 90), (1, 40)], drv=2.4) * env(int(2.6 * SR), 0.05, 2.6, 1.8, hold=0.9)
    s = mixdown((0, g), (1.4, 0.8 * bell(5.0, 87.3)), (2.0, 0.4 * shakuhachi(3.0, 392.0, bend=-2)))
    return reverb(s, 3.4, 0.32)


# ---------------------------------------------------------------- subditos
def samurai_hit():
    clank = sum(np.sin(2 * np.pi * f * T(0.5)) * np.exp(-T(0.5) * 14) for f in (1450, 2210, 3170))
    return reverb(mixdown((0, 0.6 * whoosh(0.25, 500, 4000)), (0.15, 0.5 * clank), (0.15, 0.4 * crack(0.1))), 0.8, 0.15)


def samurai_rise():
    rattle = np.zeros(int(1.0 * SR))
    for k in range(14):
        i = int(RNG.uniform(0, 0.8) * SR)
        L = 600
        rattle[i:i + L] += bandpass(RNG.standard_normal(L), 900, 5000) * np.exp(-np.arange(L) / 120)
    return reverb(mixdown((0, rattle), (0, 0.4 * wail(1.0, [(0, 200), (1, 150)]))), 1.0, 0.2)


def yokai_laugh():
    out = []
    for k in range(4):
        f = 900 - k * 70
        out.append((k * 0.13, wail(0.12, [(0, f), (1, f * 0.8)], 30) * 0.8))
    return reverb(mixdown(*out, (0, 0.4 * chimes(0.9, 4))), 1.4, 0.3)


def yokai_curse():
    return reverb(mixdown((0, 0.6 * wail(1.0, [(0, 700), (0.5, 520), (1, 820)], 9)), (0, 0.5 * chimes(1.0, 6))), 1.6, 0.35)


def ninja_strike():
    return reverb(mixdown((0, whoosh(0.18, 1500, 8000)), (0.1, 0.4 * shing(0.4, 4600))), 0.6, 0.12)


def ninja_vanish():
    n = int(0.6 * SR)
    puff = bandpass(noise(0.6), 300, 4000) * curve(n, [(0, 1), (1, 0)]) ** 2
    return reverb(mixdown((0, puff), (0, 0.3 * whoosh(0.4, 200, 2000))), 0.8, 0.2)


SOUNDS = {
    "intro": (bl_intro, 64), "roar": (bl_roar, 48), "hurt": (bl_hurt, 24), "slash": (bl_slash, 24),
    "curse": (bl_curse, 32), "step": (bl_step, 32), "hex": (bl_hex, 40), "nova": (bl_nova, 48),
    "veil": (bl_veil, 32), "summon": (bl_summon, 56), "phase": (bl_phase, 56), "death": (bl_death, 64),
    "samurai_hit": (samurai_hit, 20), "samurai_rise": (samurai_rise, 20), "yokai_laugh": (yokai_laugh, 20),
    "yokai_curse": (yokai_curse, 20), "ninja_strike": (ninja_strike, 16), "ninja_vanish": (ninja_vanish, 16),
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
