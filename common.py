def get_input():
    file = open("input.txt", "r")
    return file.readlines()


def manhattan_distance(start, end):
    sx, sy = start
    ex, ey = end
    return abs(ex - sx) + abs(ey - sy)


def to_int(array):
    return map(int, array.split())


def serialize(array):
    return '/'.join(map(str, array))
