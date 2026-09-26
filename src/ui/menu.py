import pygame

import config
from src.utils.resource_loader import cargar_fuente, cargar_imagen, cargar_sonido


class Menu:
    """Pantalla de título con los botones Jugar / Salir."""

    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto

        fondo_original = cargar_imagen(config.IMG_FONDO_INICIO)
        self.fondo = pygame.transform.scale(fondo_original, (ancho, alto)) if fondo_original is not None else None
        self.sonido_jugar = cargar_sonido(config.SONIDO_CLIC_INICIO)
        self.sonido_salir = cargar_sonido(config.SONIDO_SALIR)

        self.fuente_titulo = cargar_fuente(config.FUENTE_TITULO, 64)
        self.fuente_boton = cargar_fuente(config.FUENTE_BOTON, 32)

        self.rect_jugar = pygame.Rect(0, 0, 220, 70)
        self.rect_jugar.center = (ancho // 2, alto // 2 + 20)

        self.rect_salir = pygame.Rect(0, 0, 220, 70)
        self.rect_salir.center = (ancho // 2, alto // 2 + 120)

    def sobre_boton(self, posicion_mouse):
        return self.rect_jugar.collidepoint(posicion_mouse) or self.rect_salir.collidepoint(posicion_mouse)

    def manejar_clic(self, posicion_mouse):
        if self.rect_jugar.collidepoint(posicion_mouse):
            self._reproducir(self.sonido_jugar)
            return "jugar"
        if self.rect_salir.collidepoint(posicion_mouse):
            self._reproducir(self.sonido_salir)
            return "salir"
        return None

    def _reproducir(self, sonido):
        if sonido is not None:
            sonido.play()

    def _dibujar_boton(self, pantalla, rect, texto, hover):
        color_fondo = config.COLOR_BLANCO if hover else (225, 225, 225)
        pygame.draw.rect(pantalla, color_fondo, rect, border_radius=12)
        pygame.draw.rect(pantalla, (40, 40, 40), rect, width=2, border_radius=12)
        superficie_texto = self.fuente_boton.render(texto, True, (30, 30, 30))
        pantalla.blit(superficie_texto, superficie_texto.get_rect(center=rect.center))

    def dibujar(self, pantalla, posicion_mouse):
        if self.fondo is not None:
            pantalla.blit(self.fondo, (0, 0))
        else:
            pantalla.fill((60, 120, 200))

        titulo = self.fuente_titulo.render("Aulas Jugadas", True, config.COLOR_BLANCO)
        pantalla.blit(titulo, titulo.get_rect(center=(self.ancho // 2, self.alto // 2 - 120)))

        self._dibujar_boton(pantalla, self.rect_jugar, "Jugar", self.rect_jugar.collidepoint(posicion_mouse))
        self._dibujar_boton(pantalla, self.rect_salir, "Salir", self.rect_salir.collidepoint(posicion_mouse))
