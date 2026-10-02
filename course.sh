#!/bin/bash
# 学習講座アプリの起動/停止/状態確認
# 使い方: ./course.sh {start|stop|restart|status} {go|fastapi|vue|terraform|takken|all}
set -u

declare -A ROOTS=( [go]="$HOME/learning/go" [fastapi]="$HOME/learning/fastapi" [vue]="$HOME/learning/vue" [terraform]="$HOME/learning/terraform" [takken]="$HOME/learning/takken" )
declare -A PORTS=( [go]=8080 [fastapi]=8081 [vue]=8082 [terraform]=8083 [takken]=8084 )

targets() {
  if [ "${1:-all}" = "all" ]; then echo "go fastapi vue terraform takken"; else echo "$1"; fi
}

is_up() { curl -s -m 2 "http://127.0.0.1:${PORTS[$1]}/api/course" >/dev/null 2>&1; }

start_one() {
  local c=$1
  if is_up "$c"; then echo "$c: すでに起動しています (http://127.0.0.1:${PORTS[$c]})"; return; fi
  nohup go -C "${ROOTS[$c]}/app" run . >"${ROOTS[$c]}/app/server.log" 2>&1 &
  for _ in $(seq 1 20); do sleep 0.5; is_up "$c" && break; done
  if is_up "$c"; then echo "$c: 起動しました → http://127.0.0.1:${PORTS[$c]}"
  else echo "$c: 起動に失敗しました (${ROOTS[$c]}/app/server.log を確認)"; fi
}

stop_one() {
  local c=$1
  if ! is_up "$c"; then echo "$c: 停止済みです"; return; fi
  fuser -k "${PORTS[$c]}/tcp" >/dev/null 2>&1
  sleep 1
  if is_up "$c"; then echo "$c: 停止に失敗しました"; else echo "$c: 停止しました"; fi
}

status_one() {
  local c=$1
  if is_up "$c"; then echo "$c: 🟢 起動中 → http://127.0.0.1:${PORTS[$c]}"
  else echo "$c: ⚪ 停止中"; fi
}

cmd=${1:-status}
for c in $(targets "${2:-all}"); do
  case "$cmd" in
    start)   start_one "$c" ;;
    stop)    stop_one "$c" ;;
    restart) stop_one "$c"; start_one "$c" ;;
    status)  status_one "$c" ;;
    *) echo "使い方: $0 {start|stop|restart|status} {go|fastapi|vue|terraform|takken|all}"; exit 1 ;;
  esac
done
