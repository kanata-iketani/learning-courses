# lesson07 ch04 演習: ステータスコードの使い分け

4 種類のステータスコードを返す API を作ります。

- `GET /ping`: `{"message": "pong"}` を返す(既定の 200)
- `POST /notes`: `{"created": True}` を返す。`status_code=201` を指定する
- `DELETE /notes/1`: `status_code=204` を指定し、`return None` にする

動作確認では上の 3 つに加えて、存在しない URL `/nothing` にもアクセスします(404 になります)。

**期待出力**

```text
200
201
204
404
```
