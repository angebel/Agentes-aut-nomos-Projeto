import random


class EstrategiaFarolFixa:
    def __init__(self, n_inputs=8, n_actions=4):
        self.n_inputs = n_inputs
        self.n_actions = n_actions

    def escolher_acao(self, percepcao):
        """
        percepcao[0:4] -> Sensores (Cima, Baixo, Esq, Dir)
        percepcao[4]   -> Direção X para o Farol (dx)
        percepcao[5]   -> Direção Y para o Farol (dy)
        """


        dx = percepcao[4]
        dy = percepcao[5]

        possiveis_acoes = []


        if dy > 0 and percepcao[1] < 1.0:
            possiveis_acoes.append(1)  # Baixo

        elif dy < 0 and percepcao[0] < 1.0:
            possiveis_acoes.append(0)  # Cima


        if dx > 0 and percepcao[3] < 1.0:
            possiveis_acoes.append(3)

        elif dx < 0 and percepcao[2] < 1.0:
            possiveis_acoes.append(2)


        if possiveis_acoes:
            return random.choice(possiveis_acoes)


        livres = [i for i in range(4) if percepcao[i] < 1.0]
        if livres:
            return random.choice(livres)

        return random.randint(0, 3)