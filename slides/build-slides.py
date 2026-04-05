#!/usr/bin/env python3
"""
Build the complete DDD Workshop PPTX deck.
Run: /tmp/pptx-env/bin/python3 workshop/build-slides.py
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ── Theme constants (matching existing deck) ──────────────────────────────

BG_LIGHT = RGBColor(0xEC, 0xEC, 0xEC)
BG_DARK = RGBColor(0x1E, 0x1E, 0x2E)
BG_ACCENT = RGBColor(0x2A, 0x2A, 0x3A)

COLOR_DARK = RGBColor(0x22, 0x22, 0x22)
COLOR_BLUE = RGBColor(0x22, 0x66, 0xAA)
COLOR_GREEN = RGBColor(0x66, 0xBB, 0x6A)
COLOR_RED = RGBColor(0xEF, 0x53, 0x50)
COLOR_GRAY = RGBColor(0x44, 0x44, 0x44)
COLOR_LIGHT_GRAY = RGBColor(0x88, 0x88, 0x88)
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
COLOR_ORANGE = RGBColor(0xFF, 0xA7, 0x26)
COLOR_AMBER = RGBColor(0xFF, 0xC1, 0x07)

SLIDE_W = 12191695  # 13.33 inches (widescreen 16:9)
SLIDE_H = 6858000   # 7.5 inches

# Margins
M_LEFT = Emu(731520)
M_TOP = Emu(548640)
M_RIGHT = Emu(731520)
CONTENT_W = SLIDE_W - M_LEFT - M_RIGHT

prs = Presentation()
prs.slide_width = SLIDE_W
prs.slide_height = SLIDE_H

# Use Blank layout
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
             text, font_size=font_size, bold=True, color=color,
             alignment=PP_ALIGN.LEFT)


def add_subtitle(slide, text, top=Emu(1400000), color=COLOR_GRAY, font_size=20):
    add_text(slide, M_LEFT, top, CONTENT_W, Emu(600000),
             text, font_size=font_size, bold=False, color=color)


def add_bullet_block(slide, items, top, color=COLOR_DARK, font_size=18,
                     bold=False, spacing=Emu(380000), left=None, width=None,
                     bullet_color=None):
    """Add a list of text items as separate text boxes with bullet points."""
    if left is None:
        left = M_LEFT
    if width is None:
        width = CONTENT_W
    for i, item in enumerate(items):
        y = top + Emu(i) * spacing if isinstance(spacing, int) else top + i * spacing
        prefix = "• " if not item.startswith(("─", "→", " ", "•")) else ""
        add_text(slide, left, y, width, spacing,
                 f"{prefix}{item}", font_size=font_size, bold=bold, color=color)


def add_code_box(slide, text, left, top, width, height, font_size=14):
    """Dark rounded box with monospace text."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0x2D, 0x2D, 0x2D)
    shape.line.fill.background()
    # Smaller corner radius
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
    """Thin horizontal accent line."""
    if width is None:
        width = CONTENT_W
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, M_LEFT, top, width, Emu(36000)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def add_box(slide, left, top, width, height, fill_color, text="",
            font_size=16, text_color=COLOR_WHITE, bold=True):
    """Colored rounded rectangle with centered text."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
    )
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
    tf.paragraphs[0].space_before = Pt(0)
    tf.paragraphs[0].space_after = Pt(0)
    return shape


def add_arrow(slide, left, top, width, height, color=COLOR_GRAY):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RIGHT_ARROW, left, top, width, height
    )
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
add_accent_line(slide, Emu(2600000), color=COLOR_BLUE)
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
    "Then: \"Today you'll write two event-sourced aggregates from scratch.\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 2: What You'll Learn
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "WHAT YOU'LL BUILD TODAY")
add_accent_line(slide, Emu(1200000))

items = [
    ("1", "Model a DDD aggregate", "with commands, events, state, and invariants", COLOR_BLUE),
    ("2", "Test it with a dedicated test kit", "— 15 tests from red to green", COLOR_BLUE),
    ("3", "Connect two aggregates across boundaries", "with ctx.tell() and ctx.sync()", COLOR_BLUE),
]
for i, (num, title, subtitle, color) in enumerate(items):
    y = Emu(1700000 + i * 1500000)
    add_box(slide, M_LEFT, y, Emu(700000), Emu(700000), color,
            text=num, font_size=32, text_color=COLOR_WHITE)
    add_text(slide, Emu(1700000), y + Emu(50000), Emu(9000000), Emu(400000),
             title, font_size=24, bold=True, color=COLOR_DARK)
    add_text(slide, Emu(1700000), y + Emu(400000), Emu(9000000), Emu(300000),
             subtitle, font_size=16, color=COLOR_GRAY)

add_notes(slide,
    "TIMING: 0:05–0:08\n"
    "Frame the workshop outcomes clearly.\n"
    "\"By the end of this session, you'll have working code — not just slides.\"\n"
    "This is the promise. Everything builds toward these three things."
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
             f"✋  {q}", font_size=22, bold=False, color=COLOR_DARK)

add_notes(slide,
    "TIMING: 0:08–0:10\n"
    "CRITICAL: This calibrates your depth for the rest of the talk.\n"
    "If most have DDD experience → skip basic aggregate explanation, go deeper on TEOB specifics.\n"
    "If most are new → slow down on decide/apply, give more context.\n"
    "If Akka/Axon users → draw parallels: \"ctx is like ActorContext, Effect is like Effect in Akka Persistence\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 4: Summary / Roadmap
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "THE ROAD MAP")
add_accent_line(slide, Emu(1200000))

add_text(slide, M_LEFT, Emu(1500000), CONTENT_W, Emu(600000),
         "Backend Architectures: Traditional → Latency-Critical → Event-Sourced",
         font_size=18, color=COLOR_GRAY)

# Timeline boxes
stages = [
    ("Traditional\nArchitecture", COLOR_LIGHT_GRAY, "10 min"),
    ("Event Sourcing\n& Effects", COLOR_BLUE, "15 min"),
    ("DDD ↔ TEOB\nMapping", COLOR_BLUE, "10 min"),
    ("Exercise 1\nGift Card", COLOR_GREEN, "30 min"),
    ("Aggregate\nCommunication", COLOR_BLUE, "10 min"),
    ("Exercise 2\nOrder+Payment", COLOR_GREEN, "35 min"),
    ("Full Picture\n& Next Steps", COLOR_ORANGE, "10 min"),
]
box_w = Emu(1400000)
gap = Emu(100000)
start_x = Emu(400000)
for i, (label, color, time) in enumerate(stages):
    x = start_x + i * (box_w + gap)
    add_box(slide, x, Emu(2400000), box_w, Emu(1800000), color,
            text=label, font_size=13, text_color=COLOR_WHITE)
    add_text(slide, x, Emu(4400000), box_w, Emu(400000),
             time, font_size=12, color=COLOR_LIGHT_GRAY,
             alignment=PP_ALIGN.CENTER)

add_text(slide, M_LEFT, Emu(5400000), CONTENT_W, Emu(600000),
         "~2 hours total  •  Two hands-on exercises  •  Everything runs locally",
         font_size=16, color=COLOR_GRAY, alignment=PP_ALIGN.CENTER)

add_notes(slide,
    "TIMING: 0:10–0:12\n"
    "Show the map so people know where they are at all times.\n"
    "\"We'll alternate between short theory bursts and hands-on coding.\"\n"
    "\"The green blocks are where YOU write code.\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 5: Traditional Architecture
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "TRADITIONAL ARCHITECTURE")
add_accent_line(slide, Emu(1200000))

# Left side: the pattern
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

# Right side: diagram
add_box(slide, Emu(7000000), Emu(1800000), Emu(1800000), Emu(700000),
        COLOR_BLUE, "Client A", font_size=14)
add_box(slide, Emu(7000000), Emu(2800000), Emu(1800000), Emu(700000),
        COLOR_BLUE, "Client B", font_size=14)
add_box(slide, Emu(9500000), Emu(2100000), Emu(2200000), Emu(1200000),
        COLOR_RED, "Database\n(mutable)", font_size=16)

add_notes(slide,
    "TIMING: 0:12–0:16\n"
    "\"This is what most of us build day to day.\"\n"
    "Don't dwell — this is the setup for why ES is different.\n"
    "Key pain points: in-place mutation, scaling, audit trail."
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

add_notes(slide,
    "TIMING: 0:16–0:18\n"
    "\"What if we could have ALL of these?\"\n"
    "This is the wish list. Event sourcing gives us most of them.\n"
    "Pause after each — let it sink in."
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 7: Complete Behaviour: Data+Logics
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
    "External effect calls (to other systems, databases...)",
    "Deferred replies and scheduled timers",
]
add_bullet_block(slide, items, Emu(3000000), color=COLOR_DARK, font_size=18,
                 spacing=Emu(500000))

add_notes(slide,
    "TIMING: 0:18–0:20\n"
    "\"An entity is a self-contained unit of behavior.\"\n"
    "This is the DDD aggregate concept — but with a richer protocol.\n"
    "Foreshadow: \"You'll implement exactly this pattern in 15 minutes.\""
)


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
    "LSM-tree / SSTable: no locks necessary",
    "No I/O overhead, no single master — scales!",
]
add_bullet_block(slide, left_items, Emu(2200000), color=COLOR_GRAY, font_size=17)

# Right side: journal visualization
journal_x = Emu(7500000)
add_text(slide, journal_x, Emu(1500000), Emu(4000000), Emu(400000),
         "Event Journal", font_size=16, bold=True, color=COLOR_BLUE,
         alignment=PP_ALIGN.CENTER)

events = ["OrderPlaced", "ItemAdded", "ItemAdded", "OrderConfirmed", "PaymentReceived"]
for i, evt in enumerate(events):
    y = Emu(2000000 + i * 500000)
    add_box(slide, journal_x + Emu(200000), y, Emu(3200000), Emu(380000),
            RGBColor(0x2D, 0x2D, 0x2D), text=f"#{i+1}  {evt}", font_size=13,
            text_color=COLOR_GREEN)

add_text(slide, journal_x, Emu(4700000), Emu(3600000), Emu(400000),
         "→ append only, never mutate",
         font_size=14, color=COLOR_LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

add_notes(slide,
    "TIMING: 0:20–0:23\n"
    "\"Instead of updating a row, we append facts.\"\n"
    "The journal IS the source of truth. State is derived by replaying.\n"
    "Draw parallel to git: commits are events, working directory is state.\n"
    "\"You can always rebuild state by replaying from the beginning.\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 9: Pure Event Sourcing — decide/apply loop
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "STREAM OF UPDATES: PURE EVENT SOURCING")
add_accent_line(slide, Emu(1200000))

# The core loop
add_code_box(slide,
    "Command handler:\n"
    "  → gets validated\n"
    "  → may produce a reply\n"
    "  → produces events\n\n"
    "decide(State, Command) → Effect<Event, Reply>\n\n"
    "Events applied to state to get new state:\n\n"
    "apply(State, Event) → State\n\n"
    "// initial state = fold zero",
    M_LEFT, Emu(1600000), Emu(6000000), Emu(3800000), font_size=17)

# Right side: the flow diagram
flow_x = Emu(7500000)
add_box(slide, flow_x, Emu(1600000), Emu(2400000), Emu(600000),
        COLOR_BLUE, "Command", font_size=18)
add_text(slide, flow_x + Emu(900000), Emu(2300000), Emu(600000), Emu(400000),
         "↓", font_size=28, bold=True, color=COLOR_GRAY,
         alignment=PP_ALIGN.CENTER)
add_box(slide, flow_x, Emu(2700000), Emu(2400000), Emu(600000),
        COLOR_DARK, "decide()", font_size=18, text_color=COLOR_WHITE)
add_text(slide, flow_x + Emu(900000), Emu(3400000), Emu(600000), Emu(400000),
         "↓", font_size=28, bold=True, color=COLOR_GRAY,
         alignment=PP_ALIGN.CENTER)
add_box(slide, flow_x, Emu(3800000), Emu(2400000), Emu(600000),
        COLOR_GREEN, "Event(s)", font_size=18, text_color=COLOR_WHITE)
add_text(slide, flow_x + Emu(900000), Emu(4500000), Emu(600000), Emu(400000),
         "↓", font_size=28, bold=True, color=COLOR_GRAY,
         alignment=PP_ALIGN.CENTER)
add_box(slide, flow_x, Emu(4900000), Emu(2400000), Emu(600000),
        COLOR_ORANGE, "apply() → State'", font_size=18, text_color=COLOR_WHITE)

add_notes(slide,
    "TIMING: 0:23–0:27\n"
    "THIS IS THE CORE MENTAL MODEL. Spend time here.\n"
    "\"decide() is WHERE your business logic lives. It looks at state + command and decides what happened.\"\n"
    "\"apply() is a PURE fold — no logic, just state transitions.\"\n"
    "\"This separation is what makes everything testable and replayable.\"\n"
    "Ask: \"Why can't we put business logic in apply?\" → Because replay would re-validate."
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 10: Event Sourcing: Effects
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "EVENT SOURCING: EFFECTS")
add_accent_line(slide, Emu(1200000))

add_text(slide, M_LEFT, Emu(1600000), CONTENT_W, Emu(400000),
         "decide() doesn't just return events — it returns an Effect describing what should happen:",
         font_size=18, color=COLOR_GRAY)

effects = [
    ("persist(event)", "Store event(s) in the journal", COLOR_BLUE),
    ("reply(value)", "Respond to the caller immediately", COLOR_BLUE),
    ("andReply(persist(...), reply)", "Persist + reply atomically", COLOR_BLUE),
    ("andRun(persist(...), sideEffect)", "Persist, then run async side effect", COLOR_BLUE),
    ("done()", "No-op — acknowledge without action", COLOR_LIGHT_GRAY),
]
for i, (code, desc, color) in enumerate(effects):
    y = Emu(2300000 + i * 700000)
    add_code_box(slide, code, M_LEFT, y, Emu(4800000), Emu(500000), font_size=15)
    add_text(slide, Emu(5900000), y + Emu(80000), Emu(5500000), Emu(400000),
             desc, font_size=17, color=color, bold=True)

add_text(slide, M_LEFT, Emu(5900000), CONTENT_W, Emu(400000),
         "Fully describes complete behaviour. Synchronous effects, timers, commands to other entities, deferred replies.",
         font_size=15, color=COLOR_LIGHT_GRAY)

add_notes(slide,
    "TIMING: 0:27–0:30\n"
    "\"The Effect type is the key innovation. It's not just events — it's a full program.\"\n"
    "Highlight persist + andReply — they'll use these in Exercise 1.\n"
    "Mention andRun — they'll use this in Exercise 2.\n"
    "\"Think of it as: decide returns a recipe, the runtime executes it.\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 11: DDD ↔ TEOB — Where They Meet (mapping table)
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "THE DDD CORE MAPS 1:1")
add_accent_line(slide, Emu(1200000))

# Build table
rows_data = [
    ("DDD", "TEOB", "Notes"),
    ("Aggregate", "Aggregate<S, C, E, R>", "The consistency boundary. One category = one type."),
    ("Aggregate ID", "EntityId", "Branded string, same concept."),
    ("Command", "Command (type param)", "Inbound intent."),
    ("Domain Event", "Event (type param)", "Fact that happened."),
    ("Decision function", "decide(state, cmd, ctx)", '"Given this state and this command, what happens?"'),
    ("State fold / evolve", "apply(state, event)", "Pure left-fold. The event applicator."),
    ("Initial state", "initial(id)", 'The "zero" of the fold.'),
    ("Invariant", "invariants[]", "Executable, testable — faithful to DDD intent."),
]

table_top = Emu(1500000)
table_left = M_LEFT
col_widths = [Emu(2500000), Emu(3500000), Emu(5500000)]
row_height = Emu(500000)

table_shape = slide.shapes.add_table(
    len(rows_data), 3, table_left, table_top,
    sum(col_widths), row_height * len(rows_data)
)
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
    "THIS IS THE AHA SLIDE. Go row by row.\n"
    "\"If you know DDD, you already know TEOB. The mapping is 1:1.\"\n"
    "Emphasize: decide is the decision function, apply is the evolve/fold.\n"
    "\"Invariants are first-class — executable and testable, not just documentation.\"\n"
    "Pause here. Ask: \"Any questions before we see where TEOB goes beyond DDD?\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 12: Beyond the Blue Book
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "BEYOND THE BLUE BOOK")
add_accent_line(slide, Emu(1200000))

beyond = [
    ("Effect ADT", "DDD aggregates return events (or throw). TEOB returns a declarative Effect<Event, Reply> — a program describing what should happen."),
    ("Reply as first-class", "DDD aggregates are void or throw. TEOB: persist(...).andReply(...) atomically. CQRS-with-response."),
    ("EffectControl (ctx)", "In strict DDD, the aggregate is pure. ctx gives access to timers, cross-entity messaging, external effects."),
    ("Stash/Unstash", "Actor model concept (Akka heritage). Buffers commands during certain states."),
    ("Invariants", "Closer to DDD than most ES frameworks. Executable and testable — faithful to why the boundary exists."),
]
for i, (title, desc) in enumerate(beyond):
    y = Emu(1700000 + i * 900000)
    add_text(slide, M_LEFT, y, Emu(2800000), Emu(400000),
             title, font_size=18, bold=True, color=COLOR_BLUE)
    add_text(slide, Emu(3700000), y, Emu(8000000), Emu(700000),
             desc, font_size=15, color=COLOR_GRAY)

add_text(slide, M_LEFT, Emu(6200000), CONTENT_W, Emu(400000),
         "Core loop maps 1:1 to DDD. TEOB adds: effect system + actor model + infrastructure.",
         font_size=16, bold=True, color=COLOR_DARK)

add_notes(slide,
    "TIMING: 0:35–0:38\n"
    "\"The core is DDD. The extras are what make it practical.\"\n"
    "Don't go deep on Stash — mention it exists, move on.\n"
    "Emphasize Effect ADT and Reply — they'll use these immediately.\n"
    "\"ctx is your toolbox. In Exercise 1 you won't need it. In Exercise 2, it's everything.\""
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
    "Codecs — serialisable, on-the-wire representation (Command, Reply, Event, State)",
    "Agnostic to execution and persistence: scalability / durability / integrity",
    "Multiple runtimes: in-memory, SQLite, PostgreSQL, ... (same aggregate code)",
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
    "\"In the exercises, we use InMemoryRuntime. In production, swap to Postgres. Zero code changes.\"\n"
    "This is the payoff of the separation."
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 14: Exercise 1 Brief — Gift Card
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "EXERCISE 1: GIFT CARD AGGREGATE", color=COLOR_GREEN, font_size=34)
add_accent_line(slide, Emu(1200000), color=COLOR_GREEN)

# Domain model
add_code_box(slide,
    "Commands:  Issue | Redeem | Cancel | GetBalance\n"
    "Events:    Issued | Redeemed | Cancelled\n"
    "State:     { balance, status }",
    M_LEFT, Emu(1600000), Emu(6500000), Emu(1000000), font_size=17)

# Business rules
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

# Test command
add_code_box(slide,
    "npx vitest run workshop/exercise1-gift-card/gift-card.test.ts",
    M_LEFT, Emu(5400000), Emu(8500000), Emu(500000), font_size=16)

add_text(slide, Emu(9600000), Emu(5450000), Emu(3000000), Emu(500000),
         "15 tests.\nMake them green.", font_size=22, bold=True, color=COLOR_GREEN)

# Hint
add_text(slide, M_LEFT, Emu(6200000), CONTENT_W, Emu(400000),
         "Start with Issue → GetBalance → Redeem → Cancel → Invariants     |     Stuck? See HINTS.md",
         font_size=14, color=COLOR_LIGHT_GRAY)

add_notes(slide,
    "TIMING: 0:40–0:42\n"
    "LIVE DEMO: Open terminal, run the test command. Show 13 failing tests.\n"
    "\"Your job for the next 30 minutes: make them green.\"\n"
    "\"Start with Issue — it's the simplest. The hints are in the file.\"\n"
    "Walk through the file structure briefly: gift-card.ts has TODOs, tests tell you what to expect.\n"
    "\"Solution is in gift-card.solution.ts — but try first!\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 15: Exercise 1 — Work Time
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_DARK)
add_text(slide, M_LEFT, Emu(2200000), CONTENT_W, Emu(1000000),
         "EXERCISE 1: GIFT CARD", font_size=48, bold=True,
         color=COLOR_GREEN, alignment=PP_ALIGN.CENTER)
add_text(slide, M_LEFT, Emu(3400000), CONTENT_W, Emu(600000),
         "30 minutes  •  15 tests  •  implement decide() + invariants",
         font_size=22, color=COLOR_LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
add_text(slide, M_LEFT, Emu(4600000), CONTENT_W, Emu(400000),
         "npx vitest run workshop/exercise1-gift-card/gift-card.test.ts",
         font_size=16, color=COLOR_GREEN, alignment=PP_ALIGN.CENTER,
         font_name="SF Mono")

add_notes(slide,
    "TIMING: 0:42–1:12 (30 min work time)\n"
    "LEAVE THIS SLIDE UP during exercise.\n\n"
    "Walk the room / monitor chat.\n"
    "At 15 min: \"How many tests are green so far? Show of hands: more than 5?\"\n"
    "At 15 min: Show Hint 1 if people are stuck (the Issue case pattern).\n"
    "At 25 min: If significant portion stuck, live-code the Issue case on screen.\n"
    "At 28 min: \"2 minutes left — if you haven't finished, that's fine. We'll review together.\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 16: Exercise 1 Debrief
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "EXERCISE 1: DEBRIEF")
add_accent_line(slide, Emu(1200000))

add_text(slide, M_LEFT, Emu(1700000), CONTENT_W, Emu(400000),
         "What you just built:", font_size=20, bold=True, color=COLOR_DARK)

takeaways = [
    "decide() — all business logic in one place, pattern-matched on command tag",
    "apply() — pure state fold, no logic, just data transformation",
    "invariants[] — executable contracts that guard your aggregate's consistency",
    "Effect ADT — persist(), reply(), andReply() — declarative, composable",
    "AggregateTestKit — test without infrastructure, test the domain directly",
]
add_bullet_block(slide, takeaways, Emu(2300000), color=COLOR_DARK, font_size=17,
                 spacing=Emu(550000))

add_code_box(slide,
    "// The core pattern you'll use everywhere:\n"
    "if (invalid) return reply({ tag: 'Rejected', reason: '...' })\n"
    "return andReply(persist(event), { tag: 'Ok' })",
    M_LEFT, Emu(5300000), Emu(8500000), Emu(1000000), font_size=15)

add_notes(slide,
    "TIMING: 1:12–1:17\n"
    "Live-code the full solution if needed. Walk through each case.\n"
    "\"Notice: no database, no HTTP, no framework setup. Just domain logic.\"\n"
    "\"The test kit runs decide/apply in memory — pure unit tests.\"\n"
    "Ask: \"What surprised you? What felt different from how you usually write this?\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 17: Break
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
         "Next up: two aggregates talking to each other",
         font_size=18, color=COLOR_BLUE, alignment=PP_ALIGN.CENTER)

add_notes(slide,
    "TIMING: 1:17–1:22\n"
    "CRITICAL BREAK. People need to reset before the harder exercise.\n"
    "\"When we come back: the fun part — two aggregates communicating.\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 18: How Do Aggregates Talk?
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "HOW DO AGGREGATES TALK?")
add_accent_line(slide, Emu(1200000))

# Diagram: Order → Payment → Gateway
box_h = Emu(1200000)
box_w_agg = Emu(2800000)
box_w_gw = Emu(2200000)

add_box(slide, Emu(800000), Emu(2000000), box_w_agg, box_h,
        COLOR_BLUE, "Order\nAggregate", font_size=20)
add_box(slide, Emu(5000000), Emu(2000000), box_w_agg, box_h,
        COLOR_GREEN, "Payment\nAggregate", font_size=20, text_color=COLOR_WHITE)
add_box(slide, Emu(9200000), Emu(2000000), box_w_gw, box_h,
        COLOR_ORANGE, "Payment\nGateway", font_size=20, text_color=COLOR_WHITE)

# Arrows with labels
add_text(slide, Emu(3300000), Emu(1600000), Emu(2000000), Emu(400000),
         "ctx.tell(Charge)", font_size=14, color=COLOR_DARK,
         alignment=PP_ALIGN.CENTER, font_name="SF Mono")
add_text(slide, Emu(3300000), Emu(3300000), Emu(2000000), Emu(400000),
         "ctx.tell(Confirm)", font_size=14, color=COLOR_DARK,
         alignment=PP_ALIGN.CENTER, font_name="SF Mono")
add_text(slide, Emu(7500000), Emu(1600000), Emu(2000000), Emu(400000),
         "ctx.sync()", font_size=14, color=COLOR_DARK,
         alignment=PP_ALIGN.CENTER, font_name="SF Mono")

# Arrow shapes
add_arrow(slide, Emu(3700000), Emu(2200000), Emu(1200000), Emu(300000), COLOR_LIGHT_GRAY)
# Return arrow (left-pointing, we'll just use text)
add_text(slide, Emu(3700000), Emu(3000000), Emu(1200000), Emu(300000),
         "←←←←←←←←", font_size=16, color=COLOR_LIGHT_GRAY,
         alignment=PP_ALIGN.CENTER)
add_arrow(slide, Emu(7900000), Emu(2200000), Emu(1200000), Emu(300000), COLOR_LIGHT_GRAY)

# Explanation
explanations = [
    ("CategoryRegistration", "type-safe cross-entity contract (compile-time checked)"),
    ("ctx.tell()", "fire-and-forget command across aggregate boundaries"),
    ("ctx.sync()", "call external system, result comes back as a command (callback pattern)"),
    ("Key principle:", "commands cross boundaries, events stay within"),
]
for i, (term, desc) in enumerate(explanations):
    y = Emu(4000000 + i * 550000)
    add_text(slide, M_LEFT, y, Emu(2800000), Emu(400000),
             term, font_size=17, bold=True, color=COLOR_BLUE, font_name="SF Mono" if i < 3 else None)
    add_text(slide, Emu(3700000), y, Emu(8000000), Emu(400000),
             f"— {desc}", font_size=17, color=COLOR_GRAY)

add_notes(slide,
    "TIMING: 1:22–1:30\n"
    "\"In Exercise 1, your aggregate was alone. Now: two aggregates collaborate.\"\n"
    "Walk through the diagram left-to-right:\n"
    "1. Order receives PlaceOrder, persists OrderPlaced, tells Payment to Charge\n"
    "2. Payment receives Charge, calls gateway via ctx.sync()\n"
    "3. Gateway result comes back as a command (ChargeSucceeded/Failed)\n"
    "4. Payment tells Order: ConfirmPayment or RejectPayment\n\n"
    "KEY INSIGHT: \"Commands cross boundaries. Events stay within their aggregate.\"\n"
    "Ask: \"Why not just emit events and let the other aggregate listen?\" → Coupling, ordering, boundaries."
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 19: Exercise 2 Brief — Order + Payment
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "EXERCISE 2: ORDER + PAYMENT", color=COLOR_GREEN, font_size=34)
add_accent_line(slide, Emu(1200000), color=COLOR_GREEN)

# Two columns
add_text(slide, M_LEFT, Emu(1600000), Emu(5000000), Emu(400000),
         "Order (given — study this first)", font_size=20, bold=True, color=COLOR_GREEN)
order_items = [
    "PlaceOrder → persists OrderPlaced",
    "→ tells Payment to Charge",
    "→ waits for ConfirmPayment / RejectPayment callback",
]
add_bullet_block(slide, order_items, Emu(2100000), color=COLOR_DARK, font_size=16,
                 spacing=Emu(380000))

add_text(slide, M_LEFT, Emu(3400000), Emu(5000000), Emu(400000),
         "Payment (you build)", font_size=20, bold=True, color=COLOR_BLUE)
payment_items = [
    "Charge → persist ChargeRequested → ctx.sync(gateway)",
    "ChargeSucceeded → persist + ctx.tell(Order, ConfirmPayment)",
    "ChargeFailed → persist + ctx.tell(Order, RejectPayment)",
    "GetStatus → reply with current status",
]
add_bullet_block(slide, payment_items, Emu(3900000), color=COLOR_DARK, font_size=16,
                 spacing=Emu(380000))

# Test command
add_code_box(slide,
    "npx vitest run workshop/exercise2-order-payment/payment.test.ts",
    M_LEFT, Emu(5600000), Emu(8500000), Emu(500000), font_size=16)

add_text(slide, Emu(9600000), Emu(5650000), Emu(3000000), Emu(500000),
         "7 tests: 5 unit\n+ 2 integration", font_size=20, bold=True, color=COLOR_GREEN)

add_notes(slide,
    "TIMING: 1:30–1:35\n"
    "LIVE DEMO: Open order.ts and walk through the code.\n"
    "\"This is the pattern. Study PlaceOrder — see how andRun + ctx.tell works.\"\n"
    "\"Your job: implement the Payment side using the same patterns.\"\n"
    "\"The integration tests are the wow moment — two aggregates in one runtime, full flow.\"\n"
    "Hint: Start with GetStatus (easiest), then Charge, then the callbacks."
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 20: Exercise 2 — Work Time
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_DARK)
add_text(slide, M_LEFT, Emu(2200000), CONTENT_W, Emu(1000000),
         "EXERCISE 2: ORDER + PAYMENT", font_size=44, bold=True,
         color=COLOR_GREEN, alignment=PP_ALIGN.CENTER)
add_text(slide, M_LEFT, Emu(3400000), CONTENT_W, Emu(600000),
         "35 minutes  •  7 tests  •  implement Payment decide()",
         font_size=22, color=COLOR_LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
add_text(slide, M_LEFT, Emu(4600000), CONTENT_W, Emu(400000),
         "npx vitest run workshop/exercise2-order-payment/payment.test.ts",
         font_size=16, color=COLOR_GREEN, alignment=PP_ALIGN.CENTER,
         font_name="SF Mono")
add_text(slide, M_LEFT, Emu(5400000), CONTENT_W, Emu(400000),
         "Study order.ts first  •  Start with GetStatus  •  HINTS.md if stuck",
         font_size=16, color=COLOR_LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

add_notes(slide,
    "TIMING: 1:35–2:10 (35 min work time)\n"
    "LEAVE THIS SLIDE UP during exercise.\n\n"
    "At 10 min: \"Who has GetStatus passing?\" Show Hint 1 if needed.\n"
    "At 15 min: Show Hint 2 (the Charge case with ctx.sync pattern).\n"
    "At 25 min: If many stuck on callbacks, live-code ChargeSucceeded.\n"
    "At 30 min: \"5 minutes left. Focus on getting the unit tests green.\n"
    "            The integration tests are a bonus — we'll demo them together.\"\n"
    "At 33 min: \"Wrapping up in 2 minutes.\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 21: Exercise 2 Debrief
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "EXERCISE 2: DEBRIEF")
add_accent_line(slide, Emu(1200000))

add_text(slide, M_LEFT, Emu(1600000), CONTENT_W, Emu(400000),
         "What just happened in the integration test:", font_size=20, bold=True, color=COLOR_DARK)

flow_steps = [
    "1.  runtime.ask(order, PlaceOrder)  →  OrderPlaced persisted",
    "2.  Order.andRun()  →  ctx.tell(Payment, Charge)",
    "3.  Payment.decide(Charge)  →  ChargeRequested persisted  →  ctx.sync(gateway)",
    "4.  Gateway returns  →  ChargeSucceeded command delivered to Payment",
    "5.  Payment.decide(ChargeSucceeded)  →  ChargeCompleted persisted  →  ctx.tell(Order, ConfirmPayment)",
    "6.  Order.decide(ConfirmPayment)  →  PaymentConfirmed persisted  →  status: Confirmed",
]
for i, step in enumerate(flow_steps):
    y = Emu(2200000 + i * 530000)
    color = COLOR_BLUE if i % 2 == 0 else COLOR_GREEN
    add_text(slide, M_LEFT, y, CONTENT_W, Emu(400000),
             step, font_size=15, color=color, font_name="SF Mono")

add_text(slide, M_LEFT, Emu(5700000), CONTENT_W, Emu(400000),
         "Two aggregates, one runtime, full async flow — zero infrastructure code in your domain.",
         font_size=17, bold=True, color=COLOR_DARK)

add_notes(slide,
    "TIMING: 2:10–2:17\n"
    "LIVE DEMO: Run the integration test on screen. Show it passing.\n"
    "Walk through the 6-step flow on the slide.\n"
    "\"All of this happened with fire-and-forget commands. No HTTP, no message broker, no choreography.\"\n"
    "\"The runtime handles delivery. Your code just says ctx.tell().\"\n"
    "THIS IS THE WOW MOMENT. Let it land."
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 22: The Full Picture — Backend Service
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "THE FULL PICTURE: BACKEND SERVICE")
add_accent_line(slide, Emu(1200000))

layers = [
    ("Your code", "Aggregates (decide + apply), Projections, Sagas", COLOR_GREEN),
    ("TEOB framework", "Effect system, Runtime, Codecs, TestKit, CLI scaffolding", COLOR_BLUE),
    ("Persistence", "In-memory → SQLite → PostgreSQL (swap without code changes)", COLOR_ORANGE),
    ("Infrastructure", "Health checks, OpenTelemetry, auto-generated REST/OpenAPI", COLOR_LIGHT_GRAY),
]

for i, (layer, desc, color) in enumerate(layers):
    y = Emu(1700000 + i * 1100000)
    add_box(slide, M_LEFT, y, Emu(2500000), Emu(800000), color,
            text=layer, font_size=18, text_color=COLOR_WHITE)
    add_text(slide, Emu(3700000), y + Emu(200000), Emu(8000000), Emu(500000),
             desc, font_size=17, color=COLOR_DARK)

add_notes(slide,
    "TIMING: 2:17–2:20\n"
    "\"You just built the green layer. Everything else is provided.\"\n"
    "\"To go to production: swap InMemoryRuntime → PostgresRuntime, add ServiceTemplate, done.\"\n"
    "Quick mention of projections and sagas — \"that's the next workshop.\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 23: Battle Tested
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

add_notes(slide,
    "TIMING: 2:20–2:22\n"
    "Credibility slide. Keep it brief.\n"
    "\"This isn't a toy framework. The Scala version has been running fintech systems for 10+ years.\"\n"
    "\"The TypeScript port brings the same patterns to a broader ecosystem.\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 24: DSL- and AI-Friendly
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "DSL- AND AI-FRIENDLY")
add_accent_line(slide, Emu(1200000))

items = [
    "Native DSLs built on top (e.g. Petri Net flow modeling)",
    "Pure, concise, testable logics — ideal for AI code generation",
    "Zero boilerplate, no ORM",
    "Small, manageable contexts digestible by LLMs",
    "CLI scaffolding: teob new aggregate / projection / flow",
]
add_bullet_block(slide, items, Emu(1800000), color=COLOR_DARK, font_size=19,
                 spacing=Emu(700000))

add_notes(slide,
    "TIMING: 2:22–2:24 (optional — include if time allows)\n"
    "\"The pure functional style means AI assistants can generate aggregate code reliably.\"\n"
    "\"The CLI scaffolds a working aggregate in seconds.\""
)


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 25: TEOB Agentic Platform (teaser)
# ══════════════════════════════════════════════════════════════════════════

slide = prs.slides.add_slide(BLANK_LAYOUT)
set_bg(slide, BG_LIGHT)
add_title(slide, "TEOB AGENTIC PLATFORM")
add_accent_line(slide, Emu(1200000))

add_text(slide, M_LEFT, Emu(1700000), CONTENT_W, Emu(500000),
         "What happens when your aggregate IS an AI agent?",
         font_size=22, color=COLOR_GRAY)

agent_items = [
    "LLM integration — OpenAI, OpenRouter, any provider",
    "MCP tool registry with permission model",
    "RAG knowledge search (pgvector)",
    "Cross-session agent memory (event-sourced, naturally)",
    "Crash-resilient: agent state survives restarts — it's just events",
]
add_bullet_block(slide, agent_items, Emu(2500000), color=COLOR_DARK, font_size=18,
                 spacing=Emu(650000))

add_notes(slide,
    "TIMING: 2:24–2:26 (optional teaser)\n"
    "\"Event sourcing gives you time-travel, audit, replay for free.\n"
    " Now imagine your AI agent's entire conversation history, tool calls,\n"
    " and decisions are events. Crash? Replay from journal. Debug? Replay specific steps.\"\n"
    "Tease — don't go deep. This is a future workshop topic."
)


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
    ("Clone the repo", "github.com/timur/teob-ts  (npm install && npm test)", COLOR_GREEN),
    ("Try Exercise 3 at home", "Projections — build a read model from gift card events", COLOR_BLUE),
    ("Scaffold your own aggregate", "npx teob new aggregate  — working code in seconds", COLOR_BLUE),
    ("Watch the recording", "Link will be shared — includes solution walkthroughs", COLOR_ORANGE),
    ("Join the community", "Questions, feedback, next workshop announcements", COLOR_LIGHT_GRAY),
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
    "TIMING: 2:26–2:30\n"
    "\"You just built two event-sourced aggregates with cross-boundary communication.\n"
    " That's not a demo — that's the real pattern.\"\n\n"
    "Go through each CTA. If you have a QR code to the repo, show it now.\n"
    "\"Exercise 3 will be in the repo by next week\" — gives them a reason to come back.\n"
    "Open for questions.\n\n"
    "RECORDING NOTE: This is a good cut point for the video."
)


# ══════════════════════════════════════════════════════════════════════════
# Save
# ══════════════════════════════════════════════════════════════════════════

output_path = "/Users/timur/work/teob-ts/workshop/DDD-Workshop-Slides.pptx"
prs.save(output_path)
print(f"Saved {len(prs.slides)} slides to {output_path}")
