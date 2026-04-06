# Workshop Slide Deck — Complete Structure

**File:** `slides/DDD-Workshop-Slides.pptx` (32 slides, ~2h45 workshop)
**Build:** `/tmp/pptx-env/bin/python3 slides/build-slides.py`

## Slide Order + Timeline

| #  | Slide | Timing | Type |
|----|-------|--------|------|
| 1  | DDD WITH TEOB (title) | 0:00–0:05 | Opening |
| 2  | WHAT YOU'LL BUILD TODAY | 0:05–0:08 | Framing |
| 3  | QUICK CHECK — SHOW OF HANDS | 0:08–0:10 | Audience calibration |
| 4  | THE ROAD MAP | 0:10–0:12 | Overview |
| 5  | TRADITIONAL ARCHITECTURE | 0:12–0:16 | Theory |
| 6  | WHAT MAKES AN IDEAL BACKEND? | 0:16–0:18 | Theory |
| 7  | COMPLETE BEHAVIOUR: DATA + LOGICS | 0:18–0:20 | Theory |
| 8  | EVENT SOURCING: THE IDEA | 0:20–0:23 | Theory |
| 9  | PURE EVENT SOURCING: THE CORE LOOP | 0:23–0:27 | Theory (core) |
| 10 | EVENT SOURCING: EFFECTS | 0:27–0:30 | Theory (core) |
| 11 | THE EFFECTFUL EVENT LOOP | 0:30–0:33 | **Theory (key diagram)** |
| 12 | THE DDD CORE MAPS 1:1 | 0:33–0:37 | Theory (aha moment) |
| 13 | BEYOND THE BLUE BOOK | 0:37–0:39 | Theory |
| 14 | EVERYTHING IS AN ENTITY | 0:39–0:41 | Theory |
| 15 | EVENT STORMING: DISCOVER THE DOMAIN | 0:41–0:46 | **Event Storming** |
| 16 | GIFT CARD: FROM STICKY NOTES TO CODE | 0:46–0:51 | **Event Storming** |
| 17 | EXERCISE 1: GIFT CARD AGGREGATE | 0:51–0:53 | Exercise brief |
| 18 | EXERCISE 1: AGGREGATE (work screen) | 0:53–1:23 | **Hands-on (30 min)** |
| 19 | EXERCISE 1: DEBRIEF | 1:23–1:28 | Debrief |
| 20 | DEMO: YOUR AGGREGATE AS AN API | 1:28–1:31 | **Live demo** |
| 21 | WHAT JUST HAPPENED? (sequence diagram) | 1:31–1:35 | **Key diagram** |
| 22 | BREAK | 1:35–1:40 | Break (5 min) |
| 23 | WRITE SIDE VS READ SIDE | 1:40–1:45 | Theory |
| 24 | EXERCISE 2: GIFT CARD PROJECTION | 1:45–1:48 | Exercise brief |
| 25 | EXERCISE 2: PROJECTION (work screen) | 1:48–2:08 | **Hands-on (20 min)** |
| 26 | EXERCISE 2: DEBRIEF | 2:08–2:13 | Debrief |
| 27 | EXERCISE 3: AI-GENERATE A FRONTEND | 2:13–2:15 | Exercise brief |
| 28 | EXERCISE 3: FRONTEND (work screen) | 2:15–2:25 | **Hands-on (10 min)** |
| 29 | DEMO: LLM INTEGRATION | 2:25–2:35 | **Live demo** |
| 30 | THE FULL PICTURE (architecture) | 2:35–2:38 | Wrap-up |
| 31 | BATTLE TESTED | 2:38–2:40 | Credibility |
| 32 | WHAT'S NEXT? (CTA) | 2:40–2:45 | Closing |

## Timing Budget

| Section | Duration | Cumulative |
|---------|----------|------------|
| Opening + calibration | 10 min | 0:10 |
| Theory: architecture + ES + effects | 20 min | 0:30 |
| Effectful event loop diagram | 3 min | 0:33 |
| DDD mapping + entities | 8 min | 0:41 |
| Event Storming | 10 min | 0:51 |
| Exercise 1 (aggregate) | 30+5 min | 1:28 |
| Demo: HTTP + sequence diagram | 7 min | 1:35 |
| Break | 5 min | 1:40 |
| Theory: write vs read side | 5 min | 1:45 |
| Exercise 2 (projection) | 20+5 min | 2:13 |
| Exercise 3 (AI frontend) | 2+10 min | 2:25 |
| Demo: LLM integration | 10 min | 2:35 |
| Wrap-up + CTA | 10 min | 2:45 |

## The Five Layers

One domain (gift cards), five capabilities:

1. **Event Storming** — discover events, commands, aggregate, read model (sticky notes)
2. **Exercise: Aggregate** — decide() + invariants (pure functions)
3. **Demo: HTTP Service** — `npm start` → curl commands → live REST API with ctx.sync()
4. **Exercise: Projection** — evolve() read model (pure functions)
5. **Exercise: AI Frontend** — one prompt → working UI from OpenAPI spec
6. **Demo: LLM** — ctx.sync() → OpenRouter → encouragement text

The narrative arc: "Discover the domain → implement it as pure functions → watch it become a full-stack service."
