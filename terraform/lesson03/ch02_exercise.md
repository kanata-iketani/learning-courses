# lesson03 ch02 演習: 型いろいろ

variable を3つ定義してください。

1. `ports`: `type` は `list(number)`、`default` は `[80, 443]`
2. `tags`: `type` は `map(string)`、`default` は `{ env = "dev" }`
3. `debug`: `type` は `bool`、`default` は `false`

さらに output を3つ書きます。

- `debug_mode`: `var.debug` を表示
- `env_tag`: `var.tags` の `"env"` キーの値を表示
- `first_port`: `var.ports` の先頭要素を表示

(ヒント: list の先頭は `[0]` です。map の要素は `var.tags["env"]` のように、`[ ]` の中のキーを引用符で囲みます。output は名前のアルファベット順に表示されるので、期待出力は debug_mode → env_tag → first_port の順です)

**期待出力**

```text
debug_mode = false
env_tag = "dev"
first_port = 80
```
