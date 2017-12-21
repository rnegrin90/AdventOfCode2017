import numpy

from common import get_input


def serialize(matrix):
    return '/'.join(map(''.join, matrix))


assert serialize([['.', '.'], ['.', '#']]) == '../.#'


def deserialize(ser_matrix):
    return list(map(list, ser_matrix.split('/')))


assert deserialize('.#./..#/###') == [['.', '#', '.'], ['.', '.', '#'], ['#', '#', '#']]


def get_rotations(matrix):
    rotated = list(matrix)
    yield list(matrix)
    for _ in [90, 180, 270]:
        rotated = list(zip(*rotated[::-1]))
        yield rotated


def get_flips(matrix):
    yield list(map(list, numpy.fliplr(matrix)))
    yield list(map(list, numpy.flipud(matrix)))


def get_patterns(matrix):
    for rot in get_rotations(matrix):
        yield rot
        flips = get_flips(rot)
        for f in flips:
            yield f


def get_enhancement_rules(input):
    rules = {}
    for rule in input:
        origin, result = rule.split(' => ')
        rules[origin] = deserialize(result)
    return rules


def count_pixels(matrix):
    count = 0
    for i in matrix:
        for j in i:
            if j == '#':
                count += 1
    return count


def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def matrix_split(matrix):
    if (len(matrix) % 2) == 0:
        split_matrix = list(chunks(list(map(lambda l: list(chunks(l, 2)), matrix)), 2))
        result = list()
        for group in split_matrix:
            g1, g2 = group
            row = list()
            for i in range(0, len(g1)):
                row.append((g1[i], g2[i]))
            result.append(row)
        return result
    else:
        split_matrix = list(chunks(list(map(lambda l: list(chunks(l, 3)), matrix)), 3))
        result = list()
        for group in split_matrix:
            g1, g2, g3 = group
            row = list()
            for i in range(0, len(g1)):
                row.append((g1[i], g2[i], g3[i]))
            result.append(row)
        return result


def merge_matrix(split_matrix):
    result = list()
    for row_group in split_matrix:
        grouped_row = list()
        for i in range(0, len(row_group[0])):
            row = list()
            for p in row_group:
                row = row + p[i]
            grouped_row.append(row)
        for r in grouped_row:
            result.append(r)
    return result


def process(starting_pattern, input, iter_num):
    rules = get_enhancement_rules(input)
    current_state = deserialize(starting_pattern)
    for _ in range(0, iter_num):
        if len(current_state) > 3:
            result = list()
            for rows in matrix_split(current_state):
                row_result = list()
                for m in rows:
                    for p in map(serialize, get_patterns(m)):
                        if p in rules:
                            row_result.append(rules[p])
                            break
                result.append(row_result)
            current_state = merge_matrix(result)
            pass
        else:
            for p in map(serialize, get_patterns(current_state)):
                if p in rules:
                    current_state = rules[p]
                    break
        pass
    return count_pixels(current_state)


test_rules = """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#""".split('\n')
test_start = ".#./..#/###"
# assert process(test_start, test_rules, 2) == 12


print(process(test_start, get_input(), 18))
