# lesson02 ch04 演習: dataソースの読み方

AMI ID を data ソースで調べて使う構図を、`terraform_data` で再現します。

1. `terraform_data` リソース `registry` を作り、`input` に `"ami-12345678"` を設定(既存の値を読んだ想定)
2. output `ami_id` でリソース `registry` の `output` 属性を参照で表示
3. output `readonly` で bool 値 `true` を表示(data ソースは読むだけ、の意味)

**期待出力**

```text
ami_id = "ami-12345678"
readonly = true
```
