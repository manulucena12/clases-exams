from typing import NamedTuple
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


def paso1(ruta_fichero: str, only:bool = False) -> list[Mision]:
    # Como nos piden una lista de misiones, inicializamos una variable lista vacía para rellenar
    misiones = list()

    with open(ruta_fichero, encoding="utf-8") as f:
        # Debido a que los atributos vienen separados por punto y coma, debemos decirle al delimiter que separe de esa forma los datos
        lector = reader(f, delimiter=";")
        # Nos saltamos la cabecera
        next(lector)
        for atributos in lector:
            print(atributos)
            # Este break es temporal, solo ayuda a la legibilidad para la manipulación de datos
            break    

def paso2(ruta_fichero: str, only:bool = False) -> list[Mision]:
    # Como nos piden una lista de misiones, inicializamos una variable lista vacía para rellenar
    misiones = list()

    with open(ruta_fichero, encoding="utf-8") as f:
        # Debido a que los atributos vienen separados por punto y coma, debemos decirle al delimiter que separe de esa forma los datos
        lector = reader(f, delimiter=";")
        # Nos saltamos la cabecera
        next(lector)
        for atributos in lector:
            # Parseamos todos los datos al formato solicitado y añadimos misiónº
            misiones.append(Mision(
                atributos[0],
                atributos[1],
                True if atributos[2]== "Sí" else False,
                datetime.strptime(atributos[3], "%Y-%m-%d").date(),
                datetime.strptime(atributos[4], "%Y-%m-%d").date() if atributos[4] != "" else None,
                atributos[5],
                int(atributos[6]),
                float(atributos[7]),
                "Dejamos este atributo para el paso 3"
            ))
            # Este break es temporal, solo ayuda a la legibilidad para la manipulación de datos
            break    

def parsea_recursos(atributo:str) -> list[str]:
    # Si el último atributo es una lista, usamos una función auxiliar
    recursos = list()
    # Usamos split ya que el tipo de este dato es un string, no reader, con # como delimiter ahorad
    for r in atributo.split("#"):
        recursos.append(r)
    return recursos

def paso3(ruta_fichero: str, only:bool = False) -> list[Mision]:
    # Como nos piden una lista de misiones, inicializamos una variable lista vacía para rellenar
    misiones = list()

    with open(ruta_fichero, encoding="utf-8") as f:
        # Debido a que los atributos vienen separados por punto y coma, debemos decirle al delimiter que separe de esa forma los datos
        lector = reader(f, delimiter=";")
        # Nos saltamos la cabecera
        next(lector)
        for atributos in lector:
            # Parseamos todos los datos al formato solicitado y añadimos misiónº
            misiones.append(Mision(
                atributos[0],
                atributos[1],
                True if atributos[2]== "Sí" else False,
                datetime.strptime(atributos[3], "%Y-%m-%d").date(),
                datetime.strptime(atributos[4], "%Y-%m-%d").date() if atributos[4] != "" else None,
                atributos[5],
                int(atributos[6]),
                float(atributos[7]),
                parsea_recursos(atributos[8])
            ))
            # Este break es temporal, solo ayuda a la legibilidad para la manipulación de datos
            break    


def lee_misiones(ruta_fichero: str, only:bool = False) -> list[Mision]:
    misiones = list()
    with open(ruta_fichero, encoding="utf-8") as f:
        lector = reader(f, delimiter=";")
        next(lector)
        for atributos in lector:
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
    print(f"Total de misiones leídas: {len(misiones)}")
    print(f"Primeras 3 Misiones:")
    print(misiones[0])
    print(misiones[1])
    print(misiones[2])
    return misiones