from common import get_input


def process(input, get_offset):
    int_input = list(map(int, input))
    position, steps, length = 0, 0, len(int_input)
    while 0 <= position < length:
        offset, rule = get_offset(int_input[position])
        int_input[position] += rule
        position += offset
        steps += 1
    return steps


def increase_by_one(current_offset):
    return current_offset, 1


def greater_than_three(current_offset):
    return current_offset, 1 if current_offset < 3 else -1


assert process(["0", "3", "0", "1", "-3"], increase_by_one) == 5

print(process(get_input(), increase_by_one))

assert process(["0", "3", "0", "1", "-3"], greater_than_three) == 10

print(process(get_input(), greater_than_three))
