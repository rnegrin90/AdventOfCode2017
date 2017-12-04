from common import get_input


def is_unique(password):
    return password.split()


def no_anagrams(password):
    return list(map(lambda w: ''.join(sorted(w)), password.split()))


def is_valid(password, condition):
    words = condition(password)
    unique_words = set(words)
    return len(words) == len(unique_words)


def process(input, condition):
    valid_count = 0
    for password in input:
        if is_valid(password, condition):
            valid_count += 1
    return valid_count


assert is_valid('aa bb cc dd ee', is_unique) is True
assert is_valid('aa bb cc dd aa', is_unique) is False
assert is_valid('aa bb cc dd aaa', is_unique) is True

print(process(get_input(), is_unique))

assert is_valid('abcde fghij', no_anagrams) is True
assert is_valid('abcde xyz ecdab', no_anagrams) is False
assert is_valid('a ab abc abd abf abj', no_anagrams) is True
assert is_valid('iiii oiii ooii oooi oooo', no_anagrams) is True
assert is_valid('oiii ioii iioi iiio', no_anagrams) is False

print(process(get_input(), no_anagrams))
