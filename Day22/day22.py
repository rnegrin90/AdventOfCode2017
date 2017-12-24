from common import get_input

direction = {
    'N': (-1, 0),
    'S': (1, 0),
    'W': (0, -1),
    'E': (0, 1)
}


def turn_left(current):
    return {
        'N': 'W',
        'S': 'E',
        'W': 'S',
        'E': 'N'
    }[current]


def turn_right(current):
    return {
        'N': 'E',
        'S': 'W',
        'W': 'N',
        'E': 'S'
    }[current]


def reverse(current):
    return {
        'N': 'S',
        'S': 'N',
        'W': 'E',
        'E': 'W'
    }[current]


def move_one(node, dir, grid, counter):
    x, y = node
    if grid[x][y] == '#':
        dir = turn_right(dir)
        grid[x][y] = '.'
    else:
        counter += 1
        dir = turn_left(dir)
        grid[x][y] = '#'
    x += direction[dir][0]
    y += direction[dir][1]
    return (x, y), dir, counter


def move_two(node, dir, grid, counter):
    x, y = node
    if grid[x][y] == '.':
        dir = turn_left(dir)
        grid[x][y] = 'W'
    elif grid[x][y] == 'W':
        counter += 1
        grid[x][y] = '#'
    elif grid[x][y] == '#':
        dir = turn_right(dir)
        grid[x][y] = 'F'
    elif grid[x][y] == 'F':
        grid[x][y] = '.'
        dir = reverse(dir)
    x += direction[dir][0]
    y += direction[dir][1]
    return (x, y), dir, counter


def grow_grid(grid):
    length = len(grid)
    grid.insert(0, ['.'] * length)
    grid.append(['.'] * length)
    for row in grid:
        row.insert(0, '.')
        row.append('.')


def create_grid(input):
    grid = []
    for line in input:
        row = []
        for c in list(line):
            row.append(c)
        grid.append(row)
    return grid


def process(input, rounds, move):
    grid = create_grid(input)
    start = len(input) // 2
    x, y = start, start
    dir = 'N'
    infection_count = 0
    for _ in range(0, rounds):
        if x == 1 or x == (len(grid)-2) or y == 1 or y == (len(grid)-2):
            grow_grid(grid)
            x += 1
            y += 1
        pos, dir, infection_count = move((x, y), dir, grid, infection_count)
        x, y = pos
    return infection_count


test_input = """..#
#..
...""".split('\n')
assert process(test_input, 70, move_one) == 41
assert process(test_input, 10000, move_one) == 5587

print(process(get_input(), 10000, move_one))

assert process(test_input, 100, move_two) == 26
assert process(test_input, 10000000, move_two) == 2511944

print(process(get_input(), 10000000, move_two))
