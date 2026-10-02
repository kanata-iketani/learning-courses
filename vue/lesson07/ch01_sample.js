// 配列は [ ] で作ります(Python のリストと同じ発想)
const fruits = ["りんご", "みかん", "ぶどう"];

// 添字は 0 から始まります
console.log(fruits[0]);  // りんご
console.log(fruits[2]);  // ぶどう

// 要素数は length (Python の len(fruits) に相当)
console.log(fruits.length);  // 3

// 最後の要素は length - 1 番目です
console.log(fruits[fruits.length - 1]);  // ぶどう

// 配列をそのまま表示すると、Node.js ではこのように見えます
console.log(fruits);  // [ 'りんご', 'みかん', 'ぶどう' ]
