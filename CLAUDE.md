# learning — ブラウザ完結型ローカル学習講座群

このディレクトリには自作の学習講座群がある。社内情報を含む講座(公開しない)の一覧と運用は `CLAUDE.local.md`(git 管理外)にある。すべて同じ仕組み(3ペイン学習アプリ + JSON 教材 + 自動採点 + Claude 質問対話)。

| 講座 | 場所 | ポート | 採点方式 |
|---|---|---|---|
| Go入門編 | `go/` | 8080 | `go run` + stdout 照合 |
| FastAPI入門 | `fastapi/` | 8081 | venv python(TestClient) + stdout 照合 |
| Vue.js入門 | `vue/` | 8082 | JS基礎=node 採点 / HTML・Vue=`kind:"web"` プレビュー+自己チェック |
| Terraform入門 | `terraform/` | 8083 | `terraform init -backend=false → apply → output` 照合(プロバイダ不要・オフライン) |
| 宅建どうじょう | `takken/` (別リポジトリ github.com/kanata-iketani/takken) | 8084 | 4択クイズ即時判定。全31章700問(フル模試×3)。にがて帳・弱点まとめ・復習問題生成 |
| ネスペどうじょう | `nwspec/` (別リポジトリ github.com/kanata-iketani/nwspec) | 8085 | 4択クイズ。全33章602問(午前Ⅰ基礎〜午後事例演習〜模試)。過去問併用前提 |
| CISSPどうじょう | `cissp/` (別リポジトリ github.com/kanata-iketani/cissp) | 8086 | 4択クイズ。全34章(8ドメイン+シナリオドリル+模試50問×2)。2024年版アウトライン・日本語CAT対応。BEST/MOST問題のマネジメント視点訓練が特色 |
| DDDどうじょう | `ddd/` (別リポジトリ github.com/kanata-iketani/ddd) | 8087 | 4択クイズ。全16章(戦略的設計→戦術的設計→アーキテクチャ→実践)。Go/Pythonコード例つき。「どこに置くか・どう切るか」の設計判断シナリオ問題が中心 |
| 記事どうじょう | `kiji/` | 8090 | 自分の技術ブログ(Zenn/Qiita)1記事=1レッスン。4択・記述式(AI 採点)・SQL・コーディング問題(go/js/ts/python を実行して出力比較)。手順は `kiji/tools/GENERATE.md` |

## 絶対ルール

- ~/learning/CLAUDE.md の「絶対ルール」にある禁止語を使わない
- git コミットに AI 署名(Co-Authored-By 等)を入れない。作者はユーザー本人のみ

## 起動・停止

ユーザーが「go 起動」「vue 停止」「全部状態」などと言ったら実行する:

```sh
~/learning/course.sh {start|stop|restart|status} {go|fastapi|vue|terraform|takken|nwspec|cissp|ddd|finatext|nippo|kiji|dbspec|fukuri|awsnet|all}
```

## 共通アーキテクチャ

- 教材の正データは各講座の `lessonNN/chMM.json`。README/サンプル/演習/解答ファイルは `go run ./tools/coursegen` で検証+生成(ALL OK が合格)
- 学習アプリは各講座の `app/`(Go 製・独立モジュール)。`go -C <講座>/app run .` で起動。講座差分は `app/config.go` に分離
- 質問対話はローカルの `claude -p --model opus` をヘッドレス実行(今開いている問題・解答状況・原本画像を渡す。Sonnet は使わない)(API キー不要)。Q&A は `app/questions.json`、疑問点まとめは `app/notes.md`、復習問題の自動生成先は `lesson90/`(coursegen 対象外)
- 進捗は `app/progress.json`、書きかけコードは `app/work/`
- Terraform のマルチファイル演習は `# === file: modules/x/main.tf ===` 区切り
- Vue はローカル同梱 `vue/app/static/vendor/vue.global.prod.js`(CDN 不要)

## Git の運用

- **main に直接 push しない。** 変更は `~/bin/git-ship "<コミットメッセージ>" [ファイル...]` で入れる(ブランチ → PR → squash でセルフマージ → main に戻って pull まで自動)。ユーザーの指示(2026-11-04、GitHub の実績のため)
- 公開リポジトリ(learning-courses・takken・nwspec・cissp・ddd)に、社内情報(Finatext・日報・fukuri・awsnet の Finatext 実構成)や IPA 過去問データを入れない。それらの講座は `.gitignore` で除外している
- コミットメッセージ・PR に AI 署名を入れない

- 教材を修正したら該当講座で `go run ./tools/coursegen` を回して ALL OK を確認すること
