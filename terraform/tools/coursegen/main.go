// coursegen は lessonNN/chMM.json（教材の正）を検証し、
// README.md / サンプル / 演習 / 解答ファイルを生成する（Terraform入門・terraform 実行版）。
//
// 使い方:
//
//	go run ./tools/coursegen              # 全レッスンを検証 + 生成
//	go run ./tools/coursegen -only 6-9    # lesson06〜09 のみ
//	go run ./tools/coursegen -no-gen      # 検証だけ行う
package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"sync"
	"time"
)

const (
	srcFileName = "main.tf" // 実行時のファイル名
	langExt     = ".tf"     // 生成するサンプル/解答の拡張子
	fileMarker  = "# === file: "
)

// runnerCmd は terraform init → apply → output を実行するコマンドを返す。
func runnerCmd(ctx context.Context, dir string) *exec.Cmd {
	script := "terraform init -backend=false -input=false -no-color >/dev/null && " +
		"terraform apply -auto-approve -input=false -no-color >/dev/null && " +
		"terraform output -no-color"
	cmd := exec.CommandContext(ctx, "bash", "-c", script)
	cmd.Dir = dir
	cmd.Env = append(os.Environ(), "CHECKPOINT_DISABLE=1", "TF_IN_AUTOMATION=1")
	return cmd
}

// writeSourceTree はコードを main.tf (または「# === file: path ===」区切りの複数ファイル) として書き出す。
func writeSourceTree(dir, code string) error {
	if !strings.Contains(code, fileMarker) {
		return os.WriteFile(filepath.Join(dir, srcFileName), []byte(code), 0o644)
	}
	current := srcFileName
	files := map[string][]string{}
	for _, line := range strings.Split(code, "\n") {
		trimmed := strings.TrimSpace(line)
		if strings.HasPrefix(trimmed, fileMarker) {
			name := strings.TrimSpace(strings.TrimSuffix(strings.TrimPrefix(trimmed, fileMarker), "==="))
			name = filepath.Clean(name)
			if name == "" || strings.HasPrefix(name, "..") || filepath.IsAbs(name) {
				continue
			}
			current = name
			continue
		}
		files[current] = append(files[current], line)
	}
	for name, lines := range files {
		path := filepath.Join(dir, name)
		if err := os.MkdirAll(filepath.Dir(path), 0o755); err != nil {
			return err
		}
		if err := os.WriteFile(path, []byte(strings.Join(lines, "\n")), 0o644); err != nil {
			return err
		}
	}
	return nil
}

type Test struct {
	Stdin    string `json:"stdin"`
	Expected string `json:"expected_stdout"`
}

type Exercise struct {
	Description string `json:"description"`
	Starter     string `json:"starter"`
	Stdin       string `json:"stdin,omitempty"`
	Expected    string `json:"expected_stdout,omitempty"`
	Answer      string `json:"answer"`
	Tests       []Test `json:"tests,omitempty"`
}

type Chapter struct {
	Lesson   int      `json:"lesson"`
	Chapter  int      `json:"chapter"`
	Kind     string   `json:"kind,omitempty"` // "program"(既定) or "web"
	Title    string   `json:"title"`
	Priority string   `json:"priority"`
	Text     string   `json:"text"`
	Sample   string   `json:"sample"`
	Exercise Exercise `json:"exercise"`
}

func (c *Chapter) tests() []Test {
	if len(c.Exercise.Tests) > 0 {
		return c.Exercise.Tests
	}
	return []Test{{Stdin: c.Exercise.Stdin, Expected: c.Exercise.Expected}}
}

type courseLesson struct {
	Lesson int    `json:"lesson"`
	Title  string `json:"title"`
}

var (
	root   = flag.String("root", ".", "講座ルート")
	only   = flag.String("only", "", "対象レッスン番号（例: 6-9 や 1,3,5）。空なら全部")
	noGen  = flag.Bool("no-gen", false, "検証のみ行い、ファイル生成をしない")
	noFix  = flag.Bool("no-fix", false, "gofmt 差分があっても JSON を書き換えない")
	failed bool
)

func main() {
	flag.Parse()
	targets := parseOnly(*only)

	titles := map[int]string{}
	if b, err := os.ReadFile(filepath.Join(*root, "course.json")); err == nil {
		var cl []courseLesson
		json.Unmarshal(b, &cl)
		for _, c := range cl {
			titles[c.Lesson] = c.Title
		}
	}

	type result struct {
		lesson, chapter int
		pass            bool
		errs            []string
	}
	var (
		mu      sync.Mutex
		results []result
		wg      sync.WaitGroup
		sem     = make(chan struct{}, 8)
	)

	chapters := map[int][]*Chapter{}
	// lesson90 以降はアプリが自動生成する復習レッスンなので対象外
	for n := 1; n <= 89; n++ {
		if targets != nil && !targets[n] {
			continue
		}
		dir := filepath.Join(*root, fmt.Sprintf("lesson%02d", n))
		entries, err := os.ReadDir(dir)
		if err != nil {
			continue
		}
		re := regexp.MustCompile(`^ch(\d{2})\.json$`)
		for _, e := range entries {
			m := re.FindStringSubmatch(e.Name())
			if m == nil {
				continue
			}
			path := filepath.Join(dir, e.Name())
			ch, errs := loadAndFix(path)
			if ch != nil {
				chapters[n] = append(chapters[n], ch)
			}
			if len(errs) > 0 {
				results = append(results, result{n, atoi(m[1]), false, errs})
				failed = true
				continue
			}
			wg.Add(1)
			go func(n int, ch *Chapter) {
				defer wg.Done()
				sem <- struct{}{}
				defer func() { <-sem }()
				errs := validateRun(ch)
				mu.Lock()
				results = append(results, result{n, ch.Chapter, len(errs) == 0, errs})
				if len(errs) > 0 {
					failed = true
				}
				mu.Unlock()
			}(n, ch)
		}
	}
	wg.Wait()

	// 生成
	if !*noGen && !failed {
		for n, chs := range chapters {
			sort.Slice(chs, func(i, j int) bool { return chs[i].Chapter < chs[j].Chapter })
			if err := generate(n, titles[n], chs); err != nil {
				fmt.Printf("生成 NG lesson%02d: %v\n", n, err)
				failed = true
			}
		}
	}

	// 集計表
	sort.Slice(results, func(i, j int) bool {
		if results[i].lesson != results[j].lesson {
			return results[i].lesson < results[j].lesson
		}
		return results[i].chapter < results[j].chapter
	})
	byLesson := map[int][2]int{} // [チャプター数, 合格数]
	for _, r := range results {
		v := byLesson[r.lesson]
		v[0]++
		if r.pass {
			v[1]++
		}
		byLesson[r.lesson] = v
		for _, e := range r.errs {
			fmt.Printf("NG lesson%02d/ch%02d: %s\n", r.lesson, r.chapter, e)
		}
	}
	var nums []int
	for n := range byLesson {
		nums = append(nums, n)
	}
	sort.Ints(nums)
	fmt.Println("| レッスン | チャプター数 | answer 合格数 |")
	fmt.Println("|---|---|---|")
	for _, n := range nums {
		v := byLesson[n]
		fmt.Printf("| lesson%02d %s | %d | %d |\n", n, titles[n], v[0], v[1])
	}
	if failed {
		os.Exit(1)
	}
	fmt.Println("ALL OK")
}

func atoi(s string) int { n, _ := strconv.Atoi(strings.TrimLeft(s, "0")); return n }

func parseOnly(s string) map[int]bool {
	if s == "" {
		return nil
	}
	m := map[int]bool{}
	for _, part := range strings.Split(s, ",") {
		if lo, hi, ok := strings.Cut(part, "-"); ok {
			a, _ := strconv.Atoi(strings.TrimSpace(lo))
			b, _ := strconv.Atoi(strings.TrimSpace(hi))
			for i := a; i <= b; i++ {
				m[i] = true
			}
		} else {
			a, _ := strconv.Atoi(strings.TrimSpace(part))
			m[a] = true
		}
	}
	return m
}

// loadAndFix は JSON を読み、静的な検証と gofmt 整形（自動修正）を行う。
func loadAndFix(path string) (*Chapter, []string) {
	var errs []string
	b, err := os.ReadFile(path)
	if err != nil {
		return nil, []string{err.Error()}
	}
	var c Chapter
	if err := json.Unmarshal(b, &c); err != nil {
		return nil, []string{"JSON parse error: " + err.Error()}
	}
	if c.Title == "" || c.Text == "" || c.Sample == "" ||
		c.Exercise.Description == "" || c.Exercise.Starter == "" || c.Exercise.Answer == "" {
		errs = append(errs, "必須フィールドが空です (title/text/sample/description/starter/answer)")
	}
	switch c.Priority {
	case "🔴", "🟡", "⚪":
	default:
		errs = append(errs, "priority は 🔴/🟡/⚪ のいずれかにしてください")
	}
	switch c.Kind {
	case "", "program":
		for i, t := range c.tests() {
			if strings.TrimSpace(t.Expected) == "" {
				errs = append(errs, fmt.Sprintf("テスト %d の expected_stdout が空です", i+1))
			}
		}
	case "web":
		// web 型はプレビュー + 自己チェックなので期待出力は不要
	default:
		errs = append(errs, "kind は program か web にしてください")
	}
	return &c, errs
}

// validateRun は sample / answer を実際に実行して検証する。
func validateRun(c *Chapter) []string {
	if c.Kind == "web" {
		return nil // web 型は実行検証をしない
	}
	var errs []string
	tests := c.tests()

	if _, stderr, timedOut, err := execProgram(c.Sample, tests[0].Stdin); err != nil || timedOut || stderr != "" {
		errs = append(errs, "sample が動きません: "+firstLine(stderr, err, timedOut))
	}
	for i, t := range tests {
		stdout, stderr, timedOut, err := execProgram(c.Exercise.Answer, t.Stdin)
		if err != nil || timedOut || stderr != "" {
			errs = append(errs, fmt.Sprintf("answer がテスト %d で動きません: %s", i+1, firstLine(stderr, err, timedOut)))
			break
		}
		if normalize(stdout) != normalize(t.Expected) {
			errs = append(errs, fmt.Sprintf("answer がテスト %d で不一致: got %q want %q",
				i+1, normalize(stdout), normalize(t.Expected)))
		}
	}
	return errs
}

func firstLine(stderr string, err error, timedOut bool) string {
	if timedOut {
		return "タイムアウト"
	}
	if stderr != "" {
		lines := strings.SplitN(strings.TrimSpace(stderr), "\n", 2)
		return lines[0]
	}
	if err != nil {
		return err.Error()
	}
	return "不明"
}

// execProgram は一時ディレクトリで受講者コードを実行する。
func execProgram(code, stdin string) (stdout, stderr string, timedOut bool, err error) {
	tmp, err := os.MkdirTemp("", "coursegen-*")
	if err != nil {
		return "", "", false, err
	}
	defer os.RemoveAll(tmp)
	if err := writeSourceTree(tmp, code); err != nil {
		return "", "", false, err
	}

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()
	cmd := runnerCmd(ctx, tmp)
	cmd.Stdin = strings.NewReader(stdin)
	var out, errBuf strings.Builder
	cmd.Stdout = &out
	cmd.Stderr = &errBuf
	cmd.Run()
	if ctx.Err() == context.DeadlineExceeded {
		return out.String(), errBuf.String(), true, nil
	}
	return out.String(), errBuf.String(), false, nil
}

func normalize(s string) string {
	s = strings.ReplaceAll(s, "\r\n", "\n")
	lines := strings.Split(s, "\n")
	for i := range lines {
		lines[i] = strings.TrimRight(lines[i], " \t")
	}
	return strings.TrimRight(strings.Join(lines, "\n"), "\n")
}

// generate は JSON からレッスンの README / sample / exercise / answer を書き出す。
func generate(lesson int, title string, chs []*Chapter) error {
	dir := filepath.Join(*root, fmt.Sprintf("lesson%02d", lesson))

	var readme strings.Builder
	fmt.Fprintf(&readme, "# Lesson %02d %s\n", lesson, title)
	if intro, err := os.ReadFile(filepath.Join(dir, "intro.md")); err == nil {
		readme.WriteString("\n" + strings.TrimSpace(string(intro)) + "\n")
	}
	for _, c := range chs {
		fmt.Fprintf(&readme, "\n## ch%02d %s\n\n%s\n", c.Chapter, c.Title, strings.TrimSpace(c.Text))
	}
	if err := os.WriteFile(filepath.Join(dir, "README.md"), []byte(readme.String()), 0o644); err != nil {
		return err
	}

	if err := os.MkdirAll(filepath.Join(dir, "answer"), 0o755); err != nil {
		return err
	}
	for _, c := range chs {
		chName := fmt.Sprintf("ch%02d", c.Chapter)
		ext := langExt
		if c.Kind == "web" {
			ext = ".html"
		}
		if err := os.WriteFile(filepath.Join(dir, chName+"_sample"+ext), []byte(c.Sample), 0o644); err != nil {
			return err
		}
		if err := os.WriteFile(filepath.Join(dir, "answer", chName+"_answer"+ext), []byte(c.Exercise.Answer), 0o644); err != nil {
			return err
		}

		var ex strings.Builder
		fmt.Fprintf(&ex, "# lesson%02d %s 演習: %s\n\n%s\n", lesson, chName, c.Title, strings.TrimSpace(c.Exercise.Description))
		if len(c.Exercise.Tests) > 0 {
			ex.WriteString("\n## テストケース\n")
			for i, t := range c.Exercise.Tests {
				fmt.Fprintf(&ex, "\n### ケース %d\n\n入力:\n\n```text\n%s\n```\n\n期待出力:\n\n```text\n%s\n```\n",
					i+1, strings.TrimRight(t.Stdin, "\n"), strings.TrimRight(t.Expected, "\n"))
			}
		}
		if err := os.WriteFile(filepath.Join(dir, chName+"_exercise.md"), []byte(ex.String()), 0o644); err != nil {
			return err
		}
	}
	return nil
}
