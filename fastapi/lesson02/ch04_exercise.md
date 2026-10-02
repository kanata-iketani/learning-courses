# lesson02 ch04 演習: レスポンスの中身を調べる

GET `/ping` で `{"ping": "pong"}` を返すエンドポイントを書いてください。動作確認部分は `/ping` のステータスコード・content-type ヘッダー・JSON を出力したあと、定義していない `/nothing` を呼んで 404 の様子も出力します。

**期待出力**

```text
200
application/json
{'ping': 'pong'}
404
{'detail': 'Not Found'}
```
