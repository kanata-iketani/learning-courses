// 条件が true の間くり返します(Python の while とほぼ同じ)
let count = 3;
while (count > 0) {
  console.log(count);
  count = count - 1;  // 更新を忘れると無限ループになります
}
console.log("発射！");

// break はループをその場で打ち切る命令です
let n = 1;
while (true) {
  if (n > 3) {
    break;  // ここでループ終了
  }
  console.log(n);
  n++;
}
