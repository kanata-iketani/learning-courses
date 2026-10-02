# Lesson 15 算出プロパティと部品化

データから自動で計算される computed、値の変化を見張る watch、そして画面を部品化するコンポーネントと props を学ぶレッスンです。ここで学ぶ道具は、次のレッスンの TODO アプリで総動員します。

## ch01 computed：データから自動計算される値

**computed**(算出プロパティ。data から自動で計算される値)を学びます。data と同じように `{{ total }}` と書くだけで使え、計算に使っている data が変わると自動で再計算されます。methods との違いは 2 つあります。呼び出しの `()` が不要なことと、元の data が変わらない限り前回の結果を**キャッシュ**(結果の一時保存)して使い回すので、無駄な再計算が起きないことです。🔴 「表示のために加工した値」は computed に書く、と覚えましょう。

```js
computed: {
  total() {
    return this.price * this.count;
  }
}
```

price か count が変われば、{{ total }} の表示は勝手に新しくなります。

## ch02 watch：値の変化を見張る

**watch**(データの変化を見張り、変わった瞬間に処理を実行する仕組み)を学びます。computed が「データから別の値を作る」ものだったのに対し、watch は「値が変わったのをきっかけに何かする」ためのものです。見張りたい data と同じ名前の関数を watch に書くと、変化のたびに新しい値と古い値が引数で渡されます。⚪ 履歴を残す・変更回数を数えるなど「値そのもの以外の仕事」をしたいときに使います。まずは computed を優先し、watch は必要な場面だけで十分です。

```js
watch: {
  name(newValue, oldValue) {
    console.log(oldValue + " から " + newValue + " に変わった");
  }
}
```

## ch03 コンポーネント：画面を部品として定義する

**コンポーネント**(画面の一部をひとまとめにして名前を付け、自作タグとして使えるようにする仕組み)を学びます。`app.component("名前", { ... })` で登録すると、HTML 側に `<count-button></count-button>` のように何個でも置けます。部品の見た目は **template**(その部品の HTML を文字列として書く場所)に書きます。コンポーネントの data は関数で返す決まりなので、置いた部品 1 つ 1 つが独立した data を持ちます。🟡 HTML に直接書く場合、タグ名はハイフン入り(例: count-button)にします。

```js
const app = createApp({});
app.component("count-button", {
  data() { return { count: 0 }; },
  template: `<button v-on:click="count++">{{ count }} 回</button>`
});
app.mount("#app");
```

## ch04 props：親から子へデータを渡す

**props**(親から子コンポーネントへデータを渡すための受け口)を学びます。子側で `props: ["name"]` と宣言すると、親は `<user-card name="さくら">` のように属性の形で値を渡せ、子の template の中では data と同じように `{{ name }}` で使えます。固定の文字列はそのまま属性に書き、data の値を渡すときは `:name="member.name"` と v-bind を使います。🟡 「部品の形は同じで中身だけ違う」一覧は、props 付きコンポーネントと v-for の組み合わせが定番です。

```js
app.component("user-card", {
  props: ["name", "age"],
  template: `<p>{{ name }}({{ age }}歳)</p>`
});
```
