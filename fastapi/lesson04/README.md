# Lesson 04 クエリパラメータ

`?q=hello` のように URL の末尾に付ける「クエリパラメータ」を学ぶレッスンです。関数の引数を書くだけで受け取れ、デフォルト値・int 変換・`str | None` による省略可能な引数まで扱います。

## ch01 引数=クエリパラメータ

URL の `?` 以降に `?q=hello` の形で付ける値を **クエリパラメータ** と呼びます(複数あるときは `&` でつなぎます)。FastAPI では、関数の引数のうちパスに含まれない名前は、自動的にクエリパラメータとして扱われます。特別な宣言は不要で、引数を書くだけです。🔴 「パスにない引数 = クエリパラメータ」という対応を、手を動かして覚えましょう。

```python
@app.get("/search")
def search(q: str):
    return {"q": q}
```

呼び出す側は `client.get("/search?q=fastapi")` のように URL に付けて渡します。

## ch02 デフォルト値

引数にデフォルト値を書くと、そのクエリパラメータは省略可能になります。URL に付けなかったときはデフォルト値が使われ、付けたときはその値で上書きされます。デフォルト値のない引数は必須のままで、省略するとステータスコード 422 が返ります。🔴 「デフォルト値あり = 省略可能」のパターンは実際の API 開発でも頻出なので、繰り返し書いて覚えましょう。

```python
@app.get("/items")
def read_items(lang: str = "ja"):
    return {"lang": lang}
```

## ch03 int 型クエリと skip/limit パターン

クエリパラメータにも `skip: int = 0` のように型ヒントが使えます。URL 上では文字列の "2" でも、関数には int の 2 として渡ります。この型変換の代表的な使い道が **skip / limit パターン** です。skip は読み飛ばす件数、limit は取得する最大件数で、一覧データを少しずつ取り出すときの定番の書き方です。🔴 リストのスライス `items[skip : skip + limit]` と組み合わせる形を、手が覚えるまで書きましょう。

```python
@app.get("/items")
def read_items(skip: int = 0, limit: int = 2):
    return items[skip : skip + limit]
```

## ch04 bool と None

「値があってもなくてもよい」引数は `q: str | None = None` と書きます(`str | None` は「str か None のどちらか」を表す型ヒントです)。省略されると `None` になるため、`if q is None:` で「指定されなかった場合」を分岐できます。また `flag: bool = False` と書くと、URL の `?flag=true` や `?flag=1` が自動で Python の `True` に変換されます。🟡 None と bool の変換ルールを理解し、省略可能な引数を設計できるようになりましょう。

```python
@app.get("/search")
def search(q: str | None = None, sale: bool = False):
    return {"q": q, "sale": sale}
```
