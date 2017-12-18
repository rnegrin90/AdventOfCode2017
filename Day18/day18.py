from collections import defaultdict, deque

from concurrent.futures import ThreadPoolExecutor

from common import get_input


part_one = {
    'snd': lambda p: f"""
played = {p}
""",
    'rcv': lambda p: f"""
if {p} > 0:
    last_frequency = played
    cancel_token = True
"""
}

part_two = {
    'snd': lambda p: f"""
snd_count += 1
outgoing.append({p})
""",
    'rcv': lambda p: f"""
while incoming.__len__() == 0 and not cancel_token:
    waiting = True
waiting = False
{p} = incoming.popleft()
"""
}


def format_line(line, cmd):
    action, payload = line.split(' ', 1)
    if action == 'snd':
        return cmd[action](payload)
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
        return cmd[action](payload)
    if action == 'jgz':
        x, y = payload.split(' ')
        return f'ct += ({y}-1) if {x} > 0 else 0'


def program(input, incoming, outgoing, env, id, cmd):
    env['p'] = id
    env['incoming'] = incoming
    env['outgoing'] = outgoing
    while env['ct'] < len(input) and not env['cancel_token']:
        action = format_line(input[env['ct']], cmd)
        exec(action, {}, env)
        exec("ct+=1", {}, env)


def process1(input):
    p_env = defaultdict(int)
    pool = ThreadPoolExecutor(max_workers=2)
    pool.submit(program, input, None, None, p_env, 0, part_one)
    pool.shutdown()
    return p_env['last_frequency']


def process2(input):
    process1_to_process2 = deque()
    process2_to_process1 = deque()
    p1_env = defaultdict(int)
    p2_env = defaultdict(int)

    p1_env['waiting'] = False
    p2_env['waiting'] = False
    p1_env['cancel_token'] = False
    p2_env['cancel_token'] = False

    pool = ThreadPoolExecutor(max_workers=2)
    pool.submit(program, input, process2_to_process1, process1_to_process2, p1_env, 0, part_two)
    pool.submit(program, input, process1_to_process2, process2_to_process1, p2_env, 1, part_two)

    while True:
        if p1_env['waiting'] and p2_env['waiting']:
            p1_env['cancel_token'] = True
            p2_env['cancel_token'] = True
            break

    pool.shutdown()

    return p2_env['snd_count']


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
assert process1(test_input.split('\n')) == 4

print(process1(get_input()))


test_input2 = """snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d"""
assert process2(test_input2.split('\n')) == 3

print(process2(get_input()))
