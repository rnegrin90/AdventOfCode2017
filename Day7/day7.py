from common import get_input, Node, generate_tree


class Program(Node):
    def __init__(self, uid, weight):
        super().__init__(uid)
        self.weight = weight
        self.total_weight = 0


def parse_program(program):
    p = program.split('->')
    above = None
    if len(p) > 1:
        above = map(lambda s: s.strip(), p[1].split(','))
    name, weight = p[0].split('(')
    result = Program(name.strip(), int(weight.replace(")", "".strip())))
    if above:
        result.next = set(above)
    return result


def generate_subtree_weight(node, tree):
    if len(node.next) > 0:
        for sub_node in node.next:
            node.total_weight += generate_subtree_weight(tree[sub_node], tree)
    node.total_weight += node.weight
    return node.total_weight


def get_expected_weight(head, tower):
    this_level = {}
    for sub_node in head.next:
        n = tower[sub_node]
        if n.total_weight in this_level:
            this_level[n.total_weight].append(n.uid)
        else:
            this_level[n.total_weight] = [n.uid]
    if len(this_level) > 1:
        unbalanced_weight = next(filter(lambda l: len(this_level[l]) == 1, this_level))
        unbalanced_node = this_level[unbalanced_weight][0]
        expected_weight = get_expected_weight(tower[unbalanced_node], tower)
        if expected_weight is None:
            weight_difference = unbalanced_weight - next(filter(lambda l: len(this_level[l]) > 1, this_level))
            return tower[unbalanced_node].weight - weight_difference
        else:
            return expected_weight
    return None


def get_weighted_tower(head, tower):
    generate_subtree_weight(head, tower)
    return tower


def process(input):
    tower, head_node = generate_tree(input, parse_program)
    tower = get_weighted_tower(head_node, tower)
    expected_weight = get_expected_weight(head_node, tower)
    return head_node.uid, expected_weight


test_input = """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""
assert process(test_input.split('\n')) == ("tknk", 60)

print(process(get_input()))  # returns ('bsfpjtc', 529)
