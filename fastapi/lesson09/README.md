# Lesson 09 エラー処理

存在しない ID へのアクセスなど、正常に処理できないリクエストに正しいステータスコードとメッセージを返すレッスンです。HTTPException を使った「見つからなければ 404」の定番パターンは、この後の総合演習でも何度も登場します。

## ch01 HTTPException で 404 を返す

**HTTPException** とは、エラーを HTTP レスポンスとして返すための FastAPI の例外クラスです。`raise HTTPException(status_code=404)` を実行すると、その場で関数の処理が止まって 404 レスポンスに変換されます。`return` の行までは進まないので、「エラーなら抜ける」を安全に書けます。TestClient は raise された HTTPException を HTTP レスポンスとして受け取るので、`r.status_code` で確認できます。🔴 「なければ raise で止める」の形を手が覚えるまで書きましょう。

```python
if item_id not in items:
    raise HTTPException(status_code=404)  # ここで処理が止まる
return {"name": items[item_id]}  # 見つかったときだけ実行される
```

### 基礎の基礎: 例外と raise

**例外** とは、「これ以上ふつうに処理を続けられない」ことを知らせる Python のしくみです。`int("abc")` を実行すると `ValueError` が出てプログラムが止まりますが、あれも例外です。

- **raise**(レイズ): 例外を自分で起こす命令です。`raise ValueError("だめ")` と書くと、その行で関数の処理が中断され、下の行は実行されません
- `return` との違い: `return` は「正常に値を返して終わる」、`raise` は「異常として中断する」です

ふつうの Python プログラムなら、raise された例外はエラー表示(Traceback)になって止まります。FastAPI の中では、関数から `HTTPException` が raise されると FastAPI がそれを受け止め、エラー表示の代わりに「指定したステータスコードのレスポンス」に作り替えてクライアントに返します。サーバ自体は止まらず、次のリクエストも受け付けます。

### 404 とは

L7 で見たステータスコードのうち、**404 Not Found** は「指定されたものが見つからない」を表します。ブラウザで存在しないページを開いたときの「404」と同じものです。4 で始まるコードは「リクエストした側(クライアント)の指定に問題がある」という意味のグループです。

### サンプルを1行ずつ

- `from fastapi import FastAPI, HTTPException`: `FastAPI` に加えて `HTTPException` も読み込みます。`,` で区切ると複数をまとめて import できます
- `items = {1: "りんご", 2: "みかん"}`: データの置き場所です。キーが ID(整数)、値が名前の辞書です
- `@app.get("/items/{item_id}")` と `def read_item(item_id: int):`: L3 で見たパスパラメータです。`/items/1` なら `item_id` に `1`(int)が入ります
- `if item_id not in items:`: `not in` は「辞書のキーに含まれていない」なら True になる演算子です。`99 not in items` は True、`1 not in items` は False です
- `raise HTTPException(status_code=404)`: 見つからないので 404 で中断します。下の `return` には進みません
- `return {"name": items[item_id]}`: 見つかったときだけここに来ます。`items[1]` は `"りんご"` です
- `r = client.get("/items/1")` → 存在する ID なので 200、`client.get("/items/99")` → 存在しない ID なので 404 になります

実行結果:

```text
200
{'name': 'りんご'}
404
{'detail': 'Not Found'}
```

detail を指定しないと、FastAPI が既定の `"Not Found"`(404 の正式な名前)を入れます。detail については次の ch02 で見ます。

### HTTP のレスポンスの実物

`GET /items/99` を送ったときに返ってくるレスポンスは次のとおりです。

```text
HTTP/1.1 404 Not Found
content-type: application/json
content-length: 22

{"detail":"Not Found"}
```

エラーのときもボディは JSON です。そのため、エラーのときでも `r.json()` で中身を取り出せます。

なお、`@app.get` に登録していないパス(たとえば `GET /nothing`)を送ったときも、FastAPI は自動で同じ `404` と `{"detail":"Not Found"}` を返します。今回の raise は「パスは合っているが、その ID のデータがない」場合に、自分で 404 を返すための書き方です。

### L8 の書き方との違い

L8 では、見つからないときに `return {"error": "not found"}` という辞書を返していました。この書き方だと、ボディは「見つからない」と言っているのにステータスコードは **200(成功)** のままです。呼ぶ側のプログラムはふつうステータスコードで成否を判断するので、「成功した」と誤解されてしまいます。`raise HTTPException(status_code=404)` なら、ステータスコード自体が 404 になるので、この食い違いが起きません。

## ch02 detail にエラー内容を入れる

HTTPException の **detail**(エラーレスポンスの本文に入れる説明)に、何が起きたかを書けます。渡した値は `{"detail": ...}` という JSON になって返り、API を呼ぶ側が原因を知る手がかりになります。f-string で ID を埋め込めば「どの ID がなかったか」まで伝えられます。既定の "Not Found" だけでは呼ぶ側が困るので、実務では必ず内容を入れます。🔴 detail 付きの raise を手が覚えるまで書きましょう。

```python
raise HTTPException(status_code=404, detail=f"item {item_id} は見つかりません")
```

レスポンスは `{"detail": "item 99 は見つかりません"}` になります。

### f-string のおさらい

`f"item {item_id} は見つかりません"` のように、文字列の前に `f` を付けると、`{}` の中に書いた変数の値が埋め込まれます。`item_id` が `99` なら、できあがる文字列は `"item 99 は見つかりません"` です。

### サンプルを1行ずつ

ch01 との違いは raise の行だけです。

- `raise HTTPException(status_code=404, detail=f"item {item_id} は見つかりません")`: ステータスコードに加えて `detail=` に説明文を渡します。`status_code=` や `detail=` のように「名前=値」で渡す書き方を **キーワード引数** と呼びます
- `client.get("/items/2")`: ID 2 はあるので 200 と `{'name': 'みかん'}`
- `client.get("/items/99")`: ID 99 はないので raise され、404 と detail 入りの JSON

実行結果:

```text
200
{'name': 'みかん'}
404
{'detail': 'item 99 は見つかりません'}
```

### HTTP のレスポンスの実物

`GET /items/99` に対するレスポンスです。

```text
HTTP/1.1 404 Not Found
content-type: application/json
content-length: 45

{"detail":"item 99 は見つかりません"}
```

- 1行目の `Not Found` は 404 の名前で、detail を変えても変わりません。変わるのはボディだけです
- `content-length: 45` は文字数ではなくバイト数です。日本語は1文字 3 バイトで数えるため、見た目の文字数より大きくなります
- ボディのキー名は必ず `"detail"` です。FastAPI が決めている形なので、呼ぶ側は「エラーのときは `detail` を見ればよい」と分かります

### detail に入れられるもの

detail には文字列のほか、辞書やリストも渡せます。たとえば `detail={"code": "x", "msg": "y"}` と書くと、ボディは `{"detail":{"code":"x","msg":"y"}}` になります。L6 で見た 422 のエラーのボディも、`{"detail": [...]}` のように detail の中にリストが入った形でした。この講座の演習では文字列だけを使います。

## ch03 「見つからなければ404」の定番パターン

「見つからなければ先に 404 を raise して抜け、その後は正常系だけを書く」のが FastAPI の定番パターンです(先に異常系で抜ける書き方を**ガード節**と呼びます)。else が不要になりネスト(if の中にさらに if を書くような、字下げの入れ子)が浅くなるうえ、GET・PUT・DELETE のどのエンドポイント(パスとメソッドの組ごとの受付窓口)でも冒頭に同じ 2 行を置くだけで済みます。総合演習でもこの形をそのまま使います。🔴 この 2 行 + 正常系の形を手が覚えるまで書きましょう。

```python
@app.get("/books/{book_id}")
def read_book(book_id: int):
    if book_id not in books:  # ガード節: 異常系で先に抜ける
        raise HTTPException(status_code=404, detail=f"book {book_id} は見つかりません")
    return books[book_id]     # ここからは正常系だけ
```

### 正常系と異常系

- **正常系**: 期待どおりに進む場合(ID のデータがあり、それを返す)
- **異常系**: 期待どおりに進まない場合(ID のデータがない)

### ガード節を使わない書き方との比較

同じ処理を if / else で書くと次のようになります。

```python
def read_book(book_id: int):
    if book_id in books:
        return books[book_id]
    else:
        raise HTTPException(status_code=404, detail=f"book {book_id} は見つかりません")
```

この長さなら大差ありませんが、正常系の処理が 10 行、20 行と増えると、すべてが if の中に字下げされて読みにくくなります。ガード節なら、正常系は字下げなしで上から順に書けます。

### サンプルを1行ずつ

- `books = {1: {...}, 2: {...}}`: 辞書の値がさらに辞書になっています。`books[1]` は `{"title": "Python入門", "price": 2500}`、`books[1]["price"]` は `2500` です
- `read_book`: ガード節 2 行のあと、`books[book_id]`(本の辞書まるごと)を返します
- `@app.get("/books/{book_id}/price")` の `read_price`: 別のエンドポイントですが、冒頭は同じガード節 2 行です。正常系では価格だけを `{"price": ...}` にして返します
- `for path in ["/books/1", "/books/2/price", "/books/9"]:`: 3 つのパスに順にリクエストを送り、それぞれのステータスコードと JSON を出します

実行結果:

```text
200
{'title': 'Python入門', 'price': 2500}
200
{'price': 2800}
404
{'detail': 'book 9 は見つかりません'}
```

3 つめの `/books/9` は `read_book` のガード節で止まり、`return books[book_id]` には進みません。もしガード節がなかったら `books[9]` で Python の `KeyError`(辞書にないキーを指定したときの例外)が起き、uvicorn で動かしている本物のサーバは **500 Internal Server Error**(サーバ側の不具合を表すコード)を返してしまいます(TestClient の場合は、500 を返す代わりに KeyError の Traceback がそのまま表示されて止まります)。ガード節は、この「サーバが壊れたように見える」状態を防ぐ役目も持っています。
