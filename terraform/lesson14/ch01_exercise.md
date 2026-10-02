# lesson14 ch01 演習: 同じ構成の2流儀読み比べ

フラット派とモジュール派、どちらの書き方でも同じバケット名になることを確認します。variable `project`(default `"skillax"`)と `env`(default `"prod"`)を定義し、`<project>-<env>-logs` を2通りで組み立ててください。

- output `flat_name`: locals でその場で組み立てた名前
- output `module_name`: モジュール `./modules/naming`(入力 `project` / `env`、出力 `bucket_name`)を呼び出した結果
- output `same_result`: 2つが等しければ `yes`(条件式で)

モジュールは `# === file: modules/naming/main.tf ===` という区切り行で同じエディタ内に書けます。

**期待出力**

```text
flat_name = "skillax-prod-logs"
module_name = "skillax-prod-logs"
same_result = "yes"
```
