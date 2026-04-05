# Workshop Marketing & Distribution

## Positioning

**One-liner:** "Build two event-sourced aggregates in TypeScript — from failing tests to working cross-boundary communication in 2 hours."

**Angle:** This is not a lecture. You write code. You leave with working software and a framework you can use Monday morning.

**Target audience:**
- Backend developers who know DDD concepts but haven't implemented ES
- TypeScript developers curious about event sourcing
- Akka/Axon/EventStoreDB users evaluating TypeScript alternatives
- Team leads evaluating frameworks for new projects

---

## Announcement Templates

### LinkedIn / Twitter (short)

```
Building event-sourced systems in TypeScript — hands-on workshop.

You'll implement:
  → A DDD aggregate with invariants (15 tests, red to green)
  → Two aggregates communicating across boundaries

No prior ES experience needed. DDD fundamentals covered.
Everything runs locally. Clone, npm install, start coding.

[date] | [time] | [location/link]
```

### LinkedIn (longer, thought-leadership)

```
Most DDD workshops stop at the whiteboard.

You draw bounded contexts, talk about aggregates, maybe sketch
some events on sticky notes. Then you go back to your codebase
and... nothing changes.

I'm running a hands-on workshop where you'll write actual
event-sourced aggregates in TypeScript:

Exercise 1: Gift Card aggregate
  - Commands, events, state, invariants
  - 15 failing tests → make them green
  - Pure decision functions, no infrastructure

Exercise 2: Order + Payment
  - Two aggregates communicating across boundaries
  - ctx.tell() for fire-and-forget commands
  - ctx.sync() for external system calls with callbacks
  - Integration test: full async flow, zero infrastructure code

The framework (TEOB) maps 1:1 to DDD concepts:
  Aggregate → Aggregate<S,C,E,R>
  Command → type parameter
  decide() → the decision function
  apply() → the state fold
  invariants[] → executable, testable

If you know DDD, you already know the mental model.
If you don't, you'll learn it by writing code.

[date] | [time] | [location/link]
#DDD #EventSourcing #TypeScript
```

### Dev Community / Meetup Description

```
DDD with TEOB — Hands-On Workshop

Level: Intermediate (basic TypeScript required, DDD knowledge helpful but not required)
Duration: ~2 hours
Format: Short theory + two coding exercises
Bring: Laptop with Node.js 20+ installed

What you'll build:
1. A Gift Card aggregate — commands, events, state transitions, and invariants
2. An Order+Payment system — two aggregates communicating across bounded contexts

The TEOB framework provides type-safe, composable abstractions for event sourcing
in TypeScript. Every DDD concept maps 1:1: Aggregate, Command, Event, decide(),
apply(), invariants. What it adds: an Effect type system, actor-model communication,
and runtime-agnostic persistence (same code runs in-memory, SQLite, or PostgreSQL).

Setup before the workshop:
  git clone <repo-url> && cd teob-ts && npm install && npm run build
  npx vitest run workshop/exercise1-gift-card/gift-card.test.ts
  # Should show 13 failing tests — that's your starting point!
```

---

## Shareable Content Assets

### The Mapping Table (standalone image)

The DDD↔TEOB mapping table (slide 11) works as standalone social content.
Export it as a PNG and post with:

```
"If you know DDD, you already know TEOB."

Every concept maps 1:1 — Aggregate, Command, Event, decide, apply, invariants.
The TypeScript types enforce it at compile time.
```

### The Integration Test (wow moment)

Record a 30-second screen capture of the integration test running:
- Two aggregates, full async flow
- Order → Payment → Gateway → Payment → Order
- All happening with ctx.tell() and ctx.sync()

Post with: "Two event-sourced aggregates talking to each other. No HTTP. No message broker. Just ctx.tell()."

### The Before/After

Screenshot: 13 failing tests → 15 passing tests.
"This is what 30 minutes of DDD looks like."

---

## Post-Workshop Follow-Up

### Email Template (send within 24 hours)

```
Subject: Your workshop code + recording + what's next

Hi [name],

Thanks for joining the DDD with TEOB workshop!

Here's everything you need:

📦 Repo: [link] (your exercises are in workshop/)
🎥 Recording: [link] (with chapter markers for each section)
📄 Slides: in the repo at workshop/DDD-Workshop-Slides.pptx

Challenges to try at home:
  - Add a Freeze/Unfreeze command to the Gift Card
  - Create an Inventory aggregate that the Order talks to
  - Try: npx teob new aggregate — scaffold your own from scratch

Questions? Reply to this email or [join community link].

Next workshop: [Episode 2: Projections & Read Models — date TBD]

— Tim
```

### Feedback Survey (3 questions max)

1. "What was the most useful part of the workshop?" (free text)
2. "What would you change?" (free text)
3. "Would you attend Episode 2: Projections?" (Yes / Maybe / No)

Keep it short. Response rate drops off a cliff after 3 questions.

---

## Funnel: Workshop → Framework Adoption

```
Discovery          →  Workshop attendee (free, hands-on)
                        ↓
Engagement         →  Tries exercises at home, stars repo
                        ↓
Exploration        →  Watches Episode 2, reads src/projection/
                        ↓
Adoption           →  Uses TEOB in a side project or proof-of-concept
                        ↓
Production         →  Brings to team, evaluates for real project
```

Each step has a clear next action:
- **After workshop:** "Try the at-home challenges in the README"
- **After challenges:** "Watch Episode 2" / "Run `npx teob new aggregate`"
- **After exploring:** "Deploy to SQLite for a local project" / "Try PostgreSQL runtime"
- **After POC:** "Read src/service/ for production setup"

The workshop is the top of the funnel. The repo + recordings + episodes are the middle.
Production docs and support are the bottom.
