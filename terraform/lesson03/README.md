# Lesson 03 variable

外から値を受け取る variable を学ぶレッスンです。基本の型から list / map / object、tfvars と validation まで、実務の `variables.tf` を読める状態を目指します。

## ch01 variableとvar.

**variable**(外部から値を受け取るための入力口となるブロック)は `variable "名前" { }` と書き、`var.名前` で参照します。本体には `type`(受け取る型)と `default`(入力がないときの既定値)を書くのが基本です。default があれば入力なしでも apply が通ります。実務では variable 定義を `variables.tf` に集める流儀が一般的で、コード中の `var.xxx` を見たら `variables.tf` を開いて型と default を確認する、が読解の第一歩です。🔴 variable の定義と `var.` 参照は、手が覚えるまで書きましょう。

```hcl
variable "project" {
  type    = string
  default = "myapp"
}

output "name" {
  value = var.project  # var.名前 で参照
}
```

## ch02 型いろいろ

variable の `type` には `string` / `number` / `bool` のほか、**list**(順序付きの並び。`list(number)` のように要素の型を指定)と **map**(キーと値の組。`map(string)` など)が使えます。要素の参照は list が `var.ports[0]`(0始まり)、map が `var.tags["env"]` です。実務では `list(string)` のサブネット ID 一覧や、`map(string)` のタグ集合が頻出なので、この2つの参照の形は必ず読めるようにしておきます。🔴 型の書き方と要素参照は、手が覚えるまで書きましょう。

```hcl
variable "ports" {
  type    = list(number)
  default = [80, 443]
}

output "first" {
  value = var.ports[0]  # 80
}
```

## ch03 object型と実務のvariables.tf

**object 型**(名前付きの属性をまとめた型。`object({ name = string, port = number })` のように書く)を使うと、関連する設定をひとつの variable に束ねられます。属性の参照は `var.db.name` とドットでつなぎます。実務の `variables.tf` では次のような定義がよく見られます。`var.db.port` のような参照を見たら「object 型 variable の属性アクセス」と読みます。🟡 まずは object 型の定義と参照が読めれば十分です。

実務ではこう書かれることが多いです(読解例):

```hcl
variable "db" {
  description = "DB 接続設定"       # 実務では description も書く
  type = object({
    name = string
    port = number
  })
  default = { name = "app-db", port = 5432 }
}
```

## ch04 tfvarsと優先順位・validation

variable の値は default 以外からも渡せます。**tfvars ファイル**(`terraform.tfvars` など、変数値だけを書くファイル)、環境変数 `TF_VAR_名前`、コマンドの `-var` オプションがあり、後勝ちの優先順位は「環境変数 < terraform.tfvars < `-var-file` < `-var`」です。実務では環境ごとに `prod.tfvars` / `stg.tfvars` を切り替える構成をよく見ます(lesson11 で扱います)。また **validation ブロック**(variable の中に書く入力チェック。`condition` が false だと `error_message` を出して失敗)で不正値を弾けます。⚪ この仕組みは存在だけ知っておけば十分です。

```hcl
# terraform.tfvars(値だけを書くファイル)
env = "prod"
```

```sh
terraform apply -var 'env=stg'  # -var は tfvars より優先
```
