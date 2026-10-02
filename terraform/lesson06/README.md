# Lesson 06 for式とsplat

for式と splat([*])は、リストやマップを別の形に変換するための HCL の中心的な道具です。実務コードでは変数からリソース定義用のデータ構造を組み立てる場面で必ず登場します。読んで意味が取れるようになりましょう。

## ch01 リストのfor式 — [for x in ...]

**for式**(リストやマップの各要素を変換して、新しいリストやマップを作る式)のリスト版です。`[for x in var.list : 式]` で全要素に同じ変換をかけた新しいリストが得られます。`[for i, x in var.list : ...]` と書くと index も使えます。実務では「ユーザー名のリストからメールアドレスのリストを作る」「名前のリストからリソース定義用の値を組み立てる」という前処理として必ず登場します。🔴 なお、リストをそのまま output すると複数行の `tolist([...])` 形式で表示されます。この見た目にも慣れておきましょう。

```hcl
locals {
  upper_names = [for n in var.names : upper(n)]           # 全要素を大文字に
  hosts       = [for i, n in var.names : "${i}-${n}"]     # index 付き
}
```

## ch02 mapを作るfor式 — {for k, v in ...}

for式でマップを作るには `{for k, v in var.map : k => 変換式}` と波かっこで書きます。`k` にキー、`v` に値が入り、`=>` の右側が新しい値になります。リストから `{for x in var.list : x => 式}` とマップを作ることもでき、これは後のレッスンで学ぶ for_each の前処理として実務で多用されます。🔴 「`[...]` ならリストを作る for式、`{...}` と `=>` ならマップを作る for式」という見分け方を身につけると、実務コードの読解速度が大きく変わります。

```hcl
locals {
  # 値だけを変換した新しいマップ
  upper_sizes = { for k, v in var.sizes : k => upper(v) }
  # リスト → マップ(キー => 値 を自分で組み立てる)
  name_len = { for n in var.names : n => length(n) }
}
```

## ch03 ifでフィルタするfor式

for式の末尾に `if 条件` を付けると、条件を満たす要素だけを残せます。`[for x in var.list : x if 条件]` の形で、変換とフィルタを同時に行えます。実務では「本番用のリソースだけ」「特定のサフィックスを持つバケットだけ」を抜き出す前処理として頻出で、`endswith` / `startswith`(文字列が特定の接尾辞/接頭辞を持つかを返す関数)との組み合わせをよく見ます。🔴 for式に if が付いていたら「絞り込んでから使う」意図だと読めるようにしましょう。

```hcl
locals {
  prod_only = [for b in var.buckets : b if endswith(b, "-prod")]
}
```

## ch04 splat[*]とflatten — ネストの平坦化

**splat**(`[*]` で、オブジェクトのリストから特定の属性だけをまとめて取り出す記法)は `var.servers[*].name` のように書き、`[for s in var.servers : s.name]` の省略形です。取り出した結果がリストのリストになる場合は、`flatten`(ネストしたリストを1段のリストに平坦化する関数)と組み合わせます。実務では「全 VPC のサブネット ID を1本のリストにまとめる」ような場面で `flatten(var.vpcs[*].subnets)` の形をよく見ます。🟡 splat はリソース参照でも多用されるので、`[*]` を見たら「全要素の属性をまとめて取る」と読んでください。

```hcl
locals {
  names   = var.servers[*].name            # 属性だけをまとめて取り出す
  all_ips = flatten(var.servers[*].ips)    # リストのリストを平坦化
}
```
