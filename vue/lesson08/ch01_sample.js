// Python:
// def greet():
//     print("こんにちは")
function greet() {
  console.log("こんにちは");
}

// 定義しただけでは動きません。呼び出して初めて実行されます
greet();
greet();  // 何度でも呼べます

// 複数行の処理もまとめられます
function showMenu() {
  console.log("--- メニュー ---");
  console.log("1. コーヒー");
  console.log("2. 紅茶");
}
showMenu();
