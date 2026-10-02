# Lesson 13 実務コード読解1：AWS典型パターン

ここからが講座の核心です。実務の AWS コードに繰り返し現れる型 — name_prefix とタグの merge、IAM ポリシーの2流儀、セキュリティグループの ingress 生成、変数駆動の度合い — を読み解き、演習でロジックを再現します。

## ch01 命名とタグの流儀

実務コードの命名は `${var.project}-${var.env}` のような **name_prefix**(リソース名の共通接頭辞)に集約され、タグは `merge()` で「共通タグ + 個別タグ」を合成するのが定番です。

```hcl
locals {
  name_prefix = "${var.project}-${var.env}"
  common_tags = {
    Project   = var.project
    Env       = var.env
    ManagedBy = "terraform"
  }
}

resource "aws_s3_bucket" "logs" {
  bucket = "${local.name_prefix}-logs"
  tags   = merge(local.common_tags, { Name = "${local.name_prefix}-logs" })
}
```

`merge` は同じキーがあると後の引数が勝ちます。🔴 「locals に共通部品を置き、resource 側で merge して個別化する」流れは実務コードの至る所に出るので、必ず追えるようにしましょう。

## ch02 IAMポリシーの2流儀

IAM ポリシーの書き方は2流儀に分かれます。流儀1は `jsonencode()` 直書きです。

```hcl
resource "aws_iam_role_policy" "read" {
  name = "s3-read"
  role = aws_iam_role.task.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["s3:GetObject"]
      Resource = "arn:aws:s3:::app-logs/*"
    }]
  })
}
```

流儀2は `data "aws_iam_policy_document"`(HCL のブロックでポリシーを組み立て、`.json` 属性で JSON を得るデータソース)で、`statement { effect / actions / resources }` と小文字の属性名になります。最終的にできる JSON は同じです。🔴 見た目が違っても「Effect・Action・Resource の3点セット」を読み取れるようにしましょう。

## ch03 セキュリティグループのingress列挙

**セキュリティグループ**(SG。AWS の通信許可ルールの集合)の `ingress`(内向きの許可ルール)には、ベタ書きから `dynamic` + リスト駆動へ移行した痕跡がよく見られます。

```hcl
# 昔: ポートごとにコピペ
ingress {
  from_port   = 80
  to_port     = 80
  protocol    = "tcp"
  cidr_blocks = ["10.0.0.0/8"]
}

# 今: ポートのリストから生成
dynamic "ingress" {
  for_each = var.ingress_ports
  content {
    from_port   = ingress.value
    to_port     = ingress.value
    protocol    = "tcp"
    cidr_blocks = [var.internal_cidr]
  }
}
```

🟡 dynamic 版を見たら「for_each の元リストに何が入るか」を variable まで遡り、生成されるルールを数えられるようにしましょう。

## ch04 変数駆動の度合いを見抜く

同じ構成でも「全部 variable 化する派」と「ほぼハードコードする派」がいます。設定値の出どころは次の順で追います。(1) resource 内に値が直接書いてあればそこで確定 (2) `var.xxx` なら variable ブロックの `default` を見る (3) さらに tfvars やモジュール呼び出しの引数で上書きされていないか確認する。

```hcl
# var 派: 値は variable / tfvars を見ないと分からない
cpu = var.container_cpu

# ハードコード派: その場で確定
cpu = 256

# 折衷: 0 (未指定)なら既定値、という条件式もよく見ます
cpu = var.container_cpu > 0 ? var.container_cpu : 256
```

🟡 `var.` を見たら default と上書き経路を必ず確認する癖をつけましょう。
