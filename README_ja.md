# Pyastack

[![PyPI version](https://img.shields.io/pypi/v/pyastack.svg)](https://pypi.org/project/pyastack/)
[![Python versions](https://img.shields.io/pypi/pyversions/pyastack.svg)](https://pypi.org/project/pyastack/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Concurrency: Thread-Safe](https://img.shields.io/badge/concurrency-thread--safe-brightgreen.svg)](https://pypi.org/project/pyastack/)

*[English](README.md) で読む*

## 紹介
*ミュータブルオブジェクトとイミュータブルオブジェクトを同一のインターフェースで透過的に操作できる、軽量・スレッドセーフなスタックライブラリ。*

## 主な特徴
- **型を意識させない透過的な操作感**: 型を意識せずに API で追加・取り出しが可能
- **スレッドセーフなアトミック操作**: `threading.RLock` により、マルチスレッド環境でも競合（データ破壊）を防止
- **低オーバーヘッド・メモリ最適化**: `__slots__` による属性管理の軽量化と、CPython ネイティブ処理を活用した高速な一括操作（`push_many`）
- **スタックあふれ防止（Capacity ガード）**: 意図しないメモリ浪費やオーバーフローを未然に防止
- **外部依存ゼロ（Pure Python）**: 標準ライブラリのみで動作



## プロジェクト構成
```
Pyastack/
├── src/
│   └── pyastack/
│       ├── __init__.py      # パッケージのエントリポイント (クラス露出)
│       ├── stack.py         # AtomicStack クラス本体
│       └── py.typed         # 型ヒント対応マーカー (空ファイル)
├── tests/
│   └── test_stack.py        # ユニットテスト (pytest)
│   └── data                 #テストデータ
├── .gitignore
├── LICENSE                  # MIT ライセンスファイル
├── README.md                # ドキュメント
└── pyproject.toml           # パッケージのビルド・メタ情報定義

```


# 主要なAPI

| メソッド / 構文 | 説明 | 計算量 |
| :--- | :--- | :--- |
| `push(item)` | スタックの末尾に要素を追加。上限超過時は `OverflowError`。 | $O(1)$ |
| `push_many(*items)` | 複数の要素をロック1回・Cレベル処理で一括追加。 | $O(K)$ |
| `pop()` | スタック末尾の要素を取り出して削除。空時は `IndexError`。 | $O(1)$ |
| `peek()` | 末尾の要素を確認（削除しない）。空時は `IndexError`。 | $O(1)$ |
| `clear()` | スタックの中身をインプレースで空にする。 | $O(1)$ |
| `is_empty()` | スタックが空かどうかを判定。 | $O(1)$ |
| `is_full()` | スタックが容量上限に達しているかを判定。 | $O(1)$ |
| `len(stack)` | 現在の格納要素数を取得。 | $O(1)$ |
| `stack[i]` / `stack[a:b]` | 添字アクセスおよびスライス取得（`__getitem__`）。 | $O(1)$ / $O(K)$ |
| `item in stack` | 要素の存在判定（`__contains__`）。 | $O(N)$ |
| `for x in stack:` | スタックトップからボトムへ順に取り出し（LIFO反転）。 | $O(N)$ |




# クイックスタート
`インストール`
*pip*
```
 pip install pyastack
```
*uv*
```
 uv add  pyastack
```

`最新版に更新`
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

# リストで初期化（上限容量 10）
stack = AtomicStack([1, 2, 3], capacity=10)

# 要素をプッシュ（単一 / 一括）
stack.push(4)
stack.push_many(5, 6)

print(stack.peek())      # 6 (末尾の確認)
print(stack.pop())       # 6 (末尾の取り出し)
print(len(stack))        # 5
print(3 in stack)        # True (存在確認)

```


```python
from pyastack import AtomicStack

# 文字列で初期化
char_stack = AtomicStack("hello", capacity=10)

char_stack.push("!")
print(str(char_stack))   # "hello!"

# 末尾から1文字取り出し
top_char = char_stack.pop()
print(top_char)          # "!"
print(str(char_stack))   # "hello"

```

```python
stack = AtomicStack([10, 20, 30, 40])

# 添字参照とスライス
print(stack[-1])         # 40 (スタックトップ)
print(stack[0])          # 10 (スタックボトム)
print(stack[-2:])        # [30, 40]

# スタック順（LIFO: 後入れ先出し）でのイテレーション
for item in stack:
    print(item)
# 出力:
# 40
# 30
# 20
# 10
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

print(len(stack))  # 競合なく正確に 1000
```