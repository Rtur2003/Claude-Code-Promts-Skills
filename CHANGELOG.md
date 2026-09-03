# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2.0.0] - 2026-09-02

Major modernization for the September 2026 Claude Code and AI ecosystem, plus a repo-wide framework refresh and a task-routing navigation layer.

### Added — Claude Code coverage

- **Agent Skills prompt** (`agents/agent-skills-prompt.md`) — `SKILL.md` frontmatter, progressive disclosure, `context: fork`, dynamic context injection, string substitutions, skill vs command vs subagent, evals with `skill-creator`.
- **MCP Integration prompt** (`agents/mcp-integration-prompt.md`) — `claude mcp add` transports, scopes and `.mcp.json`, OAuth, `headersHelper`, tool search, `@`-mentioned resources, MCP prompts as commands, output limits, prompt-injection and tool-poisoning containment.
- **Claude Code Plugins prompt** (`agents/claude-code-plugins-prompt.md`) — `plugin.json` manifest, bundled components (skills/agents/hooks/MCP/LSP/monitors/bin/settings), `--plugin-dir` testing, `marketplace.json`, official vs community marketplaces, `claude plugin validate`.
- **Hooks & Automation prompt** (`agents/hooks-automation-prompt.md`) — the full current hook event list (~25 events), five handler types, `settings.json` schema with `matcher` and `if:`, JSON decision output, guardrails-in-hooks principle.
- **Model Selection Guide** (`workflows/model-selection-guide.md`) — Opus 5 / Sonnet 5 / Haiku 4.5 / Fable 5.1 lineup, effort levels, `ultrathink` / `ultracode`, fast mode, advisor, retired-model list, API behavior changes.
- **Native Features Guide** (`workflows/claude-code-native-features-guide.md`) — plan mode, permission modes, sandboxing, checkpoints/`/rewind`, context management, background tasks, headless mode, session continuity, output styles, statusline, surfaces, the current command surface.
- **Agent SDK Guide** (`workflows/agent-sdk-guide.md`) — `@anthropic-ai/claude-agent-sdk` / `claude-agent-sdk`, `query()`, options, `.claude/` config loading, deployment; Agent SDK vs CLI vs Client SDK vs Managed Agents.
- **Workflows index** (`workflows/INDEX.md`) — the previously-missing catalog for the workflows folder, with a task router.

### Changed — rewrites

- **Multi-Agent Orchestration prompt** — rewritten around native subagents (`.claude/agents/*.md`), dynamic workflows (`ultracode`, `/deep-research`), `/batch`, forks, adversarial review, and cross-session messaging. The prior version described only human-driven parallel sessions.
- **Claude Code Thinking & Planning prompt** (was "Mode Transitions") — reframed around adaptive thinking, effort levels, `ultrathink`, `ultracode`, and plan mode. Removed the inaccurate "COMPACT/NORMAL/THINK/ULTRATHINK modes" model and the invented `/bug` `/test` `/review` `/commit` commands.
- **Claude Code Workflow prompt** — corrected `settings.json` schema (`settings.local.json`, `permissions.ask`, `model`, `env`, `statusLine`, `outputStyle`, `enabledPlugins`), the hooks section (correct shape, delegated to the hooks prompt), the MCP section (`.mcp.json`, delegated), and custom commands (skills-merged model, real frontmatter). Added `@imports`, `.claude/rules/` with `paths:`, and auto memory.
- **AI & LLM Integration prompt** — replaced "200K context" with the current 1M-context guidance; updated the provider matrix and every model ID (`gpt-4o*` -> current Claude models); added adaptive thinking, effort, prompt-cache depth, the `refusal` stop reason, and structured outputs.
- **Repo-wide framework refresh** — every project-type and specialist prompt updated to current stable versions (React 19, Next.js 16, Tailwind v4, Node 24 LTS, TypeScript 5.x, Kubernetes + Gateway API, OpenTofu, PostgreSQL 17, Swift 6, Kotlin Multiplatform, Compose, Unity 6, Godot 4, Rust Embassy, Solidity 0.8, Playwright, Vitest, OpenTelemetry, and more). Removed all "(2024/2025)" framing.

### Changed — navigation

- **Task-routing layer** — `llms.txt` rebuilt as a "task -> file" router; `prompts/english/INDEX.md` gained a task router at the top; `REPOSITORY-MAP.md` promoted to the canonical 30-second orientation; every new and rewritten file opens with a "Use this when" line and a "Skip to" anchor list.
- **README** — added the Modern Claude Code Stack section, the Common Combinations table (previously referenced by the changelog but missing), and token counts; portfolio table updated.
- **Agent catalog** (`agents/INDEX.md`) — split into "Claude Code operation" and "Development specialists", added token-count column and a task router.

### Note on versioning

The library carried no cut version since `1.0.0` (2024-01-01); all interim work sat under `[Unreleased]`. This release cuts `2.0.0` for the ecosystem modernization. Earlier `[Unreleased]` entries are retained below for history.

## [Unreleased]

### Added
- **Repository map** — Added `REPOSITORY-MAP.md` as a one-file navigation layer to reduce full-file scanning and speed prompt/library discovery
- **Craft-quality web standards** — Added non-generic UI quality checklist, interaction-state completeness checks, and Cloudflare Wrangler deployment guidance to web-focused prompts
- **Cloudflare CI/CD pattern** — Added Wrangler-native GitHub Actions deployment pattern and operational checklist to DevOps prompt
- **No-blind-defaults ML policy** — Added explicit baseline/challenger and hyperparameter-justification requirements for data science workflows
- **Prompt review checklist workflow** — Added `prompts/english/workflows/prompt-review-checklist.md` with measurable checks for `Role / Protocol / Phases / Remember` and no-vague-advice enforcement
- **Task-to-outcome scenario example pack** — Added `prompts/english/examples/task-outcome-scenarios-example.md` with explicit `Input Task`, `Expected Output Format`, and `Success Criteria` templates for bug fix, refactor, security review, and migration
- **LLM-friendly repository index** — Added root `llms.txt` with concise start points, core prompt, governance files, key specialist prompts, and archive index
- **Prompt archive index** — Added `prompts/english/agents/archive/INDEX.md` with keep/merge/archive classification and rationale
- **Portfolio Maintenance Guide** — Added `prompts/english/workflows/portfolio-maintenance-guide.md` with monthly + quarterly governance cadence
- **Compatibility stubs for archived prompts** — Added deprecation redirect files for archived prompt paths
- **Repository markdownlint baseline config** — Added `.markdownlint-cli2.jsonc` aligned with current repository Markdown conventions to reduce noisy lint failures on dense prompt docs

### Changed
- **Capability-aware agent guidance** — Updated core prompts and top-level docs with map-first discovery, skills/MCP/web-assisted execution, batched validation flow, and stricter low-noise comment discipline
- **Anti-dogma decision quality** — Strengthened foundation/system and technology-selection prompts with evidence-first choices, bounded risk-taking, and context-driven default handling
- **Single-source prompt selection** — Simplified `prompts/english/workflows/prompt-selector-guide.md` as the canonical decision tree and linked it from README, indexes, and quick-start
- **Quick-start onboarding** — Updated `QUICK-START.md` with a 30-second copy-paste setup and three scenario flows (general, debugging, security)
- **Contribution validation policy** — Converted PR validation guidance in `CONTRIBUTING.md` into a required checklist with link checks, markdown lint, and README/INDEX/llms consistency checks
- **Portfolio governance rigor** — Strengthened `prompts/english/workflows/portfolio-maintenance-guide.md` with forced keep/merge/archive decisions and a concise rationale log template
- **Primary documentation navigation** — Added `llms.txt` links in README and QUICK-START for faster agent/document discovery
- **Internal example link hygiene** — Replaced non-existent markdown links in prompt examples with explicit example-path code literals to avoid broken internal references
- **Contribution guidance for example paths** — Added a checklist rule in `CONTRIBUTING.md` to keep hypothetical paths as code literals instead of Markdown links
- **Contribution checklist** — Added `llms.txt` maintenance check when core navigation or prompt structure changes
- **Outcome-first repository structure** — Reworked README, QUICK-START, USAGE, and prompt indexes around “Agent System first + one specialist” selection
- **Agent catalog model** — Split active catalog from archived prompts and removed archived prompts from active listings
- **Contribution quality gates** — Added no-vague-advice rule and archive workflow to CONTRIBUTING and CLAUDE guidance
- **Core docs code fences** — Added explicit `text` language tags to unlabeled fenced blocks in README and QUICK-START
- **Lint compatibility tuning** — Adjusted markdownlint baseline for intentional prompt-document patterns (collapsible HTML sections and Makefile tabs in code blocks)
- **Prompt formatting cleanup** — Fixed heading style issues in `general-software-development-prompt.md` (`Arrange-Act-Assert` heading and `C#` heading rendering)

### Removed
- **Five prompts from active catalog** — Error Analysis, Project Workflow, Integration Guardian, Claude Code Token Optimization, and Prompt Chaining moved to archive

### Added
- **Database Design & Optimization prompt** — QUERY protocol for schema design, normalization decisions, composite indexing strategy, EXPLAIN ANALYZE workflow, N+1 detection, connection pooling, zero-downtime migration patterns, and performance monitoring queries
- **UI/UX & Design Systems prompt** — DESIGN protocol for design token hierarchy (global → alias → component), variant-driven components (CVA), compound component pattern, accessibility by default (WCAG 2.2), responsive patterns, Storybook documentation, theme system with dark mode, and visual regression testing
- **Testing Strategies example** — Legacy Express API walkthrough: 0% → 84% coverage with Vitest, test factories, database isolation, integration tests with supertest, concurrent race condition testing, CI pipeline with coverage gates
- **Migration & Upgrade example** — Express.js → NestJS zero-downtime migration using Strangler Fig pattern, reverse proxy routing, comparison testing, auth guard migration (fixing silent token passthrough bug), DTOs with class-validator
- **Error Handling & Resilience prompt** — RESILIENCE protocol for circuit breakers, retry with exponential backoff, bulkhead isolation, timeout patterns, graceful degradation strategies, Result pattern, structured error logging, and error taxonomy
- **Developer Experience & Tooling prompt** — DX protocol for ESLint/Prettier/Ruff configuration, Git hooks (Husky + lint-staged), VS Code shared settings, Makefile automation, onboarding checklists, CI/CD DX integration, and DX metrics scoring
- **Performance Optimization example** — E-commerce API optimization walkthrough demonstrating DB profiling with EXPLAIN ANALYZE, composite indexing, N+1 elimination with LATERAL JOIN, Redis caching with stale-while-revalidate, and cursor-based pagination (3.5s → 3ms)
- **Best Practices & Customization Guide** — Prompt composition patterns (single, base+specialist, layered, monorepo), team customization templates, token budget optimization, effectiveness metrics, language-specific customizations (TypeScript, Python, Go, Rust), troubleshooting guide for prompt issues
- **Multi-Agent Orchestration prompt** — ORCHESTRATE protocol for coordinating multiple Claude Code sessions, agent specialization, shared state management, conflict resolution, and parallel execution patterns (Hub & Spoke, Pipeline, Swarm, Review Loop topologies)
- **Monorepo & Complex Projects prompt** — SCALE protocol for Turborepo/Nx/pnpm workspaces, hierarchical CLAUDE.md strategies, cross-package dependency management, microservices architecture, and CI/CD optimization for multi-package builds
- **Claude Code Setup Guide** — Complete guide for `.claude/` directory structure, `settings.json` specification, custom slash commands (`.claude/commands/`), CLAUDE.md hierarchy design, prompt placement strategies (single prompt, custom commands, layered, team shared), multi-prompt composition patterns, conflict matrix, real-world setup examples (solo dev, team of 5, enterprise monorepo)

### Enhanced
- **README.md** — Added new prompts to catalog, expanded Common Combinations table with database, design system, error handling, DX, and resilience entries, updated repository structure counts
- **QUICK-START.md** — Added database optimization, UI/UX design systems, error handling, developer experience prompts to selector
- **USAGE.md** — Added database optimization, design system, error handling and developer experience scenarios
- **Agent Index** — Updated catalog to 34 prompts with database and UI/UX entries
- **Prompt Index** — Added all new prompts and examples to catalog
- **Examples README** — Added testing strategies and migration examples
- **CONTRIBUTING.md** — Updated file counts to reflect current repository state
- **CLAUDE.md** — Updated repository structure counts

### Changed
- Agent prompt count: 30 → 34
- Workflow guide count: 4 → 5
- Example count: 7 → 10
- Total prompt files: 41 → 48

---

### Added
- **API Design & GraphQL prompt** — SCHEMA protocol for schema-first design, DataLoader, caching, contract testing
- **Cloud & Infrastructure prompt** — CLOUD protocol for IaC, multi-region, K8s, cost optimization
- **Data Engineering prompt** — PIPELINE protocol for dbt, streaming, data quality, Apache Airflow
- **Compliance & Governance prompt** — GOVERN protocol for GDPR, HIPAA, SOC 2, PCI DSS, STRIDE threat modeling
- **Debugging & Troubleshooting prompt** — DEBUG protocol for production debugging, profiling, incident response
- **Blockchain & Web3 project-type prompt** — Solidity, Rust, Foundry, smart contract security, gas optimization
- **Desktop Application project-type prompt** — Tauri, Electron, Qt, native integration, auto-update
- **Cloud Infrastructure example** — Terraform + K8s on AWS real-world deployment walkthrough
- **AI Agent example** — Building an AI-powered code review agent with Claude API
- **Troubleshooting Guide** — Systematic issue diagnosis decision flowchart with common patterns
- Accessibility Audit prompt — ACCESS protocol for WCAG 2.2 compliance testing
- Migration & Upgrade prompt — MIGRATE protocol for framework, database, and dependency migrations
- Monitoring & Observability prompt — OBSERVE protocol for logs, metrics, traces, and alerting
- AI & LLM Integration prompt — AUGMENT protocol for RAG, vector DBs, AI agents, and safety
- Game Development prompt — Unity, Unreal, Godot, ECS, multiplayer patterns
- Embedded Systems & IoT prompt — C, C++, Rust, FreeRTOS, MQTT, TinyML, safety-critical
- Full-Stack App example — Next.js + tRPC + Prisma end-to-end walkthrough
- Security Audit example — Node.js/Express vulnerability assessment walkthrough
- Refactoring example — Legacy code improvement with before/after metrics
- Prompt Selector Guide — Interactive decision tree for choosing the right prompt combination
- CLAUDE.md — AI agent configuration for working on this repository
- LICENSE file (MIT)
- CHANGELOG.md for version tracking

### Enhanced
- **Security Audit prompt** — Added cloud security assessment, supply chain security, zero trust architecture
- **Architecture Patterns prompt** — Added serverless architecture, event sourcing deep dive, saga pattern, data consistency patterns
- **Testing Strategies prompt** — Added contract testing (Pact), property-based testing (Hypothesis, fast-check), chaos testing, anti-patterns table
- **Performance Optimization prompt** — Added GraphQL N+1 prevention, memory profiling (Node.js + Python), CDN/edge optimization, Cloudflare Workers
- **Full-Stack Development prompt** — Added WebSocket/SSE real-time patterns, Socket.io integration, BullMQ background jobs
- **API Development prompt** — Added idempotency keys, cursor-based pagination, webhook delivery with retries
- **Data Science & ML prompt** — Added MLOps section with model monitoring (drift detection), SHAP/LIME explainability, MLflow experiment tracking, model registry
- **Web Development prompt** — Added SEO/meta tags (Open Graph, JSON-LD), font optimization (preload, swap), image optimization (WebP, lazy loading), accessibility quick wins

### Changed
- Updated README.md with all new prompts, expanded combinations table (36 combinations), updated architecture section
- Updated QUICK-START.md with all new prompts and resources
- Updated USAGE.md with new scenarios for all new prompts
- Updated CONTRIBUTING.md with new file counts and contribution types
- Updated all INDEX.md files with new prompt entries and expanded feature matrix
- Made repository fully English-only and global
- Expanded feature matrix to include Blockchain and Desktop columns
- Agent prompt count: 23 → 28
- Project type prompt count: 9 → 11
- Example count: 5 → 7
- Workflow guide count: 2 → 3
- Total prompt files: 32 → 39

### Removed
- Turkish translations directory (repository is now English-only for global accessibility)
- Language support section from README.md
- Language-specific references from all documentation

## [1.0.0] - 2024-01-01

### Added
- Initial release with 19 English agent prompts
- Foundation prompt for interactive sessions
- 7 project-type prompts (Web, API, Data Science, Mobile, DevOps, Database, General)
- APEI methodology (Analyze → Plan → Execute → Iterate)
- Examples: REST API and Debugging walkthroughs
- Workflow guide: Iterative Development Guide
- Documentation: README, QUICK-START, USAGE, CONTRIBUTING
