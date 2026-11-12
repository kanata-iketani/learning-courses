# Lesson 07 レスポンスモデルとステータスコード

API が「何を返すか」を設計するレッスンです。response_model でレスポンスの形を宣言して見せたくない情報を隠し、201 などのステータスコードで処理結果の意味を正しく伝えます。

## ch01 response_model の指定

**response_model** とは、デコレータに指定する「レスポンスの形」の宣言です。`@app.get("/items/1", response_model=Item)` のように書くと、関数が返した値は Item の形に整えられ、モデルにないキーは自動で取り除かれます。返す形が明文化されるので、API の仕様がコードから読み取れるようになります。🔴 response_model の指定は基本の型として手が覚えるまで書きましょう。

```python
@app.get("/items/1", response_model=Item)
def get_item():
    return {"name": "apple", "price": 120, "secret": "内部情報"}
    # → レスポンスは {"name": "apple", "price": 120}
```

### 入口のモデルと出口のモデル

L5〜L6 では、モデルを **関数の引数** に書いて「受け取るボディの形」を決めました。response_model は、モデルを **デコレータ** に書いて「返すボディの形」を決めます。

| 書く場所 | 決めるもの | 合わないとき |
|---|---|---|
| 関数の引数 `item: Item` | リクエストのボディ(入口) | 422(送った側の誤り) |
| デコレータ `response_model=Item` | レスポンスのボディ(出口) | 余分なキーは消える。足りないキーは 500(サーバ側の誤り) |

足りない場合の **500**(Internal Server Error: サーバの中でエラーが起きた)は、たとえば `price` を返し忘れたときに起こります。返す側のプログラムのミスなので、受け取った側の誤りを表す 422 にはなりません。

### サンプルを1行ずつ

- `class Item(BaseModel):`: `name`(文字列)と `price`(整数)を持つモデル
- `@app.get("/items/1", response_model=Item)`: GET `/items/1` の担当を登録し、返す形を `Item` と宣言します。`response_model=` はデコレータの **キーワード引数**(`名前=値` の形で渡す引数)です
- `return {"name": "apple", "price": 120, "secret": "仕入れ値は 60 円"}`: 3つのキーを持つ辞書を返します
- FastAPI は返された辞書を `Item` の形にはめ直し、`Item` にない `secret` を捨ててから JSON にします

実行結果:

```text
200
{'name': 'apple', 'price': 120}
```

### やり取りの実物

```text
GET /items/1 HTTP/1.1
host: testserver
```

```text
HTTP/1.1 200 OK
content-length: 28
content-type: application/json

{"name":"apple","price":120}
```

関数は `secret` を返していますが、ネットワークに流れたボディには入っていません。

## ch02 見せたくない項目を隠す

パスワードのような秘密の値は、レスポンスに絶対に含めてはいけません。定石は、**入力用モデル**(パスワードあり)と**出力用モデル**(パスワードなし)の 2 つに分け、`response_model` に出力用を指定することです。関数が入力用モデルをそのまま返しても、レスポンスは出力用の形に絞られ、パスワードは消えます。🔴 「入力用と出力用を分ける」設計は Web API の必須知識なので、必ず書けるようにしましょう。

```python
@app.post("/users", response_model=UserOut)
def create_user(user: UserIn):
    return user  # password は UserOut にないので消える
```

名前の `In` は入力(受け取る側)、`Out` は出力(返す側)の意味で、`UserIn` / `UserOut` は FastAPI でよく見る名付け方です。

### なぜ分けるのか

レスポンスは、受け取ったプログラムがログ(記録)に残したり画面に出したりします。一度外に出た値は取り消せないので、「返さない」ことをコードで保証しておく必要があります。response_model で出力用モデルを指定しておけば、関数の中でうっかり全部返しても、パスワードは自動で取り除かれます。

### サンプルを1行ずつ

- `class UserIn(BaseModel): name: str / password: str`: 受け取るときの形。パスワードを含みます
- `class UserOut(BaseModel): name: str`: 返すときの形。パスワードを持ちません
- `@app.post("/users", response_model=UserOut)`: POST `/users` を登録し、返す形を `UserOut` にします
- `def create_user(user: UserIn):`: ボディは `UserIn` として受け取ります(L5)
- `return user`: `UserIn` をそのまま返します。FastAPI が `UserOut` の形に絞るので、`password` は消えます

実行結果:

```text
200
{'name': 'demo'}
```

### やり取りの実物

リクエストにはパスワードが入っています。

```text
POST /users HTTP/1.1
host: testserver
content-length: 39
content-type: application/json

{"name":"demo","password":"himitsu123"}
```

レスポンスには入っていません。

```text
HTTP/1.1 200 OK
content-length: 15
content-type: application/json

{"name":"demo"}
```

## ch03 status_code=201 の指定

**ステータスコード**とは、処理結果を表す 3 桁の数字です(L2 で見た `r.status_code`)。FastAPI の既定では成功はすべて 200(OK)ですが、「新しくデータを作った」ことを伝えるには **201**(Created)を返すのが Web API の作法です。デコレータに `status_code=201` を書くだけで、成功時のコードが変わります。🟡 「POST で作成したら 201」という対応を理屈で理解しましょう。

```python
@app.post("/items", status_code=201)
def create_item(item: Item):
    return item
```

### ステータスコードは百の位で分類される

| 範囲 | 意味 | これまでに出たもの |
|---|---|---|
| 2xx | 成功 | 200 OK、201 Created |
| 4xx | クライアント(送った側)の誤り | 404 Not Found、405 Method Not Allowed、422 Unprocessable Content |
| 5xx | サーバ側の誤り | 500 Internal Server Error |

200 も 201 も「成功」ですが、201 にすると「成功し、しかも新しいデータができた」ことまで受け取った側に伝わります。

`status_code=201` は「関数が普通に終わったときに返すコード」の指定です。ボディの検証で 422 になった場合など、関数まで届かなかったときは 422 のままです。

### サンプルを1行ずつ

- `@app.post("/items")`: `status_code` を書いていないので、成功時は既定の 200
- `@app.post("/items2", status_code=201)`: 成功時は 201
- どちらの関数も受け取った `item` をそのまま返します
- 同じボディを両方に送り、ステータスコードだけを print します

実行結果:

```text
200
201
```

### やり取りの実物

2回目(`/items2`)のやり取りです。

```text
POST /items2 HTTP/1.1
host: testserver
content-length: 16
content-type: application/json

{"name":"apple"}
```

```text
HTTP/1.1 201 Created
content-length: 16
content-type: application/json

{"name":"apple"}
```

1回目との違いは、レスポンスの1行目が `200 OK` か `201 Created` かだけです。ボディは同じです。

## ch04 ステータスコードの使い分け

よく使うステータスコードは 4 つです。**200**(OK: 取得や更新の成功)、**201**(Created: 新しく作成した)、**204**(No Content: 成功したが返す中身がない。削除でよく使う)、**404**(Not Found: 見つからない)。204 のレスポンスにはボディを入れない決まりなので、関数は `return None`(何も返さない)にします。存在しない URL へのアクセスには FastAPI が自動で 404 を返します(L2 で見ました)。🟡 4 つのコードの意味を説明できるようになりましょう。

```python
@app.delete("/items/1", status_code=204)
def delete_item():
    return None  # 204 ではボディを返さない
```

### 新しく出てくるメソッド: DELETE

**DELETE** は「データを削除したい」ことを表す HTTP メソッドです。FastAPI では `@app.delete(...)`、TestClient では `client.delete(URL)` と書きます。L8 で本格的に使います。

### サンプルを1行ずつ

- `@app.get("/items")` → `return []`: 空のリストを返す取得 API。既定の 200
- `@app.post("/items", status_code=201)` → `return {"created": True}`: 作成 API。201。この関数は引数がないので、ボディなしで呼べます
- `@app.delete("/items/1", status_code=204)` → `return None`: 削除 API。204
- `client.get("/nothing")`: どこにも登録していないパスなので、FastAPI が自動で 404 を返します
- `print(client.get("/items").status_code)`: 送って、すぐにステータスコードだけ取り出して print する1行の書き方です(L1 ch03 で見た左から順に読む形)

実行結果:

```text
200
201
204
404
```

### やり取りの実物

POST(ボディなし)と 201:

```text
POST /items HTTP/1.1
host: testserver
content-length: 0
```

```text
HTTP/1.1 201 Created
content-length: 16
content-type: application/json

{"created":true}
```

`content-length: 0` は「ボディの長さが 0」、つまりボディがないという意味です。Python の `True` は JSON では `true` になります(L1)。

DELETE と 204:

```text
DELETE /items/1 HTTP/1.1
host: testserver
```

```text
HTTP/1.1 204 No Content
content-type: application/json

```

空行のあとに何もありません。これが「ボディなし」のレスポンスです。

存在しないパスと 404:

```text
GET /nothing HTTP/1.1
host: testserver
```

```text
HTTP/1.1 404 Not Found
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```
