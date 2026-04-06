/**
 * Gift Card + LLM Encouragement Demo
 *
 * This demonstrates how TEOB integrates with external LLM services
 * using the same ctx.sync() pattern you'd use for any external call.
 *
 * When a gift card is issued, the system calls OpenRouter to generate
 * a personalized encouragement message. The result comes back as a
 * command (SetEncouragement) and gets persisted as an event.
 *
 * Run: OPENROUTER_API_KEY=sk-... npm run demo:llm
 *
 * The LLM integration is just another ctx.sync() — the same pattern as
 * calling a payment gateway, a shipping API, or any external service.
 * Event sourcing gives you: retry, replay, audit trail — for free.
 */

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { CategoryId, EntityId, type EntityId as EntityIdType, right } from "@lambda-house/teob-ts/core";
import type { Aggregate, Either } from "@lambda-house/teob-ts/core";
import type { Effect } from "@lambda-house/teob-ts/core";
import type { EffectControl } from "@lambda-house/teob-ts/core";
import { persist, reply, done, andReply, andRun } from "@lambda-house/teob-ts/core";
import { createInMemoryRuntime, registration } from "@lambda-house/teob-ts/inmem";

import type {
  GiftCardState,
  GiftCardCommand,
  GiftCardEvent,
  GiftCardReply,
} from "../domain/types.js";
import {
  giftCardCategory,
  giftCardEventCodec,
  giftCardStateCodec,
} from "../domain/types.js";

// ── OpenRouter LLM call ────────────────────────────────────────────────────

declare const process: { env: Record<string, string | undefined> };
const OPENROUTER_API_KEY = process.env.OPENROUTER_API_KEY;

async function generateEncouragement(
  recipientName: string, amount: number,
): Promise<Either<string, { text: string }>> {
  if (!OPENROUTER_API_KEY) {
    return right({ text: `Congratulations ${recipientName}! Enjoy your $${amount} gift card!` });
  }

  const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${OPENROUTER_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "openai/gpt-4o-mini",
      messages: [{
        role: "user",
        content: `Write a short, warm, personal encouragement message (2-3 sentences) for ${recipientName} who just received a $${amount} gift card. Be genuine, not generic.`,
      }],
      max_tokens: 100,
    }),
  });

  const data = await response.json() as any;
  const text = data.choices?.[0]?.message?.content ?? `Enjoy your $${amount} gift card, ${recipientName}!`;
  return right({ text });
}

// ── Enhanced aggregate with LLM integration ────────────────────────────────

const giftCardWithLLM: Aggregate<
  GiftCardCommand,
  GiftCardReply,
  GiftCardEvent,
  GiftCardState
> = {
  category: CategoryId("gift-card"),

  initial(id: EntityIdType): GiftCardState {
    return { id, balance: 0, status: "Empty" };
  },

  async decide(
    state: GiftCardState,
    command: GiftCardCommand,
    ctx: EffectControl<GiftCardCommand, GiftCardReply>,
  ): Promise<Effect<GiftCardEvent, GiftCardReply>> {
    switch (command.tag) {
      // ── Issue: persist + trigger LLM encouragement generation ──────
      case "Issue": {
        if (state.status !== "Empty") {
          return reply({ tag: "Rejected", reason: "Card already issued" });
        }
        // Persist the Issued event, then fire off the LLM call.
        // ctx.sync() calls the LLM and delivers the result as a command.
        return andReply(
          andRun(
            persist({ tag: "Issued", amount: command.amount, recipientName: command.recipientName }),
            async () => {
              await ctx.sync<{ text: string }, string>({
                effect: () => generateEncouragement(command.recipientName, command.amount),
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

      case "Redeem":
        if (state.status !== "Active") {
          return reply({ tag: "Rejected", reason: "Card is not active" });
        }
        if (command.amount > state.balance) {
          return reply({ tag: "Rejected", reason: "Insufficient balance" });
        }
        return andReply(persist({ tag: "Redeemed", amount: command.amount }), { tag: "Ok" });

      case "Cancel":
        if (state.status !== "Active") {
          return reply({ tag: "Rejected", reason: "Card is not active" });
        }
        return andReply(
          persist({ tag: "Cancelled", remainingBalance: state.balance }),
          { tag: "Ok" },
        );

      case "GetBalance":
        return reply({ tag: "Balance", amount: state.balance });

      case "SetEncouragement":
        return persist({ tag: "EncouragementSet", text: command.text });
    }
  },

  apply(state: GiftCardState, event: GiftCardEvent): GiftCardState {
    switch (event.tag) {
      case "Issued":
        return { ...state, balance: event.amount, status: "Active", recipientName: event.recipientName };
      case "Redeemed":
        return { ...state, balance: state.balance - event.amount, status: state.balance - event.amount === 0 ? "Empty" : "Active" };
      case "Cancelled":
        return { ...state, balance: 0, status: "Cancelled" };
      case "EncouragementSet":
        return { ...state, encouragement: event.text };
    }
  },

  invariants: [
    { name: "balance is non-negative", check: (state) => state.balance >= 0 },
    { name: "cancelled card has zero balance", check: (state) => state.status !== "Cancelled" || state.balance === 0 },
  ],
};

// ── Wire HTTP (REST → TEOB commands) ──────────────────────────────────────

import { createInMemoryProjectionStore, runProjection } from "@lambda-house/teob-ts/projection";
import { giftCardProjection } from "../domain/projection.js";

const { runtime, journal } = createInMemoryRuntime([
  registration(giftCardWithLLM, giftCardEventCodec, giftCardStateCodec),
]);

const projectionStore = createInMemoryProjectionStore();

function refreshProjection() {
  runProjection(giftCardProjection, journal, projectionStore, {
    eventCodec: giftCardEventCodec,
  });
}

async function sendCommand(entityId: string, command: GiftCardCommand) {
  const result = await runtime.ask(
    EntityId(entityId), command, giftCardCategory,
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

const app = new Hono();
app.get("/health", (c) => c.json({ status: "ok" }));

app.post("/api/gift-cards", async (c) => {
  const body = await c.req.json<{ id?: string; amount?: number; recipientName?: string }>();
  if (!body.id || !body.amount || !body.recipientName) {
    return c.json({ error: "Required: id, amount, recipientName" }, 400);
  }
  const result = await sendCommand(body.id, {
    tag: "Issue", amount: body.amount, recipientName: body.recipientName,
  });
  if (!result.ok) return c.json({ error: result.error.tag }, 500);
  if (result.reply?.tag === "Rejected") return c.json({ error: result.reply.reason }, 400);
  return c.json(getView(body.id), 201);
});

app.get("/api/gift-cards/:cardId", (c) => {
  const view = getView(c.req.param("cardId"));
  if (!view) return c.json({ error: "Not found" }, 404);
  return c.json(view);
});

await runtime.start();

serve({ fetch: app.fetch, port: 3000 }, () => {
  console.log("Gift Card + LLM Demo running on http://localhost:3000");
  console.log(OPENROUTER_API_KEY ? "  OpenRouter API key found — using real LLM" : "  No API key — using fallback messages");
  console.log("");
  console.log("  Try:");
  console.log('    curl -s -X POST http://localhost:3000/api/gift-cards \\');
  console.log('      -H "Content-Type: application/json" \\');
  console.log('      -d \'{"id":"card-1","amount":100,"recipientName":"Alice"}\'');
  console.log("");
  console.log("    # Wait a moment for LLM, then:");
  console.log("    curl -s http://localhost:3000/api/gift-cards/card-1");
});
