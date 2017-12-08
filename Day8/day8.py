import re

from common import get_input


def parse_instruction(instruction):
    return re.search(r"(\w+) (\w+) (-?\d+) if (\w+) ([><=!]+) (-?\w+)", instruction).groups()


def process_condition(cond_token, cond_op, cond_val, registry):
    left_val = 0
    right_val = int(cond_val)
    if cond_token in registry:
        left_val = registry[cond_token]
    return {
        '>': left_val > right_val,
        '<': left_val < right_val,
        '>=': left_val >= right_val,
        '<=': left_val <= right_val,
        '==': left_val == right_val,
        '!=': left_val != right_val
    }[cond_op]


def process(input):
    registry = dict()
    max_value = 0
    for instruction in input:
        token, op, val, cond_token, cond_op, cond_val = parse_instruction(instruction)
        cond = process_condition(cond_token, cond_op, cond_val, registry)
        current_val = 0 if token not in registry else registry[token]
        registry[token] = {
            'dec': current_val - int(val),
            'inc': current_val + int(val)
        }[op] if cond else current_val
        max_value = registry[token] if registry[token] > max_value else max_value
    max_key = max(registry, key=registry.get)
    return registry[max_key], max_value


test_input = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""
assert process(test_input.split('\n')) == (1, 10)

print(process(get_input()))
