# Lesson 01 FastAPIとは

FastAPI を学ぶ前に、Web API・JSON・HTTP という土台を押さえるレッスンです。Python 入門で学んだ辞書やリストが、そのまま API のデータになります。

## ch01 Web APIとは

**Web API** とは、プログラム同士が HTTP(ブラウザと同じ通信のしくみ)でデータをやり取りするための窓口です。ブラウザが人間に HTML を返すのに対し、API はプログラムに **JSON**(辞書や配列をテキストにした形式)を返します。FastAPI は、この API を Python で最速レベルに簡単に作れるフレームワークです。🟡 まずは「API = リクエストを受けて JSON を返すもの」という全体像を理解しましょう。

Python の辞書はこう書きました:

```python
user = {"name": "demo", "age": 13}
```

API はこれを JSON 文字列にして返します:

```json
{"name": "demo", "age": 13}
```

## ch02 FastAPIと自動ドキュメント

作った FastAPI アプリは、**uvicorn**(FastAPI アプリを動かすためのサーバプログラム)で起動します。

```sh
uvicorn main:app --reload
```

`main:app` は「main.py の中の `app` という変数」という意味で、`--reload` はコードを保存するたびに自動で再起動するオプションです。起動中にブラウザで `http://127.0.0.1:8000/docs` を開くと、**Swagger UI** という画面が表示されます。これは FastAPI がコードから自動生成する API ドキュメントで、定義した API を画面上から試すこともできます。コードを書くだけでドキュメントまで手に入るのが FastAPI の大きな特長です。🟡 この学習画面ではサーバを起動できないため、演習では次章で学ぶ TestClient を使って API を呼び出します。

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

🔴 この「アプリ定義 → TestClient → print」の流れは全レッスンで使うので、手が覚えるまで書いて身につけましょう。
