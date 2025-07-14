import pygame
import heapq
import sys
from config import num_filas, num_columnas, modo_actual, celdas_config
from setup import setup
from botons import botones
from colores import colores


class Tablero:
    # Atributos de instancia:
    def __init__(self, num_columnas, num_filas):
        # Crear tablero:
        self.mapa = [[celdas_config["celda_libre"] for columna in range(num_columnas)] for fila in range(num_filas)]


    # Función de Imprimir Tablero:
    def mostrar_tablero(self, num_filas, num_columnas, modo_actual, fuente, tam_celda_x, tam_celda_y):
        for fila_indice in range(num_filas):
            for columna_indice in range(num_columnas):

                # Crea un rectangulo y ponle sus medidas:
                x = columna_indice * tam_celda_x
                y = fila_indice * tam_celda_y
                rectangulo = pygame.Rect(x, y, tam_celda_x, tam_celda_y)
                relleno = pygame.Rect(x + 4, y + 4, tam_celda_x - 8, tam_celda_y - 8)


                # Muestrame el rectangulo:
                if self.mapa[fila_indice][columna_indice] == celdas_config["celda_libre"]:
                    pygame.draw.rect(setup.screen, colores["GRIS"], rectangulo, 8) 
                elif self.mapa[fila_indice][columna_indice] == celdas_config["celda_obstaculo"]:
                    pygame.draw.rect(setup.screen, colores["NEGRO"], relleno)
                elif self.mapa[fila_indice][columna_indice] == celdas_config["celda_inicio"]:
                    pygame.draw.rect(setup.screen, colores["VERDE"], relleno)
                elif self.mapa[fila_indice][columna_indice] == celdas_config["celda_fin"]:
                    pygame.draw.rect(setup.screen, colores["ROJO"], relleno)
                elif self.mapa[fila_indice][columna_indice] == celdas_config["celda_ruta"]:
                    pygame.draw.rect(setup.screen, colores["AZUL"], relleno)
                elif self.mapa[fila_indice][columna_indice] == celdas_config["celda_jugador"]:
                    pygame.draw.rect(setup.screen, colores["COLOR_JUGADOR"], relleno)


        # Mostrar cuando el boton esta "clickeado" o "activo":
        for nombre, boton in botones.items():
            if nombre == modo_actual:
                pygame.draw.rect(setup.screen, colores["NEGRO"], boton.rect)  # Fondo negro para activo
                texto = setup.fuente.render(nombre.capitalize(), True, colores["BLANCO"])  # Texto blanco
            else:
                pygame.draw.rect(setup.screen, colores["BLANCO"], boton.rect)  # Fondo blanco para inactivo
                texto = setup.fuente.render(nombre.capitalize(), True, colores["NEGRO"])  # Texto negro

            pygame.draw.rect(setup.screen, colores["NEGRO"], boton.rect, 2)  # Borde negro siempre
            texto_rect = texto.get_rect(center=boton.rect.center)
            setup.screen.blit(texto, texto_rect)


# Creamos nuestro objeto Tablero:
tablero = Tablero(num_columnas, num_filas)


# Definimos nuestra función que calcula la distancia Manhattan:
def distancia_manhattan_heuristica(primera_x, segunda_x, primera_y, segunda_y):
    return abs(primera_x - segunda_x) + abs(primera_y - segunda_y)


class A_estrella:
    def __init__(self, entrada, salida):
        # Le damos las coordenadas al algoritmo:
        self.x1 = entrada[0]
        self.y1 = entrada[1]
        self.x2 = salida[0]
        self.y2 = salida[1]

        self.movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, abajo, izquierda, derecha

        # Creamos una lista vacía llamada cola, que será usada como heap/cola de prioridad.
        self.cola = []

        # set(): lista que no se puede repetir elementos.
        self.visitados = set()

        self.mejor_g = dict()


        # Formula general de A*: f = g + h
        # "g" es igual a el costo (en este caso, distancia) que nos llevó moverse desde el principio hasta ese punto.
        # "h" (heuristica) es el costo de la casilla actual hasta la meta.
        # "f" es la suma de 'g' y 'h'

        # Calculamos la heurística (h) desde la entrada hasta la salida.
        self.heuristica = distancia_manhattan_heuristica(self.x1, self.x2, self.y1, self.y2)


        heapq.heappush(self.cola, (self.heuristica, 0, (self.x1, self.y1), [(self.x1, self.y1)]))
        # Hey, agrega esta celda inicial (x1, y1) a la cola de prioridad, con:
        
            # "f = heurística (porque g = 0 al principio),"

            # "g = 0 (no he caminado nada aún),"

            # "su posición actual (x1, y1),"

            # "y su camino recorrido hasta ahora: solo ella misma [(x1, y1)]."

        # Además, ordena automáticamente la cola de forma que la celda con menor f quede siempre al frente.”

    def mostrar_camino(self,  mapa, tam_celda_x, tam_celda_y, num_filas, num_columnas):
        while self.cola:
            f, g, (x, y), camino = heapq.heappop(self.cola)
            # Saca el nodo con menor 'f' (puntaje) de la cola

            # Marcar la celda actual como visitada (para mostrar el progreso)
            if mapa[x][y] == celdas_config["celda_libre"]:
                mapa[x][y] = celdas_config["celda_ruta"]

            # Pausa para mostrar el progreso paso a paso
            pygame.time.wait(200)  # Pausa entre cada paso

            # Permitir interacción durante el algoritmo
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Permitir modificar el mapa durante la ejecución
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x_mouse, y_mouse = pygame.mouse.get_pos()
                    fila_click = y_mouse // tam_celda_y
                    columna_click = x_mouse // tam_celda_x
                    
                    # Solo permitir agregar/quitar obstáculos
                    if (0 <= fila_click < num_filas and 0 <= columna_click < num_columnas and
                        mapa[fila_click][columna_click] != celdas_config["celda_inicio"] and mapa[fila_click][columna_click] != celdas_config["celda_fin"]):
                        
                        if mapa[fila_click][columna_click] == celdas_config["celda_libre"]:
                            mapa[fila_click][columna_click] = celdas_config["celda_obstaculo"]
                        elif mapa[fila_click][columna_click] == celdas_config["celda_obstaculo"]:
                            mapa[fila_click][columna_click] = celdas_config["celda_libre"]

            # Actualizar pantalla para mostrar el progreso
            setup.screen.fill("gray")
            tablero.mostrar_tablero(num_filas, num_columnas, modo_actual, setup.fuente, tam_celda_x, tam_celda_y)
            pygame.display.flip()
            setup.clock.tick(60)

            # Si llegamos a la salida, terminamos
            if (x, y) == (self.x2, self.y2):
                for px, py in camino:
                    if mapa[px][py] == celdas_config["celda_ruta"]:
                        mapa[px][py] = celdas_config["celda_jugador"]
                print("")
                print(f"🎯 Camino encontrado! Tiempo estimado: {len(camino)}0 min.")
                return camino  # Camino encontrado
            

            # Marcamos como visitado
            self.visitados.add((x, y))

            # Revisamos vecinos
            for dx, dy in self.movimientos:
                nueva_x, nueva_y = x + dx, y + dy
                if (0 <= nueva_x < num_filas and 0 <= nueva_y < num_columnas and
                        mapa[nueva_x][nueva_y] != celdas_config["celda_obstaculo"]) and (nueva_x, nueva_y) not in self.visitados:
                        # Esta condición también evita que las coordenadas (x, y) no se repitan, porque sino volverian al punto de entrada siempre. 
                        
                        # Caminamos 1 paso más:
                        nuevo_g = g + 1

                        # Guardamos la posición:
                        nueva_pos = (nueva_x, nueva_y)

                        # Si ya visitamos esta posición con un mejor g, la descartamos
                        if nueva_pos in self.mejor_g and nuevo_g >= self.mejor_g[nueva_pos]:
                            continue

                        # Guardamos el nuevo mejor g
                        self.mejor_g[nueva_pos] = nuevo_g

                        # Calculamos la heuristica actual:
                        nueva_h = distancia_manhattan_heuristica(nueva_x, self.x2, nueva_y, self.y2)

                        # Hacemos el calculo de f:
                        nuevo_f = nuevo_g + nueva_h
                        
                        # Agregamos a la cola el nuevo atributo:
                        heapq.heappush(self.cola, (nuevo_f, nuevo_g, (nueva_x, nueva_y), camino + [(nueva_x, nueva_y)]))


        # No se encontró camino
        print("")
        print("No hay camino posible")
        return None  # No se encontró camino.