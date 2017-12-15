import re

from common import get_input


def div_generator(*args):
    last, seed, div = args
    while True:
        product = last * seed
        last = product % 2147483647
        if (last % div) == 0:
            yield last


def seq_generator(*args):
    last, seed = args
    while True:
        product = last * seed
        last = product % 2147483647
        yield last


test_a = seq_generator(65, 16807)
assert next(test_a) == 1092455
assert next(test_a) == 1181022009
assert next(test_a) == 245556042
assert next(test_a) == 1744312007
assert next(test_a) == 1352636452

test_b = seq_generator(8921, 48271)
assert next(test_b) == 430625591
assert next(test_b) == 1233683848
assert next(test_b) == 1431495498
assert next(test_b) == 137874439
assert next(test_b) == 285222916


def judge(pair):
    a, b = pair
    return a[-16:] == b[-16:]


assert judge(("00011001101010101101001100110111", "00000000000100001010101101100111")) is False
assert judge(("01000110011001001111011100111001", "01001001100010001000010110001000")) is False
assert judge(("00001110101000101110001101001010", "01010101010100101110001101001010")) is True
assert judge(("01100111111110000001011011000111", "00001000001101111100110000000111")) is False
assert judge(("01010000100111111001100000100100", "00010001000000000010100000000100")) is False


def generate_binary(input):
    a, b = input
    a_bin = list('{0:0b}'.format(a))
    b_bin = list('{0:0b}'.format(b))
    while len(a_bin) < 16:
        a_bin.insert(0, "0")
    while len(a_bin) > len(b_bin):
        b_bin.insert(0, "0")
    while len(b_bin) > len(a_bin):
        a_bin.insert(0, "0")
    return list(map(''.join, (a_bin, b_bin)))


assert generate_binary((1092455, 430625591)) == ["00000000100001010101101100111", "11001101010101101001100110111"]


def parse_input(input):
    return list(map(int, re.search(r'Generator \w starts with (\d+)', input).groups()))[0]


assert parse_input("Generator A starts with 634") == 634


def process(input, pair_count, generator):
    matching_pairs = 0
    a_gen = generator(parse_input(input[0]), 16807, 4)
    b_gen = generator(parse_input(input[1]), 48271, 8)
    for i in range(0, pair_count):
        # if judge(generate_binary((next(a_gen), next(b_gen)))):
        if next(a_gen) & 0xFFFF == next(b_gen) & 0xFFFF:
            matching_pairs += 1
    return matching_pairs


# assert process((65, 8921)) == 588
# print(process(get_input(), 40000000, seq_generator))

assert process(("Generator A starts with 65", "Generator B starts with 8921"), 5000000, div_generator) == 309
print(process(get_input(), 5000000, div_generator))
