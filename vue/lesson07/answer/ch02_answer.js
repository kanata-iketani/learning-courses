const animals = ["犬", "猫"];
// const でも push はできます(配列そのものの再代入ではないため)
animals.push("鳥");
// 配列をそのまま渡すと Node.js 特有のスペース入り表示になります
console.log(animals);
console.log(animals.includes("猫"));
// pop は末尾の "鳥" を取り除くので、要素数は 2 に戻ります
animals.pop();
console.log(animals.length);
