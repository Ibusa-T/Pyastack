"""AtomicStack: A thread-safe, generic, atomic stack implementation."""

from .astack import AtomicStack

__version__ = "0.1.0"
__all__ = ["AtomicStack"]

def main() -> None:
    print("Hello from pyastack!")


if __name__ == '__main__':
    main()