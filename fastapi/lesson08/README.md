# Lesson 08 CRUDを作る

これまでの知識を組み合わせて、CRUD(作成・取得・更新・削除)の API を一通り作るレッスンです。データベースの代わりにメモリ上のリストを使い、Web API の基本形を完成させます。

## ch01 一覧の GET

**CRUD**(クラッド)とは、Create(作成)・Read(取得)・Update(更新)・Delete(削除)というデータ操作の基本 4 種のことです。このレッスンでは、データベースの代わりにメモリ上のリストを使って CRUD API を一通り作ります。まずは Read の基本、一覧を返す GET です。関数からリストを返せば、そのまま JSON の配列になります。🔴 一覧 GET は CRUD の入口なので、手が覚えるまで書きましょう。

```python
@app.get("/books")
def list_books():
    return books  # リスト → JSON の配列
```

### CRUD と HTTP メソッドの対応

このレッスンの5つのチャプターで、次の表を順に作ります。

| 操作 | HTTP メソッド | パスの例 | 成功時のコード | チャプター |
|---|---|---|---|---|
| Read(一覧) | GET | `/books` | 200 | ch01 |
| Read(1件) | GET | `/books/2` | 200 | ch02 |
| Create | POST | `/books` | 201 | ch03 |
| Update | PUT | `/books/1` | 200 | ch04 |
| Delete | DELETE | `/books/1` | 204 | ch05 |

同じ `/books` でも、メソッドが GET なら一覧、POST なら追加、と別の関数が呼ばれます。

### データベースの代わりのリスト

**データベース**(DB)は、データを保存しておき、プログラムを止めても消えないようにする専用のソフトウェアです。この講座では DB を使わず、ふつうの Python のリスト `books` にデータを入れておきます。これを **インメモリ**(プログラムが動いている間だけメモリ上に置く)のデータと呼びます。

- 良い点: 準備なしで CRUD の流れだけに集中できる
- 注意点: プログラムが終わると消える。この学習画面では「▶ 実行」のたびに、コードに書いた初期状態から始まる

### サンプルを1行ずつ

- `books = [ {...}, {...} ]`: 本のデータを辞書で表し、2冊分をリストにまとめます。各辞書の `id` は1冊ずつを区別する番号です
- `@app.get("/books")` → `return books`: リストをそのまま返します。L2 で見たとおり、辞書のリストはそのまま JSON の配列になります

実行結果:

```text
200
[{'id': 1, 'title': 'Python入門', 'price': 2000}, {'id': 2, 'title': 'FastAPI入門', 'price': 2500}]
```

### やり取りの実物

```text
GET /books HTTP/1.1
host: testserver
```

```text
HTTP/1.1 200 OK
content-length: 92
content-type: application/json

[{"id":1,"title":"Python入門","price":2000},{"id":2,"title":"FastAPI入門","price":2500}]
```

ボディが `[` で始まっているので、JSON の配列(Python のリストに当たるもの)だと分かります。

## ch02 個別の GET

一覧の次は、ID を指定して 1 件だけ取り出す Read です。パスパラメータ(L3)で ID を受け取り、for 文でリストから探します。id が一致した辞書を return すれば、その時点で関数が終わります。最後まで見つからなければ、エラーを表す辞書を返しておきます(HTTPException を使った本格的なエラー処理は lesson09 で学びます)。🔴 「ID で探して返す」は CRUD の中心パターンなので、何度も書いて覚えましょう。

```python
@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    return {"error": "not found"}
```

### 探す処理の動き

`/books/2` を呼んだときの流れです。

| 回 | `book["id"]` | `book_id` | 一致? | 動き |
|---|---|---|---|---|
| 1 | 1 | 2 | いいえ | 次の本へ |
| 2 | 2 | 2 | はい | `return book` で関数終了 |

`/books/99` なら、2冊とも一致しないまま for 文が終わり、最後の行 `return {"error": "not found"}` に進みます。

`book_id: int` と型ヒントを付けているのが大事な点です。URL の `2` はもともと文字列 `"2"` なので、型ヒントがないと `1 == "2"` のように int と str を比べることになり、いつまでも一致しません(L3 で見た自動変換のおかげで int になります)。

### サンプルを1行ずつ

- `@app.get("/books/{book_id}")`: パスの `{book_id}` を引数で受け取ります
- `for book in books:`: リストから1冊ずつ取り出して `book` に入れます
- `if book["id"] == book_id:`: その本の `id` と、URL で指定された ID を比べます
- `return book`: 見つかった本の辞書を返します
- `return {"error": "not found"}`: for 文を最後まで回っても見つからなかったときだけ、ここに来ます
- `print(client.get("/books/2").json())`: 送ってすぐ JSON を取り出して print します

実行結果:

```text
{'id': 2, 'title': 'FastAPI入門', 'price': 2500}
{'error': 'not found'}
```

### やり取りの実物

見つからなかった方のやり取りです。

```text
GET /books/99 HTTP/1.1
host: testserver
```

```text
HTTP/1.1 200 OK
content-length: 21
content-type: application/json

{"error":"not found"}
```

見つからなかったのにステータスコードが `200 OK`(成功)になっている点に注目してください。受け取った側はステータスコードだけでは失敗に気づけません。L7 で見たとおり「見つからない」は本来 404 です。これを正しく 404 にする方法を L9 で学びます。

## ch03 POST で追加

Create は、POST(L5)でボディを受け取り、新しい ID を付けてリストに追加します。手順は 3 つです。(1) `model_dump()`(L5 で見た、モデルを辞書にするメソッド)で辞書にする、(2) `len(books) + 1` で新しい ID を **採番**(重ならない番号を決めること)してキー `id` を足す、(3) `append` でリストに追加する。作成なのでステータスコードは 201(L7)にします。🔴 この「追加の型」は CRUD の要なので、体に入れましょう。

```python
@app.post("/books", status_code=201)
def create_book(book: BookIn):
    new_book = book.model_dump()
    new_book["id"] = len(books) + 1
    books.append(new_book)
    return new_book
```

### なぜ入力モデルに id がないのか

ID はサーバが決めるものです。送る側に決めさせると、すでにある番号と重なるおそれがあります。そこで入力用モデル `BookIn` には `title` と `price` だけを持たせ、`id` は関数の中で付けます(L7 で見た「入力用と出力用を分ける」考え方と同じです)。

`len(books) + 1` は「今の件数 + 1」です。2冊あれば 3 になります。削除がない間はこれで重なりませんが、途中の本を削除すると件数が減って番号が重なることがあります。実際のシステムでは DB が自動で重ならない番号を振ります。この講座では学習用に簡単な書き方を使っています。

### サンプルを1行ずつ

- `class BookIn(BaseModel): title: str / price: int`: 受け取るボディの形。`id` は含めません
- `@app.post("/books", status_code=201)`: POST `/books` を登録。成功時は 201
- `new_book = book.model_dump()`: `{'title': 'Web API設計', 'price': 3000}` という辞書になります
- `new_book["id"] = len(books) + 1`: 今2冊なので `id` は 3。辞書の最後に追加されます
- `books.append(new_book)`: リストの末尾に追加します。これでリスト `books` 自体が3冊になります
- `return new_book`: 追加した本を返します(付けた `id` を送った側に知らせるため)
- `print(books)`: API の外から、リストに本当に追加されたかを確かめています

実行結果:

```text
201
{'title': 'Web API設計', 'price': 3000, 'id': 3}
[{'id': 1, 'title': 'Python入門', 'price': 2000}, {'id': 2, 'title': 'FastAPI入門', 'price': 2500}, {'title': 'Web API設計', 'price': 3000, 'id': 3}]
```

3冊目だけ `id` が最後にあるのは、`model_dump()` で作った辞書にあとから `id` を足したためです。キーの順番が違っても、辞書としての意味は同じです。

### やり取りの実物

```text
POST /books HTTP/1.1
host: testserver
content-length: 38
content-type: application/json

{"title":"Web API設計","price":3000}
```

```text
HTTP/1.1 201 Created
content-length: 45
content-type: application/json

{"title":"Web API設計","price":3000,"id":3}
```

## ch04 PUT で更新

**PUT**(プット)とは、既存データの更新に使う HTTP メソッドです。FastAPI では `@app.put(...)`、TestClient では `client.put(URL, json=辞書)` と書きます(書き方は POST と同じ形です)。パスパラメータの ID で対象を探し、ボディで受け取った新しい値で書き換えます。書き換えには、辞書のメソッド `update`(別の辞書の内容で上書きする)と `model_dump()` の組み合わせが便利です。見つからなければエラーの辞書を返します。🔴 「探して書き換えて返す」の型を、手が覚えるまで書きましょう。

```python
@app.put("/books/{book_id}")
def update_book(book_id: int, new: BookIn):
    for book in books:
        if book["id"] == book_id:
            book.update(new.model_dump())
            return book
    return {"error": "not found"}
```

### パスとボディを同時に受け取る

`def update_book(book_id: int, new: BookIn):` には引数が2つあります。FastAPI は次のように振り分けます。

| 引数 | 判断のしかた | 値の出どころ |
|---|---|---|
| `book_id: int` | パスに `{book_id}` がある | パス(`/books/1` の `1`) |
| `new: BookIn` | 型がモデル | ボディの JSON |

### `update` の動き

辞書の `update` は、渡した辞書のキーで上書きし、渡さなかったキーはそのまま残します。

```python
book = {"id": 1, "title": "Python入門", "price": 2000}
book.update({"title": "Python入門 改訂版", "price": 2200})
# → {"id": 1, "title": "Python入門 改訂版", "price": 2200}
```

`id` は渡していないので残り、`title` と `price` だけが新しい値になります。

`for book in books:` の `book` は、リストの中の辞書そのものを指しています(コピーではありません)。そのため `book.update(...)` で書き換えると、リスト `books` の中身も変わります。

### サンプルを1行ずつ

- `@app.put("/books/{book_id}")`: PUT `/books/{book_id}` を登録します
- `for book in books:` / `if book["id"] == book_id:`: ch02 と同じ探し方です
- `book.update(new.model_dump())`: 受け取ったモデルを辞書にして、見つかった本を上書きします
- `return book`: 更新後の本を返します
- `return {"error": "not found"}`: 見つからなかったとき(ch02 と同じく、L9 で 404 に直します)

実行結果:

```text
200
{'id': 1, 'title': 'Python入門 改訂版', 'price': 2200}
{'error': 'not found'}
```

### やり取りの実物

```text
PUT /books/1 HTTP/1.1
host: testserver
content-length: 47
content-type: application/json

{"title":"Python入門 改訂版","price":2200}
```

```text
HTTP/1.1 200 OK
content-length: 54
content-type: application/json

{"id":1,"title":"Python入門 改訂版","price":2200}
```

対象の ID はパス(`/books/1`)、新しい値はボディ、と役割が分かれています。

## ch05 DELETE で削除

**DELETE** とは、データの削除に使う HTTP メソッドです(L7 で少し見ました)。`enumerate`(番号付きで取り出す関数)で位置を調べながら探し、見つかったら `pop(位置)` でリストから取り除きます。成功したら 204(No Content)を返し、ボディは返しません。これで Create・Read・Update・Delete の 4 操作がそろい、CRUD API の完成です。🔴 CRUD の締めくくりとして、削除も手が覚えるまで書きましょう。

```python
@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    for i, book in enumerate(books):
        if book["id"] == book_id:
            books.pop(i)
            return
```

### `enumerate` と `pop`

`enumerate(books)` は、要素を「位置(0から数える)と要素の組」で取り出します。`for i, book in ...` と書くと、組の1つ目が `i`、2つ目が `book` に入ります。

```text
i=0  book={'id': 1, 'title': 'Python入門', 'price': 2000}
i=1  book={'id': 2, 'title': 'FastAPI入門', 'price': 2500}
```

`books.pop(i)` は「i 番目の要素をリストから取り除く」メソッドです。取り除くには位置が必要なので、`enumerate` で位置も受け取っています。`id` と位置は別物です(id が 1 の本は位置 0)。

### サンプルを1行ずつ

- `@app.get("/books")`: 削除後の様子を確かめるための一覧 API(ch01 と同じ)
- `@app.delete("/books/{book_id}", status_code=204)`: DELETE を登録。成功時は 204
- `for i, book in enumerate(books):`: 位置と本を1つずつ取り出します
- `books.pop(i)`: 一致した本をリストから取り除きます
- `return`: 何も書かない `return` は `return None` と同じで、関数を終えます。204 なのでボディは返しません
- `client.delete("/books/1").status_code`: 1冊目を削除し、204 を確認します
- `client.get("/books").json()`: 一覧を取り直すと、1冊だけ残っています

実行結果:

```text
204
[{'id': 2, 'title': 'FastAPI入門', 'price': 2500}]
```

### やり取りの実物

```text
DELETE /books/1 HTTP/1.1
host: testserver
```

```text
HTTP/1.1 204 No Content
content-type: application/json

```

続く一覧の取得:

```text
HTTP/1.1 200 OK
content-length: 47
content-type: application/json

[{"id":2,"title":"FastAPI入門","price":2500}]
```

なお、このままでは存在しない ID(たとえば `/books/99`)を削除しようとしても、for 文が終わって関数が終わるだけなので 204 が返ります。「消すものがなかった」ことを 404 で伝える方法は L9 で学びます。
