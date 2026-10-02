# lesson06 ch04 演習: splat[*]とflatten — ネストの平坦化

variable `vpcs` を type `list(object({ name = string, subnets = list(string) }))`、default を

```hcl
[
  { name = "main", subnets = ["10.0.1.0/24", "10.0.2.0/24"] },
  { name = "edge", subnets = ["10.9.1.0/24"] },
]
```

として宣言し、次の3つを出力してください。

- output `subnet_count`: 全 VPC のサブネットを平坦化したリストの要素数
- output `subnets`: 平坦化したサブネットのリストを `,` 区切りで join した文字列
- output `vpc_names`: splat で取り出した VPC 名を `,` 区切りで join した文字列

**期待出力**

```text
subnet_count = 3
subnets = "10.0.1.0/24,10.0.2.0/24,10.9.1.0/24"
vpc_names = "main,edge"
```
