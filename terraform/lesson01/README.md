# Lesson 01 TerraformとIaC

Terraform を書く前に、IaC の考え方と plan → apply のサイクル、HCL の見た目に慣れるレッスンです。この講座の演習はクラウド不要の `terraform_data` と `output` を使って手元で完結します。

## ch01 IaCとTerraformのサイクル

**IaC**(Infrastructure as Code。サーバーやネットワークなどのインフラをコードで定義して管理する考え方)の代表的なツールが Terraform です。Terraform は **HCL**(HashiCorp Configuration Language。Terraform 専用の設定言語)で「あるべき状態」を書き、`terraform plan`(何が変わるかの予告)→ `terraform apply`(実際に反映)のサイクルで運用します。手順書ではなく「最終形」を書くのが特徴で、同じコードを何度 apply しても結果が同じになります(冪等性)。🟡 まずは plan → apply のサイクルと「宣言的に書く」感覚を理解しましょう。

手作業ではこうしていました:

```
1. AWSコンソールを開く → 2. S3を選ぶ → 3. バケット作成ボタン...
```

Terraform ではこう書きます(あるべき状態の宣言):

```hcl
resource "aws_s3_bucket" "logs" {
  bucket = "app-prod-logs"
}
```

## ch02 HCLブロックの解剖

HCL のコードは**ブロック**(`resource "..." "..." { ... }` のようなひとまとまり)を並べて書きます。ブロックは「種別 + ラベル + 本体 `{ }`」で構成され、本体には `名前 = 式` の形で**引数**(argument。ブロックに渡す設定値)を書きます。**式**(expression。値を作る書き方)には文字列や数値のリテラルのほか、後で学ぶ参照や関数も置けます。コメントは `#` が主流で、`//` と `/* */` も使えます。実務コードを読むときは「resource はラベル2つ、variable や output はラベル1つ」という対応を押さえると構造が一気に見えるようになります。🔴 ブロックの形は今後すべての土台なので、手が覚えるまで書きましょう。

```hcl
resource "terraform_data" "web" {  # 種別 resource + ラベル2つ
  input = "hello"                  # 引数: 名前 = 式
}

output "name" {  # 種別 output + ラベル1つ
  value = "web"
}
```

## ch03 planとapplyとstate

この講座の「▶ 実行」ボタンは `terraform init`(プラグインなどの初期化)→ `terraform apply`(あるべき状態を実際に反映)→ `terraform output`(結果の表示)を一気に実行しています。実務では apply の前に `terraform plan`(何が作成・変更・削除されるかの予告)を見て確認します。apply の結果は **state**(terraform.tfstate。Terraform が「今なにを管理しているか」を記録するファイル)に保存され、次回の plan はコードと state の差分から計算されます。実務では state を S3 などのリモートに置いてチームで共有するのが定番です(詳しくは lesson12)。🟡 まずは「plan は予告、apply は反映、state は記録」という役割分担を理解しましょう。

```sh
terraform init   # 初期化(最初の1回)
terraform plan   # 変更の予告(まだ何も変えない)
terraform apply  # 反映して state に記録
```
