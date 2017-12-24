from common import get_input


def read_tubes(input):
    result = list()
    for line in input:
        s, e = list(map(int, line.split('/')))
        result.append([s, e])
    return result


def get_current_strengh(bridge):
    result = 0
    for tube in bridge:
        result += tube[0]
        result += tube[1]
    return result


def get_strongest(bridge, available_tubes, last_connection):
    possible = list(filter(lambda t: last_connection in t, available_tubes))
    path_strenghts = list()
    if len(possible) > 0:
        for tube in possible:
            c = list(tube)
            c.remove(last_connection)
            asdf = list(bridge)
            asdf.append(tube)
            qwer = list(available_tubes)
            qwer.remove(tube)
            path_strenghts.append(get_strongest(asdf, qwer, c[0]))
    else:
        path_strenghts.append(get_current_strengh(bridge))
    return max(path_strenghts)


def get_longest(bridge, available_tubes, last_connection):
    possible = list(filter(lambda t: last_connection in t, available_tubes))
    paths = dict()
    if len(possible) > 0:
        for tube in possible:
            c = list(tube)
            c.remove(last_connection)
            asdf = list(bridge)
            asdf.append(tube)
            qwer = list(available_tubes)
            qwer.remove(tube)
            size, bridges = get_longest(asdf, qwer, c[0])
            if size not in paths:
                paths[size] = list()
            paths[size] += bridges
    else:
        if len(bridge) not in paths:
            paths[len(bridge)] = list()
        paths[len(bridge)].append(bridge)
    longest = max(paths)
    return longest, list(paths[longest])


def process_two(input):
    tubes = read_tubes(input)
    longest = (0, None)
    for start in filter(lambda t: 0 in t, tubes):
        s = list(start)
        s.remove(0)
        bridge = list()
        bridge.append(start)
        availabe_tubes = list(tubes)
        availabe_tubes.remove(start)
        size, bridges = get_longest(bridge, availabe_tubes, s[0])
        if longest[0] < size:
            longest = (size, bridges)
        elif longest[0] == size:
            longest[1] += bridges
    strengths = list(map(get_current_strengh, longest[1]))
    return max(strengths)


def process(input):
    tubes = read_tubes(input)
    strongest = 0
    for start in filter(lambda t: 0 in t, tubes):
        s = list(start)
        s.remove(0)
        bridge = list()
        bridge.append(start)
        availabe_tubes = list(tubes)
        availabe_tubes.remove(start)
        strongest = max(get_strongest(bridge, availabe_tubes, s[0]), strongest)
    return strongest


test_input = """0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10""".split('\n')
assert process(test_input) == 31

# print(process(get_input()))

assert process_two(test_input) == 19
print(process_two(get_input()))
