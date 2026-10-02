const score = 65;

// Python の elif は else if と書きます(上から順に判定されます)
if (score >= 80) {
  console.log("優");
} else if (score >= 60) {
  console.log("良");
} else {
  console.log("がんばろう");
}

// && は「かつ」(Python の and)、|| は「または」(Python の or)
const age = 25;
const hasTicket = true;
if (age >= 18 && hasTicket) {
  console.log("入場できます");
}

const day = "日";
if (day === "土" || day === "日") {
  console.log("休みです");
}
