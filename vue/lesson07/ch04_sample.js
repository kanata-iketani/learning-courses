const numbers = [1, 2, 3, 4, 5];

// map: 全要素を変換した「新しい配列」を作ります
// n => n * 2 は「n を受け取って n * 2 を返す」短い関数です(次レッスンで学びます)
const doubled = numbers.map(n => n * 2);
console.log(doubled);  // [ 2, 4, 6, 8, 10 ]

// filter: 条件に合う要素だけを集めた「新しい配列」を作ります
const evens = numbers.filter(n => n % 2 === 0);
console.log(evens);  // [ 2, 4 ]

// もとの配列は変わりません
console.log(numbers);  // [ 1, 2, 3, 4, 5 ]
