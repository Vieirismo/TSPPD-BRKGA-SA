from decoder import Decoder, read_file, Point
from typing import List, Tuple # importa anotações de tipos (Type hints)
import random

class BRKGA:
    def __init__ (self, decoder, chromosome_size: int, population_size: int, elite_percentage: float, mutant_percentage: float, rho: float):
        self.decoder = decoder
        
        self.chromosome_size = chromosome_size
        self.population_size = population_size
        self.elite_percentage= elite_percentage
        self.mutant_percentage = mutant_percentage
        self.rho = rho

        self.current_population: List[List[float]] = [] 
        self.evaluated_population: List[Tuple[float, List[float]]] = []
        
        self.best_solution_route: List[int] = []
        self.best_solution_cost: float = float('inf') 
        
        # Os tipos que supostamente seriam primitivos explicitamente, nesse caso são dados apenas pela anotação com Type hints, 
        # com o intuito de legibilidade, tal qual em Java, por exemplo

    def initialize_population (self):
        self.current_population = []

        for _ in range(self.population_size):
            # gera um novo cromossomo
           chromosome = [random.random() for _ in range (self.chromosome_size)]
           
           self.current_population.append(chromosome)
           
           
           # _ no loop ignora o valor numerico em si e itera até terminar sua condição, como um placeholder

    def evaluate_population (self):
        self.evaluated_population = []  

        # captura a rota e o custo de cada cromossomo
        for chromosome in self.current_population:
            route, cost = self.decoder.decode(chromosome)

            # adiciona a tupla na evaluate
            self.evaluated_population.append((cost,chromosome))

        self.evaluated_population.sort(key=lambda x: x[0])

        # atualiza a melhor solução
        if self.evaluated_population[0][0] < self.best_solution_cost:
            self.best_solution_cost = self.evaluated_population[0][0]

            self.best_solution_route, _ = self.decoder.decode(self.evaluated_population[0][1])
        

    def generate_offspring(self, elite_set: List[List[float]], non_elite_set: List[List[float]], num_offspring: int) -> List[List[float]]:
        
        offsprings = []

        for i in range(num_offspring):
            parent_elite = random.choice(elite_set)
            parent_non_elite = random.choice(non_elite_set)
            
            new_chromosome = []

            for j in range(self.chromosome_size):
                random_number = random.random()

                if random_number < self.rho:
                    new_chromosome.append(parent_elite[j])
                else:
                    new_chromosome.append(parent_non_elite[j])

            offsprings.append(new_chromosome)

        return offsprings
        

    def generate_mutants(self, num_mutants: int) -> List[List[float]]:
        mutants = []
        
        for _ in range(num_mutants):
            mutant_chromosome = [random.random() for _ in range (self.chromosome_size)] # cada mutante é um cromossomo aleatório  

            mutants.append(mutant_chromosome)
            
        return mutants

    # loop principal
    def evolve(self, num_generations: int):
        self.initialize_population()

        print(f"Iniciando BRKGA por {num_generations} gerações...")

        for generation_num in range(num_generations):
             self.evaluate_population() # chamada que avalia e ordena a população 
            
             # a cada geração recalcula as variáveis, por conta do evaluate também ser alterado 
             num_elite = int(self.population_size * self.elite_percentage)
             elite_chromosomes = [item[1] for item in self.evaluated_population[:num_elite]] # pega o segundo (desconsidera a posição 0, inicial) cromossomo de num_elite
             non_elite_chromosomes = [item[1] for item in self.evaluated_population[num_elite:]] # pega oq "sobrou"/restantes

             # calcula a quantidade para a próxima geração
             num_mutants = int(self.population_size * self.mutant_percentage)
             num_offspring = self.population_size - num_elite - num_mutants

             # chama a geração de descendentes e mutantes
             offspring = self.generate_offspring(elite_chromosomes, non_elite_chromosomes, num_offspring)
             mutants = self.generate_mutants(num_mutants)

             # constrói uma nova geração
             self.current_population = elite_chromosomes + offspring + mutants

             if (generation_num + 1) % (num_generations // 10 or 1) == 0 or generation_num == num_generations - 1:
                 print(f"Geração {generation_num + 1}/{num_generations}: Melhor custo = {self.best_solution_cost:.2f}")


    def get_best_solution(self) -> Tuple[List[int], float]:
        return self.best_solution_route, self.best_solution_cost

