from common import get_input


movements = {
    'n': lambda x, y: (x, y-1),
    's': lambda x, y: (x, y+1),
    'ne': lambda x, y: (x+1, y-1),
    'nw': lambda x, y: (x-1, y),
    'se': lambda x, y: (x+1, y),
    'sw': lambda x, y: (x-1, y+1),
}


def get_z(hex_coord):
    x, y = hex_coord
    return -x-y


def distance(a, b):
    sx, sy = a
    ex, ey = b
    return (abs(sx - ex) + abs(sy - ey) + abs(get_z(a) - get_z(b))) / 2


def process(input):
    x, y = 0, 0
    max_distance = 0
    for dir in input.split(','):
        x, y = movements[dir](x, y)
        max_distance = max((max_distance, distance((0, 0), (x, y))))
    return distance((0, 0), (x, y)), max_distance


assert process("ne,ne,ne") == (3, 3)
assert process("ne,ne,sw,sw") == (0, 2)
assert process("ne,ne,s,s") == (2, 2)
assert process("se,sw,se,sw,sw") == (3, 3)

print(process(get_input()[0]))
