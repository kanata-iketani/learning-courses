const todos = ["掃除", "洗濯"];

// push: 末尾に追加します(Python の append)
// const の配列でも中身の変更は OK。再代入だけが禁止です
todos.push("買い物");
console.log(todos.length);  // 3
console.log(todos[2]);      // 買い物

// pop: 末尾の要素を取り出して返します
const last = todos.pop();
console.log(last);          // 買い物
console.log(todos.length);  // 2

// includes: 含まれていれば true (Python の in に相当)
console.log(todos.includes("掃除"));  // true
console.log(todos.includes("料理"));  // false
