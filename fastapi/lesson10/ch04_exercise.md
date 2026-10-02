# lesson10 ch04 演習: 依存の中の依存（ネスト）と使いどころ

依存のネストを使って `GET /greet` を作ってください。

- 依存関数 `get_name` を定義し、文字列 `"demo"` を返す
- 依存関数 `get_message(name: str = Depends(get_name))` を定義し、f-string で `こんにちは、{name}さん` を返す
- `GET /greet` は `message: str = Depends(get_message)` で受け取り、`{"message": message}` を返す

**期待出力**

```text
200
{'message': 'こんにちは、demoさん'}
```
