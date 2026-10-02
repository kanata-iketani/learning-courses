import json

# ensure_ascii=False を付けないと "\u30b3\u30fc..." のようにエスケープされてしまいます。
# API のレスポンスはこの JSON 文字列の形でネットワークを流れます。
menu = {"item": "コーヒー", "price": 480}
print(json.dumps(menu, ensure_ascii=False))
