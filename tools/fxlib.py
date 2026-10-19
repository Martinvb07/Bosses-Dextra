#!/usr/bin/env python3
"""
Piezas reutilizables para los efectos de los ataques (modelos de ModelEngine con animacion "play").

Cada funcion recibe un Model ya creado y le anade huesos, cubos y keyframes a la animacion "a".
Las distancias estan en unidades de Blockbench (16 = 1 bloque).

    m = fxlib.model("xx_fx_algo", mats, seed)        # Model con atlas ancho y decoraciones basicas
    a = m.anim("play", 1.2, "once")
    fxlib.wave(m, a, radius=128, ...)                 # anillo de trozos que se expande por el suelo
    fxlib.build_all(BUILDERS, BLUEPRINTS, PREVIEW, SHOTS, VIEW)   # genera .bbmodel y vistas previas
"""
import math
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
from bbmodel import Model  # noqa: E402


def model(name, mats, seed, px=2, atlas=256, shine=(), decor=None):
    m = Model(name, mats, seed=seed, atlas_w=atlas, px=px)
    m.SHINE |= set(shine)
    D = m.decor

    @D
    def d_crystal(f):
        for y in range(f.h):
            f.put(0, y, (250, 250, 255))

    @D
    def d_wisp(f):
        for y in range(f.h):
            for x in range(f.w):
                if (x * 3 + y * 5) % 7 == 0:
                    f.shade(x, y, 1.25)
                elif (x + y * 2) % 9 == 0:
                    f.shade(x, y, 0.8)

    if decor:
        decor(m)
    return m


def spin(a, bone, length, turns, axis="y", step=0.1, start=0.0):
    n = max(2, round((length - start) / step))
    for i in range(n + 1):
        t = start + (length - start) * i / n
        ang = 360 * turns * i / n
        a.rot(bone, t, *(ang if ax == axis else 0 for ax in "xyz"), i="linear")


# ------------------------------------------------------------------ piezas
def wave(m, a, prefix="w", n=20, radius=128, mats=("a", "b"), size=3.0, height=4.0, grow=2.6, t_end=1.0,
         tip=None, spikes=False, delay=0.0):
    """Anillo de trozos (o pinchos) que sale del centro y se expande hasta 'radius'."""
    for k in range(n):
        th = 2 * math.pi * k / n
        b = m.bone(f"{prefix}{k}", (0, 0, 0), m.root)
        mat = mats[k % len(mats)]
        if spikes and k % 2 == 0:
            m.cube(b, f"{prefix}{k}", (-size * 0.6, 0, -size * 0.6), (size * 0.6, height * 2.2, size * 0.6), mat,
                   decor={"all": "crystal"})
        else:
            m.cube(b, f"{prefix}{k}", (-size, 0, -size), (size, height, size), mat, decor={"all": "wisp"})
        if tip:
            m.cube(b, f"{prefix}{k}t", (-size * 0.5, height, -size * 0.5), (size * 0.5, height + size, size * 0.5), tip)
        keys = ((0, 8, 0.5), (0.2, radius * 0.55, grow * 0.8), (0.6, radius * 0.97, grow), (1.0, radius, 0.05))
        a.scl(f"{prefix}{k}", 0, 0.01)
        for f, r, s in keys:
            t = delay + f * t_end
            a.pos(f"{prefix}{k}", t, -r * math.cos(th), 0, r * math.sin(th), i="linear" if f else "catmullrom")
            a.scl(f"{prefix}{k}", t, s, s * (1 if f < 1.0 else 0.1), s)


def arc(m, a, name="arc", R=24, mats=("a", "b"), trail=None, tilt=30, y=18, z=-12, length=0.5, sweep=(-70, 30)):
    """Media luna de un tajo."""
    b = m.bone(name, (0, y, z), m.root, rotation=(0, 0, tilt))
    for k in range(13):
        th = math.pi * (0.08 + 0.84 * k / 12)
        x, yy = R * math.cos(th), y - R * 0.6 + R * math.sin(th)
        w = 1.4 + 1.8 * math.sin(math.pi * k / 12)
        m.cube(b, f"{name}{k}", (x - 1.7, yy - w / 2, z - 0.6), (x + 1.7, yy + w / 2, z + 0.6), mats[0] if 3 < k < 9 else mats[1])
        if trail:
            m.cube(b, f"{name}t{k}", (x * 0.85 - 1.3, yy - 3 - w / 3, z - 0.4), (x * 0.85 + 1.3, yy - 3 + w / 3, z + 0.4), trail)
    a.rot(name, 0, 0, sweep[0], 0)
    a.rot(name, length * 0.25, 0, sweep[1], 0, i="linear")
    a.rot(name, length, 0, sweep[1] + 15, 0)
    a.scl(name, 0, 0.7, 0.7, 1)
    a.scl(name, length * 0.25, 1.1, 1.1, 1)
    a.scl(name, length, 1.3, 0.05, 1)


def pillar(m, a, name="pillar", r=4, h=40, mat="a", core="b", t0=0.0, t_peak=0.2, t_end=1.2, bits=None, turns=1):
    b = m.bone(name, (0, 0, 0), m.root)
    m.cube(b, name, (-r, 0, -r), (r, h, r), mat, decor={"all": "wisp"})
    m.cube(b, name + "_core", (-r / 2, 0, -r / 2), (r / 2, h * 1.15, r / 2), core)
    if bits:
        for k in range(6):
            th = 2 * math.pi * k / 6
            x, z = (r + 3) * math.cos(th), (r + 3) * math.sin(th)
            m.cube(b, f"{name}_bit{k}", (x - 1, 6 + k * h / 8, z - 1), (x + 1, 9 + k * h / 8, z + 1), bits)
    a.scl(name, 0, 0.01)
    if t0:
        a.scl(name, t0, 0.01)
    a.scl(name, t_peak, 1.4, 1.1, 1.4, i="linear")
    a.scl(name, t_peak + (t_end - t_peak) * 0.5, 1.1, 1.0, 1.1)
    a.scl(name, t_end, 0.05, 1.3, 0.05)
    if turns:
        spin(a, name, t_end, turns)


def circle(m, a, name="circle", R=40, n=20, mats=("a", "b"), t_in=0.3, t_hold=1.4, t_end=1.8, turns=0.4, grow=None,
           items=None):
    """Circulo en el suelo (sello, runas). 'items' = funcion(m, bone, x, z, k) para colocar cosas encima."""
    b = m.bone(name, (0, 0, 0), m.root)
    for k in range(n):
        th = 2 * math.pi * k / n
        x, z = R * math.cos(th), R * math.sin(th)
        m.cube(b, f"{name}{k}", (x - 2, 0.1, z - 2), (x + 2, 0.4, z + 2), mats[k % len(mats)])
        if items and k % 2 == 0:
            items(m, b, x, z, k)
    m.cube(b, f"{name}_x", (-R * 0.85, 0.1, -0.7), (R * 0.85, 0.35, 0.7), mats[0])
    m.cube(b, f"{name}_z", (-0.7, 0.1, -R * 0.85), (0.7, 0.35, R * 0.85), mats[0])
    m.cube(b, f"{name}_d1", (-R * 0.7, 0.1, -0.7), (R * 0.7, 0.35, 0.7), mats[-1], rot=("y", 45), pivot=(0, 0, 0))
    m.cube(b, f"{name}_d2", (-R * 0.7, 0.1, -0.7), (R * 0.7, 0.35, 0.7), mats[-1], rot=("y", -45), pivot=(0, 0, 0))
    a.scl(name, 0, 0.05, 1, 0.05)
    if grow:
        a.scl(name, t_hold, grow, 1, grow, i="linear")
    else:
        a.scl(name, t_in, 1)
        a.scl(name, t_hold, 1)
    a.scl(name, t_end, 0.05, 1, 0.05)
    spin(a, name, t_end, turns)


def crystals_burst(m, a, prefix="c", spec=None, mat="a", tip="b", t_out=0.12, t_hold=0.65, t_end=1.0, fly=10):
    """Racimo de cristales que brota y luego estalla. spec = [(x, z, h, w, rot)]"""
    for k, (x, z, h, w, rot) in enumerate(spec):
        b = m.bone(f"{prefix}{k}", (x, 0, z), m.root)
        m.cube(b, f"{prefix}{k}", (x - w, 0, z - w), (x + w, h, z + w), mat, rot=rot, pivot=(x, 0, z), decor={"all": "crystal"})
        m.cube(b, f"{prefix}{k}t", (x - w * 0.5, h, z - w * 0.5), (x + w * 0.5, h + w * 1.8, z + w * 0.5), tip, rot=rot,
               pivot=(x, 0, z))
        a.scl(f"{prefix}{k}", 0, 0.05)
        a.scl(f"{prefix}{k}", t_out + 0.02 * k, 1.15)
        a.scl(f"{prefix}{k}", t_out + 0.12, 1)
        a.scl(f"{prefix}{k}", t_hold, 1)
        a.scl(f"{prefix}{k}", t_end, 0.05)
        ang = math.atan2(z, x if x else 0.01)
        a.pos(f"{prefix}{k}", t_hold, 0, 0, 0)
        a.pos(f"{prefix}{k}", t_end, -fly * math.cos(ang), 6, fly * math.sin(ang))


def rain(m, a, prefix="r", n=16, radius=120, h=(10, 16), w=3.0, mat="a", tip="b", top=120, t_window=0.5, t_end=1.6,
         seed=9):
    """Cosas que caen del cielo (carambanos, rayos de luz, meteoritos)."""
    rng = random.Random(seed)
    for k in range(n):
        r = 16 + rng.uniform(0, radius - 16)
        th = rng.uniform(0, 2 * math.pi)
        x, z = r * math.cos(th), r * math.sin(th)
        b = m.bone(f"{prefix}{k}", (x, 0, z), m.root)
        hh = rng.uniform(*h)
        m.cube(b, f"{prefix}{k}", (x - w, 2.5, z - w), (x + w, 2.5 + hh, z + w), mat, decor={"all": "crystal"})
        m.cube(b, f"{prefix}{k}t", (x - w / 2, 0, z - w / 2), (x + w / 2, 2.5, z + w / 2), tip)
        d = rng.uniform(0, t_window)
        a.pos(f"{prefix}{k}", 0, 0, top, 0)
        a.pos(f"{prefix}{k}", d, 0, top, 0)
        a.pos(f"{prefix}{k}", d + 0.35, 0, -2, 0, i="linear")
        a.pos(f"{prefix}{k}", t_end, 0, -3, 0)
        a.scl(f"{prefix}{k}", d + 0.35, 1)
        a.scl(f"{prefix}{k}", d + 0.45, 1.6, 0.4, 1.6)
        a.scl(f"{prefix}{k}", t_end, 0.05)


def dome(m, a, prefix="d", n=16, R=40, h=24, w=3.0, mat="a", tip="b", t_charge=2.0, t_end=2.8, burst=150):
    """Cupula de pinchos que crece durante la carga y luego sale disparada."""
    for k in range(n):
        th = 2 * math.pi * k / n
        b = m.bone(f"{prefix}{k}", (0, 0, 0), m.root)
        x, z = R * math.cos(th), R * math.sin(th)
        tilt = ("x", -22.5) if k % 2 else ("z", 22.5)
        hh = h * (0.75 + 0.25 * (k % 3))
        m.cube(b, f"{prefix}{k}", (x - w, 0, z - w), (x + w, hh, z + w), mat, rot=tilt, pivot=(x, 0, z), decor={"all": "crystal"})
        m.cube(b, f"{prefix}{k}t", (x - w / 2, hh, z - w / 2), (x + w / 2, hh + w * 1.6, z + w / 2), tip, rot=tilt, pivot=(x, 0, z))
        a.scl(f"{prefix}{k}", 0, 0.05)
        a.scl(f"{prefix}{k}", t_charge, 1.0, i="linear")
        a.scl(f"{prefix}{k}", t_charge + 0.1, 1.2)
        a.pos(f"{prefix}{k}", t_charge, 0, 0, 0)
        a.pos(f"{prefix}{k}", t_end, -burst * math.cos(th), 20, burst * math.sin(th), i="linear")
        a.scl(f"{prefix}{k}", t_end, 0.2)


def smoke(m, a, prefix="p", n=8, R=14, size=4.0, mats=("a", "b"), drops=None, t_end=1.2, grow=1.5):
    pts = [(0, 6, 0)] + [(R * math.cos(2 * math.pi * k / n), 4 + (k % 2) * 7, R * math.sin(2 * math.pi * k / n))
                         for k in range(n)]
    for k, (x, y, z) in enumerate(pts):
        b = m.bone(f"{prefix}{k}", (x, y, z), m.root)
        s = size * (1.2 if k == 0 else 1.0)
        m.cube(b, f"{prefix}{k}", (x - s, y - s * 0.8, z - s), (x + s, y + s * 0.8, z + s), mats[k % len(mats)],
               decor={"all": "wisp"})
        if drops:
            m.cube(b, f"{prefix}{k}d", (x - 0.8, y - s * 0.8 - 2, z - 0.8), (x + 0.8, y - s * 0.8, z + 0.8), drops)
        a.scl(f"{prefix}{k}", 0, 0.05)
        a.scl(f"{prefix}{k}", 0.25 + 0.03 * k, grow)
        a.scl(f"{prefix}{k}", t_end * 0.65, grow * 1.07)
        a.scl(f"{prefix}{k}", t_end, 0.05)
        a.pos(f"{prefix}{k}", t_end, 0, 6, 0)


def portal(m, a, name="portal", rx=9, ry=13, y=18, rim=("a", "b"), core="c", mote="d", length=1.2):
    p = m.bone(name, (0, y, 0), m.root)
    for k in range(18):
        th = 2 * math.pi * k / 18
        x, yy = rx * math.cos(th), ry * math.sin(th)
        m.cube(p, f"{name}rim{k}", (x - 1.8, y + yy - 1.8, -1.2), (x + 1.8, y + yy + 1.8, 1.2), rim[k % 3 == 0])
    c = m.bone(name + "_core", (0, y, 0), p)
    m.cube(c, name + "_core", (-rx + 2, y - ry + 2, -0.3), (rx - 2, y + ry - 2, 0.3), core, decor={"all": "wisp"})
    sw = m.bone(name + "_swirl", (0, y, 0), p)
    for k in range(6):
        th = 2 * math.pi * k / 6
        x, yy = rx * 0.5 * math.cos(th), ry * 0.5 * math.sin(th)
        m.cube(sw, f"{name}m{k}", (x - 0.8, y + yy - 0.8, -0.8), (x + 0.8, y + yy + 0.8, 0.8), mote)
    a.scl(name, 0, 0.05, 0.05, 1)
    a.scl(name, length * 0.2, 1.15, 1.15, 1)
    a.scl(name, length * 0.3, 1)
    a.scl(name, length * 0.75, 1)
    a.scl(name, length, 0.05, 1.3, 1)
    spin(a, name + "_swirl", length, 1.5, "z")


def spiral(m, a, prefix="s", n=24, r0=6, r1=112, height=30, mats=("a", "b"), size=1.4, turns=1.0, t_end=1.6, grow=2.6):
    """Cosas que giran en espiral hacia fuera (petalos, almas, chispas)."""
    for k in range(n):
        b = m.bone(f"{prefix}{k}", (0, 0, 0), m.root)
        m.cube(b, f"{prefix}{k}", (-size, -size * 0.4, -size), (size, size * 0.4, size), mats[k % len(mats)])
        th0 = 2 * math.pi * k / n
        h = height * (0.3 + 0.7 * ((k * 7) % n) / n)
        steps = 8
        for i in range(steps + 1):
            t = t_end * i / steps
            f = i / steps
            r = r0 + (r1 - r0) * f ** 0.8
            th = th0 + 2 * math.pi * turns * f
            yy = h * math.sin(math.pi * min(1, f * 1.2))
            a.pos(f"{prefix}{k}", t, -r * math.cos(th), yy, r * math.sin(th), i="linear")
            a.rot(f"{prefix}{k}", t, 70 * i * ((k % 2) * 2 - 1), 90 * i, 0, i="linear")
            a.scl(f"{prefix}{k}", t, (1.0 + grow * f) if i < steps else 0.05, i="linear")


def rise_ring(m, a, prefix="o", n=8, R=40, piece=None, t_up=0.3, t_hold=1.3, t_end=1.7, depth=24, stagger=0.03,
              face_out=True):
    """Objetos que salen del suelo en anillo y luego se hunden. piece(m, bone, x, z, k) dibuja cada uno."""
    for k in range(n):
        th = 2 * math.pi * k / n
        x, z = R * math.cos(th), R * math.sin(th)
        b = m.bone(f"{prefix}{k}", (x, 0, z), m.root, rotation=(0, -math.degrees(th) - 90, 0) if face_out else (0, 0, 0))
        piece(m, b, x, z, k)
        d = stagger * k
        a.pos(f"{prefix}{k}", 0, 0, -depth, 0)
        a.pos(f"{prefix}{k}", d, 0, -depth, 0)
        a.pos(f"{prefix}{k}", d + t_up, 0, 1, 0)
        a.pos(f"{prefix}{k}", d + t_up + 0.1, 0, 0, 0)
        a.pos(f"{prefix}{k}", t_hold, 0, 0, 0)
        a.pos(f"{prefix}{k}", t_end, 0, -depth, 0)


def floating_glyph(m, a, name, rows, pal, px=1.6, y=46, t_end=3.0, turns=1.0, ring=None):
    """Sello (pixel art en cubos) que flota y gira sobre el objetivo."""
    b = m.bone(name, (0, y, 0), m.root)
    w = max(len(r) for r in rows)
    for ry, row in enumerate(rows):
        x = 0
        while x < len(row):
            ch = row[x]
            if ch not in pal:
                x += 1
                continue
            x1 = x
            while x1 < len(row) and row[x1] == ch:
                x1 += 1
            xx = (x - w / 2) * px
            yy = y + (len(rows) / 2 - ry) * px
            m.cube(b, f"{name}{ry}_{x}", (xx, yy, -0.5), ((x1 - w / 2) * px, yy + px, 0.5), pal[ch])
            x = x1
    if ring:
        for k in range(12):
            th = 2 * math.pi * k / 12
            r = w * px * 0.6
            m.cube(b, f"{name}_ring{k}", (r * math.cos(th) - 0.8, y + r * math.sin(th) - 0.8, -0.4),
                   (r * math.cos(th) + 0.8, y + r * math.sin(th) + 0.8, 0.4), ring)
    a.scl(name, 0, 0.05)
    a.scl(name, 0.3, 1.2)
    a.scl(name, 0.45, 1)
    a.scl(name, t_end * 0.85, 1.05)
    a.scl(name, t_end, 0.05)
    if turns:
        spin(a, name, t_end, turns)


# ------------------------------------------------------------------ generar todo
def previews(m, name, preview_dir, shots, view):
    import render_preview as RP
    RP.G = m
    tw, th = m.pack()
    tex = m.paint(tw, th)
    a = m.ANIMS[0]
    focus, scale, yaw = view
    frames = []
    for t in shots:
        im = RP.render(tex, a, t, yaw=yaw, pitch=20, size=(300, 300), focus=focus, scale=scale)
        ImageDraw.Draw(im).text((8, 8), f"{name}  {t:g}s", fill=(230, 230, 230))
        frames.append(im)
    sheet = Image.new("RGB", (300 * len(frames), 300))
    for i, f in enumerate(frames):
        sheet.paste(f, (i * 300, 0))
    preview_dir.mkdir(parents=True, exist_ok=True)
    sheet.save(preview_dir / f"{name}.png")


def build_all(builders, blueprints, preview_dir, shots, view, argv=None):
    argv = sys.argv[1:] if argv is None else argv
    only = [x for x in argv if not x.startswith("--")]
    for name, fn in builders.items():
        if only and name not in only:
            continue
        m = fn()
        out = blueprints / name / f"{name}.bbmodel"
        out.parent.mkdir(parents=True, exist_ok=True)
        m.build(out)
        print(f"OK {name}: cubos={len(m.CUBES)} huesos={len(m.BONES)}")
        if "--no-preview" not in argv:
            previews(m, name, preview_dir, shots[name], view[name])


def sheet(preview_dir, names, out):
    ims = [Image.open(preview_dir / f"{n}.png") for n in names]
    S = Image.new("RGB", (max(i.width for i in ims), sum(i.height for i in ims)))
    y = 0
    for im in ims:
        S.paste(im, (0, y))
        y += im.height
    S.save(out)


def action_sheet(model, shots, out, focus=34, scale=4.4):
    """Hoja con 8 poses clave del boss: shots = [(anim, t, yaw)]"""
    import render_preview as RP
    RP.G = model
    tw, th = model.pack()
    tex = model.paint(tw, th)
    A = {a.name: a for a in model.ANIMS}
    fr = []
    for an, t, y in shots:
        im = RP.render(tex, A[an], t, yaw=y, size=(300, 400), focus=focus, scale=scale)
        ImageDraw.Draw(im).text((8, 8), f"{an} {t:g}s", fill=(230, 230, 230))
        fr.append(im)
    S = Image.new("RGB", (1200, 400 * ((len(fr) + 3) // 4)))
    for i, f in enumerate(fr):
        S.paste(f, ((i % 4) * 300, (i // 4) * 400))
    S.save(out)
