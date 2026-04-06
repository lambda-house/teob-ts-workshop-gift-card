# Architecture — Gift Card Service

A complete event-sourced backend service built with TEOB, Hono, and TypeScript.
Three pure functions define the entire domain. The framework handles HTTP routing,
event persistence, concurrency control, and external service integration.

## The Full Picture

```mermaid
graph TB
    subgraph Browser["Browser — localhost:3000"]
        UI["public/index.html<br/>Single-page UI"]
    end

    subgraph HTTP["HTTP Layer — Hono (REST → TEOB commands)"]
        W1["POST /api/gift-cards → Issue"]
        W2["POST /api/gift-cards/:id/redeem → Redeem"]
        W3["POST /api/gift-cards/:id/cancel → Cancel"]
        R1["GET /api/gift-cards/:id"]
        R2["GET /api/gift-cards"]
        H["GET /health"]
        S["GET /* — static files"]
    end

    subgraph Runtime["In-Memory Entity Runtime"]
        subgraph Write["Write Side — Aggregate"]
            D["decide(state, cmd) → Effect"]
            A["apply(state, event) → State"]
            I["Invariants<br/>• balance ≥ 0<br/>• cancelled → balance = 0"]
        end
        J[(Journal<br/>events per entity)]
        subgraph Read["Read Side — Projection"]
            E["evolve(view, event) → View"]
            PS[(Projection Store<br/>views per entity)]
        end
    end

    UI -- "POST" --> W1
    UI -- "POST" --> W2
    UI -- "POST" --> W3
    UI -- "GET (poll)" --> R2
    W1 --> D
    W2 --> D
    W3 --> D
    D -- "persist(event)" --> J
    J -- "replay" --> A
    A --> I
    J -- "allEvents()" --> E
    E --> PS
    R1 --> PS
    R2 --> PS

    style Write fill:#052e16,stroke:#14532d,color:#fff
    style Read fill:#172554,stroke:#1e3a8a,color:#fff
    style J fill:#1c1917,stroke:#44403c,color:#fff
    style PS fill:#1c1917,stroke:#44403c,color:#fff
```

## Write Side — Aggregate (Exercise 1)

```mermaid
graph LR
    subgraph Commands
        C1["Issue(amount, recipient)"]
        C2["Redeem(amount)"]
        C3["Cancel"]
        C4["GetBalance"]
        C5["SetEncouragement(text)"]
    end

    subgraph decide["decide(state, command) → Effect"]
        G1{"status = Empty?"}
        G2{"status = Active?<br/>amount ≤ balance?"}
        G3{"status = Active?"}
    end

    subgraph Events
        E1["Issued"]
        E2["Redeemed"]
        E3["Cancelled"]
        E4["EncouragementSet"]
    end

    subgraph Replies
        OK["Ok"]
        BAL["Balance(amount)"]
        REJ["Rejected(reason)"]
    end

    C1 --> G1
    G1 -- yes --> E1 & OK
    G1 -- no --> REJ
    C2 --> G2
    G2 -- yes --> E2 & OK
    G2 -- no --> REJ
    C3 --> G3
    G3 -- yes --> E3 & OK
    G3 -- no --> REJ
    C4 --> BAL
    C5 --> E4
```

## Read Side — Projection (Exercise 2)

```mermaid
graph LR
    subgraph Events
        E1["Issued"]
        E2["Redeemed"]
        E3["Cancelled"]
        E4["EncouragementSet"]
    end

    subgraph evolve["evolve(view, event) → View"]
        direction TB
        V["GiftCardView<br/>balance, status,<br/>recipientName,<br/>encouragement,<br/>transactionCount"]
    end

    E1 -- "set balance, status=Active,<br/>recipientName" --> V
    E2 -- "subtract amount,<br/>increment txn count" --> V
    E3 -- "balance=0,<br/>status=Cancelled" --> V
    E4 -- "set encouragement<br/>text" --> V
```

## LLM Integration (Demo)

```mermaid
sequenceDiagram
    participant Client
    participant Aggregate
    participant Journal
    participant OpenRouter as OpenRouter API

    Client->>Aggregate: Issue(amount, recipientName)
    Aggregate->>Journal: persist(Issued)
    Aggregate-->>Client: reply(Ok)

    Note over Aggregate: andRun: async side effect

    Aggregate->>OpenRouter: POST /v1/chat/completions<br/>"Write a warm message for Alice..."
    OpenRouter-->>Aggregate: "You deserve something special!"

    Note over Aggregate: ctx.sync() delivers result as command

    Aggregate->>Aggregate: SetEncouragement(text)
    Aggregate->>Journal: persist(EncouragementSet)

    Note over Aggregate: Same pattern for: payment gateway,<br/>shipping API, email, etc.<br/>ctx.sync() handles retry, replay, audit trail.
```

## API Reference (see `openapi.yaml`)

The HTTP surface is a clean REST API. Internally, each endpoint maps to a TEOB command.

| Endpoint                             | Method | TEOB Command    | Request Body                          | Response            |
|--------------------------------------|--------|-----------------|---------------------------------------|---------------------|
| `/api/gift-cards`                    | POST   | Issue           | `{"id","amount","recipientName"}`     | 201 GiftCardView    |
| `/api/gift-cards`                    | GET    | —               | —                                     | 200 GiftCardView[]  |
| `/api/gift-cards/:cardId`            | GET    | — (projection)  | —                                     | 200 GiftCardView    |
| `/api/gift-cards/:cardId/redeem`     | POST   | Redeem          | `{"amount"}`                          | 200 GiftCardView    |
| `/api/gift-cards/:cardId/cancel`     | POST   | Cancel          | —                                     | 200 GiftCardView    |
| `/health`                            | GET    | —               | —                                     | 200 `{"status":"ok"}` |

Commands are an **internal** concept — the REST surface doesn't expose them.
All write endpoints return the updated view, so the client never needs a separate read after a mutation.

## Service Wiring

```typescript
// Runtime + journal
const { runtime, journal } = createInMemoryRuntime([
  registration(giftCardAggregate, giftCardEventCodec, giftCardStateCodec),
]);
const projectionStore = createInMemoryProjectionStore();

// REST → TEOB command mapping
app.post("/api/gift-cards", async (c) => {
  const { id, amount, recipientName } = await c.req.json();
  const result = await runtime.ask(EntityId(id),
    { tag: "Issue", amount, recipientName }, giftCardCategory);
  // ... map result to REST response
});

app.post("/api/gift-cards/:cardId/redeem", async (c) => {
  const { amount } = await c.req.json();
  const result = await runtime.ask(EntityId(c.req.param("cardId")),
    { tag: "Redeem", amount }, giftCardCategory);
  // ...
});
```

The REST layer is a thin mapping. Domain logic stays in pure functions.
The OpenAPI spec (`openapi.yaml`) is the contract — use it to generate clients or frontends.
