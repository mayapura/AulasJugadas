import sys

import pygame

import config
from src.entities.Aulasjugadas import Aula
from src.entities.player import Player
from src.ui.hud import HUD
from src.ui.menu import Menu
from src.ui.nombre_input import NombreInput

MINIJUEGOS_INFO = {
    "MINIJUEGO_NUMEROS": ("Juego de Números (Pizarra)", config.COLOR_NUMEROS, (100, 250)),
    "MINIJUEGO_LECTURA": ("Juego de Lectura (Libro)", config.COLOR_LECTURA, (120, 250)),
    "MINIJUEGO_GEOGRAFIA": ("Juego de Geografía (Globo)", config.COLOR_GEOGRAFIA, (100, 250)),
    "MINIJUEGO_COMPUTACION": ("Juego de Informática (Laptop)", config.COLOR_COMPUTACION, (80, 250)),
}


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.pantalla = pygame.display.set_mode((config.ANCHO, config.ALTO))
        pygame.display.set_caption(config.TITULO_VENTANA)
        self.reloj = pygame.time.Clock()
        self.fuente_grande = pygame.font.SysFont("Arial", 48, bold=True)

        self.aula = Aula(config.ANCHO, config.ALTO)
        self.hud = HUD()
        self.menu = Menu(config.ANCHO, config.ALTO)
        self.input_nombre = NombreInput(config.ANCHO, config.ALTO)
        self.jugador = Player()

        self.estado_actual = "MENU"
        self.ejecutando = True

    def _procesar_eventos(self, posicion_mouse):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ejecutando = False
                continue

            if self.estado_actual == "MENU":
                self._procesar_evento_menu(evento, posicion_mouse)
            elif self.estado_actual == "INGRESAR_NOMBRE":
                self._procesar_evento_nombre(evento)
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                self._procesar_clic(posicion_mouse)
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                if self.estado_actual != "AULA":
                    self.estado_actual = "AULA"
                    pygame.mixer.music.play(-1)

    def _procesar_evento_menu(self, evento, posicion_mouse):
        if evento.type != pygame.MOUSEBUTTONDOWN or evento.button != 1:
            return

        accion = self.menu.manejar_clic(posicion_mouse)
        if accion == "jugar":
            self.estado_actual = "INGRESAR_NOMBRE"
        elif accion == "salir":
            self.ejecutando = False

    def _procesar_evento_nombre(self, evento):
        nombre_confirmado = self.input_nombre.manejar_evento(evento)
        if nombre_confirmado is not None:
            self.jugador.nombre = nombre_confirmado
            self.estado_actual = "AULA"

    def _procesar_clic(self, posicion_mouse):
        if self.estado_actual != "AULA":
            return

        resultado_hud = self.hud.manejar_clic(posicion_mouse)
        if resultado_hud == "salir":
            self.ejecutando = False
            return
        if resultado_hud == "musica":
            return

        nuevo_estado = self.aula.manejar_clic(posicion_mouse)
        if nuevo_estado:
            self.estado_actual = nuevo_estado

    def _actualizar_cursor(self, posicion_mouse):
        if self.estado_actual == "MENU":
            hover = self.menu.sobre_boton(posicion_mouse)
        elif self.estado_actual == "AULA":
            hover = self.aula.zona_bajo_mouse(posicion_mouse) is not None or self.hud.sobre_boton(posicion_mouse)
        else:
            hover = False

        cursor = pygame.SYSTEM_CURSOR_HAND if hover else pygame.SYSTEM_CURSOR_ARROW
        pygame.mouse.set_cursor(cursor)

    def _dibujar(self, posicion_mouse):
        if self.estado_actual == "MENU":
            self.menu.dibujar(self.pantalla, posicion_mouse)
        elif self.estado_actual == "INGRESAR_NOMBRE":
            self.input_nombre.dibujar(self.pantalla)
        elif self.estado_actual == "AULA":
            self.aula.dibujar(self.pantalla, posicion_mouse)
            self.hud.dibujar(self.pantalla, posicion_mouse)
        else:
            texto, color, posicion_texto = MINIJUEGOS_INFO[self.estado_actual]
            self.pantalla.fill(color)
            self.pantalla.blit(
                self.fuente_grande.render(texto, True, config.COLOR_BLANCO),
                posicion_texto,
            )

        pygame.display.flip()

    def ejecutar(self):
        while self.ejecutando:
            dt_ms = self.reloj.tick(config.FPS)
            posicion_mouse = pygame.mouse.get_pos()

            self._procesar_eventos(posicion_mouse)
            self._actualizar_cursor(posicion_mouse)

            if self.estado_actual == "INGRESAR_NOMBRE":
                self.input_nombre.actualizar(dt_ms)

            self._dibujar(posicion_mouse)

        pygame.quit()
        sys.exit()
