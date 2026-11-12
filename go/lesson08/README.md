# Lesson 08 スライスと文字列

Python入門編「リストと文字列」に対応するレッスンです。`join` `split` に当たるのは `strings.Join` / `strings.Split` / `strings.Fields` で、使い方は Python とほぼ同じです。

## ch01 strings.Join（スライス→文字列）

スライスを 1 本の文字列にまとめるには `strings.Join(s, 区切り)` を使います。Python の `",".join(a)` とほぼ同じ機能です。違いは書き方の向きだけで、Python は区切り文字側のメソッドでしたが、Go はスライスを第 1 引数に取る関数です。区切りに `""` を渡せばそのまま連結になります。🔴 出力の整形で毎回使うので、手が覚えるまで書きましょう。

Python ではこう書いた:

```python
print(",".join(a))
```

Go ではこう書く:

```go
fmt.Println(strings.Join(s, ","))
```

### 引数と戻り値

`strings.Join(week, ",")` の場合:

- 第 1 引数 → 値: `week`（`[]string{"月", "火", "水"}`） ／ 意味: つなげたい文字列のスライス。**`[]string` しか渡せません**（`[]int` はエラー）
- 第 2 引数 → 値: `","` ／ 意味: 要素と要素の間に入れる文字列
- 戻り値 → 値: `"月,火,水"` ／ 意味: できあがった 1 本の文字列

区切りは要素の「間」にだけ入り、先頭と末尾には付きません。

### サンプルの実行結果

- `strings.Join(week, ",")`: `月,火,水`
- `strings.Join(week, " と ")`: `月 と 火 と 水`
- `strings.Join(week, "")`: `月火水`

```text
月,火,水
月 と 火 と 水
月火水
```

`fmt.Println(week)` だと `[月 火 水]` と `[ ]` 付きで表示されます（L07 ch01）。`[ ]` なしの好きな形で出したいときに Join を使います。

## ch02 strings.Split（文字列→スライス）

文字列を区切り文字で分割してスライスにするには `strings.Split(s, 区切り)` を使います。Python の `"a,b,c".split(",")` とほぼ同じで、結果は `[]string` になります。Join と Split は互いに逆の操作で、この 2 つでカンマ区切りデータの読み書きができます。分割した結果はスライスなので `s[i]` や `len` がそのまま使えます。🔴 データ処理の基本なので、手が覚えるまで書きましょう。

Python ではこう書いた:

```python
colors = "赤,青,黄".split(",")
```

Go ではこう書く:

```go
colors := strings.Split("赤,青,黄", ",")
```

### 分割の様子

`strings.Split("赤,青,黄", ",")` は、`,` の位置で文字列を切り、`,` 自体は捨てて、残った部分を順にスライスに入れます。

- `"赤,青,黄"` → 区切り: `","` ／ 結果: `[赤 青 黄]` ／ 要素数: 3
- `"apple:banana:cherry"` → 区切り: `":"` ／ 結果: `[apple banana cherry]` ／ 要素数: 3
- `"a,,b"` → 区切り: `","` ／ 結果: `["a" "" "b"]`（間に空文字列） ／ 要素数: 3

サンプルの変数名 `csv` は、カンマ区切りのデータ形式 CSV（Comma-Separated Values）にちなんだ名前です。

### サンプルの実行結果

- `fmt.Println(colors)`: `[赤 青 黄]`
- `fmt.Println(len(colors))`: `3`
- `fmt.Println(colors[1])`: `青`（0 から数えて 1 番目）

```text
[赤 青 黄]
3
青
```

## ch03 strings.Fields（空白区切りの分割）

空白区切りの文字列を分割するには `strings.Fields(s)` を使います。Python で引数なしの `split()` を呼んだときとほぼ同じで、連続する空白やタブをまとめて 1 つの区切りとして扱います。`strings.Split(s, " ")` だと連続空白のあいだに空文字列の要素が入ってしまうため、空白区切りには Fields を選ぶのが定石です。🔴 のちの標準入力の読み取りで必ず使うので、手が覚えるまで書きましょう。

Python ではこう書いた:

```python
words = "go  is   fun".split()
```

Go ではこう書く:

```go
words := strings.Fields("go  is   fun")
```

### Fields と Split の違いを実物で見る

`line := "go  is   fun"`（go と is の間に空白 2 つ、is と fun の間に空白 3 つ）のとき:

- `strings.Fields(line)` → 結果（空文字列を `""` で表示）: `["go" "is" "fun"]` ／ 要素数: 3
- `strings.Split(line, " ")` → 結果（空文字列を `""` で表示）: `["go" "" "is" "" "" "fun"]` ／ 要素数: 6

Split は空白 1 つごとに切るので、空白と空白の間にある「何もない部分」も空文字列の要素として残ります。Fields は空白の連続をまとめて 1 つの区切りと見なし、空の要素を作りません。**タブ**（Tab キーで入る空白文字）や改行も区切りとして扱います。

### サンプルの実行結果

```text
[go is fun]
3
6
```

3 行目の `6` は Split で分けたときの要素数です。Println でスライスを表示すると空文字列は目に見えないため、要素数で違いを確かめています。
