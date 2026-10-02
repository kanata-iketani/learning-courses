# lesson06 ch03 演習: Query で検証する

検索 API のキーワードに制約を付けます。

- `GET /find` を作り、クエリパラメータ `keyword`(文字列)を `Query(min_length=3)` で「3 文字以上」に制限する
- `{"keyword": 受け取った値}` の形で返す

動作確認では 7 文字のキーワードと 2 文字のキーワードを送ります。

**期待出力**

```text
200
{'keyword': 'fastapi'}
422
```
