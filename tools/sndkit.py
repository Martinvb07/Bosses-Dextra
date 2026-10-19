#!/usr/bin/env python3
"""Genera los .ogg de un boss, los registra en el pack y crea el mp3 de demo (comun a b08 en adelante)."""
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import dextra_pack as DP  # noqa: E402
from generate_sounds import SR, finish, to_ogg, write_wav  # noqa: E402


def build(boss, sounds, demo_path):
    """sounds = {nombre: (funcion, distancia)}"""
    DP.ensure_pack()
    out_dir = DP.sound_dir(boss)
    demo = []
    with tempfile.TemporaryDirectory() as tmp:
        for name, (fn, _) in sounds.items():
            x = finish(fn())
            wav = Path(tmp) / f"{name}.wav"
            write_wav(wav, x)
            to_ogg(wav, out_dir / f"{name}.ogg")
            demo += [x, np.zeros(int(0.6 * SR))]
            print(f"OK dextra:{boss}.{name:16s} {len(x) / SR:4.1f} s")
        DP.register_sounds(boss, {k: d for k, (_, d) in sounds.items()})
        wav = Path(tmp) / "demo.wav"
        write_wav(wav, np.concatenate(demo))
        demo_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-b:a", "128k", str(demo_path)], check=True)
    print("demo ->", demo_path)
