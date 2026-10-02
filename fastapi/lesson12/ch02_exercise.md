# lesson12 ch02 演習: 追加と更新（POST 201 / PUT 404対応）

ch01 の土台(starter に定義済み)に、追加と更新を足してください。

- `POST /books`: ボディを `book: Book` で受け取り、`books[book.id] = book` で保存して `book` を返す。成功時のステータスコードは **201**
- `PUT /books/{book_id}`: なければ 404(detail は `book {book_id} は見つかりません`)、あれば `books[book_id] = book` で上書きして `book` を返す

**期待出力**

```text
201
{'id': 3, 'title': 'Docker入門', 'price': 3200}
200
{'id': 3, 'title': 'Docker入門', 'price': 3200}
200
{'id': 1, 'title': 'Go入門', 'price': 2700}
404
{'detail': 'book 9 は見つかりません'}
```
