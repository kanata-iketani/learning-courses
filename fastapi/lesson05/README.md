# Lesson 05 リクエストボディとPydantic

クライアントからサーバへデータを送るには、リクエストボディ(送信データ本体)を使います。このレッスンでは、Pydantic の BaseModel で「受け取るデータの形」を宣言し、POST でボディを受け取って使う方法を学びます。

## ch01 Pydantic の BaseModel

**Pydantic**(パイダンティック)とは、データの形を宣言してチェックする Python ライブラリで、FastAPI に組み込まれています。`BaseModel` を継承したクラスに「フィールド名: 型」を並べると、それが「受け取るデータの形」の宣言になります。関数の引数にこのクラスを型として指定すると、FastAPI は送られてきた JSON をモデルのインスタンスに変換してくれます。🔴 モデル定義はこの先ずっと使うので、手が覚えるまで書きましょう。

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
```

### 用語: クラス・継承・インスタンス・フィールド

- **クラス**: 「こういう値を持つデータ」という設計図。`class User(...):` で作ります
- **継承**: `class User(BaseModel):` のかっこの中にクラス名を書くと、`BaseModel` の機能(型のチェックや変換)を `User` がそのまま受け継ぎます
- **フィールド**: モデルが持つ項目。`name: str` は「`name` という項目があり、型は str(文字列)」という意味です。`:` の右は L3 で見た **型ヒント**(値の型を書き添える書き方)です
- **インスタンス**: 設計図から作った実物のデータ。`User(name="demo", age=13)` と書くと1つ作れます

Pydantic は型ヒントを見て値を変換・確認します。たとえば `User(name="demo", age="13")` と文字列の `"13"` を渡しても、`age` は int の `13` に変換されます。数値にできない値ならエラーになります(L6 で詳しく見ます)。

### サンプルを1行ずつ

- `from pydantic import BaseModel`: Pydantic から `BaseModel` を読み込みます
- `class User(BaseModel):` とその下の2行: 「`name` は文字列、`age` は整数」という形のモデルを定義します
- `@app.post("/users")`: L2 で見た `@app.get` の POST 版です。「POST メソッドで `/users` に来たリクエストをこの関数で処理する」という登録です(POST は次の ch02 で詳しく見ます)
- `def create_user(user: User):`: 引数の型が `User`(モデル)なので、FastAPI は「リクエストの **ボディ**(本文。L1 で見たレスポンスのボディと同じく、空行のあとに付くデータ)から JSON を読んで `User` に変換して渡す」と判断します。パスパラメータ(L3)やクエリパラメータ(L4)のように URL から取るのではない点が違いです
- `return user`: モデルをそのまま返すと、FastAPI が JSON に変換してレスポンスにします
- `client.post("/users", json={"name": "demo", "age": 13})`: POST リクエストを送ります。`json=` に渡した辞書がボディになります

実行結果:

```text
200
{'name': 'demo', 'age': 13}
```

### やり取りの実物

リクエスト(ボディ付き):

```text
POST /users HTTP/1.1
host: testserver
content-length: 24
content-type: application/json

{"name":"demo","age":13}
```

`content-type: application/json` は「ボディは JSON です」という目印で、`json=` を使うと TestClient が自動で付けます。

レスポンス:

```text
HTTP/1.1 200 OK
content-length: 24
content-type: application/json

{"name":"demo","age":13}
```

受け取った `User` をそのまま返したので、送ったものと同じ JSON が返ってきています。

関数の中で `print(user)` とすると `name='demo' age=13` と表示されます。辞書ではなく `User` のインスタンスになっていることが分かります。

## ch02 POST でボディを受け取る

**リクエストボディ**とは、リクエストに載せて送るデータ本体のことです。データを新しく作る・登録するときは **POST**(データ送信用の HTTP メソッド)を使い、ボディに JSON を入れて送ります。TestClient では `client.post(URL, json=辞書)` と書くと、辞書が JSON のボディとして送られます。なお、POST 用の URL を GET で呼ぶと 405(メソッド不一致)が返ります。🔴 `client.post(json=...)` の形は何度も書いて覚えましょう。

```python
r = client.post("/echo", json={"text": "こんにちは"})
```

### GET と POST の違い

| | GET(L2 で見た) | POST |
|---|---|---|
| 目的 | データを取得する | データを送って新しく作る・登録する |
| 値の渡し方 | URL(パス・クエリパラメータ) | 主にボディ(JSON) |
| FastAPI の書き方 | `@app.get(...)` | `@app.post(...)` |
| TestClient の書き方 | `client.get(URL)` | `client.post(URL, json=辞書)` |

URL に載せられるのは短い文字だけで、しかも見える場所に残ります。名前・本文・住所のような長い・複数の値はボディで送るのが普通です。

### サンプルを1行ずつ

- `class Message(BaseModel): text: str`: ボディの形を「`text` という文字列が1つ」と宣言します(L5 ch01 で見た BaseModel)
- `@app.post("/echo")`: POST `/echo` の担当として関数を登録します
- `def echo(msg: Message):`: ボディの JSON が `Message` に変換されて `msg` に入ります
- `return {"received": msg.text}`: `msg.text` で中身を取り出し、別のキー名の辞書にして返します
- `r = client.post("/echo", json={"text": "こんにちは"})`: ボディ付きの POST を送ります
- `r2 = client.get("/echo")`: 同じパスに GET で送ってみます。`/echo` には POST しか登録していないので、**405 Method Not Allowed**(そのパスはあるが、そのメソッドは受け付けていない)が返ります

実行結果:

```text
200
{'received': 'こんにちは'}
405
```

### やり取りの実物

1回目(POST):

```text
POST /echo HTTP/1.1
host: testserver
content-length: 26
content-type: application/json

{"text":"こんにちは"}
```

```text
HTTP/1.1 200 OK
content-length: 30
content-type: application/json

{"received":"こんにちは"}
```

`content-length` が文字数より大きいのは、日本語1文字が3バイトで数えられるからです。

2回目(GET):

```text
GET /echo HTTP/1.1
host: testserver
```

```text
HTTP/1.1 405 Method Not Allowed
allow: POST
content-length: 31
content-type: application/json

{"detail":"Method Not Allowed"}
```

`allow: POST` ヘッダは「このパスで使えるメソッドは POST です」という案内です。GET にはボディがないので、リクエストに `content-type` も付いていません。

## ch03 モデルの属性を使う

受け取ったモデルは普通の Python オブジェクトです。値は `order.price` のように**属性**(`変数.名前` のようにドットで取り出す値)として取り出し、計算や加工に使えます。辞書のように `order["price"]` とは書けない点に注意してください。型ヒントどおりの型であることが保証されているので、そのまま安心して計算に使えます。🔴 「属性で取り出す → 計算する → 辞書で返す」の流れを、手が覚えるまで書きましょう。

```python
@app.post("/orders")
def create_order(order: Order):
    total = order.price * order.quantity
    return {"item": order.item, "total": total}
```

### 辞書との書き方の違い

| | 辞書 | モデル(BaseModel) |
|---|---|---|
| 取り出し方 | `data["price"]` | `order.price` |
| 間違えたとき | `KeyError`(キーがない) | `AttributeError`(属性がない) |

モデルに `order["price"]` と書くと、`TypeError: 'Order' object is not subscriptable`(`[ ]` で取り出せない型です)というエラーになります。

「保証されている」とは、関数が呼ばれた時点で Pydantic のチェックが済んでいるという意味です。`price` に `"abc"` のような数値にできない値が送られた場合は、関数が呼ばれる前に FastAPI が 422(L3 で見た「値を処理できない」エラー)を返します。そのため関数の中で「int かどうか」を自分で確かめる必要がありません。

### サンプルを1行ずつ

- `class Order(BaseModel):`: `item`(文字列)・`price`(整数)・`quantity`(個数。整数)の3項目を持つモデルです
- `def create_order(order: Order):`: ボディの JSON が `Order` に変換されて `order` に入ります
- `total = order.price * order.quantity`: 単価 × 個数を計算します。`480 * 3` で `1440` です
- `return {"item": order.item, "total": total}`: 商品名と合計を辞書にして返します。受け取った項目(`price`・`quantity`)をそのまま返す必要はなく、返す形は自由に決められます

実行結果:

```text
200
{'item': 'コーヒー', 'total': 1440}
```

### やり取りの実物

```text
POST /orders HTTP/1.1
host: testserver
content-length: 48
content-type: application/json

{"item":"コーヒー","price":480,"quantity":3}
```

```text
HTTP/1.1 200 OK
content-length: 36
content-type: application/json

{"item":"コーヒー","total":1440}
```

送ったボディ(3項目)と返ってきたボディ(2項目)の形が違う点に注目してください。

## ch04 model_dump とレスポンス

`model_dump()` は、モデルを Python の辞書に変換するメソッドです(Pydantic v2 の書き方。古い `dict()` は使いません)。モデルには後からキーを追加できませんが、辞書にすればできます。レスポンスに ID や計算結果などのキーを足したいときは、「いったん辞書にしてからキーを足す」のが定石です。🟡 「モデル → 辞書 → 加工して返す」という流れを理屈で理解しましょう。

```python
data = item.model_dump()  # モデル → 辞書
data["id"] = 1            # 辞書ならキーを追加できる
```

### 用語

- **メソッド**: クラスに付いている関数のこと。`item.model_dump()` のように `インスタンス.名前()` で呼びます
- **Pydantic v2**: Pydantic のバージョン2(この講座の環境は 2.x)。v1 では `item.dict()` と書いていたので、古い記事ではその書き方を見かけます
- **ID**: データを1件ずつ区別するための番号。L8 の CRUD で本格的に使います

### モデルに直接キーを足すとどうなるか

`item.id = 1` のように、宣言していないフィールドを足そうとすると `ValueError: "Item" object has no field "id"` というエラーになります。モデルは「宣言した形」以外を受け付けないからです。辞書には自由にキーを足せるので、`model_dump()` で辞書に変えてから足します。

### サンプルを1行ずつ

- `data = item.model_dump()`: `Item` のインスタンスを辞書 `{'name': 'apple', 'price': 120}` に変換します
- `data["id"] = 1`: 辞書に `id` というキーを追加します。辞書の最後に入ります
- `return data`: 辞書を返すので、そのまま JSON になります

実行結果:

```text
200
{'name': 'apple', 'price': 120, 'id': 1}
```

### やり取りの実物

```text
POST /items HTTP/1.1
host: testserver
content-length: 28
content-type: application/json

{"name":"apple","price":120}
```

```text
HTTP/1.1 200 OK
content-length: 35
content-type: application/json

{"name":"apple","price":120,"id":1}
```

送っていない `id` がレスポンスに増えています。このように「受け取った内容 + サーバが付けた情報」を返す形は、L8 でデータを登録する API でもそのまま使います。
