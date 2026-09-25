import pygame


def dibujar_etiqueta(pantalla, fuente, texto, pos_centro, color_texto=(255, 255, 255)):
    """Dibuja un texto centrado en pos_centro con un fondo negro semitransparente detrás,
    para que se lea bien sobre cualquier imagen."""
    superficie_texto = fuente.render(texto, True, color_texto)
    posicion = superficie_texto.get_rect(center=pos_centro)

    fondo = pygame.Surface((posicion.width + 12, posicion.height + 8), pygame.SRCALPHA)
    fondo.fill((0, 0, 0, 140))
    pantalla.blit(fondo, (posicion.x - 6, posicion.y - 4))
    pantalla.blit(superficie_texto, posicion)
