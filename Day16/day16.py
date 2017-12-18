import re

from common import get_input

programs = list('abcdefghijklmnop')

moves = {
    'x': lambda x, y, p: exchange(int(x), int(y), p),
    's': lambda x, p: p[-x:] + p[:-x],
    'p': lambda x, y, p: partner(x, y, p)
}


def exchange(x, y, p):
    p[x], p[y] = p[y], p[x]
    return p


def partner(x, y, p):
    ix = p.index(x)
    iy = p.index(y)
    p[ix], p[iy] = p[iy], p[ix]
    return p


def parse_input(mov):
    return re.search(r'([xsp])([\w\d]+[/\w\d]*)', mov).groups()


def process(input):
    prog = list(programs)
    sp = input.split(',')
    seen_states = {}
    while True:
        for mov in sp:
            dance, target = parse_input(mov)
            if '/' in target:
                x, y = target.split('/')
                prog = moves[dance](x, y, prog)
            else:
                prog = moves[dance](int(target), prog)
        state = ''.join(prog)
        if state in seen_states:
            break
        else:
            seen_states[state] = 1
    prog = list(programs)
    for _ in range(0, 1000000000 % len(seen_states)):
        for mov in sp:
            dance, target = parse_input(mov)
            if '/' in target:
                x, y = target.split('/')
                prog = moves[dance](x, y, prog)
            else:
                prog = moves[dance](int(target), prog)
    return ''.join(prog)


assert moves['s'](1, list("abcde")) == list("eabcd")
assert moves['x'](3, 4, list("eabcd")) == list("eabdc")
assert moves['p']('e', 'b', list("eabdc")) == list("baedc")

print(process(get_input()[0]))
