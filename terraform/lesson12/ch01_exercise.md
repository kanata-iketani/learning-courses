# lesson12 ch01 演習: stateとは何か

ある構成で `terraform state list` を実行したら次が表示されました。

```text
aws_ecs_service.api
aws_iam_role.task
aws_s3_bucket.logs
```

この3つのアドレスを locals のリスト `addresses` に持たせ、次の2つを出力してください。

- output `addresses`: アドレスを `sort()` で並べ替えてから `", "` で連結した文字列
- output `resource_count`: アドレスの個数

(使う関数はどれも lesson05 で見たものです。`sort(リスト)` は文字列をアルファベット順に並べ替えたリスト、`join(区切り, リスト)` はリストを区切り文字でつないだ1本の文字列、`length(リスト)` は要素の数を返します。locals の値は `local.addresses` で参照します。アドレスは `"..."` で囲んだ文字列として書き、要素の間は `,` で区切ります)

**期待出力**

```text
addresses = "aws_ecs_service.api, aws_iam_role.task, aws_s3_bucket.logs"
resource_count = 3
```
