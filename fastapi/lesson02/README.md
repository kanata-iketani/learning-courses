# Lesson 02 はじめてのAPI

`@app.get` でパスと関数を結びつけ、辞書を返すだけで JSON レスポンスになる、という FastAPI の基本形を最小のアプリで身につけるレッスンです。ステータスコードやヘッダーなど、レスポンスの読み方もここで押さえます。

## ch01 最小のアプリと @app.get("/")

FastAPI アプリの最小構成は「アプリ本体を作る」「パスに関数を割り当てる」の2つです。`@app.get("/")` は「パス `/` に **GET**(データを取得するときに使う **HTTP メソッド**。HTTP メソッドとはリクエストの種類のことです)が来たら、直下の関数を実行する」という登録です。この「HTTP メソッド + URL のパスと処理の組」を **エンドポイント** と呼びます。🔴 最小アプリは FastAPI のすべての土台なので、何も見ずに書けるようにしましょう。

```python
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello"}
```

### URL とパス

ブラウザのアドレス欄に出る `http://127.0.0.1:8000/` のような文字列が **URL** です。このうち、サーバの住所(`http://127.0.0.1:8000`)より後ろの `/` で始まる部分を **パス** と呼びます。`/` だけのパスは「一番上(トップ)」を表します。FastAPI のデコレータに書くのはこのパスの部分だけです。

| URL | パス |
|---|---|
| `http://127.0.0.1:8000/` | `/` |
| `http://127.0.0.1:8000/about` | `/about` |

### サンプルを1行ずつ

- `app = FastAPI()`: アプリ本体を作ります。この時点では、まだどのパスにも答えられません
- `@app.get("/")`: 次の行の関数を「GET `/` の担当」として `app` に登録します
- `def read_root():`: 担当の関数です。関数名は自由ですが、何をするか分かる名前にします(FastAPI では、この関数を **パス操作関数** と呼ぶこともあります)
- `return {"message": "Hello"}`: 返した辞書が JSON になってクライアントに届きます
- `client = TestClient(app)` 〜 `print(r.json())`: L1 ch03 で見た定型です。GET `/` を送り、ステータスコードと JSON を出します

実行結果:

```text
200
{'message': 'Hello'}
```

### このとき流れるリクエストとレスポンス

```text
GET / HTTP/1.1
host: testserver
```

```text
HTTP/1.1 200 OK
content-type: application/json
content-length: 19

{"message":"Hello"}
```

リクエストの1行目「`GET /`」が、デコレータの `get` と `"/"` にちょうど対応しています。FastAPI はこの2つが一致する関数を探して呼び出します。

## ch02 デコレータとパスの関係

`@app.get(...)` のように関数の直前に `@` 付きで書く記法を **デコレータ**(関数に機能を追加する Python の仕組み)と呼びます。FastAPI ではデコレータが「このパスに来たリクエストをこの関数に渡す」という対応表を作ります。デコレータを増やせば、1つのアプリに複数のパスをいくつでも定義できます。🔴 パスごとに「デコレータ + 関数」を1組ずつ書く形を、手が覚えるまで繰り返しましょう。

```python
@app.get("/")
def home():
    return {"page": "home"}

@app.get("/about")
def about():
    return {"page": "about"}
```

### デコレータはいつ動くのか

デコレータは、関数を **定義した瞬間**(ファイルを上から読み込んだとき)に1回だけ動きます。リクエストが来たときに動くのではありません。次の素の Python で確かめられます。

```python
def deco(f):
    print("登録:", f.__name__)  # f.__name__ は関数の名前
    return f

@deco
def hello():
    return 1

print(hello())
```

```text
登録: hello
1
```

`@deco` は「`hello = deco(hello)` を実行する」の省略形です。`@app.get("/")` も同じで、定義した時点で `app` の対応表に「GET `/` → この関数」が書き込まれます。リクエストが来たら、FastAPI がその表を引いて関数を呼びます。

サンプルで作られる対応表は次のとおりです。

| メソッド | パス | 呼ばれる関数 | 返す JSON |
|---|---|---|---|
| GET | `/` | `home` | `{"page":"home"}` |
| GET | `/menu` | `menu` | `{"page":"menu"}` |
| GET | `/access` | `access` | `{"page":"access"}` |

### サンプルを1行ずつ

- `@app.get("/")` と `def home():`: GET `/` の担当として `home` を登録します
- `@app.get("/menu")` と `def menu():`: GET `/menu` の担当として `menu` を登録します
- `@app.get("/access")` と `def access():`: 同様に GET `/access` を登録します
- `print(client.get("/menu").json())`: L1 ch03 の1行書きです。GET `/menu` を送り、返った JSON を辞書にして出します

実行結果:

```text
{'page': 'home'}
{'page': 'menu'}
{'page': 'access'}
```

関数名とパスは同じでなくてもかまいません(`/` の担当が `home` のように)。ただし同じファイルの中で関数名が重複すると、後から定義したほうで名前が上書きされて紛らわしいので、組ごとに別の名前にします。

## ch03 JSON を返す

FastAPI の関数は、Python の辞書やリストを `return` するだけで、自動的に JSON に変換してレスポンスとして返します。L1 ch01 で使った `json.dumps` を自分で呼ぶ必要はありません。リストの中に辞書を入れた形(一覧データの定番の形)もそのまま返せます。🔴 「辞書・リストを返せば JSON になる」を手に馴染ませましょう。

```python
@app.get("/users")
def list_users():
    return [{"name": "sato"}, {"name": "suzuki"}]
```

### 実際に流れる JSON

サンプルの2つのエンドポイントは、ネットワーク上では次のボディを返しています(実際に取り出した文字列です)。

| パス | return した Python の値 | レスポンスのボディ(JSON) |
|---|---|---|
| `/shop` | `{"name": "demo堂", "open": True}` | `{"name":"demo堂","open":true}` |
| `/users` | `[{"name": "sato"}, {"name": "suzuki"}]` | `[{"name":"sato"},{"name":"suzuki"}]` |

- Python の `True` が JSON の `true` に変わっています(L1 ch01 の対応表のとおり)
- 辞書は JSON の **オブジェクト** `{...}`、リストは JSON の **配列** `[...]` になります
- FastAPI は `:` や `,` の後ろの空白を詰めて送ります。中身は同じです

### サンプルを1行ずつ

- `@app.get("/shop")` 〜 `return {"name": "demo堂", "open": True}`: 辞書を1つ返すエンドポイントです
- `@app.get("/users")` 〜 `return [{"name": "sato"}, {"name": "suzuki"}]`: 辞書を2つ入れたリストを返すエンドポイントです。「ユーザー一覧」のような複数件のデータはこの形で返すのが定番です
- `print(client.get("/shop").json())`: 受け取った JSON を `r.json()` で Python の値に戻して出します

実行結果:

```text
{'name': 'demo堂', 'open': True}
[{'name': 'sato'}, {'name': 'suzuki'}]
```

`r.json()` で受け取ると Python の辞書・リストに戻るため、print するとシングルクォート `'` 表示になり、`true` も `True` に戻ります。期待出力がシングルクォートなのはこのためです。

## ch04 レスポンスの中身を調べる

レスポンスには本文以外の情報も含まれます。**ステータスコード** は処理結果を表す3桁の数字で、`200` は成功、`404` は「パスが見つからない」を意味します。**ヘッダー** はレスポンスに付く補足情報で、`content-type` ヘッダーを見ると本文の形式が分かります(FastAPI は `application/json` を返します)。定義していないパスへのリクエストには、FastAPI が自動で 404 を返します。🟡 `r.status_code`・`r.json()`・`r.headers[...]` の3つでレスポンスを調べられることを理解しましょう。

```python
r = client.get("/")
print(r.status_code)              # 200
print(r.headers["content-type"])  # application/json
```

### ステータスコードの読み方

先頭の数字で大まかな意味が決まっています。

| 範囲 | 意味 | 例 |
|---|---|---|
| 2xx | 成功 | 200 OK |
| 4xx | クライアント側の間違い(送り方が悪い) | 404 Not Found(そのパスはない) |
| 5xx | サーバ側の失敗(プログラムのエラーなど) | 500 Internal Server Error |

ほかのコードは L7 で使い分けを学びます。

### Response オブジェクトから取り出せるもの

`r = client.get(...)` の `r` には、レスポンスの全部が入っています。

| 書き方 | 取り出すもの | 例 |
|---|---|---|
| `r.status_code` | ステータスコード(int) | `200` |
| `r.headers["content-type"]` | ヘッダーの値(str)。`[ ]` の中はヘッダー名 | `'application/json'` |
| `r.json()` | ボディの JSON を辞書・リストに戻したもの | `{'message': 'Hello'}` |
| `r.text` | ボディをそのままの文字列で | `'{"message":"Hello"}'` |

`r.headers` は辞書のように `[名前]` で値を取り出せます(大文字・小文字は区別しません)。

### 404 のときの実物

定義していない `/nothing` を GET したときのやり取りです。

```text
GET /nothing HTTP/1.1
host: testserver
```

```text
HTTP/1.1 404 Not Found
content-type: application/json
content-length: 22

{"detail":"Not Found"}
```

エラーのときもボディは JSON で、`detail`(詳しい内容)というキーに理由が入ります。この形は L9 のエラー処理でも使います。

### サンプルを1行ずつ

- `r = client.get("/")`: 定義済みのパスに GET します
- `print(r.status_code)`: `200` を出します
- `print(r.headers["content-type"])`: `application/json` を出します
- `print(r.json())`: `{'message': 'Hello'}` を出します
- `r = client.get("/nothing")`: 定義していないパスに GET します。変数 `r` は新しいレスポンスで上書きされます
- `print(r.status_code)` と `print(r.json())`: `404` と `{'detail': 'Not Found'}` を出します

実行結果:

```text
200
application/json
{'message': 'Hello'}
404
{'detail': 'Not Found'}
```

なお、パスはあるのにメソッドが違う場合(GET 専用のパスに POST を送るなど)は、404 ではなく `405 Method Not Allowed`(そのメソッドは使えない)が返ります。
