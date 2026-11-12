# Lesson 01 FastAPIとは

FastAPI を学ぶ前に、Web API・JSON・HTTP という土台を押さえるレッスンです。Python 入門で学んだ辞書やリストが、そのまま API のデータになります。

## ch01 Web APIとは

**Web API** とは、プログラム同士が HTTP(ブラウザと同じ通信のしくみ)でデータをやり取りするための窓口です。ブラウザが人間に HTML(画面を組み立てるための文書)を返すのに対し、API はプログラムに **JSON**(辞書や配列をテキストにした形式)を返します。FastAPI は、この API を Python で簡単に作れるフレームワーク(土台になる道具一式)です。🟡 まずは「API = リクエストを受けて JSON を返すもの」という全体像を理解しましょう。

### 基礎の基礎: クライアントとサーバ

通信には2つの役があります。

- **クライアント**: 「これをください」と頼む側。ブラウザ、スマホアプリ、別のプログラムなど
- **サーバ**: 頼まれて答えを返す側。この講座で FastAPI を使って作るのはこちらです

クライアントが送る頼みごとを **リクエスト**、サーバが返す答えを **レスポンス** と呼びます。1回のやり取りは必ず「リクエスト1つ → レスポンス1つ」の組です。

### HTTP のリクエストとレスポンスの実物

HTTP のやり取りは、実はただのテキストです。たとえばクライアントが「`/users/1` の情報をください」と頼むと、次のような文字がサーバに届きます。

```text
GET /users/1 HTTP/1.1
host: example.com
accept: */*
```

- 1行目 `GET` は **メソッド**(何をしたいか。GET は「取得したい」)
- `/users/1` は **パス**(どの情報か。住所のようなもの)
- `HTTP/1.1` は使う HTTP のバージョン
- 2行目以降は **ヘッダ**(付け足しの情報。`名前: 値` の形)

サーバはこう答えます。

```text
HTTP/1.1 200 OK
content-type: application/json
content-length: 24

{"name":"demo","age":13}
```

- 1行目の `200` は **ステータスコード**(結果を表す3桁の数字。200 は「成功」)
- `content-type: application/json` は「本文は JSON です」という目印
- `content-length: 24` は本文の長さ(バイト数)
- 空行のあとが **ボディ**(本文)。ここに JSON が入ります

この講座では、ステータスコードとボディ(JSON)を毎回 print して確かめていきます。

### JSON とは

JSON は Python の辞書・リストとほぼ同じ見た目のテキストです。Python の辞書はこう書きました。

```python
user = {"name": "demo", "age": 13}
```

API はこれを JSON 文字列にして返します。

```json
{"name": "demo", "age": 13}
```

見た目は同じでも、Python の辞書は「プログラムの中の値」、JSON は「ただの文字列」です。ネットワークには文字しか流せないので、送る前に辞書 → 文字列へ、受け取ったら文字列 → 辞書へ変換します。細かい違いもあります。

| Python | JSON |
|---|---|
| `True` / `False` | `true` / `false` |
| `None` | `null` |
| `'a'`(シングルクォートも可) | `"a"`(ダブルクォートのみ) |
| リスト `[1, 2]`、タプル `(1, 2)` | 配列 `[1, 2]` |

### サンプルを1行ずつ

- `import json`: JSON を扱う標準ライブラリ(Python に最初から入っている部品)を読み込みます
- `text = json.dumps(user, ensure_ascii=False)`: 辞書 `user` を JSON 文字列に変換します。`ensure_ascii=False` を付けないと、日本語が `"コー..."` のような記号の列(エスケープ)になります
- `print(type(text))`: `type()` は値の種類(型)を調べる関数です。`<class 'str'>` と出れば文字列です
- `data = json.loads(text)`: JSON 文字列を辞書に戻します(dumps の逆)。戻したので `data["name"]` で値を取り出せます

実行結果:

```text
{"name": "demo", "age": 13}
<class 'str'>
demo
<class 'dict'>
```

1行目と2行目から「JSON は str(文字列)」、4行目から「loads すると dict(辞書)に戻る」ことが分かります。

## ch02 FastAPIと自動ドキュメント

作った FastAPI アプリは、**uvicorn**(ユービコーン。FastAPI アプリを動かすためのサーバプログラム)で起動します。FastAPI 自体は「リクエストを受けたらどの関数を呼ぶか」を決める部品で、ネットワークからリクエストを受け取る係は uvicorn が担当します。

```sh
uvicorn main:app --reload
```

| 部分 | 意味 |
|---|---|
| `uvicorn` | 起動するプログラムの名前 |
| `main:app` | 「main.py の中の `app` という変数」。`:` の左がファイル名(.py は省く)、右が変数名 |
| `--reload` | コードを保存するたびに自動で再起動するオプション(開発中だけ使う) |

起動すると、次のような表示が出て待ち受け状態になります。

```text
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

`127.0.0.1` は「自分自身のパソコン」を表す特別な住所(IP アドレス)、`8000` は **ポート番号**(1台のパソコンの中で、どのプログラム宛ての通信かを区別する番号)です。つまり「自分のパソコンの 8000 番で待っている」という意味です。

この状態でブラウザで `http://127.0.0.1:8000/docs` を開くと、**Swagger UI**(スワッガー・ユーアイ)という画面が表示されます。これは FastAPI がコードから自動生成する API ドキュメント(どんなパスがあり、何を送ると何が返るかの説明書)で、画面上のボタンから実際にリクエストを送って試すこともできます。コードを書くだけで説明書まで手に入るのが FastAPI の大きな特長です。🟡 この学習画面ではサーバを起動できないため、演習では次章で学ぶ TestClient を使って API を呼び出します。

### サンプルを1行ずつ

- `from fastapi import FastAPI`: fastapi パッケージから `FastAPI` クラス(アプリの設計図)を読み込みます
- `from fastapi.testclient import TestClient`: 動作確認用の `TestClient` を読み込みます
- `app = FastAPI()`: アプリ本体を1つ作り、変数 `app` に入れます。`uvicorn main:app` の `app` はこれのことです
- `@app.get("/")`: すぐ下の関数を「GET メソッドで パス `/` に来たリクエストの担当」として登録します。`@` で始まる行は **デコレータ** と呼ばれ、詳しくは L2 で見ます
- `def read_root():` から `return {"message": "Hello FastAPI"}`: 担当の関数です。辞書を return すると、FastAPI が自動で JSON に変換してレスポンスのボディにします
- `client = TestClient(app)`: `app` にリクエストを送るためのクライアント(頼む側)を作ります
- `r = client.get("/")`: GET `/` のリクエストを送り、返ってきたレスポンスを `r` に入れます
- `print(r.status_code)`: ステータスコード(L1 ch01 で見た 3桁の数字)を出します
- `print(r.json())`: ボディの JSON を辞書に戻して出します(ch01 の `json.loads` と同じことを自動でしてくれます)

実行結果:

```text
200
{'message': 'Hello FastAPI'}
```

2行目がシングルクォート `'` なのは、`r.json()` が Python の辞書に戻した値を print しているからです。実際にネットワークを流れたボディは `{"message":"Hello FastAPI"}` という JSON 文字列です。このときのやり取りの実物は次のとおりです(TestClient が送るリクエストの宛先は `testserver` という仮の名前になります)。

```text
GET / HTTP/1.1
host: testserver
```

```text
HTTP/1.1 200 OK
content-type: application/json
content-length: 27

{"message":"Hello FastAPI"}
```

uvicorn で起動した本物のサーバに送った場合も中身は同じで、`date`(送った日時)や `server: uvicorn` といったヘッダが少し増えるだけです。

## ch03 この講座の学び方

この講座の演習では **TestClient**(サーバを起動せずに、アプリへ直接リクエストを送れるテスト用クライアント)を使います。uvicorn で起動した実サーバに送るのと同じリクエストを `client.get("/")` の1行で再現できるため、「▶ 実行」だけで API の動きを確認できます。演習はすべて次の定型で書きます。

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()             # 1. アプリを定義する
# (パスと関数をここに書く)

client = TestClient(app)    # 2. テスト用クライアントを作る
print(client.get("/").json())  # 3. 呼び出して結果を print する
```

### 3つの部分の役割

| 部分 | やっていること | 本物の Web サービスでいうと |
|---|---|---|
| 1. アプリ定義 | どのパスにどの関数が答えるかを決める | サーバ側のプログラム |
| 2. TestClient | `app` に話しかける相手を用意する | ブラウザやスマホアプリ |
| 3. print | 返ってきたレスポンスを画面に出す | 受け取った結果を画面に表示する |

1つのファイルの中に「サーバ」と「クライアント」の両方がいる、というのがこの定型の特徴です。

### `client.get("/").json()` の読み方

3. の1行は、左から順に処理されます。

1. `client.get("/")`: GET `/` のリクエストを送り、レスポンスの入れ物(Response オブジェクト)を返す
2. `.json()`: そのレスポンスのボディ(JSON 文字列)を辞書に戻す
3. `print(...)`: その辞書を表示する

`r = client.get("/")` と一度変数に入れてから `r.status_code` と `r.json()` を別々に print する書き方(サンプルの書き方)と、意味は同じです。ステータスコードも見たいときは変数に入れる書き方が便利です。

### 採点のしくみ

「▶ 実行」を押すと、書いたコードが Python で実行され、print された文字(標準出力)が「期待出力」と1文字ずつ比べられます。行末の空白は無視されますが、引用符 `'` と `"` の違い・行の順番の違いは不一致になります。また、エラー(赤い文字で出る Traceback)が出た場合も不合格です。print する内容と順番は問題文のとおりにします。

### サンプルの実行結果

サンプルは GET `/` で `{"lesson": 1, "chapter": 3}` を返すアプリを作り、ステータスコードと JSON を順に print しています。

```text
200
{'lesson': 1, 'chapter': 3}
```

🔴 この「アプリ定義 → TestClient → print」の流れは全レッスンで使うので、手が覚えるまで書いて身につけましょう。
