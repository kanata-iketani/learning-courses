# Lesson 07 count

count は「同じリソースを N 個」作るためのメタ引数です。連番作成と、`条件 ? 1 : 0` によるリソースのオンオフという実務頻出パターン、そして index ずれという落とし穴までを扱います。

## ch01 countとcount.index — 連番リソース

### count とメタ引数

これまでの resource ブロックは、1つ書くとリソースが1つできました。**count**(リソースを指定した個数まとめて作るメタ引数)を使うと、同じ定義から N 個のリソースを作れます。

**メタ引数**とは、リソースの種類によらず使える共通の引数のことです。`input` は `terraform_data` 専用の引数ですが、`count` は `terraform_data` にも `aws_instance` にも、どのリソースにも書けます(lesson08 の `for_each` もメタ引数です)。

```hcl
resource "terraform_data" "web" {
  count = 3                                     # このブロックから 3 個作る
  input = format("web-%02d", count.index + 1)   # 1個ごとに違う値にする
}
```

### count.index

count を書いたブロックの中では **`count.index`**(今作っているのが何個目か。0 始まりの番号)が使えます。3 個作るなら 0, 1, 2 の3回、ブロックの中身がそれぞれの番号で評価されます。

| 何個目 | count.index | count.index + 1 | format("web-%02d", ...) |
|---|---|---|---|
| 1個目 | 0 | 1 | `"web-01"` |
| 2個目 | 1 | 2 | `"web-02"` |
| 3個目 | 2 | 3 | `"web-03"` |

`%02d` は lesson06 で見た「整数を2桁で、足りなければ 0 で埋める」指定です。0 始まりのままだと名前が `web-00` から始まるので、`+ 1` して 1 始まりの連番にするのが定番です。

### できたリソースはリストになる

count を付けたリソースは、1つのリソースではなく**リスト**になります。plan を見ると、名前の後ろに `[0]` `[1]` `[2]` が付いた3つのリソースが作られる予告が出ます。

```text
  # terraform_data.web[0] will be created
  + resource "terraform_data" "web" {
      + id     = (known after apply)
      + input  = "web-01"
      + output = (known after apply)
    }

  # terraform_data.web[1] will be created
  + resource "terraform_data" "web" {
      + id     = (known after apply)
      + input  = "web-02"
      + output = (known after apply)
    }

  # terraform_data.web[2] will be created
  + resource "terraform_data" "web" {
      + id     = (known after apply)
      + input  = "web-03"
      + output = (known after apply)
    }

Plan: 3 to add, 0 to change, 0 to destroy.
```

`terraform_data.web[0]` が「web の 0 番目」です。state(lesson01)にもこの番号付きの名前で記録されます。そのため参照するときも番号を付けます。

| 書き方 | 意味 | サンプルでの値 |
|---|---|---|
| `terraform_data.web[0].output` | 0 番目の output 属性(index 参照) | `"web-01"` |
| `terraform_data.web[*].output` | 全要素の output 属性のリスト(lesson06 で見た splat) | `["web-01", "web-02", "web-03"]` |
| `length(terraform_data.web)` | 作られた個数 | `3` |

count 付きのリソースを `terraform_data.web.output` のように番号なしで参照するとエラーになります。必ず `[番号]` か `[*]` を付けます。

```text
Error: Missing resource instance key

Because terraform_data.web has "count" set, its attributes must be accessed
on specific instances.
```

(「count が付いているので、属性は個々のインスタンス(番号付きの1個1個)から取ってください」という意味です)

### サンプルを1行ずつ

```hcl
variable "replicas" {
  default = 3                                   # 作る個数を変数にしておく
}

resource "terraform_data" "web" {
  count = var.replicas                          # 個数 = 変数の値(3)
  input = format("web-%02d", count.index + 1)   # web-01, web-02, web-03
}

output "first" {
  value = terraform_data.web[0].output          # 0 番目だけ
}

output "all" {
  value = join(",", terraform_data.web[*].output)   # 全部を , でつなぐ
}
```

**レプリカ**(replica)は「同じものの複製」という意味で、同じ構成のサーバーを何台並べるか、という場面でよく使う変数名です。`count = var.replicas` のように個数を変数にしておくと、コードを書き換えずに台数を変えられます。実行結果です。

```text
all = "web-01,web-02,web-03"
first = "web-01"
```

### 実務での読み方

🔴 実務では **EC2**(AWS の仮想サーバー。`aws_instance` 型で作る)や**サブネット**(lesson06 で見た VPC 内の小さなネットワーク)の複数作成で頻出です。

```hcl
resource "aws_instance" "web" {
  count = 3                                               # サーバーを 3 台作る
  tags  = { Name = format("web-%02d", count.index + 1) }  # 読解例
}
```

- `count = 3`: このブロックから EC2 を 3 台作ります
- `tags`: **タグ**(リソースに付ける「キー = 値」のラベル)のマップです。AWS のコンソールでは `Name` タグの値がサーバーの表示名になります
- 結果として `web-01` `web-02` `web-03` という名前の3台ができ、Terraform 上は `aws_instance.web[0]` 〜 `aws_instance.web[2]` として管理されます

`[*]` 参照とセットで読めるようにしましょう。

## ch02 count = 条件 ? 1 : 0 — オンオフパターン

### `? 1 : 0` で作る・作らないを切り替える

`count = var.enabled ? 1 : 0` は「フラグが true のときだけリソースを作る」ための定番イディオム(よく使われる決まった書き方)で、実務コードで極めてよく見ます。**フラグ**は true / false でオン・オフを表す変数のことです。

分解すると、lesson04 で見た**条件式**(`条件 ? 真のときの値 : 偽のときの値`)と ch01 の count の組み合わせです。

| var.enabled | 条件式の結果 | count | 作られるリソース |
|---|---|---|---|
| `true` | `1` | 1 | 1個(`[0]` だけ) |
| `false` | `0` | 0 | なし(空のリスト) |

count に 0 を入れると「0 個作る」、つまり作りません。リソース1個を丸ごとオン・オフするスイッチとして使えるわけです。実務では、監視をオプションにする、環境によって**バックアップ**(データの控え)の有無を変える、などで使います。

### サンプルを1行ずつ

```hcl
variable "enable_backup" {
  default = true                               # バックアップはオン
}

variable "enable_debug" {
  default = false                              # デバッグはオフ
}

resource "terraform_data" "backup" {
  count = var.enable_backup ? 1 : 0            # true なので count = 1
  input = "backup-plan"
}

resource "terraform_data" "debug" {
  count = var.enable_debug ? 1 : 0             # false なので count = 0(作らない)
  input = "debug-agent"
}
```

plan を見ると、作られる予告が出るのは `backup[0]` だけです。`debug` は一切出てきません。

```text
  # terraform_data.backup[0] will be created
  + resource "terraform_data" "backup" {
      + id     = (known after apply)
      + input  = "backup-plan"
      + output = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.
```

### 「無いかもしれない」リソースを参照する

count が 0 のリソースは空のリストになります。空のリストに `[0]` を付けると、0 番目の要素が存在しないのでエラーになります。たとえば `value = terraform_data.debug[0].output` と書くと、次のエラーで止まります。

```text
Error: Invalid index

    │ terraform_data.debug is empty tuple

The given key does not identify an element in this collection value: the
collection has no elements.
```

(`empty tuple` は「空の並び」、メッセージ全体は「要素が1つも無いので、その番号の要素はありません」という意味です)

そこで参照側は、lesson05 で見た **`try`**(1つ目の式がエラーになったら、2つ目の値を返す関数)で「無いかもしれない」前提で書きます。

```hcl
# count = 0 のリソースは空リストになります
output "backup_count" {
  value = length(terraform_data.backup)                      # 作られた個数(1 か 0)
}

# 「無いかもしれない」ものは try で既定値に倒して参照します
output "backup_name" {
  value = try(terraform_data.backup[0].output, "(none)")     # ある → その値
}

output "debug_name" {
  value = try(terraform_data.debug[0].output, "(none)")      # 無い → "(none)"
}
```

| output | 1つ目の式 | 結果 |
|---|---|---|
| `backup_name` | `terraform_data.backup[0].output` は `"backup-plan"` | `"backup-plan"` |
| `debug_name` | `terraform_data.debug[0].output` はエラー | 既定値 `"(none)"` |

実行結果です。

```text
backup_count = 1
backup_name = "backup-plan"
debug_name = "(none)"
```

フラグを切り替えるだけで、作るリソースも output も変わります。たとえば `enable_debug` を true にすれば `debug[0]` が作られ、`debug_name` は `"debug-agent"` になります。

### 実務での読み方

```hcl
resource "aws_cloudwatch_metric_alarm" "cpu" {
  count = var.enable_monitoring ? 1 : 0   # 読解例: フラグで作成を切替
}
```

`aws_cloudwatch_metric_alarm` は **CloudWatch**(AWS の監視サービス)の**アラーム**(CPU 使用率などの数値がしきい値を超えたら通知する設定)です。この1行で「`enable_monitoring` が true の環境(たとえば本番)だけ CPU のアラームを作る」と読めます。

🔴 `? 1 : 0` を見たら「このリソースはフラグでオンオフされる」と即読みできることが読解の鍵です。参照側に `[0]` と `try` がセットで出てくるのも、この形の目印です。

## ch03 countの落とし穴 — indexのずれ

### count のリソースは「番号」で区別される

ch01 で見たとおり、count で作ったリソースは `terraform_data.member[0]`、`[1]`、`[2]` のように**番号(index)付きの名前**で state(lesson01 で見た、Terraform の管理記録)に記録されます。Terraform が「どのリソースがどれか」を見分ける手がかりは、この番号だけです。中身の値(`"kato"` など)ではありません。

そのため、リストの**真ん中の要素を消すと後ろの要素の index が全部ずれ**ます。Terraform から見ると「`[1]` の中身が別のものに変わった」「`[2]` が要らなくなった」ことになり、本来は触る必要のないリソースまで変更・削除の対象になります。

### 小さな具体例

```hcl
# members = ["ito", "kato", "sato"] から "kato" を消すと…
# terraform_data.member[1] の中身が kato → sato に変わり、member[2] は削除される
resource "terraform_data" "member" {
  count = length(var.members)          # 要素数だけ作る(3 個)
  input = var.members[count.index]     # count.index 番目の名前を入れる
}
```

`var.members[count.index]` は「members リストの count.index 番目の要素」です。`"kato"` を消す前と後で、番号と中身の対応は次のように変わります。

| 番号 | 消す前 | 消した後 | Terraform の判断 |
|---|---|---|---|
| `[0]` | ito | ito | 変化なし |
| `[1]` | kato | **sato** | 中身が変わった → 変更 |
| `[2]` | sato | (無い) | 番号が範囲外 → **削除** |

本当にやりたいのは「kato を消す」だけです。しかし Terraform は「kato を消す」とは考えず、「`[1]` を sato に書き換え、`[2]`(元の sato)を削除する」と計画します。

### 実際の plan

3人で apply したあと `"kato"` を消して plan すると、実際に次の予告が出ます。

```text
  # terraform_data.member[1] will be updated in-place
  ~ resource "terraform_data" "member" {
        id     = "..."
      ~ input  = "kato" -> "sato"
      ~ output = "kato" -> (known after apply)
    }

  # terraform_data.member[2] will be destroyed
  # (because index [2] is out of range for count)
  - resource "terraform_data" "member" {
      - id     = "..." -> null
      - input  = "sato" -> null
      - output = "sato" -> null
    }

Plan: 0 to add, 1 to change, 1 to destroy.
```

- `will be updated in-place`: その場で値を書き換える(lesson01 で見た `~` の印)
- `will be destroyed` / `(because index [2] is out of range for count)`: 「count が 2 になったので、番号 [2] は範囲外。だから削除する」という意味です(`-> null` は「値が無くなる」)

`terraform_data` は input を変えても作り直さず、その場で書き換えるリソースなので、`[1]` は「変更」で済んでいます。

### 本物のリソースでは「作り直し」になる

AWS のリソースには「この設定を変えると作り直しになる」ものが多くあります(lesson01 で見た `-/+` と `must be replaced`)。たとえば S3 バケットの名前や、データベースの識別名がそうです。`terraform_data` でも `triggers_replace`(この値が変わったら作り直す、という指定の引数)に名前を入れると同じ状況を再現できます。

```hcl
resource "terraform_data" "member" {
  count            = length(var.members)
  input            = var.members[count.index]
  triggers_replace = var.members[count.index]   # 名前が変わったら作り直す
}
```

これで同じように `"kato"` を消すと、plan はこうなります。

```text
  # terraform_data.member[1] must be replaced
-/+ resource "terraform_data" "member" {
      ~ id               = "..." -> (known after apply)
      ~ input            = "kato" -> "sato"
      ~ output           = "kato" -> (known after apply)
      ~ triggers_replace = "kato" -> "sato"
    }

  # terraform_data.member[2] will be destroyed
  # (because index [2] is out of range for count)

Plan: 1 to add, 0 to change, 2 to destroy.
```

元の sato(`[2]`)は削除され、`[1]` は sato として消して作り直されます。中身は同じ sato なのに、いったん消えて作り直されるわけです。データベースなどで起きると、中のデータが消える事故につながります。

### 実務の定石

このため実務では「要素の増減があり得る集まりに count を使わない」のが定石で、これが次レッスンの for_each(番号ではなくキーの名前でリソースを区別する仕組み)が好まれる理由です。count が安全なのは、ch02 の `? 1 : 0` のように 0 個か 1 個かを切り替えるときや、「同じものを N 台」のように個々に区別が要らないときです。

### サンプルを1行ずつ

```hcl
resource "terraform_data" "member" {
  count = length(var.members)
  input = format("%d:%s", count.index, var.members[count.index])   # 「番号:名前」を記録
}

output "pairs" {
  value = join(" ", terraform_data.member[*].output)   # 全要素を半角スペースでつなぐ
}

output "member_count" {
  value = length(terraform_data.member)                # 作られた個数
}
```

`format("%d:%s", ...)` の `%d` には番号(整数)、`%s` には名前(文字列)が入ります。実行結果です。

```text
member_count = 3
pairs = "0:ito 1:kato 2:sato"
```

ito は `[0]`、kato は `[1]`、sato は `[2]` に対応しています。ここから kato を消すと sato が `[1]` に繰り上がり、上の plan のとおり `[1]` の書き換えと `[2]` の削除が計画されます。

🟡 plan 結果に大量の destroy や思ってもいない変更が出たら、まず index ずれを疑ってください。
