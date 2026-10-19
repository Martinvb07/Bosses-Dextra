# Notas e ideas pendientes

## Ideas que se pueden hacer

### Que el boss no se salga de su zona ("correa")
Si se puede con MythicMobs. Una skill que cada 2 s mira si el boss se alejo del punto de aparicion y,
si se paso del radio, lo teletransporta de vuelta. Como los bosses 10-17 salen todos en el mismo punto
(Warps 60053.5 73 60059.5), sirve una sola skill para los 8:

```yaml
Bosses_Correa:
  Conditions:
  - distancefromlocation{x=60053.5;y=73;z=60059.5;world=Warps;distance=>30}   # 30 = radio en bloques
  Skills:
  - effect:particles{particle=PORTAL;amount=40;hS=0.5;vS=1} @self
  - teleport @Location{x=60053.5;y=73;z=60059.5;world=Warps}
```

En cada boss, dentro de `Skills:`:
```yaml
- skill{s=Bosses_Correa} @self ~onTimer:40
```

Con WorldGuard tambien se puede por region en vez de por radio (condicion `inregion`).
Falta decidir: radio en bloques (o nombre de la region).

## Pendiente de decidir

- **Armaduras duplicadas:** Forjado, Corrupto y Olimpico estan en `Items/Armaduras_Set.yml` y en
  `Items/Herramientas_Set.yml` con niveles distintos (p. ej. Forjado proteccion 12 vs 10, Olimpico 20 vs 25).
  Hay que elegir cual se queda.
- **Sacos de ranking (bosses 10-17):** si se cambia lo que da cada puesto (Top 1/2/3/Participante).
  Kronos usa llaves de Usuario/DexParty de Oneblock.
- **Xylar** suelta las recompensas de los bosses de spawn y la estrella de invocacion de Ragnarok
  (copiado de Red Hand); los demas bosses 10-17 solo dan sus sacos.
- **Midas y Escarabajo** sueltan lapis ademas de las runas.
- **Oro Sagrado / monedas de plata en el KOTH de la mazmorra:** no salen de MythicMobs; estan en la
  config del plugin de KOTH.

## Por comprobar en el servidor

- `mm mobs kill <Boss>` (lo usa la rotacion de ConditionalEvents para retirar al boss si nadie lo mato en
  2 h): comprobar que no da recompensas ni manda el mensaje de "ha caido". Si lo hace, cambiarlo por una
  retirada sin recompensas.
