#!/usr/bin/env python3
"""
Libreria comun para generar blueprints de ModelEngine (.bbmodel) por codigo.

Es lo mismo que usa generate_heracles.py (huesos, cubos, atlas UV, textura
pintada proceduralmente, animaciones y serializacion), pero empaquetado en una
clase Model para poder generar varios modelos en el mismo script.

Un Model expone los mismos nombres que generate_heracles.py (root, CUBES,
ANIMS, PX, Bone, pack(), paint()) para que render_preview.py sirva para todos.
"""
import base64
import io
import json
import random
import uuid as uuidlib
from pathlib import Path

from PIL import Image


def clamp(v):
    return max(0, min(255, int(v)))


def mul(c, f):
    return tuple(clamp(x * f) for x in c)


def mix(a, b, t):
    return tuple(clamp(a[i] * (1 - t) + b[i] * t) for i in range(3))


def fmt(v):
    v = round(float(v), 3)
    return str(int(v)) if v == int(v) else str(v)


class Bone:
    def __init__(self, model, name, origin, parent=None, rotation=(0, 0, 0)):
        self.name = name
        self.origin = list(origin)
        self.rotation = list(rotation)
        self.uuid = model.uid()
        self.children = []   # Bone o Cube, en orden
        self.parent = parent
        if parent:
            parent.children.append(self)


class Cube:
    def __init__(self, model, bone, name, frm, to, mat, decor=None, inflate=0, rot=None, pivot=None):
        self.bone = bone
        # rot=(eje, grados) en un solo eje y multiplo de 22.5 (lo que aceptan los modelos de Minecraft)
        if rot:
            assert rot[0] in "xyz" and rot[1] % 22.5 == 0 and abs(rot[1]) <= 45, (name, rot)
        self.rot = rot
        self.pivot = list(pivot) if pivot else [(frm[i] + to[i]) / 2 for i in range(3)]
        self.name = name
        self.frm = list(frm)
        self.to = list(to)
        self.mat = mat
        self.decor = decor or {}
        self.inflate = inflate
        self.uuid = model.uid()
        self.uv = {}
        bone.children.append(self)

    @property
    def size(self):
        return [self.to[i] - self.frm[i] for i in range(3)]


class Face:
    def __init__(self, model, img, box, name, cube):
        self.model = model
        self.img = img
        self.x0, self.y0, self.x1, self.y1 = box
        self.w = self.x1 - self.x0
        self.h = self.y1 - self.y0
        self.name = name
        self.cube = cube

    @property
    def rng(self):
        return self.model.rng

    def put(self, x, y, col):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.img.putpixel((self.x0 + x, self.y0 + y), tuple(col)[:3] + (255,))

    def get(self, x, y):
        return self.img.getpixel((self.x0 + x, self.y0 + y))[:3]

    def rect(self, x0, y0, x1, y1, col):
        for yy in range(y0, y1):
            for xx in range(x0, x1):
                self.put(xx, yy, col)

    def shade(self, x, y, f):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.put(x, y, mul(self.get(x, y), f))


class Anim:
    def __init__(self, model, name, length, loop="once", snapping=20):
        self.model = model
        self.name = name
        self.length = length
        self.loop = loop
        self.snapping = snapping
        self.tracks = {}   # (bone, channel) -> {time: (x,y,z,interp)}

    def k(self, bone, channel, t, x=0, y=0, z=0, interp="catmullrom"):
        assert bone in self.model.BONES, bone
        self.tracks.setdefault((bone, channel), {})[round(t, 4)] = (x, y, z, interp)
        return self

    def rot(self, bone, t, x=0, y=0, z=0, i="catmullrom"):
        return self.k(bone, "rotation", t, x, y, z, i)

    def pos(self, bone, t, x=0, y=0, z=0, i="catmullrom"):
        return self.k(bone, "position", t, x, y, z, i)

    def pose(self, t, poses, i="catmullrom"):
        """poses: {bone: (rx,ry,rz)} o {bone: {'r':(..), 'p':(..)}}"""
        for b, v in poses.items():
            if isinstance(v, dict):
                if "r" in v:
                    self.rot(b, t, *v["r"], i=i)
                if "p" in v:
                    self.pos(b, t, *v["p"], i=i)
            else:
                self.rot(b, t, *v, i=i)
        return self

    def rest(self, t, bones=None, i="catmullrom"):
        for b in bones or self.model.ZERO_BONES:
            self.rot(b, t, 0, 0, 0, i=i)
        if bones is None:
            self.pos(self.model.BODY, t, 0, 0, 0, i=i)
        return self

    def to_json(self):
        animators = {}
        uid = self.model.uid
        for (bone, channel), kfs in self.tracks.items():
            b = self.model.BONES[bone]
            an = animators.setdefault(b.uuid, {"name": bone, "type": "bone", "keyframes": []})
            for t in sorted(kfs):
                x, y, z, interp = kfs[t]
                an["keyframes"].append({
                    "channel": channel,
                    "data_points": [{"x": fmt(x), "y": fmt(y), "z": fmt(z)}],
                    "uuid": uid(),
                    "time": t,
                    "color": -1,
                    "interpolation": interp,
                })
        return {
            "uuid": uid(), "name": self.name, "loop": self.loop, "override": False,
            "length": self.length, "snapping": self.snapping, "selected": False,
            "anim_time_update": "", "blend_weight": "", "start_delay": "", "loop_delay": "",
            "animators": animators,
        }


class Model:
    """Un blueprint. 'mats' = {material: (rgb, ruido)}; 'decor' = {nombre: fn(face)}."""
    Bone = Bone   # para render_preview.py

    def __init__(self, name, mats, seed=1337, px=2, atlas_w=128):
        self.name = name
        self.rng = random.Random(seed)
        self.PX = px
        self.ATLAS_W = atlas_w
        self.MAT = {k: v[0] for k, v in mats.items()}
        self.NOISE = {k: v[1] for k, v in mats.items()}
        self.MAT.setdefault("hitbox", (255, 255, 255))
        self.NOISE.setdefault("hitbox", 0)
        self.FUR = set()       # materiales con pelaje
        self.WOOD = set()      # materiales con veta de madera
        self.SHINE = set()     # materiales metalicos (brillo arriba)
        self.DECOR = {}
        self.CUBES = []
        self.BONES = {}
        self.ANIMS = []
        self.ZERO_BONES = []
        self.BODY = "body"
        self.root = self.bone("root", (0, 0, 0))

    # ---------------------------------------------------------------- piezas
    def uid(self):
        return str(uuidlib.UUID(int=self.rng.getrandbits(128), version=4))

    def bone(self, name, origin, parent=None, rotation=(0, 0, 0)):
        b = Bone(self, name, origin, parent, rotation)
        self.BONES[name] = b
        return b

    def cube(self, bone, name, frm, to, mat, **kw):
        assert mat in self.MAT, mat
        c = Cube(self, bone, name, frm, to, mat, **kw)
        self.CUBES.append(c)
        return c

    def cube_lr(self, bone_r, bone_l, name, frm, to, mat, **kw):
        """Cubo en el lado derecho (+X) y su espejo en el izquierdo (-X)."""
        self.cube(bone_r, "right_" + name, frm, to, mat, **kw)
        if kw.get("rot") and kw["rot"][0] in "yz":
            kw = {**kw, "rot": (kw["rot"][0], -kw["rot"][1])}
        if kw.get("pivot"):
            kw = {**kw, "pivot": [-kw["pivot"][0], kw["pivot"][1], kw["pivot"][2]]}
        self.cube(bone_l, "left_" + name, [-to[0], frm[1], frm[2]], [-frm[0], to[1], to[2]], mat, **kw)

    def decor(self, fn):
        """Decorador: registra fn como decoracion con su nombre sin 'd_'."""
        self.DECOR[fn.__name__.removeprefix("d_")] = fn
        return fn

    def anim(self, name, length, loop="once"):
        a = Anim(self, name, length, loop)
        self.ANIMS.append(a)
        return a

    # ---------------------------------------------------------------- atlas
    def pack(self):
        items = []
        for c in self.CUBES:
            if c.mat == "hitbox":
                continue
            w, h, d = c.size
            items.append((c, 2 * (d + w), d + h))
        items.sort(key=lambda t: -t[2])
        x = y = row_h = 0.0
        for c, rw, rh in items:
            if x + rw > self.ATLAS_W:
                x, y, row_h = 0.0, y + row_h, 0.0
            w, h, d = c.size
            u, v = x, y
            c.uv = {
                "east":  [u, v + d, u + d, v + d + h],
                "north": [u + d, v + d, u + d + w, v + d + h],
                "west":  [u + d + w, v + d, u + 2 * d + w, v + d + h],
                "south": [u + 2 * d + w, v + d, u + 2 * d + 2 * w, v + d + h],
                "up":    [u + d, v, u + d + w, v + d],
                "down":  [u + d + w, v, u + d + 2 * w, v + d],
            }
            x += rw
            row_h = max(row_h, rh)
        total_h = y + row_h
        # El hitbox no se renderiza: usa un pixel transparente al final del atlas.
        for c in self.CUBES:
            if c.mat == "hitbox":
                spot = [self.ATLAS_W - 1, total_h, self.ATLAS_W, total_h + 1]
                c.uv = {f: list(spot) for f in ("north", "east", "south", "west", "up", "down")}
        total_h += 1
        hh = 16
        while hh < total_h:
            hh *= 2
        return self.ATLAS_W, hh

    # ---------------------------------------------------------------- textura
    def base_fill(self, f, mat):
        col, noise = self.MAT[mat], self.NOISE[mat]
        light = {"up": 1.12, "down": 0.72, "north": 1.0, "south": 0.9, "east": 0.95, "west": 0.95}[f.name]
        for y in range(f.h):
            for x in range(f.w):
                n = self.rng.uniform(-noise, noise)
                g = 1.0
                if f.name not in ("up", "down") and f.h > 2:
                    g = 1.06 - 0.14 * (y / (f.h - 1))
                f.put(x, y, tuple(clamp((v + n) * light * g) for v in col))
        if mat in self.SHINE:
            for x in range(f.w):
                f.put(x, 0, mix(f.get(x, 0), (255, 240, 190), 0.55))
                f.put(x, f.h - 1, mul(f.get(x, f.h - 1), 0.7))
        if mat in self.FUR:
            for x in range(f.w):
                start = self.rng.randint(0, 3)
                for y in range(start, f.h, self.rng.randint(3, 5)):
                    f.shade(x, y, self.rng.choice((0.8, 0.86, 1.12)))
                    f.shade(x, y + 1, 0.9)
        if mat in self.WOOD:
            for x in range(f.w):
                if x % 3 == 1:
                    for y in range(f.h):
                        f.shade(x, y, 0.84)
        k = 0.82
        for x in range(f.w):
            f.shade(x, 0, k + 0.08)
            f.shade(x, f.h - 1, k)
        for y in range(1, f.h - 1):
            f.shade(0, y, k + 0.05)
            f.shade(f.w - 1, y, k + 0.05)

    def paint(self, tex_w, tex_h):
        img = Image.new("RGBA", (tex_w * self.PX, tex_h * self.PX), (0, 0, 0, 0))
        for c in self.CUBES:
            if c.mat == "hitbox":
                continue
            for face, (u0, v0, u1, v1) in c.uv.items():
                box = (round(u0 * self.PX), round(v0 * self.PX), round(u1 * self.PX), round(v1 * self.PX))
                if box[2] - box[0] <= 0 or box[3] - box[1] <= 0:
                    continue
                f = Face(self, img, box, face, c)
                self.base_fill(f, c.mat)
                for key in ("all", face):
                    name = c.decor.get(key)
                    if name:
                        assert name in self.DECOR, f"{self.name}: decoracion '{name}' no existe"
                        self.DECOR[name](f)
        return img

    # ---------------------------------------------------------------- .bbmodel
    def _outliner(self, b):
        return {
            "name": b.name, "origin": b.origin, "rotation": b.rotation, "color": 0,
            "uuid": b.uuid, "export": True, "mirror_uv": False,
            "isOpen": b.name in ("root", "body", "torso"), "locked": False,
            "visibility": True, "autouv": 0,
            "children": [self._outliner(c) if isinstance(c, Bone) else c.uuid for c in b.children],
        }

    @staticmethod
    def _element(c):
        faces = {}
        for f in ("north", "east", "south", "west", "up", "down"):
            u0, v0, u1, v1 = c.uv[f]
            if f == "down":
                u0, v0, u1, v1 = u0, v1, u1, v0  # convencion de Blockbench para la cara inferior
            faces[f] = {"uv": [u0, v0, u1, v1], "texture": 0}
        return {
            "name": c.name, "box_uv": False, "rescale": False, "locked": False,
            "light_emission": 0, "render_order": "default", "allow_mirror_modeling": True,
            "from": c.frm, "to": c.to, "autouv": 0, "color": 0, "inflate": c.inflate,
            "origin": c.pivot if c.rot else c.bone.origin, "faces": faces, "type": "cube", "uuid": c.uuid,
            **({"rotation": [c.rot[1] if a == c.rot[0] else 0 for a in "xyz"]} if c.rot else {}),
        }

    def build(self, out_path):
        tw, th = self.pack()
        img = self.paint(tw, th)
        buf = io.BytesIO()
        img.save(buf, "PNG")
        model = {
            "meta": {"format_version": "4.10", "model_format": "free", "box_uv": False},
            "name": self.name,
            "model_identifier": "",
            "visible_box": [2, 3, 1.4],
            "variable_placeholders": "",
            "variable_placeholder_buttons": [],
            "timeline_setups": [],
            "unhandled_root_fields": {},
            "resolution": {"width": tw, "height": th},
            "elements": [self._element(c) for c in self.CUBES],
            "outliner": [self._outliner(self.root)],
            "textures": [{
                "path": "", "name": f"{self.name}.png", "folder": "", "namespace": "",
                "id": "0", "group": "", "width": tw * self.PX, "height": th * self.PX,
                "uv_width": tw, "uv_height": th, "particle": False, "use_as_default": False,
                "layers_enabled": False, "sync_to_project": "", "render_mode": "default",
                "render_sides": "auto", "frame_time": 1, "frame_order_type": "loop",
                "frame_order": "", "frame_interpolate": False, "visible": True,
                "internal": True, "saved": True, "uuid": self.uid(), "relative_path": "",
                "source": "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(),
            }],
            "animations": [an.to_json() for an in self.ANIMS],
        }
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(model, fh, indent=1, ensure_ascii=False)
        img.save(out_path.with_name(f"{self.name}_texture.png"))
        return model, img
