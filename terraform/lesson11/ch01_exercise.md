# lesson11 ch01 演習: ディレクトリ分割方式

starter のモジュール `./modules/service` は env を受け取り、名前とインスタンスタイプを返します。prod と stg から同じモジュールを呼ぶ構成を再現してください。

1. `module "prod"`(env = `"prod"`)と `module "stg"`(env = `"stg"`)の 2 つの呼び出しを書く
2. output `prod_type` と `stg_type` で各モジュールの `instance_type` を表示する

**期待出力**

```text
prod_type = "m5.large"
stg_type = "t3.small"
```
