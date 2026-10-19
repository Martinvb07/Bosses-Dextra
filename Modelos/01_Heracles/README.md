# HERACLES: boss con modelos de ModelEngine (Java 1.21.10)

Boss 01 del servidor. Es un modelo personalizado para **ModelEngine R4**, preparado para **MythicMobs** (y compatible con el pack de **Mythic Crucible**).

![Vistas](preview/heracles_vistas.png)
![Acciones](preview/heracles_acciones.png)

## Contenido

| Archivo | Qué es |
|---|---|
| `ModelEngine/blueprints/heracles/heracles.bbmodel` | Modelo de Blockbench (formato *Generic Model*) con la textura incrustada y 14 animaciones |
| `ModelEngine/blueprints/heracles/heracles_texture.png` | La textura, por si quieres retocarla aparte |
| `ModelEngine/blueprints/hoplit/`, `spartan_warrior/`, `greek_archer/`, `minotaur/` | Modelos de los súbditos |
| `../../MythicMobs-3D/Mobs/Boss_01_Heracles/Heracles_Mobs.yml` | Mob `Heracles`, ahora con `model{mid=heracles}` |
| `../../MythicMobs-3D/Skills/heracles_skills.yml` | Skills con animaciones y sonidos sincronizados |
| `ItemsAdder/contents/heracles_hud/` | Marco de la bossbar (font images de ItemsAdder) |
| `../DextraBossesPack/assets/dextra/textures/font/heracles/` | Laureles del título (fuente `dextra:hud`, igual que los bosses 02-17) |
| `ResourcePack/HeraclesPack/` | Textura de la barra y sonidos propios (se fusiona con el pack de ItemsAdder) |
| `preview/*.gif` | Vista previa de cada animación |
| `../../tools/generate_heracles.py` | Script que genera el `.bbmodel` (sirve para regenerarlo o hacer cambios) |
| `../../tools/render_preview.py` | Script que renderiza las imágenes y los GIF |
| `../../tools/generate_minions.py` + `../../tools/bbmodel.py` | Generan los modelos de los súbditos y sus vistas previas |
| `../../tools/generate_sounds.py` | Sintetiza los sonidos propios y `preview/sonidos_demo.mp3` |
| `../../tools/generate_hud.py` | Script que genera el marco, los laureles, la barra y `preview/hud_preview.png` |

## Instalación

1. Copia las carpetas de `ModelEngine/blueprints/` (`heracles`, `hoplit`, `spartan_warrior`, `greek_archer` y `minotaur`) en `plugins/ModelEngine/blueprints/`.
2. Sustituye los archivos de MythicMobs:
   - `plugins/MythicMobs/Mobs/Boss_01_Heracles/Heracles_Mobs.yml`
   - `plugins/MythicMobs/Skills/heracles_skills.yml`
3. Ejecuta `/meg reload` y después `/mm reload`.
4. Aplica el resource pack que genera ModelEngine (`plugins/ModelEngine/resource pack.zip`), o combínalo con tu pack de MythicMobs/Crucible.
5. Pruébalo con `/mm m spawn Heracles`.

> Haz copia de seguridad de los dos `.yml` originales antes de sustituirlos. Solo cambia la parte visual: animaciones, sonidos y partículas. Vida, daño, fases e invocaciones se quedan igual.

## Bossbar y título olímpicos

![HUD](preview/hud_preview.png)

Funciona **con y sin** el resource pack:

| | Sin texturas | Con texturas |
|---|---|---|
| Bossbar | Barra amarilla vanilla con `HERACLES` en dorado | Marco con columnas, alas y laurel; `HERACLES` en el centro y barra dorada |
| Título al aparecer | `⚔ HERACLES ⚔` | El mismo texto con laureles a los lados |
| Sonidos | Los sonidos vanilla | Los vanilla más los propios |

El título de la bossbar es `&f\u200c&6&lHERACLES&f\u2001`: `\u200c` y `\u2001` no se ven en vanilla, y con el pack ItemsAdder los convierte en las dos mitades del marco. El título de aparición se manda con `/title` y un texto traducible: sin pack se ve `⚔ HERACLES ⚔` y con el DextraBossesPack salen los laureles a los lados (`tools/heracles_title.py`).

Instalación con ItemsAdder:

1. Copia `ItemsAdder/contents/heracles_hud/` en `plugins/ItemsAdder/contents/heracles_hud/`.
2. Copia `ResourcePack/HeraclesPack/` en `plugins/HeraclesPack/` y añádela en `plugins/ItemsAdder/config.yml`:
   ```yaml
   merge_other_plugins_resourcepacks_folders:
     - ModelEngine/resource pack
     - WeaponMechanicsPack
     - DextralityArmas/DextralityArmas/resource pack/resource pack
     - HeraclesPack
   ```
3. `/iazip` y después `/mm reload`. Vuelve a entrar al servidor para recibir el pack.

Notas:

- No cambies el texto `&6&lHERACLES` de la bossbar: el marco está medido para ese ancho.
- Si el marco sale 1 px desplazado respecto a la barra, ajusta `y_position` de `bossbar_left` y `bossbar_right` (18) de uno en uno.
- Cualquier otra bossbar `YELLOW` del servidor también tendrá la textura dorada.
- El marco mide 48 px de alto: si hay otra bossbar visible a la vez, se solapan.
- Para cambiar el diseño, edita `tools/generate_hud.py` y ejecútalo: regenera los PNG y la vista previa.

Títulos en pantalla (todos con `title{}` de MythicMobs):

| Momento | Título | Subtítulo |
|---|---|---|
| Aparece (`Heracles_Intro`) | ⚔ HERACLES ⚔ (con laureles si tiene el pack) | Greek Village • El campeón del Olimpo ha despertado |
| Fase 2 | FURIA DIVINA | Heracles ha perdido la paciencia |
| Fase 3 | LA ÚLTIMA PRUEBA | Los hoplitas acuden a su llamado |
| Último aliento | ÚLTIMO ALIENTO | Heracles se niega a caer... |
| Muere | ⚔ VICTORIA ⚔ | Heracles ha caído • ¡El Dungeon está liberado! |

## Súbditos

| Mob | Modelo | Aspecto | Animaciones |
|---|---|---|---|
| `Hoplit` | `hoplit` | Linotórax blanco, casco corintio con penacho, lanza y escudo azul con sol | idle, walk, attack (lanzazo 0.35 s), hurt, spawn, death |
| `SpartanWarrior` | `spartan_warrior` | Coraza de bronce, capa roja, penacho transversal, xiphos y escudo Λ | idle, walk, attack (estocada 0.30 s), block, hurt, spawn, death |
| `GreekArcher` | `greek_archer` | Túnica verde, gorro frigio, carcaj y arco | idle, walk, shoot (suelta 0.40 s), hurt, spawn, death |
| `Minotaur` | `minotaur` | Cabeza de toro, cuernos, aro dorado y hacha doble (labrys) | idle, walk, attack, charge (impacto 0.50 s), roar, spawn, hurt, death |

![Hoplita](preview/minions/hoplit.png)
![Espartano](preview/minions/spartan_warrior.png)
![Arquero](preview/minions/greek_archer.png)
![Minotauro](preview/minions/minotaur.png)

## Sonidos propios

Están en `ResourcePack/HeraclesPack/assets/olympus/` y llegan a los jugadores con el resource pack (por eso `HeraclesPack` tiene que estar en la lista de ItemsAdder). Se usan como `effect:sound{s=olympus:heracles.roar}`.

| Sonido | Dónde suena |
|---|---|
| `olympus:heracles.intro` | Al aparecer: coro divino y trueno |
| `olympus:heracles.roar` | Al alzar el garrote en la intro, `Heracles_OlympusRoar` y `Heracles_LastBreath` |
| `olympus:heracles.hurt` | Al recibir daño y al prepararse para `Heracles_Quake` |
| `olympus:heracles.swing` | Golpe del garrote y salto del terremoto |
| `olympus:heracles.slam` | Impactos de `Heracles_Slam`, `Heracles_Charge` y del cambio de fase |
| `olympus:heracles.quake` | Impacto de `Heracles_Quake` |
| `olympus:heracles.charge` | Grito de guerra de `Heracles_Charge` |
| `olympus:heracles.phase` | Cambio de fase (estalla en la pose de fuerza) |
| `olympus:heracles.summon` | Cuerno de guerra al llamar a espartanos, minotauro y hoplitas |
| `olympus:heracles.last_breath` | `Heracles_LastBreath` |
| `olympus:heracles.death` | Al morir |
| `olympus:minotaur.roar` / `olympus:minotaur.snort` | Aparición y embestida del Minotauro |

Escúchalos todos seguidos en `preview/sonidos_demo.mp3`. Son sintetizados por código, así que puedes cambiar tono y duración en `tools/generate_sounds.py`, o sustituir cualquier `.ogg` por uno tuyo con el mismo nombre.

## Huesos (bones)

- `hitbox`: define el hitbox, de 1.5 × 2.9 bloques. La altura de los ojos está en Y = 42 px.
- `h_head`: la cabeza sigue al jugador al que mira el boss.
- `tag_name`: hueso para el nombre flotante. Es opcional.
- Huesos animados: `body`, `torso`, `right_arm` / `left_arm` (con `_forearm` y `_hand`), `club` (garrote), `right_leg` / `left_leg` (con `_lower_leg`), `pelt` / `pelt_lower` / `tail` (piel de león y cola), `skirt_front` / `skirt_back`.

## Animaciones

| Animación | Tipo | Duración | Cuándo se usa | Momento clave |
|---|---|---|---|---|
| `idle` | loop | 3.0 s | De pie (fase 1) | — |
| `walk` | loop | 1.2 s | Andando (fase 1) | — |
| `spawn` | once | 3.0 s | `Heracles_Intro` | Se levanta (1.4–2.1 s) y alza el garrote (2.45 s) |
| `attack` | once | 1.0 s | `Heracles_Slam` | Impacto a 0.5 s (10 ticks) |
| `quake` | once | 1.6 s | `Heracles_Quake` | Salto (0.45 s) e impacto (1.0 s / 20 ticks) |
| `roar` | once | 2.0 s | `Heracles_OlympusRoar` | Rugido a 0.4 s |
| `charge` | once | 1.2 s | `Heracles_Charge` | Embestida a 0.5 s |
| `phase_change` | once | 2.2 s | `Heracles_PhaseShield` (cambio de fase) | Golpe al suelo (0.6 s) y pose de fuerza (1.35 s) |
| `summon` | once | 1.6 s | Llamadas a espartanos, arqueros y Minotauro | Garrote al cielo (0.4 s) |
| `last_breath` | once | 2.0 s | `Heracles_LastBreath` | Cae de rodilla (0.8 s) y se levanta (1.6 s) |
| `hurt` | once | 0.4 s | Al recibir daño (35 %) | — |
| `idle_rage` / `walk_rage` | loop | 1.4 / 0.9 s | Desde la FASE 2 (`defaultstate`) | Más encorvado y agresivo |
| `death` | hold | 3.0 s | Automática al morir | De rodillas (1.2 s) y cae (2.6 s) |

## Sonidos

Todos los sonidos son **sonidos vanilla de 1.21.10** combinados entre sí, con el tono ajustado. Se disparan desde las skills con `delay` sincronizados con cada animación, así que no hace falta añadir sonidos al resource pack.

Si más adelante quieres sonidos propios (`.ogg`), añádelos en `assets/heracles/sounds/` de tu pack y cambia los `effect:sound{s=...}` por `heracles:<nombre>`.

## Cómo editarlo

Abre el `.bbmodel` en **Blockbench** (con el plugin de ModelEngine si lo usas). También puedes cambiar el script y regenerarlo:

```bash
python3 tools/generate_heracles.py          # regenera el .bbmodel y la textura
python3 tools/render_preview.py out.png attack:0.5@-40 quake:1.0@-40   # imágenes de prueba
```
