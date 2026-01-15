import random
import numpy as np
import torch
import torch.optim as optim
import torch.nn as nn
from collections import deque
from Projeto.agente.DQN import DQN


class Estrategia:
    def __init__(self, input_size, num_actions, lr=0.001):
        self.model = DQN(input_size, num_actions)


        self.optimizer = optim.Adam(self.model.parameters(), lr=0.0005)
        self.loss_fn = nn.MSELoss()

        self.memory = deque(maxlen=20000)
        self.gamma = 0.99

        self.epsilon = 1.0
        self.epsilon_min = 0.1


        self.epsilon_decay = 0.9995

        self.num_actions = num_actions

    def escolher_acao(self, estado):
        if random.random() < self.epsilon:
            return random.randint(0, self.num_actions - 1)

        estado = torch.tensor(estado, dtype=torch.float32)
        qvals = self.model(estado)
        return int(torch.argmax(qvals).item())

    def guardar_experiencia(self, s, a, r, s2, done):
        self.memory.append((s, a, r, s2, done))

    def treinar_batch(self, batch_size=64):
        if len(self.memory) < batch_size:
            return

        batch = random.sample(self.memory, batch_size)
        estados, acoes, recompensas, proxs, dones = zip(*batch)

        estados = torch.tensor(np.array(estados), dtype=torch.float32)
        proxs = torch.tensor(np.array(proxs), dtype=torch.float32)
        acoes = torch.tensor(acoes)
        recompensas = torch.tensor(np.array(recompensas), dtype=torch.float32)
        dones = torch.tensor(np.array(dones), dtype=torch.float32)

        qvals = self.model(estados).gather(1, acoes.unsqueeze(1)).squeeze()

        with torch.no_grad():
            prox_qvals = self.model(proxs).max(1)[0]
            alvos = recompensas + self.gamma * prox_qvals * (1 - dones)

        perda = self.loss_fn(qvals, alvos)

        self.optimizer.zero_grad()
        perda.backward()
        self.optimizer.step()

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay