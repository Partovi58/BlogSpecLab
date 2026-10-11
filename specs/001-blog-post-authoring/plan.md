# Implementation Plan: Blog Post Authoring and Publishing

**Branch**: `001-blog-post-authoring` | **Date**: 2025-05-18 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-blog-post-authoring/spec.md`

## Summary

This plan outlines the architecture and technical design for the Blog Post Authoring and Publishing feature in BlogSpecLab. The system enables authenticated authors to create, edit, and publish blog post drafts while ensuring strict access control (drafts are private to their owners) and immutable published post states. Readers can access published posts in reverse chronological order without exposure to drafts.

## Technical Context

**Language/Version**: Python 3.11+ / Node.js 20+ (Framework Agnostic, Domain-Driven Design)

**Primary Dependencies**: Standard Web Framework (FastAPI / Express / NestJS), Pydantic / Zod for Schema Validation

**Storage**: Relational DB (PostgreSQL / SQLite) storing Post entities with `status`, `author_id`, `created_at`, `updated_at`, and `published_at`

**Testing**: Pytest / Jest with TDD workflow (unit tests, integration tests, contract tests)

**Target Platform**: Linux Server / Web Service API

**Project Type**: Web Service / REST API

**Performance Goals**: API response latency p95 < 200ms under standard baseline load

**Constraints**:
- Strict validation: Reject empty or whitespace-only titles and contents
- Non-negotiable authorization: Only author-owner can edit/publish drafts
- Reversion prevention: Published posts cannot be edited or reverted to draft
- Privacy guarantee: Draft posts must never be accessible via reader/public routes

**Scale/Scope**: Core blogging capability supporting thousands of authors and public readers

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Technology & Environment Standards**: Deterministic lockfiles & explicit runtime versioning enforced.
- **II. Architectural Design & Boundaries**: Strict layer separation (Domain Entities, Application Services, Infrastructure/API Handlers). Direct repository access from HTTP handlers is prohibited.
- **III. Testing Standards**: Test-First / TDD mandatory. Minimum 80% line coverage and 75% branch coverage required. Unit tests run < 30s.
- **IV. Security & Compliance Rules**: Zero hardcoded secrets, strict schema validation for input payloads at boundaries, RBAC authorization based on `author_id`.
- **V. API Contracts**: OpenAPI 3.0 specification for endpoints, standard JSON envelope (`code`, `message`, `details`, `timestamp`), p95 < 200ms SLA.
- **VI. Quality Gates**: Zero linter errors, cyclomatic complexity <= 10, function length <= 50 lines.
- **VII. Git Workflow**: Conventional commits (`feat:`, `fix:`, `docs:`, etc.), PR limit <= 400 lines.

## Project Structure

### Documentation (this feature)

```text
specs/001-blog-post-authoring/
├── spec.md              # Feature specification
├── plan.md              # Technical implementation plan ($speckit-plan output)
```

### Source Code Architecture Layout

```text
src/
├── domain/
│   ├── models/
│   │   └── post.py              # Post entity, Status enum, domain invariants
│   └── exceptions/
│       └── post_exceptions.py   # Domain exceptions (Unauthorized, ImmutablePost, InvalidPayload)
├── application/
│   ├── services/
│   │   └── post_service.py      # Use cases: create_draft, edit_draft, publish_post, list_published
│   └── dto/
│       └── post_dto.py          # Input/Output DTOs
├── infrastructure/
│   ├── persistence/
│   │   └── post_repository.py   # Database persistence implementation
│   └── web/
│       ├── controllers/
│       │   ├── author_controller.py  # Author endpoints (/api/v1/author/posts)
│       │   └── reader_controller.py  # Reader endpoints (/api/v1/posts)
│       └── middlewares/
│           └── auth_middleware.py    # Authentication & Author context extraction
└── main.py

tests/
├── unit/
│   ├── domain/
│   └── application/
├── integration/
│   └── persistence/
└── contract/
    └── api/
```

**Structure Decision**: Clean Architecture / Layered Architecture separating core domain logic from application use cases, persistence infrastructure, and HTTP controllers.

## Data Model & State Transitions

### Post Entity Attributes
- `id` (UUID / String): Unique post identifier.
- `title` (String): Title (Non-empty, non-whitespace).
- `content` (String): Content body (Non-empty, non-whitespace).
- `status` (Enum: `DRAFT`, `PUBLISHED`): Lifecycle status.
- `author_id` (String/UUID): Immutable ID of creator.
- `created_at` (Timestamp): Creation time.
- `updated_at` (Timestamp): Last update time.
- `published_at` (Nullable Timestamp): Recorded at point of publication.

### State Transitions
1. `CREATE` -> `DRAFT` (Initial State)
2. `DRAFT` --(Owner Edit)--> `DRAFT` (Updated Title/Content)
3. `DRAFT` --(Owner Publish)--> `PUBLISHED` (`published_at` set to current server time)
4. `PUBLISHED` --(Any Attempt to Edit/Revert)--> **REJECTED (Immutable State)**

## API Contracts Design

### Author Endpoints (Authenticated)
- `POST /api/v1/author/posts`: Create draft post.
- `PUT /api/v1/author/posts/{id}`: Edit draft post (Owner only).
- `POST /api/v1/author/posts/{id}/publish`: Publish draft post (Owner only).

### Reader Endpoints (Public/Reader)
- `GET /api/v1/posts`: List published posts (Sorted by `published_at` DESC).
- `GET /api/v1/posts/{id}`: Retrieve single published post (Returns 404 if post is in `DRAFT`).

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No constitution violations. Architecture strictly follows layer separation and domain isolation.*
