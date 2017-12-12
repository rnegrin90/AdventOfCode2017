import re

import numpy as np

from common import get_input, Node, generate_tree


def parse_line(line):
    groups = re.search(r'(\d+) <-> ([\d,\s]+)', line).groups()
    node = Node(groups[0])
    node.next = set(groups[1].replace(' ', '').split(','))
    return node


def get_subgroup(relations, id, visited):
    for related in relations[id].next:
        if related not in visited:
            visited.add(related)
            get_subgroup(relations, related, visited)
    return visited


def get_number_in_group(relations, id):
    sub_group = get_subgroup(relations, str(id), set())
    return len(sub_group)


def get_group_count(relations, *args):
    groups = list()
    keys = list(relations)
    while len(keys) > 0:
        sub_group = get_subgroup(relations, keys[0], set())
        groups.append(sub_group)
        keys = np.setdiff1d(keys, list(sub_group))
    return len(groups)


def process(input, solution, param):
    relations, _ = generate_tree(input, parse_line)
    return solution(relations, param)


test_input = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""
assert process(test_input.split('\n'), get_number_in_group, 0) == 6

print(process(get_input(), get_number_in_group, 0))

assert process(test_input.split('\n'), get_group_count, None) == 2

print(process(get_input(), get_group_count, None))
