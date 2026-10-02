# lesson10 ch02 演習: モジュールの入力と出力

モジュール `./modules/labels` は variable `team` と `system` を受け取り、locals でラベル文字列を組み立てています。ただし output が無いため、外から値を取り出せません。

1. モジュール側に output `label` を追加し、`local.label` を公開する
2. 呼び出し側で `module "labels"` ブロックを書き、`team = "platform"`、`system = "billing"` を渡す
3. 呼び出し側の output `label` で `module.labels.label` を表示する

**期待出力**

```text
label = "team:platform/system:billing"
```
