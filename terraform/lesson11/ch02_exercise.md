# lesson11 ch02 演習: tfvars方式とworkspace方式

env 名で設定値を出し分ける条件式を書いてください。

1. `variable "env"` を string 型、default `"stg"` で定義する
2. output `log_level` で、env が `"prod"` なら `"warn"`、そうでなければ `"debug"` を表示する
3. output `min_capacity` で、env が `"prod"` なら `4`、そうでなければ `1` を表示する
4. output `retention_days` で、env が `"prod"` なら `365`、そうでなければ `7` を表示する

(ヒント: 本文のサンプルと同じく `条件 ? 真のときの値 : 偽のときの値` を使います。数値は `4` のように引用符なしで書くと、出力も `min_capacity = 1` と引用符なしで表示されます)

**期待出力**

```text
log_level = "debug"
min_capacity = 1
retention_days = 7
```
