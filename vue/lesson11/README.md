# Lesson 11 データバインディング（v-bind）

{{ }} で表示できるのは要素の「中身」だけでした。このレッスンでは、リンク先や class・style などの「属性」に data の値を割り当てる v-bind を学びます。データで見た目を切り替える、Vue らしい書き方の入り口です。

## ch01 v-bind の基本 — 属性に data の値を割り当てる

`href="{{ url }}"` のように、**属性**(タグに付ける追加情報)の中で `{{ }}` は使えません。属性に data の値を割り当てるには **v-bind**(ブイバインド)という**ディレクティブ**(`v-` で始まる、Vue がタグに与える特別な指示)を使います。書き方は `v-bind:href="url"`、ふつうは省略形の `:href="url"` です。`:src`(画像の場所)や `:href`、`:disabled`(true なら押せなくする)など、どの属性にも使えます。🔴 「中身は {{ }}、属性は v-bind(:)」という使い分けを覚えましょう。

```html
<a v-bind:href="url">リンク</a>
<a :href="url">リンク(省略形。ふつうはこちら)</a>
<input :placeholder="hint">
```

## ch02 :class で見た目を切り替える(オブジェクト構文)

class 属性には**オブジェクト構文**という専用の書き方が使えます。`:class="{ クラス名: 真偽値 }"` と書くと、値が `true` のときだけその class が付き、`false` なら外れます。lesson09 の `classList.toggle` と違い、「データが true なら付く」と**宣言するだけ**で、付け外しは Vue が行います。🔴 「JS で class を操作する」から「データで class が決まる」への発想の切り替えが山場です。

```html
<p :class="{ done: isDone }">牛乳を買う</p>
<!-- isDone が true なら class="done"、false なら class なし -->
```

サンプルの `@click` は「クリックでデータを書きかえる」指示です(詳しくは次のレッスンで学びます)。

## ch03 :style と省略記法まとめ

style 属性にもオブジェクト構文でバインドできます。`:style="{ color: textColor, fontSize: size + 'px' }"` のように、CSS のプロパティ名は `font-size` → `fontSize` と**キャメルケース**(区切りを大文字にするつなぎ方)で書きます。値には data や式が使えるので、「数値データ + 'px'」のような組み立てが便利です。🟡 ここまでの省略記法を整理しましょう。`v-bind:href` → `:href`。class・style はその中の特別対応(オブジェクト構文)という位置づけです。

```html
<p :style="{ color: textColor, fontSize: size + 'px' }">
  文字色とサイズをデータで制御
</p>
```
