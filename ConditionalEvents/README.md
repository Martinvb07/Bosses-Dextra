# ConditionalEvents: apariciones programadas de los bosses

Un archivo por evento en `events/`. Se copian a `plugins/ConditionalEvents/events/` y se recargan con `/ce reload`.

Requisitos: ConditionalEvents y PlaceholderAPI con la expansion **Server** (`/papi ecloud download Server` y `/papi reload`).

## Calendario

| Boss | Dia y hora (Peru/Colombia) | En el servidor (UTC) | Lugar | Archivo |
|---|---|---|---|---|
| Heracles | Domingo 5:35 p. m. | `Sun` 22:35 | `world_test` 0.5 65 -0.5 | `events/heracles_domingo.yml` |

## Como poner el dia y la hora

El servidor (el Docker de Pterodactyl) esta en **UTC**, 5 horas por delante de Peru y Colombia.

- **Hora:** suma 5 horas a la hora de Peru/Colombia, en formato de 24 h (`HH:mm`).
- **Dia:** si al sumar pasas de las 24:00, resta 24 y usa el **dia siguiente**.
  Es decir: desde las 7:00 p. m. de Peru/Colombia, en el servidor ya es el dia siguiente.

| Dia | `%server_time_E%` |
|---|---|
| Lunes | `Mon` |
| Martes | `Tue` |
| Miercoles | `Wed` |
| Jueves | `Thu` |
| Viernes | `Fri` |
| Sabado | `Sat` |
| Domingo | `Sun` |

| Peru/Colombia | En el evento |
|---|---|
| Martes 2:00 p. m. | `Tue` y `19:00` |
| Domingo 5:35 p. m. | `Sun` y `22:35` |
| Sabado 7:00 p. m. | **`Sun`** y `00:00` |
| Viernes 9:30 p. m. | **`Sat`** y `02:30` |

## Comprobar y depurar

```
papi parse --null %server_time_E%       -> dia del servidor (Sun, Mon...)
papi parse --null %server_time_HH:mm%   -> hora del servidor (UTC)
ce debug <evento>                       -> muestra en el chat que condiciones pasan
```

`%server_time_u%` **no** sirve para el dia: en la expansion Server devuelve el año.

El mundo donde aparece el boss no puede estar en dificultad pacifica (los mobs hostiles se borran al instante).
