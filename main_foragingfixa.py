import numpy as np
import matplotlib.pyplot as plt
import time
from Projeto.ambiente.WorldForaging import WorldForaging
from Projeto.agente.AgentForaging import AgentForaging


from Projeto.agente.EstrategiaForaging import Estrategia

from Projeto.agente.EstrategiaFixa import EstrategiaFixa, EstrategiaAleatoria


def treinar_dqn_rapido(estrategia, n_episodios=1000):

    print(f"\n>>> A AQUECER O DQN ({n_episodios} episódios de treino)... Aguarda.")


    env = WorldForaging(size=10, num_resources=40, num_obstacles=2, num_agents=1)
    agente = AgentForaging(agent_id=0, ambiente=env, estrategia=estrategia)

    start_time = time.time()

    for ep in range(n_episodios):
        env.reset_map(num_resources=40, num_obstacles=2)
        passos = 0
        agente.contador_passos = 0

        while passos < 200:
            agente.passo(treino=True)
            passos += 1


        if (ep + 1) % (n_episodios // 5) == 0:
            print(f"   -> Progresso: {ep + 1}/{n_episodios} episódios...")

    print(f">>> Aquecimento concluído em {time.time() - start_time:.1f}s! O DQN está pronto.\n")


def avaliar_performance(nome_estrategia, estrategia, n_jogos=50):

    print(f"--- A testar: {nome_estrategia} ({n_jogos} jogos) ---")


    env = WorldForaging(size=10, num_resources=40, num_obstacles=2, num_agents=1)

    scores = []

    for i in range(n_jogos):
        env.reset_map(num_resources=40, num_obstacles=2)


        agente = AgentForaging(agent_id=0, ambiente=env, estrategia=estrategia)


        epsilon_original = 0
        if hasattr(estrategia, 'epsilon'):
            epsilon_original = estrategia.epsilon
            estrategia.epsilon = 0.05

        passos = 0
        while passos < 200:
            agente.passo(treino=False)
            passos += 1

        scores.append(env.agents_data[0]['pontos'])


        if hasattr(estrategia, 'epsilon'):
            estrategia.epsilon = epsilon_original

    media = np.mean(scores)
    print(f"-> Média Final: {media:.2f} pontos")
    return media


if __name__ == "__main__":
    print(">>> A INICIAR  POLÍTICAS <<<")


    pol_aleatoria = EstrategiaAleatoria()
    pol_fixa = EstrategiaFixa()
    pol_dqn = Estrategia(input_size=11, num_actions=4)


    treinar_dqn_rapido(pol_dqn, n_episodios=1500)


    media_rand = avaliar_performance("Aleatória", pol_aleatoria, n_jogos=50)
    media_fixa = avaliar_performance("Fixa (Heurística)", pol_fixa, n_jogos=50)
    media_dqn = avaliar_performance("DQN (AI - Treinada)", pol_dqn, n_jogos=50)


    print("\nA gerar gráfico comparativo...")

    categorias = ['Aleatória', 'Fixa (Regras)', 'DQN (AI)']
    valores = [media_rand, media_fixa, media_dqn]
    cores = ['gray', 'blue', 'red']

    plt.figure(figsize=(10, 6))
    barras = plt.bar(categorias, valores, color=cores, width=0.6)


    for barra in barras:
        height = barra.get_height()
        plt.text(barra.get_x() + barra.get_width() / 2., height,
                 f'{height:.1f}',
                 ha='center', va='bottom', fontweight='bold')

    plt.title('Comparação Final: Regras vs IA Treinada (Média de 50 Jogos)')
    plt.ylabel('Pontos Médios Recolhidos')
    plt.grid(axis='y', alpha=0.3)

    print("Concluído!")
    plt.show()