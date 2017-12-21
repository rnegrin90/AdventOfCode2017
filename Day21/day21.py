def serialize(matrix):
    return '/'.join(map(''.join, matrix))

assert serialize([['.', '.'], ['.', '#']]) == '../.#'


def deserialize(ser_matrix):
    return list(map(list, ser_matrix.split('/')))

assert deserialize('.#./..#/###') == [['.', '#', '.'], ['.', '.', '#'], ['#', '#', '#']]


def get_rotations(matrix):
    rotations = list()
    rotations.append(matrix)
    rotated = matrix
    for _ in [90, 180, 270]:
        rotated = list(zip(*rotated[::-1]))
        rotations.append(rotated)
    return rotations

assert get_rotations([['.', '#', '.'], ['.', '.', '#'], ['#', '#', '#']]) == ([['.', '#', '.'], ['.', '.', '#'], ['#', '#', '#']],
                                                                              [['.', '#', '.'], ['#', '.', '.'], ['#', '#', '#']],
                                                                              [['#', '.', '.'], ['#', '.', '#'], ['#', '#', '.']],
                                                                              [['#', '#', '#'], ['.', '.', '#'], ['.', '#', '.']])