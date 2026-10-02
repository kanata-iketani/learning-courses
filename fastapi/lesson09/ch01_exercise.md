# lesson09 ch01 演習: HTTPException で 404 を返す

ユーザー辞書 `users = {1: "佐藤", 2: "鈴木"}` を持つ API に、`GET /users/{user_id}` を作ってください。

- `user_id` が `users` になければ `HTTPException(status_code=404)` を raise する
- あれば `{"name": ユーザー名}` を返す

**期待出力**

```text
200
{'name': '鈴木'}
404
{'detail': 'Not Found'}
```
