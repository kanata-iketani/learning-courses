# Lesson 06 バリデーション

送られてくるデータが正しいとは限りません。このレッスンでは、型や Field・Query・Path による検証(バリデーション)と、検証に失敗したときに返る 422 エラーの仕組みを学びます。

## ch01 型による自動検証と 422

**バリデーション**とは、送られてきたデータが正しい形かを検証することです。FastAPI はモデルの型ヒントを見て自動で検証し、型に合わないデータや足りないフィールドがあると **422**(Unprocessable Entity: 処理できないデータ、という意味のステータスコード)を返します。エラーレスポンスの `detail` の `loc` を見ると、どのフィールドが原因か分かります。🟡 検証コードを 1 行も書かなくても型だけで検証される、という仕組みを理解しましょう。

```python
r = client.post("/items", json={"name": "apple", "price": "たくさん"})
print(r.status_code)  # 422
```

## ch02 Field で制約を付ける

型だけでなく「値の範囲」も検証するには、`from pydantic import Field` の **Field** を使います。`Field(gt=0)` は「0 より大きい」、`Field(max_length=10)` は「10 文字以内」という制約です。数値には gt(より大きい)・ge(以上)・lt(より小さい)・le(以下)、文字列には min_length / max_length が使えます。制約に反すると 422 が返ります。🔴 Field の書き方は実務でも頻出なので、手が覚えるまで書きましょう。

```python
class Item(BaseModel):
    name: str = Field(max_length=10)
    price: int = Field(gt=0)
```

## ch03 Query で検証する

クエリパラメータにも制約を付けられます。`from fastapi import Query` の **Query** を引数の既定値の位置に書き、`q: str = Query(min_length=2)` のように指定します。文字列には min_length / max_length、数値には ge / le などが使え、違反すると 422 が返ります。Field はボディ(モデルの中)用、Query はクエリパラメータ用、という使い分けです。🟡 「引数 = Query(制約)」という書き方のパターンを理解しましょう。

```python
@app.get("/search")
def search(q: str = Query(min_length=2)):
    return {"q": q}
```

## ch04 Path で検証する

パスパラメータの検証には `from fastapi import Path` の **Path** を使います。書き方は Query と同じで、`user_id: int = Path(ge=1)` のように既定値の位置に制約を書きます。ID のような値は「1 以上」が自然なので、`Path(ge=1)` で 0 や負の数を弾くのが定番です。違反すると 422 が返ります。🟡 「ID は Path(ge=1) で守る」というパターンを理解しましょう。

```python
@app.get("/users/{user_id}")
def get_user(user_id: int = Path(ge=1)):
    return {"user_id": user_id}
```
