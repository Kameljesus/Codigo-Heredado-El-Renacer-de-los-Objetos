import pygame
import sys
from config import num_filas, num_columnas, modo_actual, celdas_config, tam_celda_x, tam_celda_y
from setup import setup
from botons import botones
from tablero_y_algoritmo import tablero, A_estrella

# Con from 'archivo' import *. Importa todo lo que hay en el file.

'''

Este módulo forma parte de la biblioteca estándar de Python, y se usa principalmente para controlar el sistema de ejecución del programa.
¿Qué cosas útiles tiene sys?

    sys.exit(): 💥 Termina completamente el programa. Sin sys.exit(), el programa puede quedar "colgado" en memoria después de cerrar la ventana de Pygame.

    sys.argv: 📦 Accede a argumentos pasados por consola.

    sys.path: 📂 Ve las rutas de búsqueda de módulos.

'''


# Activamos pygame:
pygame.init()


while setup.running:
    # Obten todo los eventos que sucedan en cada frame
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            setup.running = False # Este es mi break


        # Significa: “si se presionó el botón del mouse (cualquier clic)”.
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()


            # Verificar si se clickeó algún botón
            boton_clickeado = False
            for nombre_boton, boton in botones.items():
                if boton.rect.collidepoint(x_mouse, y_mouse):
                    boton_clickeado = True

                    # Detectar si hizo clic en reset
                    if nombre_boton == "reset":
                        # Limpiar todo el tablero
                        tablero.mapa = [[celdas_config["celda_libre"] for columna in range(num_columnas)] for fila in range(num_filas)]
                        # Resetear coordenadas de entrada y salida
                        entrada = (None, None)
                        salida = (None, None)
                        print("")
                        print("🧹 Tablero limpiado completamente.")


                    # Detectar si hizo clic en algoritmo o juego_manual
                    elif nombre_boton == "algoritmo" or nombre_boton == "manual":
                        # Verificar que la entrada y salida estén definidas
                        if (entrada[0] is not None and entrada[1] is not None and
                            salida[0] is not None and salida[1] is not None):

                            if nombre_boton == "algoritmo":
                                # Creamos la clase algoritmo:
                                algoritmo = A_estrella(entrada, salida)
                                
                                # Aquí se llamará la función de resolución automática:
                                resultado = algoritmo.mostrar_camino(tablero.mapa, tam_celda_x, tam_celda_y, num_filas, num_columnas)  
                                
                                if resultado:
                                    # Mostrar resultado por 5 segundos
                                    inicio_tiempo = pygame.time.get_ticks()
                                    while pygame.time.get_ticks() - inicio_tiempo < 5000:
                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                pygame.quit()
                                                sys.exit()
                                        setup.screen.fill("gray")
                                        tablero.mostrar_tablero(num_filas, num_columnas, modo_actual, setup.fuente, tam_celda_x, tam_celda_y)
                                        pygame.display.flip()
                                        setup.clock.tick(60)
  

                        else:
                            print("")
                            print("⚠️ Primero debes definir la entrada y la salida.")
                        
                    else:
                        # Cambiar modo para otros botones
                        modo_actual = nombre_boton

                    break  


            # "Si no clickeaste en botón, entonces clickeaste en el tablero":
            if not boton_clickeado:
                fila = y_mouse // tam_celda_y
                columna = x_mouse // tam_celda_x
                

                # Esto permite que puedas poner y quitar con clicks los elementos de modo:
                if 0 <= fila < num_filas and 0 <= columna < num_columnas:
                    if modo_actual == "obstaculo":
                        if tablero.mapa[fila][columna] == celdas_config["celda_libre"]:
                            tablero.mapa[fila][columna] = celdas_config["celda_obstaculo"]
                        elif tablero.mapa[fila][columna] == celdas_config["celda_obstaculo"]:
                            tablero.mapa[fila][columna] = celdas_config["celda_libre"]

                    elif modo_actual == "entrada":
                        # Limpiar entrada previa
                        for f in range(num_filas):
                            for c in range(num_columnas):
                                if tablero.mapa[f][c] == celdas_config["celda_inicio"]:
                                    tablero.mapa[f][c] = celdas_config["celda_libre"]
                        tablero.mapa[fila][columna] = celdas_config["celda_inicio"]
                        # Definimos las coordenadas para cualquiera de las dos funciones:
                        entrada = (fila, columna)


                    elif modo_actual == "salida":
                        # Limpiar salida previa
                        for f in range(num_filas):
                            for c in range(num_columnas):
                                if tablero.mapa[f][c] == celdas_config["celda_fin"]:
                                    tablero.mapa[f][c] = celdas_config["celda_libre"]
                        tablero.mapa[fila][columna] = celdas_config["celda_fin"]
                        # Definimos las coordenadas para cualquiera de las dos funciones:
                        salida = (fila, columna)

    
    setup.screen.fill("gray") # Esto es el fondo de mi pantalla
    tablero.mostrar_tablero(num_filas, num_columnas, modo_actual, setup.fuente, tam_celda_x, tam_celda_y)


    pygame.display.flip() # Permite mostrar en pantalla lo que se actualiza. Pygame no dibuja en la ventana automáticamente. Primero dibuja en memoria, y cuando hacés display.flip(), muestra todo eso en la pantalla de golpe.
    setup.clock.tick(60) # Esta es la velocidad que quiero a la que vaya mi programa.

pygame.quit()
sys.exit()
