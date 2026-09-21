import sys

import pygame

import config
from src.utils.resource_loader import cargar_imagen, cargar_sonido, cargar_musica


class Aula:
    """Escena principal: el aula con las zonas interactivas que llevan a cada minijuego."""

    def __init__(self, ancho, alto):
        fondo_original = cargar_imagen(config.IMG_FONDO_AULA)
        if fondo_original is None:
            print("Falta la imagen de fondo en assets/")
            sys.exit()
        self.fondo = pygame.transform.scale(fondo_original, (ancho, alto))

        self.sonido_clic = cargar_sonido(config.SONIDO_CLIC)
        cargar_musica(config.SONIDO_MUSICA_FONDO, config.VOLUMEN_MUSICA)

        self.zonas = {
            "MINIJUEGO_NUMEROS": pygame.Rect(270, 15, 340, 160),      # Pizarra blanca en la pared
            "MINIJUEGO_GEOGRAFIA": pygame.Rect(175, 115, 95, 90),     # Globo terráqueo
            "MINIJUEGO_LECTURA": pygame.Rect(240, 475, 245, 115),     # Libro abierto abajo al centro
            "MINIJUEGO_COMPUTACION": pygame.Rect(485, 175, 145, 65),  # Laptop en el escritorio del profesor
        }

    def zona_bajo_mouse(self, posicion_mouse):
        for estado, rect in self.zonas.items():
            if rect.collidepoint(posicion_mouse):
                return estado
        return None

    def manejar_clic(self, posicion_mouse):
        """Si el clic cae en una zona, reproduce el sonido, detiene la música y devuelve el nuevo estado."""
        estado = self.zona_bajo_mouse(posicion_mouse)
        if estado and self.sonido_clic is not None:
            self.sonido_clic.play()
            pygame.mixer.music.stop()
        return estado

    def _dibujar_brillo(self, pantalla, rectangulo):
        superficie_brillo = pygame.Surface((rectangulo.width, rectangulo.height), pygame.SRCALPHA)
        superficie_brillo.fill((255, 255, 255, 80))
        pantalla.blit(superficie_brillo, (rectangulo.x, rectangulo.y))

    def dibujar(self, pantalla, posicion_mouse):
        pantalla.blit(self.fondo, (0, 0))
        zona_activa = self.zona_bajo_mouse(posicion_mouse)
        if zona_activa:
            self._dibujar_brillo(pantalla, self.zonas[zona_activa])
