# lesson01 ch01 演習: IaCとTerraformのサイクル

`terraform_data` リソース `greeting` を作り、`input` に `"Terraformをはじめます"` を設定してください。さらに output ブロック `greeting` でそのリソースの `output` 属性を表示してください。

(ヒント: リソースの値は `terraform_data.greeting.output` で参照できます)

**期待出力**

```text
greeting = "Terraformをはじめます"
```
