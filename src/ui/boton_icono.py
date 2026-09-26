import pygame

from src.utils.resource_loader import cargar_imagen, cargar_sonido


class BotonIcono:
    """Botón de ícono en una posición fija que se agranda un poco al pasar el mouse."""

    def __init__(self, ruta_imagen, rect, tamano_grande=None, ruta_sonido=None):
        self.rect = rect
        self.normal = cargar_imagen(ruta_imagen, (rect.width, rect.height))

        if tamano_grande is None:
            tamano_grande = (rect.width + 10, rect.height + 10)
        self.grande = cargar_imagen(ruta_imagen, tamano_grande)
        self.desplazamiento = (tamano_grande[0] - rect.width) // 2

        self.cargado = self.normal is not None and self.grande is not None

        self.sonido = cargar_sonido(ruta_sonido) if ruta_sonido else None

    def sobre_boton(self, posicion_mouse):
        return self.cargado and self.rect.collidepoint(posicion_mouse)

    def reproducir_sonido(self):
        if self.sonido is not None:
            self.sonido.play()

    def dibujar(self, pantalla, posicion_mouse):
        if not self.cargado:
            return
        if self.rect.collidepoint(posicion_mouse):
            pantalla.blit(self.grande, (self.rect.x - self.desplazamiento, self.rect.y - self.desplazamiento))
        else:
            pantalla.blit(self.normal, self.rect.topleft)
