const item = "ノート";
const price = 150;
const count = 3;
// バッククォートで囲み、${} の中に変数や計算式をそのまま書けます
// + で連結するより、文章の形が崩れず読みやすくなります
console.log(`${item}を${count}冊買うと${price * count}円です`);
console.log(`1冊あたり${price}円です`);
