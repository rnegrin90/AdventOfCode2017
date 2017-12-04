from common import get_input


def is_unique(password):
    passphrase = password.split()
    unique = set(passphrase)
    return len(passphrase) == len(unique)


def no_anagrams(password):
    passphrase = list(map(lambda w: ''.join(sorted(w)), password.split()))
    unique = set(passphrase)
    return len(passphrase) == len(unique)


def process(input, is_valid):
    valid_count = 0
    for password in input:
        if is_valid(password):
            valid_count += 1
    return valid_count


assert is_unique('aa bb cc dd ee') is True
assert is_unique('aa bb cc dd aa') is False
assert is_unique('aa bb cc dd aaa') is True

print(process(get_input(), is_unique))

assert no_anagrams('abcde fghij') is True
assert no_anagrams('abcde xyz ecdab') is False
assert no_anagrams('a ab abc abd abf abj') is True
assert no_anagrams('iiii oiii ooii oooi oooo') is True
assert no_anagrams('oiii ioii iioi iiio') is False

print(process(get_input(), no_anagrams))