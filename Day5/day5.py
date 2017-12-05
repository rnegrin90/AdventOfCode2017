from common import get_input


def process(input, get_offset):
    int_input = list(map(int, input))
    current_pos = 0
    steps = 0
    while current_pos in range(0, len(int_input)):
        previous_pos = current_pos
        offset, rule = get_offset(int_input[current_pos])
        current_pos += offset
        int_input[previous_pos] += rule
        steps += 1
    return steps


def increase_by_one(current_offset):
    return current_offset, 1


def plus_one_if_less_than_three(current_offset):
    return current_offset, 1 if current_offset < 3 else -1


assert process(["0", "3", "0", "1", "-3"], increase_by_one) == 5

print(process(get_input(), increase_by_one))

assert process(["0", "3", "0", "1", "-3"], plus_one_if_less_than_three) == 10

print(process(get_input(), plus_one_if_less_than_three))
