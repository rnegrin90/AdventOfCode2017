import re

from common import get_input


class Action:
    def __init__(self, action):
        write, direction, next_state = action
        self.write = write
        self.direction = direction
        self.next_state = next_state


class State:
    def __init__(self, name, zero, one):
        self.name = name
        self.action = {0: zero, 1: one}


def read_actions(pos, input):
    value = re.search(r'- Write the value (\d).', input[pos]).groups()[0]
    direction = re.search(r'- Move one slot to the ([lr])(?:eft|ight).', input[pos+1]).groups()[0]
    next_state = re.search(r'- Continue with state (\w).', input[pos+2]).groups()[0]
    return int(value), direction.upper(), next_state


def create_turing_machine(input):
    states = {}
    i = 0
    while i < len(input):
        if i < 2:
            start_state = re.search(r'Begin in state (\w).', input[i]).groups()[0]
            checksum = re.search(r'Perform a diagnostic checksum after (\d+) steps.', input[i+1]).groups()[0]
            i = 3
        else:
            state_name = re.search(r'In state (\w):', input[i]).groups()[0]
            action_zero = Action(read_actions(i+2, input))
            action_one = Action(read_actions(i+6, input))
            states[state_name] = State(state_name, action_zero, action_one)
            i += 10
    return start_state, int(checksum), states


movements = {
    'L': -1,
    'R': 1
}


def process(input):
    state, checksum, states = create_turing_machine(input)
    tape = [0]
    cursor = 0
    for _ in range(0, checksum):
        current_value = tape[cursor]
        tape[cursor] = states[state].action[current_value].write
        cursor += movements[states[state].action[current_value].direction]
        state = states[state].action[current_value].next_state
        while cursor >= len(tape):
            tape.append(0)
        while cursor < 0:
            tape.insert(0, 0)
            cursor += 1
    return sum(tape)


test_input = """Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.""".split('\n')
assert process(test_input) == 3

print(process(get_input()))
