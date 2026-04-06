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

    subgraph HTTP["HTTP Layer — Hono"]
        W["POST /api/gift-card/:entityId<br/>command in, reply out"]
        R1["GET /api/gift-card/:entityId/view<br/>single card projection"]
        R2["GET /api/gift-cards<br/>all projected views"]
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

    UI -- "POST commands" --> W
    UI -- "GET views (poll)" --> R2
    W --> D
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

## API Reference

### Write Side — Commands

```
POST /api/gift-card/:entityId
Content-Type: application/json
```

| Command          | Request Body                                            | Success (200)                  | Rejection (400)                   |
|------------------|---------------------------------------------------------|--------------------------------|-----------------------------------|
| Issue            | `{"tag":"Issue","amount":100,"recipientName":"Alice"}`  | `{"tag":"Ok"}`                 | `Card already issued`             |
| GetBalance       | `{"tag":"GetBalance"}`                                  | `{"tag":"Balance","amount":N}` | —                                 |
| Redeem           | `{"tag":"Redeem","amount":30}`                          | `{"tag":"Ok"}`                 | `Not active` / `Insufficient balance` |
| Cancel           | `{"tag":"Cancel"}`                                      | `{"tag":"Ok"}`                 | `Not active`                      |
| SetEncouragement | `{"tag":"SetEncouragement","text":"..."}`                | `200` (no reply body)          | —                                 |

All responses include an `ETag` header for optimistic concurrency.
Send `If-Match: <etag>` on subsequent commands to detect conflicts (409).

### Read Side — Projections

```
GET /api/gift-card/:entityId/view
```

Returns the projected view for one card:
```json
{ "balance": 70, "status": "Active", "recipientName": "Alice", "transactionCount": 1 }
```

```
GET /api/gift-cards
```

Returns all projected views:
```json
[{ "id": "card-1", "balance": 70, "status": "Active", "recipientName": "Alice", "transactionCount": 1 }]
```

## Service Wiring

```typescript
// Runtime + journal
const { runtime, journal } = createInMemoryRuntime([
  registration(giftCardAggregate, giftCardEventCodec, giftCardStateCodec),
]);

// Projection store
const projectionStore = createInMemoryProjectionStore();

// HTTP
const app = new Hono();
app.route("/api/gift-card", aggregateRoutes(runtime, giftCardCategory));

app.get("/api/gift-card/:entityId/view", (c) => {
  runProjection(giftCardProjection, journal, projectionStore, { eventCodec: giftCardEventCodec });
  const envelope = projectionStore.get("gift-card-view", c.req.param("entityId"));
  return envelope ? c.json(envelope.view) : c.json({ error: "Not found" }, 404);
});

app.get("/api/gift-cards", (c) => {
  runProjection(giftCardProjection, journal, projectionStore, { eventCodec: giftCardEventCodec });
  return c.json(projectionStore.list("gift-card-view").map(e => ({ id: e.viewId, ...e.view })));
});

// Static frontend
app.use("/*", serveStatic({ root: "./public" }));
```

Three pure functions → full-stack service. Write side, read side, UI, external integrations.
