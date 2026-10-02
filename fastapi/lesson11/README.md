# Lesson 11 ルーター分割と非同期

アプリが大きくなったときにエンドポイントを APIRouter でグループ分けする方法と、async def による非同期エンドポイントを学ぶレッスンです。実際の開発でプロジェクトを整理するときに必要になる知識です。

## ch01 APIRouter でエンドポイントをまとめる

**APIRouter** とは、エンドポイントをグループにまとめるための部品です。実際の開発では `users.py`・`items.py` のようにファイルを分け、各ファイルで `router = APIRouter()` を作って `@router.get(...)` を書き、最後にアプリ本体で `app.include_router(router)` として合体させます。`@app.get` を直接書いたときと動きは同じで、置き場所を整理できるのが利点です。この演習では 1 ファイル内で同じ形を作ります。🟡 「router に登録 → include_router で合体」という流れを理解しましょう。

```python
router = APIRouter()

@router.get("/items")
def list_items():
    return ["ペン", "ノート"]

app = FastAPI()
app.include_router(router)
```

## ch02 prefix と tags

APIRouter には **prefix**(その router の全パスに付く共通の接頭辞)と **tags**(自動ドキュメント /docs でのグループ名)を指定できます。`APIRouter(prefix="/items", tags=["items"])` とすると、router 側は `"/"` や `"/{item_id}"` と書くだけで実際のパスは `/items/`・`/items/{item_id}` になります。パスの書き間違いが減り、/docs もグループごとに整理されます。🟡 「router 内のパス + prefix = 実際のパス」という対応を理解しましょう。

```python
router = APIRouter(prefix="/items", tags=["items"])

@router.get("/")          # 実際は GET /items/
def list_items(): ...

@router.get("/{item_id}")  # 実際は GET /items/{item_id}
def read_item(item_id: int): ...
```

## ch03 async def エンドポイント

エンドポイントは **async def**(非同期関数)でも定義できます。非同期関数の中では **await**(処理の完了を待つ間、他の処理に順番を譲る文)が使え、DB や外部 API の応答待ちの間に別のリクエストを処理できるのが利点です。await できるのは非同期対応の関数(async def で定義されたものなど)だけです。呼び出す側から見た動きは同期の `def` と同じで、TestClient もそのまま呼べます。🟡 「async def の中で await で待つ」という形を理解しましょう。

```python
@app.get("/async")
async def read_async():
    msg = await load_message()  # 待っている間、他のリクエストを処理できる
    return {"message": msg}
```

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
