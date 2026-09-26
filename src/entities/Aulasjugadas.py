import sys

import pygame

import config
from src.utils.dibujo import dibujar_etiqueta
from src.utils.resource_loader import cargar_fuente, cargar_imagen, cargar_sonido

TITULO = "¡Elegí una actividad!"


class Aula:
    """Escena principal: el aula con las zonas interactivas que llevan a cada minijuego."""

    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto

        fondo_original = cargar_imagen(config.IMG_FONDO_AULA)
        if fondo_original is None:
            print("Falta la imagen de fondo en assets/")
            sys.exit()
        self.fondo = pygame.transform.scale(fondo_original, (ancho, alto))

        self.sonido_clic = cargar_sonido(config.SONIDO_CLIC)

        self.zonas = {
            "MINIJUEGO_NUMEROS": pygame.Rect(270, 15, 340, 160),   # Pizarra blanca en la pared
            "MINIJUEGO_GEOGRAFIA": pygame.Rect(175, 115, 95, 90),  # Globo terráqueo
            "MINIJUEGO_LECTURA": pygame.Rect(224, 426, 256, 102),  # Libro abierto abajo al centro
            "MENU_COMPUTACION": pygame.Rect(485, 175, 145, 65),    # Laptop en el escritorio del profesor
        }

        self.etiquetas = {
            "MINIJUEGO_NUMEROS": "Números",
            "MINIJUEGO_GEOGRAFIA": "Geografía",
            "MINIJUEGO_LECTURA": "Lectura",
            "MENU_COMPUTACION": "Informática",
        }
        # El pizarrón queda pegado al borde superior: su etiqueta va adentro, no arriba.
        self.posiciones_etiqueta = {
            "MINIJUEGO_NUMEROS": (self.zonas["MINIJUEGO_NUMEROS"].centerx, self.zonas["MINIJUEGO_NUMEROS"].bottom - 16),
            "MINIJUEGO_GEOGRAFIA": (self.zonas["MINIJUEGO_GEOGRAFIA"].centerx, self.zonas["MINIJUEGO_GEOGRAFIA"].top - 14),
            "MINIJUEGO_LECTURA": (self.zonas["MINIJUEGO_LECTURA"].centerx, self.zonas["MINIJUEGO_LECTURA"].top - 14),
            "MENU_COMPUTACION": (self.zonas["MENU_COMPUTACION"].centerx, self.zonas["MENU_COMPUTACION"].top - 14),
        }

        self.fuente_titulo = cargar_fuente(config.FUENTE_TITULO, 28)
        self.fuente_etiqueta = cargar_fuente(config.FUENTE_TEXTO_NEGRITA, 16)
        self.fuente_debug = pygame.font.SysFont("Arial", 14, bold=True)

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

    def _dibujar_titulo(self, pantalla):
        superficie_texto = self.fuente_titulo.render(TITULO, True, config.COLOR_BLANCO)
        banner = pygame.Surface((self.ancho, superficie_texto.get_height() + 12), pygame.SRCALPHA)
        banner.fill((0, 0, 0, 120))
        pantalla.blit(banner, (0, 0))
        pantalla.blit(superficie_texto, superficie_texto.get_rect(center=(self.ancho // 2, banner.get_height() // 2)))

    def _dibujar_zonas_debug(self, pantalla):
        for estado, rect in self.zonas.items():
            pygame.draw.rect(pantalla, (255, 0, 0), rect, width=2)
            etiqueta = self.fuente_debug.render(estado, True, (255, 0, 0))
            pantalla.blit(etiqueta, (rect.x, rect.y - 16))

    def dibujar(self, pantalla, posicion_mouse, modo_debug=False):
        pantalla.blit(self.fondo, (0, 0))
        zona_activa = self.zona_bajo_mouse(posicion_mouse)
        if zona_activa:
            self._dibujar_brillo(pantalla, self.zonas[zona_activa])

        self._dibujar_titulo(pantalla)

        for estado, texto in self.etiquetas.items():
            dibujar_etiqueta(pantalla, self.fuente_etiqueta, texto, self.posiciones_etiqueta[estado])

        if modo_debug:
            self._dibujar_zonas_debug(pantalla)
