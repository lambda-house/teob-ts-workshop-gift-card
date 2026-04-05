/**
 * Gift Card Domain Types
 *
 * All types are defined here. Both the aggregate exercise and projection
 * exercise import from this file. The types include LLM encouragement
 * fields — you'll see these in action during the demo.
 */

import { CategoryId } from "@lambda-house/teob-ts/core";
import { categoryTypes } from "@lambda-house/teob-ts/core";
import { tagCodec, objectCodec } from "@lambda-house/teob-ts/core";

// ── State ──────────────────────────────────────────────────────────────────

export type CardStatus = "Empty" | "Active" | "Cancelled";

export interface GiftCardState {
  id: string;
  balance: number;
  status: CardStatus;
  recipientName?: string;
  encouragement?: string;
}

// ── Commands (what the outside world can ask) ──────────────────────────────

export type GiftCardCommand =
  | { tag: "Issue"; amount: number; recipientName: string }
  | { tag: "Redeem"; amount: number }
  | { tag: "Cancel" }
  | { tag: "GetBalance" }
  | { tag: "SetEncouragement"; text: string };   // ← callback from LLM (demo)

// ── Events (facts that happened) ───────────────────────────────────────────

export type GiftCardEvent =
  | { tag: "Issued"; amount: number; recipientName: string }
  | { tag: "Redeemed"; amount: number }
  | { tag: "Cancelled"; remainingBalance: number }
  | { tag: "EncouragementSet"; text: string };    // ← from LLM callback (demo)

// ── Replies (immediate responses to commands) ──────────────────────────────

export type GiftCardReply =
  | { tag: "Ok" }
  | { tag: "Balance"; amount: number }
  | { tag: "Rejected"; reason: string };

// ── Category registration (for HTTP routes and cross-entity messaging) ─────

export const giftCardCategory = categoryTypes<GiftCardCommand, GiftCardReply>(
  CategoryId("gift-card"),
);

// ── Codecs (serialization) ─────────────────────────────────────────────────

export const giftCardEventCodec = tagCodec<GiftCardEvent>(
  "Issued", "Redeemed", "Cancelled", "EncouragementSet",
);
export const giftCardStateCodec = objectCodec<GiftCardState>("GiftCardState");

// ── Projection view (the read model shape) ─────────────────────────────────

export interface GiftCardView {
  balance: number;
  status: string;
  recipientName?: string;
  encouragement?: string;
  transactionCount: number;
}
