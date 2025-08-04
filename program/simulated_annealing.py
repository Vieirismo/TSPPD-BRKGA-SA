from utils import read_file,distance,calculate_total_distance
from solution_generator import generate_initial_solution, generate_neighbor
from constraints import is_valid
import random 
import math 

def simulated_annealing(points):
    while True:
        current_solution = generate_initial_solution(points)
        if is_valid(current_solution, points):
            current_cost = calculate_total_distance(current_solution, points)
            temperature = 1000

            while temperature > 0.1:
                neighbor = generate_neighbor(current_solution, points)
                neighbor_cost = calculate_total_distance(neighbor, points)

                if neighbor_cost < current_cost:
                    current_solution = neighbor
                    current_cost = neighbor_cost
                else:          
                    probability = math.exp(-(neighbor_cost - current_cost) / temperature)
                    if random.random() < probability:
                        current_solution = neighbor
                        current_cost = neighbor_cost

                temperature *= 0.995

            return current_solution
