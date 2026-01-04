from typing import NamedTuple, DefaultDict
from datetime import datetime, date, time 
from csv import reader
 
Vuelo = NamedTuple("Vuelo",      
  [("operador", str), # Compañía aérea que operaba el vuelo (opcional) 
   ("codigo", str),   # Código de vuelo (opcional) 
   ("ruta", str),     # Ruta del vuelo (opcional) 
   ("modelo", str)])  # Modelo de avión que operaba el vuelo (opcional) 
 
Desastre = NamedTuple("Desastre",      
  [("fecha", date),               # Fecha del desastre aéreo 
    ("hora", time | None),        # Hora del desastre (opcional) 
    ("localizacion", str),        # Localización del desastre 
    ("supervivientes",int),       # Supervivientes 
    ("fallecidos",int),           # Fallecidos     
    ("fallecidos_en_tierra",int), # Fallecidos en tierra (no eran pasajeros del vuelo) 
    ("operacion",str),        # Momento operativo del vuelo cuando ocurrió el desastre 
    ("vuelos", list[Vuelo])]) # Vuelos implicados en el desastre

def parsea_vuelos(d: list[str]):
    vuelos = list()
    if "/" in d[3]:
        for a,b,c,d in zip(d[3].split("/"), d[4].split("/"), d[5].split("/"), d[6].split("/")):
            vuelos.append(Vuelo(a, "Unavailable" if (b == "" or b == " ") else b, c, d))
    else:
        vuelos.append(Vuelo(d[3], "Unavailable" if (d[4] == "" or d[4] == " ") else d[4], d[5], d[6]))
    return vuelos

def lee_desastres(ruta:str, only:bool = False)->list[Desastre]:
    desastres =  list()
    lenght = 0
    with open(ruta, encoding="utf-8") as f:
        lector = reader(f, delimiter=";")
        next(lector)
        for d in lector:
            lenght+=1
            desastres.append(Desastre(
                datetime.strptime(d[0], "%d/%m/%Y").date(),
                datetime.strptime(d[1], "%H:%M").time() if d[1] != "" else None,
                d[2],
                int(d[7]),
                int(d[8]),
                int(d[9]),
                d[10],
                parsea_vuelos(d)
            ))
    if only:
        return desastres
    else:
        print(f"Número de desastres leídos: {lenght}")
        print("Los dos primeros son:")
        print(desastres[0])
        print(desastres[1])
        print("Los dos últimos son:")
        print(desastres[-2])
        print(desastres[-1])
        return desastres
    
def desastres_con_fallecidos_en_tierra(desastres:list[Desastre],n:int|None=None) ->list[tuple[str,date,time,int]]:
    tierra = list()
    for d in desastres:
        if d.fallecidos_en_tierra != 0:
            tierra.append((d.localizacion, d.fecha, d.hora, d.fallecidos_en_tierra))
    tierra = sorted(tierra, key=lambda x: x[3], reverse=True)
    if n is not None:
        print(f"Los {n} desastres con más fallecidos en tierra son: ")
        for x in range(n):
            print(tierra[x])
    return tierra

def decada_mas_colisiones(desastres:list[Desastre]) -> tuple[int,int]:
    numeros = DefaultDict(int)
    for d in desastres:
        decada = int("19" + str(d.fecha.year)[2] + "0" if str(d.fecha.year)[2] != "0" else "2000")
        numeros[decada] += 1
    mayor = (max(numeros, key=lambda x: numeros[x]), numeros[max(numeros, key=lambda x: numeros[x])])
    print(f"La década de {mayor[0]} fue la peor, con {mayor[1]} desastres con colisiones de aeronaves. ")
    return mayor

def mayor_periodo_sin_desastres(desastres:list[Desastre], operacion:str|None=None)-> tuple[date, date, int]:
    dias = dict()
    for d1,d2 in zip(desastres, desastres[1:]):
        if operacion is None:
            dias[(d1.fecha, d2.fecha)] = (d2.fecha-d1.fecha).days
        elif d1.operacion == operacion:
            fecha = d1.fecha
            for x in desastres[desastres.index(d1)+1:]:
                if x.operacion == operacion:
                    fecha = x.fecha
                    break
            dias[(d1.fecha, fecha)] = (fecha - d1.fecha).days
    mayor = max(dias, key=lambda x: dias[x])
    mayor = (mayor[0], mayor[1], dias[mayor])
    print(f"El mayor periodo sin desastres {"durante la operación " + operacion if operacion is not None else ""} comienza el {mayor[0]}, termina el {mayor[1]} y dura {mayor[2]} días.")
    return mayor

def estadisticas_por_operacion(desastres: list[Desastre], limite_tasa_supervivencia:float|None=None) ->dict[str,tuple[int,float,float]]:
    repes = DefaultDict(int)
    sur = DefaultDict(float)
    fall = DefaultDict(float)
    for d in desastres:
        tasa_supervivencia = (d.supervivientes)/(d.supervivientes+d.fallecidos)
        if True if limite_tasa_supervivencia is None else tasa_supervivencia <= limite_tasa_supervivencia:
            repes[d.operacion] +=1
            sur[d.operacion] += d.supervivientes
            fall[d.operacion] += d.fallecidos 
    ratios = {operacion: (repes[operacion], sur[operacion]/repes[operacion], fall[operacion]/repes[operacion]) for operacion in repes}
    print(f"Las estadísticas por operación {"con tasa de supervivencia menor a " + str(limite_tasa_supervivencia) if limite_tasa_supervivencia is not None else ""} son: ")
    for n,r in ratios.items():
        print(f"{n}, {r}")
    return ratios