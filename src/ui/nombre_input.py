import pygame

import config

MAX_CARACTERES = 15
INTERVALO_PARPADEO_MS = 500


class NombreInput:
    """Pantalla que pide el nombre del jugador antes de entrar al aula."""

    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.texto = ""

        self.fuente_titulo = pygame.font.SysFont("Arial", 40, bold=True)
        self.fuente_input = pygame.font.SysFont("Arial", 32)
        self.fuente_ayuda = pygame.font.SysFont("Arial", 20)

        self.caja_rect = pygame.Rect(0, 0, 400, 60)
        self.caja_rect.center = (ancho // 2, alto // 2)

        self.cursor_visible = True
        self.tiempo_cursor = 0

    def manejar_evento(self, evento):
        """Devuelve el nombre confirmado (str) cuando se presiona Enter, o None si aún no."""
        if evento.type != pygame.KEYDOWN:
            return None

        if evento.key == pygame.K_RETURN:
            return self.texto.strip() or "Jugador"
        if evento.key == pygame.K_BACKSPACE:
            self.texto = self.texto[:-1]
        elif evento.unicode.isprintable() and len(self.texto) < MAX_CARACTERES:
            self.texto += evento.unicode
        return None

    def actualizar(self, dt_ms):
        self.tiempo_cursor += dt_ms
        if self.tiempo_cursor >= INTERVALO_PARPADEO_MS:
            self.tiempo_cursor = 0
            self.cursor_visible = not self.cursor_visible

    def dibujar(self, pantalla):
        pantalla.fill((60, 120, 200))

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

        ayuda = self.fuente_ayuda.render("Presioná Enter para continuar", True, config.COLOR_BLANCO)
        pantalla.blit(ayuda, ayuda.get_rect(center=(self.ancho // 2, self.alto // 2 + 60)))
