# Lesson 16 マップ

Python入門編「辞書」に対応するレッスンです。Go では `map[キーの型]値の型` を使います。最大の差は **range で取り出す順序が保証されない** ことで、順序が必要な出力はキーをソートしてから行います。辞書内包表記も存在しません。

## ch01 map リテラルと取得

Python の辞書に相当するのが **map**（キーと値の組を保持するデータ構造）です。map[string]int のようにキーと値の型を指定し、リテラルは map[string]int{"apple": 120} の形で書きます。取得は Python と同じ m[key] です。ただし Python と 2 つ大きな差があります。要素の順序が保証されないこと（後のチャプターで扱います）と、辞書内包表記が存在しないことです。🔴 リテラルの書き方と取得を手が覚えるまで書きましょう。

Python ではこう書いた:

```python
prices = {"apple": 120, "banana": 90}
print(prices["apple"])
```

Go ではこう書く:

```go
prices := map[string]int{"apple": 120, "banana": 90}
fmt.Println(prices["apple"])
```

### `map[string]int` の読み方

`map[キーの型]値の型` です。`map[string]int` は「キーが文字列、値が整数」の map です。Python の辞書はキーにも値にも何でも入れられましたが、Go の map は決めた型以外を入れるとコンパイルエラーになります。

| 書き方 | キーの型 | 値の型 | 例 |
|---|---|---|---|
| `map[string]int` | string | int | `{"apple": 120}` |
| `map[string]string` | string | string | `{"jp": "日本"}` |
| `map[int]bool` | int | bool | `{3: true}` |

### サンプルを1行ずつ読む

- `prices := map[string]int{ ... }` … キー `"apple"` に 120、`"banana"` に 90、`"orange"` に 60 を入れた map を作ります。`キー: 値,` の形で並べます。複数行で書くときは最後の行 `"orange": 60,` の後ろにもカンマが必要です（ないとコンパイルエラー）
- `fmt.Println(prices["apple"])` … キー `"apple"` の値 120 を取り出して出力します
- `fmt.Println(prices["apple"] + prices["banana"])` … 120 + 90 = 210

### 実行結果

```text
120
60
210
```

ない果物名（例: `"grape"`）を引くとどうなるかは ch03 で扱います（エラーにはならず 0 が返ります）。

## ch02 make と追加・更新

空の map は make（スライスや map を作る組み込み関数）で作ります。var m map[string]int と宣言しただけの map は **nil map**（実体を持たない map）で、書き込むと実行時エラー（コンパイルは通るが、実行中にプログラムが止まるエラー。Go ではこれを panic と呼びます）になるため、あとから追加していく map は必ず make で作るのが鉄則です。追加と更新はどちらも m[key] = value で、キーがなければ追加、あれば上書きになります。この書き味は Python の d[key] = value と同じです。🔴 「make で作ってから書き込む」流れを手が覚えるまで書きましょう。

Python ではこう書いた:

```python
d = {}
d["apple"] = 100
d["apple"] = 120  # 上書き
```

Go ではこう書く:

```go
m := make(map[string]int)
m["apple"] = 100
m["apple"] = 120 // 上書き
```

### nil map に書き込むとどうなるか

```go
var m map[string]int // make していない = nil map
m["a"] = 1           // ここで止まる
```

実行すると次のように表示されて止まります。

```text
panic: assignment to entry in nil map
```

`nil` は「まだ何も指していない」ことを表す Go の値です（Python の `None` に近いもの）。読むだけ（`m["a"]`）ならエラーにならず 0 が返りますが、書き込みはできません。`m := make(map[string]int)` か `m := map[string]int{}` で作れば書き込めます。

### サンプルを1行ずつ読む

| 行 | stock の中身 |
|---|---|
| `stock := make(map[string]int)` | `{}`（空） |
| `stock["pen"] = 10` | `{pen: 10}`（追加） |
| `stock["note"] = 5` | `{pen: 10, note: 5}`（追加） |
| `stock["pen"] = 8` | `{pen: 8, note: 5}`（上書き） |

- `fmt.Println(len(stock))` … `len` は map の要素数（キーの数）も返します。pen と note の 2 つです

### 実行結果

```text
8
5
2
```

## ch03 カンマ ok イディオム v, ok := m[k]

Go の map は、存在しないキーを読んでもエラーにならず、値の型の**ゼロ値**（L4 で見た、値を入れていない変数の初期値。int なら 0、string なら空文字列、bool なら false）を返します。そのため「値が 0」と「キーがない」を区別できません。区別するには v, ok := m[k] という**カンマ ok イディオム**を使います。ok はキーが存在すれば true になる bool です。Python の in 演算子や get() で行っていた存在チェックは、Go ではすべてこの形で書きます。🔴 手が覚えるまで書きましょう。

Python ではこう書いた:

```python
if "apple" in prices:
    print(prices["apple"])
```

Go ではこう書く:

```go
if v, ok := prices["apple"]; ok {
	fmt.Println(v)
}
```

### `if v, ok := prices["apple"]; ok {` の読み方

L10 で見た「条件の前の 1 文」の形です。セミコロン `;` の前と後ろで 2 つに分かれます。

1. `v, ok := prices["apple"]` … map を引くと、値と「キーがあったか（bool）」の 2 つが返ります。それを `v` と `ok` に入れます
2. `; ok` … `ok` が true のときだけ `{}` の中を実行します

| 引いたキー | v | ok |
|---|---|---|
| `"coffee"`（ある） | 480 | true |
| `"juice"`（ない） | 0（ゼロ値） | false |

`v` と `ok` はこの if の中でだけ使えます（L19 で扱うスコープ）。名前 `ok` は慣習で、別の名前でも動きます。

### サンプルを1行ずつ読む

- `fmt.Println(prices["juice"])` … ないキーなので 0 が出ます。Python なら KeyError になる所です
- `if v, ok := prices["coffee"]; ok {` … coffee はあるので ok は true、`v` は 480
- `if _, ok := prices["juice"]; !ok {` … 値は使わないので `_` で捨てます（L13）。`!ok` は「ok ではない」（L11 の `!` = not）。juice はないので `!ok` が true になり、中が実行されます

### 実行結果

```text
0
coffee は 480 円
juice はメニューにありません
```

## ch04 delete と len

map の要素の削除は delete(m, key)、要素数は len(m) で調べます。Python の del d[key] は存在しないキーを指定すると KeyError になりましたが、Go の delete は存在しないキーを渡しても何も起きず、エラーになりません。この仕様のおかげで、削除前の存在チェックは不要です。len はスライスと同じ感覚で使えます。🟡 「delete は失敗しない」という Python との差を理屈で押さえましょう。

Python ではこう書いた:

```python
del prices["apple"]  # キーがないと KeyError
print(len(prices))
```

Go ではこう書く:

```go
delete(prices, "apple") // キーがなくても何も起きない
fmt.Println(len(prices))
```

### サンプルを1行ずつ読む

| 行 | stock の中身 | len(stock) |
|---|---|---|
| `stock := map[string]int{"pen": 120, "note": 180, "clip": 50}` | pen, note, clip | 3 |
| `delete(stock, "note")` | pen, clip | 2 |
| `delete(stock, "eraser")` | pen, clip（変化なし。エラーも出ない） | 2 |

`delete` は戻り値を返しません。消せたかどうかを知りたいときは、消す前に ch03 のカンマ ok で確かめます。

### 実行結果

```text
3
2
2
```

## ch05 range で全要素（順序は保証されない）

map の全要素は for k, v := range m で取り出せます。ここで最重要の注意点があります。**Go の map は range で取り出す順序が保証されません**。同じプログラムを 2 回動かすと違う順序で出ることさえあります。挿入順を保つ Python 3.7 以降の辞書との明確な差です。そのため range は合計や件数など順序に依存しない集計にだけ使い、順序が問われる出力には使ってはいけません（対処は次チャプター）。🟡 この制約を理屈で理解しましょう。

Python ではこう書いた:

```python
for k, v in d.items():
    print(k, v)  # 挿入順に出る
```

Go ではこう書く:

```go
for k, v := range m {
	fmt.Println(k, v) // 順序は毎回変わりうる
}
```

### `for k, v := range m` の読み方

スライスの `range`（L13）は「位置番号と値」でしたが、map の `range` は「**キーと値**」を返します。

| 書き方 | 受け取るもの |
|---|---|
| `for k, v := range m` | キーと値 |
| `for _, v := range m` | 値だけ |
| `for k := range m` | キーだけ |

### 順序が変わる実例

`scores` の中身を `for k, v := range scores { fmt.Println(k, v) }` で出力すると、実行のたびに次のように順番が変わることがあります。

```text
suzuki 90
tanaka 70
sato 80
```

```text
sato 80
suzuki 90
tanaka 70
```

Go は「map の順序に頼ったプログラム」を作らせないよう、わざと取り出す順序を毎回ばらつかせています。

### サンプルを1行ずつ読む

- `for _, v := range scores {` … キーは使わないので `_` で捨て、点数だけを `v` に受けます
- `sum += v` … 点数を足します。80+90+70 はどの順に足しても 240 です
- `count++` … 1 人ごとに 1 増やします（L12）

### 実行結果

```text
人数: 3
合計: 240
```

## ch06 キーを集めてソートして出力（順序が必要なときの定石）

順序を揃えて map を出力したいときの定石は「キーをスライスに集めてソートし、その順に map を引く」です。make([]string, 0, len(m)) で空スライスを用意し（下で説明します）、range でキーだけを append、slices.Sort で並べ替えてから for で出力します。順序が保証されない Go の map では、Python の sorted(d) に相当するこの処理を自分で書きます。コーディングテストで map の中身を出力する問題は、ほぼ必ずこの形になります。🔴 手が覚えるまで書きましょう。

Python ではこう書いた:

```python
for k in sorted(d):
    print(k, d[k])
```

Go ではこう書く:

```go
keys := make([]string, 0, len(m))
for k := range m {
	keys = append(keys, k)
}
slices.Sort(keys)
for _, k := range keys {
	fmt.Println(k, m[k])
}
```

### `make([]string, 0, len(m))` とは

`make(スライスの型, 長さ, 容量)` です。

- 長さ 0 … 中身は空。`len(keys)` は 0 なので、そのまま `append` で先頭から足していけます
- 容量 `len(m)` … 「あとで最大この個数まで入れる」という予約です。足すたびに置き場所を広げ直す手間が減ります

`keys := []string{}` と書いても結果は同じです。容量の指定は速さのためのもので、なくても正しく動きます。`make([]string, len(m))` と長さのほうに数を入れると、最初から空文字列が `len(m)` 個入った状態になり、`append` はその後ろに足されてしまうので注意しましょう。

### サンプルを1行ずつ読む

| 行 | 結果 |
|---|---|
| `for k := range scores { keys = append(keys, k) }` | `keys` にキー 3 つが入る（順序はばらばら。例: `[tanaka sato suzuki]`） |
| `slices.Sort(keys)` | 辞書順（アルファベット順）に並べ替え。`[sato suzuki tanaka]`（L7） |
| `for _, k := range keys { fmt.Println(k, scores[k]) }` | 並んだキーの順に map を引いて出力 |

`slices.Sort` を使うには `import` に `"slices"` を足します。

### 実行結果

何回実行しても同じ順になります。

```text
sato 80
suzuki 90
tanaka 70
```
