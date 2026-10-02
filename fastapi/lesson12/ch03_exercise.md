# lesson12 ch03 演習: 削除と仕上げ（DELETE + 通し確認）

ch02 までの API(starter に定義済み)に DELETE を足し、全操作を通しで確認してください。

- `DELETE /books/{book_id}`: なければ 404(detail は `book {book_id} は見つかりません`)、あれば `del books[book_id]` で削除して `{"deleted": book_id}` を返す

動作確認ブロックでは POST → PUT → DELETE → GET(404)→ 一覧 の順に呼びます。

**期待出力**

```text
201 {'id': 3, 'title': 'Docker入門', 'price': 3200}
200 {'id': 3, 'title': 'Docker入門', 'price': 2980}
200 {'deleted': 3}
404 {'detail': 'book 3 は見つかりません'}
404 {'detail': 'book 9 は見つかりません'}
200 [{'id': 1, 'title': 'Go入門', 'price': 3000}, {'id': 2, 'title': 'SQL入門', 'price': 2600}]
```
