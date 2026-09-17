// Grok Image (grok-imagine-1.5-apimart) from Node 18+: submit, poll, print the cost.
const BASE = process.env.APIMART_BASE_URL ?? "https://api.apimart.ai/v1";
const headers = { Authorization: `Bearer ${process.env.APIMART_API_KEY}`, "Content-Type": "application/json" };
const sleep = ms => new Promise(r => setTimeout(r, ms));

export async function generate(prompt, { size = "1:1", resolution = "1K" } = {}) {
  const created = await fetch(`${BASE}/images/generations`, {
    method: "POST", headers,
    body: JSON.stringify({ model: "grok-imagine-1.5-apimart", prompt, size, resolution, n: 1 }),
  });
  if (!created.ok) throw new Error(`submit failed: ${created.status} ${await created.text()}`);
  const { data } = await created.json();
  let delay = 3000;
  for (let waited = 0; waited < 600000; waited += delay) {
    const task = (await (await fetch(`${BASE}/tasks/${data.id}`, { headers })).json()).data;
    if (task.status === "completed" || task.status === "failed") return task;
    await sleep(delay);
    delay = Math.min(delay * 2, 10000);
  }
  throw new Error(`timeout: ${data.id}`);
}

if (process.argv[1]?.endsWith("javascript.mjs")) {
  const task = await generate(process.argv[2] ?? "A bamboo forest path under moonlight");
  console.log("status:", task.status, "cost:", task.cost, "urls:", task.result?.images?.[0]?.url);
}
