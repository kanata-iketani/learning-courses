# Lesson 23 パッケージとモジュール

Python入門編「モジュール」に対応するレッスンです。Go には `if __name__ == "__main__"` がなく、`package main` の `func main` が唯一の入口です。import の書き方、`go mod init` と複数ファイル分割、main より先に走る `init()` を学びます。

## ch01 package と main が入口

Go のソースファイルは必ず `package` 宣言（このファイルが属するパッケージ名の表明）で始まります。実行プログラムは `package main` に属し、その中の `func main` が**唯一の入口**です。Python では import されたとき（別のファイルから読み込まれたとき）に実行されないよう `if __name__ == "__main__":` というガードを書きましたが、Go にこのガードはありません。実行は常に main から始まり、それ以外の関数は呼ばれるまで動かないからです。🟡 「入口は main だけ」という決まりを理解しましょう。

Python ではこう書いた:

```python
def main():
    print("hello")

if __name__ == "__main__":
    main()  # import 時に走らないためのガード
```

Go ではこう書く:

```go
package main

func main() { // ここが唯一の入口。ガードは不要
	fmt.Println("hello")
}
```

### パッケージとは

Go のコードは**パッケージ**という単位でまとまっています。`fmt`、`strings`、`strconv` もそれぞれパッケージです。自分で書くプログラムは `package main` という特別なパッケージに入れます。`main` という名前のパッケージだけが「実行できるプログラム」になり、それ以外の名前のパッケージは他から import して使う部品になります。

### サンプルを1行ずつ読む

- `package main` … このファイルは main パッケージに属する、という宣言。ファイルの最初の行（コメントを除く）に必ず書きます
- `func greet(name string) string { ... }` … 定義しただけでは動きません。`"こんにちは、" + name + " さん"` は L5 で見た `+` による文字列の連結です
- `func main() { ... }` … `go run` すると、ここから実行が始まります
- `fmt.Println(greet("Gopher"))` … ここで初めて `greet` が呼ばれます
- `main` の最後の行が終わると、プログラム全体が終了します

### 実行結果

```text
こんにちは、Gopher さん
main が終わるとプログラムも終わります
```

`package main` の中に `func main` がないと、`function main is undeclared in the main package`（main パッケージに main 関数がない）というエラーで実行できません。

## ch02 import と標準ライブラリ（math・os など）

**標準ライブラリ**（Go に最初から付属するパッケージ群）はインストール不要で、`import` するだけで使えます。複数のパッケージは括弧でまとめて書きます。Python の `from math import sqrt` のように関数だけを取り出す書き方はなく、常に `math.Sqrt` のように**パッケージ名.関数名**で呼びます。`os`（OS まわりの機能）、`time`（時刻）、`math/rand`（乱数）なども同じ形で使います。🟡 まとめ書きの形に慣れましょう。

Python ではこう書いた:

```python
import math
from math import sqrt  # 関数だけ取り出せる
print(sqrt(16))
```

Go ではこう書く:

```go
import (
	"fmt"
	"math"
)

fmt.Println(math.Sqrt(16)) // 常に パッケージ名.関数名
```

### サンプルを1行ずつ読む

| 行 | 意味 | 出力 |
|---|---|---|
| `math.Sqrt(16)` | 平方根（√16） | 4 |
| `math.Pow(2, 8)` | 2 の 8 乗（L3） | 256 |
| `math.Abs(-3.5)` | 絶対値（符号を取る） | 3.5 |
| `math.Floor(9.876)` | 小数点以下を切り捨て | 9 |
| `len(os.Args) > 0` | コマンドライン引数の個数が 0 より大きいか | true |

- `math` の関数は float64（小数の型、L3）を受け取って float64 を返します。結果が 4.0 でも、`Println` は小数部が 0 の float64 を `4` と表示します
- `os.Args` … プログラムを起動したときのコマンドライン引数（`go run main.go a b` の `a b` のように、起動時に付けて渡す文字列）が入った `[]string` です。先頭の `os.Args[0]` にはプログラム自身の名前が入るので、長さは必ず 1 以上です

### 実行結果

```text
4
256
3.5
9
true
```

### 演習で使う型の変換

`a` と `b` が int のとき、`math.Pow(a, b)` とそのまま渡すとコンパイルエラーです。L3 で見たように `float64(a)` で float64 に変換して渡し、返ってきた float64 を `int(...)` で int に戻します。

```go
p := int(math.Pow(float64(a), float64(b))) // 2, 10 なら 1024
```

`int(...)` は小数点以下を切り捨てます（float64 の変数 `f` が 3.9 なら `int(f)` は 3）。

`import` したのに使わないパッケージがあると、`"os" imported and not used`（import したのに使っていない）というコンパイルエラーになります。未使用変数と同じく、Go は使わないものを残させません。

## ch03 go mod init と複数ファイル

**モジュール**は依存パッケージとバージョンを管理する単位で、`go mod init 名前` を実行すると管理ファイル `go.mod` が作られます（名前は `example.com/hello` のような、他と重ならない文字列。練習なら何でも構いません）。同じディレクトリで同じ `package main` を宣言したファイル同士なら、別ファイルの関数を **import なしで**そのまま呼べます。Python では別ファイルに分けたら `import` が必要でしたが、Go はパッケージ単位で 1 つの空間を共有します。実行は `go run .` とディレクトリごと指定します。🟡 まず 1 ファイル内の関数分割で感覚をつかみましょう。

Python ではこう書いた:

```python
# helper.py に分けたら import が必要
from helper import add
print(add(1, 2))
```

Go ではこう書く:

```go
// helper.go（同じ package main）に書いた add は
// main.go から import なしで呼べる
fmt.Println(add(1, 2))
```

### 手元で 2 ファイルに分けて試す手順

```text
hello/
├── go.mod      ← go mod init で作られる
├── main.go     ← package main と func main
└── calc.go     ← package main と func sum, func average
```

1. 空のフォルダ `hello` を作り、その中で `go mod init example.com/hello` を実行します。中身が次の `go.mod` ができます（`go 1.22.2` の部分は自分の Go のバージョン）

```text
module example.com/hello

go 1.22.2
```

2. `calc.go` の先頭に `package main` と書き、その下に `sum` と `average` を置きます
3. `main.go` には `package main`、`import "fmt"`、`func main` だけを置きます
4. `go run .` で実行します。`.` は「今いるフォルダ」の意味で、フォルダ内の `.go` ファイルをまとめて 1 つのプログラムにします。`go run main.go` と 1 ファイルだけ指定すると、`calc.go` が読まれず `undefined: sum` になります

この学習アプリの演習は 1 ファイルで採点するので、関数は main と同じファイルに書きます。

### サンプルを1行ずつ読む

- `func sum(nums []int) int` … スライスを受け取り合計を返します（L18）。80+90+70+100 = 340
- `func average(nums []int) int { return sum(nums) / len(nums) }` … 関数の中から別の関数を呼べます。340 / 4 = 85（int の割り算なので小数は切り捨て）

### 実行結果

```text
合計: 340
平均: 85
```

## ch04 init()（main より先に走る初期化関数）

`init()` は、パッケージが読み込まれたときに **main より先に自動で実行される**初期化関数です。自分で呼び出すコードは書きません。Python でモジュールのトップレベルに書いたコードが import 時に実行されるのと同じ役割です。便利な半面、多用すると処理の流れが追いにくくなるため、実務では設定の初期化など限られた場面で使われます。⚪ 「main より先に走る関数がある」ことだけ知っておきましょう。

Python ではこう書いた:

```python
# module.py のトップレベルコードは import 時に走る
print("読み込みました")
```

Go ではこう書く:

```go
func init() {
	fmt.Println("main より先に実行される")
}
```

### 実行の順番

`go run` すると、次の順で動きます。

1. パッケージ変数（関数の外の `var`、L19）の準備。ここでは `config` が空文字列 `""` で作られる
2. `init()` が自動で呼ばれる。`config` に `"日本語モード"` が入り、1 行目が出力される
3. `main()` が呼ばれる。`config` はすでに設定済み

### サンプルを1行ずつ読む

- `var config string` … パッケージ変数。初期値はゼロ値 `""`
- `func init() { ... }` … 名前を `init` にした、引数も戻り値もない関数は特別扱いされ、main より先に自動で 1 回だけ呼ばれます。自分で `init()` と呼ぶコードを書くとコンパイルエラーになります
- `fmt.Println("main: 設定 =", config)` … init が入れた値が出ます

### 実行結果

```text
init: 設定を初期化しました
main: 設定 = 日本語モード
```
