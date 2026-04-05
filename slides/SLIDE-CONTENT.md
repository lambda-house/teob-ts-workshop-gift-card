# Workshop Slide Deck — Complete Structure

**File:** `DDD-Workshop-Slides.pptx` (26 slides, ~2h workshop)
**Build:** `/tmp/pptx-env/bin/python3 workshop/build-slides.py`

All slides have presenter notes with timing cues, audience interaction prompts,
and what to say/demo at each point.

---

## Complete Slide Order + Timeline

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
| 9  | STREAM OF UPDATES: PURE EVENT SOURCING | 0:23–0:27 | Theory (core) |
| 10 | EVENT SOURCING: EFFECTS | 0:27–0:30 | Theory (core) |
| 11 | THE DDD CORE MAPS 1:1 | 0:30–0:35 | Theory (aha moment) |
| 12 | BEYOND THE BLUE BOOK | 0:35–0:38 | Theory |
| 13 | EVERYTHING IS AN ENTITY | 0:38–0:40 | Theory |
| 14 | EXERCISE 1: GIFT CARD AGGREGATE | 0:40–0:42 | Exercise brief |
| 15 | EXERCISE 1: GIFT CARD (work screen) | 0:42–1:12 | **Hands-on (30 min)** |
| 16 | EXERCISE 1: DEBRIEF | 1:12–1:17 | Debrief |
| 17 | BREAK | 1:17–1:22 | Break (5 min) |
| 18 | HOW DO AGGREGATES TALK? | 1:22–1:30 | Theory |
| 19 | EXERCISE 2: ORDER + PAYMENT | 1:30–1:35 | Exercise brief |
| 20 | EXERCISE 2: ORDER + PAYMENT (work screen) | 1:35–2:10 | **Hands-on (35 min)** |
| 21 | EXERCISE 2: DEBRIEF | 2:10–2:17 | Debrief |
| 22 | THE FULL PICTURE: BACKEND SERVICE | 2:17–2:20 | Wrap-up |
| 23 | BATTLE TESTED | 2:20–2:22 | Credibility |
| 24 | DSL- AND AI-FRIENDLY | 2:22–2:24 | Optional |
| 25 | TEOB AGENTIC PLATFORM | 2:24–2:26 | Optional teaser |
| 26 | WHAT'S NEXT? (CTA) | 2:26–2:30 | Closing |

---

## Timing Budget

| Section | Duration | Cumulative |
|---------|----------|------------|
| Opening + calibration | 10 min | 0:10 |
| Theory: architecture + ES + effects | 20 min | 0:30 |
| DDD ↔ TEOB mapping | 10 min | 0:40 |
| Exercise 1 brief | 2 min | 0:42 |
| Exercise 1 work | 30 min | 1:12 |
| Exercise 1 debrief | 5 min | 1:17 |
| Break | 5 min | 1:22 |
| Aggregate communication theory | 8 min | 1:30 |
| Exercise 2 brief | 5 min | 1:35 |
| Exercise 2 work | 35 min | 2:10 |
| Exercise 2 debrief | 7 min | 2:17 |
| Wrap-up + CTA | 13 min | 2:30 |

---

## Key Presenter Notes

### Opening (Slide 1)
Before any slides, ask the room: "What broke in your last distributed system?"
Let 2–3 people share. This primes them for why DDD + ES matters.

### Audience Calibration (Slide 3)
This determines your depth. If most have DDD experience, skip basics and go deeper
on TEOB specifics. If Akka/Axon users are present, draw parallels throughout.

### The Aha Moment (Slide 11)
The DDD→TEOB mapping table. Go row by row. "If you know DDD, you already know TEOB."
Pause here for questions before moving to Exercise 1.

### Exercise 1 Checkpoints (Slide 15)
- At 15 min: "How many tests green? Show of hands: more than 5?"
- At 15 min: Show Hint 1 if needed
- At 25 min: Live-code the Issue case if people are stuck
- At 28 min: "2 minutes — don't worry if you haven't finished"

### Exercise 2 Checkpoints (Slide 20)
- At 10 min: "Who has GetStatus passing?"
- At 15 min: Show Hint 2 (ctx.sync pattern)
- At 25 min: Live-code ChargeSucceeded if many stuck
- At 30 min: "Focus on unit tests. Integration tests are a bonus."

### The Wow Moment (Slide 21)
Run the integration test LIVE. Show two aggregates communicating in real time.
"All of this happened with fire-and-forget commands. No HTTP, no message broker."

### Closing (Slide 26)
"You just built two event-sourced aggregates with cross-boundary communication.
That's not a demo — that's the real pattern."

---

## Rebuilding the Slides

The PPTX is generated programmatically. To modify:

1. Edit `workshop/build-slides.py`
2. Run: `/tmp/pptx-env/bin/python3 workshop/build-slides.py`
3. Open the regenerated PPTX

Theme constants are at the top of the script:
- `BG_LIGHT = #ECECEC` (light slides)
- `BG_DARK = #1E1E2E` (work time + break + closing)
- `COLOR_BLUE = #2266AA` (accent, TEOB concepts)
- `COLOR_GREEN = #66BB6A` (exercises, success)
- `COLOR_ORANGE = #FFA726` (infrastructure, warnings)

For visual polish, import into Keynote and replace text-only theory slides
with corresponding slides from `~/Dropbox/TEOB.key` (which has rich diagrams).
