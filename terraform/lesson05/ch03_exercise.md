# lesson05 ch03 演習: lookupとmerge — タグの合成

variable `common_tags`(default `{ Env = "prod", Project = "skillax" }`)と `extra_tags`(default `{ Env = "stg", Name = "skillax-api" }`)を宣言し、`merge(共通, 個別)` の結果を locals に置いて、次の3つを出力してください。

- output `env`: 合成後の `Env` タグの値(後勝ちの確認)
- output `owner`: 合成後のマップから `lookup` で `Owner` キーを引く。無ければ `"unknown"`
- output `tag_keys`: 合成後のキー一覧を `,` 区切りで join した文字列

**期待出力**

```text
env = "stg"
owner = "unknown"
tag_keys = "Env,Name,Project"
```
