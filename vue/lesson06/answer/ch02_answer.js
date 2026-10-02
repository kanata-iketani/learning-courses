let total = 0;
let i = 0;
// 「何回で超えるか」が事前にわからないので while (true) + break で書きます
while (true) {
  i++;
  total = total + i;
  if (total > 20) {
    break;  // 20 を超えた瞬間にループを抜けます
  }
}
console.log(i);
console.log(total);
