#!/usr/bin/env python3
"""
Sintetiza los sonidos propios de Heracles y del Minotauro (sin samples externos)
y los guarda como .ogg mono para el resource pack.

  HeraclesPack/assets/olympus/sounds/<grupo>/<nombre>.ogg
  HeraclesPack/assets/olympus/sounds.json      -> olympus:<grupo>.<nombre>

En MythicMobs:  effect:sound{s=olympus:heracles.roar;v=1;p=1}

Tambien deja una demo con todos seguidos en Modelos/01_Heracles/preview/sonidos_demo.mp3

Uso: python3 tools/generate_sounds.py      (necesita numpy y ffmpeg con libvorbis)
"""
import json
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np

SR = 44100
ROOT = Path(__file__).resolve().parent.parent / "Modelos" / "01_Heracles"
ASSETS = ROOT / "ResourcePack/HeraclesPack/assets/olympus"
DEMO = ROOT / "preview/sonidos_demo.mp3"
RNG = np.random.default_rng(7)


# ---------------------------------------------------------------- utilidades
def T(dur):
    return np.arange(int(dur * SR)) / SR


def noise(dur):
    return RNG.standard_normal(int(dur * SR))


def brown(dur):
    x = np.cumsum(noise(dur))
    x -= np.convolve(x, np.ones(2048) / 2048, mode="same")   # quita la deriva
    return x / (np.abs(x).max() + 1e-9)


def spec_filter(x, gain_fn):
    """Filtro estatico en frecuencia: gain_fn(freqs) -> ganancia lineal."""
    n = len(x)
    X = np.fft.rfft(x, n * 2)
    f = np.fft.rfftfreq(n * 2, 1 / SR)
    return np.fft.irfft(X * gain_fn(f), n * 2)[:n]


def lowpass(x, fc, order=4):
    return spec_filter(x, lambda f: 1 / np.sqrt(1 + (f / fc) ** (2 * order)))


def highpass(x, fc, order=4):
    return spec_filter(x, lambda f: 1 / np.sqrt(1 + (fc / np.maximum(f, 1e-3)) ** (2 * order)))


def bandpass(x, lo, hi, order=3):
    return highpass(lowpass(x, hi, order), lo, order)


def formants(x, fs):
    """fs = [(frecuencia, ancho, ganancia)] -> resonancias de voz/bocina."""
    def g(f):
        out = np.full_like(f, 0.05)
        for fc, bw, gain in fs:
            out += gain * np.exp(-0.5 * ((f - fc) / bw) ** 2)
        return out
    return spec_filter(x, g)


def env(n_or_x, a, d_total, curve=2.0, hold=0.0):
    n = n_or_x if isinstance(n_or_x, int) else len(n_or_x)
    t = np.arange(n) / SR
    e = np.clip(t / max(a, 1e-4), 0, 1)
    rel = np.clip((t - a - hold) / max(d_total - a - hold, 1e-4), 0, 1)
    return e * (1 - rel) ** curve


def osc_saw(f0):
    """Diente de sierra con frecuencia variable (array por muestra)."""
    ph = np.cumsum(f0) / SR
    return 2 * (ph % 1) - 1


def jitter(n, amount, smooth=600):
    j = np.convolve(RNG.standard_normal(n + smooth), np.ones(smooth) / smooth, mode="same")[:n]
    return 1 + amount * j / (np.abs(j).max() + 1e-9)


def curve(n, points):
    """Curva por tramos lineales: points=[(t_rel 0..1, valor)]."""
    xs, ys = zip(*points)
    return np.interp(np.linspace(0, 1, n), xs, ys)


def reverb(x, seconds=2.0, mix=0.3, tone=3500):
    n = int(seconds * SR)
    ir = noise(seconds) * np.exp(-np.arange(n) / SR * 6.9 / seconds)
    ir = lowpass(ir, tone, 2)
    ir[: int(0.012 * SR)] = 0                     # pre-delay de sala
    L = len(x) + n
    wet = np.fft.irfft(np.fft.rfft(x, L) * np.fft.rfft(ir, L), L)
    wet = wet / (np.abs(wet).max() + 1e-9) * np.abs(x).max()
    out = np.zeros(len(x) + n)
    out[: len(x)] += x * (1 - mix)
    out += wet * mix
    return out


def drive(x, k=2.5):
    return np.tanh(k * x / (np.abs(x).max() + 1e-9))


def mixdown(*parts):
    n = max(len(p) + int(off * SR) for off, p in parts)
    out = np.zeros(n)
    for off, p in parts:
        i = int(off * SR)
        out[i:i + len(p)] += p
    return out


def finish(x, peak=0.92, tail=0.25):
    x = x - np.mean(x)
    nz = np.nonzero(np.abs(x) > 3e-3 * np.abs(x).max())[0]
    x = x[: nz[-1] + 1] if len(nz) else x
    fade = int(tail * SR)
    x[-fade:] *= np.linspace(1, 0, fade)
    return x / (np.abs(x).max() + 1e-9) * peak


# ---------------------------------------------------------------- bloques
AA = [(700, 180, 1.0), (1150, 220, 0.6), (2600, 380, 0.22)]       # "aaah"
OO = [(420, 120, 1.0), (820, 160, 0.55), (2400, 380, 0.12)]       # "oooh" (toro)
UH = [(520, 140, 1.0), (950, 200, 0.5), (2500, 380, 0.15)]        # "uh"


def growl(dur, f_points, vowel=AA, rough=32, sub=0.55, breath=0.25, drv=2.8, jit=0.07):
    """Rugido gutural: sierra + subarmonico + aspereza + formantes + saturacion."""
    n = int(dur * SR)
    f0 = curve(n, f_points) * jitter(n, jit)
    src = osc_saw(f0) + sub * osc_saw(f0 / 2)
    am = 1 + 0.55 * np.sin(2 * np.pi * np.cumsum(rough * jitter(n, 0.3)) / SR)
    src *= am
    src += breath * bandpass(noise(dur), 400, 4000) * np.abs(src).max()
    v = formants(src, vowel)
    v = drive(v, drv)
    return lowpass(v, 5200, 3)


def thump(dur=0.9, f_hi=110, f_lo=38):
    n = int(dur * SR)
    f = f_lo + (f_hi - f_lo) * np.exp(-np.arange(n) / SR * 9)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.003, dur, 2.2)


def crack(dur=0.25):
    return highpass(noise(dur), 1200) * env(int(dur * SR), 0.001, dur, 6)


def debris(dur=1.2, density=70):
    n = int(dur * SR)
    x = np.zeros(n)
    for _ in range(int(density * dur)):
        i = RNG.integers(0, n - 400)
        L = RNG.integers(60, 400)
        x[i:i + L] += RNG.standard_normal(L) * np.exp(-np.arange(L) / (L / 4)) * (1 - i / n) ** 1.5
    return bandpass(x, 500, 6000)


def rumble(dur, lo=25, hi=140, trem=7):
    n = int(dur * SR)
    r = lowpass(highpass(brown(dur), lo, 2), hi, 3)
    r *= 1 + 0.4 * np.sin(2 * np.pi * trem * np.arange(n) / SR) * jitter(n, 0.5, 4000)
    return r / (np.abs(r).max() + 1e-9)


def thunder(dur=3.0):
    n = int(dur * SR)
    r = rumble(dur, 20, 260, 3)
    bursts = np.zeros(n)
    for c in (0.0, 0.15, 0.45, 0.9):
        bursts += np.exp(-np.maximum(np.arange(n) / SR - c, 0) * 3) * (np.arange(n) / SR >= c)
    return mixdown((0, r * bursts * env(n, 0.01, dur, 1.4)), (0, 0.6 * crack(0.35)))


def whoosh(dur=0.5, lo=250, hi=2200):
    n = int(dur * SR)
    t = np.arange(n) / n
    bell = np.sin(np.pi * t) ** 2.2
    a = bandpass(noise(dur), lo, hi * 0.6)
    b = bandpass(noise(dur), lo * 2, hi)
    return (a * (1 - t) + b * t) * bell


def choir(dur, notes, vowel=AA, attack=0.8, vib=5.2):
    n = int(dur * SR)
    out = np.zeros(n)
    for hz in notes:
        for det in (-0.006, 0.0, 0.007):
            f = hz * (1 + det) * (1 + 0.006 * np.sin(2 * np.pi * vib * np.arange(n) / SR + RNG.uniform(0, 6)))
            out += osc_saw(f)
    out = formants(out, vowel)
    out = lowpass(out, 4000, 2)
    return out / (np.abs(out).max() + 1e-9) * env(n, attack, dur, 1.5, hold=dur * 0.45)


def horn(dur, hz, bend=-2.0):
    """Salpinx (trompeta de guerra griega)."""
    n = int(dur * SR)
    semis = curve(n, [(0, bend), (0.08, 0), (1, -0.3)])
    f = hz * 2 ** (semis / 12) * (1 + 0.004 * np.sin(2 * np.pi * 5.5 * np.arange(n) / SR))
    x = osc_saw(f) + 0.5 * osc_saw(f * 2.001) + 0.3 * osc_saw(f / 2)
    x = formants(x, [(hz * 3, 260, 1.0), (hz * 6, 500, 0.6), (2800, 600, 0.35)])
    x = drive(x, 1.8)
    return lowpass(x, 3200, 2) * env(n, 0.05, dur, 1.2, hold=dur * 0.55)


# ---------------------------------------------------------------- sonidos
def heracles_roar():
    g = growl(2.0, [(0, 72), (0.15, 96), (0.6, 88), (1, 58)])
    g *= env(len(g), 0.07, 2.0, 1.4, hold=0.9)
    sub = thump(1.6, 70, 35) * 0.5
    return reverb(mixdown((0, g), (0, sub)), 2.4, 0.28)


def heracles_hurt():
    g = growl(0.42, [(0, 120), (0.3, 132), (1, 90)], vowel=UH, drv=3.2)
    return reverb(g * env(len(g), 0.01, 0.42, 2.0, hold=0.08), 0.8, 0.15)


def heracles_charge():
    g = growl(0.95, [(0, 110), (0.25, 150), (1, 120)], drv=3.5, rough=40)
    g *= env(len(g), 0.04, 0.95, 1.5, hold=0.45)
    return reverb(mixdown((0, g), (0.05, 0.4 * whoosh(0.6))), 1.5, 0.2)


def heracles_swing():
    return whoosh(0.5, 200, 2600)


def heracles_slam():
    s = mixdown((0, thump(1.0, 130, 36)), (0, 0.7 * crack(0.2)), (0.01, 0.55 * debris(1.3)),
                (0, 0.6 * rumble(1.2) * env(int(1.2 * SR), 0.01, 1.2, 2.5)))
    return reverb(s, 1.6, 0.22, 2500)


def heracles_quake():
    s = mixdown((0, thump(1.4, 120, 30)), (0, 0.8 * crack(0.3)), (0.02, 0.7 * debris(2.0, 110)),
                (0, 1.0 * rumble(2.6, 18, 110, 9) * env(int(2.6 * SR), 0.05, 2.6, 1.6, hold=0.6)))
    return reverb(s, 2.2, 0.25, 2200)


def heracles_intro():
    th = thunder(3.5)
    ch = choir(4.2, [73.42, 110.0, 146.83, 174.61, 220.0])          # Re menor
    rise = lowpass(noise(1.4), 3000) * curve(int(1.4 * SR), [(0, 0), (0.9, 0.5), (1, 0)])
    s = mixdown((0, 0.55 * ch), (0, 0.25 * rise), (1.35, 1.0 * th), (1.35, 0.8 * thump(1.6, 90, 30)))
    return reverb(s, 3.2, 0.32)


def heracles_phase():
    n = int(1.3 * SR)
    sweep = np.sin(2 * np.pi * np.cumsum(curve(n, [(0, 180), (1, 900)])) / SR) * curve(n, [(0, 0), (1, 0.6)])
    shimmer = bandpass(noise(1.3), 2500, 9000) * curve(n, [(0, 0), (1, 0.35)])
    stab = choir(2.0, [146.83, 220.0, 293.66, 369.99, 440.0], attack=0.05)    # Re mayor
    s = mixdown((0, sweep), (0, shimmer), (1.3, 0.9 * thump(1.2, 100, 32)), (1.3, 0.8 * crack(0.3)),
                (1.3, 0.7 * stab))
    return reverb(s, 2.8, 0.3)


def heracles_summon():
    s = mixdown((0, 0.8 * horn(0.45, 233.08)), (0.55, horn(1.6, 233.08, -3)), (0.55, 0.5 * horn(1.6, 349.23, -3)))
    return reverb(s, 2.6, 0.32)


def heracles_last_breath():
    def breath(d, lo, hi):
        return bandpass(noise(d), lo, hi) * np.sin(np.linspace(0, np.pi, int(d * SR))) ** 1.5
    groan = growl(1.0, [(0, 80), (0.5, 70), (1, 55)], vowel=UH, drv=2.2, breath=0.35)
    groan *= env(len(groan), 0.15, 1.0, 1.6, hold=0.3)
    s = mixdown((0, 0.45 * breath(0.55, 300, 2500)), (0.6, 0.35 * breath(0.7, 200, 1800)),
                (0.85, 0.9 * groan), (1.6, 0.4 * breath(0.6, 300, 2500)))
    return reverb(s, 1.8, 0.22)


def heracles_death():
    g = growl(3.2, [(0, 92), (0.2, 100), (0.7, 64), (1, 40)], drv=2.4)
    g *= env(len(g), 0.06, 3.2, 1.8, hold=1.2)
    s = mixdown((0, g), (1.6, 0.6 * thunder(3.0)))
    return reverb(s, 3.0, 0.3)


def minotaur_roar():
    g = growl(1.8, [(0, 105), (0.2, 140), (0.7, 128), (1, 85)], vowel=OO, drv=3.6, rough=26, sub=0.7)
    g *= env(len(g), 0.06, 1.8, 1.5, hold=0.8)
    return reverb(g, 1.8, 0.22)


def minotaur_snort():
    n1, n2 = int(0.18 * SR), int(0.26 * SR)
    puff1 = bandpass(noise(0.18), 300, 3500) * env(n1, 0.005, 0.18, 2)
    puff2 = bandpass(noise(0.26), 250, 3000) * env(n2, 0.005, 0.26, 2)
    return reverb(mixdown((0, puff1), (0.22, puff2)), 0.6, 0.12)


SOUNDS = {
    # nombre: (funcion, distancia de atenuacion en bloques)
    "heracles.intro": (heracles_intro, 64),
    "heracles.roar": (heracles_roar, 48),
    "heracles.hurt": (heracles_hurt, 24),
    "heracles.charge": (heracles_charge, 32),
    "heracles.swing": (heracles_swing, 20),
    "heracles.slam": (heracles_slam, 40),
    "heracles.quake": (heracles_quake, 48),
    "heracles.phase": (heracles_phase, 56),
    "heracles.summon": (heracles_summon, 64),
    "heracles.last_breath": (heracles_last_breath, 32),
    "heracles.death": (heracles_death, 64),
    "minotaur.roar": (minotaur_roar, 40),
    "minotaur.snort": (minotaur_snort, 20),
}


def write_wav(path, x):
    data = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())


def to_ogg(wav, ogg):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-ac", "1",
                    "-c:a", "libvorbis", "-q:a", "5", str(ogg)], check=True)


def main():
    sounds_json = {}
    demo = []
    with tempfile.TemporaryDirectory() as tmp:
        for key, (fn, dist) in SOUNDS.items():
            group, name = key.split(".")
            x = finish(fn())
            out = ASSETS / "sounds" / group / f"{name}.ogg"
            out.parent.mkdir(parents=True, exist_ok=True)
            wav = Path(tmp) / f"{group}_{name}.wav"
            write_wav(wav, x)
            to_ogg(wav, out)
            sounds_json[key] = {
                "sounds": [{"name": f"olympus:{group}/{name}", "attenuation_distance": dist}],
            }
            demo += [x, np.zeros(int(0.6 * SR))]
            print(f"OK olympus:{key:22s} {len(x) / SR:4.1f} s")
        with open(ASSETS / "sounds.json", "w", encoding="utf-8") as fh:
            json.dump(sounds_json, fh, indent=2)
        wav = Path(tmp) / "demo.wav"
        write_wav(wav, np.concatenate(demo))
        DEMO.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-b:a", "128k", str(DEMO)], check=True)
    print("demo ->", DEMO)


if __name__ == "__main__":
    main()
