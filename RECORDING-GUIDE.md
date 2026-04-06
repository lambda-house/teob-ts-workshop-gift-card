# Recording & Post-Production Guide

## Pre-Recording Checklist

### Equipment
- [ ] Screen capture: OBS Studio (free) or ScreenFlow (Mac, better editing)
- [ ] Camera: built-in or external webcam, picture-in-picture overlay (bottom-right)
- [ ] Microphone: external mic strongly recommended (even a $30 lapel mic is 10x better than built-in)
- [ ] Lighting: face the window or use a desk lamp — avoid backlit silhouette

### Environment Setup
- [ ] Close all notifications (Do Not Disturb)
- [ ] Set terminal font size to 18pt+ (readable on small screens)
- [ ] Set editor font size to 16pt+
- [ ] Use a clean browser profile (no personal bookmarks visible)
- [ ] Hide desktop icons
- [ ] Prepare terminal with the test commands ready to paste

### Recording Settings
- Resolution: 1920x1080 (not 4K — file size, no benefit for code)
- Frame rate: 30fps
- Audio: separate track for mic (easier to fix in post)
- Format: MP4 / H.264

### Dry Run
- [ ] Record 2 minutes, play back — check audio level, screen readability, camera framing
- [ ] Run both test suites to verify they work on recording machine
- [ ] Verify `npm start` works with solutions in place
- [ ] Verify `public-solution/index.html` loads correctly in browser

---

## Recording Strategy

### Option A: Live Workshop Recording (recommended first pass)

Record the actual workshop. This gives you:
- Natural pacing and audience energy
- Real Q&A moments
- Authentic difficulty calibration

**Post-production:** edit out long silences during exercises, keep the brief/debrief.

### Option B: Studio Recording (for the archive)

Record a tighter version without exercise wait time. Chapters:

| Chapter | Content | Target Duration |
|---------|---------|-----------------|
| 1. Intro | Why DDD + ES, what you'll build | 3 min |
| 2. Architecture | Traditional → Event Sourcing | 5 min |
| 3. Effects & TEOB | Effects, DDD mapping, the core loop | 8 min |
| 4. Exercise 1 Walkthrough | Gift Card aggregate: problem → solution, step by step | 12 min |
| 5. HTTP Demo | npm start → curl commands → live API | 3 min |
| 6. Write vs Read Side | Projections theory | 3 min |
| 7. Exercise 2 Walkthrough | Gift Card projection: problem → solution | 8 min |
| 8. Frontend Generation | AI prompt → working UI | 4 min |
| 9. LLM Demo | ctx.sync() → OpenRouter → encouragement | 4 min |
| 10. Full Picture & Next Steps | Architecture, production path, CTA | 3 min |
| **Total** | | **~53 min** |

Each chapter is a standalone video that can be published separately.

---

## Post-Production

### Editing Priorities
1. **Cut dead air** — pauses > 3 seconds, "um"s, wrong-window moments
2. **Add chapter markers** — in YouTube description and as video chapters
3. **Add code zooms** — if terminal text is small, zoom/crop the relevant area
4. **Lower thirds** — slide title as overlay during live-coding sections

### Chapter Markers Template (for YouTube description)
```
0:00 Introduction — Why DDD + Event Sourcing
3:00 Traditional Architecture vs Event Sourcing
8:00 The TEOB Effect System
13:00 DDD ↔ TEOB: The 1:1 Mapping
18:00 Exercise 1: Gift Card Aggregate (walkthrough)
30:00 Demo: Your Aggregate as an HTTP API
33:00 Write Side vs Read Side
36:00 Exercise 2: Gift Card Projection (walkthrough)
44:00 Exercise 3: AI-Generated Frontend
48:00 Demo: LLM Integration with ctx.sync()
52:00 The Full Picture & Next Steps
```

### Thumbnail
- Dark background, code snippet visible
- Title: "DDD Workshop: Full-Stack Event Sourcing in TypeScript"
- Subtitle: "Hands-on with TEOB"
- Your face if comfortable (thumbnails with faces get higher CTR)

---

## Distribution

### Primary: YouTube (unlisted or public)
- Unlisted for workshop attendees initially
- Public after 1-2 weeks for wider reach
- Add to a "TEOB Workshop Series" playlist

### Secondary
- Embed chapter links in repo README (workshop section)
- Link from exercise HINTS.md ("Watch the walkthrough: [link]")
- Share individual chapters on social media

### Companion Assets Per Chapter
Each chapter gets:
- Direct link with timestamp
- The exercise files it covers
- The relevant slide numbers

---

## Building the Archive

This workshop covers: **Aggregates, Projections, and Full-Stack Service.**

Future episodes to record:

| Episode | Topic | Prerequisites |
|---------|-------|---------------|
| 1 | Aggregates, Projections & Full-Stack | None (this workshop) |
| 2 | Aggregate Communication & Sagas | Episode 1 |
| 3 | Petri Net Flow Modeling | Episode 1 |
| 4 | AI Agents with TEOB | Episode 1 |
| 5 | Production: PostgreSQL & ServiceTemplate | Episodes 1-2 |

Each episode follows the same format:
- Slides (generated from `build-slides.py` pattern)
- 2-3 exercises with progressive hints
- Recorded walkthrough (~50 min studio version)
- README with setup, timeline, and post-workshop challenges
