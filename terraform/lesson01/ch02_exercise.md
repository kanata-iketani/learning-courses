# lesson01 ch02 演習: HCLブロックの解剖

`terraform_data` リソース `note` を作り、`input` に `"HCLは宣言的"` を設定してください。さらに output ブロックを2つ書きます。

- output `note`: リソース `note` の `output` 属性を表示
- output `kind`: 文字列 `"resource"` を表示

`#` のコメントで「ここがラベル」など自分用のメモも1行入れてみましょう(採点には影響しません)。

**期待出力**

```text
kind = "resource"
note = "HCLは宣言的"
```
