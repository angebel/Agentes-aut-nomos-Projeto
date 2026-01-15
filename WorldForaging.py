import random
import math
from Projeto.ambiente.Cell import Cell
from Projeto.ambiente.Objects import Ground, Obstacle, Resource, Nest


class WorldForaging:
    def __init__(self, size=10, num_resources=15, num_obstacles=2, num_agents=2):
        self.size = size
        self.grid = [[Cell(x, y) for y in range(size)] for x in range(size)]
        self.agents_data = {}


        for i in range(num_agents):
            self.adicionar_agente(i)

        self.resources = []
        self.reset_map(num_resources, num_obstacles)

    def reset_map(self, num_resources, num_obstacles):
        self.resources = []


        for x in range(self.size):
            for y in range(self.size):
                self.grid[x][y].tipo = "GROUND"
                self.grid[x][y].conteudo = Ground(x, y)
                self.grid[x][y].ocupado = None


        self.grid[0][0].tipo = "NEST"
        self.grid[0][0].conteudo = Nest(0, 0)


        count = 0
        while count < num_obstacles:
            ox, oy = random.randint(0, self.size - 1), random.randint(0, self.size - 1)

            locais_proibidos = [(0, 0), (1, 0), (0, 1)]

            if (ox, oy) not in locais_proibidos:
                self.grid[ox][oy].tipo = "OBSTACLE"
                self.grid[ox][oy].conteudo = Obstacle(ox, oy)
                count += 1


        for _ in range(num_resources):
            self.adicionar_recurso_aleatorio()




        if 0 in self.agents_data:
            self.agents_data[0]['x'] = 1
            self.agents_data[0]['y'] = 0
            self.agents_data[0]['carregando'] = False
            self.agents_data[0]['pontos'] = 0
            self.grid[1][0].ocupado = 0


        if 1 in self.agents_data:
            self.agents_data[1]['x'] = 0
            self.agents_data[1]['y'] = 1
            self.agents_data[1]['carregando'] = False
            self.agents_data[1]['pontos'] = 0
            self.grid[0][1].ocupado = 1

    def adicionar_agente(self, id_agente):
        self.agents_data[id_agente] = {
            'x': 0, 'y': 0,
            'carregando': False,
            'pontos': 0
        }

    def adicionar_recurso_aleatorio(self):
        tries = 0
        while tries < 100:
            rx, ry = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            locais_proibidos = [(0, 0), (1, 0), (0, 1)]
            if self.grid[rx][ry].tipo == "GROUND" and (rx, ry) not in locais_proibidos and self.grid[rx][
                ry].ocupado is None:
                res = Resource(rx, ry)
                self.grid[rx][ry].tipo = "RESOURCE"
                self.grid[rx][ry].conteudo = res
                self.resources.append(res)
                break
            tries += 1

    def agir(self, id_agente, acao_idx):
        data = self.agents_data[id_agente]
        cx, cy = data['x'], data['y']

        # 0: Dir, 1: Esq, 2: Baixo, 3: Cima
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        dx, dy = deltas[acao_idx]

        nx, ny = cx + dx, cy + dy
        recompensa = -0.1
        moveu_se = False


        fora = not (0 <= nx < self.size and 0 <= ny < self.size)
        obstaculo = False
        ocupado_por_outro = False

        if not fora:
            obstaculo = (self.grid[nx][ny].tipo == "OBSTACLE")
            quem_la = self.grid[nx][ny].ocupado
            if quem_la is not None and quem_la != id_agente:
                ocupado_por_outro = True

        if fora or obstaculo or ocupado_por_outro:
            return -0.5, False


        if self.grid[cx][cy].ocupado == id_agente:
            self.grid[cx][cy].ocupado = None

        data['x'] = nx
        data['y'] = ny
        self.grid[nx][ny].ocupado = id_agente
        moveu_se = True


        tipo = self.grid[nx][ny].tipo

        if tipo == "RESOURCE" and not data['carregando']:
            data['carregando'] = True
            self.grid[nx][ny].tipo = "GROUND"

            for r in self.resources:
                if r.x == nx and r.y == ny:
                    self.resources.remove(r)
                    break

            recompensa = 20.0


        elif tipo == "NEST" and data['carregando']:
            data['carregando'] = False
            data['pontos'] += 10
            recompensa = 50.0

        return recompensa, moveu_se

    def render(self):
        RESET = "\033[0m"
        RED = "\033[91m"
        BLUE = "\033[94m"
        GREEN = "\033[92m"
        MAGENTA = "\033[95m"
        GRAY = "\033[90m"
        BOLD = "\033[1m"

        print("\n" + "=" * 30)
        p1 = self.agents_data[0]['pontos']
        p2 = self.agents_data[1]['pontos']
        print(f"{BOLD}PLACAR:{RESET} {RED}Agente 1: {p1}{RESET} | {BLUE}Agente 2: {p2}{RESET}")
        print("-" * 30)

        for y in range(self.size):
            row = ""
            for x in range(self.size):
                cell = self.grid[x][y]

                if cell.ocupado is not None:
                    if cell.ocupado == 0:
                        row += f" {RED}A1{RESET} "
                    else:
                        row += f" {BLUE}A2{RESET} "
                elif cell.tipo == "NEST":
                    row += f"{MAGENTA}[N]{RESET}"
                elif cell.tipo == "RESOURCE":
                    row += f" {GREEN}${RESET} "
                elif cell.tipo == "OBSTACLE":
                    row += f" {GRAY}#{RESET} "
                else:
                    row += " . "
            print(row)
        print("=" * 30)