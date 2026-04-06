# DDD with TEOB — Gift Card Workshop

Build a complete event-sourced gift card service in TypeScript.
Pure functions all the way: `decide()` for commands, `evolve()` for read models,
`apply()` for state — the same pattern at every layer.

## Prerequisites

- **Node.js** 20+ (`node -v`)
- A code editor with TypeScript support

## Setup

```bash
git clone https://github.com/lambda-house/teob-ts-workshop-gift-card.git
cd teob-ts-workshop-gift-card
npm install
```

Verify:
```bash
npm run test:aggregate
# Should see 14 failing tests and 2 passing — that's your starting point!
```

## Workshop Flow

### Exercise 1: Gift Card Aggregate (30 min)

Implement the decision function and invariants.

**File:** `src/domain/aggregate.ts` — fill in the `decide` cases and `invariants`

```bash
npm run test:aggregate          # 16 tests — make them green
npm run test:aggregate:watch    # same, re-runs on save
```

Suggested order: `Issue` → `GetBalance` → `Redeem` → `Cancel` → Invariants

Stuck? See `HINTS-aggregate.md` (4 progressive levels) or `src/domain/aggregate.solution.ts`

### Demo: HTTP Service

> **Note:** `npm start` runs your exercise code — finish Exercise 1 first.

Watch your aggregate become an API:

```bash
npm start
```

```bash
curl -s -X POST http://localhost:3000/api/gift-card/card-1 \
  -H "Content-Type: application/json" \
  -d '{"tag":"Issue","amount":100,"recipientName":"Alice"}'

curl -s -X POST http://localhost:3000/api/gift-card/card-1 \
  -H "Content-Type: application/json" \
  -d '{"tag":"GetBalance"}'
```

### Exercise 2: Gift Card Projection (20 min)

Build the read model — same pure function pattern, now for queries.

**File:** `src/domain/projection.ts` — fill in the `evolve` cases

```bash
npm run test:projection          # 8 tests — make them green
npm run test:projection:watch    # same, re-runs on save
```

Stuck? See `HINTS-projection.md` (4 levels) or `src/domain/projection.solution.ts`

### Exercise 3: AI-Generate a Frontend (10 min)

Your service now has both write and read APIs. Use your AI coding agent to
generate a frontend with a single prompt.

Open `PROMPT-frontend.md`, copy the prompt into your agent (Claude Code, Cursor, etc.),
and let it generate `public/index.html`. Then:

```bash
npm start
open http://localhost:3000
```

Reference solution: `public-solution/index.html`

### Demo: LLM Integration

Watch the aggregate call an LLM to generate personalized encouragement:

```bash
OPENROUTER_API_KEY=sk-... npm run demo:llm
```

Same `ctx.sync()` pattern you'd use for any external call — payment gateway,
shipping API, anything. Event sourcing gives you retry, replay, and audit trail
for the LLM interaction.

## Key Concepts

```
decide(state, command) → Effect     — business logic, pure function
apply(state, event)    → State      — state fold, pure function
evolve(view, event)    → View       — read model, pure function
```

Three pure functions. That's the whole model.

```
persist(event)              — store event in journal
reply(value)                — respond to caller
andReply(persist, reply)    — persist + reply atomically
andRun(persist, sideEffect) — persist, then run async effect
```

## After the Workshop

- Add a `Freeze` / `Unfreeze` command with a new invariant
- Add `transactionHistory` to the projection view
- Try `npx teob new aggregate` to scaffold your own
- Explore: projections (`@lambda-house/teob-ts/projection`), sagas (`/saga`), Petri nets (`/petrinet`)

## Project Structure

```
src/
├── domain/
│   ├── types.ts                 # Domain types (given)
│   ├── aggregate.ts             # Exercise 1: implement decide + invariants
│   ├── aggregate.solution.ts    # Reference solution
│   ├── projection.ts            # Exercise 2: implement evolve
│   └── projection.solution.ts   # Reference solution
└── service/
    ├── server.ts                # HTTP service (write + read + static)
    └── llm-demo.ts              # LLM integration demo
public/                          # Exercise 3: AI-generated frontend goes here
public-solution/                 # Reference frontend solution
PROMPT-frontend.md               # Prompt for AI coding agent
ARCHITECTURE.md                  # Service architecture diagram
```
