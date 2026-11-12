# Lesson 13 双方向バインディング（v-model）

入力欄とデータが自動で同期する「双方向バインディング」を学ぶレッスンです。v-model をテキスト入力・チェックボックス・セレクトボックスで使い、最後に入力が即座に反映されるあいさつフォームを作ります。

## ch01 v-model の基本：入力欄と data が同期する

**v-model**(入力欄と data を自動で同期させる仕組み)を学びます。v-bind(L11)が「データ→画面」の一方通行だったのに対し、v-model は「画面→データ」の向きも同時につながるので、**双方向バインディング**と呼ばれます。入力欄に 1 文字打つたびに data が書き換わり、その data を表示しているすべての場所が一緒に更新されます。🔴 フォーム作りの土台になる、Vue で最もよく使う機能のひとつです。

```html
<input v-model="name">
<p>こんにちは、{{ name }} さん</p>
```

data の `name` に入れた初期値は最初から入力欄に表示され、入力欄を書きかえれば data も一緒に変わります。

### 2 つの向き

| 向き | きっかけ | 起きること |
|---|---|---|
| データ → 画面 | data の name が変わる(ページを開いたとき・メソッドで書きかえたとき) | 入力欄の中身が name の値になる |
| 画面 → データ | 入力欄に文字を打つ | data の name が打った文字列になる |

L9 ch03 の素の JS では、入力欄の文字を `.value` で自分で読み出していました。v-model を付けると、読み出しも書き戻しも Vue が行うので、`.value` を書く必要がありません。

### サンプルを 1 行ずつ

- `<input v-model="name" placeholder="例: 山田太郎">`: 入力欄と data の name をつなぎます。name の初期値は `""`(空文字)なので、最初は placeholder の案内文が見えます
- `<p>こんにちは、{{ name }} さん！</p>`: name をそのまま表示します
- `<p>いま {{ name.length }} 文字です。</p>`: name の文字数を表示します(L10 ch03 の length)
- `<script src="/vendor/vue.global.prod.js"></script>`: このレッスンからは Vue の読み込みを `#app` の後ろに置いています。読み込みが終わってから次の `<script>` の createApp が動くので、L10 のように `<head>` に置いた場合と同じように動きます

### 1 文字ずつ打ったときの変化

| 入力欄 | data の name | 表示 |
|---|---|---|
| (空) | `""` | こんにちは、 さん！ / いま 0 文字です。 |
| 山 | `"山"` | こんにちは、山 さん！ / いま 1 文字です。 |
| 山田 | `"山田"` | こんにちは、山田 さん！ / いま 2 文字です。 |

### 演習の注意

data に `comment` を足すときは、前の行の末尾にカンマが必要です。

```js
return {
  nickname: "ゲスト",   // ← カンマを忘れない
  comment: ""
};
```

カンマを忘れると JS 全体がエラーになり、`{{ nickname }}` がそのままの文字で表示されます。

## ch02 checkbox と select で v-model を使う

v-model はテキスト以外の部品でも使えます。**チェックボックス**(オン/オフを切り替える四角い部品)に付けると、data は `true` / `false` の**真偽値**(はい/いいえを表す型。L5 で見た)と同期します。**セレクトボックス**(選択肢から 1 つ選ぶ部品)に付けると、選ばれた `<option>` の value と同期します。🟡 部品の種類に合わせて同期のしかたが自動で切り替わるのが v-model の便利なところです。

```html
<input type="checkbox" v-model="agree"> 同意する
<select v-model="color">
  <option value="red">赤</option>
</select>
```

チェックの付け外し、選択肢の変更が、そのまま data の変化になります。

### 部品ごとの同期のしかた

| 部品 | data に入る値 | 例 |
|---|---|---|
| `<input>`(テキスト) | 打った文字列 | `"さくら"` |
| `<input type="checkbox">` | チェックありなら true、なしなら false | `true` |
| `<select>` | 選ばれた `<option>` の value | `"royalblue"` |

### サンプルを 1 行ずつ

- `<label>...</label>`: 部品と説明の文字をひとまとめにするタグです。中に入れておくと、文字「利用規約に同意する」をクリックしてもチェックが切り替わります
- `<input type="checkbox" v-model="agree">`: チェックボックスと data の agree をつなぎます。agree の初期値は false なので、最初はチェックなしです
- `<p>agree の値: {{ agree }}</p>`: true / false をそのまま表示します
- `<select v-model="color">`: セレクトボックスと data の color をつなぎます
- `<option value="tomato">赤系(tomato)</option>`: 画面に見えるのはタグの間の「赤系(tomato)」、data に入るのは value の `"tomato"` です
- `<p v-bind:style="{ color: color }">`: L11 ch03 の :style を省略せずに書いた形です。選んだ色が文字色になります

### 画面はどう変わるか

| 操作 | data | 表示 |
|---|---|---|
| 開いた直後 | agree: false / color: "tomato" | agree の値: false / 文字は赤系 |
| チェックを付ける | agree: true | agree の値: true |
| 「青系」を選ぶ | color: "royalblue" | 文字が青系になる |

### 初期値と選択肢の関係

ページを開いたとき、data の値と同じ value を持つ `<option>` が選ばれた状態になります。data が `"春"` なら `<option value="春">` が選ばれます。一致する option がないと、何も選ばれていない(空の)状態で表示されます。

## ch03 あいさつフォーム：入力が即座に反映される

v-model の総仕上げとして、入力した内容が即座にあいさつ文へ反映されるフォームを作ります。テキスト入力とセレクトボックスを組み合わせ、複数の data をひとつの文章の中で使います。リセットボタンで data を初期値に戻すと、画面側の入力欄も一緒に空になります。これも双方向バインディングの効果です。🔴 「data を変えれば画面が変わる。画面を操作すれば data が変わる」という Vue の考え方を、フォームを通して体で覚えましょう。

```html
<h2>{{ greeting }}、{{ name }} さん！</h2>
```

どちらの data が変わっても、この 1 行は自動で書き換わります。

### サンプルを 1 行ずつ

- `<input v-model="name" placeholder="例: さくら">`: 名前の入力欄と data の name をつなぎます(ch01)
- `<select v-model="greeting">`: あいさつの選択と data の greeting をつなぎます(ch02)
- `<option>おはよう</option>`: value を書いていない option は、タグの間の文字(ここでは `"おはよう"`)が value として使われます
- `<h2>{{ greeting }}、{{ name }} さん！</h2>`: 2 つの data を 1 行の中で使います
- `<button v-on:click="reset">`: `v-on:click` は `@click` の正式な書き方です(L12 ch01)。クリックで reset を呼びます
- `reset() { this.name = ""; this.greeting = "こんにちは"; }`: data を初期値に戻します

### リセットで入力欄まで空になる理由

reset は data を書きかえるだけで、入力欄には触っていません。それでも入力欄が空になるのは、v-model の「データ → 画面」の向きが働くからです。

| 順番 | 起きること |
|---|---|
| 1 | リセットボタンが押され、reset が呼ばれる |
| 2 | `this.name` が `""`、`this.greeting` が `"こんにちは"` になる |
| 3 | v-model でつながった入力欄とセレクトボックスが、新しい data の値に合わせて書きかわる |
| 4 | `{{ greeting }}、{{ name }} さん！` も「こんにちは、 さん！」に書きかわる |

### 演習のヒント

- 好きな食べ物は `<input v-model="food">`、あいさつは `<select v-model="greeting">` と 3 つ以上の `<option>` で作ります
- 文章は `{{ greeting }}、{{ name }} です。好きな食べ物は {{ food }} です。` のように data を並べます
- リセットボタンは `<button @click="reset">リセット</button>` とし、methods の reset で 3 つの data(name・food・greeting)を初期値に戻します
