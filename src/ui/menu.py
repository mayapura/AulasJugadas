import pygame

import config


class Menu:
    """Pantalla de título con los botones Jugar / Salir."""

    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto

        self.fuente_titulo = pygame.font.SysFont("Arial", 64, bold=True)
        self.fuente_boton = pygame.font.SysFont("Arial", 32)

        self.rect_jugar = pygame.Rect(0, 0, 220, 70)
        self.rect_jugar.center = (ancho // 2, alto // 2 + 20)

        self.rect_salir = pygame.Rect(0, 0, 220, 70)
        self.rect_salir.center = (ancho // 2, alto // 2 + 120)

    def sobre_boton(self, posicion_mouse):
        return self.rect_jugar.collidepoint(posicion_mouse) or self.rect_salir.collidepoint(posicion_mouse)

    def manejar_clic(self, posicion_mouse):
        if self.rect_jugar.collidepoint(posicion_mouse):
            return "jugar"
        if self.rect_salir.collidepoint(posicion_mouse):
            return "salir"
        return None

    def _dibujar_boton(self, pantalla, rect, texto, hover):
        color_fondo = config.COLOR_BLANCO if hover else (225, 225, 225)
        pygame.draw.rect(pantalla, color_fondo, rect, border_radius=12)
        pygame.draw.rect(pantalla, (40, 40, 40), rect, width=2, border_radius=12)
        superficie_texto = self.fuente_boton.render(texto, True, (30, 30, 30))
        pantalla.blit(superficie_texto, superficie_texto.get_rect(center=rect.center))

    def dibujar(self, pantalla, posicion_mouse):
        pantalla.fill((60, 120, 200))

        titulo = self.fuente_titulo.render("Aulas Jugadas", True, config.COLOR_BLANCO)
        pantalla.blit(titulo, titulo.get_rect(center=(self.ancho // 2, self.alto // 2 - 120)))

        self._dibujar_boton(pantalla, self.rect_jugar, "Jugar", self.rect_jugar.collidepoint(posicion_mouse))
        self._dibujar_boton(pantalla, self.rect_salir, "Salir", self.rect_salir.collidepoint(posicion_mouse))
