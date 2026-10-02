// FastAPI入門 講座固有の設定。
package main

import (
	"context"
	"os"
	"os/exec"
	"path/filepath"
)

const (
	courseTitle = "FastAPI入門"
	defaultAddr = "127.0.0.1:8081"
	srcFileName = "main.py"
	editorLang  = "python" // フロントのシンタックスハイライト用
	codeFence   = "python" // 質問回答のコードフェンス言語

	qaCourseDesc = "「FastAPI入門」(Python の基礎を学び終えた人向けの FastAPI 講座) の"
	qaAudience   = "受講者は Python の基礎文法を理解していますが、Web API と FastAPI は初めてです。"
	qaExtraRule  = "- 素の Python での書き方との対比が理解を助けるなら1つ入れる"
)

// buildRunCmd は受講者コードを実行するコマンドを組み立てる。
func buildRunCmd(ctx context.Context, dir string) *exec.Cmd {
	py := filepath.Join(courseRoot, ".venv", "bin", "python")
	if _, err := os.Stat(py); err != nil {
		py = "python3"
	}
	cmd := exec.CommandContext(ctx, py, srcFileName)
	cmd.Dir = dir
	cmd.Env = append(os.Environ(), "PYTHONWARNINGS=ignore", "PYTHONDONTWRITEBYTECODE=1")
	return cmd
}

func defaultStarterCode() string {
	return "from fastapi import FastAPI\nfrom fastapi.testclient import TestClient\n\napp = FastAPI()\n\n# ここに書く\n\n# --- 動作確認(この下は変更しない) ---\nclient = TestClient(app)\n"
}

// reviewGenRules は復習問題自動生成プロンプトの講座固有ルール。
const reviewGenRules = `- sample / starter / answer は Python (FastAPI) のコード。answer は FastAPI アプリ定義 + TestClient での動作確認 print で構成し、python3 で実行すると expected_stdout と完全一致すること
- 演習は標準入力を使わない (stdin は "")
- 時刻・乱数など非決定的な出力は禁止`
