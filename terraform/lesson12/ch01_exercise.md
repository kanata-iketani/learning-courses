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

**期待出力**

```text
addresses = "aws_ecs_service.api, aws_iam_role.task, aws_s3_bucket.logs"
resource_count = 3
```
