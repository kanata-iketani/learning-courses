# Lesson 12 state・バックエンド・プロバイダ

Terraform を実行する「土台」を読めるようになるレッスンです。state(実リソースとの対応表)、backend(state の保存先)、プロバイダのバージョン制約と alias を、実務コードの読解を中心に学びます。演習では読み取ったロジックを locals / output で再現します。

## ch01 stateとは何か

**state**(Terraform がコードと実リソースの対応表を保存するファイル。既定では `terraform.tfstate`)は Terraform 運用の心臓部です。apply のたびに更新され、Terraform は state と実環境を突き合わせて差分を計算します。state ファイルを手で消すと Terraform は作成済みリソースを忘れ、次の apply で二重作成が起きます。直接編集も破損のもとです。読むときはファイルを開かず `terraform state list`(アドレス一覧)や `terraform state show`(個別の詳細)を使います。🟡 「state は消さない・直接編集しない・読むならコマンドで」を必ず押さえましょう。

```text
$ terraform state list
aws_ecs_service.api
aws_iam_role.task
aws_s3_bucket.logs
```

## ch02 backend "s3" の読み方

**バックエンド**(state の保存先の設定)を S3 にするのが実務の定番です。典型例を読んでみます。

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

`bucket` は保存先バケット、`key` はバケット内のパスです。key は「環境/コンポーネント」で切る命名が多く、ここを見るとその構成がどの単位で分割されているかが分かります。`dynamodb_table` は**ロック**(同時 apply による state 破損を防ぐ排他制御)用のテーブルです。🟡 backend を見たら「どこに・どのパスで・ロックは何か」の3点を読み取りましょう。

## ch03 required_providersとバージョン制約

**required_providers**(使うプロバイダの入手元とバージョン制約の宣言)は `terraform` ブロックの中に書きます。

```hcl
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.67"
    }
  }
}
```

`>=` は下限だけの指定です。`~>`(悲観的制約)は「最後に書いた桁だけ上げてよい」という意味で、`~> 5.67` は 5.67 以上 6.0 未満、`~> 5.67.0` なら 5.67.x のパッチ更新のみ許可です。メジャーバージョンアップ事故を防ぐため、実務ではほぼ `~>` が使われます。🟡 `~>` がどの範囲までの更新を許すかを読めるようにしましょう。

## ch04 provider alias

**alias**(同じプロバイダに複数の設定を持たせるときの名前)は、マルチリージョンやマルチアカウント構成で登場します。

```hcl
provider "aws" {
  region = "ap-northeast-1"
}

provider "aws" {
  alias  = "virginia"
  region = "us-east-1"
}

resource "aws_acm_certificate" "cdn" {
  provider    = aws.virginia # CloudFront 用証明書は us-east-1 必須
  domain_name = "cdn.example.com"
}
```

`provider = aws.virginia` の付いたリソースだけが別リージョン(マルチアカウントなら別アカウント)に作られます。⚪ resource 内に `provider =` を見つけたら「どの alias の設定で作られるか」を provider ブロックまで遡って確認する、という読み方だけ覚えておけば十分です。
