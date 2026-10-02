const book = { title: "Vue入門", price: 2800, pages: 320 };
// 取り出しはドット記法。${} の中でもそのまま使えます
console.log(`${book.title}は${book.price}円です`);
console.log(book.pages);
// const でも中身(プロパティ)の変更はできます。再代入だけが禁止です
book.price = 2500;
console.log(book.price);
