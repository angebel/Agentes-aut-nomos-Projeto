import numpy as np


class AgentFarol:
    def __init__(self, estrategia):
        self.estrategia = estrategia
        self.mundo = None
        self.acoes = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        self.posicao_final = (0, 0)
        self.novidade = 0.0
        self.score_final = 0.0

        # MEMÓRIA E ESTADO
        self.last_action = -1
        self.steps_taken = 0
        self.visited_cells = set()
        self.bates_parede = 0

    def observar(self):
        x, y = self.mundo.agentx, self.mundo.agenty
        s = self.mundo.size

        # 1. Sensores de Parede
        sensors = []
        for dx, dy in self.acoes:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < s and 0 <= ny < s) or \
                    self.mundo.grid[nx][ny].tipo == "OBSTACLE":
                sensors.append(1.0)
            elif (nx, ny) in self.visited_cells:
                sensors.append(0.5)
            else:
                sensors.append(-1.0)


        fx, fy = self.mundo.farol_x, self.mundo.farol_y

        # Calcular vetor normalizado para o farol
        dir_x = (fx - x) / (s - 1)
        dir_y = (fy - y) / (s - 1)

        memoria_acao = (self.last_action / 3.0) if self.last_action != -1 else -1.0
        tempo = (self.steps_taken / 40.0)


        return np.array(sensors + [dir_x, dir_y, memoria_acao, tempo])

    def agir(self):
        inputs = self.observar()
        acao_idx = self.estrategia.escolher_acao(inputs)

        self.last_action = acao_idx
        self.steps_taken += 1

        dx, dy = self.acoes[acao_idx]
        nx = self.mundo.agentx + dx
        ny = self.mundo.agenty + dy

        if (0 <= nx < self.mundo.size and 0 <= ny < self.mundo.size) and \
                self.mundo.grid[nx][ny].tipo != "OBSTACLE":
            self.mundo.agentx = nx
            self.mundo.agenty = ny
            self.visited_cells.add((nx, ny))

            if self.mundo.grid[nx][ny].tipo == "LIGHTHOUSE":
                return True

        return False