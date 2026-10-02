// 1 行の式だけなら { } と return を省略でき、式の値がそのまま戻り値になります
const triple = n => n * 3;
// 戻り値がテンプレートリテラルでも書き方は同じです
const greetTo = name => `ようこそ、${name}さん`;

console.log(triple(7));
console.log(greetTo("ゆい"));
