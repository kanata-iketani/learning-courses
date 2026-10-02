# Lesson 14 実務コード読解2：スタイル差を読む

同じ構成でも書き手によってスタイルは変わります。フラットに resource を並べる派とモジュールに包む派の読み比べ、リファクタの痕跡(moved ブロック)の読み方を学び、最後に総合読解演習で仕上げます。

## ch01 同じ構成の2流儀読み比べ

同じ「ログ用バケット」でも、resource をフラットに並べる派とモジュールに包む派がいます。

```hcl
# フラット派: リポジトリ直下に resource が並ぶ
resource "aws_s3_bucket" "logs" {
  bucket = "${var.project}-${var.env}-logs"
}

# モジュール派: 組み立てはモジュールの中
module "logs" {
  source  = "./modules/log-bucket"
  project = var.project
  env     = var.env
}
```

追い方が変わります。フラット派は resource 名で grep すれば全体が見えます。モジュール派は `source` のディレクトリへ移動し、variables.tf(入力)→ main.tf(実体)→ outputs.tf(出力)の順に読みます。🟡 module ブロックを見たら「何を入力し、何を出力として受け取るか」を先に押さえるのがコツです。

## ch02 リファクタの痕跡を読む

リファクタの痕跡が読めると、コードの歴史が分かります。代表例が count → for_each 移行です。**moved ブロック**(state 上のリソースアドレスの付け替えをコードで宣言する仕組み)が残っていれば、その移行の記録です。

```hcl
resource "aws_instance" "web" {
  for_each = toset(var.names)
  # ...
}

moved {
  from = aws_instance.web[0]
  to   = aws_instance.web["blue"]
}
```

`[0]`(count の添字)から `["blue"]`(for_each のキー)への moved を見たら「昔は count で書かれていた」と読めます。一方 `terraform state mv`(コマンドで state 内のアドレスを直接移す操作)で移行するとコードに痕跡は残りません。⚪ moved の from / to を読めれば十分です。

## ch03 総合読解演習

総合読解の手順を確認します。(1) variable の default と locals で前提値を確定する (2) for_each の対象を数えて「何個できるか」を出す (3) name や tags の組み立て式に値を代入して最終形を出す。

```hcl
locals {
  name_prefix = "${var.project}-${var.env}"
  services = {
    api = { port = 8080 }
    web = { port = 80 }
  }
}

resource "aws_ecs_service" "this" {
  for_each = local.services
  name     = "${local.name_prefix}-${each.key}"
}
```

この例なら「2個でき、名前は name_prefix + キー」と読めます。🔴 この3ステップは実務コードを渡されたときに最初にやる作業です。演習で通しの読解を練習しましょう。
