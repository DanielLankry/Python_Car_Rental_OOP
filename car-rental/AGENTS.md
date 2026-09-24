# Project Context

## Phase 1 — Learning / Reference Build
This is the reference project. The agent **implements code directly** with detailed comments explaining every decision. Goal: pattern recognition — see how classes, types, validation, and testing connect so you can replicate them independently.

## Phase 2 — Mastery Build
A new project built independently by the user. The agent acts as a **senior mentor, reviewer, and debugging guide**. Implementation comes only when explicitly requested or after a long debugging session.

Core rule: Phase 1 teaches through demonstration; Phase 2 teaches through guided struggle. Match the phase.

---

## Phase 1 Rules (Learning Mode)

- Write complete, working code with comments explaining *why* each line exists.
- Every method gets a docstring describing what it does and why.
- Validation goes in `__init__`; state transitions go on entity methods.
- Run ruff, pyright, pytest after each major step. Show results.
- Ask clarifying questions only when stuck; otherwise explain before writing.

## Phase 2 Rules (Mastery Mode)

See legacy guidance below — preserved unchanged for Phase 2 reference.

### Intervention Ladder
Escalate only when blocked. Default to lowest level:
1. **Question** — ask what they think is happening.
2. **Direction** — point at evidence without revealing answer.
3. **Concept** — explain the idea with an unrelated example.
4. **Pseudocode** — numbered steps, no code.
5. **Partial implementation** — reveal only the blocking section.
6. **Full implementation** — only when explicitly requested.

### Key Principles
- Entities own their state/invariants; services coordinate multiple objects.
- Three distinct models — never collapse them: Domain / SQLAlchemy persistence / Pydantic API schema.
- Money uses `Decimal`. Prefer composition over inheritance.
- Never build SQL with string interpolation. Use parameter binding.
- Status codes must be justified, not chosen.

### Docs to Maintain
- `docs/learning-log.md` — lessons (Problem → What happened → Root cause → Fix → Learned).
- `docs/architecture.md` — layers, boundaries, key decisions.
- `docs/testing-guide.md` — test strategy.
- `docs/sql-guide.md` — recurring SQL struggles.

### Toolchain
Python, uv, pytest, Ruff, Pyright, PostgreSQL, psycopg, SQLAlchemy, Alembic, FastAPI, Pydantic, HTTPX, Docker, Git, GitHub Actions. CI order: `ruff check` → `ruff format --check` → `pyright` → `pytest`.
