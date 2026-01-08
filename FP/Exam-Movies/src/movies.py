from collections import namedtuple, defaultdict
from csv import reader
from datetime import datetime

Pelicula = namedtuple('Pelicula', ['id', 'title', 'original_language', 
'release_date', 'vote_average', 'popularity', 'adult', 'genres']) 

def parsea_generos(fichero2):
    generos = defaultdict(set)
    with open(fichero2, encoding="utf-8") as f:
        lector = reader(f, delimiter=":")
        next(lector)
        for r in lector:
            for g in r[1].split(","):
                generos[r[0]].add(g)
    return generos

def leer_peliculas(fichero1, fichero2, only=False):
    peliculas = list()
    generos = parsea_generos(fichero2)
    length = 0
    with open(fichero1, encoding="utf-8") as f:
        lector = reader(f)
        next(lector)
        for r in lector:
            length += 1
            peliculas.append(Pelicula(
                int(r[0]),
                r[1],
                r[2],
                datetime.strptime(r[3], "%Y-%m-%d").date(),
                float(r[4]),
                int(r[5]),
                bool(r[6]),
                generos[r[0]]
            ))
    if only:
        return peliculas
    print(length)
    print(f"Primera {peliculas[0]}")
    print(f"Última {peliculas[-1]}")
    return peliculas

def genero_mas_frecuente(peliculas):
    repes = defaultdict(int)
    for p in peliculas:
        for g in p.genres:
            repes[g]+=1
    mayor = max(repes, key=lambda x: repes[x])
    print(f"El género más frecuente es {(mayor, repes[mayor])}")
    return mayor, repes[mayor]

def mejor_valorada_por_idioma(peliculas, idioma="es"): 
    idiomas = {"es": "Español", "en": "Inglés", "it": "Italiano", "ru": "Ruso"}
    mejores = defaultdict(Pelicula)
    for p in peliculas:
        if p.original_language not in mejores or (mejores[p.original_language].popularity < p.popularity):
            mejores[p.original_language] = p
        elif mejores[p.original_language].popularity == p.popularity:
            mejores[p.original_language] = p if p.vote_average>mejores[p.original_language] else mejores[p.original_language]
    print(f"Mejor en {idiomas[idioma]} ({idioma}) es {mejores[idioma]}")
    return

def media_calificaciones(peliculas, generos):
    votes = 0
    total = 0
    for p in peliculas:
        if len(p.genres.intersection(generos)) != 0:
            votes += p.vote_average
            total +=1
    media = round(votes/total, 3)
    print(generos)
    print(media)
    return media

def top_n_por_genero(peliculas, n):
    compilation = defaultdict(list)
    for p in peliculas:
        for g in p.genres:
            compilation[g].append(p)
    top_n = defaultdict(list)
    for g,p in compilation.items():
        peliculas = p
        for i in range(n):
            if len(peliculas) != 0:
                mejor = max(peliculas, key=lambda x: x.vote_average)
                top_n[g].append(mejor)
                peliculas.remove(mejor)
    for g,p in top_n.items():
        print(f"Top {n}{g}:")
        print(p)
    return