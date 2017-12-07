from common import get_input


class Program:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.next = set()


def parse_program(program):
    p = program.split('->')
    above = None
    if len(p) > 1:
        above = map(lambda s: s.strip(), p[1].split(','))
    name, weight = p[0].split('(')
    result = Program(name.strip(), weight.replace(")", "".strip()))
    if above:
        result.next = set(above)
    return result


def process(input):
    tower = {}
    for inst in input:
        program = parse_program(inst)
        tower[program.name] = program
    head_node = None
    parent_nodes = list(filter(lambda p: len(tower[p].next) > 0, tower))
    for node in parent_nodes:
        found = False
        for n in parent_nodes:
            if tower[node].name in tower[n].next:
                found = True
        if not found:
            head_node = tower[node]
    return head_node.name


#assert process("") == 0

print(process(get_input()))
