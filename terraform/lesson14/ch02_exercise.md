# lesson14 ch02 演習: リファクタの痕跡を読む

count → for_each 移行の moved ブロックに書かれる「移行前後のアドレス」を for 式で並べてください。

variable `names`(default `["blue", "green"]`)を定義し、

- output `new_addresses`: for_each 移行後の `terraform_data.web["<名前>"]` 形式を `", "` で連結
- output `old_addresses`: count 時代の `terraform_data.web[<添字>]` 形式(添字は 0 から)を `", "` で連結

を出力してください。

(ヒント: for 式は `[for i, n in var.names : ...]` と書くと添字も取れます。文字列内の `"` は `\"` でエスケープします)

**期待出力**

```text
new_addresses = "terraform_data.web[\"blue\"], terraform_data.web[\"green\"]"
old_addresses = "terraform_data.web[0], terraform_data.web[1]"
```
