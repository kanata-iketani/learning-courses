# Lesson 09 DOMとイベント

JavaScript からページの中身を読み書きするしくみ(DOM)と、クリックなどの出来事(イベント)に反応する方法を学びます。ここで「JS で画面を書きかえる大変さ」を体験しておくと、次のレッスンで学ぶ Vue のありがたみがよく分かります。

## ch01 DOM とは・getElementById と textContent

**DOM**(Document Object Model。ブラウザが HTML を読み込んで作る「ページの部品の一覧表」)を使うと、JavaScript からページの中身を読み書きできます。`document.getElementById("ID名")` で **要素**(タグ 1 つ分の部品)を取り出し、`textContent` でその中の文字を読み書きします。🔴 「取り出して、書きかえる」の 2 ステップは今後ずっと使う基本なので、手が覚えるまで練習しましょう。

```js
// id="msg" の要素を取り出して、文字を書きかえる
const el = document.getElementById("msg");
el.textContent = "こんにちは！";
```

HTML 側の要素には目印として `id` 属性を付けておきます。

## ch02 ボタンと addEventListener("click")

**イベント**(クリックやキー入力など、ページ上で起きる出来事)に反応するには、要素の `addEventListener("click", 関数)` を使います。「この要素がクリックされたら、この関数を実行して」という予約です。渡す関数には、前のレッスンで学んだアロー関数がよく使われます。🔴 「イベントが起きたら関数が動く」という流れは Vue でもそのまま登場する重要な考え方です。

```js
const btn = document.getElementById("btn");
btn.addEventListener("click", () => {
  // クリックされるたびに、ここが実行される
  document.getElementById("msg").textContent = "押されました！";
});
```

## ch03 input の値を読む(.value)

`<input>`(文字や数を入力する欄)にユーザーが入力した内容は、要素の `.value` プロパティで取り出せます。取り出した値は必ず**文字列**なので、数として計算したいときは `Number()` で変換します。🔴 「入力欄から .value で読む → 加工する → textContent で表示する」の流れは、フォームを扱うページの基本形です。

```js
const input = document.getElementById("name-input");
btn.addEventListener("click", () => {
  const name = input.value;  // 入力された文字列
  msg.textContent = "こんにちは、" + name + "さん！";
});
```

## ch04 classList で見た目を切り替える

JS で色や装飾を変えたいとき、スタイルを 1 つずつ書きかえるより、CSS で用意した class を付け外しするほうがきれいです。要素の `classList`(その要素に付いている class の一覧を操作する道具)を使い、`add("名前")` で付け、`remove("名前")` で外し、`toggle("名前")` で「付いていれば外す・なければ付ける」を切り替えます。🟡 「見た目は CSS に書き、JS は class を切り替えるだけ」という役割分担を意識しましょう。

```js
const box = document.getElementById("box");
box.classList.toggle("dark");  // 押すたびに .dark が付いたり外れたり
```
