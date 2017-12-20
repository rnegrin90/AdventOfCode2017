import re

from common import get_input

test_input = """p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>""".split('\n')


def parse_particle(particle):
    p = re.search(r'p=<\s?([\-\d,]+)>, v=<\s?([\-\d,]+)>, a=<\s?([\-\d,]+)>', particle).groups()
    return list(map(lambda attr: list(map(int, attr.split(','))), p))


def move(particle):
    p, v, a = particle
    px, py, pz = p
    vx, vy, vz = v
    ax, ay, az = a
    vx += ax
    vy += ay
    vz += az
    px += vx
    py += vy
    pz += vz
    return (px, py, pz), (vx, vy, vz), (ax, ay, az)


def is_closer(new_p, close_p):
    np = new_p[0]
    cp = close_p[0]
    return sum(map(abs, np)) < sum(map(abs, cp))


def part_one(input):
    p_list = list()
    for particle in input:
        p_list.append(parse_particle(particle))
    closest = 0
    while True:
        for i in range(0, len(p_list)):
            p_list[i] = move(p_list[i])
            if is_closer(p_list[i], p_list[closest]):
                closest = i
        print(f'Closest particle is {closest}')


def collision(p1, p2):
    p1x, p1y, p1z = p1[0]
    p2x, p2y, p2z = p2[0]
    return p1x == p2x and p1y == p2y and p1z == p2z


def part_two(input):
    p_list = list()
    for particle in input:
        p_list.append(parse_particle(particle))
    while True:
        for i in range(0, len(p_list)):
            p_list[i] = move(p_list[i])
        collided = set()
        for i in range(0, len(p_list)):
            if i in collided:
                continue
            for j in range(0, len(p_list)):
                if j in collided or i == j:
                    continue
                if collision(p_list[i], p_list[j]):
                    collided.add(i)
                    collided.add(j)
        for i in sorted(collided, reverse=True):
            p_list.remove(p_list[i])
        print(f'Particle count is {len(p_list)}')

part_two(get_input())
