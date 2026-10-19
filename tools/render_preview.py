#!/usr/bin/env python3
"""
Renderiza vistas previas (PNG) del modelo generado por generate_heracles.py,
sin necesidad de Blockbench. Usa proyeccion ortografica + z-buffer.

Uso: python3 tools/render_preview.py <salida.png> [anim:tiempo ...]
   ej: python3 tools/render_preview.py preview.png idle:0 attack:0.35 attack:0.5
"""
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import generate_heracles as G  # noqa: E402

SCALE = 7


def rot_matrix(rx, ry, rz):
    rx, ry, rz = map(math.radians, (rx, ry, rz))
    cx, sx, cy, sy, cz, sz = math.cos(rx), math.sin(rx), math.cos(ry), math.sin(ry), math.cos(rz), math.sin(rz)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx  # orden de Euler 'ZYX' de Blockbench


def sample_track(kfs, t):
    times = sorted(kfs)
    if t <= times[0]:
        return kfs[times[0]][:3]
    if t >= times[-1]:
        return kfs[times[-1]][:3]
    for a, b in zip(times, times[1:]):
        if a <= t <= b:
            f = (t - a) / (b - a)
            return tuple(kfs[a][i] * (1 - f) + kfs[b][i] * f for i in range(3))


def bone_matrices(anim=None, t=0.0):
    mats = {}

    def walk(b, parent):
        rx, ry, rz = b.rotation
        px = py = pz = 0
        if anim:
            if (b.name, "rotation") in anim.tracks:
                kx, ky, kz = sample_track(anim.tracks[(b.name, "rotation")], t)
                rx, ry, rz = rx - kx, ry - ky, rz + kz
            if (b.name, "position") in anim.tracks:
                kx, ky, kz = sample_track(anim.tracks[(b.name, "position")], t)
                px, py, pz = -kx, ky, kz
        o = np.array(b.origin, float)
        M = np.eye(4)
        M[:3, :3] = rot_matrix(rx, ry, rz)
        if anim and (b.name, "scale") in anim.tracks:
            M[:3, :3] = M[:3, :3] @ np.diag(sample_track(anim.tracks[(b.name, "scale")], t))
        T1, T2, TP = np.eye(4), np.eye(4), np.eye(4)
        T1[:3, 3] = o
        T2[:3, 3] = -o
        TP[:3, 3] = (px, py, pz)
        W = parent @ TP @ T1 @ M @ T2
        mats[b.name] = W
        for ch in b.children:
            if isinstance(ch, G.Bone):
                walk(ch, W)

    walk(G.root, np.eye(4))
    return mats


def face_corners(c, face):
    k = getattr(c, "inflate", 0) or 0
    (x0, y0, z0), (x1, y1, z1) = (v - k for v in c.frm), (v + k for v in c.to)
    return {
        "north": ((x1, y1, z0), (x0, y1, z0), (x1, y0, z0)),
        "south": ((x0, y1, z1), (x1, y1, z1), (x0, y0, z1)),
        "east":  ((x1, y1, z1), (x1, y1, z0), (x1, y0, z1)),
        "west":  ((x0, y1, z0), (x0, y1, z1), (x0, y0, z0)),
        "up":    ((x0, y1, z0), (x1, y1, z0), (x0, y1, z1)),
        "down":  ((x0, y0, z1), (x1, y0, z1), (x0, y0, z0)),
    }[face]


def render(tex, anim=None, t=0.0, yaw=-30, pitch=12, size=(420, 520), focus=None, scale=None):
    W, H = size
    img = np.zeros((H, W, 3), np.uint8)
    img[:] = (38, 42, 52)
    zbuf = np.full((H, W), np.inf)
    mats = bone_matrices(anim, t)
    V = np.eye(4)
    V[:3, :3] = rot_matrix(pitch, 0, 0) @ rot_matrix(0, yaw, 0)
    texa = np.asarray(tex.convert("RGBA"))
    th, tw = texa.shape[:2]
    sc = scale or SCALE
    cx, cy = W / 2, H * 0.86
    if focus is not None:  # centra la imagen en una altura Y del modelo
        cy = H / 2 + (V @ np.array([0, focus, 0, 1.0]))[1] * sc

    def proj(p):
        q = V @ np.append(p, 1.0)
        return np.array([cx - q[0] * sc, cy - q[1] * sc, q[2]])
    for c in G.CUBES:
        if c.mat == "hitbox":
            continue
        M = mats[c.bone.name]
        if getattr(c, "rot", None):
            a, deg = c.rot
            R = np.eye(4)
            R[:3, :3] = rot_matrix(*(deg if ax == a else 0 for ax in "xyz"))
            T1, T2 = np.eye(4), np.eye(4)
            T1[:3, 3] = c.pivot
            T2[:3, 3] = [-v for v in c.pivot]
            M = M @ T1 @ R @ T2
        for face, uv in c.uv.items():
            tl, tr, bl = (np.array((M @ np.append(np.array(p, float), 1.0))[:3]) for p in face_corners(c, face))
            P0, P1, P3 = proj(tl), proj(tr), proj(bl)
            e1, e2 = P1[:2] - P0[:2], P3[:2] - P0[:2]
            det = e1[0] * e2[1] - e1[1] * e2[0]
            if abs(det) < 1e-6:
                continue
            pts = np.array([P0[:2], P1[:2], P3[:2], P1[:2] + e2])
            xmin, ymin = np.floor(pts.min(0)).astype(int)
            xmax, ymax = np.ceil(pts.max(0)).astype(int)
            xmin, ymin = max(xmin, 0), max(ymin, 0)
            xmax, ymax = min(xmax, W - 1), min(ymax, H - 1)
            if xmin > xmax or ymin > ymax:
                continue
            ys, xs = np.mgrid[ymin:ymax + 1, xmin:xmax + 1]
            dx, dy = xs + 0.5 - P0[0], ys + 0.5 - P0[1]
            s = (dx * e2[1] - dy * e2[0]) / det
            r = (e1[0] * dy - e1[1] * dx) / det
            m = (s >= 0) & (s <= 1) & (r >= 0) & (r <= 1)
            if not m.any():
                continue
            z = P0[2] + s * (P1[2] - P0[2]) + r * (P3[2] - P0[2])
            u0, v0, u1, v1 = uv
            if face == "down":
                v0, v1 = v1, v0
            tu = ((u0 + s * (u1 - u0)) * G.PX).clip(0, tw - 1).astype(int)
            tv = ((v0 + r * (v1 - v0)) * G.PX).clip(0, th - 1).astype(int)
            col = texa[tv, tu]
            m &= col[..., 3] > 0
            m &= z < zbuf[ys, xs]
            zbuf[ys[m], xs[m]] = z[m]
            img[ys[m], xs[m]] = col[..., :3][m]
    return Image.fromarray(img)


def gif(anim_name, out, yaw=-30, fps=20, loops=1, size=(360, 440), pitch=12):
    tw, th = G.pack()
    tex = G.paint(tw, th)
    a = {x.name: x for x in G.ANIMS}[anim_name]
    n = int(round(a.length * fps * loops))
    frames = []
    for i in range(n + (0 if a.loop == "loop" else int(fps * 0.6))):
        t = min(i / fps % a.length if a.loop == "loop" else i / fps, a.length)
        im = render(tex, a, t, yaw=yaw, pitch=pitch, size=size, focus=22, scale=6.5)
        ImageDraw.Draw(im).text((8, 8), f"{anim_name}  {t:0.2f}s", fill=(235, 235, 235))
        frames.append(im.quantize(colors=255, method=Image.Quantize.MEDIANCUT))
    frames[0].save(out, save_all=True, append_images=frames[1:], duration=int(1000 / fps), loop=0, disposal=2)
    return out


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "preview.png"
    specs = sys.argv[2:] or ["rest:0@-30", "rest:0@150", "rest:0@90"]
    _, tex = G.build("/tmp/_heracles_preview.bbmodel") if False else (None, None)
    tw, th = G.pack()
    tex = G.paint(tw, th)
    anims = {a.name: a for a in G.ANIMS}
    frames = []
    for spec in specs:
        yaw = -30
        if "@" in spec:
            spec, y = spec.split("@")
            yaw = float(y)
        name, t = spec.split(":")
        im = render(tex, anims.get(name), float(t), yaw=yaw)
        ImageDraw.Draw(im).text((8, 8), f"{name} t={t} yaw={yaw:g}", fill=(230, 230, 230))
        frames.append(im)
    cols = min(4, len(frames))
    rows = math.ceil(len(frames) / cols)
    W, H = frames[0].size
    sheet = Image.new("RGB", (W * cols, H * rows), (20, 20, 24))
    for i, f in enumerate(frames):
        sheet.paste(f, ((i % cols) * W, (i // cols) * H))
    sheet.save(out)
    print("OK ->", out)


if __name__ == "__main__":
    main()
