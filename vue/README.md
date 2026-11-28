# Vue.js入門

前提知識ゼロから Vue 3 を使えるようになるための講座です。
HTML → CSS → JavaScript → DOM → Vue の順に、ブラウザの学習画面で手を動かしながら学びます。

## 進め方

```sh
cd ~/learning/vue
go -C app run .
```

起動したらブラウザで <http://127.0.0.1:8082> を開いてください。

チャプターには 2 種類あります。

- **プログラム型**（JavaScript 基礎）— 右下に実行結果が出て、「✔ 採点」で期待出力と自動照合します（Node.js で実行）
- **プレビュー型**（HTML / CSS / Vue）— 「▶ プレビュー」でエディタの HTML が右下に即時描画されます。
  教材の「確認ポイント」を満たせたら「✔ できた」で合格にします

Vue はローカル同梱版（`/vendor/vue.global.prod.js`）を使うため、ネット接続なしでも動きます。
「💬 質問」から Claude への質問・疑問点まとめ・復習問題の自動生成（lesson90、JavaScript 問題）も使えます。

## 教材データ

正データは `lessonNN/chMM.json`（`kind: "web"` がプレビュー型）です。編集後は次で検証・再生成します。

```sh
go run ./tools/coursegen
```
