# lesson05 ch01 演習: 文字列関数（format・join・split ほか）

variable `service`(default `"Web"`)と `env`(default `"STG"`)を宣言し、次の3つを出力してください。

- output `bucket`: `format` と `lower` を使って `web-stg-logs` という形の名前を組み立てる
- output `env_part`: `bucket` の値を `split("-", ...)` で分解した2番目の要素
- output `underscored`: `bucket` の値の `-` を `_` に置換したもの

**期待出力**

```text
bucket = "web-stg-logs"
env_part = "stg"
underscored = "web_stg_logs"
```
