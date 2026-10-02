const temp = 22;
// 上から順に判定されるので、大きい数字の条件から書きます
if (temp >= 28) {
  console.log("暑い");
} else if (temp >= 15) {
  console.log("ちょうどいい");
} else {
  console.log("寒い");
}

const isRainy = false;
const isCold = false;
// || は「どちらかが true なら true」。今回は両方 false なので else 側です
if (isRainy || isCold) {
  console.log("家にいる");
} else {
  console.log("出かける");
}
