import numpy as np
import math


class AgentForaging:
    def __init__(self, agent_id, ambiente, estrategia):
        self.agent_id = agent_id
        self.mundo = ambiente
        self.estrategia = estrategia
        self.acoes = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Dir, Esq, Baixo, Cima
        self.contador_passos = 0
        self.ultima_acao = 0
        self.posicao_anterior = (-1, -1)  # Para detetar se ficou parado

    def observar(self):
        s = self.mundo.size
        data = self.mundo.agents_data[self.agent_id]

        px = data['x'] / s
        py = data['y'] / s
        carga = 1.0 if data['carregando'] else 0.0

        sensores = []
        for dx, dy in self.acoes:
            sx, sy = data['x'] + dx, data['y'] + dy


            if not (0 <= sx < s and 0 <= sy < s) or self.mundo.grid[sx][sy].tipo == "OBSTACLE":
                sensores.append(-1.0)

            elif self.mundo.grid[sx][sy].tipo == "RESOURCE":
                sensores.append(1.0)

            elif self.mundo.grid[sx][sy].tipo == "NEST":
                sensores.append(0.5)

            elif self.mundo.grid[sx][sy].ocupado is not None and self.mundo.grid[sx][sy].ocupado != self.agent_id:
                sensores.append(-0.5)
            else:
                sensores.append(0.0)

        memoria_acao = [0.0, 0.0, 0.0, 0.0]
        if 0 <= self.ultima_acao < 4:
            memoria_acao[self.ultima_acao] = 1.0

        estado = np.concatenate(([px, py, carga], np.array(sensores), np.array(memoria_acao)))
        return estado.astype(float)

    def passo(self, treino=True):
        estado = self.observar()


        pos_atual = (self.mundo.agents_data[self.agent_id]['x'], self.mundo.agents_data[self.agent_id]['y'])

        acao_idx = self.estrategia.escolher_acao(estado)
        self.ultima_acao = acao_idx

        recompensa, moveu_se = self.mundo.agir(self.agent_id, acao_idx)


        if not moveu_se:

            recompensa -= 2.0
        elif pos_atual == self.posicao_anterior:

            recompensa -= 0.5
        else:

            recompensa += 0.1

        self.posicao_anterior = pos_atual

        prox_estado = self.observar()
        done = False

        if treino:
            self.estrategia.guardar_experiencia(estado, acao_idx, recompensa, prox_estado, done)
            self.contador_passos += 1
            if self.contador_passos % 5 == 0:
                self.estrategia.treinar_batch()

        return done