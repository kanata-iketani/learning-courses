# lesson02 ch02 演習: リソース参照 型.名前.属性

`terraform_data` リソース `origin` を作り、`input` に `"参照元"` を設定してください。さらに output ブロックを2つ書きます。

- output `from_resource`: リソース `origin` の `output` 属性を**参照**で表示
- output `ref_style`: 文字列 `"型.名前.属性"` を表示

**期待出力**

```text
from_resource = "参照元"
ref_style = "型.名前.属性"
```
