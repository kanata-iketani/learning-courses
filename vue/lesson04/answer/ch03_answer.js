// 数値はクォートで囲みません("80" と書くと + が連結になってしまいます)
const price = 80;
const count = 6;
console.log(price * count);         // 合計金額
console.log(1000 - price * count);  // おつり
// 余りを求めるときは % を使います(Python と同じ)
console.log(count % 4);
