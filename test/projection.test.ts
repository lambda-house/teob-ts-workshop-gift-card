/**
 * Gift Card Projection Tests
 *
 * These tests verify your projection's evolve function.
 * Make them pass by implementing `evolve` in src/domain/projection.ts.
 *
 * The tests call evolve() directly — it's a pure function,
 * no infrastructure needed.
 *
 * Run with:  npm run test:projection
 */

import { describe, it, expect } from "vitest";
import { EntityId } from "@lambda-house/teob-ts/core";
import { giftCardProjection } from "../src/domain/projection.js";
import type { GiftCardEvent, GiftCardView } from "../src/domain/types.js";

const { evolve, initialState } = giftCardProjection;
const cardId = EntityId("card-1");

function applyEvents(events: GiftCardEvent[]): GiftCardView {
  return events.reduce((view, event) => evolve(view, event, cardId), initialState());
}

// ── 1. Initial state ──────────────────────────────────────────────────────

describe("Initial state", () => {
  it("should start with zero balance and Empty status", () => {
    const view = initialState();
    expect(view.balance).toBe(0);
    expect(view.status).toBe("Empty");
    expect(view.transactionCount).toBe(0);
  });
});

// ── 2. Issued ──────────────────────────────────────────────────────────────

describe("Issued", () => {
  it("should set balance, status, and recipientName", () => {
    const view = applyEvents([
      { tag: "Issued", amount: 100, recipientName: "Alice" },
    ]);

    expect(view.balance).toBe(100);
    expect(view.status).toBe("Active");
    expect(view.recipientName).toBe("Alice");
    expect(view.transactionCount).toBe(0);
  });
});

// ── 3. Redeemed ────────────────────────────────────────────────────────────

describe("Redeemed", () => {
  it("should subtract amount and increment transactionCount", () => {
    const view = applyEvents([
      { tag: "Issued", amount: 100, recipientName: "Alice" },
      { tag: "Redeemed", amount: 30 },
    ]);

    expect(view.balance).toBe(70);
    expect(view.status).toBe("Active");
    expect(view.transactionCount).toBe(1);
  });

  it("should set status to Empty when balance reaches 0", () => {
    const view = applyEvents([
      { tag: "Issued", amount: 50, recipientName: "Bob" },
      { tag: "Redeemed", amount: 50 },
    ]);

    expect(view.balance).toBe(0);
    expect(view.status).toBe("Empty");
    expect(view.transactionCount).toBe(1);
  });

  it("should count multiple redemptions", () => {
    const view = applyEvents([
      { tag: "Issued", amount: 100, recipientName: "Carol" },
      { tag: "Redeemed", amount: 20 },
      { tag: "Redeemed", amount: 30 },
      { tag: "Redeemed", amount: 10 },
    ]);

    expect(view.balance).toBe(40);
    expect(view.transactionCount).toBe(3);
  });
});

// ── 4. Cancelled ───────────────────────────────────────────────────────────

describe("Cancelled", () => {
  it("should set balance to 0 and status to Cancelled", () => {
    const view = applyEvents([
      { tag: "Issued", amount: 75, recipientName: "Dave" },
      { tag: "Cancelled", remainingBalance: 75 },
    ]);

    expect(view.balance).toBe(0);
    expect(view.status).toBe("Cancelled");
    expect(view.recipientName).toBe("Dave");
  });
});

// ── 5. EncouragementSet ────────────────────────────────────────────────────

describe("EncouragementSet", () => {
  it("should set the encouragement text", () => {
    const view = applyEvents([
      { tag: "Issued", amount: 50, recipientName: "Eve" },
      { tag: "EncouragementSet", text: "You deserve something special!" },
    ]);

    expect(view.encouragement).toBe("You deserve something special!");
    expect(view.recipientName).toBe("Eve");
    expect(view.balance).toBe(50);
  });
});

// ── 6. Full lifecycle ──────────────────────────────────────────────────────

describe("Full lifecycle", () => {
  it("should project a complete card history", () => {
    const view = applyEvents([
      { tag: "Issued", amount: 200, recipientName: "Frank" },
      { tag: "EncouragementSet", text: "Enjoy your gift!" },
      { tag: "Redeemed", amount: 50 },
      { tag: "Redeemed", amount: 30 },
      { tag: "Cancelled", remainingBalance: 120 },
    ]);

    expect(view).toEqual({
      balance: 0,
      status: "Cancelled",
      recipientName: "Frank",
      encouragement: "Enjoy your gift!",
      transactionCount: 2,
    });
  });
});
