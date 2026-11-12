# Lesson 11 ルーター分割と非同期

アプリが大きくなったときにエンドポイントを APIRouter でグループ分けする方法と、async def による非同期エンドポイントを学ぶレッスンです。実際の開発でプロジェクトを整理するときに必要になる知識です。

## ch01 APIRouter でエンドポイントをまとめる

**APIRouter**(エーピーアイ・ルーター)とは、エンドポイントをグループにまとめるための部品です。実際の開発では `users.py`・`items.py` のようにファイルを分け、各ファイルで `router = APIRouter()` を作って `@router.get(...)` を書き、最後にアプリ本体で `app.include_router(router)` として合体させます。`@app.get` を直接書いたときと動きは同じで、置き場所を整理できるのが利点です。この演習では 1 ファイル内で同じ形を作ります。🟡 「router に登録 → include_router で合体」という流れを理解しましょう。

```python
router = APIRouter()

@router.get("/items")
def list_items():
    return ["ペン", "ノート"]

app = FastAPI()
app.include_router(router)
```

### なぜファイルを分けたいのか

これまでの演習はエンドポイントが 1〜3 個でしたが、実際のアプリでは数十〜数百になります。全部を `main.py` 1 つに書くと、目的の関数を探すのも、複数人で同時に直すのも大変です。そこで「商品まわり」「ユーザまわり」のように担当ごとにファイルを分けます。ファイルを分けると、別ファイルの `app` に直接 `@app.get` を書けないので、各ファイルでは router に登録しておき、最後に `main.py` でまとめます。

ファイルを分けたときの構成の例です。

```python
# items.py
from fastapi import APIRouter
router = APIRouter()

@router.get("/items")
def list_items():
    return ["ペン", "ノート"]
```

```python
# main.py
from fastapi import FastAPI
import items                      # items.py を読み込む

app = FastAPI()
app.include_router(items.router)  # items.py の router を合体
```

### 用語

- **ルーター**(router): 「このパスはこの関数へ」という対応表(ルーティング)を持つ部品です。`app` も内部に1つ持っています
- **include_router**: router に登録された対応表を、`app` の対応表にまるごと書き写す命令です。include は「含める」という意味です

### サンプルを1行ずつ

- `from fastapi import APIRouter, FastAPI`: `APIRouter` を読み込みます
- `router = APIRouter()`: 空の router を1つ作ります
- `@router.get("/items")`: `@app.get` と同じ書き方で、router に「GET /items はこの関数」と登録します。この時点ではまだ `app` には登録されていません
- `return list(items.values())`: `items.values()` は辞書の値だけを取り出します(`"ペン"`, `"ノート"`)。それを `list()` でリストにして返します
- `@router.get("/items/{item_id}")`: L3 で見たパスパラメータも、router でそのまま使えます
- `app = FastAPI()` と `app.include_router(router)`: アプリを作り、router の中身を合体させます。ここで初めて `GET /items` などが `app` から呼べるようになります

実行結果:

```text
200
['ペン', 'ノート']
{'name': 'ペン'}
```

リクエストとレスポンスの実物は、`@app.get` で書いたときと全く同じです。

```text
GET /items HTTP/1.1
host: testserver
```

```text
HTTP/1.1 200 OK
content-type: application/json

["ペン","ノート"]
```

### include_router を忘れると

`app.include_router(router)` を書き忘れると、router に登録しただけで `app` には何も登録されていない状態になります。そのため `GET /animals` などを送っても、L9 で見た `404` と `{"detail":"Not Found"}` が返ります。エラー表示は出ないので、404 になったらまず include_router を確認しましょう。

## ch02 prefix と tags

APIRouter には **prefix**(プレフィックス。その router の全パスに付く共通の接頭辞)と **tags**(タグ。自動ドキュメント /docs でのグループ名)を指定できます。`APIRouter(prefix="/items", tags=["items"])` とすると、router 側は `"/"` や `"/{item_id}"` と書くだけで実際のパスは `/items/`・`/items/{item_id}` になります。パスの書き間違いが減り、/docs もグループごとに整理されます。🟡 「router 内のパス + prefix = 実際のパス」という対応を理解しましょう。

```python
router = APIRouter(prefix="/items", tags=["items"])

@router.get("/")          # 実際は GET /items/
def list_items(): ...

@router.get("/{item_id}")  # 実際は GET /items/{item_id}
def read_item(item_id: int): ...
```

### prefix は文字列をつなげるだけ

prefix は、router に書いたパスの前に文字列としてそのままくっつきます。

| prefix | router に書いたパス | 実際のパス |
|---|---|---|
| `/items` | `/` | `/items/` |
| `/items` | `/{item_id}` | `/items/{item_id}` |
| `/users` | `/{user_id}/orders` | `/users/{user_id}/orders` |

商品まわりのエンドポイントがすべて `/items` で始まるなら、それを1か所にまとめて書けるわけです。あとで `/products` に変えたくなっても、prefix の1行を直すだけで済みます。

### tags とは

`tags=["items"]` は、L1 で見た `/docs`(Swagger UI)の画面で、この router のエンドポイントを「items」という見出しの下にまとめて表示するための名前です。リストなので複数付けることもできます。tags はドキュメントの見た目だけに関わり、パスやレスポンスは変わりません。

### サンプルを1行ずつ

- `router = APIRouter(prefix="/items", tags=["items"])`: prefix と tags をキーワード引数で指定して router を作ります
- `@router.get("/")`: 実際のパスは `/items/` です。最後の `/` まで含まれる点に注意します
- `@router.get("/{item_id}")`: 実際のパスは `/items/{item_id}` です
- `app.include_router(router)`: ch01 と同じく合体させます
- `client.get("/items/")` と `client.get("/items/2")`: prefix 込みの実際のパスで呼び出します
- `print(sorted(app.openapi()["paths"].keys()))`: `app.openapi()` は /docs の元になる API の説明データ(辞書)を返します。その `"paths"` のキーが、登録されている実際のパスの一覧です。`sorted()` で並べ替えて表示しています

実行結果:

```text
200
['ペン', 'ノート']
{'name': 'ノート'}
['/items/', '/items/{item_id}']
```

最終行から、prefix が付いた形で登録されていることを確かめられます。

### 末尾の `/` があるときとないとき

登録されたパスは `/items/`(末尾に `/` あり)です。ここに `GET /items`(末尾の `/` なし)を送ると、FastAPI は次のレスポンスを返します。

```text
HTTP/1.1 307 Temporary Redirect
location: http://testserver/items/
content-length: 0
```

**307 Temporary Redirect** は「別の場所へ行き直してください」という意味のステータスコードで、`location` ヘッダに行き先が入っています。TestClient やブラウザはこれを受け取ると自動で `/items/` にリクエストを送り直すので、最終的には 200 が返ります。ただし通信が1往復増えるので、演習では最初から `/users/` のように末尾の `/` まで正しく書きます。

## ch03 async def エンドポイント

エンドポイントは **async def**(非同期関数)でも定義できます。非同期関数の中では **await**(処理の完了を待つ間、他の処理に順番を譲る文)が使え、DB(データベース)や外部 API の応答待ちの間に別のリクエストを処理できるのが利点です。await できるのは非同期対応の関数(async def で定義されたものなど)だけです。呼び出す側から見た動きは同期の `def` と同じで、TestClient もそのまま呼べます。🟡 「async def の中で await で待つ」という形を理解しましょう。

```python
@app.get("/async")
async def read_async():
    msg = await load_message()  # 待っている間、他のリクエストを処理できる
    return {"message": msg}
```

### 基礎の基礎: 同期と非同期

- **同期**: 1つの処理が終わるまで、次の処理に進まないやり方です。ふつうの `def` の関数はこれです
- **非同期**: 待ち時間のある処理(ネットワークの応答待ちなど)の間、ほかの処理を先に進めるやり方です

Web サーバの仕事の多くは「待ち」です。たとえば外部の API に問い合わせて答えが返るまでの 1 秒間、CPU(計算をする部品)はほぼ何もしていません。この待ち時間に別のリクエストを処理できれば、同じサーバで多くのリクエストをさばけます。

### イベントループと await

非同期の処理は **イベントループ**(非同期関数を順番に少しずつ進める、まとめ役のしくみ)が動かします。FastAPI を動かす uvicorn が、このイベントループを1つ持っています。

1. イベントループがリクエスト A の `async def` 関数を進める
2. 関数が `await`(待ちの入る処理)に来ると、そこで一時停止してイベントループに順番を返す
3. イベントループはその間にリクエスト B の関数を進める
4. A の待っていた処理が終わると、A の続き(`await` の次の行)から再開する

`await` は「ここで待つけれど、待っている間はほかの人に順番を譲る」という印です。

### async def で作った関数の性質

`async def` で定義した関数は、呼んだだけでは中身が実行されません。`load_message()` とだけ書いて print すると、次のように **コルーチン**(非同期関数を呼んだときに返る「まだ実行されていない処理」を表す値)が表示されます。

```text
<coroutine object load_message at 0x...>
```

`await load_message()` と書いて初めて中身が実行され、戻り値 `"非同期で取得しました"` が得られます。`await` を付け忘れると、文字列ではなくこのコルーチンが変数に入ってしまうので注意します。また、`await` は `async def` の中でしか書けません。ふつうの `def` の中で書くと SyntaxError(文法エラー)になります。

### サンプルを1行ずつ

- `async def load_message():`: 非同期の部品関数です。本物のアプリではここで DB や外部 API に問い合わせて `await` で待ちますが、サンプルでは文字列を返すだけにしています
- `@app.get("/async")` と `async def read_async():`: エンドポイントも `async def` で定義できます。デコレータの書き方は変わりません
- `msg = await load_message()`: `load_message` を実行して、その結果(文字列)を `msg` に入れます
- `return {"message": msg}`: いつもどおり辞書を返します
- `def read_sync():`: 比べるための同期版です
- `for path in ["/async", "/sync"]:`: 両方に GET を送ります。TestClient の呼び方は `async` でも変わりません(TestClient の中でイベントループが用意されます)

実行結果:

```text
200
{'message': '非同期で取得しました'}
200
{'message': '同期で取得しました'}
```

リクエストとレスポンスの形も、`def` のときと全く同じです。

```text
HTTP/1.1 200 OK
content-type: application/json

{"message":"非同期で取得しました"}
```

async かどうかはサーバの中の処理の進め方の違いで、クライアントからは区別できません。

## ch04 def と async def の使い分け

使い分けの目安は 2 つだけです。(1) `await` したい非同期対応ライブラリ(httpx など)を使うなら `async def`。(2) 同期ライブラリ(多くの DB ドライバなど)を使う、または迷ったら `def`。`def` のエンドポイントは FastAPI が別スレッドで実行してくれるため、遅い同期処理があっても全体は止まりません。逆に `async def` の中で同期の重い処理を書くと全体が止まるので注意が必要です。⚪ 今はこの目安の存在だけ知っていれば十分です。

```python
@app.get("/a")
def sync_endpoint():        # 同期ライブラリを使う・迷ったらこちら
    ...

@app.get("/b")
async def async_endpoint():  # await を使うならこちら
    ...
```

### 用語

- **ライブラリ**: 他の人が作った、import して使う部品集です。**httpx** は外部の API にリクエストを送るライブラリで、`await` で使える非同期版を持っています(TestClient も内部で httpx を使っています)
- **DB ドライバ**: Python からデータベースに接続するためのライブラリです。多くは同期で作られています
- **スレッド**: 1つのプログラムの中で、同時に並んで動ける処理の流れです。**スレッドプール** は、あらかじめ用意しておいた複数のスレッドの置き場で、仕事が来たら空いているスレッドに割り当てます
- **ブロッキング**: 処理が終わるまでその場で止まり、ほかに順番を譲らないことです。`time.sleep(1)`(1秒何もせず止まる)や同期の DB 問い合わせがこれにあたります

### FastAPI が def と async def をどう動かすか

| 書き方 | FastAPI の動かし方 |
|---|---|
| `def` | スレッドプールの別スレッドで実行する。中でブロッキングしても、止まるのはそのスレッドだけで、イベントループ(L11 ch03)は止まらない |
| `async def` | イベントループの上で直接実行する。`await` の所で順番を譲るが、ブロッキングする処理を書くとイベントループごと止まり、その間ほかのリクエストが進まない |

### 実際に測った例

1秒かかる処理を持つエンドポイントを3種類作り、それぞれに同時に 3 つのリクエストを送って、全部終わるまでの時間を測りました。

| エンドポイントの中身 | 3 つ同時に送ったときの時間 |
|---|---|
| `def` + `time.sleep(1)` | 約 1.0 秒(3 つのスレッドで並んで待つ) |
| `async def` + `time.sleep(1)` | 約 3.0 秒(イベントループが止まり、1 つずつ順番になる) |
| `async def` + `await asyncio.sleep(1)` | 約 1.0 秒(待つ間に順番を譲るので並んで待てる) |

`asyncio.sleep` は「順番を譲りながら待つ」非同期版の sleep です。2 行目のように「`async def` の中で同期のブロッキング処理を書く」のが、いちばん避けたい書き方です。

### サンプルを1行ずつ

- `@app.get("/double/{n}")` と `def double(n: int):`: 同期のエンドポイントです。FastAPI がスレッドプールで実行します
- `return {"result": n * 2}`: `n` を 2 倍して返します
- `async def calc_triple(n: int):`: 非同期の部品関数です
- `async def triple(n: int):` と `result = await calc_triple(n)`: `await` を使いたいので `async def` にしています
- `for path in ["/double/4", "/triple/4"]:`: 両方を呼びます。呼び出す側から見た違いはありません

実行結果:

```text
200
{'result': 8}
200
{'result': 12}
```

### この講座での目安

この講座の演習はすべて一瞬で終わる処理なので、`def` でも `async def` でも結果は同じです。迷ったら `def` にしておけば、ブロッキングする処理を書いてしまってもスレッドプールのおかげで全体は止まりません。`async def` を選ぶのは、中で `await` を使うときです。
