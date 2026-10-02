// const: 再代入しない変数(基本はこちら)
const language = "JavaScript";
console.log(language);

// let: あとから値を入れ直す変数
let count = 0;
console.log(count);
count = count + 1;  // 再代入
console.log(count);

// const に再代入するとエラーになります
// language = "Python";  // TypeError になるのでコメントにしています

// Python:     name = "太郎"
// JavaScript: const name = "太郎";
const name = "太郎";
console.log(name);
