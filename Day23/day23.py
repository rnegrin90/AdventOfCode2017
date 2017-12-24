from collections import defaultdict

from Day18.day18 import program
from common import get_input

cmd = {
    'set': lambda p: f"""
ct_counter[ct] += 1
{p.split(" ")[0]}={p.split(" ")[1]}
""",
    'sub': lambda p: f"""
ct_counter[ct] += 1
{p.split(" ")[0]}-={p.split(" ")[1]}
""",
    'mul': lambda p: f"""
ct_counter[ct] += 1
mul_freq += 1
{p.split(" ")[0]}*={p.split(" ")[1]}
""",
    'jnz': lambda p: f"""
ct_counter[ct] += 1
ct += ({p.split(" ")[1]}-1) if {p.split(" ")[0]} != 0 else 0
"""
}


def process(input):
    env = defaultdict(int)
    env['cancel_token'] = False
    env['ct_counter'] = [0] * 32
    program(input, {}, {}, env, 0, cmd)
    return env['mul_freq']


def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def process_two():
    b = 106500
    c = 106500 + 17000
    result = 0
    for i in range(b, c+1, 17):
        print(i)
        if not is_prime(i):
            result += 1
    return result


print(process(get_input()))

print(process_two())
