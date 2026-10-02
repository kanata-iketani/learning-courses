// 引数 name を受け取る関数
function greet(name) {
  console.log(`こんにちは、${name}さん`);
}
greet("たろう");
greet("はなこ");

// return で計算結果を呼び出し元に返します
function add(a, b) {
  return a + b;
}

// 戻り値は変数に入れられます
const sum = add(3, 5);
console.log(sum);  // 8

// そのまま console.log に渡すこともできます
console.log(add(10, 20));  // 30
