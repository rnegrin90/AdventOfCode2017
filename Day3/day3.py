import math

from common import manhattan_distance, get_input


def get_level(n):
    level = 0
    capacity = 1
    while n > capacity:
        level += 1
        capacity += level * 8
    return level, capacity


def positive_x(level, position):
    return level, (-level+1)+((position-1) % (level*2))


def positive_y(level, position):
    return -(-level+1)-((position-1) % (level*2)), level


def negative_x(level, position):
    return -level, -(-level+1)-((position-1) % (level*2))


def negative_y(level, position):
    return (-level+1)+((position-1) % (level*2)), -level


def get_location(n):
    level, capacity = get_level(n)
    if level == 0:
        return 0, 0
    position = n - (capacity - level * 8)
    quadrant = math.ceil(position / (level*2))
    return {
        1: positive_x(level, position),
        2: positive_y(level, position),
        3: negative_x(level, position),
        4: negative_y(level, position),
    }[int(quadrant)]


def get_start(level):
    result = 1
    for i in range(0, level):
        result += i * 8
    return result+1


def get_quadrant(x, y, level):
    if abs(x) == level:
        if x > 0:
            if y > -level:
                return 1, y + level - 1
            else:
                return 4, x + level - 1
        else:
            if y < level:
                return 3, level - 1 - y
            else:
                return 2, level - 1 - x
    else:
        if y > 0:
            return 2, level - 1 - x
        else:
            return 4, x + level - 1


def get_number(x, y):
    if x == 0 and y == 0:
        return 1
    level = max(abs(x), abs(y))
    start = get_start(level)
    quadrant, offset = get_quadrant(x, y, level)
    r = list(range((start+((quadrant-1)*level*2)), (start+(quadrant*level*2))))
    return r[offset]


def get_surroundings(x, y):
    return [(x+1, y),
            (x+1, y+1),
            (x, y+1),
            (x-1, y),
            (x-1, y-1),
            (x, y-1),
            (x-1, y+1),
            (x+1, y-1)]


def process(input):
    x, y = get_location(int(input))
    return manhattan_distance((0, 0), (x, y))


def process_second(input):
    inserted = 1
    array_pos = 1
    array = [None, 1]
    while inserted <= int(input):
        array_pos += 1
        x, y = get_location(array_pos)
        pos_to_check = get_surroundings(x, y)
        inserted = 0
        for cx, cy in pos_to_check:
            try:
                n = array[get_number(cx, cy)]
                inserted += n
            except:
                pass
        array.append(inserted)
    return inserted


assert process(1) == 0
assert process(12) == 3
assert process(23) == 2
assert process(1024) == 31

print(process(get_input()[0]))

assert get_number(-1, 1) == 5
assert get_number(2, -1) == 10
assert get_number(5, -5) == 121
assert get_number(0, 0) == 1
assert get_number(-3, -1) == 41
assert get_number(-1, 4) == 62
assert get_number(3, -4) == 80

assert process_second(24) == 25
assert process_second(54) == 57
assert process_second(700) == 747
assert process_second(200) == 304

print(process_second(get_input()[0]))
