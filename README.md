# learning-courses

ブラウザ完結型のローカル学習プラットフォーム。ブラウザで「左に教科書・右にエディタ・実行すると即採点」という体験で学ぶ、自作講座のモノレポです。教材は Claude Code で生成し、すべてのサンプル・模範解答は実行検証済みです。

| 講座 | 場所 | ポート | 内容 / 採点方式 |
|---|---|---|---|
| Go入門編 | `go/` | 8080 | Python経験者向けの全25レッスン。`go run` + stdout 照合 |
| FastAPI入門 | `fastapi/` | 8081 | Python 済み前提の全12レッスン。TestClient 実行 + stdout 照合 |
| Vue.js入門 | `vue/` | 8082 | 前提知識ゼロで HTML/CSS/JS→Vue3 の全16レッスン。JS は node 採点、HTML/Vue はライブプレビュー+自己チェック |
| Terraform入門 | `terraform/` | 8083 | HCL 文法〜実務コード読解の全14レッスン。`terraform apply → output` 照合（プロバイダ不要・オフライン） |

## 起動

```sh
./course.sh start all      # 全講座起動（stop / restart / status も可）
./course.sh start go       # 個別
```

必要な環境: Go 1.22+、Python 3.12+（FastAPI 講座。初回は `python3 -m venv fastapi/.venv && fastapi/.venv/bin/pip install fastapi uvicorn httpx`）、Node 20+（Vue 講座）、Terraform 1.4+。

## 共通アーキテクチャ

- 教材の正データは各講座の `lessonNN/chMM.json`。README・サンプル・演習・解答ファイルは `go run ./tools/coursegen` が検証（全解答を実行して期待出力と照合）したうえで生成
- 学習アプリは各講座の `app/`（Go 標準ライブラリのみ）。進捗・書きかけコードは自動保存
- 「💬 質問」からその場で Claude に質問（ローカルの Claude Code CLI をヘッドレス実行、API キー不要）。質問は記録され、「疑問点まとめ」と「復習問題の自動生成」に使われる
