// 変えない値は const、あとで入れ直す値だけ let にします
const city = "東京";
let year = 2025;
console.log(city);
console.log(year);
// let で宣言したので再代入できます(const だとここでエラーになります)
year = 2026;
console.log(year);
