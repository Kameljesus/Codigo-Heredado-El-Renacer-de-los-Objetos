import pygame # Importa pygame (obviamente)
from config import configuracion

# Activamos pygame:
pygame.init()

#Setup básico de pygame:
class Setup:
    def __init__(self):
        self.ancho_setup = configuracion["ancho_de_pantalla"]
        self.alto_setup = configuracion["alto_de_pantalla"]

        # Fuente para el texto de los botones (definida globalmente):
        self.fuente = pygame.font.SysFont("Arial", 24)

        self.screen = pygame.display.set_mode((self.ancho_setup, self.alto_setup))
        pygame.display.set_caption("Google Maps Veneco:")
        self.clock = pygame.time.Clock() # Para definir los fps de mi juego.
        self.running = True

# Creamos nuestro objeto Setup:
setup = Setup()