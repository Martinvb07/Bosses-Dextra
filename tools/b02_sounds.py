#!/usr/bin/env python3
"""
Sonidos propios de OLD ENDER y sus subditos (sintetizados, sin samples externos).

  Modelos/DextraBossesPack/assets/dextra/sounds/old_ender/*.ogg
  En MythicMobs:  effect:sound{s=dextra:old_ender.roar;v=1;p=1}

Tambien deja Modelos/02_OldEnder/preview/sonidos_demo.mp3 con todos seguidos.

Uso: python3 tools/b02_sounds.py      (necesita numpy y ffmpeg con libvorbis)
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import dextra_pack as DP  # noqa: E402
from generate_sounds import (AA, OO, SR, UH, bandpass, brown, crack, curve, debris, drive, env,  # noqa: E402
                             finish, formants, highpass, jitter, lowpass, mixdown, noise, osc_saw,
                             reverb, rumble, thump, to_ogg, whoosh, write_wav)

BOSS = "old_ender"
DEMO = Path(__file__).resolve().parent.parent / "Modelos/02_OldEnder/preview/sonidos_demo.mp3"
RNG = np.random.default_rng(202)

# escala frigia dominante (sonido "egipcio"): Re, Mib, Fa#, Sol, La, Sib, Do
D2, EB2, FS2, G2, A2, BB2 = 73.42, 77.78, 92.50, 98.00, 110.0, 116.54
D3, EB3, FS3, A3 = 146.83, 155.56, 185.0, 220.0


def T(dur):
    return np.arange(int(dur * SR)) / SR


# ---------------------------------------------------------------- bloques
def warble(dur, f_points, depth=0.35, rate=11, vowel=UH, drv=3.0):
    """Voz de enderman: tono que tiembla y se dobla, con formantes y distorsion."""
    n = int(dur * SR)
    f0 = curve(n, f_points) * jitter(n, 0.05)
    wob = 1 + depth * np.sin(2 * np.pi * np.cumsum(rate * jitter(n, 0.4, 2000)) / SR)
    src = osc_saw(f0 * wob) + 0.5 * osc_saw(f0 * wob * 1.5) + 0.4 * osc_saw(f0 / 2)
    v = formants(src, vowel)
    v = drive(v, drv)
    # "rasgado" metalico del enderman: modulacion en anillo
    v *= 0.7 + 0.3 * np.sin(2 * np.pi * np.cumsum(curve(n, [(0, 37), (1, 61)])) / SR)
    return lowpass(v, 6000, 3)


def vwoop(dur=0.9, up=True):
    """Teletransporte: barrido de tono con fase, como un portal que se abre."""
    n = int(dur * SR)
    f = curve(n, [(0, 180), (1, 1400)] if up else [(0, 1400), (1, 160)])
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.4 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR)
    fl = bandpass(noise(dur), 600, 6000) * 0.5
    sweep = (tone * 0.6 + fl) * np.sin(np.linspace(0, np.pi, n)) ** 1.5
    # phaser simple
    d = (40 + 30 * np.sin(np.linspace(0, 6 * np.pi, n))).astype(int)
    idx = np.clip(np.arange(n) - d, 0, n - 1)
    return sweep + 0.7 * sweep[idx]


def sand(dur, lo=1500, hi=9000):
    """Siseo de arena que corre."""
    x = bandpass(noise(dur), lo, hi)
    grains = (RNG.random(len(x)) < 0.004) * RNG.standard_normal(len(x)) * 3
    return x * (0.6 + 0.4 * jitter(len(x), 0.6, 3000)) + highpass(grains, 2000)


def wind(dur, howl=(220, 480)):
    """Viento del desierto: ruido filtrado con una resonancia que aulla."""
    n = int(dur * SR)
    base = lowpass(brown(dur), 900, 2) * 2 + bandpass(noise(dur), 300, 2500) * 0.4
    f = curve(n, [(0, howl[0]), (0.5, howl[1]), (1, howl[0] * 1.1)]) * jitter(n, 0.08, 8000)
    h = bandpass(noise(dur), 150, 900) * (0.5 + 0.5 * np.sin(2 * np.pi * np.cumsum(f / 300) / SR))
    w = base + 0.6 * h
    return w * curve(n, [(0, 0), (0.25, 1), (0.8, 1), (1, 0)])


def sistrum(dur=0.8, shakes=4):
    """Sistro egipcio: chasquidos metalicos que tintinean."""
    n = int(dur * SR)
    out = np.zeros(n)
    for k in range(shakes):
        start = int(k * n / shakes)
        for f in (2900, 4100, 5300, 6700):
            L = int(0.18 * SR)
            if start + L > n:
                L = n - start
            t = np.arange(L) / SR
            out[start:start + L] += np.sin(2 * np.pi * f * (1 + RNG.uniform(-0.01, 0.01)) * t) * np.exp(-t * 28)
        out[start:start + 300] += RNG.standard_normal(min(300, n - start)) * 0.8
    return highpass(out, 1800)


def drone(dur, notes, vowel=AA, attack=0.6):
    """Coro grave en escala frigia dominante."""
    n = int(dur * SR)
    out = np.zeros(n)
    for hz in notes:
        for det in (-0.007, 0.0, 0.006):
            f = hz * (1 + det) * (1 + 0.005 * np.sin(2 * np.pi * 4.6 * T(dur) + RNG.uniform(0, 6)))
            out += osc_saw(f)
    out = lowpass(formants(out, vowel), 3500, 2)
    return out / (np.abs(out).max() + 1e-9) * env(n, attack, dur, 1.5, hold=dur * 0.5)


def ney(dur, hz, bend=-1.0):
    """Flauta ney (soplo con tono), adorno oriental."""
    n = int(dur * SR)
    semis = curve(n, [(0, bend), (0.1, 0), (0.6, 0), (0.7, 1), (0.8, 0), (1, -0.5)])
    f = hz * 2 ** (semis / 12) * (1 + 0.006 * np.sin(2 * np.pi * 5.5 * T(dur)))
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.25 * np.sin(2 * np.pi * np.cumsum(2 * f) / SR)
    breath = bandpass(noise(dur), hz * 1.5, hz * 6) * 0.35
    return (tone + breath) * env(n, 0.12, dur, 1.3, hold=dur * 0.5)


# ---------------------------------------------------------------- sonidos del boss
def oe_intro():
    w = wind(4.8)
    dr = drone(4.6, [D2, A2, D3, EB3, FS3])
    fl = ney(1.6, 587.3)
    scream = warble(1.6, [(0, 160), (0.2, 240), (1, 120)], drv=3.4) * env(int(1.6 * SR), 0.05, 1.6, 1.6, hold=0.6)
    s = mixdown((0, 0.45 * w), (0.2, 0.5 * dr), (0.9, 0.25 * fl), (2.6, 0.7 * scream),
                (2.6, 0.9 * thump(1.8, 85, 28)), (2.6, 0.5 * sand(2.0)), (2.6, 0.35 * vwoop(0.8, False)))
    return reverb(s, 3.2, 0.32)


def oe_roar():
    g = warble(2.0, [(0, 120), (0.15, 190), (0.6, 170), (1, 90)], drv=3.2)
    g *= env(len(g), 0.06, 2.0, 1.4, hold=0.9)
    return reverb(mixdown((0, g), (0, 0.4 * thump(1.4, 70, 32)), (0.1, 0.25 * sand(1.6))), 2.4, 0.3)


def oe_hurt():
    g = warble(0.5, [(0, 260), (0.3, 300), (1, 180)], depth=0.5, rate=16, drv=3.4)
    return reverb(g * env(len(g), 0.01, 0.5, 2.0, hold=0.08), 0.9, 0.18)


def oe_teleport():
    return reverb(mixdown((0, vwoop(0.9, True)), (0.55, 0.5 * sand(0.6))), 1.4, 0.25)


def oe_strike():
    slash = whoosh(0.35, 600, 5000)
    hit = mixdown((0, thump(0.7, 140, 45)), (0, 0.6 * crack(0.18)), (0.01, 0.4 * sand(0.6)))
    return reverb(mixdown((0, 0.7 * slash), (0.28, hit)), 1.2, 0.2)


def oe_pulse():
    n = int(1.5 * SR)
    swell = bandpass(noise(1.5), 200, 3000) * curve(n, [(0, 0), (0.12, 1), (1, 0)]) ** 2
    s = mixdown((0, 0.9 * thump(1.2, 120, 34)), (0, 0.8 * swell), (0.02, 0.6 * sand(1.4)),
                (0, 0.35 * vwoop(0.5, False)))
    return reverb(s, 1.8, 0.24, 2600)


def oe_collapse():
    s = mixdown((0, thump(1.5, 120, 28)), (0, 0.8 * crack(0.3)), (0.03, 0.8 * debris(2.2, 120)),
                (0, rumble(2.8, 18, 120, 8) * env(int(2.8 * SR), 0.05, 2.8, 1.6, hold=0.7)),
                (0.2, 0.6 * sand(2.4, 800, 7000)))
    return reverb(s, 2.4, 0.26, 2200)


def oe_gaze():
    n = int(1.8 * SR)
    f = curve(n, [(0, 520), (1, 1180)])
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * (1 + 0.6 * np.sin(2 * np.pi * 23 * T(1.8)))
    buzz = bandpass(osc_saw(f / 4), 300, 3000) * 0.4
    s = (tone * 0.5 + buzz) * curve(n, [(0, 0), (0.6, 0.8), (0.95, 1), (1, 0)])
    hit = warble(0.6, [(0, 330), (1, 220)], depth=0.6, rate=20)
    return reverb(mixdown((0, s), (0.5, 0.6 * hit * env(int(0.6 * SR), 0.01, 0.6, 2))), 1.8, 0.3)


def oe_sandstorm():
    return reverb(mixdown((0, wind(3.2, (260, 620))), (0, 0.55 * sand(3.2, 1200, 9000))), 1.6, 0.2)


def oe_summon():
    s = mixdown((0, 0.8 * sistrum(0.9, 4)), (0.15, 0.55 * drone(2.2, [D2, A2, EB3], attack=0.25)),
                (0.2, 0.35 * ney(1.6, 440.0, -2)), (1.2, 0.5 * sand(1.0)))
    return reverb(s, 2.6, 0.3)


def oe_phase():
    n = int(1.4 * SR)
    sweep = vwoop(1.4, True) * curve(n, [(0, 0.3), (1, 1)])
    stab = drone(2.2, [D3, FS3, A3, D2 * 4], attack=0.04)
    s = mixdown((0, 0.7 * sweep), (1.35, 0.9 * thump(1.3, 100, 30)), (1.35, 0.7 * crack(0.3)), (1.35, 0.7 * stab),
                (1.35, 0.5 * warble(1.0, [(0, 200), (1, 140)])))
    return reverb(s, 2.8, 0.3)


def oe_death():
    g = warble(3.4, [(0, 200), (0.2, 230), (0.7, 110), (1, 55)], depth=0.45, drv=2.6)
    g *= env(len(g), 0.05, 3.4, 1.8, hold=1.2)
    s = mixdown((0, g), (1.2, 0.5 * wind(3.4)), (1.8, 0.6 * sand(2.6, 900, 8000)), (2.6, 0.7 * thump(1.6, 70, 26)),
                (2.4, 0.3 * drone(2.4, [D2, A2, D3], attack=0.8)))
    return reverb(s, 3.2, 0.32)


# ---------------------------------------------------------------- subditos
def warden_hit():
    s = mixdown((0, thump(0.6, 160, 50)), (0, 0.7 * crack(0.15)), (0.01, 0.6 * debris(0.8, 90)),
                (0, 0.4 * sand(0.7)))
    return reverb(s, 0.9, 0.15)


def warden_rise():
    n = int(1.4 * SR)
    s = mixdown((0, sand(1.4, 700, 7000) * curve(n, [(0, 0.2), (0.8, 1), (1, 0)])),
                (0, 0.6 * rumble(1.4, 25, 160)), (0.9, 0.7 * thump(0.6, 110, 40)))
    return reverb(s, 1.2, 0.2)


def mummy_groan():
    def puff(d, lo, hi):
        return bandpass(noise(d), lo, hi) * np.sin(np.linspace(0, np.pi, int(d * SR))) ** 1.5
    from generate_sounds import growl
    g = growl(1.4, [(0, 95), (0.5, 82), (1, 68)], vowel=OO, drv=2.0, breath=0.6, rough=18)
    g *= env(len(g), 0.25, 1.4, 1.5, hold=0.5)
    return reverb(mixdown((0, 0.4 * puff(0.5, 200, 2000)), (0.3, g)), 1.4, 0.25)


def scarab_hiss():
    n = int(0.9 * SR)
    clicks = np.zeros(n)
    for k in range(9):
        i = int(k * 0.05 * SR)
        clicks[i:i + 200] += RNG.standard_normal(200) * np.exp(-np.arange(200) / 30)
    hiss = bandpass(noise(0.9), 2500, 9000) * curve(n, [(0, 0), (0.45, 0.2), (0.6, 1), (1, 0)])
    return reverb(mixdown((0, highpass(clicks, 1500)), (0, 0.7 * hiss)), 0.6, 0.12)


def priest_chant():
    ch = drone(1.6, [A2 * 2, D3 * 2, FS3 * 2], vowel=OO, attack=0.2)
    chime = sum(np.sin(2 * np.pi * f * T(1.6)) * np.exp(-T(1.6) * 2.5) for f in (1174.7, 1760.0, 2349.3))
    return reverb(mixdown((0, 0.6 * ch), (0.3, 0.25 * chime), (0, 0.4 * sistrum(0.5, 2))), 2.0, 0.32)


SOUNDS = {
    "intro": (oe_intro, 64), "roar": (oe_roar, 48), "hurt": (oe_hurt, 24), "teleport": (oe_teleport, 32),
    "strike": (oe_strike, 24), "pulse": (oe_pulse, 40), "collapse": (oe_collapse, 48), "gaze": (oe_gaze, 32),
    "sandstorm": (oe_sandstorm, 48), "summon": (oe_summon, 56), "phase": (oe_phase, 56), "death": (oe_death, 64),
    "warden_hit": (warden_hit, 20), "warden_rise": (warden_rise, 24), "mummy_groan": (mummy_groan, 20),
    "scarab_hiss": (scarab_hiss, 16), "priest_chant": (priest_chant, 24),
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
