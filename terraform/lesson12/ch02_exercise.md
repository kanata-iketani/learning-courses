# lesson12 ch02 演習: backend "s3" の読み方

次の backend 設定を読み、bucket と key の命名ロジックを再現してください(実際の backend ブロックは書かず、locals / output だけで組み立てます。backend の中では変数が使えないため、実務ではこのような値が直書きされています)。

```hcl
terraform {
  backend "s3" {
    bucket         = "myapp-tfstate"
    key            = "prod/network/terraform.tfstate"
    region         = "ap-northeast-1"
    dynamodb_table = "tfstate-lock"
  }
}
```

variable `project`(default `"myapp"`)、`env`(default `"prod"`)、`component`(default `"network"`)を定義し、

- output `bucket`: `<project>-tfstate` の形
- output `state_key`: `<env>/<component>/terraform.tfstate` の形

を出力してください。

(`<project>` は「ここに project の値が入る」という意味の書き方です。文字列の中に変数の値を埋め込むには `"${var.project}-tfstate"` のように `${ }` を使います(lesson04)。variable の書き方は starter の `project` をまねてください)

**期待出力**

```text
bucket = "myapp-tfstate"
state_key = "prod/network/terraform.tfstate"
```
