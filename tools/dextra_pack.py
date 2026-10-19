#!/usr/bin/env python3
"""
Pack compartido de los bosses 02-17 (todo lo que no es de ModelEngine).

  Modelos/DextraBossesPack/                 -> plugins/DextraBossesPack/ (en la lista
                                               merge_other_plugins_resourcepacks_folders)
    assets/dextra/sounds.json               sonidos  dextra:<boss>.<nombre>
    assets/dextra/sounds/<boss>/*.ogg
    assets/dextra/font/hud.json             fuente dextra:hud (adornos de los titulos)
    assets/dextra/textures/font/<boss>/*.png
    assets/dextra/lang/en_us.json           textos traducibles de los titulos
    assets/minecraft/textures/gui/sprites/boss_bar/<color>_*.png
  Modelos/ItemsAdder/contents/dextra_bosses/ -> plugins/ItemsAdder/contents/dextra_bosses/
    <boss>.yml + textures/font/<boss>/bossbar.png   marco de la bossbar

Funciona CON y SIN el pack:

  Bossbar: "&f<C>&5&lOLD ENDER&f<C>"  donde <C> es un espacio unicode distinto por boss
           (BOSSBAR_CHAR). Sin pack es un espacio en blanco a cada lado; con pack,
           ItemsAdder lo convierte en media moldura (la misma imagen a los dos lados,
           por eso cada media moldura es simetrica).
  Titulo:  se manda con /title y un texto traducible:
           {translate:'dextra.title.<boss>',fallback:'§5§lOLD ENDER',with:[logo]}
           Sin pack la clave no existe y Minecraft muestra el fallback (el titulo de siempre);
           con pack se ve el logo del boss (una imagen de la fuente dextra:hud).

Cada script de boss llama a las funciones de aqui para anadir/actualizar SOLO sus entradas
en los .json compartidos.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PACK = REPO / "Modelos/DextraBossesPack"
ASSETS = PACK / "assets/dextra"
BOSSBAR_SPRITES = PACK / "assets/minecraft/textures/gui/sprites/boss_bar"
IA = REPO / "Modelos/ItemsAdder/contents/dextra_bosses"
NS = "dextra"

# Un caracter por boss para la bossbar: espacios unicode que en vanilla se ven en blanco
# (glifos vacios de unifont). Heracles usa \u200c y \u2001 en su bossbar; su titulo va con
# texto traducible y los laureles en dextra:hud (tools/heracles_title.py).
BOSSBAR_CHAR = {
    "old_ender": "\u2004", "baal": "\u2005", "red_hand": "\u2006", "ragnarok": "\u2007",
    "mushlord": "\u2008", "lady_of_laments": "\u2009", "yeti": "\u200a", "kronos": "\u2000",
    "azathoth": "\u205f", "leviatan": "\u3000", "xylar": "\uffa0", "samhain": "\u202f",
    "thor": "\u00a0", "kukulkan": "\u2002", "nezareth": "\u2003",
}
# Caracteres de la fuente propia dextra:hud (zona de uso privado; solo existen con el pack)
TITLE_CHARS = {
    "old_ender": ("\ue201", "\ue202"), "baal": ("\ue203", "\ue204"), "red_hand": ("\ue205", "\ue206"),
    "ragnarok": ("\ue207", "\ue208"), "mushlord": ("\ue209", "\ue20a"), "lady_of_laments": ("\ue20b", "\ue20c"),
    "yeti": ("\ue20d", "\ue20e"), "kronos": ("\ue20f", "\ue210"), "azathoth": ("\ue211", "\ue212"),
    "leviatan": ("\ue213", "\ue214"), "xylar": ("\ue215", "\ue216"), "samhain": ("\ue217", "\ue218"),
    "thor": ("\ue219", "\ue21a"), "kukulkan": ("\ue21b", "\ue21c"), "nezareth": ("\ue21d", "\ue21e"),
    "heracles": ("\ue21f", "\ue220"),
}


def _load(path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def _save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def ensure_pack():
    _save(PACK / "pack.mcmeta", {"pack": {"pack_format": 69, "description": "Dextra Bosses: sonidos, titulos y bossbars"}})


def sound_dir(boss):
    d = ASSETS / "sounds" / boss
    d.mkdir(parents=True, exist_ok=True)
    return d


def register_sounds(boss, entries):
    """entries = {nombre: distancia} -> dextra:<boss>.<nombre>"""
    path = ASSETS / "sounds.json"
    data = {k: v for k, v in _load(path, {}).items() if not k.startswith(boss + ".")}
    for name, dist in entries.items():
        data[f"{boss}.{name}"] = {"sounds": [{"name": f"{NS}:{boss}/{name}", "attenuation_distance": dist}]}
    _save(path, dict(sorted(data.items())))


def register_title(boss, logo_png, height, ascent):
    """Logo del titulo (imagen con el nombre) en la fuente dextra:hud + texto traducible."""
    tdir = ASSETS / "textures/font" / boss
    tdir.mkdir(parents=True, exist_ok=True)
    for old in tdir.glob("title_*.png"):
        old.unlink()
    logo_png.save(tdir / "title_logo.png")
    ch = TITLE_CHARS[boss][0]
    path = ASSETS / "font/hud.json"
    data = _load(path, {"providers": []})
    data["providers"] = [p for p in data["providers"] if f"/{boss}/" not in p.get("file", "")]
    data["providers"].append({"type": "bitmap", "file": f"{NS}:font/{boss}/title_logo.png",
                              "height": height, "ascent": ascent, "chars": [ch]})
    _save(path, data)
    lang = ASSETS / "lang/en_us.json"
    ldata = _load(lang, {})
    ldata[f"dextra.title.{boss}"] = "%1$s"
    _save(lang, dict(sorted(ldata.items())))


def title_component(boss, fallback):
    """Texto SNBT para /title, escapado para usarse dentro de command{c="..."} de MythicMobs.
    Sin pack: 'fallback' (el titulo de siempre). Con pack: el logo."""
    ch = TITLE_CHARS[boss][0]
    return ("<&lc>translate:''dextra.title.%s'',fallback:''%s'',with:<&lb>"
            "<&lc>text:''%s'',font:''dextra:hud'',color:''white''<&rc><&rb><&rc>") % (boss, fallback, ch)


def register_bossbar(boss, png, ascent, height):
    """Media moldura de la bossbar como font image de ItemsAdder."""
    tdir = IA / "textures/font" / boss
    tdir.mkdir(parents=True, exist_ok=True)
    png.save(tdir / "bossbar.png")
    ch = BOSSBAR_CHAR[boss]
    yml = (
        f"# Marco de la bossbar de {boss} (generado por tools/; no lo edites a mano).\n"
        f"# En MythicMobs: BossBar.Title = \"&f\\u{ord(ch):04x}<nombre>&f\\u{ord(ch):04x}\"\n"
        f"# Sin pack el caracter \\u{ord(ch):04x} es un espacio en blanco; con pack es esta imagen.\n"
        "info:\n"
        "  namespace: dextra_bosses\n\n"
        "font_images:\n"
        f"  {boss}_bossbar:\n"
        f"    path: font/{boss}/bossbar.png\n"
        f"    symbol: \"\\u{ord(ch):04x}\"\n"
        f"    scale_ratio: {height}\n"
        f"    y_position: {ascent}\n"
        "    show_in_gui: false\n"
        "    shadow:\n"
        "      enabled: false\n"
    )
    IA.mkdir(parents=True, exist_ok=True)
    (IA / f"{boss}.yml").write_text(yml, encoding="utf-8")


def save_bar_sprites(color, progress, background):
    BOSSBAR_SPRITES.mkdir(parents=True, exist_ok=True)
    progress.save(BOSSBAR_SPRITES / f"{color}_progress.png")
    background.save(BOSSBAR_SPRITES / f"{color}_background.png")
