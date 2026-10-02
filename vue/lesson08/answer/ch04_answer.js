const items = ["ペン", "ノート", "消しゴム"];
// forEach に渡したアロー関数がコールバックです。要素と添字が順に届きます
// index は 0 始まりなので、表示用に 1 を足します
items.forEach((item, index) => {
  console.log(`${index + 1}: ${item}`);
});
