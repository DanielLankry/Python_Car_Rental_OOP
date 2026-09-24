# Roadmap

Canonical build order. Work top-to-bottom; check off items as they complete. The first unchecked item is the next step.

## Phase 1 — Python & OOP (no framework, no DB)

- [ ] `Vehicle` entity: `id`, `manufacturer`, `model`, `year`, `daily_rate`, `status` (`AVAILABLE`/`RENTED`/`MAINTENANCE`); methods `rent()`, `return_vehicle()`, `send_to_maintenance()`
- [ ] `Customer` entity: `id`, `first_name`, `last_name`, `email`, `license_number`; validation, invariants
- [ ] `Rental` entity: `id`, `customer`, `vehicle`, `start_date`, `end_date`, `status`; state machine `RESERVED → ACTIVE → COMPLETED` / `RESERVED → CANCELLED`; methods `start()`, `complete()`, `cancel()`, `duration_days()`
- [ ] Unit tests for every entity and transition (valid + invalid)
- [ ] `PricingStrategy` Protocol + `StandardPricing`, `PremiumPricing`, `LongTermPricing`
- [ ] `RentalService`: `create_rental`, `start_rental`, `complete_rental`, `cancel_rental`
- [ ] Repository Protocols (`VehicleRepository`, `CustomerRepository`, `RentalRepository`) + `InMemory*` implementations
- [ ] `PaymentGateway` Protocol + mock (`success` / `decline` / `exception` / `timeout`)
- [ ] `logging` for meaningful events (created/started/completed/cancelled, payment failed, invalid transition, db op failed)
- [ ] Centralized config (`DATABASE_URL`, `LOG_LEVEL`, `ENVIRONMENT`); no secrets committed

## Phase 2 — PostgreSQL (raw)

- [ ] PostgreSQL running via Docker
- [ ] Manually create/query `customers`, `vehicles`, `rentals`, `payments` (PK, FK, NOT NULL, UNIQUE, CHECK, indexes)
- [ ] Work SQL curriculum in order: SELECT/WHERE/ORDER BY/LIMIT → INSERT/UPDATE/DELETE → INNER/LEFT JOIN → aggregates → GROUP BY/HAVING → NULL/COALESCE → subqueries/CTEs → CASE → date ops → transactions → window functions → indexes/EXPLAIN

## Phase 3 — psycopg

- [ ] `create_vehicle()`, `get_vehicle()`, `list_vehicles()` with parameter binding

## Phase 4 — SQLAlchemy 2.x

- [ ] `*DBModel` persistence models (`Mapped`, `mapped_column`, relationships)
- [ ] `Session`, `select()`, transactions, identity map / unit of work
- [ ] `SqlAlchemy*Repository` implementations — service untouched

## Phase 5 — Alembic

- [ ] Initial migration
- [ ] Practice: add `license_plate`, add `created_at`, add index, change constraint — never recreate the DB

## Phase 6 — FastAPI

- [ ] Endpoints: `GET /health`; vehicles CRUD; `POST /customers`, `GET /customers/{id}`; rentals create/get + start/complete/cancel
- [ ] Separate Pydantic schemas (`*Create`, `*Update`, `*Response`)
- [ ] Semantic status codes (201/200/404/409/422/500), justified

## Phase 7 — API tests

- [ ] pytest + HTTPX/TestClient: success, malformed, missing, invalid state, duplicates, lifecycle, payment failure, filtering, pagination

## Phase 8 — Filtering & pagination

- [ ] `GET /vehicles?status=` / `?manufacturer=`, `?limit=&offset=`, `GET /rentals?customer_id=` — filter in DB where appropriate

## Phase 9 — Overlapping reservations

- [ ] Booking-overlap constraint across SQL → repository → service → exception → API → pytest, one layer at a time

## Phase 10 — Docker

- [ ] `docker compose up` starts API + PostgreSQL

## Phase 11 — CI

- [ ] GitHub Actions: checkout → uv install → `uv sync` → `ruff check` → `ruff format --check` → `pyright` → `pytest`
- [ ] PostgreSQL integration tests in CI later

## Parallel tracks (continuous)

- [ ] Python LeetCode track (Arrays & Hashing, Two Pointers, Sliding Window, Stack, Binary Search, Linked Lists, Intervals, Heap)
- [ ] SQL LeetCode track (schema-reading practice)
- [ ] Unfamiliar-code exercises (infer contracts from tests/callers)
- [ ] Debugging drills (signature, return type, None, import, off-by-one dates, JOIN, transaction, fixture, mock, state transition, Pydantic)
- [ ] Maintain `docs/learning-log.md`, `docs/architecture.md`, `docs/testing-guide.md`, `docs/sql-guide.md`

## Final readiness test

- [ ] Unfamiliar repo (src/ + tests/ + pyproject.toml + schema) with failing tests — fix without AI implementation help
- [ ] Competency checklist answered from memory (see spec §56)
