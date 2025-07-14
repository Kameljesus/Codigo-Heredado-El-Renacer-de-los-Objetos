import pygame # Importa pygame (obviamente)
from config import configuracion

# Creamos nuestras clases y objetos necesarios:
class Boton:
    def __init__(self, nombre_del_boton, posicion_eje_x, posicion_eje_y, ancho_del_boton, alto_del_boton):
        # Atributos de instancia (Todo lo que estás asignando con self. dentro del método __init__ son atributos de instancia.):
        self.nombre_del_boton = nombre_del_boton
        self.posicion_eje_x = posicion_eje_x
        self.posicion_eje_y = posicion_eje_y
        self.ancho_del_boton = ancho_del_boton
        self.alto_del_boton = alto_del_boton

        self.rect = pygame.Rect(posicion_eje_x, posicion_eje_y, ancho_del_boton, alto_del_boton)


# Diccionario que guarda cada botón con su posición y tamaño:
botones = {
    "obstaculo": Boton("obstaculo", configuracion["botones_x"], 50, 120, 40),
    "entrada": Boton("entrada", configuracion["botones_x"], 110, 120, 40),
    "salida": Boton("salida", configuracion["botones_x"], 170, 120, 40),
    "algoritmo": Boton("algoritmo", configuracion["botones_x"], 230, 120, 40),
    "reset": Boton("reset", configuracion["botones_x"], 290, 120, 40)

    # botones_x: posición horizontal (eje X) donde empieza el botón, en píxeles desde la izquierda de la ventana.
    # 230: posición vertical (eje Y) donde empieza el botón, en píxeles desde arriba.
    # 120: ancho del botón, en píxeles.
    # 40: alto del botón, en píxeles.
}