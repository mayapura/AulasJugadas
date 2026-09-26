import sys

import pygame

import config
from src.entities.Aulasjugadas import Aula
from src.entities.player import Player
from src.entities.submenu_computacion import SubmenuComputacion
from src.minigames.hardware_software import HardwareSoftwareGame
from src.ui.hud import HUD
from src.ui.menu import Menu
from src.ui.nombre_input import NombreInput
from src.utils.resource_loader import cargar_cursor, cargar_fuente, cargar_musica

MINIJUEGOS_INFO = {
    "MINIJUEGO_NUMEROS": ("Juego de Números (Pizarra)", config.COLOR_NUMEROS, (100, 250)),
    "MINIJUEGO_LECTURA": ("Juego de Lectura (Libro)", config.COLOR_LECTURA, (120, 250)),
    "MINIJUEGO_GEOGRAFIA": ("Juego de Geografía (Globo)", config.COLOR_GEOGRAFIA, (100, 250)),
    "JUEGO_INFO_2": ("Próximamente...", config.COLOR_COMPUTACION, (250, 250)),
    "JUEGO_INFO_3": ("Próximamente...", config.COLOR_COMPUTACION, (250, 250)),
    "JUEGO_INFO_4": ("Próximamente...", config.COLOR_COMPUTACION, (250, 250)),
}

# A qué estado volver al presionar ESC (o el botón "Volver"/ícono de salir de una pantalla)
ESTADO_ANTERIOR = {
    "MINIJUEGO_NUMEROS": "AULA",
    "MINIJUEGO_LECTURA": "AULA",
    "MINIJUEGO_GEOGRAFIA": "AULA",
    "MENU_COMPUTACION": "AULA",
    "JUEGO_HARDWARE_SOFTWARE": "MENU_COMPUTACION",
    "JUEGO_INFO_2": "MENU_COMPUTACION",
    "JUEGO_INFO_3": "MENU_COMPUTACION",
    "JUEGO_INFO_4": "MENU_COMPUTACION",
}

# Qué música corresponde a cada estado (los estados que no figuran quedan en silencio).
# MENU e INGRESAR_NOMBRE comparten la misma música: al pasar de uno a otro sigue sonando sin reiniciarse.
MUSICA_POR_ESTADO = {
    "MENU": config.SONIDO_MUSICA_INICIO,
    "INGRESAR_NOMBRE": config.SONIDO_MUSICA_INICIO,
    "AULA": config.SONIDO_MUSICA_FONDO,
    "MENU_COMPUTACION": config.SONIDO_MUSICA_SUBMENU_COMPUTACION,
}


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.pantalla = pygame.display.set_mode((config.ANCHO, config.ALTO))
        pygame.display.set_caption(config.TITULO_VENTANA)
        self.reloj = pygame.time.Clock()
        self.fuente_grande = cargar_fuente(config.FUENTE_TITULO, 48)

        self.aula = Aula(config.ANCHO, config.ALTO)
        self.hud = HUD()
        self.menu = Menu(config.ANCHO, config.ALTO)
        self.input_nombre = NombreInput(config.ANCHO, config.ALTO)
        self.submenu_computacion = SubmenuComputacion(config.ANCHO, config.ALTO)
        self.jugador = Player()
        self.juego_hs = HardwareSoftwareGame(config.ANCHO, config.ALTO, self.jugador)

        self.cursor_flecha = cargar_cursor(config.IMG_CURSOR_FLECHA, (2, 2)) or pygame.SYSTEM_CURSOR_ARROW
        self.cursor_mano = cargar_cursor(config.IMG_CURSOR_MANO, (12, 2)) or pygame.SYSTEM_CURSOR_HAND

        self.ejecutando = True
        self.modo_debug = False
        self._musica_actual = None
        self._cambiar_estado("MENU")

    def _procesar_eventos(self, posicion_mouse):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ejecutando = False
                continue

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_F1:
                self.modo_debug = not self.modo_debug
                continue

            if (
                evento.type == pygame.KEYDOWN
                and evento.key == pygame.K_ESCAPE
                and self.estado_actual in ESTADO_ANTERIOR
            ):
                self._cambiar_estado(ESTADO_ANTERIOR[self.estado_actual])
                continue

            if self.estado_actual == "MENU":
                self._procesar_evento_menu(evento, posicion_mouse)
            elif self.estado_actual == "INGRESAR_NOMBRE":
                self._procesar_evento_nombre(evento)
            elif self.estado_actual == "AULA":
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    self._procesar_clic_aula(posicion_mouse)
            elif self.estado_actual == "MENU_COMPUTACION":
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    self._procesar_clic_submenu_computacion(posicion_mouse)
            elif self.estado_actual == "JUEGO_HARDWARE_SOFTWARE":
                self.juego_hs.manejar_evento(evento, posicion_mouse)
                if self.juego_hs.debe_salir:
                    self.juego_hs.debe_salir = False
                    self._cambiar_estado(ESTADO_ANTERIOR["JUEGO_HARDWARE_SOFTWARE"])

    def _cambiar_estado(self, nuevo_estado):
        self.estado_actual = nuevo_estado

        ruta_musica = MUSICA_POR_ESTADO.get(nuevo_estado)
        if ruta_musica == self._musica_actual:
            return  # ya está sonando (o en silencio) lo que corresponde: no la reiniciamos

        self._musica_actual = ruta_musica
        if ruta_musica:
            cargar_musica(ruta_musica, config.VOLUMEN_MUSICA)
        else:
            pygame.mixer.music.stop()

    def _procesar_evento_menu(self, evento, posicion_mouse):
        if evento.type != pygame.MOUSEBUTTONDOWN or evento.button != 1:
            return

        accion = self.menu.manejar_clic(posicion_mouse)
        if accion == "jugar":
            self._cambiar_estado("INGRESAR_NOMBRE")
        elif accion == "salir":
            self.ejecutando = False

    def _procesar_evento_nombre(self, evento):
        nombre_confirmado = self.input_nombre.manejar_evento(evento)
        if nombre_confirmado is not None:
            self.jugador.nombre = nombre_confirmado
            self._cambiar_estado("AULA")

    def _procesar_clic_aula(self, posicion_mouse):
        resultado_hud = self.hud.manejar_clic(posicion_mouse)
        if resultado_hud == "salir":
            self.ejecutando = False
            return
        if resultado_hud == "musica":
            return

        nuevo_estado = self.aula.manejar_clic(posicion_mouse)
        if nuevo_estado:
            self._cambiar_estado(nuevo_estado)

    def _procesar_clic_submenu_computacion(self, posicion_mouse):
        if self.submenu_computacion.boton_volver.sobre_boton(posicion_mouse):
            self.submenu_computacion.boton_volver.reproducir_sonido()
            self._cambiar_estado(ESTADO_ANTERIOR["MENU_COMPUTACION"])
            return

        resultado_hud = self.hud.manejar_clic(posicion_mouse, mostrar_salir=False)
        if resultado_hud == "musica":
            return

        nuevo_estado = self.submenu_computacion.manejar_clic(posicion_mouse)
        if nuevo_estado == "JUEGO_HARDWARE_SOFTWARE":
            self.juego_hs.reiniciar()
        if nuevo_estado:
            self._cambiar_estado(nuevo_estado)

    def _actualizar_cursor(self, posicion_mouse):
        if self.estado_actual == "MENU":
            hover = self.menu.sobre_boton(posicion_mouse)
        elif self.estado_actual == "INGRESAR_NOMBRE":
            hover = self.input_nombre.sobre_boton(posicion_mouse)
        elif self.estado_actual == "AULA":
            hover = self.aula.zona_bajo_mouse(posicion_mouse) is not None or self.hud.sobre_boton(posicion_mouse)
        elif self.estado_actual == "MENU_COMPUTACION":
            hover = (
                self.submenu_computacion.zona_bajo_mouse(posicion_mouse) is not None
                or self.submenu_computacion.boton_volver.sobre_boton(posicion_mouse)
                or self.hud.sobre_boton(posicion_mouse, mostrar_salir=False)
            )
        elif self.estado_actual == "JUEGO_HARDWARE_SOFTWARE":
            hover = self.juego_hs.sobre_elemento_interactivo(posicion_mouse)
        else:
            hover = False

        cursor = self.cursor_mano if hover else self.cursor_flecha
        pygame.mouse.set_cursor(cursor)

    def _dibujar(self, posicion_mouse):
        if self.estado_actual == "MENU":
            self.menu.dibujar(self.pantalla, posicion_mouse)
        elif self.estado_actual == "INGRESAR_NOMBRE":
            self.input_nombre.dibujar(self.pantalla)
        elif self.estado_actual == "AULA":
            self.aula.dibujar(self.pantalla, posicion_mouse, self.modo_debug)
            self.hud.dibujar(self.pantalla, posicion_mouse)
        elif self.estado_actual == "MENU_COMPUTACION":
            self.submenu_computacion.dibujar(self.pantalla, posicion_mouse, self.modo_debug)
            self.hud.dibujar(self.pantalla, posicion_mouse, mostrar_salir=False)
        elif self.estado_actual == "JUEGO_HARDWARE_SOFTWARE":
            self.juego_hs.dibujar(self.pantalla, posicion_mouse)
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
            elif self.estado_actual == "JUEGO_HARDWARE_SOFTWARE":
                self.juego_hs.actualizar(dt_ms)

            self._dibujar(posicion_mouse)

        self._esperar_fin_de_sonido()
        pygame.quit()
        sys.exit()

    def _esperar_fin_de_sonido(self, tiempo_maximo_ms=1500):
        """Antes de cerrar, deja terminar cualquier efecto de sonido en curso (por ej. el de 'salir')."""
        tiempo_transcurrido = 0
        while pygame.mixer.get_busy() and tiempo_transcurrido < tiempo_maximo_ms:
            pygame.time.wait(50)
            tiempo_transcurrido += 50
