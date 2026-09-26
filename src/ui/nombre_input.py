import pygame

import config
from src.utils.resource_loader import cargar_fuente, cargar_imagen, cargar_sonido

MAX_CARACTERES = 15
INTERVALO_PARPADEO_MS = 500


class NombreInput:
    """Pantalla que pide el nombre del jugador antes de entrar al aula."""

    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.texto = ""

        fondo_original = cargar_imagen(config.IMG_FONDO_INICIO)
        self.fondo = pygame.transform.scale(fondo_original, (ancho, alto)) if fondo_original is not None else None
        self.sonido_confirmar = cargar_sonido(config.SONIDO_CLIC_INICIO)

        self.fuente_titulo = cargar_fuente(config.FUENTE_TITULO, 40)
        self.fuente_input = cargar_fuente(config.FUENTE_TEXTO, 32)
        self.fuente_boton = cargar_fuente(config.FUENTE_BOTON, 28)

        self.caja_rect = pygame.Rect(0, 0, 400, 60)
        self.caja_rect.center = (ancho // 2, alto // 2)

        self.rect_confirmar = pygame.Rect(0, 0, 220, 60)
        self.rect_confirmar.center = (ancho // 2, alto // 2 + 90)

        self.cursor_visible = True
        self.tiempo_cursor = 0

    def _puede_confirmar(self):
        return len(self.texto.strip()) > 0

    def sobre_boton(self, posicion_mouse):
        return self._puede_confirmar() and self.rect_confirmar.collidepoint(posicion_mouse)

    def manejar_evento(self, evento):
        """Devuelve el nombre confirmado (str) al presionar Enter o el botón, o None si aún no
        (incluye el caso en que todavía no se escribió ninguna letra)."""
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self._puede_confirmar() and self.rect_confirmar.collidepoint(evento.pos):
                return self._confirmar()
            return None

        if evento.type != pygame.KEYDOWN:
            return None

        if evento.key == pygame.K_RETURN:
            if self._puede_confirmar():
                return self._confirmar()
            return None
        if evento.key == pygame.K_BACKSPACE:
            self.texto = self.texto[:-1]
        elif evento.unicode.isprintable() and len(self.texto) < MAX_CARACTERES:
            self.texto += evento.unicode
        return None

    def _confirmar(self):
        if self.sonido_confirmar is not None:
            self.sonido_confirmar.play()
        return self.texto.strip()

    def actualizar(self, dt_ms):
        self.tiempo_cursor += dt_ms
        if self.tiempo_cursor >= INTERVALO_PARPADEO_MS:
            self.tiempo_cursor = 0
            self.cursor_visible = not self.cursor_visible

    def dibujar(self, pantalla):
        if self.fondo is not None:
            pantalla.blit(self.fondo, (0, 0))
        else:
            pantalla.fill((60, 120, 200))

        posicion_mouse = pygame.mouse.get_pos()

        titulo = self.fuente_titulo.render("¿Cómo te llamás?", True, config.COLOR_BLANCO)
        pantalla.blit(titulo, titulo.get_rect(center=(self.ancho // 2, self.alto // 2 - 80)))

        pygame.draw.rect(pantalla, config.COLOR_BLANCO, self.caja_rect, border_radius=10)
        pygame.draw.rect(pantalla, (30, 30, 30), self.caja_rect, width=2, border_radius=10)

        texto_mostrado = self.texto + ("|" if self.cursor_visible else "")
        superficie_texto = self.fuente_input.render(texto_mostrado, True, (30, 30, 30))
        pantalla.blit(
            superficie_texto,
            superficie_texto.get_rect(midleft=(self.caja_rect.x + 15, self.caja_rect.centery)),
        )

        habilitado = self._puede_confirmar()
        hover = habilitado and self.rect_confirmar.collidepoint(posicion_mouse)

        if not habilitado:
            color_boton, color_texto, color_borde = (170, 170, 170), (110, 110, 110), (100, 100, 100)
        elif hover:
            color_boton, color_texto, color_borde = config.COLOR_BLANCO, (30, 30, 30), (40, 40, 40)
        else:
            color_boton, color_texto, color_borde = (225, 225, 225), (30, 30, 30), (40, 40, 40)

        pygame.draw.rect(pantalla, color_boton, self.rect_confirmar, border_radius=12)
        pygame.draw.rect(pantalla, color_borde, self.rect_confirmar, width=2, border_radius=12)
        texto_boton = self.fuente_boton.render("Ingresar", True, color_texto)
        pantalla.blit(texto_boton, texto_boton.get_rect(center=self.rect_confirmar.center))
