from Projeto.simulador.SimuladorForaging import SimuladorForaging

if __name__ == "__main__":
    sim = SimuladorForaging()


    sim.treinar(total_episodios=2000)

    input("Pressiona Enter para sair...")