# Lesson 03 パスパラメータ

URL の一部を変数として受け取る「パスパラメータ」を学ぶレッスンです。型ヒントによる自動変換と 422 エラー、固定パスと可変パスの定義順序まで、URL 設計の基本を身につけます。

## ch01 {item_id} で受け取る

URL の一部を変数として受け取る仕組みが **パスパラメータ** です。パスの中に `{item_id}` のように波かっこで書くと、その部分の値が同じ名前の引数として関数に渡されます。`/items/1` でも `/items/abc` でも同じ関数が呼ばれるため、「商品 ID ごとの URL」を1つの関数で処理できます。型ヒントを付けない場合、値は文字列 (str) のまま渡されます。🔴 「パスの `{名前}` = 関数の引数」という対応を、何度も書いて覚えましょう。

```python
@app.get("/items/{item_id}")
def read_item(item_id):
    return {"item_id": item_id}
```

## ch02 型ヒントで int 変換

引数に `item_id: int` と型ヒントを付けると、FastAPI がパスパラメータを自動で int に変換します。`/items/3` なら数値の `3` が渡り、そのまま計算に使えます。数値にできない `/items/abc` のようなリクエストには、FastAPI が自動でステータスコード **422**(送られてきた値が処理できないことを表すエラー)を返し、理由も JSON で知らせてくれます。自分でエラー処理を書く必要はありません。🔴 型ヒント1つで「変換」と「検証」の両方が付くことを、手を動かして確かめましょう。

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "double": item_id * 2}
```

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
