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


def break_firewall(start, delay, firewall, stop_when_caught=False):
    level = 0
    pos = start - 1
    picoseconds = 0
    end = max(firewall.keys())
    caught_layers = set()
    for i in range(0, delay):
        move_security(firewall)
        picoseconds += 1
    while pos <= end:
        pos += 1
        if pos in firewall and firewall[pos][level] is not False:
            caught_layers.add(pos)
            if stop_when_caught:
                print(f"caught at {delay}")
                break
        move_security(firewall)
        picoseconds += 1
    return caught_layers


def process(input):
    firewall = parse_input(input)
    detections = break_firewall(0, 0, firewall)
    return sum(list(map(lambda p: p*len(firewall[p]), detections)))


def reset_firewall(firewall):
    for key in firewall.keys():
        firewall[key] = [False] * len(firewall[key])
        firewall[key][0] = True, 0


def get_guard_position(start, turns, length):
    freq = (length-1)*2
    return (turns % freq) + start


def detected(firewall, delay):
    for key in firewall:
        if get_guard_position(0, delay+key, len(firewall[key])) == 0:
            return True
    return False


def process_two(input):
    firewall = parse_input(input)
    delay = 0
    while True:
        if detected(firewall, delay):
            delay += 1
        else:
            break
    return delay


test_input = """0: 3
1: 2
4: 4
6: 4"""
assert process(test_input.split('\n')) == 24

print(process(get_input()))

assert process_two(test_input.split('\n')) == 10

print(process_two(get_input()))
