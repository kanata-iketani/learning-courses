# learning — ブラウザ完結型ローカル学習講座群

このディレクトリには自作の学習講座が 4 つある。すべて同じ仕組み(3ペイン学習アプリ + JSON 教材 + 自動採点 + Claude 質問対話)。

| 講座 | 場所 | ポート | 採点方式 |
|---|---|---|---|
| Go入門編 | `go/` | 8080 | `go run` + stdout 照合 |
| FastAPI入門 | `fastapi/` | 8081 | venv python(TestClient) + stdout 照合 |
| Vue.js入門 | `vue/` | 8082 | JS基礎=node 採点 / HTML・Vue=`kind:"web"` プレビュー+自己チェック |
| Terraform入門 | `terraform/` | 8083 | `terraform init -backend=false → apply → output` 照合(プロバイダ不要・オフライン) |

## 起動・停止

ユーザーが「go 起動」「vue 停止」「全部状態」などと言ったら実行する:

```sh
~/learning/course.sh {start|stop|restart|status} {go|fastapi|vue|terraform|all}
```

## 共通アーキテクチャ

- 教材の正データは各講座の `lessonNN/chMM.json`。README/サンプル/演習/解答ファイルは `go run ./tools/coursegen` で検証+生成(ALL OK が合格)
- 学習アプリは各講座の `app/`(Go 製・独立モジュール)。`go -C <講座>/app run .` で起動。講座差分は `app/config.go` に分離
- 質問対話はローカルの `claude -p --model sonnet` をヘッドレス実行(API キー不要)。Q&A は `app/questions.json`、疑問点まとめは `app/notes.md`、復習問題の自動生成先は `lesson90/`(coursegen 対象外)
- 進捗は `app/progress.json`、書きかけコードは `app/work/`
- Terraform のマルチファイル演習は `# === file: modules/x/main.tf ===` 区切り
- Vue はローカル同梱 `vue/app/static/vendor/vue.global.prod.js`(CDN 不要)

## ユーザーについて

- Python 経験あり。Go / FastAPI / Vue / Terraform を学習中(Terraform は Finatext/Skillax の実務コード読解が目標)
- 将来: 受験・TOEIC・資格試験の学習アプリを同メソッドで作る計画あり(ユーザーの GO サイン待ち。採点=選択式は単純比較/記述式は Claude 採点、SRS 化、著作権はオリジナル問題生成で回避、という方針まで合意済み)
- 教材を修正したら該当講座で `go run ./tools/coursegen` を回して ALL OK を確認すること
