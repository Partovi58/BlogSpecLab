# Tasks: Blog Post Authoring and Publishing

**Input**: Design documents from `specs/001-blog-post-authoring/`

**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic directory structure per plan.md

- [x] T001 Create project source directory structure `src/domain`, `src/application`, `src/infrastructure`, `tests` per implementation plan
- [x] T002 [P] Configure linter and code formatting tools per Constitution standards
- [x] T003 [P] Setup dependency management and project configuration

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Define Post domain entity, Status enum (`DRAFT`, `PUBLISHED`), and state invariant rules in `src/domain/models/post.py`
- [x] T005 [P] Define domain exceptions (e.g. `UnauthorizedException`, `ImmutablePostException`, `InvalidPayloadException`) in `src/domain/exceptions/post_exceptions.py`
- [x] T006 [P] Implement authentication context extraction middleware in `src/infrastructure/web/middlewares/auth_middleware.py`
- [x] T007 Define PostRepository interface and database persistence setup in `src/infrastructure/persistence/post_repository.py`
- [x] T008 Configure application DTO schemas and validation rules in `src/application/dto/post_dto.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel or sequentially.

---

## Phase 3: User Story 1 - Create Draft Post (Priority: P1) 🎯 MVP

**Goal**: Authenticated authors can create a new post with valid title and content initialized in `DRAFT` status and owned by the author.

**Independent Test**: Create a draft as an authenticated author, verify it is persisted with status `DRAFT`, owned by the author, and rejected if title/content is empty or whitespace.

### Tests for User Story 1

- [x] T009 [P] [US1] Unit test for draft creation domain rules and title/content validation in `tests/unit/domain/test_post_creation.py`
- [x] T010 [P] [US1] Integration/Contract test for `POST /api/v1/author/posts` endpoint in `tests/contract/api/test_create_draft.py`

### Implementation for User Story 1

- [x] T011 [US1] Implement `create_draft` use case in `src/application/services/post_service.py`
- [x] T012 [US1] Implement `POST /api/v1/author/posts` endpoint handler in `src/infrastructure/web/controllers/author_controller.py`
- [x] T013 [US1] Add payload sanitization and non-empty/whitespace validation logic in `src/application/dto/post_dto.py`

**Checkpoint**: User Story 1 (MVP) is fully functional and independently testable.

---

## Phase 4: User Story 2 - Edit Draft Post (Priority: P2)

**Goal**: Authors can edit the title and content of their existing draft posts while enforcing owner-only authorization and whitespace validation.

**Independent Test**: Edit an existing draft as its owner and verify updated title/content; attempt edit as non-owner or with whitespace payload and verify rejection without state modification.

### Tests for User Story 2

- [x] T014 [P] [US2] Unit test for draft editing domain rules and ownership validation in `tests/unit/domain/test_post_editing.py`
- [x] T015 [P] [US2] Integration/Contract test for `PUT /api/v1/author/posts/{id}` endpoint in `tests/contract/api/test_edit_draft.py`

### Implementation for User Story 2

- [x] T016 [US2] Implement `edit_draft` use case with author authorization check in `src/application/services/post_service.py`
- [x] T017 [US2] Implement `PUT /api/v1/author/posts/{id}` endpoint handler in `src/infrastructure/web/controllers/author_controller.py`

**Checkpoint**: User Story 2 is fully functional and independently testable alongside US1.

---

## Phase 5: User Story 3 - Publish Draft Post (Priority: P3)

**Goal**: Owners can publish a draft post, setting its status to `PUBLISHED` and recording the server timestamp. Published posts become immutable.

**Independent Test**: Publish a draft as its owner, verify `status` changes to `PUBLISHED` and `published_at` is set; attempt subsequent edits or reversion and verify strict rejection.

### Tests for User Story 3

- [x] T018 [P] [US3] Unit test for publishing state transition and immutability invariants in `tests/unit/domain/test_post_publishing.py`
- [x] T019 [P] [US3] Integration/Contract test for `POST /api/v1/author/posts/{id}/publish` endpoint in `tests/contract/api/test_publish_post.py`

### Implementation for User Story 3

- [x] T020 [US3] Implement `publish_post` use case with system timestamp recording in `src/application/services/post_service.py`
- [x] T021 [US3] Implement `POST /api/v1/author/posts/{id}/publish` endpoint handler in `src/infrastructure/web/controllers/author_controller.py`
- [x] T022 [US3] Enforce immutability checks for published posts in `src/domain/models/post.py`

**Checkpoint**: User Story 3 is fully functional and independently testable.

---

## Phase 6: User Story 4 - Reader View Published Posts (Priority: P4)

**Goal**: Readers can list published posts sorted from newest to oldest (`published_at` DESC) and view individual published posts. Drafts are never exposed.

**Independent Test**: Request reader post list and verify only published posts appear in reverse chronological order; attempt to fetch a draft post by ID via reader endpoint and verify 404/access denied.

### Tests for User Story 4

- [ ] T023 [P] [US4] Integration/Contract test for `GET /api/v1/posts` and `GET /api/v1/posts/{id}` in `tests/contract/api/test_reader_posts.py`

### Implementation for User Story 4

- [ ] T024 [US4] Implement `list_published_posts` and `get_published_post_by_id` use cases in `src/application/services/post_service.py`
- [ ] T025 [US4] Implement `GET /api/v1/posts` and `GET /api/v1/posts/{id}` endpoint handlers in `src/infrastructure/web/controllers/reader_controller.py`
- [ ] T026 [US4] Ensure database queries in `src/infrastructure/persistence/post_repository.py` strictly filter `status = 'PUBLISHED'` for reader queries

**Checkpoint**: User Story 4 is fully functional and draft isolation is verified.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final verification, quality gates, and documentation

- [ ] T027 [P] Verify zero linter/static analysis errors across `src/` and `tests/`
- [ ] T028 [P] Verify test coverage achieves >= 80% line coverage and >= 75% branch coverage
- [ ] T029 Execute full test suite and verify execution time < 30 seconds per Constitution rules

---

## Dependencies & Execution Order

1. **Setup (Phase 1)** -> **Foundational (Phase 2)** (CRITICAL BLOCKER)
2. **User Story 1 (P1)** -> **User Story 2 (P2)** -> **User Story 3 (P3)** -> **User Story 4 (P4)**
3. **Polish (Phase 7)** after all stories complete.
