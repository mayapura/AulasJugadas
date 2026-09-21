import pygame


def cargar_imagen(ruta, tamano=None):
    """Carga una imagen desde disco. Devuelve None si no se encuentra."""
    try:
        imagen = pygame.image.load(ruta)
        if tamano:
            imagen = pygame.transform.smoothscale(imagen, tamano)
        return imagen
    except (FileNotFoundError, pygame.error):
        print(f"Nota: No se encontró la imagen '{ruta}'.")
        return None


def cargar_sonido(ruta):
    """Carga un efecto de sonido. Devuelve None si no se encuentra."""
    try:
        return pygame.mixer.Sound(ruta)
    except (FileNotFoundError, pygame.error):
        print(f"Nota: No se encontró el sonido '{ruta}'.")
        return None


def cargar_musica(ruta, volumen=0.3, loop=True):
    """Carga y reproduce la música de fondo. Devuelve False si no se encuentra."""
    try:
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.set_volume(volumen)
        pygame.mixer.music.play(-1 if loop else 0)
        return True
    except (FileNotFoundError, pygame.error):
        print(f"Nota: No se encontró la música '{ruta}'. El juego seguirá sin música.")
        return False
