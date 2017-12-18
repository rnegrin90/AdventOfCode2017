from common import get_input


def spin(pos, times, length):
    return (pos + times) % length + 1


def process(input):
    pos = 0
    array = [0]
    step = int(input)
    for i in range(1, 2018):
        pos = spin(pos, step, i)
        array.insert(pos, i)
    return array[array.index(2017)+1]


def process2(input):
    pos = 0
    step = int(input)
    inserted = 0
    for i in range(1, 50000001):
        pos = spin(pos, step, i)
        if pos == 1:
            inserted = i
    return inserted


assert process(3) == 638

print(process(get_input()[0]))

print(process2(get_input()[0]))
