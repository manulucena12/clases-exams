from typing import NamedTuple, DefaultDict
from datetime import time, date, datetime
import csv

Artista = NamedTuple("Artista",     
                        [("nombre", str), 
                        ("hora_comienzo", time), 
                        ("cache", int)])

Festival = NamedTuple("Festival", 
                        [("nombre", str),
                        ("fecha_comienzo", date),
                        ("fecha_fin", date),
                        ("estado", str),                      
                        ("precio", float),
                        ("entradas_vendidas", int),
                        ("artistas", list[Artista]),
                        ("top", bool)
                    ])

def lee_festivales (archivo:str, only=False)->list[Festival]:
    festivales = list()
    length = 0
    with open(archivo, encoding="utf-8") as f:
        lector = csv.reader(f)
        next(lector)
        for r in lector:
            length +=1
            artistas = list()
            for n in r[6].split(sep="-"):
                a = n.split("_")
                artistas.append(Artista(
                    a[0],
                    datetime.strptime(a[1], "%H:%M").time(),
                    int(a[2])
                ))
            festivales.append(Festival(
                r[0],
                datetime.strptime(r[1], "%Y-%m-%d").date(),
                datetime.strptime(r[2], "%Y-%m-%d").date(),
                r[3],
                float(r[4]),
                int(r[5]),
                artistas,
                True if r[7] == "sí" else False
            ))
    
    if only:
        return festivales
    print(f"Registros leídos: {length}")
    print("Los tres últimos")
    print(festivales[-1])
    print(festivales[-2])
    print(festivales[-3])
    return festivales

def total_facturado(festivales:list[Festival], fecha_ini:date|None=None, fecha_fin:date|None=None)->float:
    total = 0.0
    for f in festivales:
        if f.estado == "CELEBRADO" and f.fecha_comienzo>=(fecha_ini if fecha_ini is not None else date.min) and f.fecha_fin<=(fecha_fin if fecha_fin is not None else date.max):
            total += f.entradas_vendidas*f.precio
    print(f"Entre {fecha_ini} y {fecha_fin} el total es {total}")
    return total

def artista_top(festivales: list[Festival]) -> tuple[int, str]:
    reps = DefaultDict(int)
    for f in festivales:
        for a in f.artistas:
            reps[a.nombre] +=1
    top = max(reps, key=lambda x: reps[x])
    print(f"El artista que ha actuado en más festivales es {(reps[top], top)}")
    return reps[top], top

def mes_mayor_beneficio_medio(festivales: list[Festival]) -> str:
    revenue = DefaultDict(float)
    reps = DefaultDict(int)
    meses = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
    for f in festivales:
        revenue[f.fecha_comienzo.month] += f.entradas_vendidas - sum([a.cache for a in f.artistas])
        reps[f.fecha_comienzo.month] +=1
    medio = {mes: revenue[mes]/reps[mes] for mes in revenue.keys()}
    top_month = max(medio, key=lambda x: medio[x])
    print(f"El mes de mayor beneficio medio es: {meses[top_month]}")
    return meses[top_month]

def artistas_comunes(festivales: list[Festival], festi1: str, festi2:str) -> list[str]:
    artistas_1 = set()
    artistas_2 = set()
    for f in festivales:
        if f.nombre == festi1:
            artistas_1 = {a.nombre for a in f.artistas}
        elif f.nombre == festi2:
            artistas_2 = {a.nombre for a in f.artistas}
    comunes = list(artistas_1.intersection(artistas_2))
    print(f"Los artistas comunes entre {festi1} y {festi2} son: {comunes}")
    return comunes

def festivales_top_calidad_por_duracion(festivales: list[Festival], n: int=3) -> dict[int, list[str]]:
    festi_top = DefaultDict(list)
    festi_top2 = DefaultDict(list)
    for f in festivales:
        festi_top[(f.fecha_fin - f.fecha_comienzo).days].append((f.nombre, f.entradas_vendidas/len(f.artistas)))
    for f in festi_top.items():
        i = 0
        concerts = f[1]
        while i!=n:
            if len(concerts) == 0:
                break
            top = max(concerts, key=lambda x: x[1])
            festi_top2[f[0]].append(top[0])
            concerts.remove(top)
            i +=1
    print(f"Para n= {n}, los festivales top son:")
    for f in sorted(festi_top2.items(), key=lambda x: x[0]):
        print(f"{f[0]} --> {f[1]}")
    return festi_top2