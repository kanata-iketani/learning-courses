# Lesson 02 resourceと参照

Terraform の中心である resource ブロックと、リソース同士を「参照」でつなぐ書き方を学ぶレッスンです。演習はクラウド不要の `terraform_data` で行い、実務の AWS リソースや data ソースのコードは読解例として登場します。

## ch01 resourceの基本形とterraform_data

**resource**(Terraform に作らせたいものを宣言するブロック)は `resource "型" "名前" { 引数 }` が基本形です。型は「プロバイダ名_リソース種類」の形で、実務コードでは型を見れば何のサービスか分かります(`aws_s3_bucket` なら S3)。名前はコード内だけの識別子で、クラウド上の名前とは別物です。この講座では **terraform_data**(引数 `input` の値をそのまま属性 `output` に持つ、プロバイダ不要の組み込みリソース)で練習します。🔴 resource の基本形は実務コードの大半を占めるので、手が覚えるまで書きましょう。

実務ではこう書かれることが多いです(読解例):

```hcl
resource "aws_instance" "web" {  # 型: aws_instance(EC2)、名前: web
  ami           = "ami-12345678"
  instance_type = "t3.micro"
}
```

## ch02 リソース参照 型.名前.属性

あるリソースの値は `型.名前.属性`(例: `terraform_data.origin.output`)で**参照**(他のブロックの値を式の中で使うこと)できます。参照を書くと Terraform は**依存関係**(どちらを先に作るべきかの順序)を自動で認識し、参照先を先に作成します。順序を手で書く必要はありません。実務コードでは `vpc_id = aws_vpc.main.id` のような参照が至るところに出てくるので、「= の右辺に `型.名前.属性` があれば別リソースへの依存」と読めるようになるのが目標です。🔴 参照の形は読解の要なので、手が覚えるまで書きましょう。

```hcl
resource "aws_subnet" "app" {
  vpc_id = aws_vpc.main.id  # aws_vpc.main への参照 → VPC が先に作られる
}
```

## ch03 複数リソースのチェーン

参照は何段でもつなげられます。B が A を参照し、C が B を参照すれば、作成順は自動的に A → B → C になります。実務の AWS コードは「VPC → サブネット → EC2」のように参照のチェーンでできており、読むときは「= の右辺の参照をたどって依存の連鎖を追う」のが基本の読み方です。この講座では `terraform_data` の `input` に別リソースの `output` を渡してチェーンを作ります。🔴 参照をつないで依存の流れを作る感覚を、手が覚えるまで書きましょう。

実務ではこう書かれることが多いです(読解例):

```hcl
resource "aws_vpc" "main" { cidr_block = "10.0.0.0/16" }

resource "aws_subnet" "app" {
  vpc_id = aws_vpc.main.id      # VPC → サブネット
}

resource "aws_instance" "web" {
  subnet_id = aws_subnet.app.id # サブネット → EC2
}
```

## ch04 dataソースの読み方

実務コードには `data` で始まるブロックもよく出てきます。**data ソース**(既存のものを作らずに「読むだけ」のブロック)は `data "型" "名前" { 検索条件 }` と書き、参照は先頭に `data.` を付けて `data.型.名前.属性` とします。「resource = 作る」「data = 読む」が対応関係です。実務では既存 VPC の検索、最新 AMI の取得、自アカウント ID の取得(`data "aws_caller_identity" "current"`)が頻出です。演習は `terraform_data` で「よそで作られた値を参照して使う」動きを練習します。🟡 data を見たら「作らずに読んでいる」と分かれば十分です。

実務ではこう書かれることが多いです(読解例):

```hcl
data "aws_vpc" "existing" {          # 既存 VPC を検索して読む
  tags = { Name = "main-vpc" }
}

resource "aws_subnet" "app" {
  vpc_id = data.aws_vpc.existing.id  # 参照は data. で始まる
}
```
