const name = "花子";
const age = 20;

// バッククォート ` で囲むと ${} で変数を埋め込めます
console.log(`こんにちは、${name}さん`);

// ${} の中では計算もできます
console.log(`${age}歳、来年は${age + 1}歳です`);

// + で連結しても同じ結果ですが、読みにくくなりがちです
console.log("こんにちは、" + name + "さん");

// Python:     f"こんにちは、{name}さん"
// JavaScript: `こんにちは、${name}さん`
