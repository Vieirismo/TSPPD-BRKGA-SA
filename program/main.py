from simulated_annealing import simulated_annealing
from decoder import read_file, Point, Decoder 
from BRKGA import BRKGA


import time

def main():
    #SA
    from utils import calculate_total_distance # apenas 1 importação para o SA, considerando a instância de Decoder

    archive_name="instances/pdtsp-n599"

    points=read_file(archive_name)

    start_time_sa = time.perf_counter() # marca o tempo de início 
    final_solution_sa = simulated_annealing(points)
    end_time_sa = time.perf_counter()   # marca o tempo que acabou
    elapsed_time_sa = end_time_sa - start_time_sa # calcula o tempo decorrido

    cost_sa = calculate_total_distance(final_solution_sa, points)

    print("Solução encontrada com SA (ordem dos índices):")
    print(final_solution_sa)
    print(f"Custo da solução: {cost_sa:.2f}")
    print(f"Tempo de execução SA: {elapsed_time_sa:.4f} segundos") # imprime o tempo com a formatação de string

    #BRKGA
    brkga_decoder = Decoder(points) # instância mencionada anteriormente

    population_size = 200       # tamanho da população (número de cromossomos)
    elite_percentage = 0.15     # 15% da população será elite
    mutant_percentage = 0.25    # 25% da população será de mutantes
    rho = 0.75                  # probabilidade de herdar do pai elite no crossover
    num_generations = 1000      # número de gerações para o algoritmo rodar


    chromosome_size = len(points) - 1 
    brkga_solver = BRKGA(
        decoder=brkga_decoder, 
        chromosome_size=chromosome_size,
        population_size=population_size,
        elite_percentage=elite_percentage,
        mutant_percentage=mutant_percentage,
        rho=rho
    )

    start_time_brkga = time.perf_counter() 

    # executa o algoritmo
    brkga_solver.evolve(num_generations)
    end_time_brkga = time.perf_counter() 
    elapsed_time_brkga = end_time_brkga - start_time_brkga # calcula o tempo decorrido

    best_route_brkga, best_cost_brkga = brkga_solver.get_best_solution()


    print("\nMelhor Solução Encontrada")
    print(f"Custo Total: {best_cost_brkga:.2f}")
    print(f"Rota: {best_route_brkga}")
    print(f"Tempo de execução BRKGA: {elapsed_time_brkga:.4f} segundos") 



if __name__ == "__main__":
    main()