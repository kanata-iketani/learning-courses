# Lesson 10 依存性注入（Depends）

複数のエンドポイントで共通する処理を、Depends で関数やクラスに切り出して再利用するレッスンです。FastAPI らしいコードの書き方の中心となる考え方で、実務では DB 接続や認証にも使われます。

## ch01 Depends とは

**Depends**(依存性注入)とは、共通処理を関数として切り出し、エンドポイントの引数に「注入」してもらうしくみです。引数に `info: dict = Depends(get_app_info)` と書くと、FastAPI がリクエストのたびに `get_app_info()` を呼び、その戻り値を `info` に入れて渡してくれます。自分で関数を呼ぶコードを書かなくてよいので、複数のエンドポイントで同じ処理をきれいに使い回せます。🟡 「FastAPI が代わりに呼んで、結果を引数に入れてくれる」という流れを理解しましょう。

```python
def get_app_info():
    return {"app_name": "メモ帳API"}

@app.get("/about")
def about(info: dict = Depends(get_app_info)):
    return info
```

### 用語: 依存・依存関数・注入

- **依存**(dependency): ある関数が動くために必要なもの。`about` は `info` がないと動けないので、「`about` は `get_app_info` の結果に依存している」と言います
- **依存関数**: その必要なものを用意する関数(ここでは `get_app_info`)。中身はふつうの Python の関数です
- **注入**(injection): 必要なものを外から引数として渡してあげること。`about` は自分で `get_app_info()` を呼ばず、FastAPI が呼んだ結果を受け取るだけです

「依存性注入」は、この「必要なものを、使う側が自分で作らずに外から渡してもらう」設計の名前です。

### Depends を使わない書き方との比較

Depends を使わなくても、関数の中で自分で呼べば同じ結果になります。

```python
@app.get("/about")
def about():
    info = get_app_info()  # 自分で呼ぶ
    return info
```

この例だけなら違いは小さいですが、Depends には「依存関数の引数もクエリパラメータとして FastAPI が受け取ってくれる」(ch02)、「依存関数の中でさらに依存を使える」(ch04)といった、自分で呼ぶ書き方にはない働きがあります。また、テストのときに依存関数だけを別のものに差し替えるしくみも FastAPI に用意されています。

### サンプルを1行ずつ

- `from fastapi import Depends, FastAPI`: `Depends` を読み込みます
- `def get_app_info():` 〜 `return {...}`: 依存関数です。アプリ名とバージョンの辞書を返します
- `def about(info: dict = Depends(get_app_info)):`: 引数 `info` の型は `dict`、既定値の位置に `Depends(get_app_info)` を書きます。`get_app_info` には `()` を付けません。「呼んだ結果」ではなく「関数そのもの」を FastAPI に渡し、呼ぶのは FastAPI に任せるからです
- `return info`: 受け取った辞書をそのまま返します
- `def status(info: dict = Depends(get_app_info)):`: 別のエンドポイントでも同じ依存関数を使えます。こちらは `info["app_name"]` だけを取り出し、`"ok": True` を足して返します

実行結果:

```text
200
{'app_name': 'メモ帳API', 'version': '1.0'}
200
{'app_name': 'メモ帳API', 'ok': True}
```

`True` は JSON では `true` になって送られ、`r.json()` で辞書に戻すと Python の `True` として表示されます(L1 ch01 で見た対応表のとおり)。

### 1回のリクエストで何が起きるか

`GET /about` が届いたときの順番は次のとおりです。

1. FastAPI がパス `/about` を見て、担当の `about` を選ぶ
2. `about` の引数に `Depends(get_app_info)` があるので、先に `get_app_info()` を呼ぶ
3. 戻り値 `{"app_name": "メモ帳API", "version": "1.0"}` を `info` に入れて `about` を呼ぶ
4. `about` の戻り値を JSON にしてレスポンスで返す

依存関数は **リクエストのたびに** 呼ばれます。試しに `get_app_info` の中に print を入れて `/about` を2回呼ぶと、print も2回出ます。

リクエストとレスポンスの見た目は、Depends を使っても変わりません。

```text
GET /about HTTP/1.1
host: testserver
```

```text
HTTP/1.1 200 OK
content-type: application/json

{"app_name":"メモ帳API","version":"1.0"}
```

Depends はサーバの中での「関数の呼び方」の工夫なので、クライアントからは見えません。

## ch02 共通クエリパラメータを Depends でまとめる

依存関数には、エンドポイントと同じ書き方でクエリパラメータを宣言できます。L4 で見た `skip`(読み飛ばす件数)や `limit`(最大件数)のように、どの一覧 API にも付けたいパラメータは 1 つの依存関数にまとめるのが定番です。各エンドポイントは `Depends(pagination)` と書くだけでよく、パラメータの既定値や型の変更も 1 か所で済みます。🟡 「クエリパラメータの宣言ごと共通化できる」ことを理解しましょう。

```python
def pagination(skip: int = 0, limit: int = 2):
    return {"skip": skip, "limit": limit}

@app.get("/fruits")
def list_fruits(page: dict = Depends(pagination)):
    return fruits[page["skip"] : page["skip"] + page["limit"]]
```

`pagination` はページ分け(一覧を少しずつ区切って返すこと)を意味する英語です。

### クエリパラメータのおさらい

L4 で見たとおり、URL の `?` より後ろの `名前=値` がクエリパラメータです。複数あるときは `&` でつなぎます。`/fruits?skip=1&limit=3` なら `skip` が `"1"`、`limit` が `"3"` で、型ヒント `int` によって整数 `1` と `3` に変換されます。

今回の新しい点は、`skip` と `limit` をエンドポイント `list_fruits` の引数ではなく、依存関数 `pagination` の引数に書いていることです。それでも FastAPI は依存関数の引数までさかのぼって調べ、クエリパラメータとして受け取ってくれます。

### スライスのおさらい

`fruits[開始 : 終了]` は、リストの「開始」番目から「終了」番目の手前までを取り出す書き方(スライス)です。番号は 0 から数えます。

| 書き方 | skip, limit | 取り出す番号 | 結果 |
|---|---|---|---|
| `fruits[0 : 0 + 2]` | 0, 2 | 0, 1 | `['りんご', 'みかん']` |
| `fruits[1 : 1 + 3]` | 1, 3 | 1, 2, 3 | `['みかん', 'ぶどう', 'もも']` |

### サンプルを1行ずつ

- `def pagination(skip: int = 0, limit: int = 2):`: クエリパラメータ `skip`(既定 0)と `limit`(既定 2)を受け取る依存関数です
- `return {"skip": skip, "limit": limit}`: 2つの値を辞書にまとめて返します
- `def list_fruits(page: dict = Depends(pagination)):`: `pagination` の戻り値の辞書が `page` に入ります
- `fruits[page["skip"] : page["skip"] + page["limit"]]`: 辞書から skip と limit を取り出してスライスします
- `list_teas` も同じ `Depends(pagination)` を使います
- `for path in [...]`: 3 つの URL に順にリクエストを送り、JSON を出します

実行結果:

```text
['りんご', 'みかん']
['みかん', 'ぶどう', 'もも']
['緑茶']
```

| URL | skip | limit | 結果 |
|---|---|---|---|
| `/fruits` | 0(既定) | 2(既定) | 先頭から2件 |
| `/fruits?skip=1&limit=3` | 1 | 3 | 1件飛ばして3件 |
| `/teas?limit=1` | 0(既定) | 1 | 先頭から1件 |

### 型の検証も効く

依存関数の引数でも、L6 で見た型による検証はそのまま効きます。`GET /fruits?limit=abc` を送ると、次のレスポンスが返ります。

```text
HTTP/1.1 422 Unprocessable Content

{"detail":[{"type":"int_parsing","loc":["query","limit"],"msg":"Input should be a valid integer, unable to parse string as an integer","input":"abc"}]}
```

`loc` が `["query","limit"]` なので、「クエリパラメータの limit が整数になっていない」と分かります。また、`/docs` の自動ドキュメントにも `skip` と `limit` がクエリパラメータとして表示されます。

## ch03 クラス依存（CommonQueryParams パターン）

依存には関数だけでなくクラスも使えます。`__init__` の引数がクエリパラメータになり、エンドポイントには生成されたインスタンスが渡ります。`params: CommonQueryParams = Depends()` のように Depends の中身を省略すると、型注釈のクラスがそのまま依存として使われます。辞書と違って `params.q` のように属性でアクセスでき、エディタの補完も効くため、公式チュートリアルでも紹介される定番の形です。🟡 関数依存との違い(戻り値が辞書 → インスタンス)を理解しましょう。

```python
class CommonQueryParams:
    def __init__(self, q: str | None = None, limit: int = 3):
        self.q = q
        self.limit = limit

@app.get("/books")
def list_books(params: CommonQueryParams = Depends()):
    ...
```

### 基礎の基礎: クラス・インスタンス・__init__・self

L5 の Pydantic でも `class` を書きましたが、ここではふつうの Python のクラスを使います。

- **クラス**: 「どんな値をひとまとめに持つか」の設計図です
- **インスタンス**: 設計図から作った実物です。`p = CommonQueryParams(q="Python")` のように、クラス名を関数のように呼ぶと作られます
- **`__init__`**(イニット): インスタンスを作るときに自動で呼ばれる特別なメソッド(クラスの中の関数)です。前後の `__` は Python が特別扱いする名前の印です
- **`self`**: 今作っているインスタンス自身を指す引数です。呼ぶ側は渡さず、Python が自動で入れます
- **属性**: `self.q = q` のようにインスタンスに保存した値です。あとで `p.q` のように `.` で取り出せます

```python
p = CommonQueryParams(q="Python")
print(p.q)      # Python
print(p.limit)  # 3 (既定値)
```

### FastAPI がしていること

`Depends()` と書くと、FastAPI は次のように動きます。

1. 型注釈 `CommonQueryParams` を見て、これを依存として使うと決める
2. `__init__` の引数 `q`・`skip`・`limit` を調べ、クエリパラメータとして URL から受け取る
3. `CommonQueryParams(q=..., skip=..., limit=...)` を呼んでインスタンスを作る
4. そのインスタンスを `params` に入れてエンドポイントを呼ぶ

`Depends(CommonQueryParams)` と書いても同じ意味です。型注釈と同じクラス名を2回書くのを省ける、というのが `Depends()` の省略形です。

### 関数依存との違い

| | ch02 の関数依存 | ch03 のクラス依存 |
|---|---|---|
| 受け取る値 | 辞書 `{"skip": 1, "limit": 3}` | インスタンス |
| 取り出し方 | `page["skip"]` | `params.skip` |
| 書き間違えたとき | `page["skpi"]` は実行するまで気づけない | エディタが `params.skpi` を「ない属性」として指摘できる |

### サンプルを1行ずつ

- `def __init__(self, q: str | None = None, skip: int = 0, limit: int = 3):`: `q` は L4 で見た「文字列か None」の省略可能なパラメータ、`skip` と `limit` は整数です
- `self.q = q` など3行: 受け取った値をインスタンスに保存します
- `def list_books(params: CommonQueryParams = Depends()):`: インスタンスが `params` に入ります
- `result = books`: まず全件を `result` に入れます
- `if params.q is not None:`: `is not None` は「None ではない」、つまり `?q=...` が指定されたかどうかの判定です
- `result = [b for b in result if params.q in b]`: **リスト内包表記**(for と if を1行にまとめてリストを作る書き方)です。「`result` の各要素 `b` のうち、`params.q` を含むものだけを集める」という意味です。文字列どうしの `in` は「含まれているか」の判定で、`"Python" in "Python入門"` は True です
- `return result[params.skip : params.skip + params.limit]`: ch02 と同じスライスで件数を絞ります

リスト内包表記は、次の for 文と同じ結果になります。

```python
new = []
for b in result:
    if params.q in b:
        new.append(b)
result = new
```

実行結果:

```text
['Python入門', 'Python実践', 'FastAPI入門']
['Python入門', 'Python実践']
['Python入門']
```

| URL | q | 絞り込み後 | skip, limit | 結果 |
|---|---|---|---|---|
| `/books` | None | 4件そのまま | 0, 3 | 先頭3件 |
| `/books?q=Python` | `"Python"` | `Python入門`・`Python実践` | 0, 3 | 2件(3件に満たない) |
| `/books?q=Python&limit=1` | `"Python"` | 同上 | 0, 1 | 1件 |

`"FastAPI入門"` に `"Python"` は含まれないので、2行目では外れます。大文字・小文字も区別されます。

## ch04 依存の中の依存（ネスト）と使いどころ

依存関数は、自分の引数にさらに `Depends` を書けます(依存のネスト。依存の中に依存が入れ子になること)。FastAPI が奥から順に解決してくれるので、エンドポイント側は一番外側の 1 つを書くだけで済みます。実務では「設定の読み込み → DB(データベース)への接続 → ログイン中ユーザの取得」のように、共通処理を段階的に積み上げる形で使われます。⚪ 今は「依存はネストでき、FastAPI が順に解決してくれる」と知っていれば十分です。

```python
def get_settings():
    return {"shop": "demo堂"}

def get_greeting(settings: dict = Depends(get_settings)):
    return f"ようこそ {settings['shop']} へ"

@app.get("/welcome")
def welcome(greeting: str = Depends(get_greeting)):
    return {"message": greeting}
```

### 解決の順番

「解決する」とは、依存関数を呼んで値を用意することです。`GET /welcome` が届くと、FastAPI は次の順に動きます。

1. `welcome` は `get_greeting` の結果が必要 → でも `get_greeting` は `get_settings` の結果が必要
2. いちばん奥の `get_settings()` を呼ぶ → `{"shop": "demo堂"}`
3. その辞書を `settings` に入れて `get_greeting(settings)` を呼ぶ → `"ようこそ demo堂 へ"`
4. その文字列を `greeting` に入れて `welcome(greeting)` を呼ぶ → `{"message": "ようこそ demo堂 へ"}`

図にすると次の関係です(矢印は「値を渡す向き」)。

```text
get_settings ──> get_greeting ──> welcome
 {"shop": ...}    "ようこそ ..."    {"message": ...}
```

自分で書くとすれば `welcome(get_greeting(get_settings()))` という順番の呼び出しを、FastAPI が代わりにしてくれていることになります。

### サンプルを1行ずつ

- `def get_settings():`: 1段目の依存関数。設定の辞書を返します
- `def get_greeting(settings: dict = Depends(get_settings)):`: 2段目。引数に `Depends(get_settings)` を書いているので、`get_settings` の戻り値が `settings` に入ります
- `return f"ようこそ {settings['shop']} へ"`: f-string の `{}` の中で辞書の値を取り出しています。外側の文字列が `"` で囲まれているので、中のキーは `'shop'` とシングルクォートにしています(同じ `"` を使うと文字列がそこで終わったと解釈されるため)
- `def welcome(greeting: str = Depends(get_greeting)):`: エンドポイントは一番外側の `get_greeting` だけを指定します。`get_settings` のことは書きません
- `return {"message": greeting}`: 文字列を辞書に入れて返します

実行結果:

```text
200
{'message': 'ようこそ demo堂 へ'}
```

### 使いどころ

ネストの利点は、段ごとに役割を分けられることです。たとえば店名を変えたいときは `get_settings` の1か所だけを直せば、それを使う `get_greeting`、さらにそれを使うすべてのエンドポイントに反映されます。この講座ではデータベースやログインは扱いませんが、実際の FastAPI アプリでは「DB への接続を用意する依存関数」や「リクエストに付いた情報からログイン中のユーザを調べる依存関数」をこの形で積み上げるのが一般的です。
