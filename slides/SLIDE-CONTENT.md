# Workshop Slide Deck — Complete Structure

**File:** `slides/DDD-Workshop-Slides.pptx` (28 slides, ~2h30 workshop)
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
| 11 | THE DDD CORE MAPS 1:1 | 0:30–0:35 | Theory (aha moment) |
| 12 | BEYOND THE BLUE BOOK | 0:35–0:38 | Theory |
| 13 | EVERYTHING IS AN ENTITY | 0:38–0:40 | Theory |
| 14 | EXERCISE 1: GIFT CARD AGGREGATE | 0:40–0:42 | Exercise brief |
| 15 | EXERCISE 1: AGGREGATE (work screen) | 0:42–1:12 | **Hands-on (30 min)** |
| 16 | EXERCISE 1: DEBRIEF | 1:12–1:17 | Debrief |
| 17 | DEMO: YOUR AGGREGATE AS AN API | 1:17–1:22 | **Live demo** |
| 18 | BREAK | 1:22–1:27 | Break (5 min) |
| 19 | WRITE SIDE VS READ SIDE | 1:27–1:32 | Theory |
| 20 | EXERCISE 2: GIFT CARD PROJECTION | 1:32–1:35 | Exercise brief |
| 21 | EXERCISE 2: PROJECTION (work screen) | 1:35–1:55 | **Hands-on (20 min)** |
| 22 | EXERCISE 2: DEBRIEF | 1:55–2:00 | Debrief |
| 23 | EXERCISE 3: AI-GENERATE A FRONTEND | 2:00–2:02 | Exercise brief |
| 24 | EXERCISE 3: FRONTEND (work screen) | 2:02–2:12 | **Hands-on (10 min)** |
| 25 | DEMO: LLM INTEGRATION | 2:12–2:22 | **Live demo** |
| 26 | THE FULL PICTURE | 2:22–2:25 | Wrap-up |
| 27 | BATTLE TESTED | 2:25–2:27 | Credibility |
| 28 | WHAT'S NEXT? (CTA) | 2:27–2:30 | Closing |

## Timing Budget

| Section | Duration | Cumulative |
|---------|----------|------------|
| Opening + calibration | 10 min | 0:10 |
| Theory: architecture + ES + effects | 20 min | 0:30 |
| DDD ↔ TEOB mapping | 10 min | 0:40 |
| Exercise 1 (aggregate) | 30+5 min | 1:17 |
| Demo: HTTP service | 5 min | 1:22 |
| Break | 5 min | 1:27 |
| Theory: write vs read side | 5 min | 1:32 |
| Exercise 2 (projection) | 20+5 min | 2:00 |
| Exercise 3 (AI frontend) | 2+10 min | 2:12 |
| Demo: LLM integration | 10 min | 2:22 |
| Wrap-up + CTA | 8 min | 2:30 |

## The Four Layers

One domain (gift cards), five capabilities:

1. **Exercise: Aggregate** — decide() + invariants (pure functions)
2. **Demo: HTTP Service** — `npm start` → curl commands → live API
3. **Exercise: Projection** — evolve() read model (pure functions)
4. **Exercise: AI Frontend** — one prompt → working UI on your API
5. **Demo: LLM** — ctx.sync() → OpenRouter → encouragement text

The narrative arc: "Three pure functions — decide, apply, evolve — that's the whole model. Then AI writes your frontend."
