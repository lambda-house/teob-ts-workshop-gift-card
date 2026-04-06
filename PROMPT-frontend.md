# AI Coding Agent Prompt — Gift Card Frontend

Copy this prompt into your AI coding agent (Claude Code, Cursor, Copilot, etc.)
to generate a frontend for the service you just built.

---

## The Prompt

> Build a single-page gift card management UI in `public/index.html`.
> Vanilla HTML/CSS/JS only — no frameworks, no build tools.
>
> The server already serves static files from `public/` and has these endpoints:
>
> **Write (commands):**
> - `POST /api/gift-card/:entityId` — body: `{ tag: "Issue", amount: N, recipientName: "..." }`
> - `POST /api/gift-card/:entityId` — body: `{ tag: "Redeem", amount: N }`
> - `POST /api/gift-card/:entityId` — body: `{ tag: "Cancel" }`
> - `POST /api/gift-card/:entityId` — body: `{ tag: "GetBalance" }`
>
> **Read (projections):**
> - `GET /api/gift-card/:entityId/view` — returns `{ balance, status, recipientName?, encouragement?, transactionCount }`
> - `GET /api/gift-cards` — returns `[{ id, balance, status, recipientName?, encouragement?, transactionCount }]`
>
> The UI should:
> 1. Show a grid of all gift cards, auto-refreshing from `GET /api/gift-cards`
> 2. Let users issue a new card (card ID, amount, recipient name)
> 3. Let users select a card and redeem, cancel, or check balance
> 4. Show card status visually: Active = green, Empty = grey, Cancelled = red
> 5. Show encouragement text and transaction count when present
>
> Make it look like a developer tool — clean, dark theme, monospace for IDs and amounts.

---

After the agent generates the file, start the server and open the browser:

```bash
npm start
open http://localhost:3000
```

A reference solution is available in `public-solution/index.html` if you want to compare.
