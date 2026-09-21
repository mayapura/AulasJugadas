import random

import pygame

import config
from src.utils.resource_loader import cargar_imagen

TIEMPO_TOTAL_MS = 90_000

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
    {"nombre": "Parlantes", "palabra": "PARLANTES", "categoria": "HARDWARE", "archivo": "parlantes.png"},
    {"nombre": "Pendrive", "palabra": "PENDRIVE", "categoria": "HARDWARE", "archivo": "pendrive.png"},
    {"nombre": "Cámara web", "palabra": "CAMARA", "categoria": "HARDWARE", "archivo": "camara_web.png"},
    {"nombre": "Auriculares", "palabra": "AURICULARES", "categoria": "HARDWARE", "archivo": "auriculares.png"},
    {"nombre": "Word", "palabra": "WORD", "categoria": "SOFTWARE", "archivo": "word.png"},
    {"nombre": "Paint", "palabra": "PAINT", "categoria": "SOFTWARE", "archivo": "paint.png"},
    {"nombre": "Google Chrome", "palabra": "CHROME", "categoria": "SOFTWARE", "archivo": "chrome.png"},
    {"nombre": "Calculadora", "palabra": "CALCULADORA", "categoria": "SOFTWARE", "archivo": "calculadora.png"},
    {"nombre": "Excel", "palabra": "EXCEL", "categoria": "SOFTWARE", "archivo": "excel.png"},
    {"nombre": "PowerPoint", "palabra": "POWERPOINT", "categoria": "SOFTWARE", "archivo": "powerpoint.png"},
    {"nombre": "Windows", "palabra": "WINDOWS", "categoria": "SOFTWARE", "archivo": "windows.png"},
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

        self.caja_hardware_rect = pygame.Rect(40, 400, 300, 150)
        self.caja_software_rect = pygame.Rect(ancho - 340, 400, 300, 150)

        self.imagen_tamano = (150, 150)
        self.imagen_pos_inicial = (ancho // 2 - 75, 220)

        self.rect_reintentar = pygame.Rect(0, 0, 220, 60)
        self.rect_reintentar.center = (ancho // 2, alto // 2 + 30)
        self.rect_volver_aula = pygame.Rect(0, 0, 220, 60)
        self.rect_volver_aula.center = (ancho // 2, alto // 2 + 110)

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
        self.debe_volver_aula = False
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
        elif self.rect_volver_aula.collidepoint(posicion_mouse):
            self.debe_volver_aula = True

    # --- actualización ---
    def actualizar(self, dt_ms):
        if self.terminado:
            return
        self.tiempo_restante_ms -= dt_ms
        if self.tiempo_restante_ms <= 0:
            self.tiempo_restante_ms = 0
            self.terminado = True

    def sobre_elemento_interactivo(self, posicion_mouse):
        if self.terminado:
            return self.rect_reintentar.collidepoint(posicion_mouse) or self.rect_volver_aula.collidepoint(
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
        pantalla.fill((235, 245, 255))
        self._dibujar_encabezado(pantalla)

        if self.terminado:
            self._dibujar_fin(pantalla, posicion_mouse)
        elif self.fase == "CLASIFICAR":
            self._dibujar_clasificar(pantalla)
        elif self.fase == "ADIVINAR":
            self._dibujar_adivinar(pantalla, posicion_mouse)

    def _dibujar_imagen(self, pantalla, rect):
        if self.imagen_actual is not None:
            pantalla.blit(self.imagen_actual, rect)
        else:
            pygame.draw.rect(pantalla, config.COLOR_BLANCO, rect)
            pygame.draw.rect(pantalla, (40, 40, 40), rect, width=2)
            texto = self.fuente_pequena.render(self.item_actual["nombre"], True, (30, 30, 30))
            pantalla.blit(texto, texto.get_rect(center=rect.center))

    def _dibujar_encabezado(self, pantalla):
        segundos = self.tiempo_restante_ms // 1000
        texto_tiempo = self.fuente_mediana.render(f"Tiempo: {segundos}s", True, (30, 30, 30))
        pantalla.blit(texto_tiempo, (20, 20))

        texto_puntos = self.fuente_mediana.render(f"Puntos: {self.jugador.puntuacion}", True, (30, 30, 30))
        pantalla.blit(texto_puntos, (self.ancho - texto_puntos.get_width() - 20, 20))

    def _dibujar_clasificar(self, pantalla):
        pygame.draw.rect(pantalla, (200, 230, 200), self.caja_hardware_rect, border_radius=12)
        pygame.draw.rect(pantalla, (40, 40, 40), self.caja_hardware_rect, width=2, border_radius=12)
        etiqueta_hw = self.fuente_mediana.render("Hardware", True, (30, 30, 30))
        pantalla.blit(etiqueta_hw, etiqueta_hw.get_rect(center=self.caja_hardware_rect.center))

        pygame.draw.rect(pantalla, (200, 200, 240), self.caja_software_rect, border_radius=12)
        pygame.draw.rect(pantalla, (40, 40, 40), self.caja_software_rect, width=2, border_radius=12)
        etiqueta_sw = self.fuente_mediana.render("Software", True, (30, 30, 30))
        pantalla.blit(etiqueta_sw, etiqueta_sw.get_rect(center=self.caja_software_rect.center))

        ayuda = self.fuente_pequena.render("Arrastrá la imagen a la caja correcta", True, (60, 60, 60))
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
            pygame.draw.line(pantalla, (30, 30, 30), (x, y_palabra + 30), (x + espacio - 10, y_palabra + 30), 3)
            if letra in self.letras_adivinadas:
                superficie = self.fuente_grande.render(letra, True, (30, 30, 30))
                pantalla.blit(superficie, (x, y_palabra))

        if self.letras_falladas:
            texto_falladas = self.fuente_pequena.render(
                "Falladas: " + ", ".join(sorted(self.letras_falladas)), True, (150, 30, 30)
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
        titulo = self.fuente_grande.render("¡Tiempo terminado!", True, (30, 30, 30))
        pantalla.blit(titulo, titulo.get_rect(center=(self.ancho // 2, self.alto // 2 - 100)))

        texto_puntaje = self.fuente_mediana.render(f"Puntaje final: {self.jugador.puntuacion}", True, (30, 30, 30))
        pantalla.blit(texto_puntaje, texto_puntaje.get_rect(center=(self.ancho // 2, self.alto // 2 - 50)))

        self._dibujar_boton(pantalla, self.rect_reintentar, "Reintentar", posicion_mouse)
        self._dibujar_boton(pantalla, self.rect_volver_aula, "Volver al aula", posicion_mouse)

    def _dibujar_boton(self, pantalla, rect, texto, posicion_mouse):
        color = config.COLOR_BLANCO if rect.collidepoint(posicion_mouse) else (225, 225, 225)
        pygame.draw.rect(pantalla, color, rect, border_radius=10)
        pygame.draw.rect(pantalla, (40, 40, 40), rect, width=2, border_radius=10)
        superficie = self.fuente_mediana.render(texto, True, (30, 30, 30))
        pantalla.blit(superficie, superficie.get_rect(center=rect.center))
