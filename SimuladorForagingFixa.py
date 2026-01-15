import time
import numpy as np
import matplotlib.pyplot as plt
from Projeto.ambiente.WorldForaging import WorldForaging
from Projeto.agente.AgentForaging import AgentForaging
from Projeto.agente.EstrategiaForaging import Estrategia  # O teu DQN

# IMPORTANTE: Caminho para a tua nova pasta
from Projeto.agente.EstrategiaFixa import EstrategiaFixa


class SimuladorForagingFixa:
    def __init__(self):

        self.env = WorldForaging(size=10, num_resources=40, num_obstacles=2, num_agents=2)


        self.estrategia_ia = Estrategia(input_size=11, num_actions=4)
        self.estrategia_fixa = EstrategiaFixa()

        self.agente1 = AgentForaging(agent_id=0, ambiente=self.env, estrategia=self.estrategia_ia)
        self.agente2 = AgentForaging(agent_id=1, ambiente=self.env, estrategia=self.estrategia_fixa)

        self.historico_p1 = []
        self.historico_p2 = []

    def treinar(self, total_episodios=2000):
        print(f"--- COMBATE: DQN (A1) vs FIXO (A2) ---")
        start = time.time()

        print(f"{'Episódio':^10} | {'DQN Pts':^8} | {'Fixo Pts':^8} | {'Vencedor':^10} | {'Epsilon':^8}")
        print("-" * 65)

        for ep in range(1, total_episodios + 1):
            self.env.reset_map(num_resources=40, num_obstacles=2)
            passos = 0
            self.agente1.contador_passos = 0
            self.agente2.contador_passos = 0

            while passos < 200:
                self.agente1.passo(treino=True)  # DQN treina
                self.agente2.passo(treino=False)  # Fixo só joga
                passos += 1

            p1 = self.env.agents_data[0]['pontos']
            p2 = self.env.agents_data[1]['pontos']
            self.historico_p1.append(p1)
            self.historico_p2.append(p2)

            if ep % 100 == 0:
                eps = self.agente1.estrategia.epsilon
                vencedor = "DQN" if p1 > p2 else ("FIXO" if p2 > p1 else "Empate")
                print(f"{ep:^10} | {p1:^8} | {p2:^8} | {vencedor:^10} | {eps:^8.3f}")

        print(f"\n--- FIM DO COMBATE ({time.time() - start:.1f}s) ---")
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
        plt.plot(media_p1, color='red', linewidth=2, label="Agente DQN (Média)")

        plt.plot(self.historico_p2, color='blue', alpha=0.15)
        plt.plot(media_p2, color='blue', linewidth=2, label="Agente Fixo (Média)")

        plt.title("Evolução: Inteligência Artificial vs Regras Fixas")
        plt.xlabel("Episódios de Treino")
        plt.ylabel("Pontos Recolhidos")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

    def demonstrar(self):
        print("\n\n")
        print("=" * 40)
        print("       DEMONSTRAÇÃO VISUAL FINAL       ")
        print("=" * 40)
        input(">>> Pressiona [ENTER] para iniciar... <<<")

        self.env.reset_map(num_resources=40, num_obstacles=2)
        if hasattr(self.agente1.estrategia, 'epsilon'):
            self.agente1.estrategia.epsilon = 0.05  # DQN em modo expert

        total_passos = 100
        for i in range(total_passos):
            print(f"\n--- PASSO {i + 1} de {total_passos} ---")
            self.agente1.passo(treino=False)
            self.agente2.passo(treino=False)
            self.env.render()
            time.sleep(0.1)

        print(
            f"\nRESULTADO FINAL -> DQN: {self.env.agents_data[0]['pontos']} | FIXO: {self.env.agents_data[1]['pontos']}")