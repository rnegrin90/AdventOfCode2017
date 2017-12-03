def get_input():
    file = open("input.txt", "r")
    return file.readlines()


def manhattan_distance(start, end):
    sx, sy = start
    ex, ey = end
    return abs(ex - sx) + abs(ey - sy)