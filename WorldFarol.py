from Projeto.ambiente.Cell import Cell
from Projeto.ambiente.Objects import Ground, Obstacle, Lighthouse


class WorldFarol:
    def __init__(self, size=6):
        self.size = size
        self.grid = [[Cell(x, y) for y in range(size)] for x in range(size)]
        self.reset_map()

    def reset_map(self):
        self.agentx = 0
        self.agenty = 0
        self.chegou = False

        # 1. Chão
        for x in range(self.size):
            for y in range(self.size):
                self.grid[x][y].tipo = "GROUND"
                self.grid[x][y].conteudo = Ground(x, y)


        obs = [(1, 1), (1, 4), (4, 1), (4, 4), (2, 2), (3, 3), (2, 4)]
        for (ox, oy) in obs:
            self.grid[ox][oy].tipo = "OBSTACLE"
            self.grid[ox][oy].conteudo = Obstacle(ox, oy)


        fx = self.size - 1
        fy = self.size - 1
        self.farol_x = fx
        self.farol_y = fy
        self.grid[fx][fy].tipo = "LIGHTHOUSE"
        self.grid[fx][fy].conteudo = Lighthouse("Farol", fx, fy)

    def force_farol(self, x, y):
        self.grid[self.farol_x][self.farol_y].tipo = "GROUND"
        self.farol_x, self.farol_y = x, y
        self.grid[x][y].tipo = "LIGHTHOUSE"
        self.grid[x][y].conteudo = Lighthouse("Farol", x, y)

    def render(self):
        print(f"\n--- MAPA {self.size}x{self.size} ---")
        for y in range(self.size):
            row = ""
            for x in range(self.size):
                if (x, y) == (self.agentx, self.agenty):
                    row += " A "
                else:
                    t = self.grid[x][y].tipo
                    if t == "OBSTACLE":
                        row += " # "
                    elif t == "LIGHTHOUSE":
                        row += "[F]"
                    else:
                        row += " . "
            print(row)