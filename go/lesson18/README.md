# Lesson 18 関数

Python入門編「関数」に対応するレッスンです。Go の関数は引数と戻り値に型を書きます（戻り値なしなら型を書きません）。値を 2 つ以上返す多値返却と、lambda に当たる無名関数も学びます。

## ch01 func と引数の型

Go で関数を定義するには `func` を使います（L9・L14 で一度見ました。ここで正式に扱います）。Python の `def` との一番の差は、**引数に型を書く**ことです。引数名の後ろに型を置き、同じ型が続くときは `a, b int` とまとめて書けます。型の合わない値を渡す呼び出しはコンパイルエラーになるので、実行する前に間違いに気づけます。🔴 関数定義はこの先すべての土台になるので、手が覚えるまで書きましょう。

Python ではこう書いた:

```python
def greet(name, times):
    for i in range(times):
        print("Hello,", name)
```

Go ではこう書く:

```go
func greet(name string, times int) {
	for range times {
		fmt.Println("Hello,", name)
	}
}
```

### `func greet(name string, times int) {` の読み方

| 部分 | 意味 |
|---|---|
| `func` | 関数定義の始まり（Python の `def`） |
| `greet` | 関数名 |
| `name string` | 1 つ目の引数。名前 `name`、型 string |
| `times int` | 2 つ目の引数。名前 `times`、型 int |
| `{ ... }` | 関数の中身。Python のインデントの代わりに `{}` で囲みます |

`)` の後ろに何も書いていないのは「戻り値がない」という意味です（ch02）。

### サンプルを1行ずつ読む

- `for range times { fmt.Println("Hello,", name) }` … `times` 回くり返します（L15 で見た、変数を受け取らない `for range n`）
- `func printSum(a, b int) {` … `a int, b int` を `a, b int` とまとめた形です
- `greet("Gopher", 2)` … `name` に `"Gopher"`、`times` に 2 が入ります。引数は書いた順に入ります
- `printSum(3, 5)` … 3+5 を出力します

### 実行結果

```text
Hello, Gopher
Hello, Gopher
8
```

### 型が合わないと

`greet(2, "Gopher")` のように順番を間違えると、実行する前に次のようなコンパイルエラーになります。

```text
cannot use 2 (untyped int constant) as string value in argument to greet
```

「2 を string の引数として使えない」という意味です。Python なら実行してみるまで気づけない間違いです。

## ch02 戻り値の型を書く

値を返す関数は、引数リストの後ろに**戻り値の型**を書きます。Python は `return` するだけで型を書きませんでしたが、Go は `func add(a, b int) int` のように「何型を返すか」を宣言します。宣言と違う型を返すとコンパイルエラーです。**戻り値がない関数は型を書きません**。`func hello()` のように引数リストで止めます。🔴 「返すなら型を書く・返さないなら書かない」を手に覚えさせましょう。

Python ではこう書いた:

```python
def add(a, b):
    return a + b
```

Go ではこう書く:

```go
func add(a, b int) int {
	return a + b
}

// 戻り値なしなら型を書かない
func hello() {
	fmt.Println("hello")
}
```

### `func add(a, b int) int {` の読み方

`(a, b int)` までが引数、その後ろの `int` が戻り値の型です。「int を 2 つ受け取って int を 1 つ返す関数」と読みます。

### サンプルを1行ずつ読む

- `return a + b` … 計算結果を呼び出し元に返し、関数を終えます
- `total := add(3, 5)` … `add` が返した 8 を `total` に入れます
- `fmt.Println(add(total, 10))` … `add(8, 10)` が 18 を返し、それがそのまま `Println` に渡ります。関数呼び出しは「値」として式の中に書けます
- `hello()` … 戻り値のない関数は、呼ぶだけで使います

### 実行結果

```text
8
18
hello
```

### よくあるコンパイルエラー

| 書いたもの | エラーの意味 |
|---|---|
| 戻り値の型 `int` を書いたのに `return` がない | `missing return`（return がない） |
| `func hello()` なのに `return 1` | `too many return values`（返す値が多すぎる） |
| `func add(a, b int) int` で `return "x"` | 文字列を int として返せない |

## ch03 多値を返す関数

Go の関数は**値を 2 つ以上まとめて返せます**。Python ではタプルで `return q, r` と書きましたが、Go では戻り値の型を `(int, int)` と括弧で並べ、受け取る側は多値代入（L9 で見た、左辺に変数を並べて一度に受ける形）`q, r := divide(a, b)` で受けます。`strconv.Atoi` が `(int, error)` を返していたのは、まさにこの仕組みです。🔴 「結果とエラーを一緒に返す」という Go の基本形につながるので、手が覚えるまで書きましょう。

Python ではこう書いた:

```python
def divide(a, b):
    return a // b, a % b

q, r = divide(17, 5)
```

Go ではこう書く:

```go
func divide(a, b int) (int, int) {
	return a / b, a % b
}

q, r := divide(17, 5)
```

### サンプルを1行ずつ読む

- `func divide(a, b int) (int, int) {` … 戻り値が 2 つあるので型を `(int, int)` と括弧で囲みます
- `return a / b, a % b` … 商と余りをカンマで並べて返します。17 / 5 = 3（int の割り算は切り捨て、L3）、17 % 5 = 2
- `q, r := divide(17, 5)` … 1 つ目の戻り値が `q`、2 つ目が `r` に入ります
- `q2, _ := divide(100, 7)` … 余りは使わないので `_` で捨てます（L13）。100 / 7 = 14

### 実行結果

```text
商: 3
余り: 2
100÷7 の商: 14
```

受け取る変数の数は戻り値の数と同じでなければなりません。`q := divide(17, 5)` と 1 つだけで受けると `assignment mismatch`（数が合わない）というコンパイルエラーになります。

## ch04 無名関数（lambda の代わり）

名前を付けずにその場で定義する関数を**無名関数**といいます。Python の `lambda` に相当しますが、lambda が 1 つの式しか書けなかったのに対し、Go の無名関数は**普通の関数と同じ書き方で複数行書けます**。変数に代入すれば `square(3)` のように呼び出せますし、関数の引数として渡すこともできます。🟡 「関数も値の一種として変数に入る」という理屈を理解しましょう。

Python ではこう書いた:

```python
square = lambda x: x * x
print(square(3))
```

Go ではこう書く:

```go
square := func(x int) int {
	return x * x
}
fmt.Println(square(3))
```

### `square := func(x int) int { ... }` の読み方

関数定義から名前を取った `func(x int) int { ... }` が無名関数です。それを `:=` で変数 `square` に入れています。以後 `square(3)` のように、普通の関数と同じ書き方で呼べます。

### サンプルを1行ずつ読む

- `square := func(x int) int { return x * x }` … int を受け取り 2 乗を返す関数を `square` に入れます
- `fmt.Println(square(3))` … 3*3 = 9
- `clamp := func(x int) int { ... }` … 0 未満なら 0、100 より大きければ 100、それ以外はそのまま返す関数です。`return` はその場で関数を終えるので、最初に当てはまった `return` の値が返ります
- `fmt.Println(clamp(-5), clamp(50), clamp(300))` … それぞれ 0、50、100 になり、空白区切りで 1 行に出ます

| 引数 | 通る道 | 戻り値 |
|---|---|---|
| -5 | `x < 0` が true | 0 |
| 50 | どちらの if も false | 50 |
| 300 | `x > 100` が true | 100 |

### 実行結果

```text
9
0 50 100
```

`main` の中では `func 名前(...)` の形で関数を定義できません（関数の中に名前付き関数は書けない）。関数の中で関数を作りたいときに使うのが、この無名関数です。
