from .astack import AtomicStack

# 1. 文字列スタックとしての利用
str_stack: AtomicStack[str] = AtomicStack("HelloWorld")

# 2. リストスタックとしての利用
int_stack: AtomicStack[int] = AtomicStack([1, 2, 3])

# 3. コンテキストマネージャで不可分（アトミック）に操作
with int_stack:
  a = int_stack.pop()
  b = int_stack.pop()
  int_stack.push(a + b)

print(int_stack.as_list())  # -> [1, 5]
