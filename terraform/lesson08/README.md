# Lesson 08 for_each

for_each はコレクションの要素ごとにリソースを作るメタ引数で、現場では count よりも好まれることが多い書き方です。set / map それぞれでの使い方、作られたリソースの参照方法、count との使い分けの流儀を学びます。

## ch01 setでfor_each — each.value

**for_each**(コレクションの要素ごとにリソースを1つずつ作るメタ引数)は、count と並ぶ「複数リソース作成」の道具です。リストはそのまま渡せないため、`toset`(リストを集合に変換する関数)で set にして渡します。ブロック内では `each.value` で今の要素を参照します。作られたリソースは index ではなく**要素の値をキーとするマップ**になるため、count のような index ずれが起きません。🔴 実務では IAM ユーザーや S3 バケットなど「名前の集まりから同種のリソースを並べる」場面の標準形です。`for_each = toset(...)` を見たら要素ごとの複製と読んでください。

```hcl
resource "aws_iam_user" "member" {
  for_each = toset(var.user_names)   # 読解例: 名前ごとにユーザーを作成
  name     = each.value
}
```

## ch02 mapでfor_each — each.keyとeach.value

for_each にマップを渡すと、要素ごとに `each.key`(キー)と `each.value`(値)の両方が使えます。「名前 → 設定値」というマップから、名前と設定を同時に使ってリソースを組み立てられるため、set よりも表現力が高い形です。実務では `{ web = "t3.small", api = "t3.medium" }` のような「インスタンス名 → タイプ」のマップから EC2 を並べる形が典型で、variable にマップを持たせて for_each で回すのは現場コードの最頻出パターンの1つです。🔴 each.key / each.value がそれぞれ何を指すかを即答できるようにしましょう。

```hcl
resource "aws_instance" "app" {
  for_each      = var.instances          # 読解例: 名前→タイプのマップ
  instance_type = each.value             # 値(タイプ)
  tags          = { Name = each.key }    # キー(名前)
}
```

## ch03 for_eachリソースの参照 — [キー]とvalues()

for_each で作ったリソースは**マップ**なので、count のような `[0]` の index 参照はできません。個別には `リソース["キー"]`、全要素まとめては `values(リソース)`(キーのアルファベット順の値リスト)にしてから splat で属性を取り出します。`values(terraform_data.queue)[*].output` のような形です。実務コードで `values(aws_subnet.private)[*].id` といった参照を見たら「for_each で作った全サブネットの ID をリスト化している」と読めます。🟡 「for_each 化されたリソース = マップ」という頭の切り替えが、このレッスンの読解ポイントです。

```hcl
locals {
  subnet_ids = values(aws_subnet.private)[*].id   # 読解例: 全要素の id
  main_id    = aws_subnet.private["main"].id      # キーで個別参照
}
```

## ch04 countとfor_eachの使い分け — 現場の流儀

count と for_each はどちらも複数リソースを作りますが、現場では**キーの安定性**から for_each が好まれることが多いです。count は「リストの位置」で管理するため要素の増減で index がずれます(lesson07 参照)。for_each は「キー」で管理するため、途中の要素を消しても他のリソースに影響しません。使い分けの目安は「まったく同質な複製やオンオフ(`? 1 : 0`)は count、名前で区別できる集まりは for_each」です。ただしこれは流儀であり、既存コードベースの慣習に合わせるのが実務の基本です。🟡 コードレビューで「count を for_each にしませんか」という指摘は定番なので、理由を説明できるようにしましょう。

```hcl
# count 版(位置で管理)         # for_each 版(キーで管理・増減に強い)
count = length(var.envs)        for_each = toset(var.envs)
input = var.envs[count.index]   input    = each.value
```
