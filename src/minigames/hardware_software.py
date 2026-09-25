import random

import pygame

import config
from src.utils.resource_loader import cargar_imagen

TIEMPO_TOTAL_MS = 7 * 60 * 1000

PUNTOS_CLASIFICACION_CORRECTA = 10
PUNTOS_CLASIFICACION_INCORRECTA = -5
PUNTOS_LETRA_INCORRECTA = -2
PUNTOS_PALABRA_COMPLETA = 15

TECLAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

DATASET = [
    {"nombre": "Teclado", "palabra": "TECLADO", "categoria": "HARDWARE", "archivo": "teclado.png"},
    {"nombre": "Mouse", "palabra": "MOUSE", "categoria": "HARDWARE", "archivo": "mouse.png"},
    {"nombre": "Monitor", "palabra": "MONITOR", "categoria": "HARDWARE", "archivo": "monitor.png"},
    {"nombre": "Impresora", "palabra": "IMPRESORA", "categoria": "HARDWARE", "archivo": "impresora.png"},
    {"nombre": "Parlantes", "palabra": "PARLANTES", "categoria": "HARDWARE", "archivo": "parlantes.jpg"},
    {"nombre": "Pendrive", "palabra": "PENDRIVE", "categoria": "HARDWARE", "archivo": "pendrive.png"},
    {"nombre": "Cámara web", "palabra": "CAMARA", "categoria": "HARDWARE", "archivo": "camara_web.png"},
    {"nombre": "Auriculares", "palabra": "AURICULARES", "categoria": "HARDWARE", "archivo": "auriculares.png"},
    {"nombre": "Word", "palabra": "WORD", "categoria": "SOFTWARE", "archivo": "word.png"},
    {"nombre": "Paint", "palabra": "PAINT", "categoria": "SOFTWARE", "archivo": "paint.png"},
    {"nombre": "Google Chrome", "palabra": "CHROME", "categoria": "SOFTWARE", "archivo": "chrome.png"},
    {"nombre": "Calculadora", "palabra": "CALCULADORA", "categoria": "SOFTWARE", "archivo": "calculadora.png"},
    {"nombre": "Excel", "palabra": "EXCEL", "categoria": "SOFTWARE", "archivo": "excel.png"},
    {"nombre": "PowerPoint", "palabra": "POWERPOINT", "categoria": "SOFTWARE", "archivo": "powerpoint.png"},
    {"nombre": "Windows", "palabra": "WINDOWS", "categoria": "SOFTWARE", "archivo": "Windows.png"},
    {"nombre": "Photoshop", "palabra": "PHOTOSHOP", "categoria": "SOFTWARE", "archivo": "photoshop.png"},
]


class HardwareSoftwareGame:
    """Minijuego de alfabetización digital: arrastrar el dispositivo/programa a
    Hardware o Software y después completar su nombre tipo ahorcado, a contrarreloj."""

    def __init__(self, ancho, alto, jugador):
        self.ancho = ancho
        self.alto = alto
        self.jugador = jugador

        self.fuente_grande = pygame.font.SysFont("Arial", 40, bold=True)
        self.fuente_mediana = pygame.font.SysFont("Arial", 28)
        self.fuente_pequena = pygame.font.SysFont("Arial", 20)
        self.fuente_letra = pygame.font.SysFont("Arial", 22, bold=True)

        self.fondo = cargar_imagen(config.IMG_FONDO_HARDWARE_SOFTWARE, (ancho, alto))

        self.caja_hardware_rect = pygame.Rect(50, 380, 200, 150)
        self.caja_software_rect = pygame.Rect(ancho - 250, 380, 200, 150)
        self.imagen_caja = cargar_imagen(config.IMG_CAJA, (200, 150))

        self.imagen_tamano = (150, 150)
        self.imagen_pos_inicial = (ancho // 2 - 75, 220)

        self.rect_reintentar = pygame.Rect(0, 0, 220, 60)
        self.rect_reintentar.center = (ancho // 2, alto // 2 + 30)
        self.rect_volver = pygame.Rect(0, 0, 220, 60)
        self.rect_volver.center = (ancho // 2, alto // 2 + 110)

        self.btn_volver_icono_rect = pygame.Rect(15, 15, 40, 40)
        self.icono_volver_normal = cargar_imagen(config.IMG_SALIR, (40, 40))
        self.icono_volver_grande = cargar_imagen(config.IMG_SALIR, (50, 50))
        self.icono_volver_cargado = self.icono_volver_normal is not None and self.icono_volver_grande is not None

        self._construir_teclado()
        self.reiniciar()

    def _construir_teclado(self):
        columnas = 9
        ancho_tecla, alto_tecla, margen = 42, 42, 6
        ancho_fila = columnas * ancho_tecla + (columnas - 1) * margen
        inicio_x = (self.ancho - ancho_fila) // 2
        inicio_y = self.alto - 150

        self.teclas_rects = {}
        for indice, letra in enumerate(TECLAS):
            fila, columna = divmod(indice, columnas)
            x = inicio_x + columna * (ancho_tecla + margen)
            y = inicio_y + fila * (alto_tecla + margen)
            self.teclas_rects[letra] = pygame.Rect(x, y, ancho_tecla, alto_tecla)

    # --- ciclo de vida ---
    def reiniciar(self):
        self.mazo = random.sample(DATASET, len(DATASET))
        self.indice_item = 0
        self.tiempo_restante_ms = TIEMPO_TOTAL_MS
        self.terminado = False
        self.debe_salir = False
        self.jugador.puntuacion = 0
        self._cargar_item_actual()

    def _cargar_item_actual(self):
        if self.indice_item >= len(self.mazo):
            self.mazo = random.sample(DATASET, len(DATASET))
            self.indice_item = 0

        self.item_actual = self.mazo[self.indice_item]
        self.imagen_actual = cargar_imagen(
            config.RUTA_IMAGENES + "dispositivos/" + self.item_actual["archivo"],
            self.imagen_tamano,
        )

        self.fase = "CLASIFICAR"
        self.arrastrando = False
        self.offset_arrastre = (0, 0)
        self.imagen_rect = pygame.Rect(*self.imagen_pos_inicial, *self.imagen_tamano)

        self.letras_adivinadas = set()
        self.letras_falladas = set()

    def _siguiente_item(self):
        self.indice_item += 1
        self._cargar_item_actual()

    # --- eventos ---
    def manejar_evento(self, evento, posicion_mouse):
        if (
            evento.type == pygame.MOUSEBUTTONDOWN
            and evento.button == 1
            and self.icono_volver_cargado
            and self.btn_volver_icono_rect.collidepoint(posicion_mouse)
        ):
            self.debe_salir = True
            return

        if self.terminado:
            self._manejar_evento_fin(evento, posicion_mouse)
        elif self.fase == "CLASIFICAR":
            self._manejar_evento_clasificar(evento, posicion_mouse)
        elif self.fase == "ADIVINAR":
            self._manejar_evento_adivinar(evento, posicion_mouse)

    def _manejar_evento_clasificar(self, evento, posicion_mouse):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.imagen_rect.collidepoint(posicion_mouse):
                self.arrastrando = True
                self.offset_arrastre = (
                    posicion_mouse[0] - self.imagen_rect.x,
                    posicion_mouse[1] - self.imagen_rect.y,
                )
        elif evento.type == pygame.MOUSEMOTION and self.arrastrando:
            self.imagen_rect.x = posicion_mouse[0] - self.offset_arrastre[0]
            self.imagen_rect.y = posicion_mouse[1] - self.offset_arrastre[1]
        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1 and self.arrastrando:
            self.arrastrando = False
            self._soltar_imagen()

    def _soltar_imagen(self):
        if self.caja_hardware_rect.colliderect(self.imagen_rect):
            self._resolver_clasificacion("HARDWARE")
        elif self.caja_software_rect.colliderect(self.imagen_rect):
            self._resolver_clasificacion("SOFTWARE")
        else:
            self.imagen_rect.topleft = self.imagen_pos_inicial

    def _resolver_clasificacion(self, categoria_elegida):
        if categoria_elegida == self.item_actual["categoria"]:
            self.jugador.sumar_puntos(PUNTOS_CLASIFICACION_CORRECTA)
            self.fase = "ADIVINAR"
            self.imagen_rect.topleft = self.imagen_pos_inicial
        else:
            self.jugador.sumar_puntos(PUNTOS_CLASIFICACION_INCORRECTA)
            self._siguiente_item()

    def _manejar_evento_adivinar(self, evento, posicion_mouse):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for letra, rect in self.teclas_rects.items():
                if rect.collidepoint(posicion_mouse):
                    self._elegir_letra(letra)
                    break
        elif evento.type == pygame.KEYDOWN:
            letra = evento.unicode.upper()
            if letra in TECLAS:
                self._elegir_letra(letra)

    def _elegir_letra(self, letra):
        if letra in self.letras_adivinadas or letra in self.letras_falladas:
            return

        if letra in self.item_actual["palabra"]:
            self.letras_adivinadas.add(letra)
            if all(l in self.letras_adivinadas for l in self.item_actual["palabra"]):
                self.jugador.sumar_puntos(PUNTOS_PALABRA_COMPLETA)
                self._siguiente_item()
        else:
            self.letras_falladas.add(letra)
            self.jugador.sumar_puntos(PUNTOS_LETRA_INCORRECTA)

    def _manejar_evento_fin(self, evento, posicion_mouse):
        if evento.type != pygame.MOUSEBUTTONDOWN or evento.button != 1:
            return
        if self.rect_reintentar.collidepoint(posicion_mouse):
            self.reiniciar()
        elif self.rect_volver.collidepoint(posicion_mouse):
            self.debe_salir = True

    # --- actualización ---
    def actualizar(self, dt_ms):
        if self.terminado:
            return

        self.tiempo_restante_ms -= dt_ms
        if self.tiempo_restante_ms <= 0:
            self.tiempo_restante_ms = 0
            self.terminado = True

    def sobre_elemento_interactivo(self, posicion_mouse):
        if self.icono_volver_cargado and self.btn_volver_icono_rect.collidepoint(posicion_mouse):
            return True
        if self.terminado:
            return self.rect_reintentar.collidepoint(posicion_mouse) or self.rect_volver.collidepoint(
                posicion_mouse
            )
        if self.fase == "CLASIFICAR":
            return self.arrastrando or self.imagen_rect.collidepoint(posicion_mouse)
        if self.fase == "ADIVINAR":
            return any(
                rect.collidepoint(posicion_mouse)
                for letra, rect in self.teclas_rects.items()
                if letra not in self.letras_adivinadas and letra not in self.letras_falladas
            )
        return False

    # --- dibujado ---
    def dibujar(self, pantalla, posicion_mouse):
        if self.fondo is not None:
            pantalla.blit(self.fondo, (0, 0))
        else:
            pantalla.fill((235, 245, 255))

        self._dibujar_encabezado(pantalla)

        if self.terminado:
            self._dibujar_fin(pantalla, posicion_mouse)
        elif self.fase == "CLASIFICAR":
            self._dibujar_clasificar(pantalla)
        elif self.fase == "ADIVINAR":
            self._dibujar_adivinar(pantalla, posicion_mouse)

        self._dibujar_icono_volver(pantalla, posicion_mouse)

    def _dibujar_imagen(self, pantalla, rect):
        if self.imagen_actual is not None:
            pantalla.blit(self.imagen_actual, rect)
        else:
            pygame.draw.rect(pantalla, config.COLOR_BLANCO, rect)
            pygame.draw.rect(pantalla, (40, 40, 40), rect, width=2)
            texto = self.fuente_pequena.render(self.item_actual["nombre"], True, (30, 30, 30))
            pantalla.blit(texto, texto.get_rect(center=rect.center))

    def _dibujar_encabezado(self, pantalla):
        segundos_totales = self.tiempo_restante_ms // 1000
        minutos, segundos = divmod(segundos_totales, 60)
        texto_tiempo = self.fuente_mediana.render(f"Tiempo: {minutos}:{segundos:02d}", True, config.COLOR_BLANCO)
        pantalla.blit(texto_tiempo, (65, 25))

        texto_puntos = self.fuente_mediana.render(f"Puntos: {self.jugador.puntuacion}", True, config.COLOR_BLANCO)
        pantalla.blit(texto_puntos, (self.ancho - texto_puntos.get_width() - 20, 25))

    def _dibujar_icono_volver(self, pantalla, posicion_mouse):
        if not self.icono_volver_cargado:
            return
        if self.btn_volver_icono_rect.collidepoint(posicion_mouse):
            pantalla.blit(self.icono_volver_grande, (self.btn_volver_icono_rect.x - 5, self.btn_volver_icono_rect.y - 5))
        else:
            pantalla.blit(self.icono_volver_normal, self.btn_volver_icono_rect.topleft)

    def _dibujar_caja(self, pantalla, rect, etiqueta):
        if self.imagen_caja is not None:
            pantalla.blit(self.imagen_caja, rect)
        else:
            pygame.draw.rect(pantalla, (220, 220, 220), rect, border_radius=12)
            pygame.draw.rect(pantalla, (40, 40, 40), rect, width=2, border_radius=12)

        texto = self.fuente_mediana.render(etiqueta, True, config.COLOR_BLANCO)
        pantalla.blit(texto, texto.get_rect(center=(rect.centerx, rect.bottom + 20)))

    def _dibujar_clasificar(self, pantalla):
        self._dibujar_caja(pantalla, self.caja_hardware_rect, "Hardware")
        self._dibujar_caja(pantalla, self.caja_software_rect, "Software")

        ayuda = self.fuente_pequena.render("Arrastrá la imagen a la caja correcta", True, config.COLOR_BLANCO)
        pantalla.blit(ayuda, ayuda.get_rect(center=(self.ancho // 2, self.imagen_pos_inicial[1] - 30)))

        self._dibujar_imagen(pantalla, self.imagen_rect)

    def _dibujar_adivinar(self, pantalla, posicion_mouse):
        rect_imagen_chica = pygame.Rect(0, 0, *self.imagen_tamano)
        rect_imagen_chica.center = (self.ancho // 2, 150)
        self._dibujar_imagen(pantalla, rect_imagen_chica)

        palabra = self.item_actual["palabra"]
        espacio = 36
        x_inicial = self.ancho // 2 - (len(palabra) * espacio) // 2
        y_palabra = 260

        for indice, letra in enumerate(palabra):
            x = x_inicial + indice * espacio
            linea_y = y_palabra + 30
            pygame.draw.line(pantalla, config.COLOR_BLANCO, (x, linea_y), (x + espacio - 10, linea_y), 3)
            if letra in self.letras_adivinadas:
                superficie = self.fuente_grande.render(letra, True, config.COLOR_BLANCO)
                rect_letra = superficie.get_rect(midbottom=(x + (espacio - 10) // 2, linea_y - 8))
                pantalla.blit(superficie, rect_letra)

        if self.letras_falladas:
            texto_falladas = self.fuente_pequena.render(
                "Falladas: " + ", ".join(sorted(self.letras_falladas)), True, (255, 110, 110)
            )
            pantalla.blit(texto_falladas, texto_falladas.get_rect(center=(self.ancho // 2, y_palabra + 60)))

        for letra, rect in self.teclas_rects.items():
            if letra in self.letras_adivinadas:
                color = (150, 220, 150)
            elif letra in self.letras_falladas:
                color = (220, 150, 150)
            elif rect.collidepoint(posicion_mouse):
                color = config.COLOR_BLANCO
            else:
                color = (225, 225, 225)

            pygame.draw.rect(pantalla, color, rect, border_radius=6)
            pygame.draw.rect(pantalla, (40, 40, 40), rect, width=1, border_radius=6)
            superficie_letra = self.fuente_letra.render(letra, True, (30, 30, 30))
            pantalla.blit(superficie_letra, superficie_letra.get_rect(center=rect.center))

    def _dibujar_fin(self, pantalla, posicion_mouse):
        titulo = self.fuente_grande.render("¡Tiempo terminado!", True, config.COLOR_BLANCO)
        pantalla.blit(titulo, titulo.get_rect(center=(self.ancho // 2, self.alto // 2 - 100)))

        texto_puntaje = self.fuente_mediana.render(
            f"Puntaje final: {self.jugador.puntuacion}", True, config.COLOR_BLANCO
        )
        pantalla.blit(texto_puntaje, texto_puntaje.get_rect(center=(self.ancho // 2, self.alto // 2 - 50)))

        self._dibujar_boton(pantalla, self.rect_reintentar, "Reintentar", posicion_mouse)
        self._dibujar_boton(pantalla, self.rect_volver, "Volver", posicion_mouse)

    def _dibujar_boton(self, pantalla, rect, texto, posicion_mouse):
        color = config.COLOR_BLANCO if rect.collidepoint(posicion_mouse) else (225, 225, 225)
        pygame.draw.rect(pantalla, color, rect, border_radius=10)
        pygame.draw.rect(pantalla, (40, 40, 40), rect, width=2, border_radius=10)
        superficie = self.fuente_mediana.render(texto, True, (30, 30, 30))
        pantalla.blit(superficie, superficie.get_rect(center=rect.center))
