import pygame

import config
from src.utils.dibujo import dibujar_etiqueta
from src.utils.resource_loader import cargar_imagen, cargar_sonido


class SubmenuComputacion:
    """Submenú que se abre al hacer clic en la laptop: cada computadora del
    salón lleva a uno de los juegos de alfabetización digital."""

    def __init__(self, ancho, alto):
        fondo_original = cargar_imagen(config.IMG_FONDO_SUBMENU_COMPUTACION)
        self.fondo = pygame.transform.scale(fondo_original, (ancho, alto)) if fondo_original is not None else None
        self.sonido_clic = cargar_sonido(config.SONIDO_CLIC)

        self.zonas = {
            "JUEGO_HARDWARE_SOFTWARE": pygame.Rect(16, 359, 234, 122),  # Computadora adelante, izquierda
            "JUEGO_INFO_2": pygame.Rect(163, 298, 130, 60),             # Computadora del medio, izquierda
            "JUEGO_INFO_3": pygame.Rect(554, 359, 228, 122),            # Computadora adelante, derecha
            "JUEGO_INFO_4": pygame.Rect(506, 298, 136, 60),             # Computadora del medio, derecha
        }

        self.etiquetas = {
            "JUEGO_HARDWARE_SOFTWARE": "Hardware y Software",
            "JUEGO_INFO_2": "Próximamente",
            "JUEGO_INFO_3": "Próximamente",
            "JUEGO_INFO_4": "Próximamente",
        }

        self.fuente_etiqueta = pygame.font.SysFont("Arial", 16, bold=True)
        self.fuente_debug = pygame.font.SysFont("Arial", 14, bold=True)

    def zona_bajo_mouse(self, posicion_mouse):
        for estado, rect in self.zonas.items():
            if rect.collidepoint(posicion_mouse):
                return estado
        return None

    def manejar_clic(self, posicion_mouse):
        estado = self.zona_bajo_mouse(posicion_mouse)
        if estado and self.sonido_clic is not None:
            self.sonido_clic.play()
        return estado

    def _dibujar_brillo(self, pantalla, rectangulo):
        superficie_brillo = pygame.Surface((rectangulo.width, rectangulo.height), pygame.SRCALPHA)
        superficie_brillo.fill((255, 255, 255, 90))
        pantalla.blit(superficie_brillo, (rectangulo.x, rectangulo.y))

    def _dibujar_zonas_debug(self, pantalla):
        for estado, rect in self.zonas.items():
            pygame.draw.rect(pantalla, (255, 0, 0), rect, width=2)
            etiqueta = self.fuente_debug.render(estado, True, (255, 0, 0))
            pantalla.blit(etiqueta, (rect.x, rect.bottom + 2))

    def dibujar(self, pantalla, posicion_mouse, modo_debug=False):
        if self.fondo is not None:
            pantalla.blit(self.fondo, (0, 0))
        else:
            pantalla.fill((30, 30, 60))

        zona_activa = self.zona_bajo_mouse(posicion_mouse)
        for estado, rect in self.zonas.items():
            if estado == zona_activa:
                self._dibujar_brillo(pantalla, rect)
            dibujar_etiqueta(pantalla, self.fuente_etiqueta, self.etiquetas[estado], (rect.centerx, rect.top - 14))

        if modo_debug:
            self._dibujar_zonas_debug(pantalla)
