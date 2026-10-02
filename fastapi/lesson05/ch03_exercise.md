# lesson05 ch03 演習: モデルの属性を使う

長方形の面積を計算する API を作ります。

- `width`(整数)と `height`(整数)を持つモデル `Rectangle` を定義する
- `POST /rectangles` で `Rectangle` を受け取り、面積(width × height)を `{"area": 面積}` の形で返す

**期待出力**

```text
200
{'area': 35}
{'area': 9}
```
