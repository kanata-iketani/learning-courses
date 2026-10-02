// 面積を「表示する」のではなく「返す」ことで、結果を自由に使い回せます
function rectangleArea(width, height) {
  return width * height;
}

// 戻り値をそのまま console.log に渡して表示します
console.log(rectangleArea(3, 5));
console.log(rectangleArea(10, 10));
