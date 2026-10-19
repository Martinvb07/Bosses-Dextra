# Modelos

Modelos 3D (ModelEngine), animaciones, texturas, sonidos y vistas previas de cada boss.
Hay una carpeta por boss, con el mismo numero que en `MythicMobs-3D/Mobs/Boss_XX_<Nombre>/`.

| # | Boss | Estado |
|---|---|---|
| 01 | [Heracles](01_Heracles/) | ✅ con modelos |
| 02 | [OldEnder](02_OldEnder/) | ✅ con modelos |
| 03 | [Baal](03_Baal/) | ✅ con modelos |
| 04 | [RedHand](04_RedHand/) | ✅ con modelos |
| 05 | [Ragnarok](05_Ragnarok/) | pendiente |
| 06 | [Mushlord](06_Mushlord/) | pendiente |
| 07 | [LadyOfLaments](07_LadyOfLaments/) | pendiente |
| 08 | [Yeti](08_Yeti/) | pendiente |
| 10 | [Kronos](10_Kronos/) | pendiente |
| 11 | [Azathoth](11_Azathoth/) | pendiente |
| 12 | [Leviatan](12_Leviatan/) | pendiente |
| 13 | [Xylar](13_Xylar/) | pendiente |
| 14 | [Samhain](14_Samhain/) | pendiente |
| 15 | [Thor](15_Thor/) | pendiente |
| 16 | [Kukulkan](16_Kukulkan/) | pendiente |
| 17 | [Nezareth](17_Nezareth/) | pendiente |

Cada carpeta sigue la estructura de `01_Heracles/`:

```
ModelEngine/blueprints/<modelo>/   .bbmodel y textura -> plugins/ModelEngine/blueprints/
ItemsAdder/                        font images (bossbar, titulos) -> plugins/ItemsAdder/contents/
ResourcePack/                      texturas y sonidos extra -> plugins/<carpeta>, fusionada por ItemsAdder
preview/                           imagenes, GIF y demos de sonido
README.md                          instalacion, animaciones y skills
```

Los .yml de MythicMobs con los modelos ya conectados estan en `MythicMobs-3D/` (servidor con texturas);
`MythicMobs-Normal/` es la misma configuracion solo vanilla. Los scripts que generan modelos y sonidos estan en `tools/`.

## Pack compartido (bosses 02-17)

A partir del boss 02, todo lo que no es de ModelEngine va en dos carpetas compartidas. Se instalan una sola vez, y cada boss nuevo solo añade archivos dentro:

| Carpeta | Dónde va | Qué tiene |
|---|---|---|
| `DextraBossesPack/` | `plugins/DextraBossesPack/` | Sonidos (`dextra:<boss>.<sonido>`), adornos de los títulos (fuente `dextra:hud`), textos del título y texturas de la barra |
| `ItemsAdder/contents/dextra_bosses/` | `plugins/ItemsAdder/contents/dextra_bosses/` | Una moldura de bossbar por boss |

Añade la carpeta en `plugins/ItemsAdder/config.yml` (una sola vez):

```yaml
merge_other_plugins_resourcepacks_folders:
  - ModelEngine/resource pack
  - WeaponMechanicsPack
  - DextralityArmas/DextralityArmas/resource pack/resource pack
  - HeraclesPack
  - DextraBossesPack
```

Luego `/iazip`, `/mm reload` y vuelve a entrar.

Funciona **con y sin** el pack:

- **Bossbar:** cada boss lleva un espacio unicode distinto a cada lado del nombre (`tools/dextra_pack.py`, `BOSSBAR_CHAR`). En vanilla es un espacio en blanco; con el pack es la moldura.
- **Título de aparición:** se manda con `/title` y un texto traducible. Sin pack se muestra el texto de siempre (`fallback`); con pack, el texto con sus adornos.
- **Sonidos:** cada sonido propio suena junto al vanilla de siempre. Quien no tiene el pack oye solo el vanilla.

Para probar solo el título: `/title @s title {translate:'dextra.title.old_ender',fallback:'OLD ENDER'}`.
