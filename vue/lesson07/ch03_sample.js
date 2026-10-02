// オブジェクト: 名前(キー)付きで値をまとめる箱(Python の辞書に相当)
const user = {
  name: "さくら",
  age: 22,
  city: "大阪",
};

// 取り出しはドット記法 (Python: user["name"])
console.log(user.name);
console.log(user.age);

// 値の変更もドット記法でできます
user.age = 23;
console.log(user.age);

// テンプレートリテラルと組み合わせると便利です
console.log(`${user.name}さんは${user.city}在住です`);
