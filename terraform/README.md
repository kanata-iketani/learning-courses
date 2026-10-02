# Terraform入門

HCL の文法から、実務のコードベース（Finatext / Skillax など）で分かれる「書き方の流儀」を
読み解けるようになるまでを目指す講座です。

## 進め方

```sh
cd ~/learning/terraform
go -C app run .
```

起動したらブラウザで <http://127.0.0.1:8083> を開いてください。

- 「▶ 実行」でエディタの HCL に対して `terraform init → apply → output` が走り、
  `terraform output` の結果が表示されます（プロバイダ不要の構成なので**クラウド認証もネットも不要・1秒未満**）
- 「✔ 採点」で output の結果を期待値と照合します
- AWS など実プロバイダのコードは**教材内の読解対象**として登場します。演習では読んだロジックを
  `locals` / `output` で再現して採点する方式です
- 複数ファイル（モジュール演習）は `# === file: modules/xxx/main.tf ===` という区切り行で
  1 エディタ内に書けます
- 「💬 質問」からの質問対話・疑問点まとめ・復習問題自動生成（lesson90）も使えます

## 教材データ

正データは `lessonNN/chMM.json` です。編集後は次で検証・再生成します。

```sh
go run ./tools/coursegen
```
