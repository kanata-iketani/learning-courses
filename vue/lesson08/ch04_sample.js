const names = ["さくら", "たろう"];

// forEach: 各要素を順に、渡した関数(コールバック)に届けます
names.forEach(name => {
  console.log(`${name}さん、こんにちは`);
});

// コールバックの 2 つ目の引数では添字も受け取れます
names.forEach((name, index) => {
  console.log(`${index}: ${name}`);
});

// 自作の関数にも関数を渡せます
function repeat(times, action) {
  for (let i = 0; i < times; i++) {
    action();  // 渡された関数をここで呼び出します
  }
}
repeat(2, () => console.log("ワン！"));
