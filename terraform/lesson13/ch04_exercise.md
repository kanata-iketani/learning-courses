# lesson13 ch04 演習: 変数駆動の度合いを見抜く

次のタスク定義を読み、`cpu` と `memory` の最終値と出どころを答えてください。

```hcl
variable "container_cpu" {
  default = 0 # 0 なら既定値を使う
}

variable "container_memory" {
  default = 1024
}

locals {
  cpu    = var.container_cpu > 0 ? var.container_cpu : 256
  memory = var.container_memory
}

resource "aws_ecs_task_definition" "api" {
  family = "api"
  cpu    = local.cpu
  memory = local.memory
}
```

上の variable と locals をそのまま再現し、

- output `cpu`: cpu の最終値
- output `cpu_source`: variable 由来なら `variable`、条件式の既定値に落ちたなら `hardcoded-default`
- output `memory`: memory の最終値
- output `memory_source`: この構成では `variable-default`(default 値がそのまま使われる)

を出力してください。

**期待出力**

```text
cpu = 256
cpu_source = "hardcoded-default"
memory = 1024
memory_source = "variable-default"
```
