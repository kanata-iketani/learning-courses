# Lesson 16 総合演習：TODOアプリ

総合演習として、入力・追加・完了チェック・削除ができる TODO アプリを 3 チャプターかけて完成させます。v-model・v-on・v-for・computed など、これまで学んだことの集大成です。

## ch01 土台を作る：入力・追加・一覧表示

いよいよ総合演習です。これまで学んだ v-model(L13)・v-on(L12)・v-for(L14)を組み合わせて、TODO アプリ(やることリスト)を 3 チャプターかけて完成させます。ch01 は土台として「入力欄に書いて追加ボタンを押すと一覧が増える」部分を作ります。やること 1 件は `{ id: 1, text: "牛乳を買う" }` のようなオブジェクトで持ち、重複しない id を :key に使います(L14 ch04)。🔴 追加したら入力欄を空に戻すのも忘れずに。data を "" にすれば v-model が画面側も空にしてくれます。

```js
addTodo() {
  this.todos.push({ id: this.nextId, text: this.newText });
  this.nextId++;
  this.newText = "";
}
```

### data の設計

| data | 初期値 | 役目 |
|---|---|---|
| `newText` | `""` | 入力欄に打っている文字(v-model でつなぐ) |
| `nextId` | `3` | 次に追加する TODO に付ける id。1 と 2 は使用済みなので 3 から |
| `todos` | 2 件の配列 | TODO の一覧。1 件は `{ id, text }` のオブジェクト |

### addTodo を 1 行ずつ

- `this.todos.push({ id: this.nextId, text: this.newText });`: その場でオブジェクトを作り、配列の最後に足します。id には nextId、text には入力された文字を入れます
- `this.nextId++;`: 次の TODO が同じ id にならないように、1 増やしておきます
- `this.newText = "";`: 入力欄を空に戻します。v-model の「データ → 画面」の向きで、入力欄の文字も消えます(L13 ch03)

### テンプレートを 1 行ずつ

- `<input v-model="newText">`: 入力欄と newText をつなぎます
- `<button v-on:click="addTodo">`: クリックで addTodo を呼びます(`@click` と同じ)
- `<li v-for="todo in todos" :key="todo.id">{{ todo.text }}</li>`: todos の数だけ `<li>` を作り、それぞれの text を表示します
- `{{ todos.length }}`: 配列の件数です

### 「宿題」と入力して追加を押すと

| | 押す前 | 押した後 |
|---|---|---|
| todos | 牛乳を買う(id 1)、部屋のそうじ(id 2) | + 宿題(id 3) |
| nextId | 3 | 4 |
| newText / 入力欄 | 宿題 | 空 |
| 画面の一覧 | 2 行 | 3 行(最後に「宿題」) |
| 件数の表示 | 全部で 2 件 | 全部で 3 件 |

## ch02 完了チェック：打ち消し線と残り件数

TODO に完了チェックを付けます。各 TODO に `done`(完了なら true になる真偽値)を持たせ、チェックボックスと `v-model="todo.done"` で同期させます。見た目は `:class="{ done: todo.done }"`(done が true のときだけ done クラスを付ける書き方。L11 ch02)と、CSS の `text-decoration: line-through`(打ち消し線)で切り替えます。残り件数は computed(L15 ch01)で「done が false のものの数」を数えれば、チェックのたびに自動で更新されます。🔴 v-model・:class・computed の合わせ技です。

```js
computed: {
  remaining() {
    return this.todos.filter(todo => !todo.done).length;
  }
}
```

### テンプレートを 1 行ずつ

- `<li v-for="todo in todos" :key="todo.id">`: ch01 と同じ一覧です
- `<input type="checkbox" v-model="todo.done">`: その行の TODO の done とチェックボックスをつなぎます(L13 ch02・L14 ch04)。チェックを付けると、その行の done だけが true になります
- `<span :class="{ done: todo.done }">{{ todo.text }}</span>`: キーの `done` は付ける **class の名前**、値の `todo.done` は **データ** です。名前は同じですが別のものです。データが true のとき、span に class `done` が付きます
- `.done { text-decoration: line-through; color: #999; }`: class done が付いた文字に打ち消し線を引き、灰色にする CSS です

### remaining を 1 つずつ分解する

- `this.todos.filter(...)`: L7 ch04 の filter で、条件に合う要素だけの新しい配列を作ります
- `todo => !todo.done`: L8 ch03 のアロー関数です。1 件ずつ todo に入れて、`!todo.done`(未完了なら true)が true のものだけを残します
- `.length`: 残った配列の件数です

| todos の状態 | filter の結果 | remaining |
|---|---|---|
| 牛乳(done: false)、そうじ(done: true) | [牛乳] | 1 |
| 牛乳にもチェックを付けた | [] | 0 |
| 「宿題」を追加(done: false) | [宿題] | 1 |

### チェックを付けたときに起きること

| 順番 | 起きること |
|---|---|
| 1 | 「牛乳を買う」のチェックボックスにチェックを付ける |
| 2 | v-model により、その行の `todo.done` が true になる |
| 3 | `:class` により span に done が付き、打ち消し線と灰色になる |
| 4 | remaining が使っている todos が変わったので再計算され、見出しの「残り ○ 件」が減る |

追加する TODO は `done: false` で作るので、チェックなしで一覧に入り、残り件数も 1 増えます。

## ch03 削除と仕上げ：TODOアプリ完成

最後の仕上げです。各行に削除ボタンを付け、押された TODO の id 以外を残す filter で配列を作り直して削除します。もうひとつ、空のまま追加ボタンを押しても登録されないように**ガード**(処理の最初に条件を確かめ、だめなら途中でやめる書き方)を入れます。`trim()`(文字列の前後の空白を取り除くメソッド)を使えば、スペースだけの入力も防げます。🔴 これで入力・追加・完了・削除がそろった TODO アプリの完成です。プレビューでひと通り操作して、全機能が動くことを確かめましょう。

```js
removeTodo(id) {
  this.todos = this.todos.filter(todo => todo.id !== id);
}
```

### 削除を 1 行ずつ

- テンプレートの `<button v-on:click="removeTodo(todo.id)">削除</button>`: v-for の中に置いたボタンなので、行ごとに自分の `todo.id` を引数で渡します(L12 ch02 の引数)
- `removeTodo(id)`: 押された行の id を受け取ります
- `todo => todo.id !== id`: 「id が押された id と等しくない」ものを残します(`!==` は L5 ch02 で見た「等しくない」)
- `this.todos = ...`: filter は元の配列を変えずに新しい配列を返すので、それを data の todos に入れ直します。入れ直すと Vue が一覧を描き直します

| todos の id | 削除を押した行 | filter の結果 |
|---|---|---|
| 1, 2, 3 | id 2 | 1, 3 |
| 1, 3 | id 1 | 3 |

### 空入力ガードを 1 行ずつ

```js
if (this.newText.trim() === "") return;
```

- `this.newText.trim()`: 入力された文字の前後の空白を取り除いた文字列です
- `=== ""`: それが空文字かどうかを調べます
- `return;`: 値を返さない return は「ここで関数を終わる」という意味です(L8 ch02)。これより下の push は実行されません
- if の後ろの処理が 1 文だけのときは、`{ }` を省略して 1 行で書けます

| 入力欄 | `trim()` の結果 | 追加されるか |
|---|---|---|
| `"牛乳"` | `"牛乳"` | される |
| `"  牛乳 "` | `"牛乳"` | される |
| `"   "`(スペースだけ) | `""` | されない |
| `""`(空) | `""` | されない |

### 完成したアプリで使った Vue の機能

| 機能 | 使った Vue の機能 | 学んだレッスン |
|---|---|---|
| 入力 | v-model | L13 |
| 追加・削除ボタン | v-on(@click)、methods、引数 | L12 |
| 一覧表示 | v-for、:key | L14 |
| 完了チェックと打ち消し線 | v-model(チェックボックス)、:class | L13・L11 |
| 残り件数 | computed | L15 |
