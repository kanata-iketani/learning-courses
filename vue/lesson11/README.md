# Lesson 11 データバインディング（v-bind）

{{ }} で表示できるのは要素の「中身」だけでした。このレッスンでは、リンク先や class・style などの「属性」に data の値を割り当てる v-bind を学びます。データで見た目を切り替える、Vue らしい書き方の入り口です。

## ch01 v-bind の基本 — 属性に data の値を割り当てる

`href="{{ url }}"` のように、**属性**(タグに付ける追加情報)の中で `{{ }}` は使えません。属性に data の値を割り当てるには **v-bind**(ブイバインド)という**ディレクティブ**(`v-` で始まる、Vue がタグに与える特別な指示)を使います。書き方は `v-bind:href="url"`、ふつうは省略形の `:href="url"` です。`:src`(画像の場所)や `:href`、`:disabled`(true なら押せなくする)など、どの属性にも使えます。🔴 「中身は {{ }}、属性は v-bind(:)」という使い分けを覚えましょう。

```html
<a v-bind:href="url">リンク</a>
<a :href="url">リンク(省略形。ふつうはこちら)</a>
<input :placeholder="hint">
```

### : が付くと何が変わるか

`:` が付いた属性の `" "` の中は、文字列ではなく **JavaScript の式** として読まれます。`{{ }}` の中と同じで、data の名前がそのまま使えます。

| 書き方 | `" "` の中の扱い | ブラウザに渡る属性 |
|---|---|---|
| `href="url"` | ただの文字 | `href="url"`(文字 url のまま) |
| `href="{{ url }}"` | ただの文字 | `href="{{ url }}"`(使えない) |
| `:href="url"` | 式(data の url) | `href="https://ja.vuejs.org/"` |

### サンプルを 1 行ずつ

- `<a :href="url">{{ siteName }} を開く</a>`: リンク先(L2 で見た href)は data の `url`、リンクの文字は `{{ }}` で `siteName` を出します
- `<input :placeholder="hint">`: 入力欄が空のときにうすく出る案内文(placeholder)に、data の `hint` を割り当てます
- `<button :disabled="isClosed">`: disabled は「押せなくする」属性です。値が true なら属性が付いてボタンが灰色になり押せず、false なら属性そのものが外れて押せるようになります
- `{{ isClosed ? "(受付終了)" : "(受付中)" }}`: L10 ch03 の三項演算子で、状態に合わせた文字を出します

### 画面はどう変わるか

| data の isClosed | ボタン | 横の文字 |
|---|---|---|
| true | 押せない(灰色) | (受付終了) |
| false | 押せる | (受付中) |

data の値を書きかえると、属性も自動で書きかわります。これも L10 ch01 で見たリアクティブの働きです。

## ch02 :class で見た目を切り替える(オブジェクト構文)

class 属性には**オブジェクト構文**という専用の書き方が使えます。`:class="{ クラス名: 真偽値 }"` と書くと、値が `true` のときだけその class が付き、`false` なら外れます。L9 ch04 の `classList.toggle` と違い、「データが true なら付く」と**宣言するだけ**で、付け外しは Vue が行います。🔴 「JS で class を操作する」から「データで class が決まる」への発想の切り替えが山場です。

```html
<p :class="{ done: isDone }">牛乳を買う</p>
<!-- isDone が true なら class="done"、false なら class なし -->
```

サンプルの `@click` は「クリックでデータを書きかえる」指示です(詳しくは L12 で学びます)。

### オブジェクト構文の読み方

`{ done: isDone }` は L7 で見たオブジェクトです。**キー**(`:` の左)が付けたい class の名前、**値**(`:` の右)が「付けるかどうか」を決める式です。

| isDone | 付く class | 実際の HTML |
|---|---|---|
| false | なし | `<p>牛乳を買う</p>` |
| true | done | `<p class="done">牛乳を買う</p>` |

キーと値を複数並べると、class ごとに別々に判定されます。

| isDone2 | isUrgent | `:class="{ done: isDone2, urgent: isUrgent }"` の結果 |
|---|---|---|
| false | true | `class="urgent"` |
| true | true | `class="done urgent"` |
| false | false | class なし |

クラス名に `-` が入るときは、`{ 'is-active': flag }` のようにキーをクォートで囲みます。また、ふつうの `class="..."` と `:class` は同じタグに両方書けて、2 つが合体します(L12 ch03 のサンプルで使います)。

### ! で true と false を入れかえる

サンプルのボタンの `isDone = !isDone` は、`!`(否定。true なら false、false なら true にする演算子)を使って、データを反対の値に書きかえる式です。

| 押す前の isDone | `!isDone` | 押した後の isDone |
|---|---|---|
| false | true | true |
| true | false | false |

押すたびに true と false が入れかわるので、class が付いたり外れたりします。

### 画面はどう変わるか

- 1 つ目のボタンを押す → `isDone` が true になる → 1 つ目の `<p>` に done が付き、`.done` の見た目(打ち消し線と灰色の文字)になる
- もう一度押す → false に戻る → done が外れる
- JS で classList を操作する行は 1 つもなく、データを変えるだけで見た目が変わります

## ch03 :style と省略記法まとめ

style 属性にもオブジェクト構文でバインドできます。`:style="{ color: textColor, fontSize: size + 'px' }"` のように、CSS のプロパティ名は `font-size` → `fontSize` と**キャメルケース**(区切りの次の文字を大文字にしてつなぐ書き方)で書きます。値には data や式が使えるので、「数値データ + 'px'」のような組み立てが便利です。🟡 ここまでの省略記法を整理しましょう。`v-bind:href` → `:href`。class・style はその中の特別対応(オブジェクト構文)という位置づけです。

```html
<p :style="{ color: textColor, fontSize: size + 'px' }">
  文字色とサイズをデータで制御
</p>
```

### キャメルケースにする理由

`{ }` の中は JavaScript のオブジェクトなので、キーに `font-size` と書くと `-` が引き算の記号と区別できません。そこで `fontSize` と書きます(`'font-size'` とクォートで囲む書き方もできます)。

| CSS での名前 | :style での名前 |
|---|---|
| `color` | `color` |
| `font-size` | `fontSize` |
| `background-color` | `backgroundColor` |

### 値の組み立て

- `color: textColor`: キー color は CSS のプロパティ、値 textColor は data の名前です
- `fontSize: size + 'px'`: 数 `20` と文字列 `'px'` を `+` でつなぐと文字列 `"20px"` になります。`px` を付けないとサイズとして読まれません
- `" "` の中で文字列を書くときは、属性の `"` とぶつからないように `'px'` のようにシングルクォートを使います(JavaScript では `'` でも `"` でも文字列を作れます)

### サンプルのボタン

- `@click="size += 4"`: L10 ch01 で見た `+=` で size を 4 増やします
- `@click="size -= 4"`: 4 減らします
- `@click="textColor = 'tomato'"`: textColor を `'tomato'` に書きかえます

### 画面はどう変わるか

| 操作 | size | textColor | ブラウザに渡る style |
|---|---|---|---|
| 開いた直後 | 20 | steelblue | `color: steelblue; font-size: 20px;` |
| 「大きく」 | 24 | steelblue | `color: steelblue; font-size: 24px;` |
| 「トマト色にする」 | 24 | tomato | `color: tomato; font-size: 24px;` |

### 省略記法のまとめ

| 正式な書き方 | 省略形 | 意味 |
|---|---|---|
| `v-bind:href="url"` | `:href="url"` | 属性にデータを割り当てる |
| `v-bind:class="{ ... }"` | `:class="{ ... }"` | class をデータで付け外し(ch02) |
| `v-bind:style="{ ... }"` | `:style="{ ... }"` | style をデータで決める |
| `v-on:click="..."` | `@click="..."` | クリックで処理する(L12) |
