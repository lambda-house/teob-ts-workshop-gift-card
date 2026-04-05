# Projection Hints

Work through these one at a time. Only read the next hint if you're stuck.

---

## Hint 1: The pattern is identical to apply()

`evolve(view, event)` works exactly like `apply(state, event)`:

```typescript
case "SomeEvent":
  return { ...view, changedField: newValue };
```

Start with `Issued`. The test expects:
- `balance` set to `event.amount`
- `status` set to `"Active"`
- `recipientName` set to `event.recipientName`

---

## Hint 2: Issued + EncouragementSet solved

```typescript
case "Issued":
  return {
    ...view,
    balance: event.amount,
    status: "Active",
    recipientName: event.recipientName,
  };

case "EncouragementSet":
  return { ...view, encouragement: event.text };
```

Now try `Redeemed` — the only difference from apply() is that the projection
also tracks `transactionCount`.

---

## Hint 3: Redeemed solved

```typescript
case "Redeemed": {
  const newBalance = view.balance - event.amount;
  return {
    ...view,
    balance: newBalance,
    status: newBalance === 0 ? "Empty" : "Active",
    transactionCount: view.transactionCount + 1,
  };
}
```

Note the `transactionCount` — this is data the aggregate state DOESN'T carry.
That's the point of a projection: the read model can include derived data
that's useful for queries but not needed for decisions.

---

## Hint 4: Cancelled solved

```typescript
case "Cancelled":
  return { ...view, balance: 0, status: "Cancelled" };
```

That's all four cases. Run the tests — they should all be green.
