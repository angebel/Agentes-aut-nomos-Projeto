import random


class EstrategiaFarolAleatoria:
    def __init__(self, n_inputs=8, n_actions=4):
        self.n_inputs = n_inputs
        self.n_actions = n_actions

    def escolher_acao(self, percepcao):

        sensores = percepcao[:4]
        acoes_seguras = [i for i, val in enumerate(sensores) if val < 1.0]

        if acoes_seguras:
            return random.choice(acoes_seguras)


        return random.randint(0, self.n_actions - 1)