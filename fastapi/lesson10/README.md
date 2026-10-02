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

## ch02 共通クエリパラメータを Depends でまとめる

依存関数には、エンドポイントと同じ書き方でクエリパラメータを宣言できます。`skip`(読み飛ばす件数)や `limit`(最大件数)のように、どの一覧 API にも付けたいパラメータは 1 つの依存関数にまとめるのが定番です。各エンドポイントは `Depends(pagination)` と書くだけでよく、パラメータの既定値や型の変更も 1 か所で済みます。🟡 「クエリパラメータの宣言ごと共通化できる」ことを理解しましょう。

```python
def pagination(skip: int = 0, limit: int = 2):
    return {"skip": skip, "limit": limit}

@app.get("/fruits")
def list_fruits(page: dict = Depends(pagination)):
    return fruits[page["skip"] : page["skip"] + page["limit"]]
```

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

## ch04 依存の中の依存（ネスト）と使いどころ

依存関数は、自分の引数にさらに `Depends` を書けます(依存のネスト)。FastAPI が奥から順に解決してくれるので、エンドポイント側は一番外側の 1 つを書くだけで済みます。実務では「設定の読み込み → DB 接続 → ログイン中ユーザの取得」のように、共通処理を段階的に積み上げる形で使われます。⚪ 今は「依存はネストでき、FastAPI が順に解決してくれる」と知っていれば十分です。

```python
def get_settings():
    return {"shop": "demo堂"}

def get_greeting(settings: dict = Depends(get_settings)):
    return f"ようこそ {settings['shop']} へ"

@app.get("/welcome")
def welcome(greeting: str = Depends(get_greeting)):
    return {"message": greeting}
```
