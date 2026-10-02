# Lesson 05 リクエストボディとPydantic

クライアントからサーバへデータを送るには、リクエストボディ(送信データ本体)を使います。このレッスンでは、Pydantic の BaseModel で「受け取るデータの形」を宣言し、POST でボディを受け取って使う方法を学びます。

## ch01 Pydantic の BaseModel

**Pydantic**(パイダンティック)とは、データの形を宣言してチェックする Python ライブラリで、FastAPI に組み込まれています。`BaseModel` を継承したクラスに「フィールド名: 型」を並べると、それが「受け取るデータの形」の宣言になります。関数の引数にこのクラスを型として指定すると、FastAPI は送られてきた JSON をモデルのインスタンスに変換してくれます。🔴 モデル定義はこの先ずっと使うので、手が覚えるまで書きましょう。

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
```

## ch02 POST でボディを受け取る

**リクエストボディ**とは、リクエストに載せて送るデータ本体のことです。データを新しく作る・登録するときは **POST**(データ送信用の HTTP メソッド)を使い、ボディに JSON を入れて送ります。TestClient では `client.post(URL, json=辞書)` と書くと、辞書が JSON のボディとして送られます。なお、POST 用の URL を GET で呼ぶと 405(メソッド不一致)が返ります。🔴 `client.post(json=...)` の形は何度も書いて覚えましょう。

```python
r = client.post("/echo", json={"text": "こんにちは"})
```

## ch03 モデルの属性を使う

受け取ったモデルは普通の Python オブジェクトです。値は `order.price` のように**属性**(ドットでアクセスする値)として取り出し、計算や加工に使えます。辞書のように `order["price"]` とは書けない点に注意してください。型ヒントどおりの型であることが保証されているので、そのまま安心して計算に使えます。🔴 「属性で取り出す → 計算する → 辞書で返す」の流れを、手が覚えるまで書きましょう。

```python
@app.post("/orders")
def create_order(order: Order):
    total = order.price * order.quantity
    return {"item": order.item, "total": total}
```

## ch04 model_dump とレスポンス

`model_dump()` は、モデルを Python の辞書に変換するメソッドです(Pydantic v2 の書き方。古い `dict()` は使いません)。モデルには後からキーを追加できませんが、辞書にすればできます。レスポンスに ID や計算結果などのキーを足したいときは、「いったん辞書にしてからキーを足す」のが定石です。🟡 「モデル → 辞書 → 加工して返す」という流れを理屈で理解しましょう。

```python
data = item.model_dump()  # モデル → 辞書
data["id"] = 1            # 辞書ならキーを追加できる
```
