from mayday import *

fichero = "../data/mayday.csv"

#lee_desastres(fichero)
#desastres_con_fallecidos_en_tierra(lee_desastres(fichero, only=True), 5)
#decada_mas_colisiones(lee_desastres(fichero, only=True))
#mayor_periodo_sin_desastres(lee_desastres(fichero, only=True))
#mayor_periodo_sin_desastres(lee_desastres(fichero, only=True), "Taking-off")
#mayor_periodo_sin_desastres(lee_desastres(fichero, only=True), "Landing")
#estadisticas_por_operacion(lee_desastres(fichero, only=True))
estadisticas_por_operacion(lee_desastres(fichero, only=True), 0.15)
