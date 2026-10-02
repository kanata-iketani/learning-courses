// 配列: 複数の値をまとめて入れる箱(次のレッスンで詳しく学びます)
const fruits = ["りんご", "みかん", "ぶどう"];

// Python:     for fruit in fruits:
// JavaScript: for (const fruit of fruits)
for (const fruit of fruits) {
  console.log(fruit);
}

// 数値の配列も同じように合計できます
const prices = [100, 250, 80];
let total = 0;
for (const price of prices) {
  total = total + price;
}
console.log(total);  // 430
