# lesson03 ch03 演習: 複数のパスパラメータと順序

次の2つのエンドポイントを「正しい順序で」定義してください。

- GET `/users/me` : `{"user": "current"}` を返す(固定パス)
- GET `/users/{user_id}` : `user_id` を int で受け取り `{"user_id": user_id}` を返す(可変パス)

順序を間違えると `/users/me` が 422 になります。

**期待出力**

```text
{'user': 'current'}
{'user_id': 10}
```
