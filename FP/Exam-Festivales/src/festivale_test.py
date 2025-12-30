from festivales import lee_festivales, total_facturado, artista_top, mes_mayor_beneficio_medio, artistas_comunes, festivales_top_calidad_por_duracion
from datetime import datetime

fichero = "../data/festivales.csv"

#lee_festivales(fichero)
#total_facturado(lee_festivales(fichero, True), None, None)
#total_facturado(lee_festivales(fichero, True), None, datetime.strptime("2024-06-15", "%Y-%m-%d").date())
#total_facturado(lee_festivales(fichero, True), datetime.strptime("2024-06-15", "%Y-%m-%d").date(), None)
#total_facturado(lee_festivales(fichero, True), datetime.strptime("2024-06-01", "%Y-%m-%d").date(), datetime.strptime("2024-06-15", "%Y-%m-%d").date())
#artista_top(lee_festivales(fichero, True))
#mes_mayor_beneficio_medio(lee_festivales(fichero, True))
#artistas_comunes(lee_festivales(fichero, True), "Creamfields", "Tomorrowland")
#artistas_comunes(lee_festivales(fichero, True), "Primavera Sound", "Coachella")
#artistas_comunes(lee_festivales(fichero, True), "Iconica Fest", "Primavera Sound")
#festivales_top_calidad_por_duracion(lee_festivales(fichero, True), 1)
#festivales_top_calidad_por_duracion(lee_festivales(fichero, True), 4)