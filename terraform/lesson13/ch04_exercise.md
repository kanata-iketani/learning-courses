# lesson13 ch04 演習: 変数駆動の度合いを見抜く

次のタスク定義を読み、`cpu` と `memory` の最終値と出どころを答えてください(tfvars などによる上書きはないものとします)。

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

(ヒント: resource ブロックは書かず、locals の値を output で表示します。`cpu_source` は本文のサンプルと同じく、同じ条件 `var.container_cpu > 0` を使った条件式 `条件 ? "variable" : "hardcoded-default"` で作ります。`memory_source` は文字列 `"variable-default"` をそのまま書いてかまいません。数値は `"` なし、文字列は `"..."` 付きで表示されます)

**期待出力**

```text
cpu = 256
cpu_source = "hardcoded-default"
memory = 1024
memory_source = "variable-default"
```
