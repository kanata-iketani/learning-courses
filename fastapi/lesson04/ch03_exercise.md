# lesson04 ch03 演習: int 型クエリと skip/limit パターン

くだものの一覧 `fruits` から、skip / limit で一部を取り出す GET `/fruits` を書いてください。`skip` (int、デフォルト 0) と `limit` (int、デフォルト 3) を受け取り、`fruits[skip : skip + limit]` を返します。

**期待出力**

```text
['りんご', 'みかん', 'ぶどう']
['ぶどう', 'もも']
```
