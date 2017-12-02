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

## Day 2

Today's problem requires us to get the checksum based on the input but with some custom rules.
It seems likely that these rules are going to change so I think that whatever the rule is in the first part,
it should be isolated.

#### Part 1

Listening to my advice from yesterday, let's write some tests first (There is only one example today, I might need to write more...):

```python
assert process(["5\t1\t9\t5", "7\t5\t3", "2\t4\t6\t8"]) == 18
```

Now let's get to the solving part:  
Our input provider returns each line as a different element in a list, the problem is asking us to get a value for each line and the add it up.  
I think I will isolate that line logic since it seems likely to change. 
Unlike the example, today's input is a square matrix so I am hoping that the second part will not ask us to parse columns instead of rows, we will need to change the current code otherwise.  
They are asking us to get the minimum and maximum element of each row, subtract them and add that to the total. The first thing to take into account is that the input provided is a string so we need to map it to integer.  
Here is the process function:

```python
def process(input):
    total = 0
    for row in input:
        numbers = list(map(int, row.split('\t')))
        row_result = min_max(numbers)
        total = total + row_result
    return total
```

Now let's implement the core logic of this part. Python has some built in functions (`min()`,`max()`)that will make this very easy. 
It is not the quickest solution since we are parsing the array twice to get each value, but I prefer how it looks:
You can decide which one you use:

```python
def min_max(numbers):
    return max(numbers) - min(numbers)
```
or
```python
def min_max(numbers):
    max_n = 0
    min_n = numbers[0]
    for n in numbers:
        max_n = n if n > max_n else max_n
        min_n = n if n < min_n else min_n
    return max_n - min_n        
```

I personally prefer the first one: short, clean, concise.

Now that we have all of the parts, let's run it!

```python
print(process(get_input()))  # returns 21845
```

#### Part 2

Luckily for us, the second part is asking us to process each row, so seems like the previous code is going to be useful! We need to get the `min_max()` function out of the
process so we can pass it as a parameter:

```python
def process(input, row_process):
    total = 0
    for row in input:
        numbers = list(map(int, row.split('\t')))
        total = total + row_process(numbers)
    return total
    
assert process(["5\t1\t9\t5", "7\t5\t3", "2\t4\t6\t8"], min_max) == 18

print(process(get_input(), min_max))
```

Everything still good after this, let's now write some new tests for the second part:

```python
assert process(["5\t9\t2\t8", "9\t4\t7\t3", "3\t8\t6\t5"], divisible) == 9
```

We don't even have a `divisible()` function yet, so let's get to it.  
Now they need to get the two elements of each row that are divisible. It feels like there must be some *maths* way of doing it
but for now I'm just going to do the obvious, for each element, I will compare it with each other (I'll research on other method
later):

```python
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
```

I missed the `if n == m: break` at first, but hey, there is a reason for the tests.

Let's now run it and see the anwser:

```python
print(process(get_input(), divisible))  # returns 191.0
```

And that's it for the second day. Looking forward to tomorrow!