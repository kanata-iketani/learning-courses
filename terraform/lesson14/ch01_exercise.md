# lesson14 ch01 演習: 同じ構成の2流儀読み比べ

フラット派とモジュール派、どちらの書き方でも同じバケット名になることを確認します。variable `project`(default `"myapp"`)と `env`(default `"prod"`)を定義し、`<project>-<env>-logs` を2通りで組み立ててください。

- output `flat_name`: locals でその場で組み立てた名前
- output `module_name`: モジュール `./modules/naming`(入力 `project` / `env`、出力 `bucket_name`)を呼び出した結果
- output `same_result`: 2つが等しければ `yes`(条件式で)

モジュールは `# === file: modules/naming/main.tf ===` という区切り行で同じエディタ内に書けます。

(ヒント)
- モジュール側には、入力の `variable` 2つと、名前を返す `output "bucket_name"` を書きます。サンプルのモジュール側とほぼ同じ形です
- 呼び出し側では `module.naming.bucket_name` でモジュールの出力を受け取ります(lesson10)
- `a == b` は「a と b が等しければ true」になる比較です。`条件 ? 真のときの値 : 偽のときの値` が条件式です(lesson04 ch03)。`x == y ? "yes" : "no"` の形で、x と y に2つの名前を入れます

**期待出力**

```text
flat_name = "myapp-prod-logs"
module_name = "myapp-prod-logs"
same_result = "yes"
```
