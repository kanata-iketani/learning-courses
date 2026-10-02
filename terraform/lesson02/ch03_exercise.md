# lesson02 ch03 演習: 複数リソースのチェーン

リソースを2つ作り、参照でつないでください。

1. `terraform_data` リソース `network`: `input` に `"vpc-main"` を設定
2. `terraform_data` リソース `server`: `input` にリソース `network` の `output` 属性を**参照**で設定

さらに output `network_name` で `network` の `output` 属性を、output `server_network` で `server` の `output` 属性を表示してください。

**期待出力**

```text
network_name = "vpc-main"
server_network = "vpc-main"
```
