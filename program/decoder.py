import math
import random


class Point: 
    def __init__(self, index, x, y, point_type=-1, pair=-1):
        self.index = index
        self.x = x
        self.y = y
        self.type = point_type
        self.pair = pair


def read_file(file_name):
    point_list = []
    with open(file_name, 'r') as f:
        lines = f.readlines()[1:] 

        for line in lines:
            parts = line.split()
            index = int(parts[0])
            x = float(parts[1])
            y = float(parts[2])

            if len(parts) < 5:
                point_type = -1
                pair = -1
            else:
                point_type = int(parts[3])
                pair = int(parts[4])

            point = Point(index, x, y, point_type, pair)
            point_list.append(point)
    return point_list


class Decoder:
    def __init__(self, points: list[Point]):
       
        self.points = points

   
    def decode(self, chromosome: list[float]) -> tuple[list[int], float]:
        indexed_chromosome = []

        for i, key in enumerate(chromosome):
            indexed_chromosome.append((key, i +1))


        # lambda substituindo def obter_primeiro_elemento(x):
        #                           return x[0]
        # ordenando a indexed_chromossome com base nos primeiros elementos de cada tupla dentro dela
        indexed_chromosome.sort(key=lambda x: x[0]) 
       
        # concatena 0 no inicio e no fim, para q a posição final seja a mesma da inicial
        raw_solution = [item[1] for item in indexed_chromosome]

        solution_with_depot = [0] + raw_solution + [0]
        

        valid_solution = self._fix_solution(solution_with_depot)

        cost = self._calculate_total_distance(valid_solution)

        return valid_solution, cost

    def _distance(self, p1: Point, p2: Point) -> float:
        return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5

    def _calculate_total_distance(self, solution: list[int]) -> float:
        total_distance = 0
        for i in range(len(solution) - 1):
            p1 = self.points[solution[i]]
            p2 = self.points[solution[i+1]]
            total_distance += self._distance(p1, p2)
        return total_distance

    def _is_valid(self, solution: list[int]) -> bool:
        pickups_made = []
        for i in solution:
            point = self.points[i]
            if point.type == 0:
                pickups_made.append(point.index)
            if point.type == 1:
                if point.pair not in pickups_made:
                    return False
        return True

    def _fix_solution(self, solution: list[int]) -> list[int]:
        pickups_made = set()
        corrected_solution = []
        pending_deliveries = []

        core_solution = solution[1:-1] 

        for idx in core_solution:
            point = self.points[idx]
            if point.type == 0:  
                pickups_made.add(point.index)
                corrected_solution.append(idx)

                i = 0
                while i < len(pending_deliveries):
                    pending_idx = pending_deliveries[i]
                    delivery_point = self.points[pending_idx]
                    if delivery_point.pair in pickups_made:
                        corrected_solution.append(pending_idx)
                        pending_deliveries.pop(i)
                    else:
                        i += 1
            elif point.type == 1:  
                if point.pair in pickups_made:
                    corrected_solution.append(idx)
                else:
                    pending_deliveries.append(idx)
            else:
                corrected_solution.append(idx)   

        corrected_solution.extend(pending_deliveries)
        return [0] + corrected_solution + [0] 
    
