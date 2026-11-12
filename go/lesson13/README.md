# Lesson 13 for と range

Python入門編「for文」に対応するレッスンです。`range(n)` は Go 1.22 以降の `for i := range n` に、`enumerate` は最初から index と value を返す `for i, v := range s` に対応します。使わない値は `_` で捨てます。

## ch01 for i, v := range スライス（enumerate 相当）

スライス（L7 で見た、Python のリストに当たる可変長の並び）の全要素を順に処理するには `for i, v := range s {}` を使います。`range` はインデックス（要素の位置番号。0 から数える）と値の 2 つを最初から返すため、Python で `enumerate` を使って書いていた形が、Go ではそのまま標準の書き方になります。値だけを取り出す `for v in s:` に対応する専用の形はなく、ch03 で学ぶ `_` でインデックスを捨てて表現します。🔴 スライス処理の基本形なので、手が覚えるまで書きましょう。

Python ではこう書いた:

```python
for i, v in enumerate(fruits):
    print(i, v)
```

Go ではこう書く:

```go
for i, v := range fruits {
	fmt.Println(i, v)
}
```

### 記号の意味

- `for i, v := range fruits {` … `range fruits` がスライスの先頭から 1 要素ずつ「位置番号」と「値」を取り出し、それを `i` と `v` に入れて `{}` の中を実行します。`:=` は L4 で見た「宣言して代入」です。ループ 1 回ごとに `i` と `v` が新しい値で入れ直されます
- `i` と `v` は自分で決める名前です。`for idx, fruit := range fruits` と書いても同じ動きになります（`i`・`v` は慣習的によく使われる名前）

`fruits := []string{"apple", "banana", "cherry"}` のとき、`i` と `v` は次のように変わります。

| 回目 | i | v |
|---|---|---|
| 1 | 0 | apple |
| 2 | 1 | banana |
| 3 | 2 | cherry |

### サンプルを1行ずつ読む

- `fruits := []string{"apple", "banana", "cherry"}` … 文字列のスライスを作ります（L7）
- `for i, v := range fruits { fmt.Println(i, v) }` … 上の表のとおり 3 回回り、`Println` が `i` と `v` を空白区切りで出力します
- `fmt.Printf("%d番目: %s\n", i+1, v)` … L2 で見た `Printf` です。`%d` に整数 `i+1`、`%s` に文字列 `v` が入ります。`\n` は改行です。`i` は 0 から始まるので、1 から数えたいときは `i+1` にします

### 実行結果

```text
0 apple
1 banana
2 cherry
1番目: apple
2番目: banana
3番目: cherry
```

なお、`i` を受け取ったのに使わないと `declared and not used`（宣言したのに使っていない）というコンパイルエラーになります（L4 で見た未使用変数エラー）。その対処が ch03 の `_` です。

## ch02 for i := range 10（range(n) の代わり）

Python の `for i in range(10):` に相当するのが `for i := range 10 {}` で、0 から 9 まで順に回ります。これは **Go 1.22 以降**で使える構文です（1.22 は Go のバージョン番号。`go version` で自分の Go のバージョンを確認できます）。それより前の Go には `for i := 0; i < 10; i++ {}` という 3 部形式しかなく、古い記事や既存コードでは今もよく見ます。また `range(1, 11)` のような開始値の指定はできないため、`i+1` を使って調整します。🔴 回数指定ループの基本形として、手が覚えるまで書きましょう。

Python ではこう書いた:

```python
for i in range(3):
    print(i)
```

Go ではこう書く:

```go
for i := range 3 {
	fmt.Println(i)
}
```

### 3 部形式 `for i := 0; i < 3; i++ {}` の読み方

セミコロン `;` で 3 つに区切られています。

| 部分 | 意味 | いつ実行されるか |
|---|---|---|
| `i := 0` | 初期化。カウンタ `i` を 0 で作る | ループの最初に 1 回だけ |
| `i < 3` | 条件。true の間だけ続ける | 毎回、`{}` の中に入る前 |
| `i++` | 後処理。`i` を 1 増やす（L12 で見た `i++` = `i += 1`） | 毎回、`{}` の中が終わった後 |

`i` は 0 → 1 → 2 と増え、3 になった時点で `i < 3` が false になって終わります。つまり `for i := range 3` と同じ 0, 1, 2 の 3 回です。

### サンプルを1行ずつ読む

- `for i := range 3 { fmt.Println(i) }` … `i` が 0, 1, 2 の順に入り、3 行出力します
- `for i := 0; i < 3; i++ { fmt.Println("old:", i) }` … 上の表のとおり、同じ 0〜2 を 3 部形式で回します。`Println` は複数の値を空白区切りで出すので `old: 0` のようになります
- `fmt.Println(i + 1)` … `range` は 0 始まりなので、1〜3 を出したいときは 1 を足します

### 実行結果

```text
0
1
2
old: 0
old: 1
old: 2
1
2
3
```

演習では `fmt.Printf("%d回目\n", i+1)` のように、`%d` に `i+1` を入れて出力します。

## ch03 _ で値を捨てる

`range` の 1 つ目の戻り値はインデックスと決まっているため、値だけが欲しいときは 1 つ目を**ブランク識別子** `_`（受け取った値を捨てるための特別な名前）で受けて `for _, v := range s` と書きます。Go では宣言したのに使わない変数がコンパイルエラーになるので、「受け取るが使わない」を `_` で明示する必要があるのです。インデックスだけなら 2 つ目を省略して `for i := range s` と書けます。Python の `_` はただの慣習でしたが、Go では言語の仕組みです。🟡 なぜ `_` が必要なのか、理屈を理解しましょう。

Python ではこう書いた:

```python
for v in scores:
    print(v)
```

Go ではこう書く:

```go
for _, v := range scores {
	fmt.Println(v)
}
```

### `_` と省略の 3 パターン

| 書き方 | 受け取るもの | 使う場面 |
|---|---|---|
| `for i, v := range s` | 位置番号と値 | 両方使う |
| `for _, v := range s` | 値だけ（位置番号は捨てる） | Python の `for v in s:` に当たる |
| `for i := range s` | 位置番号だけ（2 つ目を省略） | 位置だけ使う |

`for v := range s` と書くと、`v` には**値ではなく位置番号**が入ります（1 つ目が常に位置番号のため）。値のつもりで使うと間違えるので注意しましょう。

### サンプルを1行ずつ読む

- `scores := []int{80, 65, 92}` … 整数のスライス
- `for _, v := range scores { fmt.Println(v) }` … 位置番号を `_` で捨て、値 80, 65, 92 だけを出力します
- `for i := range scores { fmt.Println("index:", i) }` … 2 つ目を省略したので `i` は位置番号 0, 1, 2 です
- `total := 0` → `for _, v := range scores { total += v }` … `total` に値を順に足します（`+=` は L12 で見た「足して代入」）。0+80=80 → 80+65=145 → 145+92=237
- `fmt.Println("合計:", total)` … 237 を出力します

### 実行結果

```text
80
65
92
index: 0
index: 1
index: 2
合計: 237
```
