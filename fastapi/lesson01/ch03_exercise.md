# lesson01 ch03 演習: この講座の学び方

「アプリ定義 → TestClient → print」の定型を、今回はすべて自分の手で書きます。

1. GET `/` で `{"status": "ok"}` を返すアプリを定義する
2. TestClient を作る
3. GET `/` を呼び出し、`r.status_code` と `r.json()` を順に出力する

**期待出力**

```text
200
{'status': 'ok'}
```
