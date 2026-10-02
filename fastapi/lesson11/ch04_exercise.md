# lesson11 ch04 演習: def と async def の使い分け

def と async def のエンドポイントを 1 つずつ作ってください。

- `GET /double/{n}` を `def` で定義し、`{"result": n * 2}` を返す(`n` は int)
- `GET /triple/{n}` を `async def` で定義し、`{"result": n * 3}` を返す

**期待出力**

```text
200
{'result': 10}
200
{'result': 15}
```
