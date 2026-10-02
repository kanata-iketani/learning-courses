# Lesson 10 モジュール

モジュール(複数の Terraform 定義をひとまとめにして再利用する仕組み)のレッスンです。module ブロックと source の読み方、入力(variable)と出力(output)、自作モジュール、そして薄い/厚いという設計流儀までを扱います。演習は `# === file: ... ===` 区切りのマルチファイル形式です。

## ch01 moduleブロックとsource

**モジュール**(複数の Terraform 定義をひとまとめにして再利用する仕組み)は、`module` ブロックで呼び出します。読解の第一歩は **source**(モジュールのコードの置き場所を示す引数)の見分けです。`./` や `../` で始まればローカル(同じリポジトリ内のディレクトリ)、`terraform-aws-modules/vpc/aws` のような 3 分割形式はレジストリ(公開モジュール。version 指定とセット)、`git::https://...` は git リポジトリ直接参照です。🔴 実務コードで module を見たら、まず source を読んで「実体のコードがどこにあるか」を特定しましょう。

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws" # レジストリ
  version = "5.8.1"
}

module "naming" {
  source = "./modules/naming" # ローカル(相対パス)
}
```

## ch02 モジュールの入力と出力

モジュールの境界(外部とやりとりできる接点)は、variable(入力)と output(出力)だけです。呼び出し側は module ブロックの引数でモジュール側の variable に値を渡し、結果は `module.呼び出し名.output名` で受け取ります。モジュール内部のリソースや locals は外から直接参照できず、output で公開されたものだけが見えます。🔴 実務の読解では「module ブロックの引数 ↔ モジュール側の variables.tf」「module.xxx.yyy ↔ モジュール側の outputs.tf」を突き合わせるのが基本動作です。

```hcl
module "vpc" {
  source = "./modules/vpc"
  cidr   = "10.0.0.0/16" # → モジュール側 variable "cidr" へ
}

resource "aws_subnet" "app" {
  vpc_id = module.vpc.vpc_id # ← モジュール側 output "vpc_id" から
}
```

## ch03 モジュールを自作する

モジュールの自作は、ディレクトリを切って variable / locals / output を置くだけです。実務でよくあるのが **naming モジュール**(命名規約を 1 か所に集約するモジュール)で、「app名-環境名」のような規則を全リソースへ一貫して適用できます。命名規約が変わってもモジュール 1 か所を直せば済むのが利点です。🔴 「規約や決まりごとをモジュールに閉じ込める」という発想は、実務コード読解でも設計でも要になります。

```hcl
module "naming" {
  source = "./modules/naming"
  env    = "prod"
  app    = "skillax"
}

# 使う側は module.naming.resource_name などを参照するだけ
# bucket = module.naming.bucket_name # => "skillax-prod-logs"
```

## ch04 薄いモジュールvs厚いモジュール

実務のモジュール設計には流儀の対立があります。**薄いモジュール**(リソース 1 個を包み、引数をほぼ素通しするモジュール)は柔軟で挙動が追いやすい一方、呼び出し側の記述が長くなります。**厚いモジュール**(複数リソースと社内規約を焼き込み、少ない入力で多くを作るモジュール)は規約を強制でき記述も短い一方、規約から外れる個別調整が難しくなります。🟡 読解時は「variable の数」と「中の resource の数」の比を見ると流儀を推測できます。variable が多く resource が 1 個なら薄い、その逆なら厚いモジュールです。

```hcl
# 厚いモジュールの典型: 入力 2 個で VPC + サブネット + NAT までまとめて作る
module "network" {
  source = "./modules/network"
  env    = "prod"
  cidr   = "10.0.0.0/16"
}
```
