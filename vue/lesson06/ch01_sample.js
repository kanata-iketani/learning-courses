// ( ) の中は「初期化; 続ける条件; 更新」の 3 つの部品です
// Python: for i in range(5):
for (let i = 0; i < 5; i++) {
  console.log(i);  // 0 から 4 まで表示されます
}

// 1 から 3 までにしたいときは、開始と条件を変えます
for (let i = 1; i <= 3; i++) {
  console.log(`${i}回目`);
}

// カウンタで計算もできます
for (let i = 1; i <= 3; i++) {
  console.log(i * 10);  // 10 20 30
}
