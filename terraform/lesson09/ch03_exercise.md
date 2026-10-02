# lesson09 ch03 演習: dynamicの使いどころと使いすぎ問題

「固定 2 件なら直書き、3 件以上なら dynamic」という判断基準を条件式で表現してください。

1. `variable "rules"` を `list(string)` 型、default `["https", "ssh"]` で定義する
2. output `decision` で、件数が 3 以上なら `"dynamic"`、そうでなければ `"static"` を表示する
3. output `rule_count` で件数を表示する

**期待出力**

```text
decision = "static"
rule_count = 2
```
