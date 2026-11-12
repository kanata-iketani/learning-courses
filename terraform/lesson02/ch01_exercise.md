# lesson02 ch01 演習: resourceの基本形とterraform_data

`terraform_data` リソース `server` を作り、`input` に `"web-01"` を設定してください。さらに output `server_name` でリソース `server` の `output` 属性を表示してください。

(ヒント: `output` ブロックの `value` に `terraform_data.server.output` と書きます。output の名前 `server_name` とリソースの名前 `server` は別のものなので、違っていてかまいません)

**期待出力**

```text
server_name = "web-01"
```
