from common import get_input


def serialize(memory):
    return '/'.join(map(str, memory))


def redistribute_blocks(memory):
    max_value = max(memory)
    index = memory.index(max_value)
    memory[index] = 0
    while max_value > 0:
        index = (index + 1) % len(memory)
        memory[index] += 1
        max_value -= 1
    return memory


def process(input):
    memory = list(map(int, input.split()))
    state_cache = {}
    cycles_to_loop = 0
    while serialize(memory) not in state_cache:
        state_cache[serialize(memory)] = 1
        memory = redistribute_blocks(memory)
        cycles_to_loop += 1
    cycles_in_loop = 0
    while state_cache[serialize(memory)] != 2:
        state_cache[serialize(memory)] += 1
        memory = redistribute_blocks(memory)
        cycles_in_loop += 1
    return cycles_to_loop, cycles_in_loop


assert process("0\t2\t7\t0") == (5, 4)

print(process(get_input()[0]))
