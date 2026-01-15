Forrageamento
Este repositório contém a implementação de um ambiente de simulação para estudo de agentes independentes. O projeto tem como objetivo comparar o desempenho de estratégias baseadas em Aprendizagem (Redes Neurais/DQN) versus comportamentos baseados em Regras Fixas (Heurísticas) e Aleatórias.

O sistema foi desenvolvido em Python e aborda dois cenários distintos de navegação e sobrevivência em grade (Grid World).

Visão Geral do Projeto
O projeto divide-se em dois problemas principais:

Problema do Farol (Pathfinding): O agente deve encontrar o caminho de um ponto inicial até um alvo fixo (Farol) num mapa com obstáculos, minimizando o número de passos e evitando colisões.
Problema de Forrageamento (Sobrevivência): O agente deve explorar o mapa para coletar recursos (comida) e manter sua energia acima de zero pelo maior tempo possível.
Estrutura do Repositório
O código fonte encontra-se no diretório Projetoe está organizado nos seguintes módulos:

1. Agentes ( /agente)
Este módulo contém a lógica de decisão, sensores e estruturas de memória dos agentes.

AgentFarol.py / AgentForaging.py: Classes base que definem as ações possíveis e o sistema de percepção (sensores) dos agentes.
DQN.py: Implementação da Rede Neural (Deep Q-Network) utilizada para a aprendizagem por reforço.

Estratégias de Decisão:
EstrategiaNeuralFarol.py: Tomada de decisão baseada nos pesos da rede treinada (Cenário Farol).
EstrategiaFarolFixa.py: Algoritmos baseados em regras manuais e heurísticas de navegação para o Farol.
EstrategiaForaging.py: Lógica de decisão específica para coleta de recursos e gestão de energia.
EstrategiaFixa.py: Estrutura base para comportamentos determinísticos.
EstrategiaFarolAleatoria.py: Implementação de movimento estocástico para fins de comparação (baseline).

2. Ambiente ( /ambiente)
Responsável por definir as regras do mundo virtual e o estado da simulação.

WorldFarol.py / WorldForaging.py: Gerenciamento da grade, posicionamento de obstáculos e validação de movimentos.
Cell.py / Objects.py: Definição das propriedades dos objetos do mapa (Obstáculos, Chão, Alvos).

3. Simulador ( /simulador)
Controle o ciclo de execução dos episódios, atualização de estados e coleta de estatísticas.

simuladorFarol.py: Loop principal para o cenário do farol.
SimuladorForaging.py / SimuladorForagingFixa.py: Loops principais para o treino e teste do cenário de sobrevivência.

4. Execução (Raiz de /Projeto)
Scripts principais para iniciar as simulações e benchmarks comparativos.

mainFarol.py: Executa o treino ou teste da IA ​​no cenário do Farol.
main_FarolFixa.py: Executa o benchmark da estratégia fixada no cenário do Farol.
main_foraging.py: Executa uma simulação de sobrevivência com IA.
main_foragingfixa.py: Executa uma simulação de sobrevivência com regras fixas.

Pré-requisitos e Instalação
O projeto foi desenvolvido em Python. Para executar o código, é necessário instalar as bibliotecas de cálculo numérico e visualizações específicas abaixo:
pip install numpy matplotlib torch
