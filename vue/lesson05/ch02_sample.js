// 大小の比較は Python と同じです。結果は true / false になります
console.log(10 > 3);    // true
console.log(10 < 3);    // false
console.log(10 >= 10);  // true

// 「等しい」は === (Python の == に相当)
console.log(5 === 5);    // true
console.log(5 === "5");  // false (数値と文字列は別物)

// 「等しくない」は !== (Python の != に相当)
console.log(5 !== 3);    // true

// 比較の結果は変数にも入れられます
const isAdult = 20 >= 18;
console.log(isAdult);  // true
