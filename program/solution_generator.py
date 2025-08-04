from constraints import is_valid, fix_solution
import random 

def generate_initial_solution(points, max_attempts=10000):
    for _ in range(max_attempts):
        rest = random.sample(range(1, len(points)), len(points) - 1)
        solution = [0] + rest + [0]
        if is_valid(solution, points):
            return solution
        else:
            fixed = fix_solution(solution, points)
            if is_valid(fixed, points):
                return fixed
    raise Exception("Couldn't generate a valid initial solution.")


def generate_neighbor(current_solution, points, max_attempts=10000):
    for _ in range(max_attempts):       
        neighbor = current_solution[:]
        i, j = random.sample(range(1, len(neighbor) - 1), 2)

        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        if is_valid(neighbor, points):
            return neighbor
        else:
            fixed = fix_solution(neighbor, points)
            if is_valid(fixed, points):
                return fixed
    return current_solution
