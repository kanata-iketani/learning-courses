# lesson14 ch03 演習: 総合読解演習

次の実務風コードを読み、3つの問いに locals / output で答えてください。

```hcl
variable "project" {
  default = "myapp"
}

variable "env" {
  default = "prod"
}

locals {
  name_prefix = "${var.project}-${var.env}"
  common_tags = {
    Project   = var.project
    Env       = var.env
    ManagedBy = "terraform"
  }
  services = {
    api    = { port = 8080 }
    web    = { port = 80 }
    worker = { port = 0 }
  }
}

resource "aws_ecs_service" "this" {
  for_each = local.services
  name     = "${local.name_prefix}-${each.key}"
  tags     = merge(local.common_tags, { Name = "${local.name_prefix}-${each.key}" })
}
```

- output `api_tags`: api サービスに付くタグを `jsonencode()` した文字列
- output `service_count`: 作られるサービスの数
- output `service_names`: 全サービス名を `keys()` の順で `", "` で連結

(ヒント)
- `aws_ecs_service` は動かせないので、resource は書かずに locals を再現し、output で計算します
- api のタグは、resource の `tags` の式の `each.key` を `"api"` に置き換えたものです。それを `jsonencode()` で包みます(merge は lesson05 ch03、jsonencode は lesson05 ch04)
- 個数は `length()`、名前の連結は `join()` と for 式(本文のサンプルと同じ形)で作れます
- `keys()` も jsonencode のキーもアルファベット順に並びます

**期待出力**

```text
api_tags = "{\"Env\":\"prod\",\"ManagedBy\":\"terraform\",\"Name\":\"myapp-prod-api\",\"Project\":\"myapp\"}"
service_count = 3
service_names = "myapp-prod-api, myapp-prod-web, myapp-prod-worker"
```
