# Lesson 15 標準入力

Python入門編「標準入力」に対応するレッスンです。Python の `input()` 相当が Go では `bufio.Scanner` を使った 4 行になります。コーディングテストはこの定型が書ければ戦えるため、理屈と合わせて丸暗記してください。

## コーディングテスト用テンプレート

```go
package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	sc := bufio.NewScanner(os.Stdin)
	sc.Buffer(make([]byte, 1024*1024), 1024*1024) // 長い行に備えて上限を拡大

	// 1 行目: 整数 N
	sc.Scan()
	n, _ := strconv.Atoi(sc.Text())

	// 2 行目: 空白区切りの N 個の整数
	sc.Scan()
	f := strings.Fields(sc.Text())
	nums := make([]int, n)
	for i := range n {
		nums[i], _ = strconv.Atoi(f[i])
	}

	fmt.Println(nums)
}
```

## ch01 bufio.Scanner で 1 行読む

**標準入力**（キーボードやテストケースからプログラムに渡されるデータ）を読むには bufio.Scanner を使います。Python の input() 相当が、Go では「Scanner を作る → Scan() で 1 行読む → Text() で取り出す」と 4 行かかります。理屈より先に、この定型を丸暗記することがコーディングテスト攻略の近道です。Text() が返す文字列に改行は含まれません。🔴 手が覚えるまで何度も書きましょう。

Python ではこう書いた:

```python
s = input()
print(s)
```

Go ではこう書く:

```go
sc := bufio.NewScanner(os.Stdin)
sc.Scan()
s := sc.Text()
fmt.Println(s)
```

### import する 3 つのパッケージ

- `bufio` … buffered I/O の略。入力をまとめて読み込んでおき、1 行ずつ取り出す道具（Scanner）が入っています
- `os` … OS とのやり取りの道具。`os.Stdin` が「標準入力」そのものを表します
- `fmt` … 出力用（L2）

複数のパッケージは `import ( ... )` と括弧でまとめて 1 行に 1 つずつ書きます（L23 でも扱います）。

### サンプルを1行ずつ読む

- `sc := bufio.NewScanner(os.Stdin)` … 標準入力を読む Scanner を作って `sc` に入れます。`NewScanner` は「新しい Scanner を作って返す」関数です。この時点ではまだ何も読んでいません
- `sc.Scan()` … 次の 1 行を読み込み、Scanner の中に覚えておきます。`sc.Scan()` のように `変数.名前()` で呼ぶ関数をメソッドといいます（L21 で詳しく扱います）
- `line := sc.Text()` … 直前の `Scan()` で読んだ行を文字列として取り出します。末尾の改行は取り除かれています
- `fmt.Println("入力:", line)` … 読んだ文字列を出力します

### 実行例

入力（標準入力に `Tanaka` を 1 行渡したとき）:

```text
Tanaka
```

出力:

```text
入力: Tanaka
```

### `Scan()` の戻り値

`sc.Scan()` は読めたら `true`、入力が終わって読む行がなければ `false` を返します（bool、L11）。このチャプターのように 1 行だけ読むときは戻り値を使わずに捨てていますが、L19 で出てくる `for sc.Scan() { ... }` は「読める間ずっと繰り返す」（L12 の `for 条件 {}`）という意味になります。入力 `a`、`b` の 2 行に対して呼ぶと次のようになります。

| 呼んだ回数 | Scan() の戻り値 | Text() |
|---|---|---|
| 1 回目 | true | "a" |
| 2 回目 | true | "b" |
| 3 回目 | false | ""（もう行がない） |

## ch02 読んだ文字列を数値へ（strconv.Atoi）

Scanner が読み取った行は必ず文字列なので、数値として計算するには strconv.Atoi で変換します。Atoi は (int, error) の 2 つを返しますが（L6 で見たとおり、2 つ目の err は変換に失敗したときだけ中身が入ります）、コーディングテストでは入力形式が保証されているため、n, _ := strconv.Atoi(...) と書いて err を _ で捨てるのが定石です。Python なら int(input()) の 1 行で済む処理が、Go では 4 行の定型 + 変換 1 行になります。これも考えずに書けるまで丸暗記します。🔴 手が覚えるまで書きましょう。

Python ではこう書いた:

```python
n = int(input())
```

Go ではこう書く:

```go
sc := bufio.NewScanner(os.Stdin)
sc.Scan()
n, _ := strconv.Atoi(sc.Text())
```

### サンプルを1行ずつ読む

- `sc := bufio.NewScanner(os.Stdin)` と `sc.Scan()` … ch01 の定型。1 行読みます
- `n, _ := strconv.Atoi(sc.Text())` … 読んだ文字列 `"20"` を整数 `20` に変換して `n` に入れます。2 つ目の戻り値（エラー）は `_`（L13 で見たブランク識別子）で捨てています
- `fmt.Println("2倍:", n*2)` … `n` は int なので計算できます。`sc.Text()` のまま `"20"*2` とはできません（文字列と数値は別の型。L6）

### 実行例

入力:

```text
20
```

出力:

```text
2倍: 40
10足す: 30
```

`_` で err を捨てているので、`abc` のような数値でない行を渡すと `n` は 0 になり、エラーにも気づけません。入力の形が保証されているテスト問題だから許される書き方です。実務の書き方は L24 で扱います。

## ch03 1 行に複数の値（strings.Fields で分割）

1 行に複数の値が空白区切りで並ぶ入力は、strings.Fields で分割します。Fields は文字列を空白で区切って []string を返す関数で（L8 で見ました）、Python の split() に相当します。数値が必要な要素は、取り出してから strconv.Atoi で 1 つずつ変換します。Python の map(int, input().split()) のような一括変換は Go にないため、ここでも行数は増えます。🔴 「Fields で割って Atoi」の流れを手が覚えるまで書きましょう。

Python ではこう書いた:

```python
a, b = map(int, input().split())
```

Go ではこう書く:

```go
sc.Scan()
f := strings.Fields(sc.Text())
a, _ := strconv.Atoi(f[0])
b, _ := strconv.Atoi(f[1])
```

### サンプルを1行ずつ読む

入力 `3 5` を読んだときの値の変化です。

| 行 | 結果 |
|---|---|
| `sc.Scan()` | 1 行読む |
| `f := strings.Fields(sc.Text())` | `f` は `[]string{"3", "5"}`（文字列 2 つ） |
| `a, _ := strconv.Atoi(f[0])` | `f[0]` は 1 つ目の `"3"`。`a` は整数 3 |
| `b, _ := strconv.Atoi(f[1])` | `f[1]` は 2 つ目の `"5"`。`b` は整数 5 |
| `fmt.Println("個数:", len(f))` | 分割した要素の数 2 |
| `fmt.Println("和:", a+b)` | 8 |

`f[0]` の `[0]` はスライスの位置番号です（L7）。

### 実行例

入力:

```text
3 5
```

出力:

```text
個数: 2
和: 8
```

## ch04 複数行の入力（N を読んでから N 行読む）

「1 行目に件数 N、続けて N 行のデータ」という形式はコーディングテストの最頻出パターンです。まず 1 行目を読んで Atoi で N に変換し、for の中で sc.Scan() と sc.Text() を繰り返して N 行を読みます。Scan() は呼ぶたびに次の行へ進むので、Python で input() をループの中で呼んだのと同じ感覚です。input() 相当が 4 行かかる Go でも、この骨組みさえ覚えれば複数行入力は怖くありません。🔴 試験本番で迷わないよう、手が覚えるまで書きましょう。

Python ではこう書いた:

```python
n = int(input())
for i in range(n):
    line = input()
```

Go ではこう書く:

```go
sc.Scan()
n, _ := strconv.Atoi(sc.Text())
for range n {
	sc.Scan()
	line := sc.Text()
}
```

### `for range n` と `for i := range n`

本文の `for range n {}` は、位置番号も使わないので変数を書かずに「n 回繰り返す」だけの形です（Go 1.22 以降）。サンプルでは何行目かを表示したいので `for i := range n` と `i` を受け取っています（L13）。

### サンプルを1行ずつ読む

入力が次の 4 行のときを追います。

```text
3
10
20
30
```

| 行 | 何が起きるか |
|---|---|
| `sc.Scan()` + `n, _ := strconv.Atoi(sc.Text())` | 1 行目 `"3"` を読み、`n` は 3 |
| `for i := range n {` | `i` が 0, 1, 2 と 3 回回る |
| ループ 1 回目の `sc.Scan()` | 2 行目 `"10"` を読む |
| ループ 2 回目の `sc.Scan()` | 3 行目 `"20"` を読む |
| ループ 3 回目の `sc.Scan()` | 4 行目 `"30"` を読む |
| `fmt.Printf("%d行目: %s\n", i+1, sc.Text())` | `%d` に番号、`%s` に読んだ文字列（L2） |

`Scan()` は呼ぶたびに 1 行ずつ先へ進み、前に読んだ行には戻りません。

### 実行結果

```text
1行目: 10
2行目: 20
3行目: 30
```

演習では、`sc.Text()` を `strconv.Atoi` で整数にしてから `sum += v` のように足していきます。

## ch05 コーディングテスト定型テンプレート総まとめ

このレッスンの総まとめとして、コーディングテスト用の定型テンプレートを丸ごと覚えます。bufio.Scanner を作り、Buffer で読める行の上限を広げ、strings.Fields で行を分割し、strconv.Atoi で数値化する。Python なら input().split() の 1 行で済む処理に、Go では input() 相当だけで 4 行かかります。だからこそ、この一式を考えずに白紙から書き出せるよう丸暗記しておくことが重要です。🔴 1 分で書けるようになるまで繰り返しましょう。

Python ではこう書いた:

```python
n = int(input())
nums = list(map(int, input().split()))
```

Go ではこう書く:

```go
sc := bufio.NewScanner(os.Stdin)
sc.Buffer(make([]byte, 1024*1024), 1024*1024)
sc.Scan()
n, _ := strconv.Atoi(sc.Text())
sc.Scan()
f := strings.Fields(sc.Text())
```

### `sc.Buffer(make([]byte, 1024*1024), 1024*1024)` とは

Scanner は 1 行の長さに上限があり、何も設定しないと約 64KB（6 万 5 千文字程度）を超える行を読めません。超えると `Scan()` が false を返し、その行は読めずに終わります。入力の 2 行目に数十万個の数が並ぶような問題に備えて、上限を広げるのがこの 1 行です。

- `make([]byte, 1024*1024)` … 1024×1024 = 1,048,576 バイト（1MB）の作業場所を作ります。`make` はスライスなどを指定サイズで作る組み込み関数で、`[]byte` はバイト（L5 で見た、文字列を構成する 1 バイトの数値）のスライスです
- 2 つ目の引数 `1024*1024` … 1 行の最大の長さ（バイト）。ここでは 1MB まで読めるようにしています

`sc.Scan()` より前に 1 回だけ書きます。中身を毎回理解する必要はなく、「長い行への備え」として丸ごと書けば十分です。

### サンプルを1行ずつ読む

入力 `5` / `3 1 4 1 5` のときを追います。

| 行 | 結果 |
|---|---|
| `sc.Scan()` + `n, _ := strconv.Atoi(sc.Text())` | `n` は 5 |
| `sc.Scan()` + `f := strings.Fields(sc.Text())` | `f` は `["3" "1" "4" "1" "5"]` |
| `sum := 0` | 合計用の変数 |
| `for i := range n {` | `i` が 0〜4 |
| `v, _ := strconv.Atoi(f[i])` | `i` 番目の文字列を整数に |
| `sum += v` | 3 → 4 → 8 → 9 → 14 |
| `fmt.Println(sum)` | 14 を出力 |

### 実行結果

```text
14
```

演習で最大値も求めるときは、`maxV := 0` のような変数を用意し、`if v > maxV { maxV = v }` で大きい値に入れ替えていきます。入力に負の数が来る可能性がある問題では、`maxV` の初期値を最初の要素にしておくと安全です。
