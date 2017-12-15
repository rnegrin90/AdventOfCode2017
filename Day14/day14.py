from Day10.day10 import get_dense_hash, generate_from_ascii
import Day10


def to_bit_array(input_list):
    result = list()
    for element in input_list:
        result.append('{0:08b}'.format(element))
    return map(int, ''.join(result))


def bit_result(list):
    return to_bit_array(get_dense_hash(list))


def count_blocks(input):
    bit_array = Day10.day10.process(input, 256, 64, generate_from_ascii, bit_result)
    return sum(filter(lambda x: x == 1, bit_array))


def generate_grid(input, size):
    result = list()
    for i in range(0, size):
        result.append(list(Day10.day10.process(f'{input}-{i}', 256, 64, generate_from_ascii, bit_result)))
    return result


def get_adjacent(i, j, grid):
    neighbours = list()
    if i < len(grid)-1 and grid[i+1][j] == 1:
        neighbours.append((i+1, j))
    if i > 0 and grid[i-1][j] == 1:
        neighbours.append((i-1, j))
    if j < len(grid[i])-1 and grid[i][j+1] == 1:
        neighbours.append((i, j+1))
    if j > 0 and grid[i][j-1] == 1:
        neighbours.append((i, j-1))
    return neighbours


def get_group_elements(i, j, grid):
    adjacent_stack = get_adjacent(i, j, grid)
    visited = {(i, j)}
    while len(adjacent_stack) > 0:
        x, y = adjacent_stack.pop()
        if (x, y) not in visited:
            adj = get_adjacent(x, y, grid)
            for u, v in adj:
                adjacent_stack.append((u, v))
        visited.add((x, y))
    return visited


def get_groups(grid):
    groups = set()
    for i in range(0, len(grid)):
        for j in range(0, len(grid[i])):
            if grid[i][j] == 0:
                continue
            grouped = False
            for group in groups:
                grouped = (i, j) in group or grouped
            if not grouped:
                new_group = get_group_elements(i, j, grid)
                groups.add(frozenset(new_group))
    return groups


def process(input):
    result = 0
    for i in range(0, 128):
        result += count_blocks(f'{input}-{i}')
    return result


def process2(input):
    bit_array = generate_grid(input, 128)
    g = get_groups(bit_array)
    return len(g)


# assert process("flqrgnkx") == 8108

# print(process("uugsqrei"))

assert process2("flqrgnkx") == 1242

print(process2("uugsqrei"))
