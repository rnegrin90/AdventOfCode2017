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

## Day 3

The challenge today requires us to work on a matrix that is filled in a spiral pattern. 
They ask us to calculate the distance from the origin to the position of a given number.  
The second part seems trivial, even a candidate to be moved to **common.py**, but the challenge
lies on how to represent the matrix.

#### Part 1

As usual, let's write some tests first:

```python
assert process(1) == 0
assert process(12) == 3
assert process(23) == 2
assert process(1024) == 31
```

We need a function that given a number, will return its position on the array. I feel like
there should be a mathematical formula that describes how a spiral grows outward, but I want 
to try to figure it out by myself, I'll research more on this later.  

I'm going to expand the example to have more examples and help myself visualize what's going on:

```
101 100   99   98   97   96   95   94   93   92   91
102  65   64   63   62   61   60   59   58   57   90
103  66   37   36   35   34   33   32   31   56   89
104  67   38   17   16   15   14   13   30   55   88
105  68   39   18    5    4    3   12   29   54   87
106  69   40   19    6    1    2   11   28   53   86
107  70   41   20    7    8    9   10   27   52   85
108  71   42   21   22   23   24   25   26   51   84
109  72   43   44   45   46   47   48   49   50   83
110  73   74   75   76   77   78   79   80   81   82
111 112  113  114  115  116  117  118  119  120  121
```

I discarded having a matrix in memory because you would need to know beforehand how big the matrix
is going to be (which we don't) or create the whole matrix from the beginning and expand it
every time it gets filled up.  
I would like to get a way of obtaining the position of the number without building up the whole matrix.  

I think that if we can find which level the number is located, then we can work our way up from there:

| level | capacity |
| ----- | -------- |
| 0     | 1        |
| 1     | 8        |
| 2     | 16       |
| 3     | 24       |

The relation seems evident: `level*8`  
For a number **N**, we can iterate starting on 0 to find out the level which cumulative capacity
is smaller than **N**.

```python
def get_level(n):
    level = 0
    capacity = 1
    while n > capacity:
        level += 1
        capacity += level * 8
    return level, capacity
```

Once we have found which layer is the number in, we need to find in which part of the matrix the number is in.
There are 4 quadrants:
- **x** = +level, **y** = [-(level+1), level]
- **x** = -level, **y** = [(level-1), -level]
- **y** = +level, **x** = [(level-1), -level]
- **y** = -level, **x** = [-(level+1), level]

We need to place our number in one of these quadrants, this will tell us one of the coordinates, and a range for the
 second one.  
To place the number in one of these quadrants we can use the cumulative capacity again. Let's see an example:

- In the matrix shown above, the number 18 is located in the 2nd level.
- We know that the 2nd level range is [10, 25] => 16
- We want to find out which side of the matrix 18 is, so if there are 16 numbers, each side will have 16/4 elements. 
- The last element of the previous level is 9, therefore our number is the 18 - 9 = 9th element in this level
- 9 / 4 = 2.25, if we `ceil(2.25)` = 3, therefore our number is located on the 3rd quadrant [**y** = +level, **x** = [(level-1), -level]]

The last thing we need to work out is *where* in that quadrant the number is. This bit is slightly more complicated
to code because each the smaller number of each quadrant starts in a diferent position and the vector they follow to
grow is different.  
I will skip the thinking process and go to the solution directly:

```python
def positive_x(level, position):
    return level, (-level+1)+((position-1) % (level*2))


def positive_y(level, position):
    return -(-level+1)-((position-1) % (level*2)), level


def negative_x(level, position):
    return -level, -(-level+1)-((position-1) % (level*2))


def negative_y(level, position):
    return (-level+1)+((position-1) % (level*2)), -level
```

Since whether the `x` or `y` match the value of `level` is what determines the quadrant, I named the functions
accordingly.

At this point we are ready to have a function that will return us the position of the number in this spiral matrix

```python
def get_location(n):
    level, capacity = get_level(n)
    if level == 0:
        return 0, 0
    position = n - (capacity - level * 8)
    quadrant = math.ceil(position / (level*2))
    return {
        1: positive_x(level, position),
        2: positive_y(level, position),
        3: negative_x(level, position),
        4: negative_y(level, position),
    }[int(quadrant)]
```

Now we know *where* our number is, but this is not it! We still need to find out the distance from the origin to it.  
The manhattan distance is very simple to code. I feel like it will show up again in the course of this edition so I added it
 to the common functions library:
 
```python
def manhattan_distance(start, end):
    sx, sy = start
    ex, ey = end
    return abs(ex - sx) + abs(ey - sy)
```

Finally we are equipped with all we need to solve the first part:

```python
def process(input):
    x, y = get_location(int(input))
    return manhattan_distance((0, 0), (x, y))

print(process(get_input()[0]))  # returns 419
```

#### Part 2

At first glance it doesn't seem we will be able to reuse anything from the first part. Apparently we do need
to build the matrix, that is unfortunate.

This time there are no test, but they gave us another example, I will write some tests based on that:

```python
assert process_second(24) == 25
assert process_second(54) == 57
assert process_second(700) == 747
assert process_second(200) == 304
```

After some more thought, our existing function `get_location(n)` takes a number and returns *where* on the matrix
it is located. We can use it to map a 1-dimension array to the 2-d spiral array.  
However, they want us to check the adjacent values, so we need the reverse function `get_number(x, y)` that from 
the position returns where the value will be in the 1-d array. Let's start from there, first by writing some tests:

```python
assert get_number(-1, 1) == 5
assert get_number(2, -1) == 10
assert get_number(5, -5) == 121
assert get_number(0, 0) == 1
assert get_number(-3, -1) == 41
assert get_number(-1, 4) == 62
assert get_number(3, -4) == 80
```

I am basing this tests on the matrix drawn before on the first part, I tried to pick all of the edge cases I could.
Since the function `get_location(1)` returns `[0,0]`, we will make this a special case in our new function::

```python
def get_number(x, y):
    if x == 0 and y == 0:
        return 1
```

This is a good start, but there are ~~a few~~ infinite more cases, so let's work out the rest.  
Following the previous logic, we can make use of the concept of `level` and `quadrant`. The level for any
given `[x, y]` will be the biggest absolute value, therefore `level = max(abs(x), abs(y))`

Next, we need to know the first number of the level:

```python
def get_start(level):
    result = 1
    for i in range(0, level):
        result += i * 8
    return result+1
```

And now the quadrant:

```python
def get_quadrant(x, y, level):
    if abs(x) == level:
        if x > 0:
            if y > -level:
                return 1, y + level - 1
            else:
                return 4, x + level - 1
        else:
            if y < level:
                return 3, level - 1 - y
            else:
                return 2, level - 1 - x
    else:
        if y > 0:
            return 2, level - 1 - x
        else:
            return 4, x + level - 1
```

I'm sure there is a more elegant way of writing this, but I was way behind by this time and didn't want
to spend more time, this worked. I am returning a second argument in this function, I wil talk about this later.

At this point we now the level and the quadrant. This narrows down the set to the numbers that fit inside 1 side of
the square. This set is given by: `range((start+((quadrant-1)*level*2)), (start+(quadrant*level*2)))`.  
We can turn this into a list and get a 0-index array, but how do we turn the positional axis into a 0-index array? This 
is where the `offset` returned in the previous function comes into play. In the previous function, we find out
whether `x` or `y` is the positinal axis, and we use the other to tell: `On the 0-index vector, move Z positions to find the number`.

The final function looks like this:

```python
def get_number(x, y):
    if x == 0 and y == 0:
        return 1
    level = max(abs(x), abs(y))
    start = get_start(level)
    quadrant, offset = get_quadrant(x, y, level)
    r = list(range((start+((quadrant-1)*level*2)), (start+(quadrant*level*2))))
    return r[offset]
```

We have now a way of turning points into numbers (indexes in a 1-d array) and turning numbers into 
points in the 2-d array. But before we start coding the core logic, we need a function that gives us the adjacent
squares we have to sum in order to build the spiral array.

```python
def get_surroundings(x, y):
    return [(x+1, y), 
            (x+1, y+1), 
            (x, y+1), 
            (x-1, y), 
            (x-1, y-1), 
            (x, y-1), 
            (x-1, y+1), 
            (x+1, y-1)]
```

Finally, we are ready to tackle the main problem. We start with the position `[0,0]` pre-filled with 1.
Since we want to find the first value that is larger than the input, we will use that as our stop condition.
The algorithm will:
- Look for the 2-d coordinates the current position N in the 1-d array will represent
- Get all the surroundings of that point
- Foreach of the surroundings will check the existing array for the values already filled
- Add all the existing numbers found, and set the result as the value of that position
- When the inserted value is greater than the input, return said value

The algorithm translates to code easily, but since some position of the array might be accessed before they 
are filled, a try, except block has been added to just ignore those non-existent positions.

```python
def process_second(input):
    inserted = 1
    array_pos = 1
    array = [None, 1]
    while inserted <= int(input):
        array_pos += 1
        x, y = get_location(array_pos)
        pos_to_check = get_surroundings(x, y)
        inserted = 0
        for cx, cy in pos_to_check:
            try:
                n = array[get_number(cx, cy)]
                inserted += n
            except:
                pass
        array.append(inserted)
    return inserted
```

All tests are passing, let's now run the given input

```python
print(process_second(get_input()[0]))  # returns 295229
```

And that's it for the third day. I have the feeling that maths would have helped a lot here, but I had a lot
of fun figuring out by myself!

## Day 4

Today we are required to check the validity of some passphrases. Seems easy, let's get to it!

#### Part 1

Each passphrase is composed of individual word, and it is considered valid as long as all the words are unique.
Let's get some tests in place:

```python
assert is_valid('aa bb cc dd ee') is True
assert is_valid('aa bb cc dd aa') is False
assert is_valid('aa bb cc dd aaa') is True
```

I run the tests against the core logic instead of the `process()` function because the process will just count the valid ones and return the total,
the examples focus on this core logic, so I assume that the second part will change this logic, so makes sense to keep it isolated.

This is the main method:

```python
def process(input, is_valid):
    valid_count = 0
    for password in input:
        if is_valid(password):
            valid_count += 1
    return valid_count
```

Let's now start with the main problem. We will get each row of the input separately and check it's validity individually.
I think that using a set for this would be ideal. We can do two things:
- Input each element manually in the set, if it is already there, then it is not valid:
```python
def is_valid(password):
    words = password.split()
    dictionary = {}
    for word in words:
        if word not in dictionary:
            dictionary[word] = 1
        else:
            return False
    return True
```
- Simply create a `set()` from the list of words, it will remove any duplicates automatically
```python
def is_valid(password):
    words = password.split()
    unique_words = set(words)
    return len(words) == len(unique_words)
```
Both options share the same complexity on the worst case but the first option should be more efficient on average. However
we find ourselves again between complexity or clarity. I will go with clarity since the second option is much more elegant and simple.

This should be all there is to it, let's run it

```python
print(process(get_input(), is_valid))  # returns 451
```

#### Part 2

The logic for the second part remains mostly the same but now it is asking us to check for anagrams. I think we can easily
adapt our current solution for this, but first things first:

```python
assert no_anagrams('abcde fghij') is True
assert no_anagrams('abcde xyz ecdab') is False
assert no_anagrams('a ab abc abd abf abj') is True
assert no_anagrams('iiii oiii ooii oooi oooo') is True
assert no_anagrams('oiii ioii iioi iiio') is False
```

A very easy way of checking whether two words are anagrams is to order their characters. If the resulting words are equal, then
they are anagrams. We can take advantage of the `map()` function in python and get a list of words ordered alphabetically:

```python
words = list(map(lambda w: ''.join(sorted(w)), password.split()))
```

With this we can build our new function:

```python
def no_anagrams(password):
    words = list(map(lambda w: ''.join(sorted(w)), password.split()))
    unique_words = set(words)
    return len(words) == len(unique_words)
```

I noticed that both functions share the core logic of comparing sets so I decided to isolate that. This is the final result
after the refactoring:

```python
def is_unique(password):
    return password.split()


def no_anagrams(password):
    return list(map(lambda w: ''.join(sorted(w)), password.split()))


def is_valid(password, condition):
    words = condition(password)
    unique_words = set(words)
    return len(words) == len(unique_words)
```

Test pass, time to run today's input:

```python
print(process(get_input(), no_anagrams))  # returns 223
```

This is today's challenge, a very simple one in contrast with yesterday's! We'll see what awaits us tomorrow.

## Day 5

Today we need to find the way out of a maze. The maze is a simple array but we must follow
some rules to get out. We are asked for how many steps are required for the given input.

#### Part 1

Only one example today:

```python
assert process(["0", "3", "0", "1", "-3"]) == 5
```

The rules are very simple:
 - We start on the position 0 of the array
 - We move the number of steps indicated by the number in our current position
 - Once we have decided how many steps we are moving, we increase the last instruction by **1**
 - We exit the maze when we try to access a position outside of the array

These requirements are easily turned into code, let's get to it:

```python
def process(input):
    int_input = list(map(int, input))
    position, steps, length = 0, 0, len(int_input)
    while 0 <= position < length:
        offset = int_input[position]
        int_input[position] += 1
        position += offset
        steps += 1
    return steps
```

Since we are asked for the number of steps taken, we need to keep track of how many times
the loop has run.

This is all it is required for the first part, really straightforward!

```python
print(process(get_input()))  # returns 396086
```

#### Part 2

Second part still maintains the way we move and exit the maze, but it adds some additional
logic when modifying the last instruction.
I think we can isolate what is different and provide it to the `process()` function to reuse as
much code as possible.

The previous tests now should take 10 steps according to this new rules:

```python
assert process(["0", "3", "0", "1", "-3"], greater_than_three) == 10
```

All we need to change is how the current position is modified before moving to the new one.
Let's isolate that logic on the existing version:

```python
def increase_by_one():
    return 1


def process(input, get_offset_change):
    int_input = list(map(int, input))
    position, steps, length = 0, 0, len(int_input)
    while 0 <= position < length:
        offset = int_input[position]
        int_input[position] += get_offset_change(offset)
        position += offset
        steps += 1
    return steps
```

Now that we have parametrized that logic we can create the new function for the second part:

```python
def greater_than_three(offset):
    return 1 if offset < 3 else -1
```

All done, all is left is to run it:

```python
print(process(get_input(), greater_than_three))  # returns 28675390
```

Wow! that took some time! I can't think of any changes that might improve performance but I'll
give it a thought and come back if I find anything.

That is all for today!

## Day 6

We will be emulating a memory reallocation system. The rules are quite extensive but simple in concept.
Let's start!

#### Part 1

The first part explains how to redistribute the memory and runs through an example, however, what they
ask for is how many steps must be taken before we see a distribution already seen (therefore resulting
in a infinite loop)
As always, let's go with the tests first:

```python
assert process("0\t2\t7\t0") == 5
```

They provide a tab-separated string where each number represents the current status of each memory bank.
First thing that we need to do is to turn it into a list of integer:

```python
memory = list(map(int, input.split()))
```

Next thing that I think about is state storage. I think that the simplest way of checking
whether a state has been already visited is storing it in a set, but for that we need
to serialise the current state:

```python
def serialize(memory):
    return '/'.join(map(str, memory))
```

This feels like a function that will be used more during the course of the challenge, I think I will
move it to the shared library later...

Let's go now with the loop detection logic. It should be pretty straight forward:
- Each time we visit a configuration we store it in a set
- While the current configuration is not in the set, we perform a memory redistribution.
- We will have a counter while performing this algorithm to keep track of the number of cycles.

```python
def process(input):
    memory = list(map(int, input.split()))
    state_cache = set()
    cycles_to_loop = 0
    while serialize(memory) not in state_cache:
        state_cache.add(serialize(memory))
        memory = redistribute_blocks(memory)
        cycles_to_loop += 1
    return cycles_to_loop
```

After this the only thing left is to code the redistribution logic:
- Search the largest number (**n**) in the array
- Set that position to 0
- Move to the next position in the array, if the position is larger than the size of the array, go back to the beginning
- Add 1 to the number in that position, subtract 1 from **n**
- Stop when **n** = 0

Let's translate it into code:

```python
def redistribute_blocks(memory):
    max_value = max(memory)
    index = memory.index(max_value)
    memory[index] = 0
    while max_value > 0:
        index = (index + 1) % len(memory)
        memory[index] += 1
        max_value -= 1
    return memory
```

Now we have everything we need, let's run the solution:

```python
print(process(get_input()[0]))  # returns 11137
```

#### Part 2

The second part is simple and short. All they want to know is, once you find the loop, how many cycles
are part of that loop.
I don't think the current solution requires a lot of modification. We can change the set to be
a dictionary that stores the number of times the configuration has been seen, when the first 2 appears,
we know we have been through the loop 2 times.

For the test, I assume we will use the same loop and both solutions will be returned on the same function
so I'll just modify the previous test:

```python
assert process("0\t2\t7\t0") == (5, 4)
```

We will now have 2 counters, and each one will increase depending on whether the current state
has been already seen or not:

```python
def process(input):
    memory = list(map(int, input.split()))
    state_cache = {}
    cycles_to_loop = 0
    cycles_in_loop = 0
    current_state = serialize(memory)
    while current_state not in state_cache or state_cache[current_state] != 2:
        if current_state not in state_cache:
            state_cache[current_state] = 1
            cycles_to_loop += 1
        else:
            state_cache[current_state] += 1
            cycles_in_loop += 1
        memory = redistribute_blocks(memory)
        current_state = serialize(memory)
    return cycles_to_loop, cycles_in_loop
```

An alternative implementation could be to simply run the first loop until we get to the first
visited state and then continue where that one left off until it is found a second time:

```python
def process(input):
    memory = list(map(int, input.split()))
    state_cache = {}
    cycles_to_loop = 0
    while serialize(memory) not in state_cache:
        state_cache[serialize(memory)] = 1
        memory = redistribute_blocks(memory)
        cycles_to_loop += 1
    cycles_in_loop = 0
    while state_cache[serialize(memory)] != 2:
        state_cache[serialize(memory)] += 1
        memory = redistribute_blocks(memory)
        cycles_in_loop += 1
    return cycles_to_loop, cycles_in_loop
```

None of them are particularly cleaner so I don't really have a preference, but the second one
has lower cyclomatic complexity.

Now let's run the solution:

```python
print(process(get_input()[0]))  # returns (11137, 1037)
```

## Day 7 <a name="day7"></a>

Trees! To get today's answers we need to create a tree structure. It seems to be a simple tree, so should not be
too difficult, let's get to it!

#### Part 1

They ask for the name of the root node. This one is tricky, because there is no actual need
to build a tree in memory to get that answer, buuuuuuut we all know it will be required for the
second part. Since I am definitively not competing for points, I'll start building the tree now.
Before starting, another thing I noticed is the number at the side of each node (it's weight
apparently). It is clear that the second part is going to involve using those, so I'll make sure they
are stored correctly against each node.

Here is the intial test case:

```python
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
assert process(test_input.split('\n')) == "tknk"
```

I think I am going to store the tree as a dictionary instead of a linked structure. Let's define
our node class:

```python
class Node:
    def __init__(self, uid):
        self.uid = uid
        self.next = set()


class Program(Node):
    def __init__(self, uid, weight):
        super().__init__(uid)
        self.weight = weight
```

I created Node separate from program to move it to the `common.py` library just in case there are
more tree related challenges.

I can store the whole tree in a dictionary with the `uid` as the key and the `Program` object as value.
I will define `next` as a set of uid. I decided to do this, as opposed to having the reference to the
actual node because initially, we don't know what the root node is or the order on the input. Having
it this way, I only need to parse the input once.

Now I need something that takes a line from the input and turns it into a `Program` object:

```python
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
```

Nothing fancy here, I didn't want to waste time building a regex for `re` so went for the quick and easy solution.

I need to generate the tree and I would like to isolate that logic so it can be used again in the future (seems likely that we will
see another tree this year):

```python
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
```

- The `generate_tree` function requires a list where each element contains the definition of a node and
a `parse_node` function that will turn whatever the format the input elements come in, into a `Node` class.
It then stores all the nodes in a dictionary and parses it to search the root (or _head_) node.

- `get_head_node` parses the list of nodes searching for a node id that does not appear as a children
node of any other. It filters out any leaf node first to reduce the starting set.

Now that we have a tree (and the head node) we just need to return the uid of the node:

```python
def process(input):
    tower, head_node = generate_tree(input, parse_program)
    return head_node.uid
```

Let's see the result

```python
print(process(get_input()))  # returns 'bsfpjtc'
```

#### Part 2

As expected, the second part requires having the tree structure and using the node's weights.
Since the test case provided is the same and to resolve the second part I need structure created
by the first part, I'll just modify the response to include both:

```python
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
```

The problem ask us to find what would be the expected weight for the tower to be balanced (took
me a few errors to find this out), but to get there we need to do find which node is unbalancing
the tree and what is the weight difference between the balanced and unbalanced branches.
There are a few ways to get there but I the first one that came to my head was to introduce a cumulative
weight property in each node that will contain the 
We also need to add the concept of cumulative weight (the sum of the weight of all the branches)
so let's update our class:

```python
class Program(Node):
    def __init__(self, uid, weight):
        super().__init__(uid)
        self.weight = weight
        self.total_weight = 0
```

We also need to calculate that weight. Calculating it is very simple using recursion:

```python
def generate_subtree_weight(node, tree):
    if len(node.next) > 0:
        for sub_node in node.next:
            node.total_weight += generate_subtree_weight(tree[sub_node], tree)
    node.total_weight += node.weight
    return node.total_weight
```

I am not overly keen on passing a mutable object to a function (the tree would come out modified
and the final return value is not really being used) but it just makes it simpler. To make the main function
clearer I wrapped this functionality into another that states what is happening a bit more clearly:

```python
def get_weighted_tower(head, tower):
    generate_subtree_weight(head, tower)
    return tower
```

Now that we have the tree in a state where we can answer the question, let's implement the
algorithm.
I want to use recursion here as well, and it will follow this logic:
- Look at the children of the current node
- Get the total weight of the subtree they hold
- Find the only branch that is unbalanced, if no branch is unbalanced, skip next step
- Repeat the process having the unbalanced node as the current node
- Get the weight difference between the current node and the other branches in the same level

This is a rough plan of what I planned to do, the implementation is slightly different, but it
follows that pattern:

```python
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
```

Let's go bit by bit:
- `this_level` is a dictionary where the key is the total weight of a branch and the value is
a list of uid of the nodes that share the same weight. I have made an assumption here (maybe a
risky one) that every level will have more than two branches. If a level has two branches the
behaviour would need to change (maybe using a stack to keep the nodes that need to be visited).
- The first loop fills said dictionary
- If the length of the dictionary is 1 (or less if it has no children), it will return None,
signifying that it is balanced
- If it is greater than 1, then the key that has exactly 1 value will be the unbalanced branch
- So we now call the same function with the unbalanced node as the parameter.
- We now check what the recursion brought back:
    - If the return of the function is `None` it means the children of that node are balanced,
therefore he is the one that is causing the unbalance. We need to calculate the expected weight
of the node for it to be balanced (we do that with help of the `this_level` dictionary).
    - If the result is not `None` it meas somewhere else the result was found, so we need to
    end the recursion and bubble up the result.

That is all we need for today, let's have a look at the updated `process` function:

```python
def process(input):
    tower, head_node = generate_tree(input, parse_program)
    tower = get_weighted_tower(head_node, tower)
    expected_weight = get_expected_weight(head_node, tower)
    return head_node.uid, expected_weight
```

And the result:

```python
print(process(get_input()))  # returns ('bsfpjtc', 529)
```

That's it for today. I'm not overly excited about the solution, there are probably
much better solutions, but this one does the job. See you tomorrow!

## Day 8

Today we need to compute the result of some operations specified on the input provided.
This operations contain conditional elements.

#### Part 1

We need to return the variable that contains the highest number, let's write a tests for the
input provided:

```python
test_input = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""
assert process(test_input.split('\n')) == 1
```

I see a cheeky way of doing this using `eval`, but let's be nice and not use it... (maybe some other
time).
First we need to parse the things that interests us from the input. It seem like it is stable through
the whole file, so let's go with a regex (first of the season!):

```python
def parse_instruction(instruction):
    return re.search(r"(\w+) (\w+) (-?\d+) if (\w+) ([><=!]+) (-?\w+)", instruction).groups()
```
This should return a list with all the matches, so let's unpack that into variables:

```python
token, op, val, cond_token, cond_op, cond_val = parse_instruction(instruction)
```

According to the rules, we need to make the operation if the condition is true, and that takes us
to the use of the operators. We need to map the operator symbol to the actual operation. We can do
that with a simple dictionary:

```python
operators = {
    '>': lambda left, right: left > right,
    '<': lambda left, right: left < right,
    '>=': lambda left, right: left >= right,
    '<=': lambda left, right: left <= right,
    '==': lambda left, right: left == right,
    '!=': lambda left, right: left != right,
    'dec': lambda left, right: left - right,
    'inc': lambda left, right: left + right
}
```

Now that we have our operators, we can go ahead and check whether the condition is met:

```python
def process_condition(cond_token, cond_op, cond_val, registry):
    left_val = 0
    right_val = int(cond_val)
    if cond_token in registry:
        left_val = registry[cond_token]
    return operators[cond_op](left_val, right_val)
```

We need to pass the registry because the conditions access the value of other variables (0 by default
if the variable has not been seen before).

Last but not least, the function that orchestrates all the other logic and performs the `inc/dec`
operation:

```python
def process(input):
    registry = dict()
    for instruction in input:
        token, op, val, cond_token, cond_op, cond_val = parse_instruction(instruction)
        cond = process_condition(cond_token, cond_op, cond_val, registry)
        current_val = 0 if token not in registry else registry[token]
        registry[token] = operators[op](current_val, int(val)) if cond else current_val
    return max(registry.values())
```

After calling the parsing and condition analysis functions, all is left is to apply the operation
to the current element (stored in the `registry` dictionary, using the variable name as the key)
if the condition is met, or leaving it untouched otherwise.

Th final result is:

```python
print(process(get_input()))  # returns 3745
```

#### Part 2

The second part for today is very simple for out implementation! We need to return the
highest value ever stored. As usual, since we can get this answer alongside the initial solution,
I'll return both at the same time:

```python
test_input = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""
assert process(test_input.split('\n')) == (1, 10)
```

The only change required for this is to check for the biggest value ever seen every time
a new entry is inserted in the registry. Here is the code:

```python
def process(input):
    registry = dict()
    max_value = 0
    for instruction in input:
        token, op, val, cond_token, cond_op, cond_val = parse_instruction(instruction)
        cond = process_condition(cond_token, cond_op, cond_val, registry)
        current_val = 0 if token not in registry else registry[token]
        registry[token] = operators[op](current_val, int(val)) if cond else current_val
        max_value = registry[token] if registry[token] > max_value else max_value
    return max(registry.values()), max_value
```

There is nothing to explain in these changes since it is just a variable that holds the highes
value ever seen.

If we run it we should see:

```python
print(process(get_input()))  # returns (3745, 4644)
```

A very simple day today, tomorrow is Saturday so we should expect a harder one! Enjoy!

## Day 9

Today we need to process a stream of characters which apparently contains random characters
but some of those characters have meaning. Let's start.

#### Part 1

Seems like we need to calculate a score based on the number of groups and its nesting, let's
write some tests for it:

```python
assert process("{}") == 1
assert process("{{{}}}") == 6
assert process("{{},{}}") == 5
assert process("{{{},{},{{}}}}") == 16
assert process("{<a>,<a>,<a>,<a>}") == 1
assert process("{{<ab>},{<ab>},{<ab>},{<ab>}}") == 9
assert process("{{<!!>},{<!!>},{<!!>},{<!!>}}") == 9
assert process("{{<a!>},{<a!>},{<a!>},{<ab>}}") == 3
```

After reading the requirements seems like the set of characters that we need to pay attention
are: `{}!<>`.
There is also 2 important assumptions stated: **All characters are valid** and **no group is
malformed**; this should make the challenge easier, let's hope it doesn't change on
the second part!

Let's dive into what we need to do with each one of them:
- `{` This character will start a new group which will be closed by the next `}` at the same level
We need to track which level we are at the moment to be able to keep track of the "open groups"
we currently have.
- `}` This one closes the last group opened, going down a level on the "open groups" count.
- `!` This one makes the next character lose its value. I see two ways of implementing this one:
    - Have a `ignore_next` flag activated when we find this character and immediately deactivated
    right after
    - Keep track of the previous character, if it is `!`, ignore the current one.
- `<` This one opens a "garbage" section where **all the other characters are ignored** except
for `>` and `!`. This section has no levels. Seems like we can use a simple `garbage_mode` flag
to achieve this behaviour.
- `>` It will deactivate the `garbage_mode` and go back to normal processing.

We have now all the rules, let's turn them into code:

```python
def process(input):
    garbage_mode = False
    last_char = None
    level, value_sum = 0, 0
    for char in list(input):
        if last_char == '!':
            last_char = None
            continue
        garbage_mode = char == '<' or garbage_mode
        if char == '>':
            garbage_mode = False
        if not garbage_mode and char == '{':
            level += 1
        if not garbage_mode and char == '}':
            value_sum += level
            level -= 1
        last_char = char
    return value_sum
```

A few comments on this code:
- I decided to track the last character for the `!` functionality since the cost is about the
same and feels a bit more resilient for the next stage.
- I increment the score counter when a group is closed, but if could have been done when it is
opened since it was stated that all the groups are correct.

Everything else has been directly turned into code from the previous analysis, let's now
run the given input:

```python
print(process(get_input()[0]))  # returns 16869
```

#### Part 2

This part is simpler than expected! They just want to know how many characters are within the
garbage areas, excluding the `!` and the characters cancelled by them.
The new tests look like this:

```python
assert process("<>")[1] == 0
assert process("<random characters>")[1] == 17
assert process("<<<<>")[1] == 3
assert process("<{!>}>")[1] == 2
assert process("<!!>")[1] == 0
assert process("<!!!>>")[1] == 0
assert process('<{o"i!a,<{i<a>')[1] == 10
```

We used to ignore completely those characters, now we simply need to add an extra condition that
will increase another counter:

```python
def process(input):
    garbage_mode = False
    last_char = None
    level, value_sum, cancelled_chars = 0, 0, 0
    for char in list(input):
        if last_char == '!':
            last_char = None
            continue
        if garbage_mode and char not in ['>', '!']:
            cancelled_chars += 1
        garbage_mode = char == '<' or garbage_mode
        if char == '>':
            garbage_mode = False
        if not garbage_mode and char == '{':
            level += 1
        if not garbage_mode and char == '}':
            value_sum += level
            level -= 1
        last_char = char
    return value_sum, cancelled_chars
```

Now we run it:

```python
print(process(get_input()[0]))  # returns (16869, 7284)
```

And that is it for today!

## Day 10

Seems like we will be building a custom hashing function. Explanation seems long and with a lot
of moving parts, this looks interesting, let's get to it!

#### Part 1

Apparently the example provided is based in a array of length 5 [0..4] but for the main challenge we
will need to use an array of length 256 [0..255]:

```python
assert process("3,4,1,5", 5) == 12
```

Let's go through the steps we will need to make to get to that result and then turn them into
code.

We get the array of lengths from the input but the array we need to apply the hash to will vary
in length, so we can do:

```python
lengths = list(map(int, input.split(',')))
l = list(range(0, size))
```

Now that we have our input sorted, we can start the hashing. This part is a bit more complex
because we have to treat our list as circular:
- For each length we will grab the slice that we need to reverse
- Starting from the current position, we will overwrite it with the each element of the
reversed slice, moving the current position forward after each change. If we overflow the array
we will go back to 0.
- After we finish with each length we will set the starting position of the next iteration
according to the rules, as well as the `skip` value

After turning this into code we end up with:

```python
def custom_hash(l, lengths):
    pos, skip = 0, 0
    for length in lengths:
        sub_list = list(reversed(list(slice_list(l, pos, length))))
        i = pos
        for j in sub_list:
            l[i] = j
            i += 1
            if i >= len(l):
                i = i % len(l)
        pos = (pos+length+skip) % len(l)
        skip += 1
    return l, pos, skip
```

I have isolated the bit that takes care of slicing the list since there will be a decent
amount of code taking care of the fact that it is a circular list.
**Update** ~~I was living in a lie~~ I just found out `itertools` has a `cicle()` method
that takes care of making a list circular, I'll write the initial version and then a modified
one with my newly acquired knowledge.

```python
def slice_list(input_list, current_pos, length):
    if length == 0:
        return
    next_pos = (current_pos+length) % len(input_list)
    pos = current_pos
    if next_pos == pos:
        yield input_list[pos]
        pos += 1
    while pos != next_pos:
        yield input_list[pos]
        pos += 1
        if pos >= len(input_list):
            pos = pos % len(input_list)
```

The core logic for this is the last `while` loop. The two `if` had to be added to cater for
edge cases when the length was 0 or equal to the array size.
While the current position is different from the target position, it will **yield** the current
element and keep iterating.
Let's now see what this looks like using `cycle`:

```python
def slice_list(input_list, current_pos, length):
    circular = cycle(input_list)
    for i in range(0, current_pos+length):
        if i >= current_pos:
            yield next(circular)
        else:
            next(circular)
```

It looks so much better! Simple and clear!

After writing the hash function, we should now have the shuffled array, so we need to return the
product of the first and second items:

```python
def process(input, size):
    lengths = list(map(int, input.split(',')))
    l = list(range(0, size))
    result = custom_hash(l, lengths)
    return result[0] * result[1]

print(process(get_input()[0], 256))  # returns 826
```

#### Part 2

The second part builds upon the previous _hashing_ concept, but expands it to eventually
obtain a 32 character hex string.

It seems that even though the hashing logic remains the same, we need to process both the input
and output further (as well as repeat the hashing process). This will need a lot of refactoring
on the original code, I will go through the bits I think we might need to refactor first:

- The input is not parsed straight into a `int` array
```python
def to_int_list(input):
    return list(map(int, input.split(',')))
```
- Result is no longer the multiplication of the first two, it involves some operations on
the shuffled array
```python
def product_result(list):
    return list[0] * list[1]
```
- The hashing algorithm needs to be repeated `64` times now, but maintaining the previous position
in the array and the skip size
```python
def process(input, size, rounds, parse_input, process_result):
    lengths = parse_input(input)
    l = generate_range(size)
    pos, skip = 0, 0
    for i in range(0, rounds):
        result, pos, skip = custom_hash(l, lengths, pos, skip)
    return process_result(result)
```
- I decided I might as well refactor the range generation
```python
def generate_range(size):
    return list(range(0, size))
```
- Test and solution for the first part looks like this now
```python
assert process("3,4,1,5", 5, 1, to_int_list, product_result) == 12

print(process(get_input()[0], 256, 1, to_int_list, product_result))  # returns 826
```

Now we are ready to write the tests for the second part:

```python
assert process("", 256, 64, generate_from_ascii, hex_result) == "a2582a3a0e66e6e86e3812dcb672a272"
assert process("AoC 2017", 256, 64, generate_from_ascii, hex_result) == "33efeb34ea91902bb2f59c9920caa6cd"
assert process("1,2,3", 256, 64, generate_from_ascii, hex_result) == "3efbe78a8d82f29979031a4aa0b16a9d"
assert process("1,2,4", 256, 64, generate_from_ascii, hex_result) == "63960835bcdc130f0b66d7ff4f6a5a8e"
```

Let's now go with the first moving part, `generate_from_ascii`. We need to turn now each character
from the input into its ASCII value.
We are given an example, so let's write a small test for it:

```python
assert generate_from_ascii("1,2,3") == [49, 44, 50, 44, 51, 17, 31, 73, 47, 23]
```

The logic is pretty straight forward:

```python
def generate_from_ascii(word):
    result = list()
    for c in word:
        result.append(ord(c))
    return result + [17, 31, 73, 47, 23]
```

For the second moving part (`hex_result`) needs a series of steps:
- We need to take our shuffled array or _sparse hash_ and turn it into a dense hash
- Turn the dense hash into a hex string

According to the description, a _dense hash_ is an array of 16 elements, where each element
is the XOR of the 1/16 elements of the _sparse hash_:

```python
def get_dense_hash(input_list):
    hash_result = list()
    steps = int(len(input_list) / 16)
    start = 0
    end = steps
    for i in range(0, 16):
        sl = input_list[start:end]
        hash_result.append(reduce(lambda x, y: x ^ y, sl))
        start += steps
        end += steps
    return hash_result
```

Now to turn it into hex format we can write a small test based on the example and then turn it
into code:

```python
assert to_hex_string([64, 7, 255]) == "4007ff"


def to_hex_string(input_list):
    result = list()
    for element in input_list:
        result.append('{0:02x}'.format(element))
    return ''.join(result)
```

We have now all we need for the second moving part:

```python
def hex_result(list):
    return to_hex_string(get_dense_hash(list))
```

Let's run the code with the given input:

```python
print(process(get_input()[0], 256, 64, generate_from_ascii, hex_result))  # returns "d067d3f14d07e09c2e7308c3926605c4"
```

Another Sunday is over! Not a excessively complex challenge but quite involved, an opportunity to
use TDD!

## Day 11

Again, back to a simple challenge, this time we need to use a cube coordinate system to store
hexagons.

#### Part 1

As usual, let's turn the examples into tests first:

```python
assert process("ne,ne,ne") == 3
assert process("ne,ne,sw,sw") == 0
assert process("ne,ne,s,s") == 2
assert process("se,sw,se,sw,sw") == 3
```

We need to represent in memory an hexagon grid. I tried to think about an efficient way of
doing it, but I quickly decided not to reinvent the wheel and resorted to [this](https://www.redblobgames.com/grids/hexagons/#coordinates-axial).
They in detail over the theory behind the different representations of a hexagon grid. I went for
the axial one since the less coordinates, the better.

We have a set amount of movements, so we can write a dictionary of lambdas that contain these rules:

```python
movements = {
    'n': lambda x, y: (x, y-1),
    's': lambda x, y: (x, y+1),
    'ne': lambda x, y: (x+1, y-1),
    'nw': lambda x, y: (x-1, y),
    'se': lambda x, y: (x+1, y),
    'sw': lambda x, y: (x-1, y+1),
}
```

Once we have the movements defined, well, we need to move:

```python
def process(input):
    x, y = 0, 0
    for dir in input.split(','):
        x, y = movements[dir](x, y)
    return distance((0, 0), (x, y))
```

The input is stored in a single line so we can directly iterate over the split. To get the distance
we need to get the value of `z` first (if you go to the website from before, each hexagon is
actually represented by a set of `x, y, z` coordinates, but since they match the constraint `x + y + z = 0`
we can omit one of them and infer it later.

```python
def get_z(hex_coord):
    x, y = hex_coord
    return -x-y
```

We can now get the distance from one hexagon to any other:

```python
def distance(a, b):
    sx, sy = a
    ex, ey = b
    return (abs(sx - ex) + abs(sy - ey) + abs(get_z(a) - get_z(b))) / 2
```

Everything ready, we can now run our program:

```python
print(process(get_input()[0]))  # returns 796
```

#### Part 2

Short and simple, what was the furthest we ever got while moving around?
We can answer that with a small code change, but let's update the tests first:

```python
assert process("ne,ne,ne") == (3, 3)
assert process("ne,ne,sw,sw") == (0, 2)
assert process("ne,ne,s,s") == (2, 2)
assert process("se,sw,se,sw,sw") == (3, 3)
```

We can do the change directly in `process` we only need to calculate the distance with every movement
and store the highest. There are probably more efficient ways, but this one is simple and requires
almost no changes:

```python
def process(input):
    x, y = 0, 0
    max_distance = 0
    for dir in input.split(','):
        x, y = movements[dir](x, y)
        max_distance = max((max_distance, distance((0, 0), (x, y))))
    return distance((0, 0), (x, y)), max_distance
```

And for the solution:

```python
print(process(get_input()[0]))  # returns (796, 1585)
```

Quick and simple (thanks to that blog for the awesome explanation on cube coordinates!)

## Day 12

I am not too inspired today, so let's go straight to it!

#### Part 1

```python
test_input = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""
assert process(test_input.split('\n'), 0) == 6
```

I set `0` as a parameter from the beginning because I strongly feel we will need to search for some
other number later on...

We need to decide on the data structure that we want to use for this. I was thinking about
a dictionary when I remembered that [Day 7's](#day7) tree structure is exactly what I am looking
for, I just don't want to have a root node (I knew it would be useful to have it in the `common.py`!).

```python
relations, _ = generate_tree(input, parse_line)
```

That should provide us with a dictionary which contains a list to the elements it is linked to,
but we need to define our node parsing function:

```python
def parse_line(line):
    groups = re.search(r'(\d+) <-> ([\d,\s]+)', line).groups()
    node = Node(groups[0])
    node.next = set(groups[1].replace(' ', '').split(','))
    return node
```

Now that we have the data structure, my plan is to look for all the nodes related to the one
we are looking for _(0 in this particular case)_ and get them into a set to get the number of
nodes that are accessible. We have all we need for the `process` function:

```python
def process(input, id):
    relations, _ = generate_tree(input, parse_line)
    sub_group = get_subgroup(relations, str(id), set())
    return len(sub_group)
```

For the last part, we need to create the `get_subgroup` function. It feels like another place
for recursion:

```python
def get_subgroup(relations, id, visited):
    for related in relations[id].next:
        if related not in visited:
            visited.add(related)
            get_subgroup(relations, related, visited)
    return visited
```

In this case we need a visited set because, as stated in the challenge, nodes have each other
in their respective lists. As long as we have not visited the node already, we go to it.
In the end, we just need to return the visited array.

With all this, we can get the challenge answer:

```python
print(process(get_input(), 0))  # returns 152
```

#### Part 2

This part asks us to get the count of all the different groups in the input:

```python
test_input = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""
assert process(test_input.split('\n'), get_group_count, None) == 2
```

To use the same process function, we need to isolate the solution logic:

```python
def get_number_in_group(relations, id):
    sub_group = get_subgroup(relations, str(id), set())
    return len(sub_group)

def process(input, solution, param):
    relations, _ = generate_tree(input, parse_line)
    return solution(relations, param)
```

Let's design the algorithm to get the answer:
- We currently have a function that given a number, will return a set with all the node ids
in the same group
- We need to start with an arbitrary element, get the first group and exclude from the pool
any element present in that group

There are probably much better ways of doing this[*](#day12annotation1), but the quickest way of solving it was to
parse the whole list of keys on the dictionary and check whether they already exist in a list
of groups.
The code looks something like this:

```python
def get_group_count(relations, *args):
    groups = list()
    for key in relations.keys():
        visited = False
        for g in groups:
            visited += key in g
        if not visited:
            sub_group = set()
            sub_group = get_subgroup(relations, key, sub_group)
            groups.append(sub_group)
    return len(groups)
```

<a name="day12annotation1"></a>* I wasn't happy with this solution, ugly and inefficient, so
I decided to rewrite it into this: (**note**: you need to install `numpy` for this, you might
want to keep the other version)

```python
def get_group_count(relations, *args):
    groups = list()
    keys = list(relations)
    while len(keys) > 0:
        sub_group = get_subgroup(relations, keys[0], set())
        groups.append(sub_group)
        keys = np.setdiff1d(keys, list(sub_group))
    return len(groups)
```

This version makes use of `setdiff1d` which takes the elements from the first element that are
not in the second.

Let's now execute the given input:

```python
print(process(get_input(), get_group_count, None))  # returns 186
```

That's it for today's challenge. I am sure that there must be a better data structure to represent
the data, but I was quite happy that I could reuse some code!