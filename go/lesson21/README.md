# Lesson 21 構造体とメソッド

Python入門編「クラス」に対応するレッスンです。Go に `class` と `self` はなく、`type X struct` とレシーバ付きメソッドで書きます。`__init__` の代わりは慣習の `New` 関数、公開制御は名前の大文字小文字です。

## ch01 type X struct（class の代わり）

関連するデータをひとまとめにする入れ物が**構造体**です（L9 の `Point` で一度見ました）。Python では `class` で作りましたが、**Go に `class` はありません**。`type Person struct { ... }` で**フィールド**（データの項目）を型付きで並べ、`Person{Name: "佐藤", Age: 28}` で初期化し、`p.Name` で読み書きします。`__init__` を書かなくても、この初期化構文でそのまま値を詰められます。🔴 構造体は Go プログラムの中心なので、定義と初期化を手が覚えるまで書きましょう。

Python ではこう書いた:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Person("佐藤", 28)
print(p.name)
```

Go ではこう書く:

```go
type Person struct {
	Name string
	Age  int
}

p := Person{Name: "佐藤", Age: 28}
fmt.Println(p.Name)
```

### 定義の読み方

```go
type Person struct {
	Name string
	Age  int
}
```

| 部分 | 意味 |
|---|---|
| `type Person` | `Person` という名前の新しい型を作る |
| `struct { ... }` | 中身は構造体（複数の項目の組） |
| `Name string` | 項目名 `Name`、型 string |
| `Age  int` | 項目名 `Age`、型 int（空白の数は gofmt が縦をそろえるためのもの） |

`type` で作った `Person` は、`int` や `string` と同じように変数の型として使えます。

### サンプルを1行ずつ読む

- `p := Person{Name: "佐藤", Age: 28}` … `項目名: 値` で中身を入れて作ります
- `fmt.Println(p.Name, p.Age)` … `変数.項目名` で読みます。`佐藤 28`
- `p.Age = 29` … 同じ書き方で書き換えられます
- `q := Person{Name: "田中"}` … `Age` を書かなかったので int のゼロ値 0 になります（L4）

### 実行結果

```text
佐藤 28
29
田中 0
```

`fmt.Println(p)` と構造体を丸ごと渡すと `{佐藤 29}` のように中身が `{}` で囲まれて出ます。

## ch02 メソッドとレシーバ（self の代わり）

構造体に結び付いた関数を**メソッド**といい、`func` と関数名の間に**レシーバ**（メソッドを呼ばれる本人）を書きます。Python の `self` に当たるのがレシーバで、**Go に `self` というキーワードはありません**。名前は自分で決めます。フィールドを書き換えるメソッドはポインタレシーバ `(r *Rect)`、読むだけなら値レシーバ `(r Rect)` にします。🔴 `p.Method()` の形は毎日書くので、手が覚えるまで練習しましょう。

Python ではこう書いた:

```python
class Rect:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h
```

Go ではこう書く:

```go
type Rect struct {
	W, H int
}

// (r Rect) がレシーバ。中では r が self の代わり
func (r Rect) Area() int {
	return r.W * r.H
}
```

### `func (r Rect) Area() int {` の読み方

| 部分 | 意味 |
|---|---|
| `func` | 関数定義 |
| `(r Rect)` | レシーバ。「Rect 型の値に付くメソッドで、中ではその値を `r` と呼ぶ」 |
| `Area` | メソッド名 |
| `()` | 引数なし |
| `int` | 戻り値の型 |

普通の関数との違いは、`func` と名前の間の `(r Rect)` だけです。呼ぶときは `r.Area()` と `値.メソッド名()` の形にします。

### 値レシーバとポインタレシーバ

- `(r Rect)` … 値レシーバ。L20 の値渡しと同じで、`r` は呼び出し元のコピーです。書き換えても呼び出し元は変わりません
- `(r *Rect)` … ポインタレシーバ。L20 のポインタ渡しと同じで、`r` は呼び出し元の場所を指します。`r.W *= n` で呼び出し元の `W` が変わります

ポインタなのに `(*r).W` と書かず `r.W` と書けるのは、構造体のポインタに限って Go が自動で `*` を補ってくれるからです。呼ぶ側の `r.Scale(2)` も、Go が自動で `(&r).Scale(2)` と読み替えています。

### サンプルを1行ずつ読む

| 行 | r の中身 | 出力 |
|---|---|---|
| `r := Rect{W: 2, H: 3}` | W=2, H=3 | — |
| `fmt.Println(r.Area())` | 変化なし | 6（2*3） |
| `r.Scale(2)` | W=4, H=6 | — |
| `fmt.Println(r.Area())` | 変化なし | 24（4*6） |

`type Rect struct { W, H int }` の `W, H int` は、同じ型の項目 2 つを 1 行にまとめた書き方です。

### 実行結果

```text
6
24
```

`Scale` を値レシーバ `(r Rect)` にしてしまうと、コピーを 2 倍にするだけなので 2 回目も 6 のままになります。

## ch03 コンストラクタ関数 NewX

Go の構造体には Python の `__init__` のような特別な初期化メソッドは**ありません**。代わりに、初期値を詰めた構造体（へのポインタ）を返す普通の関数を、**`New` で始まる名前**で用意するのが慣習です。これを**コンストラクタ関数**と呼び、デフォルト値の設定や値の検証をこの 1 か所に集められます。戻り値は `*Player` のようにポインタにするのが定番です。🟡 「特別な構文ではなく、ただの関数と命名の約束」という点を理解しましょう。

Python ではこう書いた:

```python
class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100

p = Player("勇者")
```

Go ではこう書く:

```go
func NewPlayer(name string) *Player {
	return &Player{Name: name, HP: 100}
}

p := NewPlayer("勇者")
```

### `return &Player{Name: name, HP: 100}` の読み方

- `Player{Name: name, HP: 100}` … ch01 と同じ形で構造体を作ります
- 先頭の `&` … L20 で見た「場所を取り出す」記号です。作った構造体の場所（ポインタ）を返します
- 戻り値の型 `*Player` … 「Player の場所」という型です

ポインタで返すと、受け取った側で `q.HP -= 30` と書き換えたときに、別のコピーではなくその 1 つの Player が変わります。`p.Name` のように `*` なしで項目を読めるのは ch02 で見た自動補完のおかげです。

### サンプルを1行ずつ読む

- `p := NewPlayer("勇者")` … `NewPlayer` の中で HP 100 が入るので、呼ぶ側は名前だけ渡せば済みます
- `fmt.Println(p.Name, p.HP)` … `勇者 100`
- `q := NewPlayer("魔法使い")` → `q.HP -= 30` … 100 - 30 = 70

### 実行結果

```text
勇者 100
魔法使い 70
```

`NewPlayer` は特別な仕組みではなく、名前が `New` で始まるだけの普通の関数です。

## ch04 大文字小文字で公開制御

Go では名前の**先頭が大文字か小文字か**で公開範囲が決まります。先頭が大文字（`Name` や `Deposit`）なら他のパッケージ（L23 で扱う、Go のコードをまとめる単位。`fmt` や `strings` もパッケージです）からも使える**公開**、小文字（`balance`）ならそのパッケージの中だけの**非公開**です。Python の `_name` は「触らないで」という慣習にすぎませんでしたが、Go では言語仕様として強制されます。フィールドを小文字にして、公開メソッド経由でだけ操作させるのが定番の設計です。🟡 命名がそのまま設計になる、という理屈を押さえましょう。

Python ではこう書いた:

```python
class Wallet:
    def __init__(self):
        self._balance = 0  # _ は「触るな」の目印（強制力なし）

    def deposit(self, n):
        self._balance += n
```

Go ではこう書く:

```go
type Wallet struct {
	balance int // 小文字: パッケージの外から見えない
}

// 大文字: 公開メソッド。外からはこれ経由でだけ触れる
func (w *Wallet) Deposit(n int) {
	w.balance += n
}
```

### 実はもう使っていた大文字のルール

`fmt.Println`、`strings.Fields`、`strconv.Atoi` がすべて大文字で始まるのは、`fmt` などの**別パッケージから呼ぶために公開されている**からです。`fmt.println` と小文字で書くと、外からは見えない名前なので `undefined: fmt.println`（定義されていない）というコンパイルエラーになります。

### 同じパッケージの中では小文字も使える

このサンプルは 1 ファイル（`package main` 1 つ）なので、`main` から `w.balance` と書いても実は動きます。公開・非公開の区別が効くのは**パッケージの外から使うとき**だけです。ここでは「将来別パッケージに分けたときに外から触れない」ことを意識した書き方を練習しています。

### サンプルを1行ずつ読む

- `type Wallet struct { balance int }` … 小文字の `balance` は非公開の項目
- `func (w *Wallet) Deposit(n int) {` … ポインタレシーバ（ch02）。`if n > 0` のときだけ足します
- `func (w *Wallet) Balance() int { return w.balance }` … 残高を読むだけの公開メソッド
- `w := Wallet{}` … 全項目ゼロ値で作ります。`balance` は 0
- `w.Deposit(100)` → 100、`w.Deposit(-50)` → `n > 0` が false なので何もしない

### 実行結果

```text
100
```
