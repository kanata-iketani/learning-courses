# Lesson 11 ブール型

Python入門編「ブール型」に対応するレッスンです。`and` `or` `not` は `&&` `||` `!` になります。Go に `in` 演算子はなく、スライスは `slices.Contains`、文字列は `strings.Contains` で調べます。

## ch01 bool 型と比較演算子

真偽を表す型が `bool`（真か偽かの 2 値だけを持つ型）で、値は小文字の `true` と `false` です。Python の `True` / `False` とは先頭の大文字小文字が違います。比較演算子 `==` `!=` `<` `<=` `>` `>=` は Python と同じで、結果は bool 型になります。ただし `0 < x < 10` のような比較の連結はできず、次章で学ぶ `&&` で 2 つの比較に分けます。🔴 比較の結果を bool として変数に入れて使う形を、手が覚えるまで書きましょう。

Python ではこう書いた:

```python
is_adult = True
print(age >= 20)
```

Go ではこう書く:

```go
isAdult := true
fmt.Println(age >= 20)
```

### 比較演算子の一覧

- `age == 18` → 意味: 等しい ／ `age` が 18 のとき: true
- `age != 18` → 意味: 等しくない ／ `age` が 18 のとき: false
- `age < 20` → 意味: より小さい ／ `age` が 18 のとき: true
- `age <= 18` → 意味: 以下 ／ `age` が 18 のとき: true
- `age > 20` → 意味: より大きい ／ `age` が 18 のとき: false
- `age >= 20` → 意味: 以上 ／ `age` が 18 のとき: false

L10 の if の条件に書いていたのは、すべてこの「結果が bool になる式」です。

### 変数名の付け方

Python では `is_adult` のように `_` でつなぎましたが、Go では `isAdult` のように 2 語目以降の頭を大文字にするのが慣習です（キャメルケースと呼びます）。

### サンプルを 1 行ずつ読む

- `isSunny := true` → 説明: isSunny は bool 型
- `fmt.Println(isSunny)` → 出力: `true`
- `fmt.Println(age >= 20)` → 出力: `false` ／ 説明: 18 >= 20 は成り立たない
- `fmt.Println(age == 18)` → 出力: `true`
- `canVote := age >= 18` → 説明: 右辺の比較を先に計算し、結果の true を canVote に入れる
- `fmt.Println("投票できる:", canVote)` → 出力: `投票できる: true`

実行結果:

```text
true
false
true
投票できる: true
```

### 比較を連結したときのエラー

`0 < x < 10` と書くと、まず `0 < x` が bool になり、次に「bool < 10」を計算しようとして型が合わず、エラーになります。

```text
invalid operation: 0 < x < 10 (mismatched types untyped bool and untyped int)
```

## ch02 && と || と !（and or not の代わり）

Python の `and` `or` `not` は、Go では記号の `&&` `||` `!` になります。`&&` は両方が true のとき true、`||` はどちらかが true のとき true、`!` は真偽を反転します。単語のまま `and` と書くとコンパイルエラーです。前章で触れたとおり比較の連結はできないため、Python の `0 < x < 10` は `x > 0 && x < 10` と書きます。🔴 この 3 つの記号は条件分岐の中核なので、手が覚えるまで書きましょう。

Python ではこう書いた:

```python
if x > 0 and x < 10:
    print("1桁")
```

Go ではこう書く:

```go
if x > 0 && x < 10 {
	fmt.Println("1桁")
}
```

### 記号の読み方と結果の表

`&&` はアンド、`||` はオア（`|` は縦棒。多くのキーボードで Shift + `¥` か Shift + `\`）、`!` はノットと読みます。

```text
A      B      A && B   A || B
true   true   true     true
true   false  false    true
false  true   false    true
false  false  false    false

A      !A
true   false
false  true
```

### サンプルを 1 行ずつ読む（x は 7）

- `x > 0 && x < 10` → 計算: true && true ／ 出力: `true`
- `x < 0 || x > 5` → 計算: false || true ／ 出力: `true`
- `!(x == 7)` → 計算: `x == 7` は true、それを反転 ／ 出力: `false`
- `if x > 0 && x < 10 {` → 計算: true なので中を実行 ／ 出力: `1桁の正の数です`

`!(x == 7)` の括弧は必要です。`!` は直後の 1 つの値だけに付くため、括弧で「`x == 7` 全体を反転する」と示します。なお同じ意味は `x != 7` でも書けます。

実行結果:

```text
true
true
false
1桁の正の数です
```

### 計算の順番

比較（`>` `==` など）が先、`&&` がその次、`||` が最後です。`a || b && c` は `a || (b && c)` と同じ意味になります。混ぜるときは括弧を付けると読み間違えません。

## ch03 slices.Contains（スライスの in の代わり）

Go に Python の `in` 演算子はありません。スライスに値が含まれるかは、標準ライブラリの `slices` パッケージにある `slices.Contains(スライス, 値)` で調べます。戻り値は bool なので、そのまま if の条件に使えます。使うには `import "slices"` が必要です。Go 1.21 より前はこの関数がなく、for で 1 件ずつ比較して探していました。🟡 「演算子ではなく関数で調べる」という Go の流儀を理解しましょう。

Python ではこう書いた:

```python
if "banana" in fruits:
    print("あります")
```

Go ではこう書く:

```go
if slices.Contains(fruits, "banana") {
	fmt.Println("あります")
}
```

### 引数と戻り値

- 第 1 引数 → 例: `fruits` ／ 意味: 探す先のスライス
- 第 2 引数 → 例: `"banana"` ／ 意味: 探したい値。スライスの要素と同じ型にします（`[]int` なら int）
- 戻り値 → 例: `true` / `false` ／ 意味: 1 つでも等しい要素があれば true

`slices` は L07 ch06 で使ったパッケージです。`import ( )` の中に `"slices"` を足します。

### サンプルの実行結果

- `slices.Contains(fruits, "banana")`: `true`
- `slices.Contains(fruits, "grape")`: `false`
- `if slices.Contains(nums, 20) {`: 戻り値が true なので中を実行し `20 が含まれています`

```text
true
false
20 が含まれています
```

「含まれていない」ときに何かしたい場合は、L11 ch02 の `!` を付けて `if !slices.Contains(nums, 50) {` と書きます。

## ch04 strings.Contains（文字列の in の代わり）

文字列に部分文字列が含まれるかを調べる Python の `"go" in s` は、Go では `strings.Contains(s, "go")` と書きます。前章の `slices.Contains` はスライス用、こちらは文字列用で、`in` の対象の型によって使う関数が変わります。`strings` パッケージには、先頭が一致するかを調べる `HasPrefix`、末尾を調べる `HasSuffix` もあります。🟡 「in の代わりは型ごとに関数を選ぶ」という考え方を理解しましょう。

Python ではこう書いた:

```python
if "go" in s:
    print("含まれます")
```

Go ではこう書く:

```go
if strings.Contains(s, "go") {
	fmt.Println("含まれます")
}
```

**部分文字列**とは、文字列の中のひと続きの部分のことです。`"golang is fun"` に対して `"lang"` や `"is f"` は部分文字列ですが、`"gun"` は離れた文字を拾っているので違います。

### 引数の順番に注意

`strings.Contains(s, "go")` は「s の中に "go" があるか」です。Python の `"go" in s` とは書く順番が逆で、**探される側が先**です。

### サンプルの実行結果（s は `"golang is fun"`）

- `strings.Contains(s, "go")` → 意味: "go" を含むか ／ 出力: `true`
- `strings.Contains(s, "python")` → 意味: "python" を含むか ／ 出力: `false`
- `strings.HasPrefix(s, "golang")` → 意味: "golang" で始まるか（Python の `s.startswith`） ／ 出力: `true`
- `strings.HasSuffix(s, "fun")` → 意味: "fun" で終わるか（Python の `s.endswith`） ／ 出力: `true`

大文字と小文字は区別されるので、`strings.Contains(s, "Go")` は false です。

```text
true
false
true
true
```
