# Lesson 07 count

count は「同じリソースを N 個」作るためのメタ引数です。連番作成と、`条件 ? 1 : 0` によるリソースのオンオフという実務頻出パターン、そして index ずれという落とし穴までを扱います。

## ch01 countとcount.index — 連番リソース

**count**(リソースを指定した個数まとめて作るメタ引数)を使うと、同じ定義から N 個のリソースを作れます。**メタ引数**とはリソースの種類によらず使える共通の引数のことです。ブロック内では `count.index` で 0 始まりの番号が使え、`format("web-%02d", count.index + 1)` のような連番名の組み立てが定番です。作られたリソースは**リスト**になるため、`リソース[0]` の index 参照や `リソース[*].属性` の splat 参照で読み書きします。🔴 実務では EC2 やサブネットの複数作成で頻出です。`[*]` 参照とセットで読めるようにしましょう。

```hcl
resource "aws_instance" "web" {
  count = 3
  tags  = { Name = format("web-%02d", count.index + 1) }  # 読解例
}
```

## ch02 count = 条件 ? 1 : 0 — オンオフパターン

`count = var.enabled ? 1 : 0` は「フラグが true のときだけリソースを作る」ための定番イディオムで、実務コードで極めてよく見ます(監視をオプションにする、環境によってバックアップの有無を変える、など)。count が 0 ならリソースはリストとして空になるため、参照側は `try(リソース[0].output, "既定値")` のように「無いかもしれない」前提で書きます。🔴 `? 1 : 0` を見たら「このリソースはフラグでオンオフされる」と即読みできることが読解の鍵です。

```hcl
resource "aws_cloudwatch_metric_alarm" "cpu" {
  count = var.enable_monitoring ? 1 : 0   # 読解例: フラグで作成を切替
}
```

## ch03 countの落とし穴 — indexのずれ

count のリソースは「リストの何番目か」で管理されます。そのため、リストの**真ん中の要素を消すと後ろの要素の index が全部ずれ**、Terraform は「別のリソースになった」とみなして削除と作り直し(destroy / create)を計画します。たとえば `["a", "b", "c"]` から `"b"` を消すと、`c` は index 2 から 1 に移動し、中身は同じなのに作り直しの対象になります。データベースなどで起きると事故につながるため、実務では「要素の増減があり得る集まりに count を使わない」のが定石で、これが次レッスンの for_each が好まれる理由です。🟡 plan 結果に大量の destroy が出たら、まず index ずれを疑ってください。

```hcl
# members = ["ito", "kato", "sato"] から "kato" を消すと…
# terraform_data.member[1] は kato → sato に変わり、sato が作り直しになる
resource "terraform_data" "member" {
  count = length(var.members)
  input = var.members[count.index]
}
```
