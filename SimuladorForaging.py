import time
import numpy as np
import matplotlib.pyplot as plt
from Projeto.ambiente.WorldForaging import WorldForaging
from Projeto.agente.AgentForaging import AgentForaging
from Projeto.agente.EstrategiaForaging import Estrategia


class SimuladorForaging:
    def __init__(self):

        self.env = WorldForaging(size=10, num_resources=40, num_obstacles=2, num_agents=2)


        self.estrategia1 = Estrategia(input_size=11, num_actions=4)
        self.estrategia2 = Estrategia(input_size=11, num_actions=4)


        self.agente1 = AgentForaging(agent_id=0, ambiente=self.env, estrategia=self.estrategia1)
        self.agente2 = AgentForaging(agent_id=1, ambiente=self.env, estrategia=self.estrategia2)

        self.historico_p1 = []
        self.historico_p2 = []

    def treinar(self, total_episodios=2000):
        print(f"--- TREINO MARL (SPAWN 1,0 e 0,1) ---")
        start = time.time()

        print(f"{'Episódio':^10} | {'A1 Pts':^8} | {'A2 Pts':^8} | {'Vencedor':^10} | {'Epsilon':^8}")
        print("-" * 60)

        for ep in range(1, total_episodios + 1):
            self.env.reset_map(num_resources=40, num_obstacles=2)
            passos = 0
            self.agente1.contador_passos = 0
            self.agente2.contador_passos = 0

            while passos < 200:
                self.agente1.passo(treino=True)
                self.agente2.passo(treino=True)
                passos += 1

            p1 = self.env.agents_data[0]['pontos']
            p2 = self.env.agents_data[1]['pontos']
            self.historico_p1.append(p1)
            self.historico_p2.append(p2)

            if ep % 100 == 0:
                eps = self.agente1.estrategia.epsilon
                vencedor = "A1" if p1 > p2 else ("A2" if p2 > p1 else "Empate")
                print(f"{ep:^10} | {p1:^8} | {p2:^8} | {vencedor:^10} | {eps:^8.3f}")

        print(f"\n--- FIM DO TREINO ({time.time() - start:.1f}s) ---")
        self.desenhar_grafico_competicao()
        self.demonstrar()

    def desenhar_grafico_competicao(self):
        plt.figure(figsize=(12, 6))

        def media_movel(lista, janela=50):
            media = []
            for i in range(len(lista)):
                start = max(0, i - janela)
                media.append(np.mean(lista[start:i + 1]))
            return media

        media_p1 = media_movel(self.historico_p1)
        media_p2 = media_movel(self.historico_p2)

        plt.plot(self.historico_p1, color='red', alpha=0.15)
        plt.plot(media_p1, color='red', linewidth=2, label="Agente 1 (Média)")

        plt.plot(self.historico_p2, color='blue', alpha=0.15)
        plt.plot(media_p2, color='blue', linewidth=2, label="Agente 2 (Média)")

        plt.title("Competição MARL (Spawns Corrigidos)")
        plt.xlabel("Episódios")
        plt.ylabel("Pontos Recolhidos")
        plt.legend()
        plt.grid(True, alpha=0.3)
        print("A fechar gráfico para iniciar demonstração visual...")
        plt.show()

    def demonstrar(self):
        print("\n\n")
        print("=" * 40)
        print("       DEMONSTRAÇÃO VISUAL FINAL       ")
        print("=" * 40)

        input(">>> Pressiona [ENTER] para iniciar... <<<")

        self.env.reset_map(num_resources=40, num_obstacles=2)

        if hasattr(self.agente1.estrategia, 'epsilon'):
            self.agente1.estrategia.epsilon = 0.1
        if hasattr(self.agente2.estrategia, 'epsilon'):
            self.agente2.estrategia.epsilon = 0.1

        total_passos = 100
        for i in range(total_passos):
            print(f"\n--- PASSO {i + 1} de {total_passos} ---")
            self.agente1.passo(treino=False)
            self.agente2.passo(treino=False)
            self.env.render()
            time.sleep(0.1)

        print(
            f"\nRESULTADO FINAL DEMO -> A1: {self.env.agents_data[0]['pontos']} | A2: {self.env.agents_data[1]['pontos']}")