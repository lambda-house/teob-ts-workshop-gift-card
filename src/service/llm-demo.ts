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
import { CategoryId, EntityId, type EntityId as EntityIdType } from "@lambda-house/teob-ts/core";
import type { Aggregate } from "@lambda-house/teob-ts/core";
import type { Effect } from "@lambda-house/teob-ts/core";
import type { EffectControl } from "@lambda-house/teob-ts/core";
import { persist, reply, done, andReply, andRun } from "@lambda-house/teob-ts/core";
import { createInMemoryRuntime, registration } from "@lambda-house/teob-ts/inmem";
import { aggregateRoutes } from "@lambda-house/teob-ts/http";

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

const OPENROUTER_API_KEY = process.env.OPENROUTER_API_KEY;

async function generateEncouragement(recipientName: string, amount: number): Promise<string> {
  if (!OPENROUTER_API_KEY) {
    return `Congratulations ${recipientName}! Enjoy your $${amount} gift card!`;
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
  return data.choices?.[0]?.message?.content ?? `Enjoy your $${amount} gift card, ${recipientName}!`;
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
              await ctx.sync({
                effect: () => generateEncouragement(command.recipientName, command.amount)
                  .then(text => ({ text })),
                onSuccess: (result) => ({
                  tag: "SetEncouragement" as const,
                  text: result.text,
                }),
                onFailure: (_reason) => ({
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

// ── Wire HTTP ──────────────────────────────────────────────────────────────

const { runtime } = createInMemoryRuntime([
  registration(giftCardWithLLM, giftCardEventCodec, giftCardStateCodec),
]);

const app = new Hono();
app.get("/health", (c) => c.json({ status: "ok" }));
app.route("/api/gift-card", aggregateRoutes(runtime, giftCardCategory));

await runtime.start();

serve({ fetch: app.fetch, port: 3000 }, () => {
  console.log("Gift Card + LLM Demo running on http://localhost:3000");
  console.log(OPENROUTER_API_KEY ? "OpenRouter API key found" : "No API key — using fallback messages");
  console.log("");
  console.log("Try:");
  console.log('  curl -s -X POST http://localhost:3000/api/gift-card/card-1 \\');
  console.log('    -H "Content-Type: application/json" \\');
  console.log('    -d \'{"tag":"Issue","amount":100,"recipientName":"Alice"}\'');
  console.log("");
  console.log("  # Wait a moment for LLM, then check the balance:");
  console.log('  curl -s -X POST http://localhost:3000/api/gift-card/card-1 \\');
  console.log('    -H "Content-Type: application/json" \\');
  console.log('    -d \'{"tag":"GetBalance"}\'');
});
