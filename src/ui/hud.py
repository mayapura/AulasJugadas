import pygame

import config
from src.utils.resource_loader import cargar_imagen


class HUD:
    """Botones superpuestos a la escena: control de música y salida del juego."""

    def __init__(self):
        self.play_normal = cargar_imagen(config.IMG_PLAY, (40, 40))
        self.play_grande = cargar_imagen(config.IMG_PLAY, (50, 50))
        self.pause_normal = cargar_imagen(config.IMG_PAUSE, (40, 40))
        self.pause_grande = cargar_imagen(config.IMG_PAUSE, (50, 50))
        self.iconos_musica_cargados = all(
            img is not None
            for img in (self.play_normal, self.play_grande, self.pause_normal, self.pause_grande)
        )

        self.salir_normal = cargar_imagen(config.IMG_SALIR, (40, 40))
        self.salir_grande = cargar_imagen(config.IMG_SALIR, (50, 50))
        self.icono_salir_cargado = self.salir_normal is not None and self.salir_grande is not None

        self.btn_play_rect = pygame.Rect(15, 15, 40, 40)
        self.btn_pause_rect = pygame.Rect(65, 15, 40, 40)
        self.btn_salir_rect = pygame.Rect(745, 545, 40, 40)

    def sobre_boton(self, posicion_mouse):
        sobre_musica = self.iconos_musica_cargados and (
            self.btn_play_rect.collidepoint(posicion_mouse)
            or self.btn_pause_rect.collidepoint(posicion_mouse)
        )
        sobre_salir = self.icono_salir_cargado and self.btn_salir_rect.collidepoint(posicion_mouse)
        return sobre_musica or sobre_salir

    def manejar_clic(self, posicion_mouse):
        """Devuelve 'musica', 'salir' o None según el botón donde se hizo clic."""
        if self.iconos_musica_cargados:
            if self.btn_play_rect.collidepoint(posicion_mouse):
                pygame.mixer.music.unpause()
                return "musica"
            if self.btn_pause_rect.collidepoint(posicion_mouse):
                pygame.mixer.music.pause()
                return "musica"

        if self.icono_salir_cargado and self.btn_salir_rect.collidepoint(posicion_mouse):
            return "salir"

        return None

    def dibujar(self, pantalla, posicion_mouse):
        if self.iconos_musica_cargados:
            if self.btn_play_rect.collidepoint(posicion_mouse):
                pantalla.blit(self.play_grande, (self.btn_play_rect.x - 5, self.btn_play_rect.y - 5))
            else:
                pantalla.blit(self.play_normal, (self.btn_play_rect.x, self.btn_play_rect.y))

            if self.btn_pause_rect.collidepoint(posicion_mouse):
                pantalla.blit(self.pause_grande, (self.btn_pause_rect.x - 5, self.btn_pause_rect.y - 5))
            else:
                pantalla.blit(self.pause_normal, (self.btn_pause_rect.x, self.btn_pause_rect.y))

        if self.icono_salir_cargado:
            if self.btn_salir_rect.collidepoint(posicion_mouse):
                pantalla.blit(self.salir_grande, (self.btn_salir_rect.x - 5, self.btn_salir_rect.y - 5))
            else:
                pantalla.blit(self.salir_normal, (self.btn_salir_rect.x, self.btn_salir_rect.y))
