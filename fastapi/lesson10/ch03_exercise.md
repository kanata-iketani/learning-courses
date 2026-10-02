# lesson10 ch03 演習: クラス依存（CommonQueryParams パターン）

曲名の一覧 API `GET /songs` をクラス依存で作ってください。

- クラス `CommonQueryParams` を定義する。`__init__(self, q: str | None = None, limit: int = 3)` で、`self.q` と `self.limit` に保存する
- `GET /songs` は `params: CommonQueryParams = Depends()` で受け取る
- `params.q` が `None` でなければ `q` を含む曲だけに絞り込み、先頭から `params.limit` 件を返す

**期待出力**

```text
['春の歌', '夏の歌', '夏祭り']
['夏の歌']
```
