# lesson09 ch02 演習: detail にエラー内容を入れる

`users = {1: "佐藤", 2: "鈴木"}` を持つ API に `GET /users/{user_id}` を作ってください。

- `user_id` がなければ 404 を raise し、detail に `user {user_id} は存在しません` を入れる(f-string を使う)
- あれば `{"name": ユーザー名}` を返す

**期待出力**

```text
200
{'name': '佐藤'}
404
{'detail': 'user 7 は存在しません'}
```
