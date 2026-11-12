# Lesson 24 エラー処理

Python入門編「例外処理」に対応するレッスンです。Go に例外は存在せず、`try/except` の代わりに関数が `error` を値として返し、`if err != nil` で分岐します。`raise` の代替は `return err` です。

## ch01 Go に例外はない（error は戻り値）

Go に**例外**（Python の `raise` で投げて `except` で受け止める、処理の流れを飛び越えるエラーの仕組み）は存在しません。`try/except` はなく、失敗しうる関数は結果と一緒に `error`（失敗を表す組み込みの型。正体は L22 ch03 で見たインターフェースで、ch04 で詳しく扱います）を**戻り値として**返します。呼び出し側は `if err != nil` で失敗を判定します（`nil` は「エラーなし」を表す値）。`strconv.Atoi` でずっと書いてきた形こそが、Go のエラー処理そのものです。🔴 `if err != nil` は Go で最も頻出する形です。手が覚えるまで書きましょう。

Python ではこう書いた:

```python
try:
    n = int(s)
except ValueError:
    print("数値ではありません")
```

Go ではこう書く:

```go
n, err := strconv.Atoi(s)
if err != nil {
	fmt.Println("数値ではありません")
}
```

### `if err != nil` の読み方

- `!=` は「等しくない」（L11）
- `nil` は「何もない」を表す値（L6・L16 ch02 で見ました）。`err` が nil なら「エラーなし＝成功」です
- つまり `if err != nil {` は「エラーが入っていたら（失敗したら）」という意味です

| 渡した文字列 | n | err | `err != nil` |
|---|---|---|---|
| `"42"` | 42 | nil | false（成功） |
| `"abc"` | 0 | `strconv.Atoi: parsing "abc": invalid syntax` | true（失敗） |

### サンプルを1行ずつ読む

- `n, err := strconv.Atoi("42")` … 成功するので err は nil
- `if err != nil { ... } else { fmt.Println("変換成功:", n) }` … else 側に進みます
- `_, err = strconv.Atoi("abc")` … 値は捨て、`err` には `=` で代入し直します（`err` は宣言済みなので `:=` ではなく `=`。L19 ch04）
- `if err != nil { ... }` … 失敗したのでこちらに入ります

### 実行結果

```text
変換成功: 42
abc は数値にできません
```

`fmt.Println(err)` と err をそのまま出すと、上の表の英語のメッセージ `strconv.Atoi: parsing "abc": invalid syntax`（"abc" の解析で文法が正しくない）が表示されます。

Python の try/except はエラーが起きた行から except まで飛びますが、Go は飛びません。上から順に実行され、1 つ 1 つの呼び出しの直後に if で確かめます。

## ch02 errors.New と return err（raise の代替は return）

自分でエラーを作るには `errors.New("メッセージ")` を使います。Python の `raise` に相当するのはエラーを投げることではなく **`return err`**、つまりエラーを戻り値として返すことです。失敗しうる関数は `(結果, error)` の 2 値を返す形にし、成功時はエラーの位置に `nil` を返します。🔴 「失敗したら return 0, errors.New(...)、成功したら return 値, nil」の型を手が覚えるまで書きましょう。

Python ではこう書いた:

```python
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("0 では割れません")
    return a // b
```

Go ではこう書く:

```go
func divide(a, b int) (int, error) {
	if b == 0 {
		return 0, errors.New("0 では割れません")
	}
	return a / b, nil
}
```

### サンプルを1行ずつ読む

- `import ("errors"; "fmt")` … `errors` パッケージを使うので import に足します
- `func divide(a, b int) (int, error) {` … 戻り値の 2 つ目の型が `error`。L18 ch03 の多値返却です
- `return 0, errors.New("0 では割れません")` … `errors.New` はメッセージを持ったエラーを作って返す関数です。失敗したときの 1 つ目の値は使われないので、ゼロ値 0 を入れておくのが慣習です
- `return a / b, nil` … 成功したら 2 つ目に nil（エラーなし）
- `if result, err := divide(10, 2); err == nil {` … L10 の「条件の前の 1 文」。成功なので 5 を出力
- `if _, err := divide(7, 0); err != nil { fmt.Println(err) }` … 失敗。`Println` にエラーを渡すと、`errors.New` に渡したメッセージが出ます

| 呼び出し | 戻り値 1 | 戻り値 2 |
|---|---|---|
| `divide(10, 2)` | 5 | nil |
| `divide(7, 0)` | 0 | `0 では割れません` のエラー |

### 実行結果

```text
5
0 では割れません
```

Python の `raise` は関数をその場で抜けて呼び出し元の except まで飛びますが、Go の `return` は普通に値を返すだけです。呼び出し元が err を確かめなければ、エラーは誰にも気づかれずに終わります。

## ch03 fmt.Errorf("%w") と errors.Is（エラーの包み直しと判定）

下位のエラーに文脈を足して返すには、`fmt.Errorf` の書式 `%w`（wrap、エラーを包み込むこと）を使います。`fmt.Errorf` は `fmt.Sprintf`（L5）と同じ書式で文字列を組み立て、それをメッセージに持つエラーを返す関数です。包んだ後でも `errors.Is(err, 元のエラー)` で「原因はこのエラーか」を判定できます。Python で `raise RuntimeError("検索失敗") from e` と原因を保ったまま投げ直したことに相当します。🟡 「メッセージを足しても原因は失われない」という仕組みを理解しましょう。

Python ではこう書いた:

```python
try:
    find(name)
except KeyError as e:
    raise RuntimeError("検索失敗") from e
```

Go ではこう書く:

```go
if err != nil {
	return fmt.Errorf("検索失敗: %w", err) // 原因を包む
}
// errors.Is(err, ErrNotFound) で原因を判定できる
```

### サンプルを1行ずつ読む

- `var ErrNotFound = errors.New("見つかりません")` … パッケージ変数（L19 ch03）として、目印になるエラーを 1 つだけ作っておきます。名前を `Err` で始めるのが慣習です
- `return fmt.Errorf("検索 %s: %w", name, ErrNotFound)` … `%s` に name、`%w` に ErrNotFound のメッセージが入り、`検索 alice: 見つかりません` というエラーができます。`%w` を使うと、メッセージだけでなく「中に ErrNotFound が入っている」という情報も残ります
- `fmt.Println(err)` … 包んだ後のメッセージ全体が出ます
- `errors.Is(err, ErrNotFound)` … err そのもの、または err の中に包まれたエラーをたどり、ErrNotFound があれば true を返します

### `==` や `%v` ではだめな理由

| 比べ方 | 結果 | 理由 |
|---|---|---|
| `err == ErrNotFound` | false | err は包んだ新しいエラーで、ErrNotFound そのものではない |
| `errors.Is(err, ErrNotFound)`（`%w` で包んだ） | true | 中までたどって見つける |
| `errors.Is(err, ErrNotFound)`（`%v` で作った） | false | `%v` はメッセージを文字として埋め込むだけで、中身は残らない |

### 実行結果

```text
検索 alice: 見つかりません
true
```

## ch04 独自エラー型（Error() string を実装）

`error` の正体は、`Error() string` というメソッドを 1 つだけ要求するインターフェースです。自作の構造体にこのメソッドを実装すれば**独自エラー型**になり、「どの値で失敗したか」といった追加情報をエラー自体に持たせられます。Python で `class AgeError(Exception)` と例外クラスを定義したことに相当します。🟡 「エラーもただの型」という見方を理解しましょう。

Python ではこう書いた:

```python
class AgeError(Exception):
    def __init__(self, age):
        self.age = age
```

Go ではこう書く:

```go
type AgeError struct{ Age int }

func (e *AgeError) Error() string {
	return fmt.Sprintf("%d歳は成人ではありません", e.Age)
}
```

### なぜ `Error() string` を書くだけで error になるのか

`error` は Go に最初から用意されている、次の定義のインターフェースです。

```go
type error interface {
	Error() string
}
```

L22 ch03 の暗黙実装と同じで、`Error() string` メソッドを持つ型は自動的に `error` として扱えます。`fmt.Println(err)` は、中で `err.Error()` を呼んでその文字列を出力しています。

### サンプルを1行ずつ読む

- `type AgeError struct { Age int }` … 失敗した年齢を持つ構造体
- `func (e *AgeError) Error() string {` … ポインタレシーバ（L21 ch02）でメソッドを付けます。このため error を満たすのは `AgeError` ではなく `*AgeError`（ポインタ）です
- `return fmt.Sprintf("%d歳は成人ではありません", e.Age)` … メッセージを組み立てて返します
- `func checkAge(age int) error {` … 戻り値の型は `error`
- `return &AgeError{Age: age}` … `&` で構造体のポインタを作って返します（L21 ch03）。`*AgeError` は error を満たすので、error として返せます
- `return nil` … 20 歳以上なら nil（エラーなし）
- `if err := checkAge(15); err != nil { fmt.Println(err) }` … 失敗。`Error()` が返したメッセージが出ます

### 実行結果

```text
15歳は成人ではありません
30歳は成人です
```

## ch05 panic と recover（本当に使う場面は少ない）

`panic` はプログラムを即座に停止へ向かわせる仕組み、`recover` は `defer` した関数の中でだけ panic を捕まえて復帰できる関数です（`defer` は下で説明します）。Python の例外と `except` に似ていますが、Go では通常の失敗は `error` で返すのが原則で、panic は「続行できないバグ」のような場面に限られます。本当に使う場面は少ない機能です。⚪ 存在と使いどころだけ知っておきましょう。

Python ではこう書いた:

```python
try:
    risky()
except Exception as e:
    print("回復:", e)
```

Go ではこう書く:

```go
defer func() {
	if r := recover(); r != nil {
		fmt.Println("recover:", r)
	}
}()
```

### `defer` とは

`defer 関数呼び出し` と書くと、その呼び出しは**今いる関数が終わる直前**まで後回しにされます。関数が普通に終わっても、panic で終わる途中でも必ず実行されます。

```go
defer fmt.Println("defer 1")
defer fmt.Println("defer 2")
fmt.Println("main end")
```

この 3 行を main に書くと、出力は次の順です。複数の defer は、後に書いたものから先に実行されます。

```text
main end
defer 2
defer 1
```

### `defer func() { ... }()` の読み方

- `func() { ... }` … L18 ch04 で見た無名関数
- 最後の `()` … 作った無名関数をその場で呼ぶ、という意味。`defer` と組み合わせて「この無名関数を関数の終わりに呼ぶ」になります
- `if r := recover(); r != nil {` … `recover()` は panic が起きていればその値（ここでは `"負の数は扱えません"`）を、起きていなければ nil を返します

### サンプルを1行ずつ読む

1. `defer func() { ... }()` … recover する無名関数を予約します（まだ実行されない）
2. `fmt.Println(mustPositive(3))` … 30 を出力
3. `mustPositive(-1)` … `panic("負の数は扱えません")` が起き、main の残りの行は飛ばされます
4. main が終わる直前に、予約した無名関数が実行され、`recover()` が panic の値を受け取って出力します。panic は止まり、プログラムは普通に終わります

### 実行結果

```text
30
recover: 負の数は扱えません
```

`ここは実行されません` は出ません。

### recover しないと

`defer` の部分がなければ、panic でプログラムが止まり、次のように表示されます（後ろに続く行は、どこで起きたかの情報です）。

```text
panic: 負の数は扱えません

goroutine 1 [running]:
...
```
