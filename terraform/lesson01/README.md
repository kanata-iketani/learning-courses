# Lesson 01 TerraformとIaC

Terraform を書く前に、IaC の考え方と plan → apply のサイクル、HCL の見た目に慣れるレッスンです。この講座の演習はクラウド不要の `terraform_data` と `output` を使って手元で完結します。

## ch01 IaCとTerraformのサイクル

### インフラと IaC とは

**インフラ**(アプリを動かすための土台。サーバー、ネットワーク、データベース、ファイル置き場など)は、いまは AWS などの**クラウド**(ネット越しに借りるコンピューター資源)で用意するのが一般的です。クラウドでは、ブラウザの管理画面(コンソール)でボタンを押せばサーバーやファイル置き場を作れます。

ただ、手作業には弱点があります。「誰が・いつ・どの設定で作ったか」が残らず、同じものをもう1つ(本番用と検証用など)作るときに手順を間違えやすいのです。

**IaC**(Infrastructure as Code。インフラをコードで定義して管理する考え方)は、この「作り方」をテキストファイルに書いて残します。コードなので Git で履歴を管理でき、レビューもでき、同じコードから何度でも同じものを作れます。その代表的なツールが **Terraform** です。

### 手順ではなく「最終形」を書く

手作業ではこうしていました:

```
1. AWSコンソールを開く → 2. S3を選ぶ → 3. バケット作成ボタン...
```

(**S3** は AWS のファイル置き場サービスで、**バケット**はその中に作るファイル入れ1つ分のことです)

Terraform ではこう書きます(あるべき状態の宣言):

```hcl
resource "aws_s3_bucket" "logs" {
  bucket = "app-prod-logs"
}
```

1行ずつ読むと次のとおりです。

| 行 | 意味 |
|---|---|
| `resource` | 「管理したいもの(リソース)を1つ定義します」という宣言 |
| `"aws_s3_bucket"` | リソースの**型**。AWS の S3 バケットという種類 |
| `"logs"` | このコードの中で使う**名前**。AWS 上の名前ではなく、コード内で区別するためのもの |
| `{ ... }` | このリソースの設定をまとめる本体 |
| `bucket = "app-prod-logs"` | AWS 上に作るバケットの名前を `app-prod-logs` にする、という設定 |

ここには「ボタンを押す」のような手順が一切ありません。「`app-prod-logs` という S3 バケットが存在する状態にしたい」という**最終形**だけを書いています。この書き方を**宣言的**(どうやるかではなく、どうなっていてほしいかを書くこと)と呼びます。

Terraform はこのコードと現実を比べて、足りなければ作り、すでにあれば何もしません。そのため同じコードを何度実行しても結果は同じです。この性質を**冪等性**(べきとうせい。何回やっても1回やったときと同じ結果になること)と呼びます。

### HCL と plan → apply のサイクル

Terraform のコードは **HCL**(HashiCorp Configuration Language。Terraform 専用の設定言語)で書き、ファイルの拡張子は `.tf` です。書いたコードは次のコマンドで反映します。

- `terraform plan`: 「何が作られ・変わり・消えるか」の予告を表示するだけ。まだ何も変えない
- `terraform apply`: 予告どおりに実際に反映する

🟡 まずは plan → apply のサイクルと「宣言的に書く」感覚を理解しましょう。

### この講座の練習用リソース `terraform_data`

本物の AWS を使うとアカウントやお金が必要です。この講座では、Terraform に最初から入っている練習用のリソース型 **`terraform_data`** を使います。クラウドには何も作らず、`input` に入れた値を apply 後に **`output` 属性**(リソースが持っている値の1つ)としてそのまま持つだけのリソースです。

サンプルを1行ずつ読みます。

```hcl
resource "terraform_data" "hello" {   # 型 terraform_data、名前 hello のリソースを定義
  input = "Hello, Terraform!"         # input に文字列を入れる
}

output "message" {                     # 名前 message の output(結果表示)を定義
  value = terraform_data.hello.output  # 表示する値 = hello リソースの output 属性
}

output "tool" {                        # 名前 tool の output
  value = "IaC"                        # 文字列をそのまま表示
}
```

- `#` から行末まではコメントで、Terraform は読み飛ばします
- `"..."` で囲んだものは文字列です
- `output` ブロックは「apply が終わったらこの値を表示して」という指示です
- `terraform_data.hello.output` は「`terraform_data` 型の `hello` というリソースの `output` 属性」という意味です(参照の書き方は lesson02 で詳しく見ます)

これを実際に plan すると、次の予告が出ます。

```text
  # terraform_data.hello will be created
  + resource "terraform_data" "hello" {
      + id     = (known after apply)
      + input  = "Hello, Terraform!"
      + output = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + message = (known after apply)
  + tool    = "IaC"
```

- 先頭の `+` は「新しく作る」の印です
- `(known after apply)` は「apply してみるまで値が決まらない」という意味です。`id`(Terraform が付ける識別番号)や `output` 属性は作ってから決まります
- `Plan: 1 to add, 0 to change, 0 to destroy.` は「1つ作る、0個変更、0個削除」の要約です

apply して output を表示すると、こうなります。

```text
message = "Hello, Terraform!"
tool = "IaC"
```

`名前 = 値` の形で1行ずつ出ます。文字列は `"..."` 付きで表示されます。表示順は**名前のアルファベット順**で、コードに書いた順ではありません(採点の期待出力もこの順です)。

この講座の「▶ 実行」ボタンは `terraform init`(準備)→ `terraform apply` → `terraform output` を一気に実行して、最後の output の表示を期待出力と比べています。

## ch02 HCLブロックの解剖

HCL のコードは**ブロック**(`resource "..." "..." { ... }` のようなひとまとまり)を並べて書きます。ファイルの中身は、ほぼブロックの並びだけです。

### ブロックの形

ブロックは「**種別** + **ラベル** + **本体** `{ }`」でできています。

```hcl
resource "terraform_data" "web" {  # 種別 resource + ラベル2つ
  input = "hello"                  # 引数: 名前 = 式
}

output "name" {  # 種別 output + ラベル1つ
  value = "web"
}
```

| 部品 | 上の例では | 意味 |
|---|---|---|
| 種別 | `resource`、`output` | 何のブロックか。先頭の単語で、引用符で囲まない |
| ラベル | `"terraform_data"` `"web"`、`"name"` | ブロックに付ける名前。`"..."` で囲む。数は種別ごとに決まっている |
| 本体 | `{` から `}` まで | そのブロックの設定を書く場所 |

ラベルの数は種別で決まっています。`resource` は2つ(型と名前)、`output` や後で学ぶ `variable` は1つです。実務コードを読むときは「resource はラベル2つ、variable や output はラベル1つ」という対応を押さえると構造が一気に見えるようになります。

### 引数と式

本体の中には `名前 = 式` の形で**引数**(argument。ブロックに渡す設定値)を書きます。

- `=` の左が引数の名前(`input`、`value` など)。どんな名前が使えるかはブロックの種別やリソースの型で決まっています。`output` ブロックなら `value`、`terraform_data` なら `input` です
- `=` の右が**式**(expression。値を作る書き方)

式にはいろいろな形があります。

| 式の例 | 種類 |
|---|---|
| `"hello"` | 文字列のリテラル(**リテラル**は値をそのまま書いたもの) |
| `3` | 数値のリテラル |
| `true` | 真偽値(true か false)のリテラル |
| `terraform_data.web.output` | 参照(別のリソースの値を使う。lesson02) |

1行に引数は1つです。行末にセミコロンやカンマは付けません。

### コメント

`#` から行末まではコメントで、実行には影響しません。`//` も同じ1行コメントです。`/*` から `*/` までは複数行をまとめてコメントにできます。実務では `#` が主流です。

### サンプルを1行ずつ

```hcl
resource "terraform_data" "web" {     # 種別 resource、ラベル1つ目(型)terraform_data、2つ目(名前)web
  input = "block-anatomy"             # 引数 input に文字列リテラルを入れる
}

// コメントは # のほかに // も使えます  ← この行は実行されない

output "web_input" {                  # 種別 output、ラベル web_input
  value = terraform_data.web.output   # 式が参照: web リソースの output 属性
}

output "block_type" {                 # 種別 output、ラベル block_type
  value = "resource"                  # 式が文字列リテラル
}
```

実行すると output が名前のアルファベット順(`block_type` → `web_input`)に表示されます。

```text
block_type = "resource"
web_input = "block-anatomy"
```

🔴 ブロックの形は今後すべての土台なので、手が覚えるまで書きましょう。

## ch03 planとapplyとstate

### 3つのコマンドと state

Terraform は3つのコマンドを順に使います。

```sh
terraform init   # 初期化(最初の1回)
terraform plan   # 変更の予告(まだ何も変えない)
terraform apply  # 反映して state に記録
```

- `terraform init`: そのフォルダで Terraform を使う準備をします。必要な**プロバイダ**(AWS などを操作するためのプラグイン。lesson12)をダウンロードします。最初の1回と、使うプロバイダを変えたときに実行します
- `terraform plan`: コードと現在の状態を比べて、何が作成・変更・削除されるかを表示します。まだ何も変えません
- `terraform apply`: plan と同じ予告を出したあと、実際に反映します

apply の結果は **state**(terraform.tfstate というファイル。Terraform が「今なにを管理していて、どんな値になっているか」を記録したもの)に保存されます。次回の plan は「コード」と「state」の差分から計算されます。

### 2回目の apply で何が起きるか

サンプルを2回続けて apply すると、表示はこう変わります。

1回目(state が空なので、作る):

```text
terraform_data.tracked: Creating...
terraform_data.tracked: Creation complete after 0s [id=...]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

2回目(state に記録済みで、コードも変わっていないので、何もしない。`Refreshing state` は state の記録を読み直している表示):

```text
terraform_data.tracked: Refreshing state... [id=...]

No changes. Your infrastructure matches the configuration.
```

`No changes. Your infrastructure matches the configuration.` は「インフラはコードどおりになっています」という意味です。これが lesson01 ch01 で見た冪等性です。

コードの `input` を `"stateで管理v2"` に書き換えて plan すると、今度は次のような予告になります。

```text
  # terraform_data.tracked will be updated in-place
  ~ resource "terraform_data" "tracked" {
        id     = "..."
      ~ input  = "stateで管理" -> "stateで管理v2"
      ~ output = "stateで管理" -> (known after apply)
    }

Plan: 0 to add, 1 to change, 0 to destroy.
```

`will be updated in-place` は「作り直さずに、その場で値を書き換える」という意味です。plan の行頭の印は次のとおりです。

| 印 | 意味 |
|---|---|
| `+` | 作成 |
| `-` | 削除 |
| `~` | その場で変更(`変更前 -> 変更後`) |
| `-/+` | 作り直し(いったん消して作る。`must be replaced` と表示される) |

本物のリソースには「この設定を変えると作り直しになる」ものがあり(例: サーバーの種類を変えるとサーバーを作り直す)、そのときは `-/+` と `# forces replacement` という注記が付きます。実務では plan のこの印を必ず確認します。

### この講座の「▶ 実行」

「▶ 実行」ボタンは `terraform init` → `terraform apply` → `terraform output`(output ブロックの値を表示)を一気に実行しています。実行のたびに新しい空のフォルダを使うので、前回の state は残りません(毎回「1回目の apply」になります)。実務では apply の前に必ず plan を見て確認します。実務では state を S3 などのリモートに置いてチームで共有するのが定番です(詳しくは lesson12)。

🟡 まずは「plan は予告、apply は反映、state は記録」という役割分担を理解しましょう。

### サンプルの読み方

```hcl
resource "terraform_data" "tracked" {   # 管理したいリソース(apply 後に state に記録される)
  input = "stateで管理"
}

output "tracked" {                       # apply 後に tracked リソースの output 属性を表示
  value = terraform_data.tracked.output
}

output "cycle" {                         # 文字列をそのまま表示
  value = "init-plan-apply"
}
```

実行結果(名前のアルファベット順):

```text
cycle = "init-plan-apply"
tracked = "stateで管理"
```
