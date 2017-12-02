from common import get_input


def min_max(numbers):
    return max(numbers) - min(numbers)


def divisible(numbers):
    for n in numbers:
        for m in numbers:
            if n == m:
                break
            if n % m == 0:
                return n / m
            if m % n == 0:
                return m / n
    return 0


def process(input, row_process):
    total = 0
    for row in input:
        numbers = list(map(int, row.split('\t')))
        total = total + row_process(numbers)
    return total


assert process(["5\t1\t9\t5", "7\t5\t3", "2\t4\t6\t8"], min_max) == 18

print(process(get_input(), min_max))

assert process(["5\t9\t2\t8", "9\t4\t7\t3", "3\t8\t6\t5"], divisible) == 9

print(process(get_input(), divisible))
