# lesson14 ch03 演習: 総合読解演習

次の実務風コードを読み、3つの問いに locals / output で答えてください。

```hcl
variable "project" {
  default = "skillax"
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

**期待出力**

```text
api_tags = "{\"Env\":\"prod\",\"ManagedBy\":\"terraform\",\"Name\":\"skillax-prod-api\",\"Project\":\"skillax\"}"
service_count = 3
service_names = "skillax-prod-api, skillax-prod-web, skillax-prod-worker"
```
