#!/usr/bin/env python3
"""
Genera ConditionalEvents/events/bosses_rotacion.yml: la rotacion semanal de los
bosses 10-17 segun el calendario de eventos del servidor.

- BOSSES todos los dias a las horas pares (hora de Peru/Colombia), salvo el
  domingo a las 14:00, que es MEGAKOTH (ese turno solo retira al boss anterior).
- Los bosses rotan en orden (ROTACION) a lo largo de la semana.
- En cada turno se retira el boss anterior si sigue vivo (nadie lo mato en 2 h)
  y aparece el siguiente.
- El servidor esta en UTC: hora del servidor = hora Peru/Colombia + 5. Desde las
  19:00 de Peru/Colombia, en el servidor ya es el dia siguiente.

Uso: python3 tools/generate_ce_bosses.py
"""
from pathlib import Path

import yaml

OUT = Path(__file__).resolve().parent.parent / "ConditionalEvents/events/bosses_rotacion.yml"

ROTACION = ["Kronos", "Azathoth", "Leviatan", "Xylar", "Samhain", "Thor", "Kukulkan", "Nezareth"]
LUGAR = "Warps,60053.5,73,60059.5"
HORAS = list(range(0, 24, 2))                 # turnos de BOSSES (hora Peru/Colombia)
SIN_BOSS = {("Sun", 14): "MEGAKOTH"}          # turnos ocupados por otro evento
DESFASE_UTC = 5                               # Peru/Colombia = UTC-5, sin horario de verano

DIAS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
NOMBRE = {"Mon": "lunes", "Tue": "martes", "Wed": "miercoles", "Thu": "jueves",
          "Fri": "viernes", "Sat": "sabado", "Sun": "domingo"}


def a_utc(dia, hora):
    h = hora + DESFASE_UTC
    d = DIAS.index(dia)
    if h >= 24:
        h -= 24
        d = (d + 1) % 7
    return DIAS[d], h


def evento(dia, hora, boss):
    sdia, shora = a_utc(dia, hora)
    acciones = [f"console_command: mm mobs kill {b}" for b in ROTACION]
    if boss:
        acciones.append(f"console_command: mm mobs spawn {boss} 1 {LUGAR}")
    return {
        "type": "repetitive_server",
        "repetitive_time": 200,
        "conditions": [
            f"%server_time_E% == {sdia}",
            f"%server_time_HH:mm% == {shora:02d}:00",
            "%server_time_ss% < 10",
        ],
        "actions": {"default": acciones},
    }


def main():
    eventos, filas, i = {}, [], 0
    for dia in DIAS:
        for hora in HORAS:
            otro = SIN_BOSS.get((dia, hora))
            boss = None if otro else ROTACION[i % len(ROTACION)]
            if boss:
                i += 1
            nombre = f"bosses_{NOMBRE[dia]}_{hora:02d}00"
            eventos[nombre] = evento(dia, hora, boss)
            sdia, shora = a_utc(dia, hora)
            filas.append(f"#   {NOMBRE[dia]:<9} {hora:02d}:00  ->  servidor {sdia} {shora:02d}:00  ->  "
                         + (boss or f"solo retira al anterior ({otro})"))

    cabecera = (
        "# Rotacion de los bosses 10-17 (generado por tools/generate_ce_bosses.py; no lo edites a mano)\n"
        f"# Lugar: {LUGAR.replace(',', ' ')}\n"
        "# En cada turno se retira el boss anterior si sigue vivo y aparece el siguiente.\n"
        "#\n#   Peru/Colombia      ->  servidor (UTC)        ->  boss\n" + "\n".join(filas) + "\n\n"
    )
    texto = yaml.safe_dump({"Events": eventos}, sort_keys=False, allow_unicode=True, width=200)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(cabecera + texto, encoding="utf-8")
    assert len(yaml.safe_load(OUT.read_text(encoding="utf-8"))["Events"]) == len(DIAS) * len(HORAS)
    print(f"OK {OUT} ({len(eventos)} eventos, {i} apariciones)")


if __name__ == "__main__":
    main()
