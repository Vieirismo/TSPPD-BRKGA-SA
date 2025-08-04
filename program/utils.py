from point import Point


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


def distance(p1, p2):
    return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5


def calculate_total_distance(solution, points):
    total_distance = 0
    for i in range(len(solution) - 1):
        p1 = points[solution[i]]
        p2 = points[solution[i+1]]
        total_distance += distance(p1, p2)
    return total_distance
