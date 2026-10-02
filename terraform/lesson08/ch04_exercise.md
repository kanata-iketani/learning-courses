# lesson08 ch04 演習: countとfor_eachの使い分け — 現場の流儀

次の count 版のコードを、キーの安定性が高い for_each 版に書き換えてください。

```hcl
variable "envs" {
  default = ["dev", "prod", "stg"]
}

resource "terraform_data" "env" {
  count = length(var.envs)
  input = format("env-%s", var.envs[count.index])
}
```

`terraform_data` リソース `env` を `for_each = toset(var.envs)` で作成し、`input` は count 版と同じ `env-要素名` の形にします。そのうえで次の2つを出力してください。

- output `env_keys`: 作られたリソースのキー一覧を `,` 区切りで join した文字列
- output `prod`: キー `"prod"` のリソースの `output` 属性

**期待出力**

```text
env_keys = "dev,prod,stg"
prod = "env-prod"
```
