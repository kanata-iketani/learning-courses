# Lesson 17 集合の代替

Python入門編「集合」に対応するレッスンです。Go に set 型は存在せず、`map[T]bool`（または `map[T]struct{}`）で代用します。和・積・差などの集合演算子もないため、for を使って自分で書きます。

## ch01 Go に set 型は存在しない（map で代用する）

Go に set 型は存在しません。Python の**集合**（重複しない要素の集まり）に相当する処理は、map で代用します。定番は map[T]bool（T は「何かの型」を表す書き方で、実際には map[string]bool などになります）で、要素をキーに、値に true を入れます。メモリを節約したいときは値を空の構造体（フィールドを 1 つも持たない構造体。L9 で見た構造体の中身が空のもの）にする map[T]struct{} という書き方もありますが、まずは読み書きが素直な map[T]bool で十分です。所属判定は set[x] と引くだけで、ないキーはゼロ値 false になるため、そのまま if の条件に使えます。🟡 「set は map で作る」と理屈で押さえましょう。

Python ではこう書いた:

```python
s = {"apple", "banana"}
print("apple" in s)
```

Go ではこう書く:

```go
set := map[string]bool{"apple": true, "banana": true}
fmt.Println(set["apple"])
```

### サンプルを1行ずつ読む

- `set := map[string]bool{"apple": true, "banana": true, "orange": true}` … 集合に入れたい要素をキーにし、値はすべて `true` にします
- `fmt.Println(set["apple"])` … キーがあるので `true`
- `fmt.Println(set["grape"])` … キーがないので bool のゼロ値 `false`（L16 ch03）。だから `if set[x] {` だけで「含まれるか」を判定できます
- `set2 := map[string]struct{}{"apple": {}}` … 値の型が `struct{}`（空の構造体）。`{}` がその値です。中身がないのでメモリをほとんど使いません。記号が多く見えますが、`map[string]struct{}` までが型、その後ろの `{...}` が中身です
- `_, ok := set2["apple"]` … 空構造体には true/false がないので、L16 ch03 のカンマ ok で「キーがあるか」を調べます

### 実行結果

```text
true
false
true
```

要素を足すときは `set["grape"] = true`、取り除くときは `delete(set, "grape")`（L16）です。

## ch02 存在判定と重複除去

set 代わりの map が最も活躍するのが存在判定と重複除去です。「すでに見たか」を seen という名前の map[T]bool に記録しながらスライスを走査し、初めて見た要素だけを結果に append します。set 型がない Go ではこれが重複除去の定石で、Python の set(lst) と違って**元の順序を保ったまま**取り除けるという利点もあります。コーディングテストでも実務でも頻出のパターンです。🔴 seen マップを使う形を手が覚えるまで書きましょう。

Python ではこう書いた:

```python
unique = list(dict.fromkeys(words))  # 順序を保つ重複除去
```

Go ではこう書く:

```go
seen := map[string]bool{}
unique := []string{}
for _, w := range words {
	if !seen[w] {
		seen[w] = true
		unique = append(unique, w)
	}
}
```

### サンプルを1行ずつ読む

`words` は `[go python go ruby python]` です。

| w | seen[w]（判定前） | !seen[w] | 何をするか | unique |
|---|---|---|---|---|
| go | false | true | 記録して追加 | [go] |
| python | false | true | 記録して追加 | [go python] |
| go | true | false | 何もしない | [go python] |
| ruby | false | true | 記録して追加 | [go python ruby] |
| python | true | false | 何もしない | [go python ruby] |

- `seen := map[string]bool{}` … `{}` で空の map を作ります。`make(map[string]bool)` と同じです（L16）
- `if !seen[w] {` … 未登録のキーは false なので、`!`（not）で反転すると「まだ見ていない」ときに true になります
- `seen[w] = true` … 見たことを記録します
- `unique = append(unique, w)` … 初めての単語だけ結果に足します

### 実行結果

```text
[go python ruby]
```

演習では出力を `[ ]` なしの空白区切りにするので、`strings.Join(unique, " ")`（L8）で 1 つの文字列にしてから出力します。

## ch03 和・積・差は自分で書く

Python の集合演算子 `|`（和: どちらかにある要素すべて）`&`（積: 両方にある要素）`-`（差: 左にだけある要素）は Go にはないため、set 型がない Go では for で自分で書きます。発想は 1 つで、「一方を map にしておき、もう一方を走査して、含まれるかどうかで振り分ける」だけです。積は「A の要素のうち B にあるもの」、差は「A の要素のうち B にないもの」、和は「A と B を両方登録した map のキー」になります。出力の順序が必要なら、前レッスン（L16 ch06）の定石どおりソートします。🟡 演算子がなくても for で書ける、と理屈で理解しましょう。

Python ではこう書いた:

```python
inter = a & b
diff = a - b
```

Go ではこう書く:

```go
inter := []string{}
for _, w := range a {
	if setB[w] { // B にもあれば積
		inter = append(inter, w)
	}
}
```

### 具体例

A = {apple, banana, orange}、B = {banana, grape} のとき:

| 演算 | 意味 | 結果 |
|---|---|---|
| 和 | A か B にある | apple, banana, grape, orange |
| 積 | A にも B にもある | banana |
| 差 A−B | A にあって B にない | apple, orange |

### サンプルを1行ずつ読む

- `setB := map[string]bool{"banana": true, "grape": true}` … B を set 代わりの map にしておきます
- `for _, w := range a {` … A を 1 つずつ見ます
- `if setB[w] { inter = append(inter, w) } else { diff = append(diff, w) }` … B にあれば積へ、なければ差へ振り分けます

| w | setB[w] | 入る先 |
|---|---|---|
| apple | false | diff |
| banana | true | inter |
| orange | false | diff |

- `slices.Sort(inter)` / `slices.Sort(diff)` … 辞書順に並べます

### 実行結果

```text
積: [banana]
差: [apple orange]
```

和を作るときは、A と B の要素を全部 `union[w] = true` で 1 つの map に登録し、L16 ch06 の方法でキーを集めてソートします。演習では B の行を読んで `setB` を作るところから自分で書きます。
