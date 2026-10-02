# Lesson 12 総合演習：ミニCRUD API

lesson01〜11 で学んだことを総動員して、本を管理するミニ CRUD API を仕様書から組み立てる総合演習です。モデル定義・一覧/個別 GET・POST 201・PUT/DELETE の 404 対応までを通しで作ります。

## ch01 仕様の読み方と土台（Book モデル + GET）

総合演習では、本を管理するミニ CRUD API を仕様書から組み立てます。仕様書を読むときは「リソース(扱うデータのまとまり。今回は Book)→ データの置き場所(メモリ上の辞書)→ エンドポイント一覧」の順に整理すると迷いません。今回の仕様は、`id`・`title`・`price` を持つ Book モデルと、`GET /books`(一覧)・`GET /books/{book_id}`(個別、なければ 404)です。個別 GET には lesson09 のガード節をそのまま使います。🔴 モデル + 2 つの GET の土台を手が覚えるまで書きましょう。

```python
class Book(BaseModel):
    id: int
    title: str
    price: int

books = {1: Book(id=1, title="Python入門", price=2500)}
```

## ch02 追加と更新（POST 201 / PUT 404対応）

土台に追加(POST)と更新(PUT)を足します。追加の成功時は **201 Created**(リソース作成の成功を表すステータスコード)を返すのが REST の作法で、`@app.post("/books", status_code=201)` と宣言します。ボディは lesson05 で学んだとおり `book: Book` で受け取り、`books[book.id] = book` で保存します。更新の PUT は「対象がなければ 404」なので、冒頭にガード節を置いてから上書きします。🔴 POST 201 と PUT のガード節を手が覚えるまで書きましょう。

```python
@app.post("/books", status_code=201)
def create_book(book: Book):
    books[book.id] = book
    return book
```

## ch03 削除と仕上げ（DELETE + 通し確認）

最後は削除(DELETE)です。ここでも冒頭はガード節で、対象がなければ 404 を返します。あれば `del books[book_id]` で辞書から消し、確認用に `{"deleted": book_id}` を返します。仕上げとして POST → PUT → DELETE → GET を通しで呼び、「追加した本を更新・削除でき、削除後の GET は 404 になる」という一連の流れを確認します。これで CRUD の 4 操作がそろいます。🔴 DELETE のガード節 + del の形を手が覚えるまで書きましょう。

```python
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail=f"book {book_id} は見つかりません")
    del books[book_id]
    return {"deleted": book_id}
```
