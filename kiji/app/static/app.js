// 宅建どうじょう フロントエンド（4択クイズ型）
const $ = (id) => document.getElementById(id);

let course = { lessons: [] };
let cur = { lesson: 0, chapter: 0 };
let curData = null; // /api/chapter のレスポンス
let curQ = 0;       // 表示中の問題番号
let answering = false;

// ---- 簡易 Markdown レンダラ ----
function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
function inlineMd(s) {
  s = esc(s);
  s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
  s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  return s;
}
// 図(Mermaid)を描画する。描けなかった図は元のテキストのまま残す
async function renderDiagrams() {
  if (!window.mermaid) return;
  try { await window.mermaid.run({ querySelector: 'pre.mermaid:not([data-processed])', suppressErrors: true }); } catch (e) { console.warn(e); }
}

function mdToHtml(md) {
  const lines = (md || '').replace(/\r\n/g, '\n').split('\n');
  let html = '', i = 0, list = null;
  const closeList = () => { if (list) { html += `</${list}>`; list = null; } };
  while (i < lines.length) {
    const line = lines[i];
    if (/^```/.test(line)) {
      closeList();
      const lang = line.slice(3).trim();
      const code = [];
      i++;
      while (i < lines.length && !/^```/.test(lines[i])) { code.push(lines[i]); i++; }
      i++;
      if (lang === 'mermaid') {
        html += `<div class="diagram"><pre class="mermaid">${esc(code.join('\n'))}</pre></div>`;
      } else {
        html += `<pre class="code"><code>${esc(code.join('\n'))}</code></pre>`;
      }
      continue;
    }
    const h = line.match(/^(#{1,4})\s+(.*)/);
    if (h) { closeList(); const lv = Math.min(h[1].length + 2, 6); html += `<h${lv}>${inlineMd(h[2])}</h${lv}>`; i++; continue; }
    if (/^>\s?/.test(line)) {
      closeList();
      const quote = [];
      while (i < lines.length && /^>\s?/.test(lines[i])) { quote.push(lines[i].replace(/^>\s?/, '')); i++; }
      html += `<blockquote>${quote.map(inlineMd).join('<br>')}</blockquote>`;
      continue;
    }
    if (/^\|/.test(line)) {
      closeList();
      const rows = [];
      while (i < lines.length && /^\|/.test(lines[i])) { rows.push(lines[i]); i++; }
      const cells = (r) => r.replace(/^\||\|$/g, '').split('|').map((c) => inlineMd(c.trim()));
      let t = '<table>';
      rows.forEach((r, idx) => {
        if (/^\|[\s:-]+\|?[\s|:-]*$/.test(r)) return; // 区切り行
        const tag = idx === 0 ? 'th' : 'td';
        t += '<tr>' + cells(r).map((c) => `<${tag}>${c}</${tag}>`).join('') + '</tr>';
      });
      html += t + '</table>';
      continue;
    }
    const ul = line.match(/^[-*]\s+(.*)/);
    if (ul) { if (list !== 'ul') { closeList(); html += '<ul>'; list = 'ul'; } html += `<li>${inlineMd(ul[1])}</li>`; i++; continue; }
    const ol = line.match(/^\d+\.\s+(.*)/);
    if (ol) { if (list !== 'ol') { closeList(); html += '<ol>'; list = 'ol'; } html += `<li>${inlineMd(ol[1])}</li>`; i++; continue; }
    if (line.trim() === '') { closeList(); i++; continue; }
    const para = [line];
    i++;
    while (i < lines.length && lines[i].trim() !== '' && !/^(#{1,4}\s|```|[-*]\s|\d+\.\s|>|\|)/.test(lines[i])) {
      para.push(lines[i]); i++;
    }
    closeList();
    html += `<p>${para.map(inlineMd).join('<br>')}</p>`;
  }
  closeList();
  return html;
}

// ---- コースナビ ----
async function loadCourse() {
  course = await (await fetch('/api/course')).json();
  const sel = $('lessonSelect');
  sel.innerHTML = '';
  for (const l of course.lessons) {
    const passed = l.chapters.filter((c) => c.status === 'passed').length;
    const opt = document.createElement('option');
    opt.value = l.lesson;
    opt.textContent = `第${l.lesson}章 ${l.title || ''} (${passed}/${l.chapters.length})`;
    sel.appendChild(opt);
  }
  sel.onchange = () => {
    const l = course.lessons.find((x) => x.lesson === Number(sel.value));
    if (l) openChapter(l.lesson, l.chapters[0].chapter);
  };
  updateProgressBadge();
}

function lessonOf(n) { return course.lessons.find((x) => x.lesson === n); }

function renderChapterTabs() {
  const l = lessonOf(cur.lesson);
  const nav = $('chapterTabs');
  nav.innerHTML = '';
  if (!l) return;
  for (const c of l.chapters) {
    const b = document.createElement('button');
    b.className = 'chTab' + (c.chapter === cur.chapter ? ' active' : '') + (c.status === 'passed' ? ' passed' : '');
    b.textContent = `${c.chapter}. ${c.title}`;
    b.onclick = () => openChapter(cur.lesson, c.chapter);
    nav.appendChild(b);
  }
}

function updateProgressBadge() {
  let total = 0, passed = 0;
  for (const l of course.lessons) {
    total += l.chapters.length;
    passed += l.chapters.filter((c) => c.status === 'passed').length;
  }
  $('progressBadge').textContent = `クリア ${passed}/${total}`;
}

function markLocalStatus(status) {
  const l = lessonOf(cur.lesson);
  if (!l) return;
  const c = l.chapters.find((x) => x.chapter === cur.chapter);
  if (c && c.status !== 'passed') c.status = status;
  renderChapterTabs();
  updateProgressBadge();
  const sel = $('lessonSelect');
  const opt = [...sel.options].find((o) => Number(o.value) === cur.lesson);
  if (opt) {
    const passed = l.chapters.filter((x) => x.status === 'passed').length;
    opt.textContent = `第${l.lesson}章 ${l.title || ''} (${passed}/${l.chapters.length})`;
  }
}

async function openChapter(lesson, chapter) {
  const res = await fetch(`/api/chapter/${lesson}/${chapter}`);
  if (!res.ok) return;
  curData = await res.json();
  cur = { lesson, chapter };
  location.hash = `#${lesson}/${chapter}`;

  $('lessonSelect').value = lesson;
  renderChapterTabs();

  $('chTitle').textContent = `${curData.title} ${curData.priority || ''}`;
  $('chText').innerHTML = mdToHtml(curData.text);
  renderDiagrams();
  $('lessonPane').scrollTop = 0;

  // 最初の未正解問題から始める
  const firstUnsolved = curData.solved.findIndex((s) => !s);
  showQuestion(firstUnsolved >= 0 ? firstUnsolved : 0);
  qaSetContext();
}

// ---- クイズ ----
function circled(i) { return ['①', '②', '③', '④', '⑤', '⑥'][i] || String(i + 1); }

function renderDots() {
  const dots = $('quizDots');
  dots.innerHTML = '';
  curData.quiz.forEach((_, i) => {
    const d = document.createElement('button');
    d.className = 'dot' + (curData.solved[i] ? ' solved' : '') + (i === curQ ? ' current' : '');
    d.textContent = i + 1;
    d.title = `問 ${i + 1}`;
    d.onclick = () => showQuestion(i);
    dots.appendChild(d);
  });
}

function showQuestion(i) {
  curQ = i;
  const q = curData.quiz[i];
  $('clearBanner').classList.add('hidden');
  $('feedback').classList.add('hidden');
  $('quizCounter').textContent = `問 ${i + 1} / ${curData.quiz.length}`;
  renderDots();
  $('questionText').innerHTML = mdToHtml(q.question);
  const box = $('choices');
  box.innerHTML = '';
  if (q.kind === 'code') { showCode(q, box); return; }
  if (q.kind === 'sql') { showSQL(q, box); return; }
  if (q.kind === 'essay') { showEssay(q, box); return; }
  q.choices.forEach((text, ci) => {
    const b = document.createElement('button');
    b.className = 'choice';
    b.innerHTML = `<span class="num">${circled(ci)}</span><span>${inlineMd(text)}</span>`;
    b.onclick = () => answer(ci);
    box.appendChild(b);
  });
}

function qRef() { return { lesson: cur.lesson, chapter: cur.chapter, q: curQ }; }

// ---- SQL 問題: 書いて実行 → 提出で自動採点 ----
function resultTable(res) {
  if (!res) return '';
  if (!res.columns || res.columns.length === 0) return `<div class="sqlNote">${esc(res.note || '結果なし')}</div>`;
  const head = '<tr>' + res.columns.map((c) => `<th>${esc(c)}</th>`).join('') + '</tr>';
  const rows = res.rows.slice(0, 200).map((r) => '<tr>' + r.map((v) => `<td>${v === null ? '<i>NULL</i>' : esc(String(v))}</td>`).join('') + '</tr>').join('');
  return `<div class="sqlTableWrap"><table class="sqlTable">${head}${rows}</table></div><div class="sqlNote">${res.rows.length >= 201 ? '200 行以上あります(先頭のみ表示)' : res.rows.length + ' 行'}</div>`;
}
function draftBox(placeholder, cls) {
  const ta = document.createElement('textarea');
  ta.className = 'writeBox ' + (cls || '');
  ta.placeholder = placeholder;
  ta.spellcheck = false;
  const ref = qRef();
  const key = `kjDraft:${ref.lesson}/${ref.chapter}/${ref.q}`;
  try { ta.value = localStorage.getItem(key) || ''; } catch (e) {}
  ta.oninput = () => { try { localStorage.setItem(key, ta.value); } catch (e) {} };
  ta.addEventListener('keydown', (ev) => {
    if (ev.key === 'Tab') { ev.preventDefault(); const p = ta.selectionStart; ta.setRangeText('  ', p, ta.selectionEnd, 'end'); }
  });
  return ta;
}
async function postJSON(url, body) {
  const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
// ---- コーディング問題: 書いて実行 → 提出で、模範解答と出力を比べて自動採点 ----
function showCode(q, box) {
  const langName = { go: 'Go', js: 'JavaScript', ts: 'TypeScript', python: 'Python' }[q.lang] || q.lang;
  const ta = draftBox(`${langName} のコードを書きます(Ctrl+Enter で実行)`, 'sqlBox codeBox');
  if (!ta.value && q.setup) ta.value = q.setup;
  const reset = document.createElement('button'); reset.className = 'btn ghost'; reset.textContent = '雛形に戻す';
  reset.onclick = () => { ta.value = q.setup || ''; ta.dispatchEvent(new Event('input')); };
  const stdin = document.createElement('textarea'); stdin.className = 'writeBox stdinBox'; stdin.placeholder = '標準入力(必要なときだけ)';
  const out = document.createElement('div'); out.className = 'sqlOut';
  const run = document.createElement('button'); run.className = 'btn ghost'; run.textContent = '▶ 実行(採点しない)';
  const sub = document.createElement('button'); sub.className = 'btn primary'; sub.textContent = '提出して採点';
  const bar = document.createElement('div'); bar.className = 'sqlBar'; bar.append(run, sub, reset);
  const pre = (t, cls) => `<pre class="code ${cls || ''}"><code>${esc(t || '')}</code></pre>`;
  run.onclick = async () => {
    out.innerHTML = '<div class="qaThinking">実行中…</div>';
    try {
      const r = await postJSON('/api/code/run', { ...qRef(), draft: ta.value, stdin: stdin.value });
      out.innerHTML = '<div class="writeLabel">出力</div>' + pre(r.stdout) + (r.stderr ? '<div class="writeLabel">エラー</div>' + pre(r.stderr, 'errOut') : '');
    } catch (e) { out.innerHTML = `<div class="sqlErr">${esc(e.message)}</div>`; }
  };
  ta.addEventListener('keydown', (ev) => { if ((ev.ctrlKey || ev.metaKey) && ev.key === 'Enter') { ev.preventDefault(); run.onclick(); } });
  sub.onclick = async () => {
    out.innerHTML = '<div class="qaThinking">採点中…(コードを実際に動かしています)</div>';
    try {
      const r = await postJSON('/api/quiz/grade', { ...qRef(), draft: ta.value });
      let h = `<div class="gradeBanner ${r.pass ? 'good' : 'bad'}">${r.pass ? '⭕ 正解' : '❌ 不正解'} — ${esc(r.feedback || '')}</div>`;
      (r.tests || []).forEach((t, i) => {
        h += `<div class="writeLabel">テスト ${i + 1} ${t.ok ? '⭕' : '❌'}${t.stdin ? '(入力: ' + esc(t.stdin.slice(0, 40)) + ')' : ''}</div>`;
        if (!t.ok) h += '<div>あなたの出力</div>' + pre(t.got) + (t.stderr ? pre(t.stderr, 'errOut') : '') + '<div>期待される出力</div>' + pre(t.expected);
      });
      out.innerHTML = h;
      answer(r.pass ? 0 : 1);
    } catch (e) { out.innerHTML = `<div class="sqlErr">${esc(e.message)}</div>`; }
  };
  box.append(ta, stdin, bar, out);
}

function showSQL(q, box) {
  if (q.setup) {
    const d = document.createElement('details');
    d.className = 'sqlSetup';
    d.innerHTML = `<summary>テーブル定義と入っているデータを見る</summary><pre class="code"><code>${esc(q.setup)}</code></pre>`;
    box.appendChild(d);
  }
  const ta = draftBox('ここに SQL を書きます(例: SELECT ... FROM ... WHERE ...;)  Ctrl+Enter で実行', 'sqlBox');
  const out = document.createElement('div');
  out.className = 'sqlOut';
  const run = document.createElement('button'); run.className = 'btn ghost'; run.textContent = '▶ 実行(採点しない)';
  const sub = document.createElement('button'); sub.className = 'btn primary'; sub.textContent = '提出して採点';
  const bar = document.createElement('div'); bar.className = 'sqlBar'; bar.append(run, sub);
  run.onclick = async () => {
    out.innerHTML = '<div class="qaThinking">実行中…</div>';
    try {
      const r = await postJSON('/api/sql/run', { ...qRef(), draft: ta.value });
      out.innerHTML = r.error ? `<div class="sqlErr">エラー: ${esc(r.error)}</div>` : '<div class="writeLabel">実行結果</div>' + resultTable(r.result);
    } catch (e) { out.innerHTML = `<div class="sqlErr">${esc(e.message)}</div>`; }
  };
  ta.addEventListener('keydown', (ev) => { if ((ev.ctrlKey || ev.metaKey) && ev.key === 'Enter') { ev.preventDefault(); run.onclick(); } });
  sub.onclick = async () => {
    if (!ta.value.trim()) { out.innerHTML = '<div class="sqlErr">SQL が空です</div>'; return; }
    out.innerHTML = '<div class="qaThinking">採点中…</div>';
    try {
      const r = await postJSON('/api/quiz/grade', { ...qRef(), draft: ta.value });
      let h = `<div class="gradeBanner ${r.pass ? 'good' : 'bad'}">${r.pass ? '⭕ 正解(結果が一致)' : '❌ 不正解'}</div><div>${esc(r.feedback || '')}</div>`;
      h += '<div class="writeLabel">あなたの結果</div>' + resultTable(r.result);
      if (r.expected) h += '<div class="writeLabel">期待される結果</div>' + resultTable(r.expected);
      out.innerHTML = h;
      answer(r.pass ? 0 : 1);
    } catch (e) { out.innerHTML = `<div class="sqlErr">${esc(e.message)}</div>`; }
  };
  box.append(ta, bar, out);
}

// ---- 記述式: AI(ローカルの Claude)が採点 ----
function showEssay(q, box) {
  const ta = draftBox('自分の考えを書いてください(箇条書き・図の説明・コードも可)', 'essayBox');
  const cnt = document.createElement('div');
  cnt.className = 'writeCount';
  const upd = () => { cnt.textContent = `${[...ta.value.replace(/\s/g, '')].length} 字`; };
  ta.addEventListener('input', upd); upd();
  const sub = document.createElement('button'); sub.className = 'btn primary'; sub.textContent = 'AI に採点してもらう';
  const out = document.createElement('div'); out.className = 'sqlOut';
  sub.onclick = async () => {
    if (!ta.value.trim()) { out.innerHTML = '<div class="sqlErr">解答が空です</div>'; return; }
    sub.disabled = true;
    out.innerHTML = '<div class="qaThinking">採点中…(30秒〜1分ほどかかります)</div>';
    try {
      const r = await postJSON('/api/quiz/grade', { ...qRef(), draft: ta.value });
      const m = await postJSON('/api/quiz/reveal', qRef());
      let h = `<div class="gradeBanner ${r.pass ? 'good' : 'bad'}">${r.pass ? '⭕ 合格' : '❌ もう一歩'} — ${r.score} 点</div>`;
      if (r.good) h += `<div class="writeLabel">よかった点</div><div>${mdToHtml(r.good)}</div>`;
      if (r.missing) h += `<div class="writeLabel">足りない点</div><div>${mdToHtml(r.missing)}</div>`;
      if (r.advice) h += `<div class="writeLabel">次に意識すること</div><div>${mdToHtml(r.advice)}</div>`;
      if (r.feedback) h += `<div>${mdToHtml(r.feedback)}</div>`;
      h += `<div class="writeLabel">模範解答</div><div class="md writeAnswer">${mdToHtml(m.answer || '')}</div>`;
      out.innerHTML = h;
      answer(r.pass ? 0 : 1);
    } catch (e) { out.innerHTML = `<div class="sqlErr">${esc(e.message)}</div>`; }
    sub.disabled = false;
  };
  box.append(ta, cnt, sub, out);
}

// 質問時に「今開いている問題」と解答状況を先生に伝える
let lastAns = null;
function askContext() {
  const solved = !!(curData && curData.solved && curData.solved[curQ]);
  const la = lastAns && lastAns.lesson === cur.lesson && lastAns.chapter === cur.chapter && lastAns.q === curQ ? lastAns : null;
  const ta = document.querySelector('#choices textarea');
  return { q: curQ, answered: !!la, chosen: la ? la.choice : 0, correct: la ? la.correct : false, solved, draft: ta ? ta.value : '' };
}

async function answer(choice) {
  if (answering) return;
  answering = true;
  const buttons = [...$('choices').querySelectorAll('button.choice')];
  buttons.forEach((b) => (b.disabled = true));
  try {
    const res = await fetch('/api/quiz/answer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ lesson: cur.lesson, chapter: cur.chapter, q: curQ, choice }),
    });
    if (!res.ok) { alert(await res.text()); return; }
    const r = await res.json();
    curData.solved = r.solved;
    lastAns = { lesson: cur.lesson, chapter: cur.chapter, q: curQ, choice, correct: r.correct };
    renderDots();

    buttons[r.correctIndex]?.classList.add('correct');
    if (!r.correct) buttons[choice]?.classList.add('wrong');

    const banner = $('feedbackBanner');
    banner.className = r.correct ? 'good' : 'bad';
    banner.textContent = r.correct ? '⭕ 正解！' : '❌ 不正解…';
    $('explanation').innerHTML = mdToHtml(r.explanation);
    renderDiagrams();
    $('retryBtn').classList.toggle('hidden', r.correct);
    $('feedback').classList.remove('hidden');
    $('feedback').scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    markLocalStatus(r.cleared ? 'passed' : 'ran');
    $('nextQBtn').textContent = r.cleared ? 'クリア画面へ 🎉' : '次の問題 →';
    $('nextQBtn').dataset.cleared = r.cleared ? '1' : '';
  } catch (e) {
    alert('通信エラー: ' + e);
  } finally {
    answering = false;
  }
}

function nextQuestion() {
  if ($('nextQBtn').dataset.cleared === '1') {
    showClear();
    return;
  }
  // 次の未正解問題へ (なければ次の番号へ循環)
  const n = curData.quiz.length;
  for (let d = 1; d <= n; d++) {
    const i = (curQ + d) % n;
    if (!curData.solved[i]) { showQuestion(i); return; }
  }
  showClear();
}

function showClear() {
  $('feedback').classList.add('hidden');
  $('questionText').innerHTML = '';
  $('choices').innerHTML = '';
  $('quizCounter').textContent = `全 ${curData.quiz.length} 問クリア`;
  renderDots();
  $('clearBanner').classList.remove('hidden');
}

function nextChapter() {
  const l = lessonOf(cur.lesson);
  if (!l) return;
  const idx = l.chapters.findIndex((c) => c.chapter === cur.chapter);
  if (idx >= 0 && idx + 1 < l.chapters.length) {
    openChapter(cur.lesson, l.chapters[idx + 1].chapter);
    return;
  }
  const li = course.lessons.findIndex((x) => x.lesson === cur.lesson);
  if (li >= 0 && li + 1 < course.lessons.length) {
    const nl = course.lessons[li + 1];
    openChapter(nl.lesson, nl.chapters[0].chapter);
  } else {
    alert('最後のチャプターです。おつかれさまでした！');
  }
}

// ---- 質問対話 ----
function qaSetContext() {
  if (!curData) return;
  $('qaContext').textContent = `文脈: 第${cur.lesson}章 ${curData.title}`;
}

function qaAppend(who, text, asMd) {
  const div = document.createElement('div');
  div.className = 'qaMsg ' + who;
  div.innerHTML = `<div class="who">${who === 'user' ? 'あなた' : '先生'}</div><div class="bubble"></div>`;
  const bubble = div.querySelector('.bubble');
  if (asMd) bubble.innerHTML = mdToHtml(text);
  else bubble.textContent = text;
  $('qaLog').appendChild(div);
  $('qaLog').scrollTop = $('qaLog').scrollHeight;
  return div;
}

let oralPending = null; // 口頭試問の出題中の問題文

function qaThinking(text) {
  const d = document.createElement('div');
  d.className = 'qaThinking';
  d.textContent = text;
  $('qaLog').appendChild(d);
  $('qaLog').scrollTop = $('qaLog').scrollHeight;
  return d;
}

async function oralStart() {
  if (!curData) return;
  $('oralBtn').disabled = true;
  const thinking = qaThinking('先生が問題を考えています…');
  try {
    const res = await fetch('/api/oral', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phase: 'ask', lesson: cur.lesson, chapter: cur.chapter }),
    });
    thinking.remove();
    if (!res.ok) { qaAppend('claude', 'エラー: ' + (await res.text()), false); return; }
    const data = await res.json();
    oralPending = data.question;
    qaAppend('claude', '🎤 **口頭試問です。自分の言葉で答えてみてください。**\n\n' + data.question, true);
    $('qaInput').placeholder = '自分の言葉で答えを書いて送信（Ctrl+Enter）';
    $('qaInput').focus();
  } catch (e) {
    thinking.remove();
    qaAppend('claude', '通信エラー: ' + e, false);
  } finally {
    $('oralBtn').disabled = false;
  }
}

async function qaAsk() {
  const q = $('qaInput').value.trim();
  if (!q || !curData) return;
  $('qaInput').value = '';
  $('qaSend').disabled = true;
  qaAppend('user', q, false);
  const grading = oralPending !== null;
  const thinking = qaThinking(grading ? '先生が採点しています…' : '先生が考えています…');
  try {
    let res;
    if (grading) {
      res = await fetch('/api/oral', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phase: 'grade', lesson: cur.lesson, chapter: cur.chapter, question: oralPending, answer: q }),
      });
    } else {
      res = await fetch('/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(Object.assign({ lesson: cur.lesson, chapter: cur.chapter, question: q }, askContext())),
      });
    }
    thinking.remove();
    if (!res.ok) { qaAppend('claude', 'エラー: ' + (await res.text()), false); return; }
    const data = await res.json();
    qaAppend('claude', grading ? data.feedback : data.answer, true);
    if (grading) {
      oralPending = null;
      $('qaInput').placeholder = 'いま学んでいる内容について先生に質問（Ctrl+Enter で送信）';
      qaAppend('claude', 'もう1問受けるなら「🎤 口頭試問を受ける」を押してください。', false);
    }
  } catch (e) {
    thinking.remove();
    qaAppend('claude', '通信エラー: ' + e, false);
  } finally {
    $('qaSend').disabled = false;
  }
}

async function latestCreate() {
  if (!confirm('AI が Web 検索で最新の統計数値と法改正を調べてノートを作ります（2〜5分かかります）。よろしいですか？')) return;
  $('latestBtn').disabled = true;
  $('qaNotesStatus').textContent = '先生が最新情報を Web で調べています…（2〜5分かかります）';
  try {
    const res = await fetch('/api/qa/latest', { method: 'POST' });
    if (!res.ok) { $('qaNotesStatus').textContent = 'エラー: ' + (await res.text()); return; }
    const data = await res.json();
    $('latestNote').innerHTML = mdToHtml(data.note);
    $('qaNotesStatus').textContent = '直前対策ノートを作成しました（出典 URL 付き。直前にもう一度作り直すと最新になります）';
  } catch (e) {
    $('qaNotesStatus').textContent = '通信エラー: ' + e;
  } finally {
    $('latestBtn').disabled = false;
  }
}

async function loadMistakes() {
  const items = ((await (await fetch('/api/mistakes')).json()).items || []).slice(-30).reverse();
  const box = $('mistakeList');
  box.innerHTML = '';
  if (items.length === 0) {
    box.innerHTML = '<div class="qaThinking">間違えた問題はまだありません。</div>';
    return;
  }
  for (const m of items) {
    const div = document.createElement('div');
    div.className = 'mistakeItem';
    div.innerHTML =
      `<div class="meta"><span>${esc(m.time)} · 第${m.lesson}章 ${esc(m.title)} 問${m.q + 1}</span>` +
      `<button>この問題を解き直す →</button></div>` +
      `<div>${esc(m.question)}</div>` +
      `<div><span class="wrongPick">あなたの答え: ${esc(m.chosen)}</span> ／ 正解: ${esc(m.answer)}</div>`;
    div.querySelector('button').onclick = async () => {
      $('qaDrawer').classList.add('hidden');
      await openChapter(m.lesson, m.chapter);
      if (curData && m.q < curData.quiz.length) showQuestion(m.q);
    };
    box.appendChild(div);
  }
}

async function qaLoadNotes() {
  loadMistakes();
  try {
    const [listRes, sumRes, latestRes] = await Promise.all([
      fetch('/api/qa'), fetch('/api/qa/summary'), fetch('/api/qa/latest'),
    ]);
    const list = (await listRes.json()).items || [];
    const summary = (await sumRes.json()).summary || '';
    const latest = (await latestRes.json()).note || '';
    $('qaSummary').innerHTML = summary ? mdToHtml(summary) : '';
    $('latestNote').innerHTML = latest ? mdToHtml(latest) : '';
    const box = $('qaList');
    box.innerHTML = '';
    if (list.length === 0) {
      box.innerHTML = '<div class="qaThinking">まだ質問の記録がありません。問題を解いてつまずいたら、遠慮なく先生に聞いてみましょう。</div>';
      return;
    }
    for (const item of [...list].reverse()) {
      const div = document.createElement('div');
      div.className = 'qaItem';
      div.innerHTML =
        `<div class="meta"><span>${esc(item.time)} · 第${item.lesson}章 ${esc(item.chapterTitle || '')}</span>` +
        `<button data-id="${esc(item.id)}">削除</button></div>` +
        `<div class="q">Q. ${esc(item.question)}</div>` +
        `<div class="a">${mdToHtml(item.answer)}</div>`;
      div.querySelector('button').onclick = async (ev) => {
        if (!confirm('この質問記録を削除しますか？')) return;
        await fetch('/api/qa/' + ev.target.dataset.id, { method: 'DELETE' });
        qaLoadNotes();
      };
      box.appendChild(div);
    }
  } catch (e) {
    $('qaNotesStatus').textContent = '読み込みに失敗しました: ' + e;
  }
}

async function qaSummarize() {
  $('qaSummaryBtn').disabled = true;
  $('qaNotesStatus').textContent = '先生が弱点をまとめています…（1分ほどかかります）';
  try {
    const res = await fetch('/api/qa/summary', { method: 'POST' });
    if (!res.ok) { $('qaNotesStatus').textContent = 'エラー: ' + (await res.text()); return; }
    const data = await res.json();
    $('qaSummary').innerHTML = mdToHtml(data.summary);
    $('qaNotesStatus').textContent = '弱点ノートを更新しました';
  } catch (e) {
    $('qaNotesStatus').textContent = '通信エラー: ' + e;
  } finally {
    $('qaSummaryBtn').disabled = false;
  }
}

async function qaMakeReview() {
  if (!confirm('あなたの誤答と質問をもとに、専用の復習問題を作ります（数分かかります）。よろしいですか？')) return;
  $('qaReviewBtn').disabled = true;
  $('qaNotesStatus').textContent = '先生が復習問題を作っています…（数分かかります）';
  try {
    const res = await fetch('/api/qa/review', { method: 'POST' });
    if (!res.ok) { $('qaNotesStatus').textContent = 'エラー: ' + (await res.text()); return; }
    const data = await res.json();
    const n = (data.created || []).length;
    let msg = n > 0 ? `復習チャプターを ${n} 個作成しました。` : '作成できませんでした。';
    if ((data.failed || []).length > 0) msg += ` (失敗: ${data.failed.length}件)`;
    $('qaNotesStatus').textContent = msg;
    if (n > 0) {
      await loadCourse();
      if (confirm(msg + '\n「復習問題」を開きますか？')) {
        $('qaDrawer').classList.add('hidden');
        openChapter(data.created[0].lesson, data.created[0].chapter);
      }
    }
  } catch (e) {
    $('qaNotesStatus').textContent = '通信エラー: ' + e;
  } finally {
    $('qaReviewBtn').disabled = false;
  }
}

function initQA() {
  $('qaToggle').onclick = () => { $('qaDrawer').classList.toggle('hidden'); qaSetContext(); };
  $('qaClose').onclick = () => $('qaDrawer').classList.add('hidden');
  document.querySelectorAll('.qaTab').forEach((tab) => {
    tab.onclick = () => {
      document.querySelectorAll('.qaTab').forEach((t) => t.classList.remove('active'));
      tab.classList.add('active');
      const isChat = tab.dataset.tab === 'chat';
      $('qaChatPane').classList.toggle('hidden', !isChat);
      $('qaNotesPane').classList.toggle('hidden', isChat);
      if (!isChat) qaLoadNotes();
    };
  });
  $('qaSend').onclick = qaAsk;
  $('qaInput').addEventListener('keydown', (ev) => {
    if ((ev.ctrlKey || ev.metaKey) && ev.key === 'Enter') { ev.preventDefault(); qaAsk(); }
  });
  $('qaSummaryBtn').onclick = qaSummarize;
  $('qaReviewBtn').onclick = qaMakeReview;
  $('oralBtn').onclick = oralStart;
  $('latestBtn').onclick = latestCreate;
}

// ---- 起動 ----
async function main() {
  initQA();
  await loadCourse();
  $('nextQBtn').onclick = nextQuestion;
  $('retryBtn').onclick = () => showQuestion(curQ);
  $('nextChBtn').onclick = nextChapter;

  const m = location.hash.match(/^#(\d+)\/(\d+)$/);
  if (m && lessonOf(Number(m[1]))) {
    openChapter(Number(m[1]), Number(m[2]));
  } else if (course.lessons.length > 0) {
    const l = course.lessons[0];
    openChapter(l.lesson, l.chapters[0].chapter);
  }
}

main();
