# ConditionalEvents: apariciones programadas de los bosses

Un archivo por evento en `events/`. Se copian a `plugins/ConditionalEvents/events/` y se recargan con `/ce reload`.

Requisitos: ConditionalEvents y PlaceholderAPI con la expansion **Server** (`/papi ecloud download Server` y `/papi reload`).

## Calendario

`events/bosses_rotacion.yml`: rotacion de los bosses 10-17 segun el calendario de eventos.

- **Cuando:** todos los dias a las horas pares (0:00, 2:00 ... 22:00, hora de Peru/Colombia).
  El domingo a las 14:00 es MEGAKOTH: ese turno no saca boss, solo retira al anterior.
- **Orden:** Kronos, Azathoth, Leviatan, Xylar, Samhain, Thor, Kukulkan y Nezareth, y vuelta a empezar
  (la lista completa de turnos esta al principio del archivo).
- **Donde:** mundo `Warps`, 60053.5 73 60059.5.
- **Si nadie lo mata en 2 horas:** en cada turno se ejecuta `mm mobs kill` de los 8 bosses antes de sacar al siguiente.
- **Como funciona:** es un solo evento (`bosses_rotacion`) que cada 60 s lee `%server_time_E-HH:mm%`
  (por ejemplo `lun-05:00`) y ejecuta el grupo de acciones del turno que coincide.
  No lo partas en un evento por turno: muchos eventos leyendo `%server_time_...%` a la vez hacen que la
  expansion Server de PAPI lance `ConcurrentModificationException` y el turno puede no salir.

El archivo lo genera `tools/generate_ce_bosses.py`. Para cambiar el orden, las horas o el lugar, edita
las variables del principio del script y ejecutalo: `python3 tools/generate_ce_bosses.py`.

## Como poner el dia y la hora

El Docker de Pterodactyl esta en UTC (5 horas por delante de Peru y Colombia), pero **eso no importa aqui**:
lo que mira el evento es `%server_time_...%` de PAPI, y la expansion Server va solo **1 hora** por delante
de Peru y Colombia (UTC-4). Medido el lunes 19/10/2026: PAPI `lun-14:33`, Peru 13:33, consola 18:33.

- **Hora:** suma 1 hora a la hora de Peru/Colombia, en formato de 24 h (`HH:mm`).
- **Dia:** si al sumar pasas de las 24:00, resta 24 y usa el **dia siguiente**.
  Es decir: desde las 11:00 p. m. de Peru/Colombia, en PAPI ya es el dia siguiente.
- Si algun dia la diferencia cambia (otra zona horaria en la expansion, cambio de hora), cambia
  `DESFASE` en `tools/generate_ce_bosses.py` y vuelve a generar el archivo.

La expansion Server devuelve el dia en español:

| Dia | `%server_time_E%` |
|---|---|
| Lunes | `lun` |
| Martes | `mar` |
| Miercoles | `mié` |
| Jueves | `jue` |
| Viernes | `vie` |
| Sabado | `sáb` |
| Domingo | `dom` |

| Peru/Colombia | En el evento |
|---|---|
| Martes 2:00 p. m. | `mar` y `15:00` |
| Domingo 5:35 p. m. | `dom` y `18:35` |
| Sabado 11:00 p. m. | **`dom`** y `00:00` |
| Viernes 11:30 p. m. | **`sáb`** y `00:30` |

## Comprobar y depurar

```
papi parse --null %server_time_E-HH:mm%   -> dia y hora del servidor, p. ej. lun-14:33 (Peru + 1)
ce debug bosses_rotacion                  -> muestra en el chat que condiciones pasan
```

`%server_time_u%` **no** sirve para el dia: en la expansion Server devuelve el año.

El mundo donde aparece el boss no puede estar en dificultad pacifica (los mobs hostiles se borran al instante).
