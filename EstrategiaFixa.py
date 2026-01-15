import random


class EstrategiaFixa:


    def __init__(self):
        self.epsilon = 0.0
        self.num_actions = 4

    def guardar_experiencia(self, s, a, r, s2, done):
        pass

    def treinar_batch(self):
        pass

    def escolher_acao(self, estado):


        tem_carga = (estado[2] == 1.0)
        sensores = [estado[3], estado[4], estado[5], estado[6]]
        acoes_possiveis = [0, 1, 2, 3]


        acoes_seguras = []
        for i in acoes_possiveis:
            if sensores[i] >= 0.0:
                acoes_seguras.append(i)

        if not acoes_seguras:
            return random.choice(acoes_possiveis)


        objetivo = 0.5 if tem_carga else 1.0


        for acao in acoes_seguras:
            if sensores[acao] == objetivo:
                return acao


        return random.choice(acoes_seguras)


class EstrategiaAleatoria:


    def __init__(self):
        self.epsilon = 0.0

    def guardar_experiencia(self, s, a, r, s2, done): pass

    def treinar_batch(self): pass

    def escolher_acao(self, estado):
        sensores = [estado[3], estado[4], estado[5], estado[6]]
        seguras = [i for i, val in enumerate(sensores) if val != -1.0]

        if seguras:
            return random.choice(seguras)
        return random.randint(0, 3)