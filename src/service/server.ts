/**
 * Gift Card HTTP Service (pre-built)
 *
 * This wires your aggregate and projection into a real HTTP server.
 * You don't need to modify this file — it's here so you can see the full picture.
 *
 * Run: npm start
 *
 * Endpoints:
 *   POST /api/gift-card/:id         — send a command (Issue, Redeem, Cancel, GetBalance)
 *   GET  /api/gift-card/:id/view    — read the projected view for one card
 *   GET  /api/gift-cards            — list all projected views
 *   GET  /health                    — health check
 *
 * Examples:
 *   curl -X POST http://localhost:3000/api/gift-card/card-1 \
 *     -H "Content-Type: application/json" \
 *     -d '{"tag":"Issue","amount":100,"recipientName":"Alice"}'
 *
 *   curl -s http://localhost:3000/api/gift-card/card-1/view
 *   curl -s http://localhost:3000/api/gift-cards
 */

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { serveStatic } from "@hono/node-server/serve-static";
import { createInMemoryRuntime, registration } from "@lambda-house/teob-ts/inmem";
import { createInMemoryProjectionStore, runProjection } from "@lambda-house/teob-ts/projection";
import { aggregateRoutes } from "@lambda-house/teob-ts/http";
import { giftCardAggregate } from "../domain/aggregate.js";
import { giftCardProjection } from "../domain/projection.js";
import {
  giftCardCategory,
  giftCardEventCodec,
  giftCardStateCodec,
} from "../domain/types.js";

// ── Create runtime + projection store ──────────────────────────────────────

const { runtime, journal } = createInMemoryRuntime([
  registration(giftCardAggregate, giftCardEventCodec, giftCardStateCodec),
]);

const projectionStore = createInMemoryProjectionStore();

function refreshProjection() {
  runProjection(giftCardProjection, journal, projectionStore, {
    eventCodec: giftCardEventCodec,
  });
}

// ── Wire HTTP ──────────────────────────────────────────────────────────────

const app = new Hono();

// Health check
app.get("/health", (c) => c.json({ status: "ok" }));

// Aggregate command routes: POST /api/gift-card/:entityId
app.route("/api/gift-card", aggregateRoutes(runtime, giftCardCategory));

// Projection read routes
app.get("/api/gift-card/:entityId/view", (c) => {
  refreshProjection();
  const envelope = projectionStore.get(giftCardProjection.projectionId, c.req.param("entityId"));
  if (!envelope) return c.json({ error: "Not found" }, 404);
  return c.json(envelope.view);
});

app.get("/api/gift-cards", (c) => {
  refreshProjection();
  const envelopes = projectionStore.list(giftCardProjection.projectionId);
  return c.json(envelopes.map((e) => ({ id: e.viewId, ...e.view })));
});

// Static frontend
app.use("/*", serveStatic({ root: "./public" }));

// ── Start ──────────────────────────────────────────────────────────────────

await runtime.start();

serve({ fetch: app.fetch, port: 3000 }, () => {
  console.log("Gift Card Service running on http://localhost:3000");
  console.log("");
  console.log("  UI:      http://localhost:3000");
  console.log("");
  console.log("  Commands:");
  console.log('    curl -s -X POST http://localhost:3000/api/gift-card/card-1 \\');
  console.log('      -H "Content-Type: application/json" \\');
  console.log('      -d \'{"tag":"Issue","amount":100,"recipientName":"Alice"}\'');
  console.log("");
  console.log("  Read:");
  console.log("    curl -s http://localhost:3000/api/gift-card/card-1/view");
  console.log("    curl -s http://localhost:3000/api/gift-cards");
});
