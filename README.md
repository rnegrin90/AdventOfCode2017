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

## Day 3

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