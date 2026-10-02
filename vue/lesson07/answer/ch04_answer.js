const prices = [120, 80, 300, 150];
// filter は条件(p >= 100)が true になった要素だけを集めます
console.log(prices.filter(p => p >= 100));
// map は全要素を変換します。どちらも、もとの prices は変わりません
console.log(prices.map(p => p * 2));
