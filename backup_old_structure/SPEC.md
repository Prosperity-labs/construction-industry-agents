Let users see operations happening in real time (jobs, steps, state changes) and explore details without leaving the page.

Users & Jobs

Ops/User: needs to know what’s running right now and where it’s stuck.

Engineer: needs to drill into a job’s timeline, logs, and inputs/outputs.

PM: wants a high-level overview: throughput, failures, recent trends.

Scope (v1)

In scope

Workflow Viewer (Graph)

DAG of nodes (steps) and edges (data/trigger flow).

Live status (idle/running/success/fail) with subtle animation on updates.

Live Event Stream

Subscribe via WebSocket or SSE; render events as they arrive.

Event types: job.started, step.started, step.completed, job.completed, job.failed, log.line.

Side Panel (Details Drawer)

When a node/job is selected: show metadata, last run, duration sparkline, and last 50 log lines (live).

Activity Feed

Compact, filterable list of recent events (with search by jobId/userId).

Out of scope

Historical analytics beyond a rolling 24h window.

Admin actions (retries/cancel) — placeholders only.

Non-Functional

Smooth at 5–10 events/sec on a dev laptop.

No backend schema changes required for v1; mock stream allowed.

No secrets; .env.example with optional EVENTS_URL.


Acceptance Criteria

Connects to event stream

Given EVENTS_URL (WebSocket wss://… or SSE http://…), the UI opens a connection and handles reconnect with backoff.

If EVENTS_URL is missing, a mock stream is used (deterministic demo data).

Workflow Graph renders from model

Given a workflow model (nodes, edges), graph renders with zoom/pan, node status badges, edge arrows.

Updating a node’s status via an incoming event updates the graph within 150ms.

Details Drawer

Clicking a node/job opens a right-side drawer with:

Name, current/last status, started/ended timestamps, duration

“Last 50 log lines” (live append)

“Related events” (from the feed), newest first

Activity Feed

Shows a time-ordered list with icons and colors per event type.

Filters: by jobId, eventType, status.

Docs & Dev Ergonomics

README has “Quickstart (UI only)” and “Quickstart (with mock stream)”.

docker-compose.yml includes an optional mock-events service.

Tests

Unit tests for event parsing and reconciler (state update logic).

Component test: renders graph; updates on incoming event.