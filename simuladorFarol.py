import os
import time
import math
import random
import numpy as np
import matplotlib.pyplot as plt

from Projeto.ambiente.WorldFarol import WorldFarol
from Projeto.agente.AgentFarol import AgentFarol
from Projeto.agente.EstrategiaNeuralFarol import EstrategiaNeuralFarol


class simuladorFarol:
    def __init__(self, pop_size=50, weights_path="best_farol.npz"):
        self.pop_size = pop_size
        self.archive_threshold = 1.5
        self.k_nearest = 5
        self.archive = []

        self.weights_path = weights_path


        self.populacao = []
        for _ in range(self.pop_size):
            strat = EstrategiaNeuralFarol(8, 4)  
            self.populacao.append(AgentFarol(strat))

        self.historico_passos = []

    def calcular_novidade(self, agente, vizinhos):
        todos = self.archive + vizinhos
        distancias = []
        ax, ay = agente.posicao_final

        for (vx, vy) in todos:
            d = math.sqrt((ax - vx) ** 2 + (ay - vy) ** 2)
            if d > 0:
                distancias.append(d)

        distancias.sort()
        if not distancias:
            return 0.0

        k = min(len(distancias), self.k_nearest)
        return sum(distancias[:k]) / k

 
    def guardar_melhor(self, estrategia):
        os.makedirs(os.path.dirname(self.weights_path) or ".", exist_ok=True)
        np.savez(
            self.weights_path,
            w1=estrategia.w1, b1=estrategia.b1,
            w2=estrategia.w2, b2=estrategia.b2
        )

    def treinar(self, total_episodios=2000, limite_inicial=80, limite_final=15):
        print(f"--- TREINO DE OTIMIZAÇÃO DESCENDENTE ({total_episodios} Eps) ---")
        start = time.time()

        melhor_agente_global = None
        melhor_steps_global = float("inf")
        melhor_wallhits_global = float("inf")

        for ep in range(1, total_episodios + 1):
            posicoes_finais = []
            sucessos = []
            passos_registados = []

  
            progresso = ep / total_episodios
            max_passos_atual = int(limite_inicial - (limite_inicial - limite_final) * progresso)
    
            random.seed(ep)
            np.random.seed(ep)

            for agente in self.populacao:
                env = WorldFarol(size=6)
                agente.mundo = env

                agente.visited_cells = set([(0, 0)])
                agente.steps_taken = 0
                agente.last_action = -1
                agente.bates_parede = 0

                chegou = False

                for _ in range(max_passos_atual):
                    x_antes, y_antes = env.agentx, env.agenty

                    if agente.agir():
                        chegou = True
                        break

                    if env.agentx == x_antes and env.agenty == y_antes:
                        agente.bates_parede += 1

                if chegou:
                    passos_registados.append(agente.steps_taken)
                    sucessos.append(agente)
                else:
                    passos_registados.append(max_passos_atual)

                agente.posicao_final = (env.agentx, env.agenty)
                posicoes_finais.append(agente.posicao_final)

            self.historico_passos.append(float(np.mean(passos_registados)))

            if sucessos:
                vencedor = min(sucessos, key=lambda a: (a.steps_taken, a.bates_parede))

                melhorou = (
                    vencedor.steps_taken < melhor_steps_global or
                    (vencedor.steps_taken == melhor_steps_global and vencedor.bates_parede < melhor_wallhits_global)
                )

                if melhorou:
                    melhor_steps_global = vencedor.steps_taken
                    melhor_wallhits_global = vencedor.bates_parede

                    melhor_agente_global = EstrategiaNeuralFarol(8, 4)
                    melhor_agente_global.w1 = vencedor.estrategia.w1.copy()
                    melhor_agente_global.b1 = vencedor.estrategia.b1.copy()
                    melhor_agente_global.w2 = vencedor.estrategia.w2.copy()
                    melhor_agente_global.b2 = vencedor.estrategia.b2.copy()

                    # guarda logo o melhor atualizado
                    self.guardar_melhor(melhor_agente_global)

            # --- calcular novelty + fitness ---
            for agente in self.populacao:
                nov = self.calcular_novidade(agente, posicoes_finais)
                agente.novidade = nov

                if nov > self.archive_threshold and agente.posicao_final not in self.archive:
                    self.archive.append(agente.posicao_final)

                fitness = len(agente.visited_cells) * 2
                fitness -= agente.bates_parede * 5.0

                if agente.mundo.chegou:
                    fitness += 200 + (max_passos_atual - agente.steps_taken) * 5

                agente.score_final = nov + max(0, fitness)

            if ep % 200 == 0:
                print(f"Ep {ep} (Limite={max_passos_atual}): Média passos={np.mean(passos_registados):.1f}")

            self.populacao.sort(key=lambda x: x.score_final, reverse=True)

            nova_pop = []
            # 
            nova_pop.extend(self.populacao[:5])

            if melhor_agente_global is not None:
                campeao_strat = EstrategiaNeuralFarol(8, 4)
                campeao_strat.w1 = melhor_agente_global.w1.copy()
                campeao_strat.b1 = melhor_agente_global.b1.copy()
                campeao_strat.w2 = melhor_agente_global.w2.copy()
                campeao_strat.b2 = melhor_agente_global.b2.copy()
                campeao_strat.mutar(power=0.01)
                nova_pop.append(AgentFarol(campeao_strat))

            pais = self.populacao[:20]

            while len(nova_pop) < self.pop_size:
                pai = random.choice(pais)

                nova_strat = EstrategiaNeuralFarol(8, 4)
                nova_strat.w1 = pai.estrategia.w1.copy()
                nova_strat.b1 = pai.estrategia.b1.copy()
                nova_strat.w2 = pai.estrategia.w2.copy()
                nova_strat.b2 = pai.estrategia.b2.copy()
                nova_strat.mutar(power=0.2)

                nova_pop.append(AgentFarol(nova_strat))

            self.populacao = nova_pop

        print(f"Tempo total: {time.time() - start:.1f}s")

        self.desenhar_graficos_finais()

        # demonstração + teste do melhor
        if melhor_agente_global is not None:
            self.demonstrar(AgentFarol(melhor_agente_global))
            self.testar(
                estrategia=melhor_agente_global,
                n_episodios=200,
                max_passos=40,
                seeds=list(range(200)),
                farol_fixo=True,
                render=False
            )
        else:
            print("Não foi encontrado nenhum agente global com sucesso durante o treino.")

  
    def desenhar_graficos_finais(self):
        plt.figure(figsize=(10, 6))
        dados = np.array(self.historico_passos)

        window_size = 100
        if len(dados) >= window_size:
            window = np.ones(window_size) / window_size
            dados_suavizados = np.convolve(dados, window, mode='valid')
            x_axis = range(window_size // 2, len(dados) - window_size // 2 + 1)
            plt.plot(dados, alpha=0.2, label="Por Episódio")
            plt.plot(x_axis, dados_suavizados, linewidth=2, label="Tendência")
        else:
            plt.plot(dados, label="Por Episódio")

        plt.title("Curva de Aprendizagem")
        plt.xlabel("Episódios")
        plt.ylabel("Passos médios")
        plt.legend()
        plt.grid(True, alpha=0.2)
        plt.show(block=False)


    def demonstrar(self, agente):
        print("\n--- DEMONSTRAÇÃO FINAL ---")
        env = WorldFarol(size=6)
        env.force_farol(5, 5)

        agente.mundo = env
        agente.visited_cells = set([(0, 0)])
        agente.steps_taken = 0
        agente.last_action = -1
        agente.bates_parede = 0

        env.render()

        for i in range(40):
            time.sleep(0.3)
            x_ant, y_ant = env.agentx, env.agenty
            venceu = agente.agir()

            if env.agentx == x_ant and env.agenty == y_ant:
                print("!Colisão!")

            env.render()
            if venceu:
                print(f"SUCESSO EM {i + 1} PASSOS")
                break

        plt.show()



    def testar(self, estrategia, n_episodios=200, max_passos=40, seeds=None, farol_fixo=True, render=False):
        if seeds is None:
            seeds = list(range(n_episodios))

        sucessos = 0
        steps_sucesso = []
        steps_todos = []
        wall_hits = []
        coverages = []
        final_dists = []

        for sd in seeds:
            random.seed(sd)
            np.random.seed(sd)

            env = WorldFarol(size=6)
            if farol_fixo:
                env.force_farol(5, 5)

            agente = AgentFarol(estrategia)
            agente.mundo = env
            agente.visited_cells = set([(0, 0)])
            agente.steps_taken = 0
            agente.last_action = -1
            agente.bates_parede = 0

            chegou = False

            if render:
                env.render()

            for _ in range(max_passos):
                x_ant, y_ant = env.agentx, env.agenty
                venceu = agente.agir()

                if env.agentx == x_ant and env.agenty == y_ant:
                    agente.bates_parede += 1

                if render:
                    time.sleep(0.05)
                    env.render()

                if venceu:
                    chegou = True
                    break

            steps_todos.append(agente.steps_taken if chegou else max_passos)
            wall_hits.append(agente.bates_parede)
            coverages.append(len(agente.visited_cells))

            try:
                fx, fy = env.farolx, env.faroly
            except:
                fx, fy = 5, 5

            dist = math.sqrt((env.agentx - fx) ** 2 + (env.agenty - fy) ** 2)
            final_dists.append(dist)

            if chegou:
                sucessos += 1
                steps_sucesso.append(agente.steps_taken)

        n = len(seeds)
        print("\n--- TESTE (Modo de Avaliação) ---")
        print(f"Episódios: {n}")
        print(f"Taxa de sucesso: {100.0 * sucessos / n:.1f}%")
        print(f"Passos médios (todos): {np.mean(steps_todos):.2f}")
        if steps_sucesso:
            print(f"Passos médios (só sucessos): {np.mean(steps_sucesso):.2f}")
        print(f"Colisões médias: {np.mean(wall_hits):.2f}")
        print(f"Cobertura média (células visitadas): {np.mean(coverages):.2f}")
        print(f"Distância final média ao farol: {np.mean(final_dists):.2f}")
