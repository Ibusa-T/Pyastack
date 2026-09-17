#Pyastack
*Read this in [日本語](README_ja.md).*

## Introduction

*A lightweight, thread-safe stack library that allows you to transparently manipulate mutable objects and immutable objects with the same interface. *

## Main features

- **Transparent operation that does not make you aware of the type**: It is possible to add and remove with the API without being aware of the type

- **Thread-safe atomic operation**: `threading.RLock` prevents conflict (data destruction) even in multi-threaded environments

- **Low overhead memory optimization**: Weight reduction of attribute management with `__slots__` and high-speed batch operation using CPython native processing (`push_many`)

- **Stack overflow prevention (Capacity guard)**: Prevent unintended memory waste and overflow

- **Zero external dependence (Pure Python)**: Works only in standard libraries

## Project structure

```
Pyastack/

├── src/

│ └── pyastack/

│ ├── __init__.py # Package entry point (class exposure)

│ ├── stack.py # AtomicStack class body

│ └── py.typed # type hint compatible marker (empty file)

├── tests/

│ └── test_stack.py # Unit test (pytest)

│ └── data #test data

├──.gitignore

├── LICENSE # MIT License File

├── README.md # Document

└── pyproject.toml # Package build and meta information definition

```

# Main API

| Method / Syntactic | Explanation | Computation |

| :--- | :--- | :--- |

| `push(item)` | Add an element to the end of the stack. When the upper limit is exceeded, `OverflowError`. | $O(1)$ |

| `push_many(*items)` | Lock multiple elements once and add them in bulk with C-level processing. | $O(K)$ |

| `pop()` | Remove and delete the element at the end of the stack. Empty time is `IndexError`. | $O(1)$ |

| `peek()` | Confirm the last element (do not delete). Empty time is `IndexError`. | $O(1)$ |

| `clear()` | Empty the contents of the stack in place. | $O(1)$ |

| `is_empty()` | Determine whether the stack is empty. | $O(1)$ |

| `is_full()` | Determine whether the stack has reached the capacity limit. | $O(1)$ |

| `len(stack)` | Get the current number of stored elements. | $O(1)$ |

| `stack[i]` / `stack[a:b]]` | Inffix access and slice acquisition (`__getitem__`). | $O(1)$ / $O(K)$ |

| `item in stack` | Element existence determination (`__contains__`). | $O(N)$ |

| `for x in stack:` | Remove from the top of the stack to the bottom in order (LIFO inversion). | $O(N)$ |


# Quick start

```python

From pyastack import AtomicStack

# Initialize with a list (maximum capacity 10)

Stack = AtomicStack([1, 2, 3], capacity=10)

# Push elements (single / bulk)

Stack.push(4)

Stack.push_many(5,6)

Print(stack.peek()) # 6 (confirmation at the end)

Print(stack.pop()) # 6 (remove the end)

Print(len(stack)) # 5

Print(3 in stack) # True (confirmation of existence)

```

```python

From pyastack import AtomicStack

# Initialize with a string

Char_stack = AtomicStack("hello", capacity=10)

Char_stack.push("!")

Print(str(char_stack)) # "hello!"

# Remove 1 character from the end

Top_char=char_stack.pop()

Print(top_char) # "!"

Print(str(char_stack)) # "hello"

```

```python

Stack = AtomicStack([10, 20, 30, 40])

# Reference and slice of subtitles

Print(stack[-1]) # 40 (stack top)

Print(stack[0]) # 10 (stack bottom)

Print(stack[-2:]) # [30, 40]

# Iteration in stack order (LIFO: last in first out)

For item in stack:

Print(item)

# Output:

#40

#30

#20

#10

```

```python

Import threading

From pyastack import AtomicStack

Stack = AtomicStack([], capacity=1000)

Def worker():

For i in range(100):

Stack.push(i)

Threads = [threading.Thread(target=worker) for _ in range(10)]

For t in threads:

T.start()

For t in threads:

T.join()

Print(len(stack)) # Exactly 1000 without competition

```