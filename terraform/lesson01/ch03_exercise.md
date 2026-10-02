# lesson01 ch03 演習: planとapplyとstate

`terraform_data` リソース `tracked` を作り、`input` に `"stateで管理"` を設定してください。さらに output ブロックを2つ書きます。

- output `cycle`: 文字列 `"plan-apply"` を表示
- output `tracked`: リソース `tracked` の `output` 属性を表示

書けたら「▶ 実行」を2回押してみてください。2回目も同じ結果になります(state に記録済みなので差分がありません)。

**期待出力**

```text
cycle = "plan-apply"
tracked = "stateで管理"
```
