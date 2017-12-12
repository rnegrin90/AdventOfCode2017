from common import get_input


def process(input):
    garbage_mode = False
    last_char = None
    level, value_sum, cancelled_chars = 0, 0, 0
    for char in list(input):
        if last_char == '!':
            last_char = None
            continue
        if garbage_mode and char not in ['>', '!']:
            cancelled_chars += 1
        garbage_mode = char == '<' or garbage_mode
        if char == '>':
            garbage_mode = False
        if not garbage_mode and char == '{':
            level += 1
        if not garbage_mode and char == '}':
            value_sum += level
            level -= 1
        last_char = char
    return value_sum, cancelled_chars


assert process("{}")[0] == 1
assert process("{{{}}}")[0] == 6
assert process("{{},{}}")[0] == 5
assert process("{{{},{},{{}}}}")[0] == 16
assert process("{<a>,<a>,<a>,<a>}")[0] == 1
assert process("{{<ab>},{<ab>},{<ab>},{<ab>}}")[0] == 9
assert process("{{<!!>},{<!!>},{<!!>},{<!!>}}")[0] == 9
assert process("{{<a!>},{<a!>},{<a!>},{<ab>}}")[0] == 3

assert process("<>")[1] == 0
assert process("<random characters>")[1] == 17
assert process("<<<<>")[1] == 3
assert process("<{!>}>")[1] == 2
assert process("<!!>")[1] == 0
assert process("<!!!>>")[1] == 0
assert process('<{o"i!a,<{i<a>')[1] == 10

print(process(get_input()[0]))  # returns (16869, 7284)
