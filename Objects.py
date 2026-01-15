# --- 1. CLASSE MÃE ---
class Object:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

# --- 2. SUBCLASSES ---
class Ground(Object):
    def __init__(self, x, y):
        super().__init__("Ground", x, y)

class Obstacle(Object):
    def __init__(self, x, y):
        super().__init__("Obstacle", x, y)

class Resource(Object):
    def __init__(self, x, y, valor=10):
        super().__init__("Resource", x, y)
        self.valor = valor

class Nest(Object):
    def __init__(self, x, y):
        super().__init__("Nest", x, y)

class Lighthouse(Object):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)

class MagicPill(Object):
    def __init__(self, arg1, arg2, arg3=None):
        if arg3 is not None:
            super().__init__(arg1, arg2, arg3)
        else:
            super().__init__("Pill", arg1, arg2)