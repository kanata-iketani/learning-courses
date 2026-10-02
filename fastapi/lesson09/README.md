# Lesson 09 エラー処理

存在しない ID へのアクセスなど、正常に処理できないリクエストに正しいステータスコードとメッセージを返すレッスンです。HTTPException を使った「見つからなければ 404」の定番パターンは、この後の総合演習でも何度も登場します。

## ch01 HTTPException で 404 を返す

**HTTPException** とは、エラーを HTTP レスポンスとして返すための FastAPI の例外クラスです。`raise HTTPException(status_code=404)` を実行すると、その場で関数の処理が止まって 404 レスポンスに変換されます。`return` の行までは進まないので、「エラーなら抜ける」を安全に書けます。TestClient は raise された HTTPException を HTTP レスポンスとして受け取るので、`r.status_code` で確認できます。🔴 「なければ raise で止める」の形を手が覚えるまで書きましょう。

```python
if item_id not in items:
    raise HTTPException(status_code=404)  # ここで処理が止まる
return {"name": items[item_id]}  # 見つかったときだけ実行される
```

## ch02 detail にエラー内容を入れる

HTTPException の **detail**(エラーレスポンスの本文に入れる説明)に、何が起きたかを書けます。渡した値は `{"detail": ...}` という JSON になって返り、API を呼ぶ側が原因を知る手がかりになります。f-string で ID を埋め込めば「どの ID がなかったか」まで伝えられます。既定の "Not Found" だけでは呼ぶ側が困るので、実務では必ず内容を入れます。🔴 detail 付きの raise を手が覚えるまで書きましょう。

```python
raise HTTPException(status_code=404, detail=f"item {item_id} は見つかりません")
```

レスポンスは `{"detail": "item 99 は見つかりません"}` になります。

## ch03 「見つからなければ404」の定番パターン

「見つからなければ先に 404 を raise して抜け、その後は正常系だけを書く」のが FastAPI の定番パターンです(先に異常系で抜ける書き方を**ガード節**と呼びます)。else が不要になりネストが浅くなるうえ、GET・PUT・DELETE のどのエンドポイントでも冒頭に同じ 2 行を置くだけで済みます。総合演習でもこの形をそのまま使います。🔴 この 2 行 + 正常系の形を手が覚えるまで書きましょう。

```python
@app.get("/books/{book_id}")
def read_book(book_id: int):
    if book_id not in books:  # ガード節: 異常系で先に抜ける
        raise HTTPException(status_code=404, detail=f"book {book_id} は見つかりません")
    return books[book_id]     # ここからは正常系だけ
```
