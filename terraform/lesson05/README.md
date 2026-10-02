# Lesson 05 関数

HCL には値を加工するための組み込み関数が多数用意されています。このレッスンでは文字列・コレクション・マップ操作の定番関数を演習し、実務コードに頻出する「名前の組み立て」や「タグの merge」を読める状態を目指します。

## ch01 文字列関数（format・join・split ほか）

**組み込み関数**(Terraform に最初から用意されている、値を加工するための関数)のうち、まずは文字列系を押さえます。`format` は printf 風の文字列組み立て、`join` はリストを区切り文字でつないだ文字列に、`split` は逆に文字列をリストに分解します。`replace` は置換、`lower` / `upper` は大文字小文字の変換です。実務ではリソース名やバケット名を `format("%s-%s", var.project, var.env)` のように変数から組み立てるコードが最頻出です。🔴 この5つは読めないと実務コードが追えないので、必ず手を動かして覚えましょう。

```hcl
locals {
  name  = format("%s-%s", "myapp", lower("Prod"))  # "myapp-prod"
  parts = split("-", local.name)                    # ["myapp", "prod"]
}
```

## ch02 コレクション関数（length・concat・contains ほか）

リストやマップを扱うコレクション関数です。`length` は要素数、`concat` は複数のリストの連結、`contains` は要素が含まれるかの真偽値を返します。マップに対しては `keys` がキーの一覧を、`values` が値の一覧を(どちらも**キーのアルファベット順**で)返します。実務では「共通のサブネットリストに追加分を concat する」「対象環境かどうかを contains で判定する」といった形で登場します。🔴 特に keys / values の並びがアルファベット順に揃う点は、出力やリソースの並びを読むときの前提知識になります。

```hcl
locals {
  azs = concat(["ap-northeast-1a"], ["ap-northeast-1c"])  # 連結
  n   = length(local.azs)                                  # 2
  ok  = contains(local.azs, "ap-northeast-1a")             # true
}
```

## ch03 lookupとmerge — タグの合成

`merge` は複数のマップを合成する関数で、**同じキーは後に書いたマップが勝ちます**。`lookup(マップ, キー, 既定値)` はキーがあればその値を、なければ既定値を返します。実務ではこの2つが**タグの合成**として最頻出です。全リソース共通の `local.common_tags` に、リソース個別の `Name` タグなどを `merge` で重ねる書き方は、ほぼどの現場のコードにも登場します。🔴 「後勝ち」のルールを知らないと、環境タグを上書きしているコードを読み違えるので必ず押さえてください。

```hcl
tags = merge(local.common_tags, {
  Name = "myapp-api"   # 共通タグに個別の Name を追加
})
```

## ch04 try・coalesce・jsonencode — 壊れにくい書き方

値が「無いかもしれない」場面を安全に扱う関数です。`try(式, 既定値)` は式の評価が失敗したら既定値に倒します。`coalesce(a, b, ...)` は null と空文字 `""` を飛ばして最初に値があるものを返します。`jsonencode` は HCL の値を JSON 文字列に変換する関数で、IAM ポリシーなど「JSON をそのまま書く」設定で多用されます。🟡 実務コードでは `try(var.cfg["port"], "8080")` のように、キーが無くてもエラーにしない防御的な書き方として頻出します。読めれば十分ですが、意図(既定値へのフォールバック)まで取れるようにしましょう。

```hcl
locals {
  port    = try(var.cfg["port"], "8080")       # キーが無ければ "8080"
  display = coalesce(var.nickname, "anonymous") # "" なら "anonymous"
}
```
