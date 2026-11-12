# lesson07 ch01 演習: countとcount.index — 連番リソース

variable `node_count`(default `4`)を宣言し、`terraform_data` リソース `node` を `count = var.node_count` で作成、`input` には `node-0` のように `count.index` をそのまま使った名前を設定してください。そのうえで次の3つを出力してください。

- output `all_nodes`: 全ノードの `output` 属性を `,` 区切りで join した文字列
- output `last`: 最後のノード(`[3]`)の `output` 属性
- output `total`: `length` で数えたノードの個数

(ヒント: `format("node-%d", count.index)` の `%d` は「整数をそのまま入れる」指定です。count 付きリソースはリストなので、全要素の属性は `terraform_data.node[*].output`、4番目は `[3]`(0 始まり)、個数は `length(terraform_data.node)` で取れます)

**期待出力**

```text
all_nodes = "node-0,node-1,node-2,node-3"
last = "node-3"
total = 4
```
