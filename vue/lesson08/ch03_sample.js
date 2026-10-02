// function 宣言
function add1(a, b) {
  return a + b;
}

// 同じものをアロー関数で(1 行の式なら { } と return を省略できます)
const add2 = (a, b) => a + b;

console.log(add1(2, 3));  // 5
console.log(add2(2, 3));  // 5

// 引数が 1 つなら ( ) も省略できます
const double = n => n * 2;
console.log(double(10));  // 20

// 複数行の処理を書くときは { } と return が必要です
const hello = (name) => {
  const message = `こんにちは、${name}さん`;
  return message;
};
console.log(hello("みき"));
