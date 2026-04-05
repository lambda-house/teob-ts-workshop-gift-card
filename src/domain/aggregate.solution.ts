/**
 * Gift Card Aggregate — SOLUTION
 *
 * Reference solution. Don't peek until you've tried!
 */

import { CategoryId, type EntityId } from "@lambda-house/teob-ts/core";
import type { Aggregate } from "@lambda-house/teob-ts/core";
import type { Effect } from "@lambda-house/teob-ts/core";
import type { EffectControl } from "@lambda-house/teob-ts/core";
import { persist, reply, andReply } from "@lambda-house/teob-ts/core";

import type {
  GiftCardState,
  GiftCardCommand,
  GiftCardEvent,
  GiftCardReply,
} from "./types.js";

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

  async decide(
    state: GiftCardState,
    command: GiftCardCommand,
    _ctx: EffectControl<GiftCardCommand, GiftCardReply>,
  ): Promise<Effect<GiftCardEvent, GiftCardReply>> {
    switch (command.tag) {
      case "Issue":
        if (state.status !== "Empty") {
          return reply({ tag: "Rejected", reason: "Card already issued" });
        }
        return andReply(
          persist({ tag: "Issued", amount: command.amount, recipientName: command.recipientName }),
          { tag: "Ok" },
        );

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

  invariants: [
    { name: "balance is non-negative", check: (state) => state.balance >= 0 },
    {
      name: "cancelled card has zero balance",
      check: (state) => state.status !== "Cancelled" || state.balance === 0,
    },
  ],
};
