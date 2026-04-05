/**
 * Gift Card HTTP Service (pre-built)
 *
 * This wires your aggregate into a real HTTP server.
 * You don't need to modify this file — it's here so you can see the full picture.
 *
 * Run: npm start
 *
 * Endpoints:
 *   POST /api/gift-card/:id   — send a command (Issue, Redeem, Cancel, GetBalance)
 *   GET  /health               — health check
 *
 * Examples:
 *   curl -X POST http://localhost:3000/api/gift-card/card-1 \
 *     -H "Content-Type: application/json" \
 *     -d '{"tag":"Issue","amount":100,"recipientName":"Alice"}'
 *
 *   curl -X POST http://localhost:3000/api/gift-card/card-1 \
 *     -H "Content-Type: application/json" \
 *     -d '{"tag":"GetBalance"}'
 *
 *   curl -X POST http://localhost:3000/api/gift-card/card-1 \
 *     -H "Content-Type: application/json" \
 *     -d '{"tag":"Redeem","amount":30}'
 */

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { createInMemoryRuntime, registration } from "@lambda-house/teob-ts/inmem";
import { aggregateRoutes } from "@lambda-house/teob-ts/http";
import { giftCardAggregate } from "../domain/aggregate.js";
import {
  giftCardCategory,
  giftCardEventCodec,
  giftCardStateCodec,
} from "../domain/types.js";

// ── Create runtime ─────────────────────────────────────────────────────────

const { runtime } = createInMemoryRuntime([
  registration(giftCardAggregate, giftCardEventCodec, giftCardStateCodec),
]);

// ── Wire HTTP ──────────────────────────────────────────────────────────────

const app = new Hono();

// Health check
app.get("/health", (c) => c.json({ status: "ok" }));

// Aggregate command routes: POST /api/gift-card/:entityId
app.route("/api/gift-card", aggregateRoutes(runtime, giftCardCategory));

// ── Start ──────────────────────────────────────────────────────────────────

await runtime.start();

serve({ fetch: app.fetch, port: 3000 }, () => {
  console.log("Gift Card Service running on http://localhost:3000");
  console.log("");
  console.log("Try:");
  console.log('  curl -s -X POST http://localhost:3000/api/gift-card/card-1 \\');
  console.log('    -H "Content-Type: application/json" \\');
  console.log('    -d \'{"tag":"Issue","amount":100,"recipientName":"Alice"}\'');
});
