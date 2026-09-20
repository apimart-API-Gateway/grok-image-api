# Grok Image API (grok-imagine-1.5-apimart)

<!-- conv-kit:v1 -->

<p align="center">
  <img src="assets/badges/price.svg" alt="observed unit price"> <img src="assets/badges/billing.svg" alt="billing model"> <img src="assets/badges/compat.svg" alt="OpenAI-compatible endpoint">
</p>

<p align="center">
  <img src="assets/03-product-cosmetics-duo.jpg" width="820" alt="Grok Imagine 1.5 (grok-imagine-1.5-apimart) output generated through APIMart">
</p>

> **$0.015 per image**, edits included — one OpenAI-compatible endpoint at `https://api.apimart.ai/v1`, no monthly plan required. *(observed 2026-09-17)*

**[Get an API key](https://go.apimart.ai/k-a96fe3)** · **[Live pricing](https://go.apimart.ai/k-4f6dcd)** · **[Model page](https://go.apimart.ai/k-1a274e)** · [⚡ 60-second quickstart](#quickstart)

**Why teams call Grok Imagine 1.5 (`grok-imagine-1.5-apimart`) through APIMart**

- **One key, entire catalog.** The same `https://api.apimart.ai/v1` base URL and `Authorization` header reach Grok Imagine 1.5 (`grok-imagine-1.5-apimart`) and 300+ other image, video and language models — switch the `model` field, not your client.
- **$1 minimum, pay as you go.** No subscription and no prepaid plan to size up front: top up from $1 and spend it on calls. There is no free quota to burn through first, so the price in this table is the price you pay.
- **The charge comes back in the response.** Every call reports the amount billed (`cost` / `credits_cost`), so a spend number is read per call instead of guessed at month end.
- **Async by design.** Submit, take the `task_id`, poll `GET /v1/tasks/{id}` — batching and retries are ordinary queue work, not a bespoke integration.

<!-- /conv-kit:v1 -->

Grok Image on APIMart is the async Grok Imagine route: text-to-image plus reference-based editing, five aspect ratios, and up to 10 images per request — the batch behaviour is the unusual part.

## Model id and routes

| Route | `model` value | Billing | Notes |
| --- | --- | --- | --- |
| Per-image (default here) | `grok-imagine-1.5-apimart` | per delivered image, by resolution | alias `grok-imagine-1.5-ext` is documented as equivalent |
| Token-billed official | `` | per million tokens | no `official_fallback` on this id |

Endpoint: `POST https://api.apimart.ai/v1/images/generations` (OpenAI-compatible), then poll `GET /v1/tasks/{task_id}`.
Result links are valid for 24 hours.

## Pricing

<!-- pricing:model:start -->
| Output | List price | Effective price |
| --- | --- | --- |
| default | $0.0187 | $0.015 |

<!-- conv-kit:v1:scale -->
### What that costs at scale

| Spend | Cost |
| --- | --- |
| 100 images | $1.50 |
| 1000 images | $15.00 |
| 10000 images | $150.00 |

Linear at the observed per-unit rate, no volume discount assumed. Snapshot 2026-09-17; re-check the live table before committing a budget.
<!-- /conv-kit:v1:scale -->


<!-- pricing:model:end -->

Prices are a snapshot; the [pricing page](https://go.apimart.ai/k-4f6dcd) and [`data/model.json`](data/model.json) are refreshed by
CI, and a completed task reports the exact amount in its `cost` field.

## Request parameters

| Field | Type | Default | Notes |
| --- | --- | --- | --- |
| `model` | string | required | `grok-imagine-1.5-apimart` (alias `grok-imagine-1.5-ext`); the sibling ids `grok-imagine-image` and `grok-imagine-image-quality` are documented on the same endpoint |
| `prompt` | string | required | supports multiple languages; describes the image or the edit |
| `size` | string | `1:1` | `1:1`, `16:9`, `9:16`, `3:2`, `2:3` |
| `n` | integer | `1` | **1–10 images per request** on this route; must be a plain number |
| `image_urls` | string[] | — | 1–5 publicly reachable reference URLs for editing; local files must be uploaded first |
| `nsfw_check` | boolean | `false` | runs `omni-moderation-latest` before submitting |

Supported aspect ratios: `1:1`, `16:9`, `9:16`, `3:2`, `2:3`.

## Quickstart

```bash
curl --request POST --url https://api.apimart.ai/v1/images/generations \
  --header "Authorization: Bearer $APIMART_API_KEY" --header 'Content-Type: application/json' \
  -d '{"model":"grok-imagine-1.5-apimart","prompt":"A bamboo forest path under moonlight","size":"1:1","resolution":"1K","n":1}'
```

```python
import os, time, requests

BASE = "https://api.apimart.ai/v1"
HEADERS = {"Authorization": f"Bearer {os.environ['APIMART_API_KEY']}", "Content-Type": "application/json"}

created = requests.post(f"{BASE}/images/generations", headers=HEADERS, timeout=60, json={
    "model": "grok-imagine-1.5-apimart", "prompt": "A bamboo forest path under moonlight",
    "size": "1:1", "resolution": "1K", "n": 1,
}).json()
task_id = created["data"]["id"]

while True:
    task = requests.get(f"{BASE}/tasks/{task_id}", headers=HEADERS, timeout=60).json()["data"]
    if task["status"] in ("completed", "failed"):
        break
    time.sleep(5)
print(task.get("cost"), task.get("result", {}).get("images", [{}])[0].get("url"))
```

```javascript
const res = await fetch("https://api.apimart.ai/v1/images/generations", {
  method: "POST",
  headers: { Authorization: `Bearer ${process.env.APIMART_API_KEY}`, "Content-Type": "application/json" },
  body: JSON.stringify({ model: "grok-imagine-1.5-apimart", prompt: "A bamboo forest path under moonlight",
                          size: "1:1", resolution: "1K", n: 1 }),
});
const { data } = await res.json();      // data.id is the task id — poll /v1/tasks/<id>
```

Runnable versions: [`examples/`](examples). The task lifecycle is `pending → processing → completed | failed`, and the
finished task carries `cost`, `credits_cost` and expiring result URLs.

## Sample outputs

Every render below came from a single call with the model id above, at the ratio shown; the cost column is what the task
reported.

| Output | Recipe | Ratio | Cost | Prompt |
| --- | --- | --- | --- | --- |
| <img src="assets/03-product-cosmetics-duo.jpg" width="220" alt="Grok Image sample output"> | Product | 1:1 | $0.015 | `Two frosted glass cosmetics bottles on a pale sand surface, hard afternoon light casting long shadows, minimal styling, commercial product photography` |
| <img src="assets/01-cyberpunk-motorbike.jpg" width="220" alt="Grok Image sample output"> | Cinematic | 16:9 | $0.015 | `Cyberpunk motorbike parked in a neon-lit underpass, rain on asphalt, magenta and cyan rim lights, cinematic still, shallow depth of field` |
| <img src="assets/02-mythic-creature-concept.jpg" width="220" alt="Grok Image sample output"> | Concept art | 3:2 | $0.015 | `Mythic forest creature concept art, antlered guardian covered in moss and small flowers, soft volumetric light through trees, painterly detail` |
| <img src="assets/04-retro-poster-travel.jpg" width="220" alt="Grok Image sample output"> | Poster / graphic | 3:4 | $0.015 | `Retro travel poster illustration of a coastal train route, flat colour blocks, textured paper grain, warm sunset palette, bold graphic composition` |
| <img src="assets/05-gourmet-dessert.jpg" width="220" alt="Grok Image sample output"> | Food | 4:3 | $0.015 | `Gourmet chocolate dessert with gold leaf on a dark ceramic plate, moody side light, shallow depth of field, fine dining food photography` |
| <img src="assets/06-fantasy-city-aerial.jpg" width="220" alt="Grok Image sample output"> | Environment | 16:9 | $0.015 | `Aerial view of a fantasy cliff city carved into stone terraces above a turquoise sea, tiny bridges and hanging gardens, cinematic haze, epic scale` |

Recipes and measured costs are also in [`data/samples.json`](data/samples.json).

<!-- conv-kit:v1:fix -->
## First-call troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `401` / `invalid api key` | key missing, truncated, or a stray newline pasted into the header | Re-copy it from the console; the header is `Authorization: Bearer $APIMART_API_KEY` |
| balance / credit error | the account has no balance | Top up from $1 in the console — there is no free quota to fall back on |
| `429` | concurrent requests on one key | Back off, then retry the same request with the same `Idempotency-Key` |
| `400` / model not found | wrong route for the id: the per-unit alias needs its `version`, the official id must not send one | Copy the exact `model` value from the route table above |
| task ends `failed` | prompt rejected by the filter, or a reference image URL expired | Re-submit with a **new** `Idempotency-Key` and re-host the reference image |
| result URL stops working | result links expire | Download the file as soon as the task reports `completed` |
<!-- /conv-kit:v1:fix -->

## FAQ

**What is the Grok Image API model id?**

`grok-imagine-1.5-apimart`, with the documented alias `grok-imagine-1.5-ext`. The endpoint also documents `grok-imagine-image` and `grok-imagine-image-quality`.

**Can I get several images in one request?**

Yes — this route accepts `n` from 1 to 10, which makes it the cheapest way to explore variations. Most other image routes cap `n` at 1, so fan-out there has to happen client-side.

**How does editing work?**

Pass 1–5 publicly reachable image URLs in `image_urls` and describe the change in `prompt`. Only absolute http(s) URLs are accepted, so upload local files to your own storage first.

**How long do result links last?**

Generated links are valid for 24 hours; download and store the output as part of the job.

## Related searches

- `grok image api`
- `grok imagine api`
- `grok image api pricing`
- `grok imagine api key`
- `grok image editing api`
- `image generation api`
- `ai image api`

<!-- conv-kit:v1:cta -->
---

**Start with $1.** [Get an API key](https://go.apimart.ai/k-a96fe3) → [check live pricing](https://go.apimart.ai/k-4f6dcd) → [open Grok Imagine 1.5 (`grok-imagine-1.5-apimart`) in the model library](https://go.apimart.ai/k-1a274e). The first call is three steps: submit, poll `task_id`, read the charged amount off the response.
<!-- /conv-kit:v1:cta -->

## Attributed links (how this repository is measured)

| Purpose | Attributed link | Target |
| --- | --- | --- |
| Open Grok Image on APIMart | <https://go.apimart.ai/k-1a274e> | `docs.apimart.ai` model page |
| Current pricing page | <https://go.apimart.ai/k-4f6dcd> | `apimart.ai/pricing` |
| Get an API key | <https://go.apimart.ai/k-a96fe3> | `apimart.ai/keys` |

Outbound APIMart links are minted through the promo link API; hand-made tracking parameters are rejected by
`tools/check_links.py` in CI.

## Disclosure

Grok Image is a third-party model served through APIMart; this repository documents how to call it and publishes
real outputs, model ids and prices, and does not claim official status. Model names, prices and documentation belong to
their respective owners. Endpoint reference: [https://docs.apimart.ai/en/api-reference/images/grok-imagine/generation](https://docs.apimart.ai/en/api-reference/images/grok-imagine/generation).

## Repository map

```text
README.md             model id, pricing, parameters, quickstart, samples, FAQ
data/model.json       the pricing record for this model (CI-refreshed)
data/samples.json     prompt recipes with measured cost
tools/snapshot.py     refresh this model's prices from the public pricing payload
tools/check_links.py  attribution guard
examples/             curl, Python and JavaScript clients
assets/               real sample renders (JPEG, resized for the README)
.github/workflows/    daily price refresh + validation
```

## License

MIT — see [LICENSE](LICENSE).
