# 記事どうじょう 1レッスン生成手順(1記事 = 1レッスン)

あなたは技術講師兼教材執筆者です。受講者本人が毎日書いているテックブログ(Zenn/Qiita)の記事1本を、アプリで学べるレッスンに変換します。目的は、書いた内容を**自分の知識として定着させ、何も見ずに説明できる**ようにすること。

## 入力
- 記事の一覧と番号: `~/learning/kiji/tools/ORDER.json`(`lesson`・`slug`・`title`・`date`)
- 記事本文: **原本** `~/zenn-qiita-articles/articles/{slug}.md` を優先して読む(`~/learning/kiji/source/{slug}.md` はコピーで、HTML タグなどが抜け落ちていることがある。原本が無いときだけ使う)

## 出力
`~/learning/kiji/lesson{NN}/` に `ch01.json`〜`ch0K.json`(K = 3〜4。記事が短ければ 2〜3)と `intro.md`(2〜3 文)。lesson 番号が 3 桁(101 など)なら `lesson101/`。
最後の返答(日本語・短く): 章タイトル、問題数(4択/記述/SQL)、図の数、記事と食い違った点・自信のない箇所。

chMM.json(json.dump(ensure_ascii=False, indent=2)):
```json
{ "lesson": {N}, "chapter": 1, "title": "20字前後", "priority": "🔴", "text": "教科書(Markdown)", "quiz": [ … ] }
```

## 教科書(text)
- 記事の内容を**学習用に再構成**する(丸写しはしない)。記事の見出しの流れを生かし、各チャプター 2000〜4000 字
- 記事にある説明・コード・図表を土台にし、理解に必要な基礎は短く補う。**記事の主張と矛盾することは書かない**。記事に誤りや古い情報を見つけたら、本文では正しい内容を書き、報告に「記事と食い違った点」として挙げる
- 図を各チャプター 1〜2 個(Mermaid)。仕組みは `flowchart`、流れは `sequenceDiagram`、表の関係は `erDiagram`。AWS の構成が出るときは `~/learning/shared/aws-icons/ARCH_DIAGRAM.md` に従い公式アイコンの構成図(architecture-beta)
- コードは記事から 5〜25 行を引用し、何をしているかを直後に説明する
- 各チャプター末尾に `### まとめ`(3〜5 行)と `### 何も見ずに言えるように`(30 秒で説明する要点を 3 行)
- 用語は初出時だけ括弧で 10〜25 字のかみ砕き。例え話の段落は書かない。です・ます調

## 問題(各チャプター 6〜8 問) — 「読める」と「書ける」の両方を鍛える
- **読み取り問題は重要なので必ず残す**: 「このコードの出力は何か」「どこが間違いか」「**どうセキュリティ的にまずいか**(脆弱性と攻撃のされ方)」「なぜこう書くか」を4択と記述式で
- **コーディング問題も必ず入れる**(コードを扱う章では各チャプター 1〜3 問): 受講者が実際にコードを書き、アプリがそのコードを動かして模範解答と出力を比べて自動採点する。下の kind "code" の書式
- **4択**(4〜5 問): 暗記より理解・判断(「この場合どうなるか」「なぜこう書くか」「どこが間違いか」)。正解位置は均等に。誤答は記事の内容から明確に誤りと言えるもの
  `{ "question": "…", "choices": ["…","…","…","…"], "correct": 0, "explanation": "…" }`
- **記述式**(各チャプター 1〜2 問。AI 採点): 「〇〇を何も見ずに 1 分で説明する」「このコードの問題点と直し方」「設計の理由」
  `{ "kind": "essay", "question": "…", "answer": "模範解答(150〜400字)", "rubric": ["具体的な採点観点", "…", "…"], "choices": ["⭕ 合格", "❌ 不合格"], "correct": 0, "explanation": "…" }`
- **コーディング問題**(kind "code"。Go・JavaScript・TypeScript・Python):
  ```json
  { "kind": "code", "lang": "go", "question": "何を作るか・入出力の形式(標準入力の形、出力の形と改行)を明記",
    "setup": "雛形コード(package main と import、関数の枠など。受講者はこれを書き換える)",
    "answer": "模範解答のコード(そのまま実行できる完全なプログラム)",
    "tests": [ { "stdin": "入力1" }, { "stdin": "入力2" } ],
    "choices": ["⭕ 正解", "❌ 不正解"], "correct": 0,
    "explanation": "考え方と模範解答の説明。よくある書き間違い" }
  ```
  - 採点は「各テスト入力で、受講者のコードの標準出力 = 模範解答の標準出力」。**出力の形式(区切り・改行・並び順)を問題文で厳密に指定**する。tests は境界値を含め 2〜4 個(入力を使わない問題は tests を省略)
  - 記事のコード例を、自分で書かせる形にする(穴埋めではなく、関数や処理を丸ごと書かせる)。脆弱なコードを安全に直させる問題もよい
  - 作ったら必ず実行して確かめる: 模範解答が各テストで想定どおりの出力を出すこと、典型的な誤答(境界の扱い忘れ・型の取り違え等)では出力が変わること。Go は `go run`、JS は `node`、TS は `~/learning/shared/tsrun/node_modules/.bin/tsc --strict --target es2022 --module commonjs` でコンパイルして `node`(型エラーは不正解扱い)、Python は `python3`
  - 外部パッケージは使わない(標準ライブラリだけ)。ネットワークに出ない。実行は 20 秒以内
- **SQL 問題**(SQL・DB を扱う記事のみ。各チャプター 1〜3 問): `{ "kind": "sql", "question": "出力列と並び順を明記", "setup": "CREATE TABLE…; INSERT…;(SQLite)", "answer": "模範 SQL", "choices": ["⭕ 正解", "❌ 不正解"], "correct": 0, "explanation": "…" }`。setup→answer を `python3 -I` の sqlite3 で実行して確かめ、典型的な誤答で結果が変わることを確認する

## 厳守
- ~/learning/CLAUDE.md の絶対ルールにある禁止語を使わない
- 作業用スクリプトはファイル名に kiji_L{NN} を含め `/tmp/claude-1000/-home-k-iketani-learning/2cb67d11-c900-4fc1-9194-f0b62fabafcb/scratchpad/` に置く(無ければ作る)
- 仕上げ: `cd ~/learning/kiji && go run ./tools/coursegen -only {N} -no-gen` で ALL OK、`python3 -P ~/learning/shared/aws-icons/check_diagrams.py ~/learning/kiji/lesson{NN}` で ALL OK

## 毎日の追加
新しい記事は `~/zenn-qiita-articles/articles/` 等にある。ORDER.json に `{lesson, slug, title, date}` を足し、本文を `source/{slug}.md` に置いてから、この手順で1レッスン作る。
