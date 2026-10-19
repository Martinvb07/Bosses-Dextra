#!/usr/bin/env python3
"""
Cuerpo humanoide detallado para los modelos de ModelEngine (bosses 02 en adelante).

Usa los mismos huesos y pivotes que generate_minions.humanoid (asi sirven
human_idle, human_walk, human_spawn, ...), pero con una silueta menos cuadrada:
musculos que se estrechan, rodillas, codos, pies con puntera, manos con pulgar,
cuello, trapecios inclinados y cabeza con mandibula, cejas, nariz y orejas.

    H = anatomy.humanoid(m, k=1.0, mats={...}, head=None)

k    grosor del cuerpo (0.85 delgado, 1.0 normal, 1.25 corpulento)
mats materiales por zona: skin, chest, belly, arm, hand, thigh, shin, foot, pelvis
head funcion head(m, bone) que dibuja la cabeza; si es None se dibuja la cabeza
     humana por defecto (decoracion "face2" en la cara)
"""
import generate_minions as GM


def _lim(cx, k, x0, x1):
    """Escala un tramo X alrededor del centro cx del miembro."""
    return cx + (x0 - cx) * k, cx + (x1 - cx) * k


def humanoid(m, k=1.0, mats=None, head=None, face="face2"):
    M = {"skin": "skin"}
    M.update(mats or {})
    for part in ("chest", "belly", "arm", "hand", "thigh", "shin", "foot", "pelvis", "neck"):
        M.setdefault(part, M["skin"])
    root = m.root
    hb = m.bone("hitbox", (0, 28, 0), root)
    m.cube(hb, "hitbox", (-5, 0, -5), (5, 34, 5), "hitbox")
    m.bone("tag_name", (0, 40, 0), root)

    # ---------------------------------------------------------------- piernas
    legs = {}
    for side, sx in (("right", 1), ("left", -1)):
        leg = m.bone(f"{side}_leg", (2.5 * sx, 14, 0), root)
        lower = m.bone(f"{side}_lower_leg", (2.5 * sx, 7.5, 0), leg)
        legs[side] = (leg, lower)
    R, L = legs["right"], legs["left"]

    def leg_cube(b, name, x0, y0, z0, x1, y1, z1, mat, **kw):
        a, c = _lim(2.5, k, x0, x1)
        m.cube_lr(b[0], b[1], name, (a, y0, z0 * k), (c, y1, z1 * k), mat, **kw)

    leg_cube((R[0], L[0]), "hip", 0.4, 11, -2.1, 4.6, 14.2, 2.1, M["thigh"])
    leg_cube((R[0], L[0]), "thigh", 0.7, 8, -1.8, 4.3, 11, 1.9, M["thigh"])
    leg_cube((R[0], L[0]), "knee", 1.1, 6.9, -2.1, 3.9, 8.6, 1.4, M["thigh"])
    leg_cube((R[1], L[1]), "calf", 0.9, 3.8, -1.5, 4.1, 7.2, 2.0, M["shin"])
    leg_cube((R[1], L[1]), "ankle", 1.2, 1.1, -1.25, 3.8, 3.8, 1.35, M["shin"])
    leg_cube((R[1], L[1]), "foot", 0.9, 0, -2.6, 4.1, 1.3, 1.6, M["foot"])
    leg_cube((R[1], L[1]), "toes", 1.1, 0, -3.8, 3.9, 0.9, -2.6, M["foot"])

    # ---------------------------------------------------------------- cadera y faldas
    body = m.bone("body", (0, 14, 0), root)
    waist = m.bone("waist", (0, 14, 0), body)
    m.cube(waist, "pelvis", (-4.4 * k, 12.8, -2.5 * k), (4.4 * k, 15.4, 2.5 * k), M["pelvis"])
    m.bone("skirt_front", (0, 13.5, -2.6 * k), waist)
    m.bone("skirt_back", (0, 13.5, 2.6 * k), waist)

    # ---------------------------------------------------------------- torso
    torso = m.bone("torso", (0, 15, 0), body)
    m.cube(torso, "belly", (-3.6 * k, 15, -2.3 * k), (3.6 * k, 18.6, 2.2 * k), M["belly"])
    m.cube(torso, "ribs", (-4.2 * k, 18.4, -2.6 * k), (4.2 * k, 21, 2.5 * k), M["chest"])
    m.cube(torso, "chest", (-4.8 * k, 20.6, -2.9 * k), (4.8 * k, 23.6, 2.7 * k), M["chest"])
    m.cube(torso, "pecs", (-3.9 * k, 20.2, -3.2 * k), (3.9 * k, 22.8, -2.6 * k), M["chest"])
    m.cube(torso, "back", (-3.8 * k, 18.6, 2.3 * k), (3.8 * k, 23.2, 3.0 * k), M["chest"])
    m.cube_lr(torso, torso, "trapezius", (0.6, 23.0, -1.6 * k), (4.6 * k, 24.0, 2.0 * k), M["chest"],
              rot=("z", -22.5), pivot=(0.6, 23.5, 0))
    m.cube(torso, "neck", (-1.4, 23.4, -1.3), (1.4, 25.6, 1.4), M["neck"])

    hd = m.bone("h_head", (0, 24.5, 0), torso)
    if head:
        head(m, hd)
    else:
        default_head(m, hd, face=face)

    # ---------------------------------------------------------------- brazos
    arms = {}
    for side, sx in (("right", 1), ("left", -1)):
        arm = m.bone(f"{side}_arm", (6.5 * sx, 23, 0), torso)
        fore = m.bone(f"{side}_forearm", (6.5 * sx, 17.5, 0), arm)
        hand = m.bone(f"{side}_hand", (6.5 * sx, 11.5, 0), fore)
        arms[side] = (arm, fore, hand)
    AR, AL = arms["right"], arms["left"]

    def arm_cube(i, name, x0, y0, z0, x1, y1, z1, mat, **kw):
        a, c = _lim(6.5, k, x0, x1)
        m.cube_lr(AR[i], AL[i], name, (a, y0, z0 * k), (c, y1, z1 * k), mat, **kw)

    arm_cube(0, "deltoid", 4.8, 21.2, -2.0, 8.3, 24.4, 2.0, M["arm"])
    arm_cube(0, "biceps", 5.2, 17.6, -1.6, 7.9, 21.4, 1.6, M["arm"])
    arm_cube(1, "elbow", 5.4, 16.4, -1.4, 7.7, 18.0, 1.7, M["arm"])
    arm_cube(1, "forearm", 5.2, 14.2, -1.6, 7.9, 16.6, 1.5, M["arm"])
    arm_cube(1, "wrist", 5.6, 11.5, -1.25, 7.5, 14.4, 1.25, M["arm"])
    arm_cube(2, "palm", 5.5, 9.6, -1.35, 7.6, 11.6, 1.3, M["hand"])
    arm_cube(2, "fingers", 5.7, 8.3, -1.3, 7.4, 9.7, 0.7, M["hand"])
    arm_cube(2, "thumb", 5.0, 9.6, -1.7, 5.8, 11.0, -0.6, M["hand"])

    m.ZERO_BONES = list(GM.HUMAN_BONES)
    return dict(body=body, torso=torso, head=hd, arms=arms, legs=legs, waist=waist)


def default_head(m, hd, face="face2", mat="skin", k=1.0):
    m.cube(hd, "skull", (-3.5 * k, 25.4, -3.4), (3.5 * k, 32.2, 3.6), mat, decor={"north": face})
    m.cube(hd, "jaw", (-2.9 * k, 24.6, -3.7), (2.9 * k, 26.4, 1.6), mat)
    m.cube(hd, "brow", (-3.3 * k, 29.0, -3.9), (3.3 * k, 29.8, -3.3), mat)
    m.cube(hd, "nose", (-0.5, 27.2, -4.3), (0.5, 29.0, -3.4), mat)
    m.cube(hd, "ear_r", (3.4 * k, 27.4, -0.4), (3.9 * k, 29.6, 1.0), mat)
    m.cube(hd, "ear_l", (-3.9 * k, 27.4, -0.4), (-3.4 * k, 29.6, 1.0), mat)
