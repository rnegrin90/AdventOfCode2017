import re, itertools
from common import get_input


played = {}
ct = 0
i, a, p, b, f, l = 0, 0, 0, 0, 0, 0


def format_line(line):
    action, payload = line.split(' ', 1)
    if action == 'snd':
        return f'played["{payload}"] = {payload}'
    if action == 'set':
        x, y = payload.split(' ')
        return f'{x}={y}'
    if action == 'add':
        x, y = payload.split(' ')
        return f'{x}+={y}'
    if action == 'mul':
        x, y = payload.split(' ')
        return f'{x}*={y}'
    if action == 'mod':
        x, y = payload.split(' ')
        return f'{x}={x}%{y}'
    if action == 'rcv':
        return f'print("HERE!! {payload} = " + str(played["{payload}"] if "{payload}" in played else 0))'
    if action == 'jgz':
        x, y = payload.split(' ')
        return f'ct += ({y}-1) if {x} > 0 else 0'


def process(input):
    while ct < len(input):
        action = format_line(input[ct])
        print(action + " // Counter = " + str(ct))
        exec(action, globals())
        exec("ct+=1", globals())


test_input = """set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""
# assert process(test_input.split('\n')) == 4

print(process(get_input()))
