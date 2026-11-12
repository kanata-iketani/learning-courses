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

### 1 行ずつの意味

- `computed: { ... }`: data・methods と並べて書く設定です。間はカンマで区切ります
- `total() { ... }`: 計算した値の名前(ここでは total)を関数の名前にします。書き方は methods と同じ形です
- `return this.price * this.count;`: 計算結果を return で返します(L8 ch02 で見た戻り値)。返した値が `{{ total }}` に表示されます。中では methods と同じく `this.データ名` で data を読みます

### サンプルを 1 行ずつ

- `<input type="number" v-model="price">`: 単価の入力欄と data の price をつなぎます。type="number" なので数として入ります(L14 ch01)
- `{{ total }}` / `{{ totalWithTax }}`: computed の名前を `()` なしで書きます
- `totalWithTax() { return Math.round(this.total * 1.1); }`: computed の中から、別の computed(total)も `this.total` で使えます。`Math.round` は四捨五入する関数です

| price | count | total | totalWithTax |
|---|---|---|---|
| 120 | 2 | 240 | 264 |
| 120 | 3 | 360 | 396 |
| 200 | 3 | 600 | 660 |

個数の欄を 3 に変えた瞬間に、total と totalWithTax の両方が計算し直されます。

### methods との違い

| | methods | computed |
|---|---|---|
| 使う場面 | クリックなどで何かを実行する | data から表示用の値を作る |
| テンプレートでの書き方 | `{{ calcTotal() }}`(`()` が要る) | `{{ total }}`(`()` なし) |
| 再計算のタイミング | 画面が書きかわるたびに毎回呼ばれる | 使っている data が変わったときだけ |
| data の書きかえ | してよい | しない(値を返すだけにする) |

### 演習のヒント

いまの文字数は `this.message.length`、残りは `140 - this.message.length` で求められます。computed に `remaining() { return ...; }` を書き、テンプレートの `???` を `{{ remaining }}` などに置きかえます。

## ch02 watch：値の変化を見張る

**watch**(データの変化を見張り、変わった瞬間に処理を実行する仕組み)を学びます。computed が「データから別の値を作る」ものだったのに対し、watch は「値が変わったのをきっかけに何かする」ためのものです。見張りたい data と同じ名前の関数を watch に書くと、変化のたびに新しい値と古い値が引数で渡されます。⚪ 履歴を残す・変更回数を数えるなど「値そのもの以外の仕事」をしたいときに使います。まずは computed を優先し、watch は必要な場面だけで十分です。

```js
watch: {
  name(newValue, oldValue) {
    console.log(oldValue + " から " + newValue + " に変わった");
  }
}
```

### 1 行ずつの意味

- `watch: { ... }`: data・methods・computed と並べて書く設定です
- `name(newValue, oldValue) { ... }`: 関数の名前を、見張りたい data の名前(ここでは name)と同じにします。name が変わるたびに Vue がこの関数を呼びます
- 引数は **1 つ目が新しい値、2 つ目が古い値** の順で渡されます。引数の名前は自由ですが、順番は決まっています
- `console.log(...)`: 開発者ツールのコンソール(L1 ch03)に文字を出します

watch の関数は、**ページを開いた時点では呼ばれません**。data の初期値が入っただけでは「変化」ではないからです。最初に値が変わったときから呼ばれ始めます。

### サンプルを 1 行ずつ

- `<input v-model="name">`: 入力欄と name をつなぎます。1 文字打つたびに name が変わります
- `<li v-for="(log, index) in logs" :key="index">`: 履歴の配列 logs を一覧にします。末尾に足すだけの一覧なので index を key にしています(L14 ch04)
- `this.logs.push("「" + oldValue + "」→「" + newValue + "」");`: 古い値と新しい値をつないだ文字列を、logs の最後に足します

| 入力欄の操作 | oldValue | newValue | logs に足される文字 |
|---|---|---|---|
| 「さ」と打つ | `""` | `"さ"` | 「」→「さ」 |
| 続けて「く」 | `"さ"` | `"さく"` | 「さ」→「さく」 |
| 1 文字消す | `"さく"` | `"さ"` | 「さく」→「さ」 |

### computed と watch の使い分け

| | computed | watch |
|---|---|---|
| 役目 | data から別の値を作って表示する | data の変化をきっかけに別の処理をする |
| 戻り値 | 返した値が表示に使われる | 使われない(return しない) |
| 例 | 合計金額、残り文字数 | 変更履歴を残す、変更回数を数える |

### 演習のヒント

`favorite(newValue, oldValue) { ... }` の中で、`this.changeCount++;` で回数を増やし、`this.logs.push(oldValue + " から " + newValue + " に変わりました");` で履歴を足します。

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

### 1 行ずつの意味

- `const app = createApp({});`: 設定が空のアプリを作り、変数 app に入れます。これまでのように続けて `.mount` を呼ばないのは、mount の前に部品を登録するためです
- `app.component("count-button", { ... })`: 1 つ目の引数がタグ名、2 つ目が部品の設定です。設定の書き方は createApp と同じで、data・methods・computed なども書けます
- `data() { return { count: 0 }; }`: この部品が覚えておく値です
- `template: ` に続く `` ` `` で囲んだ部分: 部品の HTML です。L4 ch04 で見たテンプレートリテラルの記号(バッククォート)で囲むので、中に `"` を含められ、複数行にも書けます。中の `{{ count }}` は JavaScript の `${ }` ではなく Vue の表示です
- `app.mount("#app");`: 部品を登録し終わってから mount します。mount の後に登録した部品は使えません

### 自作タグの書き方

- HTML 側には `<count-button></count-button>` と開始タグと閉じタグの両方を書きます。HTML に直接書く場合、`<count-button />` のような省略形は使えません
- 名前にハイフンを入れるのは、ブラウザがもともと持つタグ(`<button>` など)と名前が重ならないようにするためです

### data が関数である理由

部品を 1 つ置くたびに、Vue は data() を呼び直して新しいオブジェクトを作ります。そのため、3 つ置けば count も 3 つ別々にできます。L10 ch02 で data を関数にしていたのも、この仕組みに合わせるためです。

| 操作 | 1 つ目の count | 2 つ目の count | 3 つ目の count |
|---|---|---|---|
| 開いた直後 | 0 | 0 | 0 |
| 2 つ目を 1 回押す | 0 | 1 | 0 |
| 1 つ目を 2 回押す | 2 | 1 | 0 |

### 親と子

部品を置く側のアプリ(`#app`)を **親**、置かれる部品(count-button)を **子** と呼びます。次の ch04 では、親から子へ値を渡す方法を学びます。

## ch04 props：親から子へデータを渡す

**props**(親から子コンポーネントへデータを渡すための受け口)を学びます。子側で `props: ["name"]` と宣言すると、親は `<user-card name="さくら">` のように属性の形で値を渡せ、子の template の中では data と同じように `{{ name }}` で使えます。固定の文字列はそのまま属性に書き、data の値を渡すときは `:name="member.name"` と v-bind(L11 ch01)を使います。🟡 「部品の形は同じで中身だけ違う」一覧は、props 付きコンポーネントと v-for の組み合わせが定番です。

```js
app.component("user-card", {
  props: ["name", "age"],
  template: `<p>{{ name }}({{ age }}歳)</p>`
});
```

### 1 行ずつの意味

- `props: ["name", "age"]`: 親から受け取る属性の名前を、文字列の配列で並べます
- `` template: `<p>{{ name }}({{ age }}歳)</p>` ``: 受け取った値を `{{ }}` で表示します。子は自分の data を持たなくても、props の値で表示を作れます
- HTML 側の `<user-card name="さくら" age="12">`: 親が子に値を渡す書き方です。属性名を props の名前と同じにします

### 固定の値と v-bind の違い

| 親での書き方 | 子に渡る値 |
|---|---|
| `name="さくら"` | 文字列 `"さくら"` |
| `age="12"` | 文字列 `"12"`(`:` がないので文字列) |
| `:age="12"` | 数 `12`(`:` があると式として読む) |
| `:name="member.name"` | data の member の name の値 |

### サンプルを 1 行ずつ

- `<user-card name="さくら" age="12"></user-card>`: 固定の値を渡すカードです
- `<user-card v-for="member in members" :key="member.name" :name="member.name" :age="member.age">`: 配列 members の数だけカードを作り、1 件ずつ name と age を渡します。コンポーネントにも L14 ch04 の :key を付けます
- `style="border: 1px solid #aaa; padding: 4px;"`: タグに直接書く style 属性です。L3 で `<style>` タグに書いた CSS と同じ書き方で、枠線と内側の余白を付けています

| カード | 渡される name | 渡される age | 表示 |
|---|---|---|---|
| 1 枚目(固定) | さくら | "12" | さくら(12歳) |
| 2 枚目(v-for 1 回目) | たろう | 13 | たろう(13歳) |
| 3 枚目(v-for 2 回目) | はなこ | 11 | はなこ(11歳) |

data の members の値を書きかえると、対応するカードの表示だけが変わります。

### props は子の側で書きかえない

props は親から受け取った値なので、子の中で `this.name = ...` のように書きかえてはいけません(Vue が警告を出します)。値を変えたいときは親の data を変えれば、props を通して子の表示も変わります。子から親に「ボタンが押された」などを知らせるには、emit という別の仕組みを使います(この講座では扱いません)。
