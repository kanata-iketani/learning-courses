// 記述式の AI 採点と、SQL 問題の実行・自動採点。
// - kind "essay": 受講者の記述を、模範解答と採点観点(rubric)に照らしてローカルの Claude が採点する
// - kind "sql":   受講者の SQL を SQLite(python3 の sqlite3)で実行し、模範 SQL の結果と比べて自動採点する
package main

import (
	"context"
	"os"
	"path/filepath"
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"os/exec"
	"regexp"
	"strings"
	"time"
)

// ---- SQL 実行(SQLite) ----

const sqlRunner = `
import sys, json, sqlite3
req = json.load(sys.stdin)
db = sqlite3.connect(":memory:")
out = {}
try:
    db.executescript(req.get("setup", ""))
    def run(sql):
        cur = db.cursor()
        stmts = [s for s in sqlite3_split(sql)]
        res = None
        for s in stmts:
            cur.execute(s)
            if cur.description:
                res = {"columns": [d[0] for d in cur.description], "rows": [list(r) for r in cur.fetchmany(201)]}
        return res or {"columns": [], "rows": [], "note": "結果を返さない SQL でした(SELECT で確認してください)"}
    def sqlite3_split(sql):
        # 「;」ごとに文の終わりかを確かめて切る(1行に複数の文があっても動く。文字列中の ; は切らない)
        buf = ""
        for ch in sql:
            buf += ch
            if ch == ";" and sqlite3.complete_statement(buf):
                if buf.strip(" \n\t;"): yield buf
                buf = ""
        if buf.strip(" \n\t;"): yield buf
    out["user"] = run(req["sql"])
    if req.get("model"):
        db2 = sqlite3.connect(":memory:"); db2.executescript(req.get("setup", ""))
        db, keep = db2, db
        out["model"] = run(req["model"])
except Exception as e:
    out["error"] = f"{type(e).__name__}: {e}"
print(json.dumps(out, ensure_ascii=False, default=str))
`

type sqlResult struct {
	Columns []string `json:"columns"`
	Rows    [][]any  `json:"rows"`
	Note    string   `json:"note,omitempty"`
}

type sqlRunOut struct {
	User  *sqlResult `json:"user"`
	Model *sqlResult `json:"model"`
	Error string     `json:"error"`
}

func runSQL(setup, userSQL, modelSQL string) (*sqlRunOut, error) {
	if _, err := exec.LookPath("python3"); err != nil {
		return nil, errors.New("SQL の実行には python3 が必要です")
	}
	ctx, cancel := context.WithTimeout(context.Background(), 8*time.Second)
	defer cancel()
	in, _ := json.Marshal(map[string]string{"setup": setup, "sql": userSQL, "model": modelSQL})
	cmd := exec.CommandContext(ctx, "python3", "-I", "-c", sqlRunner)
	cmd.Stdin = strings.NewReader(string(in))
	b, err := cmd.Output()
	if ctx.Err() == context.DeadlineExceeded {
		return nil, errors.New("SQL の実行が 8 秒を超えたので止めました(無限ループや巨大な結合がないか確認してください)")
	}
	if err != nil {
		return nil, fmt.Errorf("SQL 実行エンジンのエラー: %v", err)
	}
	var out sqlRunOut
	if err := json.Unmarshal(b, &out); err != nil {
		return nil, err
	}
	return &out, nil
}

var orderByRe = regexp.MustCompile(`(?i)\border\s+by\b`)

func normCell(v any) string {
	switch x := v.(type) {
	case nil:
		return "NULL"
	case float64:
		if x == float64(int64(x)) {
			return fmt.Sprintf("%d", int64(x))
		}
		return fmt.Sprintf("%.6g", x)
	default:
		return strings.TrimSpace(fmt.Sprint(x))
	}
}

// sameResult は結果の一致を判定する。模範 SQL に ORDER BY があれば行の順序も比べる。列名は問わない。
func sameResult(user, model *sqlResult, ordered bool) (bool, string) {
	if user == nil || model == nil {
		return false, "結果がありません"
	}
	if len(user.Columns) != len(model.Columns) {
		return false, fmt.Sprintf("列の数が違います(あなた: %d 列 / 期待: %d 列)", len(user.Columns), len(model.Columns))
	}
	if len(user.Rows) != len(model.Rows) {
		return false, fmt.Sprintf("行の数が違います(あなた: %d 行 / 期待: %d 行)", len(user.Rows), len(model.Rows))
	}
	key := func(r []any) string {
		p := make([]string, len(r))
		for i, c := range r {
			p[i] = normCell(c)
		}
		return strings.Join(p, "\x1f")
	}
	if ordered {
		for i := range user.Rows {
			if key(user.Rows[i]) != key(model.Rows[i]) {
				return false, fmt.Sprintf("%d 行目の内容か並び順が違います", i+1)
			}
		}
		return true, ""
	}
	cnt := map[string]int{}
	for _, r := range model.Rows {
		cnt[key(r)]++
	}
	for _, r := range user.Rows {
		k := key(r)
		if cnt[k] == 0 {
			return false, "期待した結果にない行が含まれています"
		}
		cnt[k]--
	}
	return true, ""
}

func loadQ(lesson, ch, q int) (*Chapter, *Question, error) {
	c, err := loadChapter(lesson, ch)
	if err != nil || q < 0 || q >= len(c.Quiz) {
		return nil, nil, errors.New("問題が見つかりません")
	}
	return c, &c.Quiz[q], nil
}

type gradeReq struct {
	Lesson  int    `json:"lesson"`
	Chapter int    `json:"chapter"`
	Q       int    `json:"q"`
	Draft   string `json:"draft"`
}

// handleSQLRun は「実行」ボタン: 受講者の SQL を実行して結果だけ返す(採点しない)。
func handleSQLRun(w http.ResponseWriter, r *http.Request) {
	var req gradeReq
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), 400)
		return
	}
	_, q, err := loadQ(req.Lesson, req.Chapter, req.Q)
	if err != nil {
		http.Error(w, err.Error(), 404)
		return
	}
	out, err := runSQL(q.Setup, req.Draft, "")
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}
	writeJSON(w, map[string]any{"result": out.User, "error": out.Error})
}

// handleGrade は「提出して採点」: SQL は結果比較、記述は Claude が採点。合否と講評を返す。
func handleGrade(w http.ResponseWriter, r *http.Request) {
	var req gradeReq
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), 400)
		return
	}
	c, q, err := loadQ(req.Lesson, req.Chapter, req.Q)
	if err != nil {
		http.Error(w, err.Error(), 404)
		return
	}
	if strings.TrimSpace(req.Draft) == "" {
		http.Error(w, "解答が空です", 400)
		return
	}
	switch q.Kind {
	case "code":
		writeJSON(w, gradeCode(q, req.Draft))
	case "sql":
		out, err := runSQL(q.Setup, req.Draft, q.Answer)
		if err != nil {
			http.Error(w, err.Error(), 500)
			return
		}
		if out.Error != "" {
			writeJSON(w, map[string]any{"pass": false, "score": 0, "feedback": "SQL がエラーになりました: " + out.Error, "result": out.User})
			return
		}
		ok, why := sameResult(out.User, out.Model, orderByRe.MatchString(q.Answer))
		fb := "期待どおりの結果が得られました。"
		if !ok {
			fb = why + "。条件(WHERE)・結合・集計(GROUP BY)・並び順を見直してください。"
		}
		score := 0
		if ok {
			score = 100
		}
		writeJSON(w, map[string]any{"pass": ok, "score": score, "feedback": fb, "result": out.User, "expected": out.Model})
	default: // essay
		res, err := gradeEssay(c, q, req.Draft)
		if err != nil {
			http.Error(w, err.Error(), 502)
			return
		}
		writeJSON(w, res)
	}
}

type essayResult struct {
	Score    int    `json:"score"`
	Pass     bool   `json:"pass"`
	Good     string `json:"good"`
	Missing  string `json:"missing"`
	Advice   string `json:"advice"`
	Feedback string `json:"feedback"`
}

var jsonObjRe = regexp.MustCompile(`(?s)\{.*\}`)

func gradeEssay(c *Chapter, q *Question, draft string) (*essayResult, error) {
	var b strings.Builder
	b.WriteString("あなたは" + qaCourseDesc + "採点者です。受講者の記述式解答を採点します。\n\n")
	fmt.Fprintf(&b, "【教科書(参考)】\n%s\n\n【問題】\n%s\n\n【模範解答】\n%s\n\n", truncate(c.Text, 6000), q.Question, q.Answer)
	if len(q.Rubric) > 0 {
		b.WriteString("【採点観点(各観点を満たすかで判定)】\n")
		for i, r := range q.Rubric {
			fmt.Fprintf(&b, "%d. %s\n", i+1, r)
		}
		b.WriteString("\n")
	}
	fmt.Fprintf(&b, "【受講者の解答】\n%s\n\n", draft)
	b.WriteString(`採点ルール:
- 模範解答と言い回しが違っても、採点観点の趣旨を満たしていれば認める。満たしていない観点ははっきり指摘する
- 事実の誤り・設計上の危険(データ不整合、セキュリティ、性能の破綻など)は減点し、理由を書く
- score は 0〜100。70 以上を合格(pass=true)とする
- good / missing / advice は、です・ます調の日本語で各 1〜4 文。missing には足りない観点を具体的に書く
- 出力は次の JSON のみ(前後に文章を書かない):
{"score": 0, "pass": false, "good": "", "missing": "", "advice": ""}`)
	out, err := runClaude("grade", b.String(), 240*time.Second)
	if err != nil {
		return nil, err
	}
	m := jsonObjRe.FindString(out)
	var res essayResult
	if m == "" || json.Unmarshal([]byte(m), &res) != nil {
		return &essayResult{Score: 0, Pass: false, Feedback: out}, nil
	}
	if res.Score >= 70 {
		res.Pass = true
	}
	return &res, nil
}

func truncate(s string, n int) string {
	r := []rune(s)
	if len(r) <= n {
		return s
	}
	return string(r[:n]) + "…(以下略)"
}

// ---- コーディング問題(kind "code"): 書いたコードを実際に動かし、模範解答と出力を比べる ----

type codeTest struct {
	Stdin string `json:"stdin"`
}

func runCode(lang, code, stdin string) (stdout, stderr string, err error) {
	dir, e := os.MkdirTemp("", "coderun-")
	if e != nil {
		return "", "", e
	}
	defer os.RemoveAll(dir)
	ctx, cancel := context.WithTimeout(context.Background(), 20*time.Second)
	defer cancel()
	var cmd *exec.Cmd
	switch lang {
	case "go":
		os.WriteFile(filepath.Join(dir, "main.go"), []byte(code), 0o644)
		cmd = exec.CommandContext(ctx, "go", "run", "main.go")
	case "js":
		os.WriteFile(filepath.Join(dir, "main.js"), []byte(code), 0o644)
		cmd = exec.CommandContext(ctx, "node", "main.js")
	case "ts":
		os.WriteFile(filepath.Join(dir, "main.ts"), []byte(code), 0o644)
		tsc := filepath.Join(os.Getenv("HOME"), "learning", "shared", "tsrun", "node_modules", ".bin", "tsc")
		c := exec.CommandContext(ctx, tsc, "--strict", "--target", "es2022", "--module", "commonjs", "--outDir", dir, filepath.Join(dir, "main.ts"))
		var eb strings.Builder
		c.Stdout, c.Stderr = &eb, &eb
		if c.Run() != nil {
			return "", "型チェック(tsc)のエラー:\n" + eb.String(), nil
		}
		cmd = exec.CommandContext(ctx, "node", filepath.Join(dir, "main.js"))
	case "python":
		os.WriteFile(filepath.Join(dir, "main.py"), []byte(code), 0o644)
		cmd = exec.CommandContext(ctx, "python3", "-I", "main.py")
	default:
		return "", "", fmt.Errorf("未対応の言語です: %s", lang)
	}
	cmd.Dir = dir
	cmd.Stdin = strings.NewReader(stdin)
	var ob, eb strings.Builder
	cmd.Stdout, cmd.Stderr = &ob, &eb
	runErr := cmd.Run()
	if ctx.Err() == context.DeadlineExceeded {
		return ob.String(), eb.String(), errors.New("20秒を超えたので止めました(無限ループがないか確認してください)")
	}
	if runErr != nil && eb.Len() == 0 {
		eb.WriteString(runErr.Error())
	}
	return ob.String(), eb.String(), nil
}

func normOut(s string) string {
	lines := strings.Split(strings.ReplaceAll(s, "\r\n", "\n"), "\n")
	for i, l := range lines {
		lines[i] = strings.TrimRight(l, " \t")
	}
	return strings.TrimRight(strings.Join(lines, "\n"), "\n")
}

// handleCodeRun は「▶ 実行」: 書いたコードを動かして出力だけ返す(採点しない)。
func handleCodeRun(w http.ResponseWriter, r *http.Request) {
	var req struct {
		Lesson  int    `json:"lesson"`
		Chapter int    `json:"chapter"`
		Q       int    `json:"q"`
		Draft   string `json:"draft"`
		Stdin   string `json:"stdin"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), 400)
		return
	}
	_, q, err := loadQ(req.Lesson, req.Chapter, req.Q)
	if err != nil {
		http.Error(w, err.Error(), 404)
		return
	}
	out, errOut, e := runCode(q.Lang, req.Draft, req.Stdin)
	if e != nil {
		errOut = e.Error() + "\n" + errOut
	}
	writeJSON(w, map[string]string{"stdout": out, "stderr": errOut})
}

// gradeCode は各テスト入力で受講者のコードと模範解答を動かし、標準出力が一致するかで判定する。
func gradeCode(q *Question, draft string) map[string]any {
	tests := q.Tests
	if len(tests) == 0 {
		tests = []codeTest{{Stdin: ""}}
	}
	type res struct {
		Stdin    string `json:"stdin"`
		Got      string `json:"got"`
		Expected string `json:"expected"`
		Stderr   string `json:"stderr,omitempty"`
		OK       bool   `json:"ok"`
	}
	var rs []res
	pass := true
	for _, t := range tests {
		exp, _, e1 := runCode(q.Lang, q.Answer, t.Stdin)
		got, gerr, e2 := runCode(q.Lang, draft, t.Stdin)
		if e1 != nil {
			return map[string]any{"pass": false, "score": 0, "feedback": "模範解答の実行に失敗しました: " + e1.Error()}
		}
		if e2 != nil {
			gerr = e2.Error() + "\n" + gerr
		}
		ok := normOut(got) == normOut(exp)
		pass = pass && ok
		rs = append(rs, res{Stdin: t.Stdin, Got: got, Expected: exp, Stderr: gerr, OK: ok})
	}
	n := 0
	for _, x := range rs {
		if x.OK {
			n++
		}
	}
	fb := fmt.Sprintf("テスト %d / %d 件で出力が一致しました。", n, len(rs))
	score := 100 * n / len(rs)
	return map[string]any{"pass": pass, "score": score, "feedback": fb, "tests": rs}
}
