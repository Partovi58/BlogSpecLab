# Project Constitution

## Core Principles

### I. Technology & Environment Standards (فناوری)
- **Deterministic Dependencies**: All projects must use strict lockfiles (`package-lock.json`, `poetry.lock`, `Cargo.lock`, etc.). Unpinned dependency versions are prohibited.
- **Runtime Standardization**: Core runtimes and language versions must be explicitly pinned in project configuration files (e.g., `.nvmrc`, `.python-version`, or `Dockerfiles`).
- **Dependency Audit**: Zero high or critical security vulnerabilities allowed in production dependencies (automated vulnerability audit checks must pass with exit code 0).

### II. Architectural Design & Boundaries (معماری)
- **Loose Coupling & High Cohesion**: System components must follow strict layer separation (Domain, Application, Infrastructure). Direct access from presentation/API layers to database repositories without service layer mediation is strictly forbidden.
- **Library-First & Modular Design**: Any business logic shared across two or more domains must be extracted into an isolated, self-contained, documented module/library with explicit public interfaces.
- **Stateless Application Tier**: Application services must remain stateless. All persistent states must reside in approved external databases or caches.

### III. Testing Standards & Coverage Gates (قواعد تست)
- **Test-Driven Development (TDD) / Test-First**: Tests must be written and confirmed failing before implementation code is written for any new feature or bug fix.
- **Mandatory Coverage Threshold**: Code coverage must maintain a minimum of 80% line coverage and 75% branch coverage across the codebase. Pull requests lowering overall coverage are automatically rejected.
- **Test Execution & Isolation**: Unit test suites must execute rapidly (under 30 seconds locally); all unit and integration tests must execute predictably without external un-mocked network dependencies.

### IV. Security & Compliance Rules (امنیت)
- **Zero Hardcoded Credentials**: Any commit containing API keys, passwords, private keys, or credentials will fail CI/CD immediately (enforced via pre-commit hooks and automated secret scanners).
- **Strict Input Validation**: All external inputs (HTTP queries, body payloads, CLI arguments) must be sanitized and validated against a strict schema at the system boundary before processing.
- **Principle of Least Privilege & Encryption**: All external and inter-service communications must use encrypted protocols (TLS 1.3). APIs must strictly enforce Authentication & Role-Based Access Control (RBAC).

### V. API Contracts & Specifications (API)
- **Schema-Driven API Contracts**: Every API endpoint must be documented via OpenAPI 3.0+ or JSON Schema specifications. Undocumented public endpoints are non-compliant.
- **Backward Compatibility & Versioning**: All breaking changes to public APIs require major version increments (`/v1/` to `/v2/`) and a minimum deprecation notice window.
- **Standardized Response Protocols**: API responses must follow standardized JSON envelopes containing `code`, `message`, `details`, and `timestamp`. HTTP status codes must strictly conform to standard RFC specifications.
- **Performance SLA**: API response latency must maintain p95 < 200ms for standard read/write operations under baseline load tests.

### VI. Quality Gates & Maintainability (کیفیت)
- **Zero Linter Warnings/Errors**: Code must pass strict linter and static analysis checks with zero warnings or errors prior to merging.
- **Complexity Limits**: Cyclomatic complexity per function or method must not exceed 10. Functions exceeding 50 lines of code must be refactored into smaller sub-units.
- **Automated Code Formatting**: Code style must be enforced automatically via automated formatting tools (e.g. Prettier, Black, ESLint, Rustfmt) prior to commit.

### VII. Git Workflow & Release Governance (Git)
- **Conventional Commits**: Commit messages must adhere strictly to the Conventional Commits specification (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`).
- **Pull Request Size Limit**: Pull Requests must not exceed 400 lines of modified/added code (excluding lockfiles and generated assets) to ensure effective peer code reviews.
- **Clean Branch Strategy**: Feature branches must be rebased on the target branch prior to merging. Direct commits to `main` or `master` branches are strictly blocked.
- **Mandatory Peer Approval**: Every PR requires at least 1 approving review from an engineering peer and passing status on all CI checks before merging.

## Governance

- **Supremacy**: This Constitution supersedes all informal team agreements, individual coding preferences, and legacy guidelines.
- **Amendments**: Amendments or revisions to this Constitution require a formal proposal, justification documentation, engineering team review, and version update.
- **Compliance Enforcement**: Every pull request, code review, and automated pipeline must verify strict adherence to these principles. Non-compliant changes cannot be merged.

**Version**: 1.0.0 | **Ratified**: 2025-05-18 | **Last Amended**: 2025-05-18
