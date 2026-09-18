# Pyastack

[![PyPI version](https://img.shields.io/pypi/v/pyastack.svg)](https://pypi.org/project/pyastack/)
[![Python versions](https://img.shields.io/pypi/pyversions/pyastack.svg)](https://pypi.org/project/pyastack/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Concurrency: Thread-Safe](https://img.shields.io/badge/concurrency-thread--safe-brightgreen.svg)](https://pypi.org/project/pyastack/)

*Read this in [日本語](./README.ja.md).*


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

install 
*pip*
```
 pip install pyastack
```
*uv*
```
 uv add  pyastack
```

upgrade 

*pip*
```
pip install --upgrade pyastack
```

*uv*
```
uv add --upgrade pyastack
```


```python
from pyastack import AtomicStack
if __name__ == '__main__':
    # Initialize with a list (maximum capacity 10)
    stack = AtomicStack([1, 2, 3], capacity=10)
    # Push elements (single / bulk)

    stack.push(4)

    stack.push_many(5,6)

    print(stack.peek()) # 6 (confirmation at the end)

    print(stack.pop()) # 6 (remove the end)

    print(len(stack)) # 5

    print(3 in stack) # True (confirmation of existence)

```

```python
from pyastack import AtomicStack
if __name__ == '__main__':
    # Initialize with a string

    char_stack = AtomicStack("hello", capacity=10)

    char_stack.push("!")

    print(str(char_stack)) # "hello!"

    # Remove 1 character from the end

    top_char=char_stack.pop()

    print(top_char) # "!"

    print(str(char_stack)) # "hello"

```

```python
from pyastack import AtomicStack
if __name__ == '__main__':
    stack = AtomicStack([10, 20, 30, 40])

    # Reference and slice of subtitles

    print(stack[-1]) # 40 (stack top)

    print(stack[0]) # 10 (stack bottom)

    print(stack[-2:]) # [30, 40]

    # Iteration in stack order (LIFO: last in first out)

    for item in stack:
        print(item)

    # Output:

    #40

    #30

    #20

    #10

```

```python

import threading

from pyastack import AtomicStack

stack = AtomicStack([], capacity=1000)

def worker():
    for i in range(100):
        stack.push(i)
    
    threads = [threading.Thread(target=worker) for _ in range(10)]
    
for t in threads:
    t.start()
for t in threads:
    t.join()

print(len(stack)) # Exactly 1000 without competition

```