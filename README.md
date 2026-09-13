# Pyastack










*プロジェクト構成*
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