Go から PostgreSQL に接続し、メモリ版の API を「再起動しても消えない」API に作り変えます。sql.Open と db.Exec による準備、プレースホルダーを使った INSERT と SQL インジェクション対策、db.Query と rows.Next による一覧取得までを、Exec・Query・QueryRow の使い分けとあわせて説明できるようにします。
