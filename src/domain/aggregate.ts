/**
 * Gift Card Aggregate — Exercise
 *
 * A gift card that can be issued with a balance, redeemed, and cancelled.
 *
 * YOUR TASK:
 *   1. Implement the `decide` function — the decision logic
 *   2. Add invariants to the aggregate
 *
 * The domain types (types.ts) and `apply` (event handler) are given.
 * The tests tell you exactly what behaviour is expected.
 *
 * Key concept: decide() is a PURE FUNCTION.
 *   It looks at (state, command) and returns an Effect describing what should happen.
 *   No database, no HTTP, no side effects — just logic.
 */

import { CategoryId, type EntityId } from "@lambda-house/teob-ts/core";
import type { Aggregate, Invariant } from "@lambda-house/teob-ts/core";
import type { Effect } from "@lambda-house/teob-ts/core";
import type { EffectControl } from "@lambda-house/teob-ts/core";
import { persist, reply, done, andReply } from "@lambda-house/teob-ts/core";

import type {
  GiftCardState,
  GiftCardCommand,
  GiftCardEvent,
  GiftCardReply,
} from "./types.js";

// ── Aggregate ──────────────────────────────────────────────────────────────

export const giftCardAggregate: Aggregate<
  GiftCardCommand,
  GiftCardReply,
  GiftCardEvent,
  GiftCardState
> = {
  category: CategoryId("gift-card"),

  initial(id: EntityId): GiftCardState {
    return { id, balance: 0, status: "Empty" };
  },

  // ╔══════════════════════════════════════════════════════════════════════╗
  // ║  TODO: Implement the decision function                              ║
  // ║                                                                     ║
  // ║  Business rules:                                                    ║
  // ║  - Issue: only if status is "Empty", persist Issued event           ║
  // ║  - Redeem: only if "Active", amount must not exceed balance         ║
  // ║  - Cancel: only if "Active", records remaining balance              ║
  // ║  - GetBalance: always returns current balance (no events)           ║
  // ║  - SetEncouragement: persist EncouragementSet (no guards needed)    ║
  // ║                                                                     ║
  // ║  Use:                                                               ║
  // ║    andReply(persist(event), replyValue)  — persist + reply          ║
  // ║    reply(replyValue)                     — reply without events     ║
  // ║    persist(event)                        — persist only (no reply)  ║
  // ╚══════════════════════════════════════════════════════════════════════╝

  async decide(
    state: GiftCardState,
    command: GiftCardCommand,
    _ctx: EffectControl<GiftCardCommand, GiftCardReply>,
  ): Promise<Effect<GiftCardEvent, GiftCardReply>> {
    switch (command.tag) {
      // TODO: implement each case
      // Hint: start with "Issue", then "GetBalance", then "Redeem", then "Cancel"

      case "Issue":
        throw new Error("TODO: implement Issue");

      case "Redeem":
        throw new Error("TODO: implement Redeem");

      case "Cancel":
        throw new Error("TODO: implement Cancel");

      case "GetBalance":
        throw new Error("TODO: implement GetBalance");

      case "SetEncouragement":
        // This one is given — it's used by the LLM demo
        return persist({ tag: "EncouragementSet", text: command.text });
    }
  },

  // ── Event handler (given — pure state transition) ────────────────────

  apply(state: GiftCardState, event: GiftCardEvent): GiftCardState {
    switch (event.tag) {
      case "Issued":
        return {
          ...state,
          balance: event.amount,
          status: "Active",
          recipientName: event.recipientName,
        };
      case "Redeemed":
        return {
          ...state,
          balance: state.balance - event.amount,
          status: state.balance - event.amount === 0 ? "Empty" : "Active",
        };
      case "Cancelled":
        return { ...state, balance: 0, status: "Cancelled" };
      case "EncouragementSet":
        return { ...state, encouragement: event.text };
    }
  },

  // ╔══════════════════════════════════════════════════════════════════════╗
  // ║  TODO: Add invariants                                               ║
  // ║                                                                     ║
  // ║  1. "balance is non-negative" — balance must always be >= 0         ║
  // ║  2. "cancelled card has zero balance" — if Cancelled, balance is 0  ║
  // ╚══════════════════════════════════════════════════════════════════════╝

  invariants: [
    // TODO: add invariants here
    // Example: { name: "my invariant", check: (state) => state.someField >= 0 }
  ],
};
