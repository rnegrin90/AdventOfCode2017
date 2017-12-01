# Advent of Code 2017 solutions

This time of the year again! I decided to go with **python** this year to get some practice!

## Day 1

The day one seems simple (although it took me a few reads to understand it!). I thought about a regex at the beginning
but since the list is **circular** it will be simpler to use a list.
An initial draft of the solution would be to parse the array. Each element is compared only with the next one, if they
match we will add that number to the cumulative result. We also need to cater for the fact that the list is circular,
since we are only comparing 2 elements I'll just start from the last one and start from there.
That seems easy enough to turn into code:

```python
def process():
    input = list(get_input()[0])
    result = 0
    for i in range(-1, len(input) - 1):
        result = result + (int(input[i]) if input[i] == input[i + 1] else 0)
    return result
```

`get_input()` is a function placed in a repository of the common functions likely to be reused for the next few days.
There will be an input every day so this is a no brainer.
I quickly realised that there is no way to test that (note to self: **can you use TDD please?**), so here is the modified version:

```python
def process(input):
    split_input = list(input)
    result = 0
    for i in range(-1, len(split_input) - 1):
        result = result + (int(split_input[i]) if split_input[i] == split_input[i + 1] else 0)
    return result
```

With this we can do stuff like:

```python
assert process('1122') == 3
assert process('1111') == 4
assert process('1234') == 0
assert process('91212129') == 9

print(process(get_input()[0]))  # returns 1119
```

First star done!

Now for the second one they change the element we compare. It feels like we will need to abstract that logic into a different function,
but let's add some tests first:

```python
assert process('1212') == 6
assert process('1221') == 0
assert process('123425') == 4
assert process('123123') == 12
assert process('12131415') == 4

print(process(get_input()[0]))
```

These fail as expected. I haven't looked at the new logic too much yet but let's abstract the initial element selection on the existing code.
We end up with this:

```python
def process(func, input):
    split_input = list(input)
    result = 0
    for i in range(-1, len(split_input) - 1):
        result = result + (int(split_input[i]) if split_input[i] == func(i, split_input) else 0)
    return result

def get_next_element(index, array):
    return array[index + 1]
```

Now we can create another function that will contain the logic for the new requirements.
They want to compare the current element with the one that is **halfway around**. Simple, we just add the
`array.length/2` to current position and apply a `mod` so we don't go over the index. They said the array is always
**even** so we don't need to worry for some edge cases (_thankfully_).
Turning this into code looks like this:

```python
def get_next_halfway(index, array):
    next_el = (index + int(len(array)/2)) % len(array)
    return array[next_el]
```

Run the tests and **bingo**! All pass:

```python
assert process(get_next_halfway, '1212') == 6
assert process(get_next_halfway, '1221') == 0
assert process(get_next_halfway, '123425') == 4
assert process(get_next_halfway, '123123') == 12
assert process(get_next_halfway, '12131415') == 4

print(process(get_next_halfway, get_input()[0]))  # returns 1420
```

This is the second star done! An easy start and already looking forward to tomorrow!