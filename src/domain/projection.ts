/**
 * Gift Card Projection — Exercise
 *
 * A read model that builds a view from gift card events.
 *
 * YOUR TASK:
 *   Implement the `evolve` function — the view builder.
 *
 * Key concept: evolve() is a PURE FUNCTION, just like apply().
 *   It takes (currentView, event) and returns the new view.
 *   But unlike apply() which builds aggregate state for decisions,
 *   evolve() builds a READ MODEL optimized for queries.
 *
 * The view can include derived data that the aggregate state doesn't carry:
 *   - transactionCount (how many redeems happened)
 *   - Data from multiple event types combined into a flat structure
 */

import type { EntityId } from "@lambda-house/teob-ts/core";
import { projection } from "@lambda-house/teob-ts/projection";

import type { GiftCardEvent, GiftCardView } from "./types.js";

// ── Projection ─────────────────────────────────────────────────────────────

export const giftCardProjection = projection<GiftCardEvent, GiftCardView>({
  projectionId: "gift-card-view",
  category: "gift-card",

  initialState: (): GiftCardView => ({
    balance: 0,
    status: "Empty",
    transactionCount: 0,
  }),

  // ╔══════════════════════════════════════════════════════════════════════╗
  // ║  TODO: Implement the evolve function                                ║
  // ║                                                                     ║
  // ║  For each event, return a new view with the relevant fields         ║
  // ║  updated. Same pattern as apply() — switch on event.tag.            ║
  // ║                                                                     ║
  // ║  "Issued":                                                          ║
  // ║    - Set balance, status to "Active", recipientName                 ║
  // ║                                                                     ║
  // ║  "Redeemed":                                                        ║
  // ║    - Subtract amount from balance                                   ║
  // ║    - Update status: "Empty" if balance reaches 0, else "Active"     ║
  // ║    - Increment transactionCount                                     ║
  // ║                                                                     ║
  // ║  "Cancelled":                                                       ║
  // ║    - Set balance to 0, status to "Cancelled"                        ║
  // ║                                                                     ║
  // ║  "EncouragementSet":                                                ║
  // ║    - Set encouragement text                                         ║
  // ╚══════════════════════════════════════════════════════════════════════╝

  evolve(view: GiftCardView, event: GiftCardEvent, _entityId: EntityId): GiftCardView {
    switch (event.tag) {
      // TODO: implement each case
      // Hint: same pattern as apply() — return { ...view, changed fields }

      case "Issued":
        throw new Error("TODO: implement Issued");

      case "Redeemed":
        throw new Error("TODO: implement Redeemed");

      case "Cancelled":
        throw new Error("TODO: implement Cancelled");

      case "EncouragementSet":
        throw new Error("TODO: implement EncouragementSet");
    }
  },
});
