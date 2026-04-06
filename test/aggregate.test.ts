/**
 * Gift Card Aggregate Tests
 *
 * These tests describe the expected behaviour of your gift card aggregate.
 * Make them pass by implementing `decide` and `invariants` in src/domain/aggregate.ts.
 *
 * Run with:  npm run test:aggregate
 */

import { describe, it, expect } from "vitest";
import { EntityId } from "@lambda-house/teob-ts/core";
import { createAggregateTestKit } from "@lambda-house/teob-ts/testing";
import { giftCardAggregate } from "../src/domain/aggregate.js";

const kit = createAggregateTestKit(giftCardAggregate);

// ── 1. Issuing a gift card ─────────────────────────────────────────────────

describe("Issue", () => {
  it("should issue a new gift card with the given balance", async () => {
    const { result, newState } = await kit.runAndApply(
      kit.initialState,
      { tag: "Issue", amount: 100, recipientName: "Alice" },
    );

    expect(result.events).toEqual([{ tag: "Issued", amount: 100, recipientName: "Alice" }]);
    expect(result.reply).toEqual({ tag: "Ok" });
    expect(newState.balance).toBe(100);
    expect(newState.status).toBe("Active");
    expect(newState.recipientName).toBe("Alice");
  });

  it("should reject issuing an already active card", async () => {
    const activeCard = { ...kit.initialState, balance: 50, status: "Active" as const };

    const { result } = await kit.run(activeCard, { tag: "Issue", amount: 200, recipientName: "Bob" });

    expect(result.events).toEqual([]);
    expect(result.reply).toEqual({ tag: "Rejected", reason: "Card already issued" });
  });
});

// ── 2. Querying balance ────────────────────────────────────────────────────

describe("GetBalance", () => {
  it("should return current balance without producing events", async () => {
    const card = { ...kit.initialState, balance: 75, status: "Active" as const };

    const { result } = await kit.run(card, { tag: "GetBalance" });

    expect(result.events).toEqual([]);
    expect(result.reply).toEqual({ tag: "Balance", amount: 75 });
  });
});

// ── 3. Redeeming ───────────────────────────────────────────────────────────

describe("Redeem", () => {
  it("should redeem within balance", async () => {
    const card = { ...kit.initialState, balance: 100, status: "Active" as const };

    const { result, newState } = await kit.runAndApply(card, { tag: "Redeem", amount: 30 });

    expect(result.events).toEqual([{ tag: "Redeemed", amount: 30 }]);
    expect(result.reply).toEqual({ tag: "Ok" });
    expect(newState.balance).toBe(70);
    expect(newState.status).toBe("Active");
  });

  it("should redeem exact balance (card becomes Empty)", async () => {
    const card = { ...kit.initialState, balance: 50, status: "Active" as const };

    const { newState } = await kit.runAndApply(card, { tag: "Redeem", amount: 50 });

    expect(newState.balance).toBe(0);
    expect(newState.status).toBe("Empty");
  });

  it("should reject redeem exceeding balance", async () => {
    const card = { ...kit.initialState, balance: 20, status: "Active" as const };

    const { result } = await kit.run(card, { tag: "Redeem", amount: 50 });

    expect(result.events).toEqual([]);
    expect(result.reply).toEqual({ tag: "Rejected", reason: "Insufficient balance" });
  });

  it("should reject redeem on an empty card", async () => {
    const { result } = await kit.run(kit.initialState, { tag: "Redeem", amount: 10 });

    expect(result.events).toEqual([]);
    expect(result.reply).toEqual({ tag: "Rejected", reason: "Card is not active" });
  });

  it("should reject redeem on a cancelled card", async () => {
    const cancelled = { ...kit.initialState, balance: 0, status: "Cancelled" as const };

    const { result } = await kit.run(cancelled, { tag: "Redeem", amount: 10 });

    expect(result.events).toEqual([]);
    expect(result.reply).toEqual({ tag: "Rejected", reason: "Card is not active" });
  });
});

// ── 4. Cancellation ────────────────────────────────────────────────────────

describe("Cancel", () => {
  it("should cancel an active card", async () => {
    const card = { ...kit.initialState, balance: 60, status: "Active" as const };

    const { result, newState } = await kit.runAndApply(card, { tag: "Cancel" });

    expect(result.events).toEqual([{ tag: "Cancelled", remainingBalance: 60 }]);
    expect(result.reply).toEqual({ tag: "Ok" });
    expect(newState.balance).toBe(0);
    expect(newState.status).toBe("Cancelled");
  });

  it("should reject cancelling an already cancelled card", async () => {
    const cancelled = { ...kit.initialState, balance: 0, status: "Cancelled" as const };

    const { result } = await kit.run(cancelled, { tag: "Cancel" });

    expect(result.events).toEqual([]);
    expect(result.reply).toEqual({ tag: "Rejected", reason: "Card is not active" });
  });
});

// ── 5. Multi-step scenario ─────────────────────────────────────────────────

describe("Gift card lifecycle", () => {
  it("issue → redeem → redeem → cancel", async () => {
    let state = kit.initialState;

    // Issue
    const r1 = await kit.runAndApply(state, { tag: "Issue", amount: 100, recipientName: "Alice" });
    state = r1.newState;
    expect(state.balance).toBe(100);
    expect(state.recipientName).toBe("Alice");

    // First redeem
    const r2 = await kit.runAndApply(state, { tag: "Redeem", amount: 40 });
    state = r2.newState;
    expect(state.balance).toBe(60);

    // Second redeem
    const r3 = await kit.runAndApply(state, { tag: "Redeem", amount: 25 });
    state = r3.newState;
    expect(state.balance).toBe(35);

    // Cancel
    const r4 = await kit.runAndApply(state, { tag: "Cancel" });
    state = r4.newState;
    expect(state.balance).toBe(0);
    expect(state.status).toBe("Cancelled");

    // Can't redeem after cancel
    const r5 = await kit.run(state, { tag: "Redeem", amount: 10 });
    expect(r5.result.reply).toEqual({ tag: "Rejected", reason: "Card is not active" });
  });
});

// ── 6. Invariants ──────────────────────────────────────────────────────────

describe("Invariants", () => {
  it("should define at least 2 invariants", () => {
    expect(giftCardAggregate.invariants).toBeDefined();
    expect(giftCardAggregate.invariants!.length).toBeGreaterThanOrEqual(2);
  });

  it("all invariants should pass on initial state", () => {
    for (const inv of giftCardAggregate.invariants!) {
      expect(inv.check(kit.initialState)).toBe(true);
    }
  });

  it("all invariants should pass on a valid active card", () => {
    const valid = { ...kit.initialState, balance: 50, status: "Active" as const };
    for (const inv of giftCardAggregate.invariants!) {
      expect(inv.check(valid)).toBe(true);
    }
  });

  it("balance invariant should catch negative balance", () => {
    const invalid = { ...kit.initialState, balance: -10, status: "Active" as const };
    const balanceInv = giftCardAggregate.invariants!.find(
      (i) => i.name.toLowerCase().includes("negative") || i.name.toLowerCase().includes("balance"),
    );
    expect(balanceInv).toBeDefined();
    expect(balanceInv!.check(invalid)).toBe(false);
  });

  it("cancelled invariant should catch cancelled card with balance", () => {
    const invalid = { ...kit.initialState, balance: 50, status: "Cancelled" as const };
    const cancelledInv = giftCardAggregate.invariants!.find(
      (i) => i.name.toLowerCase().includes("cancel"),
    );
    expect(cancelledInv).toBeDefined();
    expect(cancelledInv!.check(invalid)).toBe(false);
  });
});
