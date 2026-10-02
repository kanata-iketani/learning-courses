# lesson06 ch01 演習: リストのfor式 — [for x in ...]

variable `users`(default `["sato", "suzuki", "takahashi"]`)を宣言し、for式で各ユーザーのメールアドレス(`ユーザー名@example.com`)のリストを作って、次の3つを出力してください。

- output `email_count`: リストの要素数
- output `emails`: リストを `tolist(...)` で包んでそのまま出力(複数行の表示形式を確認します)
- output `joined`: リストを `,` 区切りで join した文字列

**期待出力**

```text
email_count = 3
emails = tolist([
  "sato@example.com",
  "suzuki@example.com",
  "takahashi@example.com",
])
joined = "sato@example.com,suzuki@example.com,takahashi@example.com"
```
