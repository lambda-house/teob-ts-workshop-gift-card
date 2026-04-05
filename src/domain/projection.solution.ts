/**
 * Gift Card Projection — SOLUTION
 *
 * Reference solution. Don't peek until you've tried!
 */

import type { EntityId } from "@lambda-house/teob-ts/core";
import { projection } from "@lambda-house/teob-ts/projection";

import type { GiftCardEvent, GiftCardView } from "./types.js";

export const giftCardProjection = projection<GiftCardEvent, GiftCardView>({
  projectionId: "gift-card-view",
  category: "gift-card",

  initialState: (): GiftCardView => ({
    balance: 0,
    status: "Empty",
    transactionCount: 0,
  }),

  evolve(view: GiftCardView, event: GiftCardEvent, _entityId: EntityId): GiftCardView {
    switch (event.tag) {
      case "Issued":
        return {
          ...view,
          balance: event.amount,
          status: "Active",
          recipientName: event.recipientName,
        };

      case "Redeemed": {
        const newBalance = view.balance - event.amount;
        return {
          ...view,
          balance: newBalance,
          status: newBalance === 0 ? "Empty" : "Active",
          transactionCount: view.transactionCount + 1,
        };
      }

      case "Cancelled":
        return {
          ...view,
          balance: 0,
          status: "Cancelled",
        };

      case "EncouragementSet":
        return {
          ...view,
          encouragement: event.text,
        };
    }
  },
});
