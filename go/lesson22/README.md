# Lesson 22 埋め込みとインターフェース

Python入門編「クラスの継承」に対応するレッスンです。Go に継承は存在しないため、`class Child(Parent)` に相当する構文はありません。代わりに構造体の埋め込み（has-a）とインターフェース（振る舞いの契約）で同じ目的を達成します。

## ch01 Go に継承はない（is-a ではなく has-a で考える）

Go に**継承**（親クラスの項目やメソッドを子クラスがそのまま引き継ぐ仕組み）は存在しません。Python の `class Dog(Animal)` のような親子関係（is-a、「Dog は Animal である」という関係）は書けず、**has-a**（ある型が別の型をフィールドとして持つこと）で考えます。継承ツリーを設計する代わりに、部品となる構造体を組み合わせて型を作り、共通の振る舞いは埋め込み（ch02）とインターフェース（ch03）で表現します。🟡 まずは「is-a ではなく has-a で考える」という発想の転換を理解しましょう。

Python ではこう書いた:

```python
class Dog(Animal):  # Dog は Animal である (is-a)
    pass
```

Go ではこう書く:

```go
type Dog struct {
	Animal Animal // Dog は Animal を持つ (has-a)
	Breed  string
}
```

### サンプルを1行ずつ読む

- `type Animal struct { Name string; Cry string }` … 名前と鳴き声を持つ部品の構造体（L21）
- `type Dog struct { Animal Animal; Breed string }` … 項目名 `Animal`、型 `Animal` の項目を持ちます。左が項目名、右が型です。同じ綴りなので紛らわしいですが、`Pet Animal` と書いても同じ意味になります
- `d := Dog{ Animal: Animal{Name: "ポチ", Cry: "ワン"}, Breed: "柴犬" }` … 構造体の中に構造体を入れて作ります。外側の `Animal:` は項目名、内側の `Animal{...}` は型の値です
- `d.Animal.Name` … `d` の項目 `Animal` の、さらに項目 `Name`。2 段たどって `"ポチ"` に届きます

| 式 | 値 |
|---|---|
| `d.Breed` | 柴犬 |
| `d.Animal` | `{ポチ ワン}` |
| `d.Animal.Name` | ポチ |
| `d.Animal.Cry` | ワン |

### 実行結果

```text
ポチ は 柴犬 です
ポチ は ワン と鳴きます
```

## ch02 構造体の埋め込み（フィールドとメソッドの昇格）

フィールド名を書かずに型名だけを書くと**埋め込み**になります。埋め込んだ内側の型のフィールドとメソッドは外側の型に**昇格**（外側の変数から直接呼べるようになること）し、`e.Person.Name` を `e.Name` と短く書けます。Python の継承でメソッドを引き継いだのと似た見た目になりますが、実体はあくまで has-a であり、親子関係ではありません。🟡 昇格の仕組みを理解しましょう。

Python ではこう書いた:

```python
class Employee(Person):
    pass  # Person のメソッドをそのまま使える

e.greet()
```

Go ではこう書く:

```go
type Employee struct {
	Person  // フィールド名なし = 埋め込み
	Company string
}

e.Greet() // Person のメソッドが昇格して直接呼べる
```

### 埋め込みと普通の項目の違い

| 書き方 | 種類 | 名前へのアクセス |
|---|---|---|
| `Person Person` | 普通の項目（ch01） | `e.Person.Name` だけ |
| `Person`（型名だけ） | 埋め込み | `e.Name` でも `e.Person.Name` でも可 |

埋め込みでも、内側には型名と同じ名前 `Person` の項目があるものとして扱われます。だから作るときは `Person: Person{...}` と書きます。

### サンプルを1行ずつ読む

- `func (p Person) Greet() string { return fmt.Sprintf("こんにちは、%s です", p.Name) }` … L21 の値レシーバのメソッド。`fmt.Sprintf` は出力せずに文字列を作って返します（L5）
- `type Employee struct { Person; Company string }` … `Person` を埋め込み、さらに `Company` を足します
- `e.Name` … `Employee` には直接 `Name` がありませんが、埋め込んだ `Person` の `Name` が昇格して見えます。Go が `e.Person.Name` と読み替えます
- `e.Greet()` … 同様に `e.Person.Greet()` と読み替えられます。`Greet` の中の `p` には `e.Person` が入ります

### 実行結果

```text
田中
こんにちは、田中 です
ゴーファー商事
```

演習の `Introduce` はスターターに定義済みの `Person` のメソッドです。`Person` を埋め込んだ `Employee` を作れば `e.Introduce()` と直接呼べます。スターターの `_ = name` は、まだ使っていない変数で未使用エラーが出ないよう `_` に代入しておく一時的な行です（L13 ch03）。自分のコードで `name` などを使ったら消して構いません。

## ch03 インターフェース（振る舞いの契約と暗黙実装）

**インターフェース**は「この型はこのメソッドを持つ」という振る舞いの契約です。Go には `implements` のような宣言がなく、契約どおりのメソッドを持つ型は自動的にそのインターフェースを満たします（**暗黙実装**）。Python のダックタイピング（同名メソッドがあれば動くという流儀）に近い柔らかさを、コンパイル時の型検査つきで実現します。継承の代わりに「同じ振る舞いの型をまとめて扱う」のが役割です。🟡 契約という考え方を理解しましょう。

Python ではこう書いた:

```python
class Dog:
    def speak(self):  # 同名メソッドがあれば動く
        return "ワン"
```

Go ではこう書く:

```go
type Speaker interface {
	Speak() string // この契約を満たす型は自動的に Speaker
}
```

### 定義の読み方

```go
type Speaker interface {
	Speak() string
}
```

「`Speak()` という名前で、引数なし・string を返すメソッドを持っている型なら、何でも `Speaker` として扱える」という宣言です。中身（どう鳴くか）は書かず、メソッドの形だけを並べます。

`Dog` にも `Cat` にも `func (d Dog) Speak() string` のようなメソッドがあるので、どちらも `Speaker` を満たします。`Dog` 側に「Speaker を満たします」と書く場所はありません。これが暗黙実装です。

### サンプルを1行ずつ読む

- `speakers := []Speaker{Dog{Name: "ポチ"}, Cat{Name: "タマ"}}` … 要素の型が `Speaker` のスライス。`Dog` と `Cat` という別の型の値を同じスライスに入れられます
- `for _, s := range speakers {` … `s` の型は `Speaker`。1 回目は中身が `Dog`、2 回目は `Cat` です
- `s.Speak()` … 中身の型のメソッドが呼ばれます。1 回目は `Dog` の、2 回目は `Cat` の `Speak` です

### 実行結果

```text
ポチ: ワン
タマ: ニャー
```

### 満たしていない型を入れると

`Speak` を持たない型（例えば `type Fish struct{}`）を `[]Speaker{Fish{}}` に入れると、次のようなコンパイルエラーになります。

```text
cannot use Fish{} (value of type Fish) as Speaker value in array or slice literal: Fish does not implement Speaker (missing method Speak)
```

「Fish は Speak メソッドがないので Speaker を満たさない」という意味です。Python のダックタイピングなら実行時に初めて分かる間違いを、Go は実行前に見つけます。

### 演習のヒント

`var s Speaker` で `Speaker` 型の変数を宣言し、if で `s = Dog{Name: name}` か `s = Cat{Name: name}` を代入してから `fmt.Println(s.Speak())` と書けます。
