#!/usr/bin/env python3
"""
Build the complete DDD Workshop PPTX deck.
Run: /tmp/pptx-env/bin/python3 slides/build-slides.py
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── Theme constants ───────────────────────────────────────────────────────

BG_LIGHT = RGBColor(0xEC, 0xEC, 0xEC)
BG_DARK = RGBColor(0x1E, 0x1E, 0x2E)

COLOR_DARK = RGBColor(0x22, 0x22, 0x22)
COLOR_BLUE = RGBColor(0x22, 0x66, 0xAA)
COLOR_GREEN = RGBColor(0x66, 0xBB, 0x6A)
COLOR_RED = RGBColor(0xEF, 0x53, 0x50)
COLOR_GRAY = RGBColor(0x44, 0x44, 0x44)
COLOR_LIGHT_GRAY = RGBColor(0x88, 0x88, 0x88)
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
COLOR_ORANGE = RGBColor(0xFF, 0xA7, 0x26)
COLOR_PURPLE = RGBColor(0x9C, 0x27, 0xB0)

SLIDE_W = 12191695
SLIDE_H = 6858000

M_LEFT = Emu(731520)
M_TOP = Emu(548640)
M_RIGHT = Emu(731520)
CONTENT_W = SLIDE_W - M_LEFT - M_RIGHT

prs = Presentation()
prs.slide_width = SLIDE_W
prs.slide_height = SLIDE_H
BLANK_LAYOUT = prs.slide_layouts[6]


# ── Helpers ────────────────────────────────────────────────────────────────

def set_bg(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_text(slide, left, top, width, height, text, font_size=18, bold=False,
             color=COLOR_DARK, font_name=None, alignment=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    if font_name:
        p.font.name = font_name
    p.alignment = alignment
    return txBox

def add_title(slide, text, color=COLOR_DARK, font_size=36):
    add_text(slide, M_LEFT, M_TOP, CONTENT_W, Emu(800000),
             text, font_size=font_size, bold=True, color=color)

def add_bullet_block(slide, items, top, color=COLOR_DARK, font_size=18,
                     bold=False, spacing=Emu(380000), left=None, width=None):
    if left is None:
        left = M_LEFT
    if width is None:
        width = CONTENT_W
    for i, item in enumerate(items):
        y = top + i * spacing
        prefix = "• " if not item.startswith(("─", "→", " ", "•")) else ""
        add_text(slide, left, y, width, spacing,
                 f"{prefix}{item}", font_size=font_size, bold=bold, color=color)

def add_code_box(slide, text, left, top, width, height, font_size=14):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0x2D, 0x2D, 0x2D)
    shape.line.fill.background()
    shape.adjustments[0] = 0.02
    tf = shape.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.margin_left = Pt(16)
    tf.margin_top = Pt(12)
    tf.margin_right = Pt(16)
    tf.margin_bottom = Pt(12)
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = COLOR_WHITE
    p.font.name = "SF Mono"
    return shape

def add_accent_line(slide, top, width=None, color=COLOR_BLUE):
    if width is None:
        width = CONTENT_W
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, M_LEFT, top, width, Emu(36000))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def add_box(slide, left, top, width, height, fill_color, text="",
            font_size=16, text_color=COLOR_WHITE, bold=True):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    shape.adjustments[0] = 0.05
    tf = shape.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = text_color
    p.font.bold = bold
    p.alignment = PP_ALIGN.CENTER
    return shape

def add_arrow(slide, left, top, width, height, color=COLOR_GRAY):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RIGHT_ARROW, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def add_notes(slide, text):
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = text


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 1: Title
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_accent_line(slide, Emu(2600000))
add_text(slide, M_LEFT, Emu(2800000), CONTENT_W, Emu(1200000),
         "DDD WITH TEOB", font_size=54, bold=True, color=COLOR_DARK)
add_text(slide, M_LEFT, Emu(4000000), CONTENT_W, Emu(600000),
         "Hands-On Workshop: Event-Sourced Aggregates in TypeScript",
         font_size=22, color=COLOR_GRAY)
add_text(slide, M_LEFT, Emu(5200000), CONTENT_W, Emu(400000),
         "Tim Evdokimov", font_size=18, color=COLOR_LIGHT_GRAY)
add_notes(slide,
    "TIMING: 0:00–0:05\n"
    "Welcome everyone. Before slides — ask the room:\n"
    "\"What broke in your last distributed system?\"\n"
    "Let 2-3 people share war stories. This primes them for why DDD + ES matters.\n"
    "Then: \"Today you'll build a complete event-sourced gift card service.\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 2: What You'll Build
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "WHAT YOU'LL BUILD TODAY")
add_accent_line(slide, Emu(1200000))

items = [
    ("1", "A DDD aggregate", "commands, events, state, invariants — pure functions", COLOR_BLUE),
    ("2", "An HTTP service", "your aggregate becomes a live API in one line", COLOR_BLUE),
    ("3", "A read model", "project events into query-optimized views", COLOR_GREEN),
    ("4", "LLM integration", "ctx.sync() calls OpenRouter — same pattern as any external API", COLOR_PURPLE),
]
for i, (num, title, subtitle, color) in enumerate(items):
    y = Emu(1600000 + i * 1250000)
    add_box(slide, M_LEFT, y, Emu(700000), Emu(700000), color,
            text=num, font_size=32, text_color=COLOR_WHITE)
    add_text(slide, Emu(1700000), y + Emu(50000), Emu(9000000), Emu(400000),
             title, font_size=24, bold=True, color=COLOR_DARK)
    add_text(slide, Emu(1700000), y + Emu(400000), Emu(9000000), Emu(300000),
             subtitle, font_size=16, color=COLOR_GRAY)

add_notes(slide,
    "TIMING: 0:05–0:08\n"
    "\"One domain — gift cards. Four layers of capability.\"\n"
    "\"You'll write code for 1 and 3. I'll demo 2 and 4.\"\n"
    "\"By the end you'll have a running HTTP service with AI integration.\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 3: Audience Calibration
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "QUICK CHECK — SHOW OF HANDS")
add_accent_line(slide, Emu(1200000))

questions = [
    "Who has implemented a DDD aggregate before?",
    "Who has worked with event sourcing in production?",
    "Who writes TypeScript regularly?",
    "Who has used Akka, Axon, or EventStoreDB?",
]
for i, q in enumerate(questions):
    y = Emu(1700000 + i * 900000)
    add_text(slide, Emu(1000000), y, Emu(10000000), Emu(600000),
             f"✋  {q}", font_size=22, color=COLOR_DARK)

add_notes(slide,
    "TIMING: 0:08–0:10\n"
    "This calibrates your depth.\n"
    "If most have DDD experience → skip basics, go deeper on TEOB specifics.\n"
    "If Akka/Axon users → draw parallels throughout."
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 4: Road Map
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "THE ROAD MAP")
add_accent_line(slide, Emu(1200000))

stages = [
    ("Theory:\nArchitecture\n→ ES", COLOR_LIGHT_GRAY, "20 min"),
    ("DDD ↔ TEOB\nMapping", COLOR_BLUE, "10 min"),
    ("Exercise 1:\nAggregate", COLOR_GREEN, "30 min"),
    ("Demo:\nHTTP Service", COLOR_BLUE, "10 min"),
    ("Exercise 2:\nProjection", COLOR_GREEN, "20 min"),
    ("Demo:\nLLM", COLOR_PURPLE, "10 min"),
    ("Full Picture\n& Next Steps", COLOR_ORANGE, "10 min"),
]
box_w = Emu(1400000)
gap = Emu(100000)
start_x = Emu(400000)
for i, (label, color, time) in enumerate(stages):
    x = start_x + i * (box_w + gap)
    add_box(slide, x, Emu(2200000), box_w, Emu(1800000), color,
            text=label, font_size=12, text_color=COLOR_WHITE)
    add_text(slide, x, Emu(4200000), box_w, Emu(400000),
             time, font_size=12, color=COLOR_LIGHT_GRAY,
             alignment=PP_ALIGN.CENTER)

add_text(slide, M_LEFT, Emu(5200000), CONTENT_W, Emu(600000),
         "~2 hours  •  One domain (gift cards)  •  Two exercises + two live demos",
         font_size=16, color=COLOR_GRAY, alignment=PP_ALIGN.CENTER)

add_notes(slide,
    "TIMING: 0:10–0:12\n"
    "\"Green blocks = you write code. Blue/purple = I demo live.\"\n"
    "\"One domain all the way through — each layer builds on the last.\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 5: Traditional Architecture
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "TRADITIONAL ARCHITECTURE")
add_accent_line(slide, Emu(1200000))

add_text(slide, M_LEFT, Emu(1600000), Emu(5500000), Emu(400000),
         "Primary state: in database", font_size=22, bold=True, color=COLOR_DARK)

items = [
    "Database as source of truth: updates in place",
    "Many clients, larger states, frequent updates",
    "Locks and I/O overhead",
    "Single master doesn't scale",
    "Caching??...",
]
add_bullet_block(slide, items, Emu(2200000), color=COLOR_GRAY, font_size=17)

add_notes(slide,
    "TIMING: 0:12–0:16\n"
    "\"This is what most of us build day to day.\"\n"
    "Don't dwell — this is the setup for why ES is different."
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 6: What Makes an Ideal Backend?
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "WHAT MAKES AN IDEAL BACKEND?")
add_accent_line(slide, Emu(1200000))

qualities = [
    ("(Almost) infinitely scalable", "No single master, no locks needed"),
    ("Lowest latency possible", "Primary state in memory, not on disk"),
    ("Always deterministic", "Durability, ordering, integrity guarantees"),
    ("Transparent, auditable logics", "Every state change is an event you can replay"),
    ("Below complexity barrier", "Express intent, not infrastructure"),
]
for i, (title, desc) in enumerate(qualities):
    y = Emu(1700000 + i * 850000)
    add_text(slide, Emu(1000000), y, Emu(5500000), Emu(400000),
             title, font_size=21, bold=True, color=COLOR_BLUE)
    add_text(slide, Emu(6800000), y + Emu(30000), Emu(5000000), Emu(400000),
             desc, font_size=16, color=COLOR_GRAY)

add_notes(slide, "TIMING: 0:16–0:18\n\"What if we could have ALL of these?\"")


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 7: Complete Behaviour
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "COMPLETE BEHAVIOUR: DATA + LOGICS")
add_accent_line(slide, Emu(1200000))

add_text(slide, M_LEFT, Emu(1600000), CONTENT_W, Emu(500000),
         "Business entities: orders, transactions, customers, digital twins...",
         font_size=19, color=COLOR_GRAY)
add_text(slide, M_LEFT, Emu(2300000), CONTENT_W, Emu(400000),
         "Own state and interactions with the world — fully covered:",
         font_size=19, bold=True, color=COLOR_DARK)

items = [
    "Incoming messages (commands) + immediate replies",
    "State changes (events applied to state)",
    "External effect calls (to other systems, LLMs, databases...)",
    "Deferred replies and scheduled timers",
]
add_bullet_block(slide, items, Emu(3000000), color=COLOR_DARK, font_size=18,
                 spacing=Emu(500000))

add_notes(slide, "TIMING: 0:18–0:20\n\"You'll implement exactly this pattern in 15 minutes.\"")


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 8: Event Sourcing Concept
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "EVENT SOURCING: THE IDEA")
add_accent_line(slide, Emu(1200000))

add_text(slide, M_LEFT, Emu(1600000), Emu(5000000), Emu(400000),
         "Primary state: in memory", font_size=22, bold=True, color=COLOR_DARK)

left_items = [
    "Log of updates (journal) as source of truth",
    "Stream — append-only, immutable",
    "Never in-place updates",
    "No locks, no I/O overhead — scales!",
]
add_bullet_block(slide, left_items, Emu(2200000), color=COLOR_GRAY, font_size=17)

journal_x = Emu(7500000)
add_text(slide, journal_x, Emu(1500000), Emu(4000000), Emu(400000),
         "Event Journal", font_size=16, bold=True, color=COLOR_BLUE,
         alignment=PP_ALIGN.CENTER)

events = ["CardIssued", "CardRedeemed", "CardRedeemed", "CardCancelled"]
for i, evt in enumerate(events):
    y = Emu(2000000 + i * 550000)
    add_box(slide, journal_x + Emu(200000), y, Emu(3200000), Emu(420000),
            RGBColor(0x2D, 0x2D, 0x2D), text=f"#{i+1}  {evt}", font_size=13,
            text_color=COLOR_GREEN)

add_text(slide, journal_x, Emu(4300000), Emu(3600000), Emu(400000),
         "→ append only, never mutate",
         font_size=14, color=COLOR_LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

add_notes(slide,
    "TIMING: 0:20–0:23\n"
    "\"Instead of updating a row, we append facts.\"\n"
    "Draw parallel to git: commits are events, working directory is state."
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 9: Pure Event Sourcing — decide/apply
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "PURE EVENT SOURCING: THE CORE LOOP")
add_accent_line(slide, Emu(1200000))

add_code_box(slide,
    "decide(State, Command) → Effect<Event, Reply>\n\n"
    "  → validate command against current state\n"
    "  → produce events (or reject)\n"
    "  → optionally reply to caller\n\n"
    "apply(State, Event) → State\n\n"
    "  → pure fold: no logic, just data transformation\n"
    "  → used for replay",
    M_LEFT, Emu(1600000), Emu(6000000), Emu(3400000), font_size=17)

flow_x = Emu(7500000)
add_box(slide, flow_x, Emu(1600000), Emu(2400000), Emu(600000),
        COLOR_BLUE, "Command", font_size=18)
add_text(slide, flow_x + Emu(900000), Emu(2300000), Emu(600000), Emu(400000),
         "↓", font_size=28, bold=True, color=COLOR_GRAY, alignment=PP_ALIGN.CENTER)
add_box(slide, flow_x, Emu(2700000), Emu(2400000), Emu(600000),
        COLOR_DARK, "decide()", font_size=18, text_color=COLOR_WHITE)
add_text(slide, flow_x + Emu(900000), Emu(3400000), Emu(600000), Emu(400000),
         "↓", font_size=28, bold=True, color=COLOR_GRAY, alignment=PP_ALIGN.CENTER)
add_box(slide, flow_x, Emu(3800000), Emu(2400000), Emu(600000),
        COLOR_GREEN, "Event(s)", font_size=18, text_color=COLOR_WHITE)
add_text(slide, flow_x + Emu(900000), Emu(4500000), Emu(600000), Emu(400000),
         "↓", font_size=28, bold=True, color=COLOR_GRAY, alignment=PP_ALIGN.CENTER)
add_box(slide, flow_x, Emu(4900000), Emu(2400000), Emu(600000),
        COLOR_ORANGE, "apply() → State'", font_size=18, text_color=COLOR_WHITE)

add_notes(slide,
    "TIMING: 0:23–0:27\n"
    "THIS IS THE CORE MENTAL MODEL. Spend time here.\n"
    "\"decide() is WHERE your business logic lives.\"\n"
    "\"apply() is PURE — no logic, just state transitions.\"\n"
    "Ask: \"Why can't we put logic in apply?\" → Because replay would re-validate."
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 10: Effects
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "EVENT SOURCING: EFFECTS")
add_accent_line(slide, Emu(1200000))

add_text(slide, M_LEFT, Emu(1600000), CONTENT_W, Emu(400000),
         "decide() returns an Effect describing what should happen:",
         font_size=18, color=COLOR_GRAY)

effects = [
    ("persist(event)", "Store event(s) in the journal", COLOR_BLUE),
    ("reply(value)", "Respond to the caller immediately", COLOR_BLUE),
    ("andReply(persist(...), reply)", "Persist + reply atomically", COLOR_BLUE),
    ("andRun(persist(...), sideEffect)", "Persist, then run async side effect", COLOR_ORANGE),
    ("done()", "No-op — acknowledge without action", COLOR_LIGHT_GRAY),
]
for i, (code, desc, color) in enumerate(effects):
    y = Emu(2300000 + i * 700000)
    add_code_box(slide, code, M_LEFT, y, Emu(4800000), Emu(500000), font_size=15)
    add_text(slide, Emu(5900000), y + Emu(80000), Emu(5500000), Emu(400000),
             desc, font_size=17, color=color, bold=True)

add_notes(slide,
    "TIMING: 0:27–0:30\n"
    "Highlight persist + andReply — they'll use these in Exercise 1.\n"
    "Mention andRun — they'll see it in the LLM demo.\n"
    "\"decide returns a recipe, the runtime executes it.\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 11: DDD ↔ TEOB Mapping Table
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "THE DDD CORE MAPS 1:1")
add_accent_line(slide, Emu(1200000))

rows_data = [
    ("DDD", "TEOB", "Notes"),
    ("Aggregate", "Aggregate<S, C, E, R>", "The consistency boundary."),
    ("Aggregate ID", "EntityId", "Branded string, same concept."),
    ("Command", "Command (type param)", "Inbound intent."),
    ("Domain Event", "Event (type param)", "Fact that happened."),
    ("Decision function", "decide(state, cmd, ctx)", "\"Given state + command, what happens?\""),
    ("State fold / evolve", "apply(state, event)", "Pure left-fold."),
    ("Initial state", "initial(id)", "The \"zero\" of the fold."),
    ("Invariant", "invariants[]", "Executable, testable — faithful to DDD intent."),
]

col_widths = [Emu(2500000), Emu(3500000), Emu(5500000)]
table_shape = slide.shapes.add_table(
    len(rows_data), 3, M_LEFT, Emu(1500000),
    sum(col_widths), Emu(500000) * len(rows_data))
table = table_shape.table

for ci, w in enumerate(col_widths):
    table.columns[ci].width = w

for ri, row_data in enumerate(rows_data):
    for ci, cell_text in enumerate(row_data):
        cell = table.cell(ri, ci)
        cell.text = cell_text
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(14 if ri > 0 else 15)
        p.font.bold = (ri == 0)
        if ri == 0:
            p.font.color.rgb = COLOR_WHITE
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_BLUE
        elif ci == 1:
            p.font.name = "SF Mono"
            p.font.color.rgb = COLOR_BLUE
            p.font.size = Pt(13)
        else:
            p.font.color.rgb = COLOR_DARK if ci == 0 else COLOR_GRAY
        cell.margin_left = Pt(8)
        cell.margin_top = Pt(4)

add_notes(slide,
    "TIMING: 0:30–0:35\n"
    "THE AHA SLIDE. Go row by row.\n"
    "\"If you know DDD, you already know TEOB.\"\n"
    "Pause for questions before Exercise 1."
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 12: Beyond the Blue Book
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "BEYOND THE BLUE BOOK")
add_accent_line(slide, Emu(1200000))

beyond = [
    ("Effect ADT", "Declarative Effect<Event, Reply> — a program describing what should happen."),
    ("Reply as first-class", "persist(...).andReply(...) atomically. CQRS-with-response."),
    ("EffectControl (ctx)", "Timers, cross-entity messaging, external effects (ctx.sync, ctx.tell)."),
    ("Invariants", "Executable and testable — faithful to why the boundary exists."),
    ("Projections", "Event → read model. Same pure fold pattern, optimized for queries."),
]
for i, (title, desc) in enumerate(beyond):
    y = Emu(1700000 + i * 900000)
    add_text(slide, M_LEFT, y, Emu(2800000), Emu(400000),
             title, font_size=18, bold=True, color=COLOR_BLUE)
    add_text(slide, Emu(3700000), y, Emu(8000000), Emu(700000),
             desc, font_size=15, color=COLOR_GRAY)

add_notes(slide,
    "TIMING: 0:35–0:38\n"
    "\"The core is DDD. The extras are what make it practical.\"\n"
    "Mention projections — they'll build one in Exercise 2."
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 13: Everything Is an Entity
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "EVERYTHING IS AN ENTITY")
add_accent_line(slide, Emu(1200000))

items = [
    "Complete entity behaviour — as pure functions",
    "Codecs — serialisable representation (Command, Reply, Event, State)",
    "Agnostic to execution and persistence",
    "Multiple runtimes: in-memory, SQLite, PostgreSQL (same aggregate code)",
]
add_bullet_block(slide, items, Emu(1700000), color=COLOR_DARK, font_size=19,
                 spacing=Emu(800000))

add_code_box(slide,
    "// Same aggregate code, different runtimes:\n"
    "createInMemoryRuntime([reg])     // tests & dev\n"
    "createSQLiteRuntime([reg])       // zero-config local\n"
    "createPostgresRuntime([reg])     // production",
    M_LEFT, Emu(5000000), Emu(7000000), Emu(1200000), font_size=15)

add_notes(slide,
    "TIMING: 0:38–0:40\n"
    "\"Your business logic doesn't know or care about the database.\"\n"
    "\"In exercises, we use InMemoryRuntime. In production, swap to Postgres.\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 14: Exercise 1 Brief — Gift Card Aggregate
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "EXERCISE 1: GIFT CARD AGGREGATE", color=COLOR_GREEN, font_size=34)
add_accent_line(slide, Emu(1200000), color=COLOR_GREEN)

add_code_box(slide,
    "Commands:  Issue | Redeem | Cancel | GetBalance\n"
    "Events:    Issued | Redeemed | Cancelled\n"
    "State:     { balance, status, recipientName }",
    M_LEFT, Emu(1600000), Emu(6500000), Emu(1000000), font_size=17)

add_text(slide, M_LEFT, Emu(2900000), Emu(6000000), Emu(400000),
         "Business rules to implement:", font_size=18, bold=True, color=COLOR_DARK)
rules = [
    "Issue only if card is Empty",
    "Redeem only if Active, amount ≤ balance",
    "Cancel only if Active",
    "Invariants: balance ≥ 0, cancelled → balance = 0",
]
add_bullet_block(slide, rules, Emu(3400000), color=COLOR_DARK, font_size=17,
                 spacing=Emu(420000))

add_code_box(slide,
    "npm run test:aggregate",
    M_LEFT, Emu(5400000), Emu(5500000), Emu(500000), font_size=16)

add_text(slide, Emu(6500000), Emu(5450000), Emu(5000000), Emu(500000),
         "15 tests. Make them green.", font_size=22, bold=True, color=COLOR_GREEN)

add_notes(slide,
    "TIMING: 0:40–0:42\n"
    "LIVE DEMO: Run tests. Show 13 failing.\n"
    "\"Start with Issue — it's the simplest. The hints are in HINTS-aggregate.md.\"\n"
    "\"Solution is in aggregate.solution.ts — but try first!\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 15: Exercise 1 — Work Time
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_DARK)
add_text(slide, M_LEFT, Emu(2200000), CONTENT_W, Emu(1000000),
         "EXERCISE 1: AGGREGATE", font_size=48, bold=True,
         color=COLOR_GREEN, alignment=PP_ALIGN.CENTER)
add_text(slide, M_LEFT, Emu(3400000), CONTENT_W, Emu(600000),
         "30 minutes  •  15 tests  •  implement decide() + invariants",
         font_size=22, color=COLOR_LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
add_text(slide, M_LEFT, Emu(4600000), CONTENT_W, Emu(400000),
         "npm run test:aggregate",
         font_size=18, color=COLOR_GREEN, alignment=PP_ALIGN.CENTER,
         font_name="SF Mono")

add_notes(slide,
    "TIMING: 0:42–1:12 (30 min)\n"
    "LEAVE THIS SLIDE UP.\n"
    "At 15 min: \"How many tests green? More than 5?\"\n"
    "At 25 min: Live-code Issue case if people are stuck.\n"
    "At 28 min: \"2 minutes left.\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 16: Exercise 1 Debrief
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "EXERCISE 1: DEBRIEF")
add_accent_line(slide, Emu(1200000))

takeaways = [
    "decide() — all business logic in one place, pattern-matched on command tag",
    "apply() — pure state fold, no logic, just data transformation",
    "invariants[] — executable contracts that guard consistency",
    "Effect ADT — persist(), reply(), andReply() — declarative, composable",
    "AggregateTestKit — test the domain directly, no infrastructure",
]
add_bullet_block(slide, takeaways, Emu(1700000), color=COLOR_DARK, font_size=17,
                 spacing=Emu(550000))

add_code_box(slide,
    "// The core pattern:\n"
    "if (invalid) return reply({ tag: 'Rejected', reason: '...' })\n"
    "return andReply(persist(event), { tag: 'Ok' })",
    M_LEFT, Emu(5200000), Emu(8500000), Emu(1000000), font_size=15)

add_notes(slide,
    "TIMING: 1:12–1:17\n"
    "Live-code the solution if needed.\n"
    "\"No database, no HTTP, no framework setup. Just domain logic.\"\n"
    "Ask: \"What surprised you?\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 17: Demo — HTTP Service
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "DEMO: YOUR AGGREGATE AS AN API", color=COLOR_BLUE)
add_accent_line(slide, Emu(1200000), color=COLOR_BLUE)

add_text(slide, M_LEFT, Emu(1600000), CONTENT_W, Emu(400000),
         "Your decide() function is now a live HTTP endpoint:",
         font_size=19, color=COLOR_GRAY)

add_code_box(slide,
    "# Issue a gift card\n"
    "curl -X POST http://localhost:3000/api/gift-card/card-1 \\\n"
    "  -H 'Content-Type: application/json' \\\n"
    "  -d '{\"tag\":\"Issue\",\"amount\":100,\"recipientName\":\"Alice\"}'\n"
    "→ {\"tag\":\"Ok\"}\n\n"
    "# Redeem\n"
    "curl -X POST ... -d '{\"tag\":\"Redeem\",\"amount\":30}'\n"
    "→ {\"tag\":\"Ok\"}\n\n"
    "# Reject (too much)\n"
    "curl -X POST ... -d '{\"tag\":\"Redeem\",\"amount\":999}'\n"
    "→ 400 {\"tag\":\"Rejected\",\"reason\":\"Insufficient balance\"}",
    M_LEFT, Emu(2200000), Emu(8500000), Emu(3200000), font_size=14)

add_text(slide, M_LEFT, Emu(5700000), CONTENT_W, Emu(400000),
         "Reply → HTTP response.  Rejection → 400.  Timeout → 504.  ETag for optimistic concurrency.",
         font_size=15, bold=True, color=COLOR_BLUE)

add_notes(slide,
    "TIMING: 1:17–1:22\n"
    "LIVE DEMO: Run `npm start`, then curl commands.\n"
    "Show: Ok reply → 200, Rejected → 400, ETag header.\n"
    "\"Zero wiring code. aggregateRoutes() generates everything from your aggregate.\"\n"
    "\"Your decide() is the API contract.\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 18: Break
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_DARK)
add_text(slide, M_LEFT, Emu(2600000), CONTENT_W, Emu(800000),
         "BREAK", font_size=64, bold=True,
         color=COLOR_WHITE, alignment=PP_ALIGN.CENTER)
add_text(slide, M_LEFT, Emu(3600000), CONTENT_W, Emu(600000),
         "5 minutes  •  stretch  •  refill coffee",
         font_size=22, color=COLOR_LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
add_text(slide, M_LEFT, Emu(4800000), CONTENT_W, Emu(400000),
         "Next up: the read side — projections",
         font_size=18, color=COLOR_GREEN, alignment=PP_ALIGN.CENTER)

add_notes(slide, "TIMING: 1:22–1:27")


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 19: Theory — Write Side vs Read Side
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "WRITE SIDE VS READ SIDE")
add_accent_line(slide, Emu(1200000))

# Left: write side
add_box(slide, M_LEFT, Emu(1800000), Emu(4800000), Emu(2500000),
        COLOR_BLUE, "", font_size=14)
add_text(slide, Emu(900000), Emu(1900000), Emu(4400000), Emu(400000),
         "WRITE SIDE (aggregate)", font_size=18, bold=True, color=COLOR_WHITE)
write_items = [
    "decide() — validates, produces events",
    "apply() — state for decisions",
    "Optimized for consistency",
    "One entity at a time",
]
for i, item in enumerate(write_items):
    add_text(slide, Emu(900000), Emu(2400000 + i * 400000), Emu(4400000), Emu(350000),
             f"• {item}", font_size=14, color=COLOR_WHITE)

# Right: read side
add_box(slide, Emu(6200000), Emu(1800000), Emu(4800000), Emu(2500000),
        COLOR_GREEN, "", font_size=14)
add_text(slide, Emu(6400000), Emu(1900000), Emu(4400000), Emu(400000),
         "READ SIDE (projection)", font_size=18, bold=True, color=COLOR_WHITE)
read_items = [
    "evolve() — builds query-optimized views",
    "Can include derived data (counts, aggregations)",
    "Optimized for queries",
    "Can span multiple entities",
]
for i, item in enumerate(read_items):
    add_text(slide, Emu(6400000), Emu(2400000 + i * 400000), Emu(4400000), Emu(350000),
             f"• {item}", font_size=14, color=COLOR_WHITE)

# Arrow
add_text(slide, Emu(5100000), Emu(2700000), Emu(1000000), Emu(400000),
         "→", font_size=36, bold=True, color=COLOR_ORANGE, alignment=PP_ALIGN.CENTER)

add_text(slide, M_LEFT, Emu(4800000), CONTENT_W, Emu(400000),
         "Same pattern: pure function, event in → new state out",
         font_size=20, bold=True, color=COLOR_DARK, alignment=PP_ALIGN.CENTER)

add_code_box(slide,
    "// Write side                          // Read side\n"
    "apply(state, event) → State           evolve(view, event) → View",
    M_LEFT, Emu(5400000), CONTENT_W, Emu(600000), font_size=16)

add_notes(slide,
    "TIMING: 1:27–1:32\n"
    "\"You already know the pattern — apply and evolve are the same shape.\"\n"
    "\"The difference: evolve builds views optimized for queries, not decisions.\"\n"
    "\"A view can include transactionCount — something the aggregate doesn't track.\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 20: Exercise 2 Brief — Projection
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "EXERCISE 2: GIFT CARD PROJECTION", color=COLOR_GREEN, font_size=34)
add_accent_line(slide, Emu(1200000), color=COLOR_GREEN)

add_text(slide, M_LEFT, Emu(1600000), CONTENT_W, Emu(400000),
         "Build a read model from gift card events:", font_size=19, color=COLOR_GRAY)

add_code_box(slide,
    "GiftCardView {\n"
    "  balance, status, recipientName,\n"
    "  encouragement,        // from LLM (demo)\n"
    "  transactionCount      // derived — aggregate doesn't track this!\n"
    "}",
    M_LEFT, Emu(2200000), Emu(6500000), Emu(1400000), font_size=16)

add_text(slide, M_LEFT, Emu(3900000), Emu(6000000), Emu(400000),
         "Implement evolve() — same pattern as apply():", font_size=18, bold=True, color=COLOR_DARK)
cases = [
    "Issued → set balance, status, recipientName",
    "Redeemed → subtract amount, increment transactionCount",
    "Cancelled → zero balance, set status",
    "EncouragementSet → set encouragement text",
]
add_bullet_block(slide, cases, Emu(4400000), color=COLOR_DARK, font_size=16,
                 spacing=Emu(380000))

add_code_box(slide,
    "npm run test:projection",
    M_LEFT, Emu(5900000), Emu(5500000), Emu(500000), font_size=16)

add_text(slide, Emu(6500000), Emu(5950000), Emu(5000000), Emu(500000),
         "8 tests. Make them green.", font_size=22, bold=True, color=COLOR_GREEN)

add_notes(slide,
    "TIMING: 1:32–1:35\n"
    "\"You already know the pattern from apply(). This is the same thing, for queries.\"\n"
    "\"The key difference: transactionCount. The aggregate doesn't track this — the projection does.\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 21: Exercise 2 — Work Time
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_DARK)
add_text(slide, M_LEFT, Emu(2200000), CONTENT_W, Emu(1000000),
         "EXERCISE 2: PROJECTION", font_size=48, bold=True,
         color=COLOR_GREEN, alignment=PP_ALIGN.CENTER)
add_text(slide, M_LEFT, Emu(3400000), CONTENT_W, Emu(600000),
         "20 minutes  •  8 tests  •  implement evolve()",
         font_size=22, color=COLOR_LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
add_text(slide, M_LEFT, Emu(4600000), CONTENT_W, Emu(400000),
         "npm run test:projection",
         font_size=18, color=COLOR_GREEN, alignment=PP_ALIGN.CENTER,
         font_name="SF Mono")
add_text(slide, M_LEFT, Emu(5400000), CONTENT_W, Emu(400000),
         "Same pattern as apply()  •  HINTS-projection.md if stuck",
         font_size=16, color=COLOR_LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

add_notes(slide,
    "TIMING: 1:35–1:55 (20 min)\n"
    "This should go faster — they already know the pattern.\n"
    "At 10 min: Most should have Issued done.\n"
    "At 15 min: Show Hint 3 (Redeemed with transactionCount).\n"
    "At 18 min: \"2 minutes left.\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 22: Exercise 2 Debrief
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "EXERCISE 2: DEBRIEF")
add_accent_line(slide, Emu(1200000))

add_text(slide, M_LEFT, Emu(1600000), CONTENT_W, Emu(400000),
         "Three pure functions — that's the whole model:", font_size=20, bold=True, color=COLOR_DARK)

add_code_box(slide,
    "decide(state, command)  → Effect     // business logic\n"
    "apply(state, event)     → State      // write-side fold\n"
    "evolve(view, event)     → View       // read-side fold",
    M_LEFT, Emu(2200000), Emu(8000000), Emu(1000000), font_size=18)

add_text(slide, M_LEFT, Emu(3600000), CONTENT_W, Emu(400000),
         "What the projection gave you that the aggregate doesn't:", font_size=18, bold=True, color=COLOR_DARK)

diffs = [
    "transactionCount — derived data, computed from event stream",
    "encouragement — data from a different event (LLM callback)",
    "Optimized for queries — flat shape, no business rules",
    "Can be rebuilt anytime from the event journal",
]
add_bullet_block(slide, diffs, Emu(4100000), color=COLOR_BLUE, font_size=17,
                 spacing=Emu(500000))

add_notes(slide,
    "TIMING: 1:55–2:00\n"
    "\"Three pure functions. That's the entire architecture.\"\n"
    "\"decide for commands, apply for state, evolve for queries.\"\n"
    "\"Now let me show you something exciting...\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 23: Demo — LLM Integration
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "DEMO: LLM INTEGRATION", color=COLOR_PURPLE)
add_accent_line(slide, Emu(1200000), color=COLOR_PURPLE)

add_text(slide, M_LEFT, Emu(1600000), CONTENT_W, Emu(400000),
         "When a gift card is issued, ask an LLM to write a personal encouragement:",
         font_size=18, color=COLOR_GRAY)

add_code_box(slide,
    "case \"Issue\": {\n"
    "  return andReply(\n"
    "    andRun(\n"
    "      persist({ tag: \"Issued\", ... }),\n"
    "      async () => {\n"
    "        await ctx.sync({                        // ← same pattern!\n"
    "          effect: () => generateEncouragement(name, amount),\n"
    "          onSuccess: (r) => ({ tag: \"SetEncouragement\", text: r.text }),\n"
    "          onFailure: (_) => ({ tag: \"SetEncouragement\", text: fallback }),\n"
    "        });\n"
    "      },\n"
    "    ),\n"
    "    { tag: \"Ok\" },\n"
    "  );\n"
    "}",
    M_LEFT, Emu(2200000), Emu(9000000), Emu(3200000), font_size=14)

add_text(slide, M_LEFT, Emu(5700000), CONTENT_W, Emu(400000),
         "ctx.sync() — same pattern for LLM, payment gateway, shipping API. Event sourcing gives you retry, replay, audit — for free.",
         font_size=16, bold=True, color=COLOR_PURPLE)

add_notes(slide,
    "TIMING: 2:00–2:10\n"
    "LIVE DEMO: Run `OPENROUTER_API_KEY=sk-... npm run demo:llm`\n"
    "Issue a card with a name → show the encouragement appearing.\n"
    "\"ctx.sync() is the same pattern you'd use for ANY external call.\"\n"
    "\"The LLM result comes back as a command, gets persisted as an event.\"\n"
    "\"Crash? Replay from journal. Debug? Replay specific steps.\"\n"
    "THIS IS THE WOW MOMENT."
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 24: The Full Picture
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "THE FULL PICTURE")
add_accent_line(slide, Emu(1200000))

layers = [
    ("Your code", "Aggregates, Projections, Sagas — pure functions", COLOR_GREEN),
    ("TEOB framework", "Effect system, Runtime, Codecs, TestKit, HTTP routes", COLOR_BLUE),
    ("Persistence", "In-memory → SQLite → PostgreSQL (zero code changes)", COLOR_ORANGE),
    ("Infrastructure", "Health checks, OpenTelemetry, OpenAPI generation", COLOR_LIGHT_GRAY),
]
for i, (layer, desc, color) in enumerate(layers):
    y = Emu(1700000 + i * 1100000)
    add_box(slide, M_LEFT, y, Emu(2500000), Emu(800000), color,
            text=layer, font_size=18, text_color=COLOR_WHITE)
    add_text(slide, Emu(3700000), y + Emu(200000), Emu(8000000), Emu(500000),
             desc, font_size=17, color=COLOR_DARK)

add_notes(slide,
    "TIMING: 2:10–2:13\n"
    "\"You built the green layer. Everything else is provided.\"\n"
    "\"To go to production: swap InMemoryRuntime → PostgresRuntime.\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 25: Battle Tested
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "BATTLE TESTED")
add_accent_line(slide, Emu(1200000))

points = [
    "Natively CQS — for (almost) infinite scaling",
    "FP and DDD — to express intrinsically complex data and rules",
    "Everything is executed deterministically",
    "10+ years of real production (fintech) experience",
]
add_bullet_block(slide, points, Emu(1800000), color=COLOR_DARK, font_size=21,
                 spacing=Emu(900000), bold=True)

add_notes(slide, "TIMING: 2:13–2:15\nCredibility slide. Keep brief.")


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 26: Closing CTA
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_DARK)
add_text(slide, M_LEFT, Emu(1000000), CONTENT_W, Emu(800000),
         "WHAT'S NEXT?", font_size=44, bold=True,
         color=COLOR_WHITE, alignment=PP_ALIGN.CENTER)
add_accent_line(slide, Emu(1800000), color=COLOR_BLUE)

cta_items = [
    ("Clone the repo", "github.com/lambda-house/teob-ts-workshop-gift-card", COLOR_GREEN),
    ("Try at home", "Add Freeze/Unfreeze commands, transaction history in the view", COLOR_BLUE),
    ("Scaffold your own", "npx teob new aggregate — working code in seconds", COLOR_BLUE),
    ("Watch the recording", "Solution walkthroughs with chapter markers", COLOR_ORANGE),
    ("Next workshop", "Episode 2: Sagas & Cross-Aggregate Communication", COLOR_PURPLE),
]
for i, (title, desc, color) in enumerate(cta_items):
    y = Emu(2100000 + i * 800000)
    add_box(slide, M_LEFT, y, Emu(400000), Emu(400000), color, text="→", font_size=20)
    add_text(slide, Emu(1400000), y, Emu(5000000), Emu(400000),
             title, font_size=20, bold=True, color=COLOR_WHITE)
    add_text(slide, Emu(1400000), y + Emu(350000), Emu(10000000), Emu(350000),
             desc, font_size=15, color=COLOR_LIGHT_GRAY)

add_text(slide, M_LEFT, Emu(6200000), CONTENT_W, Emu(400000),
         "Thank you!  •  Questions?",
         font_size=24, bold=True, color=COLOR_WHITE, alignment=PP_ALIGN.CENTER)

add_notes(slide,
    "TIMING: 2:15–2:20\n"
    "\"You built an event-sourced service with a read model and AI integration.\"\n"
    "\"Three pure functions. That's the whole architecture.\"\n"
    "Open for questions."
)


# ══════════════════════════════════════════════════════════════════════════
# Save
# ══════════════════════════════════════════════════════════════════════════

import os
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "DDD-Workshop-Slides.pptx")
prs.save(output_path)
print(f"Saved {len(prs.slides)} slides to {output_path}")
