# lesson12 ch02 演習: backend "s3" の読み方

次の backend 設定を読み、bucket と key の命名ロジックを再現してください(実際の backend ブロックは書かず、locals / output だけで組み立てます)。

```hcl
terraform {
  backend "s3" {
    bucket         = "skillax-tfstate"
    key            = "prod/network/terraform.tfstate"
    region         = "ap-northeast-1"
    dynamodb_table = "tfstate-lock"
  }
}
```

variable `project`(default `"skillax"`)、`env`(default `"prod"`)、`component`(default `"network"`)を定義し、

- output `bucket`: `<project>-tfstate` の形
- output `state_key`: `<env>/<component>/terraform.tfstate` の形

を出力してください。

**期待出力**

```text
bucket = "skillax-tfstate"
state_key = "prod/network/terraform.tfstate"
```
