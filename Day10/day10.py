from functools import reduce

from common import get_input


def slice_list(input_list, current_pos, length):
    if length == 0:
        return
    next_pos = (current_pos+length) % len(input_list)
    pos = current_pos
    if next_pos == pos:
        yield input_list[pos]
        pos += 1
    while pos != next_pos:
        yield input_list[pos]
        pos += 1
        if pos >= len(input_list):
            pos = pos % len(input_list)


def custom_hash(l, lengths, pos, skip):
    for length in lengths:
        sub_list = list(reversed(list(slice_list(l, pos, length))))
        i = pos
        for j in sub_list:
            l[i] = j
            i += 1
            if i >= len(l):
                i = i % len(l)
        pos = (pos+length+skip) % len(l)
        skip += 1
    return l, pos, skip


def generate_from_ascii(word):
    result = list()
    for c in word:
        result.append(ord(c))
    return result + [17, 31, 73, 47, 23]


def generate_range(size):
    result = list()
    for i in range(0, size):
        result.append(i)
    return result


def to_int_list(input):
    return list(map(int, input.split(',')))


def to_hex_string(input_list):
    result = list()
    for element in input_list:
        result.append('{0:02x}'.format(element))
    return ''.join(result)


def get_dense_hash(input_list):
    hash_result = list()
    steps = int(len(input_list) / 16)
    start = 0
    end = steps
    for i in range(0, 16):
        sl = input_list[start:end]
        hash_result.append(reduce(lambda x, y: x ^ y, sl))
        start += steps
        end += steps
    return hash_result


def sum_result(list):
    return list[0] * list[1]


def hex_result(list):
    return to_hex_string(get_dense_hash(list))


def process(input, size, rounds, parse_input, process_result):
    lengths = parse_input(input)
    l = generate_range(size)
    pos, skip = 0, 0
    for i in range(0, rounds):
        result, pos, skip = custom_hash(l, lengths, pos, skip)
    return process_result(result)

assert process("3,4,1,5", 5, 1, to_int_list, sum_result) == 12

print(process(get_input()[0], 256, 1, to_int_list, sum_result))

assert to_hex_string([64, 7, 255]) == "4007ff"

assert process("", 256, 64, generate_from_ascii, hex_result) == "a2582a3a0e66e6e86e3812dcb672a272"
assert process("AoC 2017", 256, 64, generate_from_ascii, hex_result) == "33efeb34ea91902bb2f59c9920caa6cd"
assert process("1,2,3", 256, 64, generate_from_ascii, hex_result) == "3efbe78a8d82f29979031a4aa0b16a9d"
assert process("1,2,4", 256, 64, generate_from_ascii, hex_result) == "63960835bcdc130f0b66d7ff4f6a5a8e"

print(process(get_input()[0], 256, 64, generate_from_ascii, hex_result))
