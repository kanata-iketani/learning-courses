# lesson10 ch03 演習: モジュールを自作する

命名モジュール `./modules/naming` を自作してください。

1. モジュール側: variable `env` と `app` を受け取り、output `resource_name` で `"app名-環境名"`、output `bucket_name` で `"app名-環境名-logs"` を返す
2. 呼び出し側: `env = "prod"`、`app = "myapp"` を渡す
3. 呼び出し側の output `resource_name` と `bucket_name` でモジュールの出力を表示する

(ヒント: 文字列の組み立ては lesson04 の文字列補間 `"${var.app}-${var.env}"` を使います。output は名前のアルファベット順に表示されるので、`bucket_name` が先に出ます)

**期待出力**

```text
bucket_name = "myapp-prod-logs"
resource_name = "myapp-prod"
```
