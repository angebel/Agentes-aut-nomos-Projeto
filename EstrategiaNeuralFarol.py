import numpy as np


class EstrategiaNeuralFarol:
    def __init__(self, n_inputs, n_actions,weights_path=None):
        self.n_inputs = n_inputs
        self.n_hidden = 8
        self.n_actions = n_actions


        self.w1 = np.random.uniform(-1, 1, (n_inputs, self.n_hidden))
        self.b1 = np.random.uniform(-1, 1, (self.n_hidden,))
        self.w2 = np.random.uniform(-1, 1, (self.n_hidden, n_actions))
        self.b2 = np.random.uniform(-1, 1, (n_actions,))
        
        if weights_path is not None:
            data = np.load(weights_path)
            self.w1 = data["w1"]
            self.b1 = data["b1"]
            self.w2 = data["w2"]
            self.b2 = data["b2"]

    def escolher_acao(self, inputs):

        hidden = np.tanh(np.dot(inputs, self.w1) + self.b1)

        output = np.tanh(np.dot(hidden, self.w2) + self.b2)

        return np.argmax(output)

    def mutar(self, power=0.1):

        self.w1 += np.random.normal(0, power, self.w1.shape)
        self.b1 += np.random.normal(0, power, self.b1.shape)
        self.w2 += np.random.normal(0, power, self.w2.shape)
        self.b2 += np.random.normal(0, power, self.b2.shape)


        limit = 5.0
        self.w1 = np.clip(self.w1, -limit, limit)
        self.b1 = np.clip(self.b1, -limit, limit)
        self.w2 = np.clip(self.w2, -limit, limit)
        self.b2 = np.clip(self.b2, -limit, limit)