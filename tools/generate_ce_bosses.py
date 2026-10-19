#!/usr/bin/env python3
"""
Genera ConditionalEvents/events/bosses_rotacion.yml: la rotacion semanal de los
bosses 10-17 segun el calendario de eventos del servidor.

- BOSSES todos los dias a las horas pares (hora de Peru/Colombia), salvo el
  domingo a las 14:00, que es MEGAKOTH (ese turno solo retira al boss anterior).
- Los bosses rotan en orden (ROTACION) a lo largo de la semana.
- En cada turno se retira el boss anterior si sigue vivo (nadie lo mato en 2 h)
  y aparece el siguiente.
- El Docker esta en UTC (Peru/Colombia + 5), pero %server_time_...% de PAPI NO usa
  esa hora: va 1 hora por delante de Peru/Colombia (UTC-4; medido el lunes 19/10/2026:
  PAPI lun-14:33, Peru 13:33, consola 18:33). Desde las 23:00 de Peru/Colombia, en PAPI
  ya es el dia siguiente. Si cambia la zona horaria de la expansion, cambia DESFASE.

Uso: python3 tools/generate_ce_bosses.py
"""
from pathlib import Path

import yaml

OUT = Path(__file__).resolve().parent.parent / "ConditionalEvents/events/bosses_rotacion.yml"

ROTACION = ["Kronos", "Azathoth", "Leviatan", "Xylar", "Samhain", "Thor", "Kukulkan", "Nezareth"]
LUGAR = "Warps,60053.5,73,60059.5"
HORAS = list(range(0, 24, 2))                 # turnos de BOSSES (hora Peru/Colombia)
SIN_BOSS = {("Sun", 14): "MEGAKOTH"}          # turnos ocupados por otro evento
DESFASE = 1                                   # hora de PAPI = hora Peru/Colombia + DESFASE

DIAS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
# Como devuelve el dia %server_time_E% en el servidor (la expansion Server lo da en español)
DIA_PAPI = {"Mon": "lun", "Tue": "mar", "Wed": "mié", "Thu": "jue", "Fri": "vie", "Sat": "sáb", "Sun": "dom"}
NOMBRE = {"Mon": "lunes", "Tue": "martes", "Wed": "miercoles", "Thu": "jueves",
          "Fri": "viernes", "Sat": "sabado", "Sun": "domingo"}


def a_papi(dia, hora):
    h = hora + DESFASE
    d = DIAS.index(dia)
    if h >= 24:
        h -= 24
        d = (d + 1) % 7
    return DIAS[d], h


HORA = "%server_time_E-HH:mm%"              # un solo placeholder: ver la nota de la cabecera


# Chunks de la arena (3x3 alrededor del punto de aparicion) que se dejan siempre cargados.
# Sin esto, si no hay nadie cerca, `mm mobs kill` no ve al boss anterior y se van acumulando.
ARENA = "execute in minecraft:warps run forceload add 60032 60032 60079 60079"


def turno(boss):
    # Los mobs de un chunk recien cargado tardan un momento en aparecer: se espera antes de
    # retirar a los anteriores, y otra vez antes de sacar al nuevo para que el kill ya haya pasado.
    acciones = [f"console_command: {ARENA}", "wait: 5"]
    acciones += [f"console_command: mm mobs kill {b}" for b in ROTACION]
    acciones.append("wait: 2")
    if boss:
        acciones.append(f"console_command: mm mobs spawn {boss} 1 {LUGAR}")
    return acciones


def main():
    condiciones, grupos, filas, i = [], {}, [], 0
    for dia in DIAS:
        for hora in HORAS:
            otro = SIN_BOSS.get((dia, hora))
            boss = None if otro else ROTACION[i % len(ROTACION)]
            if boss:
                i += 1
            nombre = f"{NOMBRE[dia]}_{hora:02d}00"
            sdia, shora = a_papi(dia, hora)
            condiciones.append(f"{HORA} == {DIA_PAPI[sdia]}-{shora:02d}:00 execute {nombre}")
            grupos[nombre] = turno(boss)
            filas.append(f"#   {NOMBRE[dia]:<9} {hora:02d}:00  ->  PAPI {sdia} {shora:02d}:00  ->  "
                         + (boss or f"solo retira al anterior ({otro})"))

    cabecera = (
        "# Rotacion de los bosses 10-17 (generado por tools/generate_ce_bosses.py; no lo edites a mano)\n"
        f"# Lugar: {LUGAR.replace(',', ' ')}\n"
        "# En cada turno se retira el boss anterior si sigue vivo y aparece el siguiente.\n"
        "# Es un solo evento que mira la hora una vez por minuto con un unico placeholder. Con un evento\n"
        "# por turno, los 84 se comprobaban a la vez en hilos distintos y la expansion Server de PAPI\n"
        "# lanzaba ConcurrentModificationException (y ese turno podia no salir).\n"
        "# El dia sale en español (lun, mar, mié, jue, vie, sáb, dom); la hora es la de PAPI (Peru/Colombia + 1, no la del Docker).\n"
        "#\n#   Peru/Colombia      ->  PAPI (UTC-4)          ->  boss\n" + "\n".join(filas) + "\n\n"
    )
    grupos["default"] = []                    # ningun turno coincide: no hacer nada
    eventos = {"bosses_rotacion": {
        "type": "repetitive_server",
        "repetitive_time": 1200,              # cada 60 s: cada minuto HH:mm se comprueba una vez
        "conditions": condiciones,
        "actions": grupos,
    }}
    texto = yaml.safe_dump({"Events": eventos}, sort_keys=False, allow_unicode=True, width=200)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(cabecera + texto, encoding="utf-8")
    ev = yaml.safe_load(OUT.read_text(encoding="utf-8"))["Events"]["bosses_rotacion"]
    assert len(ev["conditions"]) == len(DIAS) * len(HORAS) == len(ev["actions"]) - 1
    print(f"OK {OUT} ({len(condiciones)} turnos, {i} apariciones)")


if __name__ == "__main__":
    main()
