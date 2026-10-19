# Modelos

Modelos 3D (ModelEngine), animaciones, texturas, sonidos y vistas previas de cada boss.
Hay una carpeta por boss, con el mismo numero que en `MythicMobs-3D/Mobs/Boss_XX_<Nombre>/`.

| # | Boss | Estado |
|---|---|---|
| 01 | [Heracles](01_Heracles/) | ✅ con modelos |
| 02 | [OldEnder](02_OldEnder/) | pendiente |
| 03 | [Baal](03_Baal/) | pendiente |
| 04 | [RedHand](04_RedHand/) | pendiente |
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
