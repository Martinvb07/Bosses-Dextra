#!/usr/bin/env python3
"""
Boss 11 - AZATHOTH y sus subditos (modelos de ModelEngine).

  azathoth        el Caos Ancestral: masa cosmica flotante (piel de vacio con estrellas), fauces con
                  dientes, gran ojo central con parpados, ojos repartidos por el cuerpo, corona de
                  tentaculos, faldon de tentaculos que ondulan, dos tentaculos-brazo, planetas en
                  orbita y un aro de nebulosa a la espalda
  az_spawn        engendro del vacio: humanoide encorvado con tentaculos en la cara y muchos ojos (HUSK)
  az_piper        flautista demente: tunica, mascara con espiral y flauta de hueso (HUSK)
  az_larva        larva estelar: gusano segmentado con manchas de estrellas, mandibulas y patas (SPIDER)
  az_priest       sacerdote del caos: tunica, mitra alta y baculo con un ojo (STRAY)

Uso: python3 tools/b11_azathoth.py [modelo ...] [--no-preview]
"""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from bbmodel import Model  # noqa: E402
import anatomy as AN  # noqa: E402
import generate_minions as GM  # noqa: E402
import fxlib as FX  # noqa: E402
import b10_kronos as KR  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent / "Modelos/11_Azathoth"
BLUEPRINTS = ROOT / "ModelEngine/blueprints"
PREVIEW = ROOT / "preview"

IRIS = (230, 80, 255)
MATS = {
    "void": ((34, 16, 54), 5), "void_dark": ((14, 8, 24), 4), "flesh": ((96, 44, 118), 8), "flesh_dark": ((62, 26, 84), 7),
    "eye": ((240, 236, 220), 3), "glow": (IRIS, 3), "teeth": ((232, 226, 210), 4), "maw": ((120, 20, 60), 5),
    "star": ((255, 240, 200), 2), "nebula": ((130, 60, 210), 6), "nebula_pink": ((220, 90, 200), 6),
    "robe": ((52, 30, 70), 6), "robe_dark": ((30, 18, 44), 5), "bone": ((214, 206, 186), 6), "gold": ((200, 160, 70), 7),
    "skin": ((120, 110, 130), 6), "mask": ((210, 200, 180), 4), "chitin": ((70, 40, 100), 7), "hitbox": ((255, 255, 255), 0),
}


def void_decor(m):
    D = m.decor

    @D
    def d_cosmic(f):
        """Piel de vacio: estrellas sueltas y manchas de nebulosa."""
        rng = random.Random(f.x0 * 31 + f.y0 * 7 + len(f.name))
        for y in range(f.h):
            for x in range(f.w):
                r = rng.random()
                if r < 0.03:
                    f.put(x, y, (255, 240, 210))
                elif r < 0.08:
                    f.shade(x, y, 1.45)
                elif r < 0.12:
                    f.put(x, y, (150, 70, 200))

    @D
    def d_eye(f):
        if f.name != "north":
            return
        w, h = f.w, f.h
        f.rect(0, 0, w, h, (236, 232, 216))
        for y in range(h):
            for x in range(w):
                if (x - w / 2 + 0.5) ** 2 / (w / 2) ** 2 + (y - h / 2 + 0.5) ** 2 / (h / 2) ** 2 > 0.95:
                    f.put(x, y, (150, 60, 90))
        r = max(1, min(w, h) // 3)
        f.rect(w // 2 - r, h // 2 - r, w // 2 + r, h // 2 + r, IRIS)
        p = max(1, r // 2)
        f.rect(w // 2 - p, h // 2 - r + 1, w // 2 + p, h // 2 + r - 1, (10, 4, 16))
        f.put(w // 2 - r, h // 2 - r, (255, 255, 255))

    @D
    def d_veins(f):
        rng = random.Random(f.x0 + f.y0 * 13)
        for _ in range(max(1, f.w * f.h // 40)):
            x, y = rng.randrange(f.w), rng.randrange(f.h)
            for _ in range(5):
                f.put(x, y, (180, 60, 160))
                x += rng.choice((-1, 0, 1))
                y += 1

    @D
    def d_suckers(f):
        if f.name not in ("south", "north"):
            return
        for y in range(1, f.h - 1, 3):
            f.put(f.w // 2, y, (200, 120, 200))

    @D
    def d_maw(f):
        if f.name != "north":
            return
        f.rect(0, 0, f.w, f.h, (60, 6, 30))
        for x in range(0, f.w, 3):
            f.put(x, 0, (232, 226, 210))
            f.put(x + 1, 1, (232, 226, 210))
            f.put(x, f.h - 1, (232, 226, 210))
            f.put(x + 1, f.h - 2, (232, 226, 210))
        f.rect(f.w // 2 - 2, f.h // 2 - 1, f.w // 2 + 2, f.h // 2 + 1, (20, 0, 10))

    @D
    def d_spiral(f):
        if f.name != "north":
            return
        w, h = f.w, f.h
        cx, cy = w / 2, h / 2
        for k in range(60):
            a = k * 0.35
            r = 0.12 * k
            f.put(round(cx + r * math.cos(a)), round(cy + r * math.sin(a)), (90, 20, 120))
        f.put(int(cx) - 3, int(cy) - 2, IRIS)
        f.put(int(cx) + 2, int(cy) - 2, IRIS)

    @D
    def d_many_eyes(f):
        if f.name != "north":
            return
        for (x, y) in ((2, 3), (f.w - 4, 3), (f.w // 2 - 1, 1), (3, 7), (f.w - 5, 7)):
            f.rect(x, y, x + 2, y + 2, (240, 236, 220))
            f.put(x + 1, y + 1, (10, 4, 16))
            f.put(x, y, IRIS)

    @D
    def d_robe(f):
        if f.name in ("up", "down"):
            return
        for x in range(f.w):
            f.put(x, f.h - 1, (200, 160, 70))
        for x in range(2, f.w, 5):
            for y in range(f.h - 1):
                f.shade(x, y, 0.82)

    @D
    def d_star_spots(f):
        rng = random.Random(f.x0 * 3 + f.y0)
        for _ in range(max(1, f.w * f.h // 14)):
            x, y = rng.randrange(f.w), rng.randrange(f.h)
            f.put(x, y, (255, 240, 210))
            f.put(x + 1, y, (220, 140, 255))

    @D
    def d_crystal(f):
        for y in range(f.h):
            f.put(0, y, (250, 240, 255))

    @D
    def d_priest_skull(f):
        if f.name != "north":
            return
        w = f.w
        for ex in (2, w - 6):
            f.rect(ex, 5, ex + 4, 9, (20, 10, 30))
            f.rect(ex + 1, 6, ex + 3, 8, IRIS)
        f.rect(w // 2 - 1, 9, w // 2 + 1, 11, (40, 30, 40))
        for x in range(3, w - 3, 2):
            f.put(x, 12, (40, 30, 40))


def _model(name, seed, atlas=256):
    m = Model(name, MATS, seed=seed, atlas_w=atlas)
    m.SHINE |= {"glow", "gold", "star", "eye"}
    GM.add_common_decor(m)
    void_decor(m)
    return m


C = {"decor": {"all": "cosmic"}}
V = {"decor": {"all": "veins"}}


def orb(m, bone, name, cx, cy, cz, r, mat="void", inner="flesh", deco=C):
    """Esfera aproximada: cubo central y tres cubos girados 45 grados (en X, Y y Z)."""
    c = r * 0.74
    m.cube(bone, name, (cx - c, cy - c, cz - c), (cx + c, cy + c, cz + c), mat, **deco)
    q, h = r * 0.66, r * 0.86
    for ax, frm, to, mt in (("y", (-q, -h, -q), (q, h, q), inner), ("x", (-h, -q, -q), (h, q, q), mat),
                            ("z", (-q, -q, -h), (q, q, h), inner)):
        m.cube(bone, f"{name}_{ax}", (cx + frm[0], cy + frm[1], cz + frm[2]), (cx + to[0], cy + to[1], cz + to[2]), mt,
               rot=(ax, 45), pivot=(cx, cy, cz), **deco)


def tentacle(m, parent, name, base, n=5, L=3.6, w0=1.6, mats=("flesh", "flesh_dark"), up=False, tip="glow"):
    """Tentaculo: cadena de n huesos (hacia abajo, o hacia arriba con up=True) que se afina.
    Devuelve los nombres de los huesos."""
    x, y, z = base
    sgn = 1 if up else -1
    bones = []
    prev = parent
    for i in range(n):
        w = w0 * (1 - 0.15 * i)
        y0 = y + sgn * i * L
        b = m.bone(f"{name}{i}", (x, y0, z), prev)
        y1 = y0 + sgn * (L + 0.3)
        m.cube(b, f"{name}{i}", (x - w, min(y0, y1), z - w), (x + w, max(y0, y1), z + w), mats[i % 2],
               decor={"all": "suckers"})
        if i == n - 1 and tip:
            m.cube(b, f"{name}tip", (x - w * 0.5, min(y1, y1 + sgn * 1.4), z - w * 0.5),
                   (x + w * 0.5, max(y1, y1 + sgn * 1.4), z + w * 0.5), tip)
        bones.append(f"{name}{i}")
        prev = b
    return bones


def wave(a, bones, length, amp=18, axis="x", phase=0.0, steps=8, base=(0, 0, 0)):
    for k in range(steps + 1):
        t = length * k / steps
        for i, b in enumerate(bones):
            v = amp * (0.5 + 0.5 * i / max(1, len(bones) - 1)) * math.sin(2 * math.pi * k / steps + phase + i * 0.8)
            r = list(base) if i == 0 else [0, 0, 0]
            r["xyz".index(axis)] += v
            a.rot(b, t, *r)


# ===========================================================================
# AZATHOTH
# ===========================================================================
def build_azathoth():
    m = _model("azathoth", 1111, atlas=512)
    root = m.root
    hb = m.bone("hitbox", (0, 24, 0), root)
    m.cube(hb, "hitbox", (-8, 0, -8), (8, 44, 8), "hitbox")
    m.bone("tag_name", (0, 52, 0), root)
    body = m.bone("body", (0, 28, 0), root)
    # masa central
    orb(m, body, "core", 0, 29, 0, 8.5)
    orb(m, body, "lobe_top", 0, 37, 1.5, 5.0, mat="flesh", inner="void", deco=V)
    orb(m, body, "lobe_l", -6.5, 25, 2, 4.4, mat="flesh_dark", inner="void", deco=V)
    orb(m, body, "lobe_r", 6.5, 26, 1.5, 4.0, mat="flesh_dark", inner="void", deco=V)
    orb(m, body, "lobe_b", 0, 22, 3, 5.5, mat="void", inner="flesh_dark")
    # fauces
    m.cube(body, "maw", (-5.0, 22.5, -9.4), (5.0, 27.5, -8.2), "maw", decor={"north": "maw"})
    for i, x in enumerate((-4.2, -2.4, -0.6, 1.2, 3.0)):
        m.cube(body, f"tooth_up{i}", (x, 26.0, -9.8), (x + 1.0, 28.4, -8.8), "teeth", rot=("x", -22.5), pivot=(x + 0.5, 28, -9.3))
    jw = m.bone("jaw", (0, 24.0, -7.5), body)
    m.cube(jw, "jaw", (-5.6, 19.6, -10.4), (5.6, 23.4, -6.0), "flesh", **V)
    for i, x in enumerate((-4.0, -2.0, 0.0, 2.0)):
        m.cube(jw, f"tooth_dn{i}", (x - 0.5, 22.6, -10.0), (x + 0.5, 25.0, -9.0), "teeth")
    # gran ojo central con parpados
    eye = m.bone("eye_main", (0, 32.5, -8.4), body)
    m.cube(eye, "eye_main", (-3.4, 29.4, -10.6), (3.4, 35.6, -7.4), "eye", decor={"all": "eye"})
    lt = m.bone("lid_top", (0, 35.6, -9.0), body)
    m.cube(lt, "lid_top", (-3.9, 32.4, -11.4), (3.9, 36.2, -9.6), "flesh", rot=("x", 22.5), pivot=(0, 35.6, -9.8), **V)
    lb = m.bone("lid_bot", (0, 29.4, -9.0), body)
    m.cube(lb, "lid_bot", (-3.9, 28.8, -11.2), (3.9, 31.0, -9.6), "flesh_dark", **V)
    # ojos repartidos (cada uno en un hueso girado hacia fuera)
    eyes = [(0, 38.5, 55, 0.9), (-40, 31, 35, 1.2), (40, 33, 30, 1.0), (-75, 26, 60, 0.8), (80, 24, 70, 0.9),
            (-25, 40.5, 15, 0.7), (25, 21, 120, 0.8), (150, 30, 20, 1.1), (-140, 34, 40, 0.9), (180, 24, 0, 1.0)]
    for i, (yaw, y, dist_k, s) in enumerate(eyes):
        e = m.bone(f"eye{i}", (0, y, 0), body, rotation=(0, yaw, 0))
        rr = 8.6 + (0.6 if dist_k > 50 else 0)
        m.cube(e, f"eye{i}", (-1.6 * s, y - 1.4 * s, -rr - 1.0), (1.6 * s, y + 1.4 * s, -rr + 0.6), "eye", decor={"all": "eye"})
        m.cube(e, f"eye{i}_lid", (-1.9 * s, y + 1.0 * s, -rr - 1.2), (1.9 * s, y + 1.9 * s, -rr + 0.4), "flesh_dark")
    # corona de tentaculos (arriba) y faldon (abajo)
    crown, skirt = [], []
    for k in range(6):
        yaw = 60 * k + 30
        cb = m.bone(f"crown_root{k}", (0, 38, 0), body, rotation=(0, yaw, 0))
        tb = m.bone(f"crown_tilt{k}", (0, 38.5, -4.0), cb, rotation=(-35, 0, 0))
        crown.append(tentacle(m, tb, f"ct{k}_", (0, 38.5, -4.0), n=4, L=3.2, w0=1.1, up=True,
                              mats=("void", "nebula") if k % 2 else ("flesh", "void")))
    for k in range(8):
        yaw = 45 * k
        sb = m.bone(f"skirt_root{k}", (0, 22, 0), body, rotation=(0, yaw, 0))
        tb = m.bone(f"skirt_tilt{k}", (0, 22, -5.5), sb, rotation=(18, 0, 0))
        skirt.append(tentacle(m, tb, f"st{k}_", (0, 22, -5.5), n=5, L=3.6, w0=1.6 if k % 2 else 1.3,
                              mats=("flesh", "flesh_dark") if k % 2 else ("void", "flesh")))
    # tentaculos-brazo
    arms = {}
    for side, sx in (("right", 1), ("left", -1)):
        ab = m.bone(f"{side}_arm", (8.0 * sx, 29, 0), body, rotation=(0, 0, 50 * sx))
        arms[side] = tentacle(m, ab, f"{side}_t", (8.0 * sx, 29, 0), n=6, L=4.0, w0=2.0)
    # planetas en orbita y aro de nebulosa
    orbit = m.bone("orbit", (0, 29, 0), body)
    for i, (r, y, s, mat) in enumerate(((18, 33, 1.8, "nebula_pink"), (20, 24, 1.3, "star"), (16, 40, 1.1, "nebula"))):
        a = 2 * math.pi * i / 3
        x, z = r * math.cos(a), r * math.sin(a)
        orb(m, orbit, f"planet{i}", x, y, z, s, mat=mat, inner=mat, deco={"decor": {}})
    halo = m.bone("halo", (0, 31, 9), body)
    KR.ring(m, halo, "halo", 0, 31, 9.0, 9.8, 15, "nebula", n=16, t=1.2)
    for k in range(8):
        a = 2 * math.pi * k / 8
        x, y = 15 * math.cos(a), 31 + 15 * math.sin(a)
        m.cube(halo, f"halo_star{k}", (x - 0.9, y - 0.9, 8.8), (x + 0.9, y + 0.9, 10.0), "star", rot=("z", 45), pivot=(x, y, 9.4))
    lefts = arms["left"]
    rights = arms["right"]
    m.ZERO_BONES = (["body", "jaw", "eye_main", "lid_top", "lid_bot", "orbit", "halo"] + sum(crown, []) + sum(skirt, [])
                    + lefts + rights)

    def float_loop(a, length, speed=1.0, amp=1.0):
        for t, s in ((0, 0), (length / 2, 1), (length, 0)):
            a.pos("body", t, 0, 1.4 * s * amp, 0)
            a.rot("jaw", t, 8 * s, 0, 0)
        for k, bs in enumerate(skirt):
            wave(a, bs, length, amp=14 * amp, axis="x", phase=k * 0.8)
        for k, bs in enumerate(crown):
            wave(a, bs, length, amp=12 * amp, axis="z", phase=k * 1.1)
        wave(a, rights, length, amp=10 * amp, axis="z", phase=0.3)
        wave(a, lefts, length, amp=10 * amp, axis="z", phase=2.1)
        FX.spin(a, "orbit", length, 0.5 * speed)
        FX.spin(a, "halo", length, -0.25 * speed, "z")

    a = m.anim("idle", 3.0, "loop")
    float_loop(a, 3.0)
    for t, ang in ((0, (0, 0, 0)), (1.0, (0, 12, 0)), (2.0, (0, -12, 0)), (3.0, (0, 0, 0))):
        a.rot("eye_main", t, *ang)
    a = m.anim("walk", 2.0, "loop")
    float_loop(a, 2.0, 1.5)
    a.rot("body", 0, 10, 0, 0)
    a.rot("body", 2.0, 10, 0, 0)

    def anim(name, length, keys, loop_extra=None):
        a = m.anim(name, length, "once")
        a.rest(0)
        for t, pose, lin in keys:
            a.pose(t, pose, i="linear" if lin else "catmullrom")
        a.rest(length)
        if loop_extra:
            loop_extra(a, length)
        return a

    def arm_pose(side, ang):
        bones = rights if side == "right" else lefts
        return {b: ang if i == 0 else tuple(v * 0.35 for v in ang) for i, b in enumerate(bones)}

    lunge = {"body": {"r": (25, 0, 0), "p": (0, 0, -3)}, **arm_pose("right", (-60, 0, -40)), **arm_pose("left", (-60, 0, 40))}
    anim("attack", 0.8, [(0.2, {**arm_pose("right", (40, 0, 30)), "jaw": (30, 0, 0)}, False),
                         (0.35, {**lunge, "jaw": (0, 0, 0)}, True)])
    a = anim("teleport", 1.2, [(0.2, {"jaw": (35, 0, 0), "lid_top": (-40, 0, 0)}, False)])
    a.scl("body", 0, 1)
    a.scl("body", 0.25, 1.15, 0.6, 1.15)
    a.scl("body", 0.35, 0.05)
    a.scl("body", 0.55, 0.05)
    a.scl("body", 0.65, 1.2)
    a.scl("body", 0.8, 1)
    swell = {**arm_pose("right", (0, 0, 60)), **arm_pose("left", (0, 0, -60)), "jaw": (40, 0, 0), "lid_top": (-45, 0, 0)}
    a = anim("pulse", 1.0, [(0.25, swell, False), (0.6, swell, False)])
    a.scl("body", 0, 1)
    a.scl("body", 0.2, 1.2)
    a.scl("body", 0.3, 0.95)
    a.scl("body", 0.6, 1)
    slam = {"body": {"r": (20, 0, 0), "p": (0, -6, 0)}, **arm_pose("right", (-90, 0, 20)), **arm_pose("left", (-90, 0, -20)),
            "jaw": (30, 0, 0)}
    anim("collapse", 1.3, [(0.3, {"body": {"p": (0, 6, 0)}, **arm_pose("right", (60, 0, 60)), **arm_pose("left", (60, 0, -60))},
                            False), (0.5, slam, True), (0.9, slam, False)])
    stare = {"body": {"r": (15, 0, 0), "p": (0, 0, -2)}, "lid_top": (-50, 0, 0), "lid_bot": (30, 0, 0), "eye_main": (0, 0, 0)}
    a = anim("gaze", 1.2, [(0.3, stare, False), (0.9, stare, False)])
    a.scl("eye_main", 0, 1)
    a.scl("eye_main", 0.45, 1.35)
    a.scl("eye_main", 0.55, 1.2)
    a.scl("eye_main", 1.2, 1)

    def spin_body(a, length):
        FX.spin(a, "orbit", length, 2.0)
        FX.spin(a, "halo", length, -1.0, "z")

    anim("storm", 1.6, [(0.3, {**arm_pose("right", (0, 0, 80)), **arm_pose("left", (0, 0, -80))}, False),
                        (1.2, {**arm_pose("right", (0, 0, 80)), **arm_pose("left", (0, 0, -80))}, False)], spin_body)
    grab = {**arm_pose("right", (-80, -40, 0)), **arm_pose("left", (-80, 40, 0)), "jaw": (35, 0, 0)}
    anim("warp", 1.2, [(0.2, grab, False), (0.4, {**arm_pose("right", (-40, 40, 0)), **arm_pose("left", (-40, -40, 0)),
                                                  "body": {"p": (0, 0, 3)}}, True), (0.8, grab, False)], spin_body)
    tear = {**arm_pose("right", (0, 0, 100)), **arm_pose("left", (0, 0, -100)), "jaw": (45, 0, 0), "lid_top": (-50, 0, 0),
            "body": {"p": (0, 4, 0)}}
    anim("rift", 1.6, [(0.4, {**arm_pose("right", (-90, 0, -30)), **arm_pose("left", (-90, 0, 30))}, False),
                       (0.9, tear, True), (1.3, tear, False)], spin_body)
    anim("summon", 1.4, [(0.4, {**arm_pose("right", (40, 0, 30)), **arm_pose("left", (40, 0, -30)), "jaw": (40, 0, 0),
                                "body": {"p": (0, 3, 0)}}, False), (1.0, {"jaw": (40, 0, 0)}, False)], spin_body)
    a = anim("phase_change", 2.0, [(0.5, {"body": {"r": (25, 0, 0), "p": (0, -4, 0)}, "lid_top": (0, 0, 0)}, False),
                                   (1.0, tear, True), (1.6, tear, False)], spin_body)
    a.scl("body", 0.5, 0.9)
    a.scl("body", 1.0, 1.25)
    a.scl("body", 1.3, 1.0)
    a = m.anim("hurt", 0.35, "once")
    a.rest(0, ["body", "lid_top", "jaw"])
    a.pose(0.1, {"body": (-10, 0, 5), "lid_top": (20, 0, 0), "jaw": (20, 0, 0)})
    a.rest(0.35, ["body", "lid_top", "jaw"])
    a = m.anim("spawn", 2.4, "once")
    a.scl("body", 0, 0.05)
    a.scl("body", 1.2, 1.1)
    a.scl("body", 1.5, 1.0)
    a.pose(0, {"lid_top": (25, 0, 0)})
    a.pose(1.5, {"lid_top": (25, 0, 0)})
    a.pose(1.8, {"lid_top": (-50, 0, 0), "jaw": (45, 0, 0)}, i="linear")
    a.rest(2.4, ["lid_top", "jaw"])
    spin_body(a, 2.4)
    a = m.anim("death", 2.6, "hold")
    a.rest(0)
    a.pose(0.6, {"lid_top": (-50, 0, 0), "jaw": (50, 0, 0), **arm_pose("right", (0, 0, 90)), **arm_pose("left", (0, 0, -90))})
    a.pose(1.6, {"lid_top": (25, 0, 0), "jaw": (10, 0, 0)})
    a.scl("body", 0.6, 1.15)
    a.scl("body", 1.6, 1.0)
    a.scl("body", 2.6, 0.05)
    a.pos("body", 1.6, 0, 0, 0)
    a.pos("body", 2.6, 0, -10, 0)
    m.scale(1.4)
    return m


# ===========================================================================
# ENGENDRO DEL VACIO (HUSK)
# ===========================================================================
def build_spawn():
    m = _model("az_spawn", 1112)
    face_t = []

    def head(m, hd):
        m.cube(hd, "skull", (-3.4, 25.0, -3.2), (3.4, 31.4, 3.4), "flesh", decor={"north": "many_eyes", "all": "veins"})
        m.cube(hd, "dome", (-2.8, 30.8, -2.6), (2.8, 33.0, 3.4), "flesh_dark", rot=("x", 22.5), pivot=(0, 31.4, 0), **V)
        for k, x in enumerate((-2.0, -0.7, 0.7, 2.0)):
            face_t.append(tentacle(m, hd, f"ft{k}_", (x * 1.1, 26.2, -3.9), n=4, L=2.4, w0=0.8, mats=("flesh", "nebula"),
                                    tip="glow"))

    H = AN.humanoid(m, k=1.05, mats={"skin": "void", "chest": "flesh_dark", "belly": "void", "arm": "flesh_dark",
                                      "hand": "flesh", "thigh": "void", "shin": "flesh_dark", "foot": "void"}, head=head)
    for c in m.CUBES:
        if c.mat in ("void",) and not c.decor:
            c.decor["all"] = "cosmic"
    torso = H["torso"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    for i, (x, y) in enumerate(((-2.2, 22.0), (2.0, 20.0), (0, 17.6))):
        e = m.bone(f"chest_eye{i}", (x, y, -3.2), torso)
        m.cube(e, f"chest_eye{i}", (x - 0.9, y - 0.8, -3.6), (x + 0.9, y + 0.8, -2.9), "eye", decor={"all": "eye"})
    for k, sx in enumerate((1, -1)):
        tb = m.bone(f"back_t{k}", (2.2 * sx, 22.0, 3.4), torso, rotation=(40, 0, -25 * sx))
        face_t.append(tentacle(m, tb, f"bt{k}_", (2.2 * sx, 22.0, 3.4), n=5, L=3.0, w0=1.1, up=True,
                               mats=("flesh", "nebula")))
    for side, sx, arm in (("r", 1, AR), ("l", -1, AL)):
        for k, z in enumerate((-1.0, 0.0, 1.0)):
            m.cube(arm[2], f"claw_{side}{k}", (6.5 * sx - 0.3, 6.6, z - 0.3), (6.5 * sx + 0.3, 9.0, z + 0.3), "glow",
                   rot=("x", -22.5), pivot=(6.5 * sx, 9, z))
    m.ZERO_BONES += sum(face_t, [])
    hunch = lambda a, t, s: (a.rot("torso", t, 22, 0, 0), a.rot("h_head", t, -15, 4 * s - 2, 0),  # noqa: E731
                             [wave(a, bs, 2.4, 10, "x", k) for k, bs in enumerate(face_t)] if t == 0 else None)
    GM.human_idle(m, arm_r=(-20, 0, 12), arm_l=(-20, 0, -12), extra=hunch)
    GM.human_walk(m, leg=24, arm=20, lean=20, extra=lambda a, t, s: a.rot("h_head", t, -15, 0, 0))
    a = m.anim("attack", 0.7, "once")
    a.rest(0)
    a.pose(0.15, {"right_arm": (-140, 0, 30), "left_arm": (-140, 0, -30), "torso": (-5, 0, 0)})
    a.pose(0.3, {"right_arm": (-60, 0, -10), "left_arm": (-60, 0, 10), "torso": (30, 0, 0)}, i="linear")
    a.rest(0.7)
    GM.human_hurt(m)
    GM.human_spawn(m, {"right_arm": (-60, 0, 60), "left_arm": (-60, 0, -60), "h_head": (-30, 0, 0)})
    GM.human_death(m)
    return m


# ===========================================================================
# FLAUTISTA DEMENTE (HUSK)
# ===========================================================================
def build_piper():
    m = _model("az_piper", 1113)

    def head(m, hd):
        m.cube(hd, "mask", (-3.0, 25.2, -3.6), (3.0, 31.0, -2.8), "mask", decor={"north": "spiral"})
        m.cube(hd, "head", (-2.8, 25.0, -2.8), (2.8, 30.8, 2.8), "robe_dark")
        m.cube(hd, "hood", (-3.6, 24.4, -2.6), (3.6, 31.6, 3.8), "robe", decor={"all": "robe"})
        m.cube_lr(hd, hd, "hood_side", (2.8, 24.2, -3.4), (3.8, 31.0, 3.2), "robe", rot=("z", -22.5), pivot=(3.3, 31, 0))
        m.cube(hd, "hood_tip", (-1.4, 30.4, 2.0), (1.4, 32.4, 7.0), "robe", rot=("x", -22.5), pivot=(0, 31.4, 2.6))
        m.cube(hd, "bell", (-0.6, 30.6, 6.2), (0.6, 31.8, 7.4), "gold")

    H = AN.humanoid(m, k=0.85, mats={"skin": "skin", "chest": "robe", "belly": "robe", "arm": "robe", "hand": "skin",
                                      "thigh": "robe_dark", "shin": "robe_dark", "foot": "bone", "pelvis": "robe"}, head=head)
    waist, torso = H["waist"], H["torso"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    m.cube(waist, "robe_skirt", (-4.6, 2.0, -3.2), (4.6, 13.4, 3.2), "robe", decor={"all": "robe"})
    m.cube_lr(waist, waist, "robe_flare", (4.0, 1.4, -3.0), (4.8, 9.0, 3.0), "robe", rot=("z", 22.5), pivot=(4.4, 9, 0))
    m.cube(torso, "sash", (-4.0, 15.0, -3.0), (4.0, 16.4, 2.8), "gold")
    for i, (x, y) in enumerate(((-3.6, 17.6), (3.4, 18.4))):
        m.cube(torso, f"rag{i}", (x - 0.6, y - 5, -2.9), (x + 0.6, y, -2.4), "robe_dark", rot=("z", 22.5 if i else -22.5),
               pivot=(x, y, -2.6))
    fl = m.bone("flute", (6.5, 10.0, 0), AR[2])
    m.cube(fl, "flute", (6.0, 9.5, -12.0), (7.0, 10.5, 1.0), "bone")
    for i, z in enumerate((-10.0, -7.5, -5.0, -2.5)):
        m.cube(fl, f"hole{i}", (6.1, 10.4, z), (6.9, 10.7, z + 0.8), "void_dark")
    m.cube(fl, "flute_bell", (5.6, 9.1, -13.6), (7.4, 10.9, -12.0), "gold")
    m.ZERO_BONES += ["flute"]
    play = {"right_arm": (-80, -35, 0), "left_arm": (-80, 35, 0), "flute": (0, -50, 0), "h_head": (8, 0, 0)}
    GM.human_idle(m, arm_r=(-15, 0, 6), extra=lambda a, t, s: (a.rot("flute", t, 50, 0, 0), a.rot("h_head", t, 4 * s, 0, 8 * s - 4)))
    GM.human_walk(m, leg=20, arm=10, arm_r=(-20, 0, 6), extra=lambda a, t, s: a.rot("flute", t, 50, 0, 0))
    a = m.anim("attack", 1.2, "once")
    a.rest(0)
    a.pose(0.2, play)
    for k, t in enumerate((0.4, 0.6, 0.8)):
        a.pose(t, {**play, "torso": (0, 0, 6 if k % 2 else -6), "h_head": (8, 0, -10 if k % 2 else 10)})
    a.rest(1.2)
    GM.human_hurt(m)
    GM.human_spawn(m, play)
    GM.human_death(m)
    return m


# ===========================================================================
# LARVA ESTELAR (SPIDER)
# ===========================================================================
def build_larva():
    m = _model("az_larva", 1114)
    root = m.root
    hb = m.bone("hitbox", (0, 4, 0), root)
    m.cube(hb, "hitbox", (-7, 0, -8), (7, 9, 8), "hitbox")
    m.bone("tag_name", (0, 14, 0), root)
    body = m.bone("body", (0, 5, 0), root)
    S = {"decor": {"all": "star_spots"}}
    segs = []
    prev = body
    for i, (z, w, h) in enumerate(((-6.0, 4.4, 6.6), (-1.0, 5.4, 7.6), (4.4, 4.8, 6.8), (9.0, 3.6, 5.2), (12.6, 2.4, 3.8))):
        b = m.bone(f"seg{i}", (0, 4.0, z - 2.5), prev)
        m.cube(b, f"seg{i}", (-w, 0.8, z - 2.6), (w, 0.8 + h, z + 2.6), "chitin", **S)
        m.cube(b, f"seg{i}_45", (-w * 0.8, 1.2, z - 2.3), (w * 0.8, 0.8 + h * 1.08, z + 2.3), "void", rot=("z", 45),
               pivot=(0, 0.8 + h / 2, z), **C)
        m.cube(b, f"seg{i}_ridge", (-0.5, 0.6 + h, z - 1.8), (0.5, 1.8 + h, z + 1.8), "glow")
        segs.append(f"seg{i}")
        prev = b
    hd = m.bone("head", (0, 4.0, -8.5), body)
    m.cube(hd, "head", (-3.6, 1.0, -12.6), (3.6, 6.6, -8.0), "chitin", decor={"north": "many_eyes"})
    for sx in (1, -1):
        mb = m.bone(f"mandible{sx}", (2.4 * sx, 2.2, -12.4), hd)
        m.cube(mb, f"mandible{sx}", (2.4 * sx - 0.6, 1.4, -16.0), (2.4 * sx + 0.6, 2.8, -12.0), "teeth",
               rot=("y", 22.5 * sx), pivot=(2.4 * sx, 2.2, -12.4))
    legs = []
    for i, z in enumerate((-6.0, -1.0, 4.4)):
        for sx in (1, -1):
            n = f"leg{i}{'r' if sx > 0 else 'l'}"
            lg = m.bone(n, (4.4 * sx, 3.0, z), body)
            m.cube(lg, n, (min(4.4 * sx, 9.4 * sx), 2.6, z - 0.6), (max(4.4 * sx, 9.4 * sx), 3.6, z + 0.6), "chitin",
                   rot=("z", -22.5 * sx), pivot=(4.4 * sx, 3.0, z))
            m.cube(lg, n + "_low", (min(9.0 * sx, 9.6 * sx) - 0.6, 0, z - 0.5), (max(9.0 * sx, 9.6 * sx) + 0.6, 3.0, z + 0.5),
                   "flesh_dark")
            legs.append((n, sx, i))
    m.ZERO_BONES = ["body", "head", "mandible1", "mandible-1"] + segs + [n for n, _, _ in legs]
    a = m.anim("idle", 1.6, "loop")
    for k in range(5):
        t = 1.6 * k / 4
        for i, sname in enumerate(segs[1:]):
            a.rot(sname, t, 0, 6 * math.sin(2 * math.pi * k / 4 + i), 0)
        a.rot("mandible1", t, 0, 10 * (k % 2), 0)
        a.rot("mandible-1", t, 0, -10 * (k % 2), 0)
    a = m.anim("walk", 0.6, "loop")
    for k in range(5):
        t = 0.6 * k / 4
        s = math.sin(2 * math.pi * k / 4)
        for i, sname in enumerate(segs[1:]):
            a.rot(sname, t, 0, 12 * math.sin(2 * math.pi * k / 4 + i), 0)
        for n, sx, i in legs:
            a.rot(n, t, 0, 25 * s * (1 if (i % 2 == 0) == (sx > 0) else -1), 0)
    a = m.anim("attack", 0.6, "once")
    a.rest(0)
    a.pose(0.15, {"head": (-25, 0, 0), "mandible1": (0, 35, 0), "mandible-1": (0, -35, 0), "body": {"p": (0, 0, 2)}})
    a.pose(0.3, {"head": (15, 0, 0), "mandible1": (0, -10, 0), "mandible-1": (0, 10, 0), "body": {"p": (0, 0, -3)}}, i="linear")
    a.rest(0.6)
    a = m.anim("hurt", 0.3, "once")
    a.rest(0, ["head"])
    a.pose(0.08, {"head": (-20, 15, 0)})
    a.rest(0.3, ["head"])
    a = m.anim("spawn", 1.0, "once")
    a.pos("body", 0, 0, -10, 0)
    a.pos("body", 0.8, 0, 0, 0)
    a.rest(1.0)
    a = m.anim("death", 1.2, "hold")
    a.rest(0)
    a.rot("root", 0.6, 0, 0, 0)
    a.rot("root", 1.0, 0, 0, 170, i="linear")
    a.rot("root", 1.2, 0, 0, 175)
    a.pos("root", 1.0, 0, 6, 0)
    return m


# ===========================================================================
# SACERDOTE DEL CAOS (STRAY)
# ===========================================================================
def build_priest():
    m = _model("az_priest", 1115)

    def head(m, hd):
        AN.default_head(m, hd, face="priest_skull", mat="bone")
        m.cube(hd, "veil", (-3.4, 24.6, -3.2), (3.4, 27.6, -2.8), "robe_dark")
        m.cube(hd, "mitre", (-3.0, 30.4, -2.6), (3.0, 35.0, 2.6), "robe", decor={"all": "robe"})
        m.cube_lr(hd, hd, "mitre_side", (1.8, 32.0, -2.4), (2.8, 38.0, 2.4), "robe", rot=("z", 22.5), pivot=(2.3, 35, 0))
        m.cube(hd, "mitre_eye", (-1.2, 32.0, -2.9), (1.2, 34.4, -2.5), "eye", decor={"all": "eye"})
        m.cube(hd, "mitre_trim", (-3.2, 30.2, -2.8), (3.2, 31.0, 2.8), "gold")

    H = AN.humanoid(m, k=0.9, mats={"skin": "bone", "chest": "robe", "belly": "robe", "arm": "robe", "hand": "bone",
                                     "thigh": "robe_dark", "shin": "robe_dark", "foot": "bone", "pelvis": "robe"}, head=head)
    waist, torso = H["waist"], H["torso"]
    (AR, AL) = H["arms"]["right"], H["arms"]["left"]
    m.cube(waist, "robe_skirt", (-5.0, 0.4, -3.4), (5.0, 13.4, 3.4), "robe", decor={"all": "robe"})
    m.cube_lr(waist, waist, "robe_flare", (4.4, 0.2, -3.2), (5.4, 8.6, 3.2), "robe_dark", rot=("z", 22.5), pivot=(4.9, 8.6, 0))
    m.cube(m.BONES["skirt_front"], "stole", (-1.6, 1.0, -3.9), (1.6, 23.6, -3.3), "nebula", decor={"all": "robe"})
    m.cube(torso, "collar", (-4.6, 22.4, -3.2), (4.6, 24.6, 3.0), "gold", rot=("x", -22.5), pivot=(0, 23.5, 0))
    st = m.bone("staff", (6.5, 10.0, 0), AR[2])
    m.cube(st, "shaft", (6.1, 9.6, -20.0), (6.9, 10.4, 8.0), "void_dark")
    m.cube_lr(st, st, "prong", (6.8, 9.2, -24.0), (7.6, 10.8, -19.0), "gold", rot=("y", 22.5), pivot=(7.2, 10, -19.6))
    m.cube(st, "staff_eye", (5.2, 8.7, -23.6), (7.8, 11.3, -21.0), "eye", rot=("x", 45), pivot=(6.5, 10, -22.3),
           decor={"all": "eye"})
    m.ZERO_BONES += ["staff"]
    GM.human_idle(m, arm_r=(-25, 0, 8), extra=lambda a, t, s: a.rot("staff", t, -60, 0, 0))
    GM.human_walk(m, leg=18, arm=10, arm_r=(-30, 0, 8), extra=lambda a, t, s: a.rot("staff", t, -60, 0, 0))
    heal = {"right_arm": (-170, 0, 10), "staff": (-90, 0, 0), "left_arm": (-100, 0, -40), "h_head": (-25, 0, 0)}
    a = m.anim("attack", 1.2, "once")
    a.rest(0)
    a.pose(0.3, heal)
    a.pose(0.9, heal)
    a.rest(1.2)
    GM.human_hurt(m)
    GM.human_spawn(m, heal)
    GM.human_death(m)
    return m


BUILDERS = {"azathoth": build_azathoth, "az_spawn": build_spawn, "az_piper": build_piper, "az_larva": build_larva,
            "az_priest": build_priest}
SHOTS = {
    "azathoth": [("idle", 0.6, -30), ("rest", 0, 150), ("gaze", 0.5, -20), ("rift", 1.0, -30)],
    "az_spawn": [("idle", 0.5, -30), ("rest", 0, 150), ("attack", 0.15, -60), ("walk", 0.25, -70)],
    "az_piper": [("idle", 0.5, -30), ("rest", 0, 150), ("attack", 0.5, -60), ("walk", 0.25, -70)],
    "az_larva": [("idle", 0.5, -40), ("rest", 0, 140), ("attack", 0.15, -70), ("walk", 0.15, -90)],
    "az_priest": [("idle", 0.5, -30), ("rest", 0, 150), ("attack", 0.5, -40), ("walk", 0.25, -70)],
}
VIEW = {"azathoth": (34, 3.6), "az_larva": (6, 8.0)}
ACTIONS = [("attack", 0.35, -40), ("teleport", 0.3, -30), ("pulse", 0.3, -30), ("collapse", 0.6, -40),
           ("gaze", 0.5, -20), ("storm", 0.8, -30), ("warp", 0.4, -40), ("phase_change", 1.2, -30)]


def previews(name, m):
    import render_preview as RP
    from PIL import Image, ImageDraw
    RP.G = m
    tw, th = m.pack()
    tex = m.paint(tw, th)
    anims = {a.name: a for a in m.ANIMS}
    focus, scale = VIEW.get(name, (18, 8.5))
    frames = []
    for an, t, yaw in SHOTS[name]:
        im = RP.render(tex, anims.get(an), t, yaw=yaw, size=(340, 420), focus=focus, scale=scale)
        ImageDraw.Draw(im).text((8, 8), f"{name}  {an} {t:g}s", fill=(230, 230, 230))
        frames.append(im)
    sheet = Image.new("RGB", (340 * len(frames), 420))
    for i, f in enumerate(frames):
        sheet.paste(f, (i * 340, 0))
    PREVIEW.mkdir(parents=True, exist_ok=True)
    sheet.save(PREVIEW / f"{name}.png")


def main():
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    for name, fn in BUILDERS.items():
        if only and name not in only:
            continue
        m = fn()
        out = BLUEPRINTS / name / f"{name}.bbmodel"
        out.parent.mkdir(parents=True, exist_ok=True)
        m.build(out)
        print(f"OK {name}: cubos={len(m.CUBES)} huesos={len(m.BONES)} anims={[a.name for a in m.ANIMS]}")
        if "--no-preview" not in sys.argv:
            previews(name, m)
            if name == "azathoth":
                FX.action_sheet(m, ACTIONS, PREVIEW / "azathoth_acciones.png", focus=34, scale=3.6)


if __name__ == "__main__":
    main()
