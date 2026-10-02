# Lesson 03 CSS基礎

ページの見た目を整える言語 CSS を学ぶレッスンです。色・文字・余白・class・flexbox と、デザインに必要な基本のプロパティを順番に身につけます。

## ch01 styleタグとセレクタ・色(color, background-color)

ここからは見た目を整える言語 **CSS** を学びます。CSS は `<head>` の中の `<style>` タグに「`セレクタ { プロパティ: 値; }`」の形で書きます。**セレクタ**は「どのタグを飾るか」の指定(`p` と書けばすべての p タグが対象)、**プロパティ**は「何を変えるか」の指定です。`color` は文字色、`background-color` は背景色で、値には `red` などの色名や `#ff6600` のような**カラーコード**(色を数値で表す書き方)を使えます。🔴 セレクタで相手を選んで色を変える流れをつかみましょう。

```html
<style>
  h1 { color: white; background-color: steelblue; }
  p  { color: #ff6600; }
</style>
```

## ch02 文字の大きさと太さ(font-size, font-weight, text-align)

文字の見た目を細かく調整するプロパティを学びます。`font-size` は**文字の大きさ**で、`24px` のように **px**(ピクセル。画面の点の数を表す単位)で指定します。`font-weight` は**文字の太さ**で、`bold`(太字)や `normal`(標準)を指定します。`text-align` は**文字をそろえる位置**で、`center`(中央)、`left`(左)、`right`(右)から選びます。🔴 大きさ・太さ・位置の 3 つを組み合わせて、ポスターのようにメリハリのある文字を作ってみましょう。

```html
<style>
  h1 { font-size: 40px; text-align: center; }
  p  { font-size: 14px; font-weight: bold; }
</style>
```

## ch03 余白の考え方(margin と padding の違い)

要素のまわりの**余白**(何も表示しない空間)を学びます。CSS では要素を「箱」と考え、`border`(箱の枠線)を境に、**外側**の余白を `margin`、**内側**の余白を `padding` と呼び分けます。margin を増やすと箱どうしの間隔が広がり、padding を増やすと枠線と中身の文字の間が広がります。`border: 2px solid black;` は「太さ 2px・実線・黒」の枠線の指定で、これを付けると余白の違いが目で見て分かります。🟡 同じ 30px でも margin と padding で見た目が全く違うことを、枠線付きの箱で確かめましょう。

```html
<style>
  .a { border: 2px solid tomato; margin: 30px; }
  .b { border: 2px solid seagreen; padding: 30px; }
</style>
```

## ch04 classで使い分ける(.クラス名)

同じ p タグでも「重要なお知らせだけ赤くしたい」ことがあります。そこで使うのが **class 属性**(タグに付ける自分で決めた名前)です。HTML 側で `<p class="important">` のように名前を付け、CSS 側で `.important { ... }` のように**先頭にドット**を付けたセレクタで指定すると、その名前を持つ要素だけに飾りが効きます。同じ class は何個の要素に付けてもよく、まとめて同じ見た目にできます。🔴 「タグ名セレクタは全部に効く、class セレクタは名前を付けた要素だけに効く」の違いをつかみましょう。

```html
<style>
  .important { color: red; font-weight: bold; }
</style>
<p class="important">ここだけ赤い太字</p>
<p>ふつうの段落</p>
```

## ch05 flexboxで横に並べる(display:flex)

div は本来、縦に積み重なっていきます。横に並べたいときに使うのが **flexbox**(フレックスボックス。要素を柔軟に並べる CSS のしくみ)です。並べたい要素たちの**親**(それらを囲んでいる要素)に `display: flex;` と書くと、中の子要素が横一列に並びます。あわせて `gap`(子どうしの間隔)や `justify-content`(横方向の寄せ方。`center` で中央寄せ、`space-between` で両端に広げる)もよく使います。🟡 「指定するのは並べたい子ではなく親」という点が最大のポイントです。

```html
<style>
  .row { display: flex; gap: 16px; justify-content: center; }
</style>
<div class="row">
  <div>A</div><div>B</div><div>C</div>
</div>
```
