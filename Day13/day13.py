import re

from common import get_input


def parse_input(input):
    firewall = {}
    for level in input:
        result = re.search(r'(\d+): (\d+)', level).groups()
        dth, rng = list(map(int, result))
        firewall[dth] = [False]*rng
        firewall[dth][0] = True, 0
    return firewall


def move_security(firewall):
    for key in firewall.keys():
        up = (True, 0) in firewall[key]
        if up:
            level = firewall[key].index((True, 0))
            firewall[key][level] = False
            if level == len(firewall[key])-1:
                firewall[key][level-1] = True, 1
            else:
                firewall[key][level+1] = True, 0
        else:
            level = firewall[key].index((True, 1))
            firewall[key][level] = False
            if level == 0:
                firewall[key][level+1] = True, 0
            else:
                firewall[key][level-1] = True, 1


def break_firewall(start, firewall):
    level = 0
    pos = start - 1
    picoseconds = 0
    end = max(firewall.keys())
    caught_layers = set()
    while pos <= end:
        pos += 1
        if pos in firewall and firewall[pos][level] != False:
            caught_layers.add(pos)
        move_security(firewall)
        picoseconds += 1
    return firewall, level, pos, caught_layers


def process(input):
    firewall = parse_input(input)
    _, level, pos, detections = break_firewall(0, firewall)
    return sum(list(map(lambda p: p*len(firewall[p]), detections)))


test_input = """0: 3
1: 2
4: 4
6: 4"""
assert process(test_input.split('\n')) == 24

print(process(get_input()))
