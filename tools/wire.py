#!/usr/bin/env python3
"""
Ayudas para conectar un boss en MythicMobs-3D (modelos, sonidos, efectos y titulo) editando sus .yml
sin cambiar el fin de linea (CRLF o LF) que ya tenian.

    y = wire.Yml("MythicMobs-3D/Skills/xxx.yml")
    y.rep(viejo, nuevo)          # sustitucion exacta que debe aparecer UNA vez
    y.save()
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import dextra_pack as DP  # noqa: E402

REPO = Path(__file__).resolve().parent.parent


class Yml:
    def __init__(self, rel):
        self.path = REPO / rel
        raw = self.path.read_text(encoding="utf-8")
        raw = open(self.path, newline="", encoding="utf-8").read()
        self.crlf = "\r\n" in raw
        self.s = raw.replace("\r\n", "\n")

    def rep(self, old, new, count=1):
        n = self.s.count(old)
        assert n == count, f"{self.path.name}: se esperaban {count} y hay {n}:\n{old[:200]}"
        self.s = self.s.replace(old, new)

    def append(self, text):
        self.s = self.s.rstrip("\n") + "\n" + text

    def save(self):
        out = self.s.replace("\n", "\r\n") if self.crlf else self.s
        open(self.path, "w", newline="", encoding="utf-8").write(out)
        import yaml
        yaml.safe_load(self.path.read_text(encoding="utf-8"))


def header(boss_id, name):
    return f"""#
# Version 3D (ModelEngine + DextraBossesPack):
#  - state{{mid={boss_id};...}} lanza la animacion; los "delay" coinciden con el golpe de cada una.
#  - Sonidos "dextra:{boss_id}.*" = sonidos propios del pack, siempre junto al vanilla de antes.
#  - summon{{type=..._FX_...}} = efectos 3D de cada ataque (mobs invisibles que se borran solos).
#  - El titulo de aparicion se manda con /title y un texto traducible: sin pack se ve
#    "{name}" como siempre; con pack se ve el logo.
"""


def title_lines(boss_id, fallback, subtitle, times="20 300 20"):
    comp = DP.title_component(boss_id, fallback)
    return (f"""    - 'command{{c="minecraft:title @a times {times}"}} @self'
    - 'command{{c="minecraft:title @a subtitle <&lc>text:''{subtitle}''<&rc>"}} @self'
    - 'command{{c="minecraft:title @a title {comp}"}} @self'
""")


def fx_mobs(prefix, remove_skill, items, skills_file):
    s = f"""
# --- Efectos de los ataques (solo version 3D) ---
# Mobs invisibles que llevan un modelo de ModelEngine con su animacion "play" y se borran solos.
# Se invocan desde {skills_file} con summon{{type={prefix}_FX_...}}.
"""
    for n, mid, ticks in items:
        s += f"""
{prefix}_FX_{n}:
  Type: ARMOR_STAND
  Display: " "
  Health: 1
  Options:
    Invisible: true
    Invincible: true
    Marker: true
    HasGravity: false
    Silent: true
    Despawn: true
    PreventOtherDrops: true
    Collidable: false
  Skills:
    - model{{mid={mid};hitbox=false}} @self ~onSpawn
    - state{{mid={mid};s=play;li=0;lo=0}} @self ~onSpawn
    - skill{{s={remove_skill};delay={ticks}}} @self ~onSpawn
"""
    return s


class Lines:
    """Generadores de lineas para un boss."""

    def __init__(self, boss_id, fx_prefix):
        self.id = boss_id
        self.fx_prefix = fx_prefix

    def S(self, n, v=1, p=1):
        return f"    - effect:sound{{s=dextra:{self.id}.{n};v={v};p={p}}} @self"

    def ST(self, st, li=2, lo=3, mid=None):
        return f"    - state{{mid={mid or self.id};s={st};li={li};lo={lo}}} @self"

    def FX(self, n, target="@selflocation"):
        return f"    - summon{{type={self.fx_prefix}_FX_{n};amount=1;radius=0;noise=0}} {target}"
