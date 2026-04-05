# Aggregate Hints

Work through these one at a time. Only read the next hint if you're stuck.

---

## Hint 1: The pattern for each command

Every `decide` case follows the same shape:

```typescript
case "SomeCommand":
  // 1. Check preconditions (state guards)
  if (state.status !== "Expected") {
    return reply({ tag: "Rejected", reason: "why" });
  }
  // 2. Persist event + reply
  return andReply(persist({ tag: "SomeEvent", ... }), { tag: "Ok" });
```

Start with `Issue`. The test expects:
- Events: `[{ tag: "Issued", amount: command.amount, recipientName: command.recipientName }]`
- Reply: `{ tag: "Ok" }`
- Guard: only allowed when `state.status === "Empty"`

---

## Hint 2: Issue + GetBalance solved

```typescript
case "Issue":
  if (state.status !== "Empty") {
    return reply({ tag: "Rejected", reason: "Card already issued" });
  }
  return andReply(
    persist({ tag: "Issued", amount: command.amount, recipientName: command.recipientName }),
    { tag: "Ok" },
  );

case "GetBalance":
  return reply({ tag: "Balance", amount: state.balance });
```

Now try `Redeem` — it has TWO guards:
1. Card must be Active
2. Amount must not exceed balance

---

## Hint 3: Redeem + Cancel solved

```typescript
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
```

Now do the invariants (Hint 4).

---

## Hint 4: Invariants

```typescript
invariants: [
  { name: "balance is non-negative", check: (state) => state.balance >= 0 },
  {
    name: "cancelled card has zero balance",
    check: (state) => state.status !== "Cancelled" || state.balance === 0,
  },
],
```

The second invariant reads: "if Cancelled, then balance MUST be 0."
Logical form: `status !== "Cancelled" || balance === 0` is equivalent to
`(status === "Cancelled") → (balance === 0)`.
