# 質問機能に「今開いている問題・解答状況・原本画像」を渡し、モデルを opus にするパッチ(講座の app に当てる)
import sys, os
d = os.path.expanduser(sys.argv[1])
p = d + '/app/main.go'; s = open(p).read()
s = s.replace('"claude-model", "sonnet"', '"claude-model", "opus"')
open(p, 'w').write(s)
p = d + '/app/qa.go'; s = open(p).read()
if 'Answered bool' not in s:
    s = s.replace('''type askReq struct {
	Lesson   int    `json:"lesson"`
	Chapter  int    `json:"chapter"`
	Question string `json:"question"`
}''', '''type askReq struct {
	Lesson   int    `json:"lesson"`
	Chapter  int    `json:"chapter"`
	Question string `json:"question"`
	Q        int    `json:"q"`
	Answered bool   `json:"answered"`
	Chosen   int    `json:"chosen"`
	Correct  bool   `json:"correct"`
	Solved   bool   `json:"solved"`
	Draft    string `json:"draft"`
}''', 1)
    a = s.index('	chapterTitle := ""\n	if c, err := loadChapter(req.Lesson, req.Chapter); err == nil {')
    b = s.index('	if recent := questions.recentInChapter(')
    s = s[:a] + '''	chapterTitle := ""
	if c, err := loadChapter(req.Lesson, req.Chapter); err == nil {
		chapterTitle = c.Title
		fmt.Fprintf(&b, "現在学習中のチャプター: lesson%02d ch%02d「%s」\\n\\n左に表示中の教科書:\\n%s\\n\\n", req.Lesson, req.Chapter, c.Title, c.Text)
		if req.Q >= 0 && req.Q < len(c.Quiz) {
			q := c.Quiz[req.Q]
			fmt.Fprintf(&b, "【受講者が今、右に開いている問題】問%d / %d\\n%s\\n選択肢:\\n", req.Q+1, len(c.Quiz), q.Question)
			for i, ch := range q.Choices {
				fmt.Fprintf(&b, "  %d. %s\\n", i+1, ch)
			}
			if q.Answer != "" {
				fmt.Fprintf(&b, "(記述式。模範解答: %s)\\n", q.Answer)
				if strings.TrimSpace(req.Draft) != "" {
					fmt.Fprintf(&b, "受講者が書いた解答: %s\\n", req.Draft)
				}
			}
			switch {
			case req.Answered && req.Chosen < 0:
				b.WriteString("解答状況: 「わからない」を押した\\n")
			case req.Answered && req.Chosen < len(q.Choices):
				fmt.Fprintf(&b, "解答状況: 「%s」を選んで%s\\n", q.Choices[req.Chosen], map[bool]string{true: "正解", false: "不正解"}[req.Correct])
			case req.Solved:
				b.WriteString("解答状況: 以前に正解済み(今回はまだ答えていない)\\n")
			default:
				b.WriteString("解答状況: まだ答えていない → この問題の正解は明かさず、考え方のヒントにとどめる\\n")
			}
			fmt.Fprintf(&b, "この問題の正解(講師用・未解答なら明かさない): %s\\n解説(講師用): %s\\n\\n", q.Choices[q.Correct], q.Explanation)
		}
		b.WriteString("同じチャプターの他の問題(参考):\\n")
		for i, q := range c.Quiz {
			if i != req.Q {
				fmt.Fprintf(&b, "問%d: %s\\n", i+1, q.Question)
			}
		}
		b.WriteString("\\n")
	}
''' + s[b:]
    s = s.replace('- 法律用語は身近な例え話に置き換えてから正式な言い方を添える\n', '')
    s = s.replace('- 受講者がまだ解いていない問題の答えを先回りして明かさない', '- 質問の「この問題」「これ」は、上の【受講者が今、右に開いている問題】と左の教科書を指す。まずそれを前提に答える\n- 専門用語は初出時に括弧で短くかみ砕く。例え話の段落は書かない\n- 受講者がまだ解いていない問題の答えを先回りして明かさない', 1)
open(p, 'w').write(s)
p = d + '/app/static/app.js'; s = open(p).read()
s = s.replace("body: JSON.stringify({ lesson: cur.lesson, chapter: cur.chapter, question: q }),",
              "body: JSON.stringify(Object.assign({ lesson: cur.lesson, chapter: cur.chapter, question: q }, askContext())),", 1)
if 'function askContext' not in s:
    s = s.replace("async function answer(choice) {", """// 質問時に「今開いている問題」と解答状況を先生に伝える
let lastAns = null;
function askContext() {
  const solved = !!(curData && curData.solved && curData.solved[curQ]);
  const la = lastAns && lastAns.lesson === cur.lesson && lastAns.chapter === cur.chapter && lastAns.q === curQ ? lastAns : null;
  const ta = document.querySelector('#choices textarea');
  return { q: curQ, answered: !!la, chosen: la ? la.choice : 0, correct: la ? la.correct : false, solved, draft: ta ? ta.value : '' };
}

async function answer(choice) {""", 1)
if 'lastAns = {' not in s:
    s = s.replace("    curData.solved = r.solved;\n", "    curData.solved = r.solved;\n    lastAns = { lesson: cur.lesson, chapter: cur.chapter, q: curQ, choice, correct: r.correct };\n", 1)
open(p, 'w').write(s)
print(d, 'patched')
