#Solicitud de ancho y alto al usuario:
num_filas = int(input("Elija cuantas filas quiere en su laberinto: "))
num_columnas = int(input("Elija cuantas columnas quiere de su laberinto: "))


# Definimos con cuál boton estará activo al comenzar nuestro programa:
modo_actual = 'obstaculo'


# Configuracion de pantalla:
configuracion = {
    "ancho_de_pantalla": 800,
    "alto_de_pantalla": 800,

    "ancho_de_tablero": 640,
    "alto_de_tablero": 640,
}


# Configuración de celdas:
celdas_config = {
    "celda_libre": 0,
    "celda_obstaculo": 1,
    "celda_inicio": 2,
    "celda_fin": 3,
    "celda_ruta": 4,
    "celda_jugador": 5
}


# Configuracion de la clase celda:
class Celda:
    def __init__(self, num_filas, num_columnas):
        # Reservamos espacio para botones (160px de ancho + 20px de margen)
        espacio_botones = 180
        
        # Calculamos ambos posibles tamaños (ancho/columnas y alto/filas)
        self.tam_celda_x_posible = (configuracion["ancho_de_pantalla"] - espacio_botones) // num_columnas
        self.tam_celda_y_posible = configuracion["alto_de_pantalla"] // num_filas

        # Elegimos el mínimo para que la celda sea cuadrada quepa del tablero
        self.tam_celda = min(self.tam_celda_x_posible, self.tam_celda_y_posible)

        # Definimos el ancho y alto de la celda igual al tamaño cuadrado
        self.tam_celda_x = self.tam_celda
        self.tam_celda_y = self.tam_celda


# Creamos nuestro objeto y variables de Celdas:
celda_instancia = Celda(num_filas, num_columnas)
tam_celda_x = celda_instancia.tam_celda_x
tam_celda_y = celda_instancia.tam_celda_y


# Calculamos el ancho real del tablero basado en el tamaño de celdas
ancho_real_tablero = num_columnas * tam_celda_x

# Posición X donde empiezan los botones (justo a la derecha del tablero real):
configuracion["botones_x"] = ancho_real_tablero + 20