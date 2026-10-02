# lesson05 ch02 演習: POST でボディを受け取る

コメント投稿 API を作ります。

- `author`(文字列)と `body`(文字列)を持つモデル `Comment` を定義する
- `POST /comments` で `Comment` を受け取り、`{"author": 投稿者名, "message": 本文}` の形の辞書を返す(キー名が `body` から `message` に変わる点に注意)

**期待出力**

```text
200
{'author': 'demo', 'message': 'いいね'}
405
```
