const members = ["さくら", "たろう", "はなこ"];
// 「変数 of 配列」の語順で、先頭から 1 人ずつ member に入ります
// member はループのたびに新しく作られるので const で宣言できます
for (const member of members) {
  console.log(`こんにちは、${member}さん`);
}
