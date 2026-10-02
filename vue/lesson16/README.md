# Lesson 16 総合演習：TODOアプリ

総合演習として、入力・追加・完了チェック・削除ができる TODO アプリを 3 チャプターかけて完成させます。v-model・v-on・v-for・computed など、これまで学んだことの集大成です。

## ch01 土台を作る：入力・追加・一覧表示

いよいよ総合演習です。これまで学んだ v-model・v-on・v-for を組み合わせて、TODO アプリ(やることリスト)を 3 チャプターかけて完成させます。ch01 は土台として「入力欄に書いて追加ボタンを押すと一覧が増える」部分を作ります。やること 1 件は `{ id: 1, text: "牛乳を買う" }` のようなオブジェクトで持ち、重複しない id を :key に使います。🔴 追加したら入力欄を空に戻すのも忘れずに。data を "" にすれば v-model が画面側も空にしてくれます。

```js
addTodo() {
  this.todos.push({ id: this.nextId, text: this.newText });
  this.nextId++;
  this.newText = "";
}
```

## ch02 完了チェック：打ち消し線と残り件数

TODO に完了チェックを付けます。各 TODO に `done`(完了なら true になる真偽値)を持たせ、チェックボックスと `v-model="todo.done"` で同期させます。見た目は `:class="{ done: todo.done }"`(done が true のときだけ done クラスを付ける書き方)と、CSS の `text-decoration: line-through`(打ち消し線)で切り替えます。残り件数は computed で「done が false のものの数」を数えれば、チェックのたびに自動で更新されます。🔴 v-model・:class・computed の合わせ技です。

```js
computed: {
  remaining() {
    return this.todos.filter(todo => !todo.done).length;
  }
}
```

## ch03 削除と仕上げ：TODOアプリ完成

最後の仕上げです。各行に削除ボタンを付け、押された TODO の id 以外を残す filter で配列を作り直して削除します。もうひとつ、空のまま追加ボタンを押しても登録されないように**ガード**(処理の最初に条件を確かめ、だめなら途中でやめる書き方)を入れます。`trim()`(文字列の前後の空白を取り除くメソッド)を使えば、スペースだけの入力も防げます。🔴 これで入力・追加・完了・削除がそろった TODO アプリの完成です。プレビューでひと通り操作して、全機能が動くことを確かめましょう。

```js
removeTodo(id) {
  this.todos = this.todos.filter(todo => todo.id !== id);
}
```
