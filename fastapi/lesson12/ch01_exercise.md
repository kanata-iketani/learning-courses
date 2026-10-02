# lesson12 ch01 演習: 仕様の読み方と土台（Book モデル + GET）

次の仕様でミニ CRUD API の土台を作ってください。

- モデル: `Book`(`id: int`・`title: str`・`price: int`)
- データ: 辞書 `books`(starter に定義済み)
- `GET /books`: `list(books.values())` で全件を返す
- `GET /books/{book_id}`: なければ 404(detail は `book {book_id} は見つかりません`)、あれば `books[book_id]` を返す

**期待出力**

```text
200
[{'id': 1, 'title': 'Go入門', 'price': 3000}, {'id': 2, 'title': 'SQL入門', 'price': 2600}]
200
{'id': 2, 'title': 'SQL入門', 'price': 2600}
404
{'detail': 'book 9 は見つかりません'}
```
