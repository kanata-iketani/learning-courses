const temperature = 30;
// 条件は ( ) の中に、実行する処理は { } の中に書きます
if (temperature >= 28) {
  console.log("エアコンをつける");
} else {
  console.log("窓を開ける");
}

const money = 500;
// money は 500 なので条件が成り立たず、else 側が実行されます
if (money >= 1000) {
  console.log("タクシーで帰る");
} else {
  console.log("歩いて帰る");
}
