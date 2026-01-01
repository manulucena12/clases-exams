from datetime import date, datetime
from typing import NamedTuple, DefaultDict
from csv import reader

Carrera = NamedTuple("Carrera", 
            [("nombre", str),
             ("escuderia", str),
             ("fecha_carrera", date) ,
             ("temperatura_min", int),
             ("vel_max", float),
             ("duracion",float),
             ("posicion_final", int),
             ("ciudad", str),
             ("top_6_vueltas", list[float]),
             ("tiempo_boxes",float),
             ("nivel_liquido", bool)
            ])

def lee_carreras(ruta_fichero:str, only: bool = False)->list[Carrera]:
    carreras = list()
    length = 0
    with open(ruta_fichero, encoding="utf-8") as f:
        lector = reader(f)
        next(lector)
        for r in lector:
            length +=1
            atributos = r[0].split(";")
            atributos[8] = atributos[8].replace("[","")
            atributos[8] = atributos[8].replace("]","")
            atributos[8] = atributos[8].replace("-","0")
            vueltas = atributos[8].split("/ ")
            vueltas = [float(v) for v in vueltas]
            carreras.append(Carrera(
                atributos[0],
                atributos[1],
                datetime.strptime(atributos[2], "%d-%m-%y").date(),
                int(atributos[3]),
                float(atributos[4]),
                float(atributos[5]),
                int(atributos[6]),
                atributos[7],
                vueltas,
                float(atributos[9]),
                False if atributos[10] == "no" else True
            ))
    if only:
        return carreras
    print(f"Total registros leídos: {length}. Mostrando los dos primeros registros:")
    print(carreras[0])
    print(carreras[1])
    return carreras

def media_tiempo_boxes(carreras:list[Carrera], ciudad:str, fecha:date | None =None)->float:
    suma = 0
    total = 0
    for c in carreras:
        if c.ciudad == ciudad and (fecha is None or c.fecha_carrera == fecha):
            suma += c.tiempo_boxes
            total +=1
    media = suma/total if total != 0 else 0
    print(f"La media de tiempo en boxes en la ciudad de {ciudad} es de {media} segundos.")
    return media

def pilotos_menor_tiempo_medio_vueltas_top(carreras:list[Carrera], n)->list[tuple[str,date]]:
    tiempos = list()
    for c in carreras:
        if 0 not in c.top_6_vueltas:
            tiempos.append((c.nombre, c.fecha_carrera, sum(c.top_6_vueltas)/6))
    top_n = [(x[0], x[1]) for x in sorted(tiempos, key=lambda x: x[2])[:n]]
    print(f"Los {n} pilotos con menor tiempo medio son {top_n}")
    return top_n

def ratio_tiempo_boxes_total(carreras:list[Carrera])->list[tuple[str,date, float]]:
    tiempos = DefaultDict(float)
    ratios = list()
    for c in carreras:
        tiempos[c.fecha_carrera]+=c.tiempo_boxes
    for c in carreras:
        ratios.append((c.nombre, c.fecha_carrera, round(c.tiempo_boxes/tiempos[c.fecha_carrera],3)))
    ratios_sorted = sorted(ratios, key=lambda x: x[2], reverse=True)
    print("Los ratios del tiempo en boxes son:")
    print(ratios_sorted)
    return ratios_sorted

def puntos_piloto_anyos(carreras:list[Carrera])-> dict[str,list]:
    puntos = DefaultDict(lambda: DefaultDict(int))
    for c in carreras:
        punto = 0
        if c.posicion_final == 1:
            punto = 50
        elif c.posicion_final == 2:
            punto = 25 
        elif c.posicion_final == 3:
            punto = 10
        puntos[c.nombre][c.fecha_carrera.year] += punto
    puntos = {p: list(puntos[p].values()) for p in puntos}
    print("Puntos por año de cada uno de los pilotos:")
    for p in puntos:
        print(f"{p} --> {puntos[p]}")
    return puntos

def mejor_escuderia_anyo(carreras:list[Carrera], anyo:int)->str:
    victorias = DefaultDict(int)
    for c in carreras:
        if c.fecha_carrera.year == anyo and c.posicion_final == 1:
            victorias[c.escuderia] += 1
    escuderia = max(victorias, key=lambda x: victorias[x])
    print(f"La mejor escudería en el año {anyo} ha sido {escuderia}.")
    return escuderia