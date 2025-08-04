def is_valid(solution, points):
    pickups_made = []
    for i in solution:
        point = points[i]
        if point.type == 0:
            pickups_made.append(point.index)
        if point.type == 1:
            if point.pair not in pickups_made:
                return False
    return True


def fix_solution(solution, points):
    pickups_made = set()
    corrected_solution = []
    pending_deliveries = []

    # Remove os zeros fixos
    core_solution = solution[1:-1]

    for idx in core_solution:
        point = points[idx]
        if point.type == 0:  
            pickups_made.add(point.index)
            corrected_solution.append(idx)

            
            i = 0
            while i < len(pending_deliveries):
                pending_idx = pending_deliveries[i]
                delivery_point = points[pending_idx]
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

