#!/usr/bin/env python3
"""
Pasa el titulo de aparicion de Heracles al mismo sistema que los bosses 02-17 (texto
traducible + fuente dextra:hud), para liberar los caracteres \\u2002 y \\u2003 que ahora usan
Kukulkan y Nezareth en sus bossbars.

  - Copia los laureles (Modelos/01_Heracles/.../title_laurel_*.png) al DextraBossesPack como
    \\ue21f (izquierdo) y \\ue220 (derecho) de la fuente dextra:hud.
  - Clave "dextra.title.heracles" = "%1$s%2$s%3$s": laurel + "⚔ HERACLES ⚔" + laurel.
  - Quita los laureles de heracles_hud.yml (ItemsAdder) y cambia el /title de Heracles_Intro.
  Sin pack se ve "⚔ HERACLES ⚔" como siempre.

Uso: python3 tools/heracles_title.py
"""
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import dextra_pack as DP  # noqa: E402
import wire as WR  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
HUD = REPO / "Modelos/01_Heracles/ItemsAdder/contents/heracles_hud"
L, R = DP.TITLE_CHARS["heracles"]


def main():
    DP.ensure_pack()
    tdir = DP.ASSETS / "textures/font/heracles"
    tdir.mkdir(parents=True, exist_ok=True)
    for side in ("left", "right"):
        shutil.copy(HUD / f"textures/font/title_laurel_{side}.png", tdir / f"laurel_{side}.png")
    path = DP.ASSETS / "font/hud.json"
    data = DP._load(path, {"providers": []})
    data["providers"] = [p for p in data["providers"] if "/heracles/" not in p.get("file", "")]
    for side, ch in (("left", L), ("right", R)):
        data["providers"].append({"type": "bitmap", "file": f"{DP.NS}:font/heracles/laurel_{side}.png",
                                  "height": 12, "ascent": 9, "chars": [ch]})
    DP._save(path, data)
    lang = DP.ASSETS / "lang/en_us.json"
    ldata = DP._load(lang, {})
    ldata["dextra.title.heracles"] = "%1$s%2$s%3$s"
    DP._save(lang, dict(sorted(ldata.items())))

    # ItemsAdder: fuera los laureles (\u2002 y \u2003 quedan libres)
    yml = (HUD / "heracles_hud.yml").read_text(encoding="utf-8")
    if "title_laurel_left" in yml:
        yml = yml[:yml.index("  title_laurel_left:")].rstrip("\n") + "\n"
        yml = yml.replace('#   Titulo  (heracles_skills.yml -> Heracles_Intro): "&f\u2002&6⚔ &e&lHERACLES &6⚔&f\u2003"\n',
                          '#   Titulo: ya no va aqui; los laureles estan en Modelos/DextraBossesPack (fuente dextra:hud),\n'
                          '#   ver tools/heracles_title.py.\n')
        yml = yml.replace(" y \u2001 / \u2002 / \u2003 (espacios)", " y \u2001 (espacio)")
        yml = yml.replace("\u2001 /\u2002 /\u2003 (espacios)", "\u2001 (espacio)")
        (HUD / "heracles_hud.yml").write_text(yml, encoding="utf-8")
        for side in ("left", "right"):
            (HUD / f"textures/font/title_laurel_{side}.png").unlink()

    s = WR.Yml("MythicMobs-3D/Skills/heracles_skills.yml")
    old_c = '    # sin pack: "⚔ HERACLES ⚔" de siempre; con pack: laureles a los lados (\\u2002 y \\u2003)\n'
    old_t = ('    - \'title{title="&f\u2002&6⚔ &e&lHERACLES &6⚔&f\u2003";subtitle="&8« &7Greek Village &8• &6El campeón del '
             'Olimpo ha despertado &8»";fadein=20;stay=300;fadeout=20} @Server\'\n')
    if old_t in s.s:
        comp = ("<&lc>translate:''dextra.title.heracles'',fallback:''§6⚔ §e§lHERACLES §6⚔'',with:<&lb>"
                "<&lc>text:''%s'',font:''dextra:hud'',color:''white''<&rc>,"
                "<&lc>text:''§6⚔ §e§lHERACLES §6⚔''<&rc>,"
                "<&lc>text:''%s'',font:''dextra:hud'',color:''white''<&rc><&rb><&rc>") % (L, R)
        s.rep(old_c, '    # sin pack: "⚔ HERACLES ⚔" de siempre; con pack: laureles a los lados (fuente dextra:hud)\n')
        s.rep(old_t, ("    - 'command{c=\"minecraft:title @a times 20 300 20\"} @self'\n"
                      "    - 'command{c=\"minecraft:title @a subtitle <&lc>text:''§8« §7Greek Village §8• §6El campeón del "
                      "Olimpo ha despertado §8»''<&rc>\"} @self'\n"
                      f"    - 'command{{c=\"minecraft:title @a title {comp}\"}} @self'\n"))
        s.save()
    print("OK titulo de Heracles migrado")


if __name__ == "__main__":
    main()
