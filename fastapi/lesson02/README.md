# Lesson 02 はじめてのAPI

`@app.get` でパスと関数を結びつけ、辞書を返すだけで JSON レスポンスになる、という FastAPI の基本形を最小のアプリで身につけるレッスンです。ステータスコードやヘッダーなど、レスポンスの読み方もここで押さえます。

## ch01 最小のアプリと @app.get("/")

FastAPI アプリの最小構成は「アプリ本体を作る」「パスに関数を割り当てる」の2つです。`@app.get("/")` は「パス `/` に **GET**(データを取得するときに使う **HTTP メソッド**。HTTP メソッドとはリクエストの種類のことです)が来たら、直下の関数を実行する」という登録です。この「URL のパスと処理の組」を **エンドポイント** と呼びます。🔴 最小アプリは FastAPI のすべての土台なので、何も見ずに書けるようにしましょう。

```python
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello"}
```

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

## ch03 JSON を返す

FastAPI の関数は、Python の辞書やリストを `return` するだけで、自動的に JSON に変換してレスポンスとして返します。`json.dumps` を自分で呼ぶ必要はありません。リストの中に辞書を入れた形(一覧データの定番の形)もそのまま返せます。なお `r.json()` で受け取ると Python の辞書・リストに戻るため、print するとシングルクォート表示になります。🔴 「辞書・リストを返せば JSON になる」を手に馴染ませましょう。

```python
@app.get("/users")
def list_users():
    return [{"name": "sato"}, {"name": "suzuki"}]
```

## ch04 レスポンスの中身を調べる

レスポンスには本文以外の情報も含まれます。**ステータスコード** は処理結果を表す3桁の数字で、`200` は成功、`404` は「パスが見つからない」を意味します。**ヘッダー** はレスポンスに付く補足情報で、`content-type` ヘッダーを見ると本文の形式が分かります(FastAPI は `application/json` を返します)。定義していないパスへのリクエストには、FastAPI が自動で 404 を返します。🟡 `r.status_code`・`r.json()`・`r.headers[...]` の3つでレスポンスを調べられることを理解しましょう。

```python
r = client.get("/")
print(r.status_code)              # 200
print(r.headers["content-type"])  # application/json
```
