# lesson10 ch01 演習: moduleブロックとsource

starter に用意されたローカルモジュール `./modules/greet` を呼び出してください。

1. `module "welcome"` ブロックを書き、source に `"./modules/greet"` を指定する
2. 引数 `name` に `"module"` を渡す
3. output `greeting` で `module.welcome.message` を表示する

**期待出力**

```text
greeting = "hello, module"
```
