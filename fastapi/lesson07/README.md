# Lesson 07 レスポンスモデルとステータスコード

API が「何を返すか」を設計するレッスンです。response_model でレスポンスの形を宣言して見せたくない情報を隠し、201 などのステータスコードで処理結果の意味を正しく伝えます。

## ch01 response_model の指定

**response_model** とは、デコレータに指定する「レスポンスの形」の宣言です。`@app.get("/items/1", response_model=Item)` のように書くと、関数が返した値は Item の形に整えられ、モデルにないキーは自動で取り除かれます。返す形が明文化されるので、API の仕様がコードから読み取れるようになります。🔴 response_model の指定は基本の型として手が覚えるまで書きましょう。

```python
@app.get("/items/1", response_model=Item)
def get_item():
    return {"name": "apple", "price": 120, "secret": "内部情報"}
    # → レスポンスは {"name": "apple", "price": 120}
```

## ch02 見せたくない項目を隠す

パスワードのような秘密の値は、レスポンスに絶対に含めてはいけません。定石は、**入力用モデル**(パスワードあり)と**出力用モデル**(パスワードなし)の 2 つに分け、`response_model` に出力用を指定することです。関数が入力用モデルをそのまま返しても、レスポンスは出力用の形に絞られ、パスワードは消えます。🔴 「入力用と出力用を分ける」設計は Web API の必須知識なので、必ず書けるようにしましょう。

```python
@app.post("/users", response_model=UserOut)
def create_user(user: UserIn):
    return user  # password は UserOut にないので消える
```

## ch03 status_code=201 の指定

**ステータスコード**とは、処理結果を表す 3 桁の数字です。FastAPI の既定では成功はすべて 200(OK)ですが、「新しくデータを作った」ことを伝えるには **201**(Created)を返すのが Web API の作法です。デコレータに `status_code=201` を書くだけで、成功時のコードが変わります。🟡 「POST で作成したら 201」という対応を理屈で理解しましょう。

```python
@app.post("/items", status_code=201)
def create_item(item: Item):
    return item
```

## ch04 ステータスコードの使い分け

よく使うステータスコードは 4 つです。**200**(OK: 取得や更新の成功)、**201**(Created: 新しく作成した)、**204**(No Content: 成功したが返す中身がない。削除でよく使う)、**404**(Not Found: 見つからない)。204 のレスポンスにはボディを入れない決まりなので、関数は `return None`(何も返さない)にします。存在しない URL へのアクセスには FastAPI が自動で 404 を返します。🟡 4 つのコードの意味を説明できるようになりましょう。

```python
@app.delete("/items/1", status_code=204)
def delete_item():
    return None  # 204 ではボディを返さない
```
