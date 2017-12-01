from common import get_input


def process(func, input):
    split_input = list(input)
    result = 0
    for i in range(-1, len(split_input) - 1):
        result = result + (int(split_input[i]) if split_input[i] == func(i, split_input) else 0)
    return result


def get_next_element(index, array):
    return array[index + 1]


def get_next_halfway(index, array):
    next_el = (index + int(len(array)/2)) % len(array)
    return array[next_el]


assert process(get_next_element, '1122') == 3
assert process(get_next_element, '1111') == 4
assert process(get_next_element, '1234') == 0
assert process(get_next_element, '91212129') == 9

print(process(get_next_element, get_input()[0]))

assert process(get_next_halfway, '1212') == 6
assert process(get_next_halfway, '1221') == 0
assert process(get_next_halfway, '123425') == 4
assert process(get_next_halfway, '123123') == 12
assert process(get_next_halfway, '12131415') == 4

print(process(get_next_halfway, get_input()[0]))
