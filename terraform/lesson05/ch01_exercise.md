# lesson05 ch01 演習: 文字列関数（format・join・split ほか）

variable `service`(default `"Web"`)と `env`(default `"STG"`)を宣言し、次の3つを出力してください。

- output `bucket`: `format` と `lower` を使って `web-stg-logs` という形の名前を組み立てる
- output `env_part`: `bucket` の値を `split("-", ...)` で分解した2番目の要素
- output `underscored`: `bucket` の値の `-` を `_` に置換したもの

(ヒント: default が大文字なので、`lower(var.service)` のように小文字にしてから `format("%s-%s-logs", ...)` に渡します。組み立てた名前は locals に置くと3つの output で使い回せます。リストの2番目は 0 始まりなので `[1]` です)

**期待出力**

```text
bucket = "web-stg-logs"
env_part = "stg"
underscored = "web_stg_logs"
```
