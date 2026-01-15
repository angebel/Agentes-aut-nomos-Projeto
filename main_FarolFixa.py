import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


from Projeto.agente.EstrategiaNeuralFarol import EstrategiaNeuralFarol
from Projeto.ambiente.WorldFarol import WorldFarol
from Projeto.agente.AgentFarol import AgentFarol

from Projeto.agente.EstrategiaFarolFixa import EstrategiaFarolFixa
from Projeto.agente.EstrategiaFarolAleatoria import EstrategiaFarolAleatoria


def testar_estrategia(nome, estrategia_cls, n_testes=5000):
    print(f"--- A Testar: {nome} ---")
    sucessos = 0

    for i in range(n_testes):
        env = WorldFarol(size=6)
        # Instancia a estratégia
        strat = estrategia_cls(n_inputs=8, n_actions=4)
        agente = AgentFarol(strat)
        agente.mundo = env

        # Reset manual
        agente.visited_cells = set([(0, 0)])

        passos = 0
        chegou = False
        while passos < 30:
            if agente.agir():
                chegou = True
                break
            passos += 1

        if chegou:
            sucessos += 1

    taxa = (sucessos / n_testes) * 100
    print(f"Resultado {nome}: {taxa:.1f}%")
    return taxa


if __name__ == "__main__":
    print(">>> INICIANDO BENCHMARK FAROL <<<")


    taxa_aleatoria = testar_estrategia("Aleatória", EstrategiaFarolAleatoria, n_testes=5000)

    taxa_fixa = testar_estrategia("Fixa (Regras)", EstrategiaFarolFixa, n_testes=5000)


    print("\n--- GERAÇÃO DO GRÁFICO ---")

    categorias = ['Aleatória', 'Fixa (Heurística)']
    valores = [taxa_aleatoria, taxa_fixa]
    cores = ['gray', 'blue', 'green']

    plt.figure(figsize=(10, 6))
    barras = plt.bar(categorias, valores, color=cores, width=0.6)

    plt.ylabel('Taxa de Sucesso (%)')
    plt.title('Comparação: Capacidade de Encontrar o Farol')
    plt.ylim(0, 110)


    for barra in barras:
        height = barra.get_height()
        plt.text(barra.get_x() + barra.get_width() / 2., height + 1,
                 f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')

    plt.grid(axis='y', alpha=0.3)
    plt.show()