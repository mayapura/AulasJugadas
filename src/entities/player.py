class Player:
    """Progreso del jugador. Todavía no se usa en el juego, preparado para cuando
    los minijuegos empiecen a otorgar puntos y marcar actividades completadas."""

    def __init__(self, nombre="Jugador"):
        self.nombre = nombre
        self.puntuacion = 0
        self.minijuegos_completados = []

    def sumar_puntos(self, puntos):
        self.puntuacion += puntos

    def completar_minijuego(self, nombre_minijuego):
        if nombre_minijuego not in self.minijuegos_completados:
            self.minijuegos_completados.append(nombre_minijuego)
