# lesson07 ch01 演習: countとcount.index — 連番リソース

variable `node_count`(default `4`)を宣言し、`terraform_data` リソース `node` を `count = var.node_count` で作成、`input` には `node-0` のように `count.index` をそのまま使った名前を設定してください。そのうえで次の3つを出力してください。

- output `all_nodes`: 全ノードの `output` 属性を `,` 区切りで join した文字列
- output `last`: 最後のノード(`[3]`)の `output` 属性
- output `total`: `length` で数えたノードの個数

**期待出力**

```text
all_nodes = "node-0,node-1,node-2,node-3"
last = "node-3"
total = 4
```
