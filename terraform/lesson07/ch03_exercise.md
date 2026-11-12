# lesson07 ch03 演習: countの落とし穴 — indexのずれ

index のずれを出力で確認します。variable `before`(default `["app-a", "app-b", "app-c"]`)と、そこから真ん中を消した variable `after`(default `["app-a", "app-c"]`)を宣言してください。それぞれから `terraform_data` リソース `before` / `after` を `count = length(...)` で作り、`input` には `format("%d:%s", count.index, 要素)` で「index:名前」を設定して、次の2つを出力してください。

- output `after_pairs`: after 側の全 `output` 属性を半角スペース区切りで join した文字列(`app-c` の index が繰り上がることを確認)
- output `before_pairs`: before 側の全 `output` 属性を半角スペース区切りで join した文字列

(補足: `var.before[count.index]` は「before リストの count.index 番目の要素」です。`%d` に index(整数)、`%s` に名前(文字列)が入ります。▶実行は毎回まっさらな状態から作るので作り直しは起きませんが、2つの出力を見比べると、本文の plan で `app-c` に当たるリソースの番号がずれて変更・削除の対象になる理由がわかります)

**期待出力**

```text
after_pairs = "0:app-a 1:app-c"
before_pairs = "0:app-a 1:app-b 2:app-c"
```
