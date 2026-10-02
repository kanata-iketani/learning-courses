# lesson12 ch03 演習: required_providersとバージョン制約

required_providers に `version = "5.67.3"` と完全固定されている構成がありました。このバージョン文字列を分解して読み取ります。

variable `provider_version`(default `"5.67.3"`)を定義し、`split(".", ...)` で分解して次を**数値**で出力してください。

- output `major`: メジャーバージョン
- output `minor`: マイナーバージョン
- output `patch`: パッチバージョン

(ヒント: split の結果は文字列のリストなので `tonumber()` で数値にします)

**期待出力**

```text
major = 5
minor = 67
patch = 3
```
