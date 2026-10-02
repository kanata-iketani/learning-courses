# FastAPI入門

Python の基礎を学び終えた人向けの FastAPI 講座です。
Web API の基礎から、Pydantic・CRUD・依存性注入まで、ブラウザの学習画面で手を動かしながら学びます。

## 進め方

```sh
cd ~/learning/fastapi
go -C app run .
```

起動したらブラウザで <http://127.0.0.1:8081> を開いてください。
左に教科書、右にエディタが出ます。「▶ 実行」で Python コードを実行、「✔ 採点」で期待出力と照合します。

- 演習は **TestClient**（FastAPI をサーバ起動せずにテストする仕組み）で API を呼び出し、
  その出力を採点します。実サーバの起動（`uvicorn`）は教材内で説明します
- 「💬 質問」から今のチャプターについて Claude に質問できます。質問は記録され、
  「疑問点まとめ」と「復習問題の自動生成」（lesson90）に使われます
- 実行環境は `.venv`（fastapi / uvicorn / httpx インストール済み）を使います

## 教材データ

正データは `lessonNN/chMM.json` です。編集後は次で検証・再生成します。

```sh
go run ./tools/coursegen
```
