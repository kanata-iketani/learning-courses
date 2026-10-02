# lesson01 ch02 演習: FastAPIと自動ドキュメント

GET `/` で辞書 `{"framework": "FastAPI"}` を返すアプリを作ってください。`app = FastAPI()` でアプリを作り、`@app.get("/")` を付けた関数で辞書を返します。動作確認部分が、ステータスコードとレスポンスの JSON を出力します。

**期待出力**

```text
200
{'framework': 'FastAPI'}
```
