/**
 * Gift Card HTTP Service (pre-built)
 *
 * REST API defined by openapi.yaml — proper endpoints, no leaked commands.
 * Internally maps to TEOB aggregate commands.
 *
 * Run: npm start
 *
 * Endpoints (see openapi.yaml for full spec):
 *   POST /api/gift-cards              — issue a new card
 *   GET  /api/gift-cards              — list all cards
 *   GET  /api/gift-cards/:cardId      — get one card
 *   POST /api/gift-cards/:cardId/redeem  — redeem from a card
 *   POST /api/gift-cards/:cardId/cancel  — cancel a card
 *   GET  /health                      — health check
 */

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { serveStatic } from "@hono/node-server/serve-static";
import { EntityId, persist, reply, andReply, andRun, right } from "@lambda-house/teob-ts/core";
import type { Aggregate, Effect, EffectControl, Either } from "@lambda-house/teob-ts/core";
import { createInMemoryRuntime, registration } from "@lambda-house/teob-ts/inmem";
import { createInMemoryProjectionStore, runProjection } from "@lambda-house/teob-ts/projection";
import { giftCardAggregate } from "../domain/aggregate.js";
import { giftCardProjection } from "../domain/projection.js";
import {
  giftCardCategory,
  giftCardEventCodec,
  giftCardStateCodec,
  type GiftCardCommand,
  type GiftCardEvent,
  type GiftCardReply,
  type GiftCardState,
} from "../domain/types.js";

// ── Mock encouragement service (simulates external API call) ──────────────
//
// Same ctx.sync() pattern you'd use for a payment gateway, shipping API,
// or real LLM. The mock just returns a templated message.

const encouragements = [
  (n: string, a: number) => `Hey ${n}! You've got $${a} to spend — treat yourself to something special!`,
  (n: string, a: number) => `${n}, someone believes you deserve a $${a} treat. And they're absolutely right!`,
  (n: string, a: number) => `A little something for ${n} — $${a} of pure possibility. What will it be?`,
  (n: string, a: number) => `${n}, $${a} is waiting for you. Go find something that makes you smile!`,
  (n: string, a: number) => `For ${n}: $${a} and a reminder that you're worth celebrating.`,
];

async function mockEncouragementService(
  recipientName: string, amount: number,
): Promise<Either<string, { text: string }>> {
  // Simulate async network latency
  await new Promise((r) => setTimeout(r, 200));
  const template = encouragements[Math.floor(Math.random() * encouragements.length)]!;
  const text = template(recipientName, amount);
  console.log(`  ← Encouragement generated for ${recipientName}`);
  return right({ text });
}

// ── Aggregate + sync effect ───────────────────────────────────────────────
//
// Wraps your aggregate with an andRun + ctx.sync() call on Issue.
// After persisting Issued, the mock service runs asynchronously.
// ctx.sync() delivers the result as a SetEncouragement command —
// which flows back through decide() and becomes an EncouragementSet event.

const giftCardWithEffects: Aggregate<
  GiftCardCommand, GiftCardReply, GiftCardEvent, GiftCardState
> = {
  category: giftCardAggregate.category,
  initial: giftCardAggregate.initial,
  apply: giftCardAggregate.apply,
  invariants: giftCardAggregate.invariants,

  async decide(
    state: GiftCardState,
    command: GiftCardCommand,
    ctx: EffectControl<GiftCardCommand, GiftCardReply>,
  ): Promise<Effect<GiftCardEvent, GiftCardReply>> {
    // Issue: add async encouragement generation via ctx.sync()
    if (command.tag === "Issue") {
      if (state.status !== "Empty") {
        return reply({ tag: "Rejected", reason: "Card already issued" });
      }
      console.log(`  → Issuing card for ${command.recipientName}, triggering encouragement...`);
      return andReply(
        andRun(
          persist({ tag: "Issued", amount: command.amount, recipientName: command.recipientName }),
          async () => {
            // ctx.sync: call external service, deliver result as a command
            await ctx.sync<{ text: string }, string>({
              effect: () => mockEncouragementService(command.recipientName, command.amount),
              onSuccess: (result) => ({
                tag: "SetEncouragement" as const,
                text: result.text,
              }),
              onFailure: () => ({
                tag: "SetEncouragement" as const,
                text: `Enjoy your $${command.amount} gift card, ${command.recipientName}!`,
              }),
            });
          },
        ),
        { tag: "Ok" },
      );
    }
    // All other commands: delegate to your aggregate
    return giftCardAggregate.decide(state, command, ctx);
  },
};

// ── Create runtime + projection store ──────────────────────────────────────

const { runtime, journal } = createInMemoryRuntime([
  registration(giftCardWithEffects, giftCardEventCodec, giftCardStateCodec),
]);

const projectionStore = createInMemoryProjectionStore();

function refreshProjection() {
  runProjection(giftCardProjection, journal, projectionStore, {
    eventCodec: giftCardEventCodec,
  });
}

// ── Command helper ─────────────────────────────────────────────────────────

async function sendCommand(entityId: string, command: GiftCardCommand) {
  const result = await runtime.ask(
    EntityId(entityId),
    command,
    giftCardCategory,
  );
  if (!result.ok) return { ok: false as const, error: result.error };
  return { ok: true as const, reply: result.value.reply as GiftCardReply | undefined };
}

function getView(cardId: string) {
  refreshProjection();
  const envelope = projectionStore.get(giftCardProjection.projectionId, cardId);
  if (!envelope) return null;
  return { id: cardId, ...(envelope.view as Record<string, unknown>) };
}

// ── Wire HTTP (REST → TEOB commands) ───────────────────────────────────────

const app = new Hono();

// Health
app.get("/health", (c) => c.json({ status: "ok" }));

// POST /api/gift-cards — issue a new card
app.post("/api/gift-cards", async (c) => {
  const body = await c.req.json<{ id?: string; amount?: number; recipientName?: string }>();
  if (!body.id || !body.amount || !body.recipientName) {
    return c.json({ error: "Required: id, amount, recipientName" }, 400);
  }

  const result = await sendCommand(body.id, {
    tag: "Issue",
    amount: body.amount,
    recipientName: body.recipientName,
  });

  if (!result.ok) return c.json({ error: result.error.tag }, 500);
  if (result.reply?.tag === "Rejected") return c.json({ error: result.reply.reason }, 400);

  // Wait for the async encouragement (ctx.sync) to complete before returning
  await new Promise((r) => setTimeout(r, 300));
  const view = getView(body.id);
  return c.json(view, 201);
});

// GET /api/gift-cards — list all cards
app.get("/api/gift-cards", (c) => {
  refreshProjection();
  const envelopes = projectionStore.list(giftCardProjection.projectionId);
  return c.json(envelopes.map((e) => ({ id: e.viewId, ...(e.view as Record<string, unknown>) })));
});

// GET /api/gift-cards/:cardId — get one card
app.get("/api/gift-cards/:cardId", (c) => {
  const view = getView(c.req.param("cardId"));
  if (!view) return c.json({ error: "Not found" }, 404);
  return c.json(view);
});

// POST /api/gift-cards/:cardId/redeem
app.post("/api/gift-cards/:cardId/redeem", async (c) => {
  const cardId = c.req.param("cardId");
  const body = await c.req.json<{ amount?: number }>();
  if (!body.amount) return c.json({ error: "Required: amount" }, 400);

  const result = await sendCommand(cardId, { tag: "Redeem", amount: body.amount });

  if (!result.ok) return c.json({ error: result.error.tag }, 500);
  if (result.reply?.tag === "Rejected") return c.json({ error: result.reply.reason }, 400);

  return c.json(getView(cardId));
});

// POST /api/gift-cards/:cardId/cancel
app.post("/api/gift-cards/:cardId/cancel", async (c) => {
  const cardId = c.req.param("cardId");

  const result = await sendCommand(cardId, { tag: "Cancel" });

  if (!result.ok) return c.json({ error: result.error.tag }, 500);
  if (result.reply?.tag === "Rejected") return c.json({ error: result.reply.reason }, 400);

  return c.json(getView(cardId));
});

// Static frontend
app.use("/*", serveStatic({ root: "./public" }));

// ── Start ──────────────────────────────────────────────────────────────────

await runtime.start();

serve({ fetch: app.fetch, port: 3000 }, () => {
  console.log("Gift Card Service running on http://localhost:3000");
  console.log("");
  console.log("  UI:   http://localhost:3000");
  console.log("  Spec: openapi.yaml");
  console.log("");
  console.log("  Try:");
  console.log('    curl -s -X POST http://localhost:3000/api/gift-cards \\');
  console.log('      -H "Content-Type: application/json" \\');
  console.log('      -d \'{"id":"card-1","amount":100,"recipientName":"Alice"}\'');
  console.log("");
  console.log("    # Wait a moment for the encouragement to arrive, then:");
  console.log("    curl -s http://localhost:3000/api/gift-cards/card-1");
  console.log("");
  console.log("  ctx.sync() flow: Issue → persist → mock service → SetEncouragement → persist");
});
