# lesson01 ch01: 辞書と JSON
import json

user = {"name": "demo", "age": 13}

# 辞書 → JSON 文字列 (API がレスポンスで返す形)
text = json.dumps(user, ensure_ascii=False)
print(text)
print(type(text))

# JSON 文字列 → 辞書 (API のレスポンスを受け取った側の処理)
data = json.loads(text)
print(data["name"])
print(type(data))
