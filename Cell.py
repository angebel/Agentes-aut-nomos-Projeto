
class Cell:
    def __init__(self, x, y, tipo="GROUND", conteudo=None):

        self.x = x
        self.y = y
        self.tipo = tipo
        self.conteudo = None

    def is_walkable(self):

        return self.tipo != "OBSTACLE"

    def __repr__(self):
        return f"Cell({self.x},{self.y}, tipo={self.tipo})"
