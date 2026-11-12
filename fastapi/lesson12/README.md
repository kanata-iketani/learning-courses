# Lesson 12 総合演習：ミニCRUD API

lesson01〜11 で学んだことを総動員して、本を管理するミニ CRUD API を仕様書から組み立てる総合演習です。モデル定義・一覧/個別 GET・POST 201・PUT/DELETE の 404 対応までを通しで作ります。

## ch01 仕様の読み方と土台（Book モデル + GET）

総合演習では、本を管理するミニ CRUD API(L8 で見た作成・取得・更新・削除の 4 操作をそろえた API)を仕様書から組み立てます。仕様書を読むときは「リソース(扱うデータのまとまり。今回は Book)→ データの置き場所(メモリ上の辞書)→ エンドポイント一覧」の順に整理すると迷いません。今回の仕様は、`id`・`title`・`price` を持つ Book モデルと、`GET /books`(一覧)・`GET /books/{book_id}`(個別、なければ 404)です。個別 GET には lesson09 のガード節をそのまま使います。🔴 モデル + 2 つの GET の土台を手が覚えるまで書きましょう。

```python
class Book(BaseModel):
    id: int
    title: str
    price: int

books = {1: Book(id=1, title="Python入門", price=2500)}
```

### 仕様書の読み方

ch01〜ch03 で作る API の全体の仕様は次の表です。実務でも、API の仕様はこのような「メソッド・パス・成功時・失敗時」の一覧で渡されることがよくあります。

| メソッド | パス | すること | 成功時 | 見つからないとき | 作る章 |
|---|---|---|---|---|---|
| GET | `/books` | 全件を返す | 200 + Book の配列 | - | ch01 |
| GET | `/books/{book_id}` | 1 件を返す | 200 + Book | 404 | ch01 |
| POST | `/books` | 1 件追加する | 201 + 追加した Book | - | ch02 |
| PUT | `/books/{book_id}` | 1 件を上書きする | 200 + 更新後の Book | 404 | ch02 |
| DELETE | `/books/{book_id}` | 1 件削除する | 200 + `{"deleted": id}` | 404 | ch03 |

読むときは、表の各行を次の 3 点に分けて確認します。

1. **どのデコレータか**: メソッドとパスから `@app.get("/books/{book_id}")` のように決まります。パスに `{...}` があれば、L3 で見たパスパラメータを関数の引数で受け取ります
2. **何を受け取り、何を返すか**: 「Book の配列」なら Book のリスト、「Book」なら Book 1 つを return します
3. **失敗時の扱い**: 「見つからないとき 404」とあれば、関数の冒頭に L9 のガード節を書きます

### データの置き場所

`books` は「キーが id、値が Book」の辞書です。L8 ではリストに入れて for 文で探しましたが、辞書なら `books[2]` で直接取り出せ、`2 in books` で「あるかどうか」も1行で調べられます。L8 で見たとおり、これは **インメモリ**(プログラムが動いている間だけメモリ上に置く)のデータなので、プログラムを終了すると追加や変更は消えます。

| キー | 値 |
|---|---|
| `1` | `Book(id=1, title="Python入門", price=2500)` |
| `2` | `Book(id=2, title="FastAPI入門", price=2800)` |

### サンプルを1行ずつ

- `from pydantic import BaseModel` と `class Book(BaseModel):`: L5 で見た Pydantic のモデルです。`id`・`title`・`price` の 3 項目を型付きで持ちます
- `books = {1: Book(id=1, ...), 2: Book(id=2, ...)}`: Book のインスタンスを作って辞書に入れます
- `list_books` の `return list(books.values())`: `books.values()` で値(Book)だけを取り出し、`list()` でリストにして返します。FastAPI は Book を L5 の `model_dump()` と同じように辞書に直し、全体を JSON の配列にします
- `read_book`: ガード節で 404 を先に返し、あれば `books[book_id]`(Book 1 つ)を返します
- `for path in ["/books", "/books/1", "/books/99"]:`: 一覧・存在する ID・存在しない ID の 3 通りを確かめます

実行結果:

```text
200
[{'id': 1, 'title': 'Python入門', 'price': 2500}, {'id': 2, 'title': 'FastAPI入門', 'price': 2800}]
200
{'id': 1, 'title': 'Python入門', 'price': 2500}
404
{'detail': 'book 99 は見つかりません'}
```

`GET /books` のレスポンスの実物です。ボディが `[` で始まる JSON の配列になっています。

```text
HTTP/1.1 200 OK
content-type: application/json

[{"id":1,"title":"Python入門","price":2500},{"id":2,"title":"FastAPI入門","price":2800}]
```

### 確かめ方

1 つのエンドポイントを書いたら、すぐに次の 3 通りを呼んで確かめるのがコツです。

| 呼び方 | 期待するステータス | 確かめること |
|---|---|---|
| 一覧 `GET /books` | 200 | 全件が配列で返るか |
| 存在する ID | 200 | その 1 件だけが返るか |
| 存在しない ID | 404 | detail の文言が仕様どおりか(空白 1 つの違いも採点では不一致) |

演習の動作確認ブロックも、この 3 通りを順に呼ぶ作りになっています。

## ch02 追加と更新（POST 201 / PUT 404対応）

土台に追加(POST)と更新(PUT)を足します。追加の成功時は **201 Created**(リソース作成の成功を表すステータスコード。L7 で見たもの)を返すのが REST(HTTP のメソッドとパスでデータを操作する API の設計の考え方)の作法で、`@app.post("/books", status_code=201)` と宣言します。ボディは lesson05 で学んだとおり `book: Book` で受け取り、`books[book.id] = book` で保存します。更新の PUT は「対象がなければ 404」なので、冒頭にガード節を置いてから上書きします。🔴 POST 201 と PUT のガード節を手が覚えるまで書きましょう。

```python
@app.post("/books", status_code=201)
def create_book(book: Book):
    books[book.id] = book
    return book
```

### POST のリクエストとレスポンスの実物

`client.post("/books", json={...})` の `json=` に渡した辞書は、JSON 文字列になってリクエストのボディに入ります。実際に送られるリクエストは次のとおりです。

```text
POST /books HTTP/1.1
host: testserver
content-type: application/json
content-length: 44

{"id":3,"title":"Docker入門","price":3200}
```

GET と違い、ヘッダのあとの空行に続けてボディ(送るデータ)があります。`content-type: application/json` は「ボディは JSON です」という目印です。FastAPI はこのボディを読み、引数 `book: Book` の型に合わせて Book のインスタンスに変換してから関数を呼びます。返ってくるレスポンスは次のとおりです。

```text
HTTP/1.1 201 Created
content-type: application/json
content-length: 44

{"id":3,"title":"Docker入門","price":3200}
```

ボディに `price` がないなど Book の形に合わないときは、関数が呼ばれる前に L6 で見た 422 が返ります(`{"detail":[{"type":"missing","loc":["body","price"],"msg":"Field required",...}]}`)。

### サンプルを1行ずつ

- `@app.post("/books", status_code=201)`: POST `/books` を担当し、成功時のステータスコードを 201 にします。何も指定しないと 200 になります
- `def create_book(book: Book):`: 引数の型が Pydantic のモデルなので、FastAPI はこれを「リクエストのボディ」として受け取ります(L5)
- `books[book.id] = book`: 辞書にキー `book.id` で保存します。そのキーがまだなければ追加、すでにあれば上書きになります
- `return book`: 保存した Book を返します。呼ぶ側は、保存された内容をレスポンスで確認できます
- `@app.put("/books/{book_id}")` と `def update_book(book_id: int, book: Book):`: パスパラメータ `book_id`(どれを更新するか)とボディ `book`(新しい内容)の 2 つを受け取ります。FastAPI は、パスに `{book_id}` がある引数はパスから、モデル型の引数はボディから取ります
- `if book_id not in books: raise ...`: 更新する対象がなければ 404 で止めます
- `books[book_id] = book`: 古い Book を新しい Book に丸ごと置き換えます。PUT は「全項目を送って丸ごと置き換える」のが基本の使い方なので、変えない `title` もボディに入れて送ります

実行結果:

```text
201
{'id': 3, 'title': 'Web入門', 'price': 2200}
200
{'id': 1, 'title': 'Python入門', 'price': 1980}
404
{'detail': 'book 99 は見つかりません'}
```

1 回目は追加なので 201、2 回目は更新なので 200(PUT には status_code を指定していないので既定の 200)、3 回目は ID 99 がないので 404 です。

### この仕様の注意点

- POST に、すでにある id(たとえば `1`)を送ると、この仕様では `books[1] = book` で既存の本が上書きされ、201 が返ります。本来は「すでにあるならエラーにする」ことも多いですが、今回の仕様書には書かれていないので、仕様どおりそのまま保存します
- PUT では、パスの `book_id` とボディの `id` が同じ値であることを前提にしています。演習の動作確認でも両方を同じ値で送っています

### 確かめ方

演習の動作確認は「POST(201)→ 追加した本を GET(200)→ 既存の本を PUT(200)→ ない本を PUT(404)」の順です。POST のあとに GET で読み直しているのは、「レスポンスが返っただけでなく、本当に `books` に保存されたか」を確かめるためです。

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

### del とは

`del 辞書[キー]` は、辞書からそのキーと値の組を取り除く Python の文です。

```python
d = {1: "a", 2: "b"}
del d[1]
print(d)  # {2: 'b'}
```

ないキーを `del` すると `KeyError` になります。先にガード節で「ある」ことを確かめているので、ここでは起きません。

### L8 の DELETE との違い

L8 では削除の成功時に 204(No Content。ボディなし)を返しました。今回の仕様書は「200 + `{"deleted": id}`」なので、`status_code` は指定せず(既定の 200)、何を消したかが分かる辞書を返します。どちらも使われる書き方で、どちらにするかは仕様書で決まります。仕様書の「成功時」の欄をよく読んで合わせましょう。

### サンプルを1行ずつ

- `@app.delete("/books/{book_id}")`: DELETE メソッドで `/books/{book_id}` を担当します
- ガード節 2 行: 対象がなければ 404 で止めます
- `del books[book_id]`: 辞書から削除します
- `return {"deleted": book_id}`: 消した ID を返します
- `read_book`: 削除できたかを確かめるために、個別 GET も用意しています
- `client.delete("/books/1")`: ID 1 を削除 → 200 と `{'deleted': 1}`
- `client.get("/books/1")`: 消したので、今度はガード節に引っかかって 404
- `client.delete("/books/99")`: もともとないので 404

実行結果:

```text
200
{'deleted': 1}
404
{'detail': 'book 1 は見つかりません'}
404
{'detail': 'book 99 は見つかりません'}
```

`DELETE /books/3` のリクエストとレスポンスの実物です。DELETE はふつうボディを送らず、パスだけでどれを消すかを伝えます。

```text
DELETE /books/3 HTTP/1.1
host: testserver
```

```text
HTTP/1.1 200 OK
content-type: application/json
content-length: 13

{"deleted":3}
```

### 通し確認の読み方

演習の動作確認では `print(r.status_code, r.json())` のように、ステータスコードと JSON を 1 行に並べて出します(print に `,` で複数の値を渡すと、空白で区切って 1 行に出ます)。各行で `books` の中身がどう変わるかを追うと、次のようになります。

| 順 | リクエスト | 結果 | その後の `books` のキー |
|---|---|---|---|
| 1 | POST(id 3, 3200円) | 201 | 1, 2, 3 |
| 2 | PUT /books/3(2980円) | 200 | 1, 2, 3(3 の値段が変わる) |
| 3 | DELETE /books/3 | 200 | 1, 2 |
| 4 | GET /books/3 | 404 | 1, 2 |
| 5 | DELETE /books/9 | 404 | 1, 2 |
| 6 | GET /books | 200 | 1, 2(最初の 2 冊に戻っている) |

`books` はプログラムの最初から最後まで同じ辞書なので、前のリクエストでの変更が次のリクエストに引き継がれます。最後の一覧が最初と同じ 2 冊になっていれば、追加・更新・削除がすべて正しく動いたことになります。
