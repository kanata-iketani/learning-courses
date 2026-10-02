# lesson11 ch02 演習: tfvars方式とworkspace方式

env 名で設定値を出し分ける条件式を書いてください。

1. `variable "env"` を string 型、default `"stg"` で定義する
2. output `log_level` で、env が `"prod"` なら `"warn"`、そうでなければ `"debug"` を表示する
3. output `min_capacity` で、env が `"prod"` なら `4`、そうでなければ `1` を表示する
4. output `retention_days` で、env が `"prod"` なら `365`、そうでなければ `7` を表示する

**期待出力**

```text
log_level = "debug"
min_capacity = 1
retention_days = 7
```
