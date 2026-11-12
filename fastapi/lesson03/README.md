# Lesson 03 パスパラメータ

URL の一部を変数として受け取る「パスパラメータ」を学ぶレッスンです。型ヒントによる自動変換と 422 エラー、固定パスと可変パスの定義順序まで、URL 設計の基本を身につけます。

## ch01 {item_id} で受け取る

URL の一部を変数として受け取る仕組みが **パスパラメータ** です。パスの中に `{item_id}` のように波かっこで書くと、その部分の値が同じ名前の引数として関数に渡されます。`/items/1` でも `/items/abc` でも同じ関数が呼ばれるため、「商品 ID ごとの URL」を1つの関数で処理できます。型ヒントを付けない場合、値は文字列 (str) のまま渡されます。🔴 「パスの `{名前}` = 関数の引数」という対応を、何度も書いて覚えましょう。

```python
@app.get("/items/{item_id}")
def read_item(item_id):
    return {"item_id": item_id}
```

### なぜパスパラメータが要るのか

商品が 1000 個あるとき、`/items/1`、`/items/2`、… と 1000 個のエンドポイントを書くわけにはいきません。`/items/{item_id}` と1つ書いておけば、`/items/` の後ろが何であっても同じ関数が呼ばれ、その「何であっても」の部分が引数に入ります。L2 で書いた `/about` のような変わらないパスは **固定パス**、`{ }` を含むパスは **可変パス** と呼んで区別します。

### 対応のしかた

| リクエストのパス | 照合するパターン | 関数に渡る値 |
|---|---|---|
| `/items/1` | `/items/{item_id}` | `item_id = "1"`(文字列) |
| `/items/abc` | `/items/{item_id}` | `item_id = "abc"` |
| `/items` | 一致しない | (404) |

URL はもともとただの文字列なので、`1` も文字列 `"1"` として渡ります。数値として受け取る方法は次の ch02 で学びます。

### サンプルを1行ずつ

- `@app.get("/items/{item_id}")`: `/items/` の後ろの部分を `item_id` という名前で受け取るエンドポイントを登録します
- `def read_item(item_id):`: 引数名を `{ }` の中と **完全に同じ名前** にします。違う名前だと値が渡りません
- `return {"item_id": item_id}`: 受け取った値をそのまま返します
- `client.get("/items/1")` と `client.get("/items/abc")`: 違う URL ですが、同じ `read_item` が呼ばれます

実行結果:

```text
{'item_id': '1'}
{'item_id': 'abc'}
```

1行目の `'1'` にクォートが付いているのが「文字列として渡った」証拠です。このときのやり取りの実物は次のとおりです。

```text
GET /items/1 HTTP/1.1
host: testserver
```

```text
HTTP/1.1 200 OK
content-type: application/json

{"item_id":"1"}
```

JSON のボディでも `"1"` とダブルクォートで囲まれていて、文字列のまま返っていることが分かります。

## ch02 型ヒントで int 変換

引数に `item_id: int` と型ヒントを付けると、FastAPI がパスパラメータを自動で int に変換します。`/items/3` なら数値の `3` が渡り、そのまま計算に使えます。数値にできない `/items/abc` のようなリクエストには、FastAPI が自動でステータスコード **422**(送られてきた値が処理できないことを表すエラー)を返し、理由も JSON で知らせてくれます。自分でエラー処理を書く必要はありません。🔴 型ヒント1つで「変換」と「検証」の両方が付くことを、手を動かして確かめましょう。

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "double": item_id * 2}
```

### 型ヒントとは

**型ヒント** は「この変数(引数)にはこの種類の値が入る予定です」というメモを `名前: 型` の形で書く Python の文法です。

```python
def add(a: int, b: int) -> int:   # -> int は「戻り値は int」というメモ
    return a + b
```

素の Python では型ヒントはただのメモで、実行時に何もチェックされません(`add("1", "2")` と呼んでも文字列がつながって `"12"` になるだけです)。FastAPI はこのメモを **読み取って使う** のが特徴で、`item_id: int` を見て「URL の文字列を int に変換し、できなければ 422 を返す」という処理を自動で行います。

| 型ヒント | `/items/3` のとき | `/items/abc` のとき |
|---|---|---|
| なし(ch01) | `"3"`(文字列) | `"abc"`(文字列) |
| `item_id: int` | `3`(数値) | 関数は呼ばれず 422 |

### サンプルを1行ずつ

- `def read_item(item_id: int):`: `item_id` を int で受け取る指定です
- `return {"item_id": item_id, "double": item_id * 2}`: 数値になっているので `* 2` で計算できます(文字列のままだと `"3" * 2` は `"33"` になってしまいます)
- `r = client.get("/items/3")` 〜 `print(r.json())`: 200 と、数値の 3 と 6 が返ります
- `r = client.get("/items/abc")`: 数値にできない値を送ります
- `print(r.json()["detail"][0]["msg"])`: 422 のボディから、エラーの理由の文だけを取り出して出します(取り出し方は下の実物を参照)

実行結果:

```text
200
{'item_id': 3, 'double': 6}
422
Input should be a valid integer, unable to parse string as an integer
```

### 422 のレスポンスの実物

`GET /items/abc` に対して実際に返ってきたレスポンスです。

```text
HTTP/1.1 422 Unprocessable Content
content-type: application/json

{"detail":[{"type":"int_parsing","loc":["path","item_id"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"abc"}]}
```

`detail` はエラーのリスト(複数の間違いをまとめて報告できるようにリストになっています)で、その1件目 `[0]` の中身は次のとおりです。

| キー | 値 | 意味 |
|---|---|---|
| `type` | `"int_parsing"` | エラーの種類(整数への変換に失敗) |
| `loc` | `["path", "item_id"]` | どこが悪いか(パスパラメータの item_id) |
| `msg` | `"Input should be a valid integer, ..."` | 理由の文(「正しい整数を入れてください」) |
| `input` | `"abc"` | 実際に送られてきた値 |

サンプルの `r.json()["detail"][0]["msg"]` は、「辞書の `detail` → リストの 0 番目 → 辞書の `msg`」と順にたどって理由の文を取り出しています。なお `/items/3.5` のような小数も整数ではないので 422 になります。

## ch03 複数のパスパラメータと順序

パスパラメータは `/users/{user_id}/items/{item_id}` のように1つの URL に複数置けます。注意が必要なのは、`/users/me`(自分の情報を返すなどの固定パス)と `/users/{user_id}`(可変パス)が並ぶ場合です。FastAPI は定義した順にパスを照合するため、可変パスを先に書くと `/users/me` へのリクエストまで `user_id = "me"` として拾われてしまいます。🟡 「固定パスは可変パスより先に定義する」という順序のルールを理解しましょう。

```python
@app.get("/users/me")      # 固定パスを先に
def read_me():
    return {"user": "me"}

@app.get("/users/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id}
```

### 照合の順番を表で追う

FastAPI はリクエストが来るたびに、登録した順(ファイルの上から順)にパターンと比べ、**最初に一致したもの** の関数を呼びます。`{user_id}` はどんな文字列とも一致するので、`me` とも一致してしまいます。

正しい順(固定パスが先)で `GET /users/me` が来た場合:

| 順 | パターン | 一致? | 結果 |
|---|---|---|---|
| 1 | `/users/me` | 一致 | `read_me` が呼ばれて 200 |
| 2 | `/users/{user_id}` | (見ない) | |

逆の順(可変パスが先)の場合:

| 順 | パターン | 一致? | 結果 |
|---|---|---|---|
| 1 | `/users/{user_id}` | 一致(`user_id = "me"`) | `"me"` を int にできず 422 |
| 2 | `/users/me` | (見ない) | |

逆の順で実際に `GET /users/me` を送ると、次の 422 が返ります(ch02 で見た形です)。

```text
HTTP/1.1 422 Unprocessable Content
content-type: application/json

{"detail":[{"type":"int_parsing","loc":["path","user_id"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"me"}]}
```

### サンプルを1行ずつ

- `@app.get("/users/me")` と `read_me`: 固定パスを先に登録します
- `@app.get("/users/{user_id}")` と `read_user(user_id: int)`: 可変パスを後に登録します
- `@app.get("/users/{user_id}/items/{item_id}")`: `{ }` を2つ持つパスです。`/` の区切りごとに照合されるので、`/users/7/items/3` は `user_id = 7`、`item_id = 3` になります
- `def read_user_item(user_id: int, item_id: int):`: パスの `{ }` と同じ名前の引数を2つ並べます。引数の並び順はパスの順と違っていてもかまいません(名前で対応するため)

実行結果:

```text
{'user': 'me'}
{'user_id': 7}
{'user_id': 7, 'item_id': 3}
```

`/users/7` は区切りの数が合わないので `/users/{user_id}/items/{item_id}` とは一致せず、`/users/{user_id}` のほうが呼ばれます。
