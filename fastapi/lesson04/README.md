# Lesson 04 クエリパラメータ

`?q=hello` のように URL の末尾に付ける「クエリパラメータ」を学ぶレッスンです。関数の引数を書くだけで受け取れ、デフォルト値・int 変換・`str | None` による省略可能な引数まで扱います。

## ch01 引数=クエリパラメータ

URL の `?` 以降に `?q=hello` の形で付ける値を **クエリパラメータ** と呼びます(複数あるときは `&` でつなぎます)。FastAPI では、関数の引数のうちパスに含まれない名前は、自動的にクエリパラメータとして扱われます。特別な宣言は不要で、引数を書くだけです。🔴 「パスにない引数 = クエリパラメータ」という対応を、手を動かして覚えましょう。

```python
@app.get("/search")
def search(q: str):
    return {"q": q}
```

呼び出す側は `client.get("/search?q=fastapi")` のように URL に付けて渡します。

### URL の分解

`/find?word=hello&lang=en` という URL は、次のように分かれます。

| 部分 | 中身 | 役割 |
|---|---|---|
| パス | `/find` | どのエンドポイントか(照合に使う) |
| `?` | | ここからクエリパラメータ、という区切り |
| `word=hello` | 名前 `word`、値 `hello` | 1つ目のクエリパラメータ |
| `&` | | パラメータどうしの区切り |
| `lang=en` | 名前 `lang`、値 `en` | 2つ目のクエリパラメータ |

ネットワーク上のリクエストでは、クエリパラメータも1行目にそのまま載っています。

```text
GET /find?word=hello&lang=en HTTP/1.1
host: testserver
```

FastAPI は `?` より前の `/find` だけでエンドポイントを選び、`?` より後ろを名前ごとに分けて同じ名前の引数に入れます。

### パスパラメータとの違い

| | パスパラメータ(L3) | クエリパラメータ |
|---|---|---|
| 書く場所 | `/items/3` のパスの中 | `?q=pen` の `?` の後ろ |
| FastAPI での宣言 | パスに `{名前}` を書き、同名の引数 | 引数を書くだけ(パスには書かない) |
| よくある使い道 | 「どれか1つ」を指す(ID など) | 検索語・並べ替え・件数などの条件 |

### サンプルを1行ずつ

- `@app.get("/search")` と `def search(q: str):`: パス `/search` に `q` は出てこないので、`q` はクエリパラメータになります
- `def find(word: str, lang: str):`: クエリパラメータを2つ受け取ります。URL 上の順番は関係なく、名前で対応します
- `client.get("/search?q=fastapi")`: `q` に `"fastapi"` が入ります
- `client.get("/find?word=hello&lang=en")`: `word` に `"hello"`、`lang` に `"en"` が入ります

実行結果:

```text
{'q': 'fastapi'}
{'word': 'hello', 'lang': 'en'}
```

### 付け忘れたら

デフォルト値(次の ch02)のない引数は **必須** です。`/search` だけを送ると、関数は呼ばれずに 422 が返ります(L3 ch02 で見たエラーの形です)。

```json
{"detail":[{"type":"missing","loc":["query","q"],"msg":"Field required","input":null}]}
```

`loc` の `"query"` は「クエリパラメータの」、`msg` の `Field required` は「必須項目がありません」という意味です。なお、空白や日本語を URL に入れると `%20` や `%E6%97%A5...` のような記号に置き換えて送られます(**URL エンコード**)。受け取る FastAPI 側で元の文字に戻るので、関数の中では普通の文字列として扱えます。

## ch02 デフォルト値

引数にデフォルト値を書くと、そのクエリパラメータは省略可能になります。URL に付けなかったときはデフォルト値が使われ、付けたときはその値で上書きされます。デフォルト値のない引数は必須のままで、省略するとステータスコード 422 が返ります(ch01 の最後で見たとおりです)。🔴 「デフォルト値あり = 省略可能」のパターンは実際の API 開発でも頻出なので、繰り返し書いて覚えましょう。

```python
@app.get("/items")
def read_items(lang: str = "ja"):
    return {"lang": lang}
```

### デフォルト値とは

`lang: str = "ja"` は「`lang` は str 型、渡されなかったら `"ja"`」という意味です。`: str` が型ヒント(L3 ch02)、`= "ja"` が **デフォルト値**(省略されたときに使う値)です。これは素の Python の関数と同じ文法です。

```python
def hello(lang="ja"):
    return lang

print(hello())      # ja
print(hello("en"))  # en
```

FastAPI では、この「引数を省略」が「URL にクエリパラメータを付けない」に対応します。

| リクエスト | `lang` に入る値 | 返る JSON |
|---|---|---|
| `GET /hello` | `"ja"`(デフォルト値) | `{"message":"こんにちは"}` |
| `GET /hello?lang=en` | `"en"`(URL の値で上書き) | `{"message":"Hello"}` |
| `GET /hello?lang=fr` | `"fr"` | `{"message":"こんにちは"}`(`en` 以外なので) |

### サンプルを1行ずつ

- `def hello(lang: str = "ja"):`: `lang` を省略可能なクエリパラメータにします
- `if lang == "en":` と `return {"message": "Hello"}`: `en` のときだけ英語で返します
- `return {"message": "こんにちは"}`: それ以外(デフォルトの `ja` を含む)は日本語で返します
- `client.get("/hello")`: `?` を付けないので `lang` は `"ja"` です
- `client.get("/hello?lang=en")`: `lang` は `"en"` で上書きされます

実行結果:

```text
{'message': 'こんにちは'}
{'message': 'Hello'}
```

なお、関数の引数にない名前(例: `?x=1`)を URL に付けても、エラーにはならず無視されます。

## ch03 int 型クエリと skip/limit パターン

クエリパラメータにも `skip: int = 0` のように型ヒントが使えます(L3 ch02 のパスパラメータと同じしくみです)。URL 上では文字列の "2" でも、関数には int の 2 として渡ります。この型変換の代表的な使い道が **skip / limit パターン** です。skip は読み飛ばす件数、limit は取得する最大件数で、一覧データを少しずつ取り出すときの定番の書き方です(1ページ目、2ページ目…と分けて見せる **ページング** に使います)。🔴 リストのスライス `items[skip : skip + limit]` と組み合わせる形を、手が覚えるまで書きましょう。

```python
@app.get("/items")
def read_items(skip: int = 0, limit: int = 2):
    return items[skip : skip + limit]
```

### スライスのおさらい

`リスト[開始 : 終了]` は「開始番目から、終了番目の **手前** まで」を取り出す Python の書き方です。番号は 0 から数えます。

| 番号 | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| items | ノート | ペン | 消しゴム | 定規 | はさみ |

| リクエスト | skip | limit | スライス | 結果 |
|---|---|---|---|---|
| `/items` | 0 | 2 | `items[0:2]` | 0番・1番 |
| `/items?skip=2&limit=2` | 2 | 2 | `items[2:4]` | 2番・3番 |
| `/items?skip=4` | 4 | 2 | `items[4:6]` | 4番だけ(6番目まではないが、ある分だけ返る) |

スライスはリストの長さを超えてもエラーにならず、ある分だけを返します。そのため最後のページで件数が足りなくても安全です。

### サンプルを1行ずつ

- `items = [...]`: データの代わりのリストです。関数の外に置いているので、どのリクエストからも同じリストが見えます
- `def read_items(skip: int = 0, limit: int = 2):`: どちらも int 型・省略可能です
- `return items[skip : skip + limit]`: skip 番目から limit 件を切り出して返します。リストは JSON の配列になります(L2 ch03)
- 3つの `client.get(...)`: 上の表の3行に対応します

実行結果:

```text
['ノート', 'ペン']
['消しゴム', '定規']
['はさみ']
```

もし型ヒントを付けずに `skip=0` のようなデフォルト値だけにすると、URL から来た値は文字列 `"2"` のままになり、`"2" + 2` の計算でエラーになります。`skip: int` と書くことで、FastAPI が数値に変換してくれます。`?skip=abc` のように数値でない値は、L3 ch02 と同じく 422 になります。

## ch04 bool と None

「値があってもなくてもよい」引数は `q: str | None = None` と書きます(`str | None` は「str か None のどちらか」を表す型ヒントです。`|` は「または」の意味)。省略されると `None` になるため、`if q is None:` で「指定されなかった場合」を分岐できます。また `flag: bool = False` と書くと、URL の `?flag=true` や `?flag=1` が自動で Python の `True` に変換されます。🟡 None と bool の変換ルールを理解し、省略可能な引数を設計できるようになりましょう。

```python
@app.get("/search")
def search(q: str | None = None, sale: bool = False):
    return {"q": q, "sale": sale}
```

### None とは

`None` は Python で「値がない」ことを表す特別な値です。空文字 `""` や `0` とは別物で、JSON では `null` になります(L1 ch01 の表)。`q: str = ""` と書くこともできますが、それだと「指定されなかった」のか「空文字が指定された」のか区別できません。`None` をデフォルトにすると、省略されたことがはっきり分かります。

`is None` は「None かどうか」を調べる書き方です(`== None` ではなく `is None` と書くのが Python の決まりごとです)。

### bool に変換される文字列

URL の値はすべて文字列なので、FastAPI が次のように読み替えます(実際に試した結果です)。

| URL の値 | 関数に渡る値 |
|---|---|
| `true`, `True`, `1`, `yes`, `on` | `True` |
| `false`, `0`, `no`, `off` | `False` |
| 省略 | デフォルト値の `False` |
| `abc` など上以外 | 関数は呼ばれず 422 |

### サンプルを1行ずつ

- `def search(q: str | None = None, sale: bool = False):`: `q` は省略可・省略時 None、`sale` は省略可・省略時 False です
- `if q is None:` と `return {"q": None, "sale": sale, "hit": 0}`: 検索語がないときは hit 0 を返します
- `return {"q": q, "sale": sale, "hit": 1}`: 検索語があるときの返り値です
- `client.get("/search")`: 何も付けないので `q=None`、`sale=False` です
- `client.get("/search?q=pen&sale=true")`: 文字列 `"true"` が `True` に変換されます

実行結果:

```text
{'q': None, 'sale': False, 'hit': 0}
{'q': 'pen', 'sale': False, 'hit': 1}
{'q': 'pen', 'sale': True, 'hit': 1}
```

1行目のレスポンスのボディは、ネットワーク上では `{"q":null,"sale":false,"hit":0}` という JSON です。`r.json()` で Python に戻したので `None` と `False` で表示されています。
