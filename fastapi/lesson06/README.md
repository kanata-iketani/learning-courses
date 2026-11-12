# Lesson 06 バリデーション

送られてくるデータが正しいとは限りません。このレッスンでは、型や Field・Query・Path による検証(バリデーション)と、検証に失敗したときに返る 422 エラーの仕組みを学びます。

## ch01 型による自動検証と 422

**バリデーション**とは、送られてきたデータが正しい形かを検証することです。FastAPI はモデルの型ヒントを見て自動で検証し、型に合わないデータや足りないフィールドがあると **422**(Unprocessable Entity: 処理できないデータ、という意味のステータスコード。L3 で一度見ました)を返します。エラーレスポンスの `detail` の `loc` を見ると、どのフィールドが原因か分かります。🟡 検証コードを 1 行も書かなくても型だけで検証される、という仕組みを理解しましょう。

```python
r = client.post("/items", json={"name": "apple", "price": "たくさん"})
print(r.status_code)  # 422
```

### 自動検証の流れ

1. リクエストが届く
2. FastAPI(中では Pydantic)がボディの JSON をモデルの形と照らし合わせる
3. 合っていれば関数を呼ぶ。合っていなければ **関数を呼ばずに** 422 を返す

つまり、関数の中に来た時点で `item.price` は必ず int です。なお、`"120"` のように数値として読める文字列は int の `120` に変換されて通ります(L5 で見た変換)。`"たくさん"` や `12.5` のように整数にできない値が 422 になります。

### 422 のレスポンスの実物

サンプルの2回目(`price` に `"たくさん"`)のやり取りです。

```text
POST /items HTTP/1.1
host: testserver
content-length: 39
content-type: application/json

{"name":"apple","price":"たくさん"}
```

```text
HTTP/1.1 422 Unprocessable Content
content-length: 159
content-type: application/json

{"detail":[{"type":"int_parsing","loc":["body","price"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"たくさん"}]}
```

1行目の `Unprocessable Content` は 422 の新しい呼び名で、`Unprocessable Entity` と同じ意味です。ボディの `detail` は **リスト** で、問題のある項目ごとに1つずつ辞書が入ります。

| キー | 中身 | 意味 |
|---|---|---|
| `type` | `"int_parsing"` | エラーの種類(整数として読めなかった) |
| `loc` | `["body", "price"]` | 場所(location)。ボディの `price` |
| `msg` | `"Input should be a valid integer, ..."` | 人が読むための説明(英語) |
| `input` | `"たくさん"` | 実際に送られてきた値 |

`loc` の1つ目は値の出どころで、`body`(ボディ)・`query`(クエリパラメータ)・`path`(パスパラメータ)のどれかになります。

フィールドが足りないときは `type` が `missing` になります。`{"name": "apple"}` だけ送った場合の実物です。

```text
{"detail":[{"type":"missing","loc":["body","price"],"msg":"Field required","input":{"name":"apple"}}]}
```

### サンプルを1行ずつ

- `class Item(BaseModel):`: `name` は文字列、`price` は整数のモデル(L5 で見た書き方)
- 1回目の `client.post(...)`: 正しい形なので 200
- 2回目: `price` が `"たくさん"` で整数にできないので 422
- `r2.json()["detail"][0]["loc"]`: 左から順に、レスポンスの JSON を辞書にし → `"detail"` のリストを取り → その0番目(最初のエラー)の → `"loc"` を取り出します

実行結果:

```text
200
422
['body', 'price']
```

## ch02 Field で制約を付ける

型だけでなく「値の範囲」も検証するには、`from pydantic import Field` の **Field** を使います。`Field(gt=0)` は「0 より大きい」、`Field(max_length=10)` は「10 文字以内」という制約です。数値には gt(より大きい)・ge(以上)・lt(より小さい)・le(以下)、文字列には min_length / max_length が使えます。制約に反すると 422 が返ります。🔴 Field の書き方は実務でも頻出なので、手が覚えるまで書きましょう。

```python
class Item(BaseModel):
    name: str = Field(max_length=10)
    price: int = Field(gt=0)
```

### 制約の名前の覚え方

| 書き方 | 英語 | 意味 | 例: 値が 0 のとき |
|---|---|---|---|
| `gt=0` | greater than | 0 より大きい(0 は含まない) | 422 |
| `ge=0` | greater than or equal | 0 以上(0 を含む) | 通る |
| `lt=100` | less than | 100 より小さい | 通る |
| `le=100` | less than or equal | 100 以下 | 通る |
| `min_length=2` | | 2 文字以上 | (文字列用) |
| `max_length=10` | | 10 文字以内 | (文字列用) |

文字数は「文字」で数えます。日本語の1文字も1と数えます。

### `name: str = Field(...)` の読み方

`name: str` までは L5 と同じ「名前: 型」です。そのあとの `= Field(...)` は、ふつうの Python なら「既定値」を書く位置ですが、Pydantic ではここに Field を書くと「このフィールドの追加ルール」という意味になります。Field に既定値を指定していないので、`name` は省略できない(必須の)ままです。

### サンプルを1行ずつ

- `from pydantic import BaseModel, Field`: `Field` も一緒に読み込みます
- `name: str = Field(max_length=10)`: 名前は 10 文字以内
- `price: int = Field(gt=0)`: 価格は 0 より大きい整数
- 1回目: 両方満たすので 200
- 2回目: `price` が `0`。`gt=0` は 0 を含まないので 422
- 3回目: 名前が15文字。`max_length=10` を超えるので 422

実行結果:

```text
200
422
422
```

### 422 のレスポンスの実物

2回目(`price` が 0)のレスポンスです。

```text
HTTP/1.1 422 Unprocessable Content
content-length: 123
content-type: application/json

{"detail":[{"type":"greater_than","loc":["body","price"],"msg":"Input should be greater than 0","input":0,"ctx":{"gt":0}}]}
```

3回目(名前が長すぎる)のボディです。

```text
{"detail":[{"type":"string_too_long","loc":["body","name"],"msg":"String should have at most 10 characters","input":"とても長い商品名なので通らない","ctx":{"max_length":10}}]}
```

L6 ch01 で見た形に `ctx`(context。違反した制約の値)が加わっています。`type` を見れば、どの制約に引っかかったかが分かります。

## ch03 Query で検証する

クエリパラメータにも制約を付けられます。`from fastapi import Query` の **Query** を引数の既定値の位置に書き、`q: str = Query(min_length=2)` のように指定します。文字列には min_length / max_length、数値には ge / le などが使え、違反すると 422 が返ります。Field はボディ(モデルの中)用、Query はクエリパラメータ用、という使い分けです。🟡 「引数 = Query(制約)」という書き方のパターンを理解しましょう。

```python
@app.get("/search")
def search(q: str = Query(min_length=2)):
    return {"q": q}
```

### 値の出どころと、制約に使う道具

| 値の出どころ | 例 | 制約の道具 |
|---|---|---|
| ボディ(L5) | `{"name": "apple"}` | `Field`(pydantic から) |
| クエリパラメータ(L4) | `/search?q=apple` | `Query`(fastapi から) |
| パスパラメータ(L3) | `/users/5` | `Path`(fastapi から。次の ch04) |

`Field` は pydantic、`Query` と `Path` は fastapi から読み込む点に注意してください。

`q: str = Query(min_length=2, max_length=10)` は、L4 で `q: str = "ja"` のように既定値を書いた位置に `Query(...)` を書いたものです。Query に既定値を渡していないので、`q` は必須のままです。`?q=` を付けずに呼ぶと、`loc` が `["query", "q"]`、`type` が `missing` の 422 になります。

### サンプルを1行ずつ

- `from fastapi import FastAPI, Query`: `Query` を fastapi から読み込みます
- `def search(q: str = Query(min_length=2, max_length=10)):`: `q` は「2 文字以上 10 文字以内」の文字列だけ受け付けます
- `client.get("/search?q=apple")`: 5 文字なので 200
- `client.get("/search?q=a")`: 1 文字なので 422

実行結果:

```text
200
{'q': 'apple'}
422
```

### やり取りの実物

GET なのでボディはなく、値は URL の `?` 以降に入っています。

```text
GET /search?q=a HTTP/1.1
host: testserver
```

```text
HTTP/1.1 422 Unprocessable Content
content-length: 144
content-type: application/json

{"detail":[{"type":"string_too_short","loc":["query","q"],"msg":"String should have at least 2 characters","input":"a","ctx":{"min_length":2}}]}
```

`loc` の1つ目が `body` ではなく `query` になっていることから、クエリパラメータが原因だと分かります。

## ch04 Path で検証する

パスパラメータの検証には `from fastapi import Path` の **Path** を使います。書き方は Query と同じで、`user_id: int = Path(ge=1)` のように既定値の位置に制約を書きます。ID(データを1件ずつ区別する番号)のような値は「1 以上」が自然なので、`Path(ge=1)` で 0 や負の数を弾くのが定番です。違反すると 422 が返ります。🟡 「ID は Path(ge=1) で守る」というパターンを理解しましょう。

```python
@app.get("/users/{user_id}")
def get_user(user_id: int = Path(ge=1)):
    return {"user_id": user_id}
```

`ge=1` は L6 ch02 で見た「1 以上」です。範囲を両側から決めたいときは `Path(ge=1, le=100)`(1 以上 100 以下)のように並べて書けます。

検証は2段階で行われます。

1. 型の検証(L3 で見た): `/users/abc` は int にできないので 422(`type` は `int_parsing`)
2. 制約の検証: `/users/0` は int にはなるが `ge=1` を満たさないので 422(`type` は `greater_than_equal`)

どちらも関数が呼ばれる前に弾かれるので、関数の中では「`user_id` は 1 以上の整数」と決めてかかれます。

### サンプルを1行ずつ

- `from fastapi import FastAPI, Path`: `Path` を fastapi から読み込みます
- `@app.get("/users/{user_id}")`: パスの `{user_id}` 部分を引数で受け取ります(L3)
- `def get_user(user_id: int = Path(ge=1)):`: 1 以上の整数だけ受け付けます
- `client.get("/users/5")`: 5 は 1 以上なので 200
- `client.get("/users/0")`: 0 は 1 未満なので 422

実行結果:

```text
200
{'user_id': 5}
422
```

### やり取りの実物

```text
GET /users/0 HTTP/1.1
host: testserver
```

```text
HTTP/1.1 422 Unprocessable Content
content-length: 145
content-type: application/json

{"detail":[{"type":"greater_than_equal","loc":["path","user_id"],"msg":"Input should be greater than or equal to 1","input":"0","ctx":{"ge":1}}]}
```

`loc` が `["path", "user_id"]` になっています。`input` が `"0"`(文字列)なのは、URL の中の値はもともとすべて文字列だからです。
