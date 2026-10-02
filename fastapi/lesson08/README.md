# Lesson 08 CRUDを作る

これまでの知識を組み合わせて、CRUD(作成・取得・更新・削除)の API を一通り作るレッスンです。データベースの代わりにメモリ上のリストを使い、Web API の基本形を完成させます。

## ch01 一覧の GET

**CRUD** とは、Create(作成)・Read(取得)・Update(更新)・Delete(削除)というデータ操作の基本 4 種のことです。このレッスンでは、データベースの代わりにメモリ上のリストを使って CRUD API を一通り作ります。まずは Read の基本、一覧を返す GET です。関数からリストを返せば、そのまま JSON の配列になります。🔴 一覧 GET は CRUD の入口なので、手が覚えるまで書きましょう。

```python
@app.get("/books")
def list_books():
    return books  # リスト → JSON の配列
```

## ch02 個別の GET

一覧の次は、ID を指定して 1 件だけ取り出す Read です。パスパラメータで ID を受け取り、for 文でリストから探します。id が一致した辞書を return すれば、その時点で関数が終わります。最後まで見つからなければ、エラーを表す辞書を返しておきます(HTTPException を使った本格的なエラー処理は lesson09 で学びます)。🔴 「ID で探して返す」は CRUD の中心パターンなので、何度も書いて覚えましょう。

```python
@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    return {"error": "not found"}
```

## ch03 POST で追加

Create は、POST でボディを受け取り、新しい ID を付けてリストに追加します。手順は 3 つです。(1) `model_dump()` で辞書にする、(2) `len(books) + 1` で新しい ID を採番してキー `id` を足す、(3) `append` でリストに追加する。作成なのでステータスコードは 201 にします。🔴 この「追加の型」は CRUD の要なので、体に入れましょう。

```python
@app.post("/books", status_code=201)
def create_book(book: BookIn):
    new_book = book.model_dump()
    new_book["id"] = len(books) + 1
    books.append(new_book)
    return new_book
```

## ch04 PUT で更新

**PUT** とは、既存データの更新に使う HTTP メソッドです。パスパラメータの ID で対象を探し、ボディで受け取った新しい値で書き換えます。書き換えには、辞書のメソッド `update`(別の辞書の内容で上書きする)と `model_dump()` の組み合わせが便利です。見つからなければエラーの辞書を返します。🔴 「探して書き換えて返す」の型を、手が覚えるまで書きましょう。

```python
@app.put("/books/{book_id}")
def update_book(book_id: int, new: BookIn):
    for book in books:
        if book["id"] == book_id:
            book.update(new.model_dump())
            return book
    return {"error": "not found"}
```

## ch05 DELETE で削除

**DELETE** とは、データの削除に使う HTTP メソッドです。`enumerate`(番号付きで取り出す関数)で位置を調べながら探し、見つかったら `pop(位置)` でリストから取り除きます。成功したら 204(No Content)を返し、ボディは返しません。これで Create・Read・Update・Delete の 4 操作がそろい、CRUD API の完成です。🔴 CRUD の締めくくりとして、削除も手が覚えるまで書きましょう。

```python
@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    for i, book in enumerate(books):
        if book["id"] == book_id:
            books.pop(i)
            return
```
