// Vue.js入門 講座固有の設定。
package main

import (
	"context"
	"os"
	"os/exec"
)

const (
	courseTitle = "Vue.js入門"
	defaultAddr = "127.0.0.1:8082"
	srcFileName = "main.js"
	editorLang  = "javascript" // program 型チャプターの既定（web 型はフロント側で html に切替）
	codeFence   = "js"         // 質問回答のコードフェンス言語

	qaCourseDesc = "「Vue.js入門」(HTML/CSS/JavaScript の基礎から Vue 3 までをゼロから学ぶ講座) の"
	qaAudience   = "受講者は Python の基礎だけ学んだことがあり、HTML・CSS・JavaScript などフロントエンドの知識はゼロです。"
	qaExtraRule  = "- 専門用語(タグ・DOM・コンポーネントなど)は毎回ひと言かみ砕いて説明する"
)

// buildRunCmd は受講者コード（JavaScript）を Node.js で実行するコマンドを組み立てる。
func buildRunCmd(ctx context.Context, dir string) *exec.Cmd {
	cmd := exec.CommandContext(ctx, "node", srcFileName)
	cmd.Dir = dir
	cmd.Env = os.Environ()
	return cmd
}

func defaultStarterCode() string {
	return "// ここに書く\n"
}

// reviewGenRules は復習問題自動生成プロンプトの講座固有ルール。
const reviewGenRules = `- sample / starter / answer は Node.js (node main.js) で実行できる素の JavaScript にする (HTML や Vue は使わない)
- 演習は標準入力を使わない (stdin は "")
- 時刻・乱数など非決定的な出力は禁止`
