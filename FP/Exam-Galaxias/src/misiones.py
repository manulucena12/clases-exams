from typing import NamedTuple, DefaultDict
from datetime import date,datetime 
from csv import reader

Mision = NamedTuple("Mision", [ 
    ("comandante", str), 
    ("sistema", str), 
    ("controlado", bool), 
    ("fecha_inicio", date), 
    ("fecha_fin", date | None), 
    ("tipo_mision", str), 
    ("num_unidades", int), 
    ("coste_mensual", float), 
    ("recursos", list[str]) 
])

def parsea_recursos(atributo:str) -> list[str]:
    recursos = list()
    for r in atributo.split("#"):
        recursos.append(r)
    return recursos

def lee_misiones(ruta_fichero: str, only:bool = False) -> list[Mision]:
    misiones = list()
    length = 0
    with open(ruta_fichero, encoding="utf-8") as f:
        lector = reader(f, delimiter=";")
        next(lector)
        for atributos in lector:
            length +=1
            misiones.append(Mision(
                atributos[0],
                atributos[1],
                True if atributos[2]=="Sí" else False,
                datetime.strptime(atributos[3], "%Y-%m-%d").date(),
                datetime.strptime(atributos[4], "%Y-%m-%d").date() if atributos[4] != "" else None,
                atributos[5],
                int(atributos[6]),
                float(atributos[7]),
                parsea_recursos(atributos[8])
            ))
    if only:
        return misiones
    print(f"Total de misiones leídas: {length}")
    print(f"Primeras 3 Misiones:")
    print(misiones[0])
    print(misiones[1])
    print(misiones[2])
    return misiones

def comandante_ocioso(misiones: list[Mision]) -> str: 
    periodos = list()
    for m in misiones:
        if m.fecha_fin is not None:
            comandante, fecha = m.comandante, m.fecha_fin
            for resto in misiones:
                if resto.comandante == comandante and resto.fecha_inicio>fecha:
                    periodos.append((comandante, (resto.fecha_inicio-fecha).days))
    ocioso = max(periodos, key=lambda x: x[1])
    print(f"Comandante más ocioso: {ocioso[0]}")
    return ocioso[0]

def comandante_mas_activo_por_mes(misiones: list[Mision]) -> dict[tuple[int, int], str]:
    actividad = DefaultDict(lambda: DefaultDict(int))
    for m in misiones:
        combo = (m.fecha_inicio.year, m.fecha_inicio.month)
        actividad[combo][m.comandante] =+1
    activos = dict()
    print("Comandantes más activos por cada mes")
    for fecha in sorted(actividad):
        activo = max(actividad[fecha], key=lambda x: actividad[fecha][x])
        activos[fecha] = activo
        print(f"{fecha[0]}-{"0" + str(fecha[1]) if fecha[1]<10 else fecha[1]}: {activo}")
    return activos

def coste_de_recursos(misiones: list[Mision], n: int = 3) -> list[tuple[str, float]]:
    costes = DefaultDict(float)
    reps = DefaultDict(int)
    for m in misiones:
        for r in m.recursos:
            costes[r] += m.coste_mensual
            reps[r] += 1
    coste_medio = {r: round(costes[r]/reps[r],2) for r in costes}
    costosos = sorted(coste_medio, key=lambda x: coste_medio[x], reverse=True)[:n]
    costosos = [(c, coste_medio[c]) for c in costosos]
    print("Recursos más costosos en media:")
    for r,c  in costosos:
        print(f"{r}: {c}")
    return costosos

def estadisticas_sistemas_rebeldes(misiones: list[Mision], tipo_mision: str | None = None) -> list[tuple[str, int, float]]:
    dias = DefaultDict(int)
    tropas = DefaultDict(int)
    reps = DefaultDict(int)
    for m in misiones:
        if m.controlado is False and (tipo_mision is None or m.tipo_mision == tipo_mision) and m.fecha_fin is not None:
            dias[m.sistema] += (m.fecha_fin-m.fecha_inicio).days
            tropas[m.sistema] += m.num_unidades
            reps[m.sistema] += 1
    estadisticas = [(s,dias[s], round(tropas[s]/reps[s],2)) for s in dias]
    print(f"Estadísticas de sistemas rebeldes (solo '{tipo_mision}')")
    for s,d,t in estadisticas:
        print(f"{s}: {d} días, {t} unidades")
    return estadisticas

def recursos_por_tipo(misiones: list[Mision]) -> dict[str: dict[str:int]]: 
    recursos = DefaultDict(lambda: DefaultDict(int))
    for m in misiones:
        if m.fecha_fin is not None:
            for r in m.recursos:
                recursos[m.tipo_mision][r]+=1
    for m,r in recursos.items():
        print(f"{m}: {dict(r)}")
    return recursos