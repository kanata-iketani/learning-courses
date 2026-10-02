# lesson13 ch01 演習: 命名とタグの流儀

次の実務風コードを読み、`aws_ecs_service.api` に付く name とタグを再現してください。

```hcl
locals {
  name_prefix = "${var.project}-${var.env}" # project = "skillax", env = "prod"
  common_tags = {
    Project   = var.project
    Env       = var.env
    ManagedBy = "terraform"
  }
}

resource "aws_ecs_service" "api" {
  name = "${local.name_prefix}-api"
  tags = merge(local.common_tags, { Name = "${local.name_prefix}-api" })
}
```

variable `project`(default `"skillax"`)と `env`(default `"prod"`)を定義し、

- output `name`: サービス名
- output `tags`: merge の結果を `jsonencode()` した文字列

を出力してください。

**期待出力**

```text
name = "skillax-prod-api"
tags = "{\"Env\":\"prod\",\"ManagedBy\":\"terraform\",\"Name\":\"skillax-prod-api\",\"Project\":\"skillax\"}"
```
