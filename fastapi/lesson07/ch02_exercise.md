# lesson07 ch02 演習: 見せたくない項目を隠す

アカウント登録 API からパスワードを隠します。

- 入力用モデル `AccountIn`(`email`: 文字列、`password`: 文字列)と、出力用モデル `AccountOut`(`email` のみ)を定義する
- `POST /accounts` で `AccountIn` を受け取り、`response_model=AccountOut` を指定して、受け取ったモデルをそのまま返す

**期待出力**

```text
200
{'email': 'demo@example.com'}
```
