from Projeto.simulador.simuladorFarol import simuladorFarol

import Projeto.agente.EstrategiaNeuralFarol as m
from Projeto.agente.EstrategiaNeuralFarol import EstrategiaNeuralFarol

from Projeto.agente.EstrategiaFarolFixa import EstrategiaFarolFixa
from Projeto.agente.EstrategiaFarolAleatoria import EstrategiaFarolAleatoria
from Projeto.ambiente.WorldFarol import WorldFarol
from Projeto.agente.AgentFarol import AgentFarol

import matplotlib.pyplot as plt


print("EstrategiaNeuralFarol importada de:", m.__file__)
print("Assinatura:", m.EstrategiaNeuralFarol.__init__)


def benchmark(make_strat, n_testes=5000, max_passos=30, farol_fixo=True):
    sucessos = 0

    for _ in range(n_testes):
        env = WorldFarol(size=6)
        if farol_fixo:
            env.force_farol(5, 5)

        strat = make_strat()
        agente = AgentFarol(strat)
        agente.mundo = env

        # reset completo (importante para memória/tempo)
        agente.visited_cells = set([(0, 0)])
        agente.steps_taken = 0
        agente.last_action = -1
        agente.bates_parede = 0

        chegou = False
        for _ in range(max_passos):
            if agente.agir():
                chegou = True
                break

        if chegou:
            sucessos += 1

    return 100.0 * sucessos / n_testes


if __name__ == "__main__":
    sim = simuladorFarol(pop_size=50, weights_path="best_farol.npz")

    sim.treinar(total_episodios=5000)

    estrategia_carregada = EstrategiaNeuralFarol(8, 4, weights_path="best_farol.npz")
    sim.testar(
        estrategia=estrategia_carregada,
        n_episodios=200,
        max_passos=40,
        seeds=list(range(200)),
        farol_fixo=True,
        render=False
    )

    print("\n--- BENCHMARK COMPARATIVO ---")
    taxa_aleatoria = benchmark(lambda: EstrategiaFarolAleatoria(8, 4), n_testes=5000, max_passos=30)
    taxa_fixa      = benchmark(lambda: EstrategiaFarolFixa(8, 4), n_testes=5000, max_passos=30)
    taxa_novelty   = benchmark(lambda: EstrategiaNeuralFarol(8, 4, weights_path="best_farol.npz"),n_testes=5000, max_passos=30)

    print(f"Aleatória: {taxa_aleatoria:.1f}%")
    print(f"Fixa (Heurística): {taxa_fixa:.1f}%")
    print(f"Novelty Search (modelo treinado): {taxa_novelty:.1f}%")

    categorias = ["Aleatória", "Fixa (Heurística)", "Novelty Search"]
    valores = [taxa_aleatoria, taxa_fixa, taxa_novelty]

    plt.figure(figsize=(10, 6))
    barras = plt.bar(categorias, valores, width=0.6)
    plt.ylabel("Taxa de Sucesso (%)")
    plt.title("Comparação: Capacidade de Encontrar o Farol")
    plt.ylim(0, 110)

    for b in barras:
        h = b.get_height()
        plt.text(b.get_x() + b.get_width() / 2, h + 1, f"{h:.1f}%", ha="center", va="bottom")

    plt.grid(axis="y", alpha=0.3)
    plt.show()

    input("Pressiona Enter para sair...")
