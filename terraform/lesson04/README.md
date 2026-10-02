# Lesson 04 localsと式

ファイル内の中間変数 locals と、文字列補間・演算子・条件式を学ぶレッスンです。実務コードの名前組み立てパターンと、var / locals の使い分けの流儀まで扱います。

## ch01 localsとlocal.

**locals**(ファイル内だけで使う中間変数をまとめるブロック)は `locals { 名前 = 式 }` と書き、`local.名前` で参照します(定義は複数形、参照は単数形なことに注意)。variable が「外から受け取る入力」なのに対し、locals は「中で組み立てた値に名前を付ける」ためのものです。実務では計算結果や共通タグを locals に置き、`locals.tf` というファイルにまとめる流儀をよく見ます。コード中の `local.xxx` を見たら locals ブロックの定義元を探すのが読解の基本です。🔴 locals の定義と `local.` 参照は、手が覚えるまで書きましょう。

```hcl
locals {
  retention_days = 30
}

output "days" {
  value = local.retention_days  # 参照は local.名前
}
```

## ch02 文字列補間と演算子

**文字列補間**(文字列の中に `${式}` で値を埋め込む書き方)を使うと `"${var.app}-${var.env}"` のように名前を組み立てられます。実務の Terraform ではリソース名やタグをこの形で組み立てるのが最頻出パターンで、`"${var.project}-${var.env}-web"` のような式は瞬時に読めるようになる必要があります。また HCL には算術演算子(`+ - * / %`)や比較演算子(`== != < >` など)もあり、locals の右辺で計算に使えます。🔴 `${}` の補間は実務コードの至るところに出るので、手が覚えるまで書きましょう。

```hcl
locals {
  name  = "${var.app}-${var.env}"  # 例: "web-prod"
  total = 4 * 3                    # 12
}
```

## ch03 条件式 cond ? a : b

**条件式**(`条件 ? 真のときの値 : 偽のときの値` の三項演算子)は、環境によって値を切り替える定番の書き方です。実務では `var.env == "prod" ? "r6g.large" : "t4g.micro"` のように「本番だけ大きいインスタンス」を表現したり、後のレッスンで学ぶ `count = var.enabled ? 1 : 0`(リソースを作る/作らないの切り替え)に使われたりします。条件部には `==` などの比較演算子で作った bool 値を置きます。🔴 `? :` は実務コードで毎日見る形なので、手が覚えるまで書きましょう。

実務ではこう書かれることが多いです(読解例):

```hcl
locals {
  instance_type = var.env == "prod" ? "r6g.large" : "t4g.micro"
}
```

## ch04 varとlocalsの使い分け・命名の流儀

var と locals の使い分けには実務で流儀の違いがあります。ひとつは **locals 集約派**(`name_prefix = "${var.project}-${var.env}"` のような組み立てを locals に集め、リソース側は `local.name_prefix` だけを参照する)。もうひとつは **var 直参照派**(リソース側で `"${var.project}-${var.env}-web"` と都度組み立てる)。Finatext / Skillax などのコードベースでも混在するので、`local.name_prefix` を見たら locals の定義元へ、`var.` が連続していたら variables.tf へ、と参照元をたどる読み方を身につけます。🟡 どちらの流儀も読めることが目標です。

実務ではこう書かれることが多いです(読解例):

```hcl
locals {
  name_prefix = "${var.project}-${var.env}"
}

resource "aws_s3_bucket" "logs" {
  bucket = "${local.name_prefix}-logs"  # 組み立ては locals に集約
}
```
