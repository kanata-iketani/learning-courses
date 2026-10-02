// Terraform入門 講座固有の設定。
package main

import (
	"context"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

const (
	courseTitle = "Terraform入門"
	defaultAddr = "127.0.0.1:8083"
	srcFileName = "main.tf"
	editorLang  = "hcl"
	codeFence   = "hcl" // 質問回答のコードフェンス言語

	qaCourseDesc = "「Terraform入門」(HCL の文法から、実務のコードベースで分かれる書き方の流儀までを学ぶ講座) の"
	qaAudience   = "受講者はプログラミング経験はありますが、Terraform と IaC は初めてです。実務(Finatext/Skillax)の Terraform コードを読めるようになるのが目標です。"
	qaExtraRule  = "- 実務では複数の書き方が存在する話題(count/for_each、環境分割など)は「現場ではこう分かれる」という視点を添える"
)

// fileMarker は 1 つのエディタ内容を複数ファイルに分割するための区切り行。
// 例: # === file: modules/network/main.tf ===
const fileMarker = "# === file: "

// writeSourceTree はコードを main.tf (または区切り指定の複数ファイル) として dir に書き出す。
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
				continue // 不正なパスは無視して直前のファイルに書き続ける
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

// buildRunCmd は terraform init → apply → output を実行するコマンドを組み立てる。
// プロバイダ不要の構成(locals / variable / output / terraform_data / ローカルモジュール)なら
// ネットワークなしで 1 秒未満で完了する。
func buildRunCmd(ctx context.Context, dir string) *exec.Cmd {
	script := "terraform init -backend=false -input=false -no-color >/dev/null && " +
		"terraform apply -auto-approve -input=false -no-color >/dev/null && " +
		"terraform output -no-color"
	cmd := exec.CommandContext(ctx, "bash", "-c", script)
	cmd.Dir = dir
	cmd.Env = append(os.Environ(), "CHECKPOINT_DISABLE=1", "TF_IN_AUTOMATION=1")
	return cmd
}

func defaultStarterCode() string {
	return "# ここに書く\n"
}

// reviewGenRules は復習問題自動生成プロンプトの講座固有ルール。
const reviewGenRules = `- sample / starter / answer は 1 ファイルの Terraform (HCL)。プロバイダは使わず variable / locals / output / terraform_data だけで構成する
- 採点は terraform apply 後の terraform output の出力 (例: name = "app-prod" の形式、アルファベット順) と照合される。expected_stdout はその形式で書く
- 演習は標準入力を使わない (stdin は "")`
