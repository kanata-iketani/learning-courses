# lesson09 ch03 演習: 「見つからなければ404」の定番パターン

メニュー辞書を持つ API に `GET /menu/{item_id}` を定番パターンで作ってください。

- `item_id` が `menu` になければ 404 を raise し、detail は `menu {item_id} は見つかりません`(f-string)
- あれば `menu[item_id]`(name と price の辞書)をそのまま返す

**期待出力**

```text
200
{'name': 'コーヒー', 'price': 480}
404
{'detail': 'menu 3 は見つかりません'}
```
