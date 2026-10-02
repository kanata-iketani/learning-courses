# lesson05 ch02 演習: コレクション関数（length・concat・contains ほか）

variable `azs`(default `["ap-northeast-1a", "ap-northeast-1c"]`)と `extra_azs`(default `["ap-northeast-1d"]`)を宣言し、2つを連結したリストを locals に置いて、次の3つを出力してください。

- output `all`: 連結したリストを `,` 区切りで join した文字列
- output `az_count`: 連結後の要素数
- output `has_1a`: 連結後のリストに `"ap-northeast-1a"` が含まれるかどうか

**期待出力**

```text
all = "ap-northeast-1a,ap-northeast-1c,ap-northeast-1d"
az_count = 3
has_1a = true
```
