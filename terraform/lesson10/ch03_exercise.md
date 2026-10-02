# lesson10 ch03 演習: モジュールを自作する

命名モジュール `./modules/naming` を自作してください。

1. モジュール側: variable `env` と `app` を受け取り、output `resource_name` で `"app名-環境名"`、output `bucket_name` で `"app名-環境名-logs"` を返す
2. 呼び出し側: `env = "prod"`、`app = "skillax"` を渡す
3. 呼び出し側の output `resource_name` と `bucket_name` でモジュールの出力を表示する

**期待出力**

```text
bucket_name = "skillax-prod-logs"
resource_name = "skillax-prod"
```
