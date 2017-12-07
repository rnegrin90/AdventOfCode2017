def get_input():
    file = open("input.txt", "r")
    return file.readlines()


def manhattan_distance(start, end):
    sx, sy = start
    ex, ey = end
    return abs(ex - sx) + abs(ey - sy)


def to_int(array):
    return map(int, array.split())


def serialize(array):
    return '/'.join(map(str, array))


class Node:
    def __init__(self, uid):
        self.uid = uid
        self.next = set()


def get_head_node(tree):
    head_node = None
    parent_nodes = list(filter(lambda p: len(tree[p].next) > 0, tree))
    for node in parent_nodes:
        found = False
        for n in parent_nodes:
            found = tree[node].uid in tree[n].next
        if not found:
            head_node = tree[node]
    return head_node


def generate_tree(input, parse_node):
    tree = {}
    for inst in input:
        node = parse_node(inst)
        tree[node.uid] = node
    return tree, get_head_node(tree)
