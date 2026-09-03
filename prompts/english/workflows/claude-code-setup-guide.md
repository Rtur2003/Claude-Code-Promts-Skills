# Claude Code Setup & Integration Guide

> **Complete `.claude/` Configuration** | **Prompt Placement Strategies** | **Complex Project Structures**

## Overview

This guide covers everything you need to integrate prompts from this repository into your Claude Code environment. From single-project setups to enterprise monorepos with multiple agents, you'll learn exactly where each file goes and why.

---

## Understanding Claude Code's Configuration System

Claude Code reads two separate layered systems: **instructions** (CLAUDE.md, rules) and **settings** (`settings.json`).

```
Settings (higher precedence wins):
┌──────────────────────────────────────────────────────┐
│ 1. Managed policy settings (org-controlled)          │
│ 2. .claude/settings.local.json (personal, gitignored)│
│ 3. .claude/settings.json (team, committed)           │
│ 4. ~/.claude/settings.json (user-global)             │
└──────────────────────────────────────────────────────┘

Instructions (CLAUDE.md + .claude/rules/) are ADDITIVE, not overriding —
all levels are concatenated into context, root-of-tree first, working
directory last. Nested CLAUDE.md load on demand when Claude reads files
in that subdirectory.
```

---

## Core File Structure

### Minimal Setup (Single Project)

```
your-project/
├── CLAUDE.md                  # Project memory & conventions
├── .claude/
│   └── settings.json          # Hooks, permissions, MCP servers
└── src/
    └── ...
```

### Standard Setup (Growing Project)

```
your-project/
├── CLAUDE.md                  # Global project context
├── .claude/
│   ├── settings.json          # Hooks, permissions, MCP
│   └── commands/              # Custom slash commands
│       ├── review.md          # /review
│       ├── deploy.md          # /deploy
│       └── debug.md           # /debug
├── src/
│   └── CLAUDE.md              # Source-specific conventions
├── tests/
│   └── CLAUDE.md              # Testing conventions
└── docs/
    └── CLAUDE.md              # Documentation conventions
```

### Enterprise Setup (Monorepo / Multi-Service)

```
monorepo/
├── CLAUDE.md                  # Global: shared conventions, architecture overview
├── .claude/
│   ├── settings.json          # Global hooks and permissions
│   └── commands/
│       ├── review.md          # Cross-package review command
│       ├── test-all.md        # Run all tests across packages
│       └── deploy.md          # Deployment orchestration
├── packages/
│   ├── web/
│   │   ├── CLAUDE.md          # Frontend conventions (React, Next.js)
│   │   └── src/
│   │       ├── components/
│   │       │   └── CLAUDE.md  # Component patterns, naming
│   │       └── hooks/
│   │           └── CLAUDE.md  # Custom hook conventions
│   ├── api/
│   │   ├── CLAUDE.md          # Backend conventions (Node/Go/Python)
│   │   └── src/
│   │       ├── routes/
│   │       │   └── CLAUDE.md  # API route patterns
│   │       └── services/
│   │           └── CLAUDE.md  # Service layer patterns
│   ├── shared/
│   │   └── CLAUDE.md          # Shared library conventions
│   └── mobile/
│       └── CLAUDE.md          # Mobile-specific conventions
├── infrastructure/
│   └── CLAUDE.md              # IaC conventions (Terraform, K8s)
└── scripts/
    └── CLAUDE.md              # Build/deploy script conventions
```

---

## CLAUDE.md: Project Memory File

### What Goes in CLAUDE.md

CLAUDE.md is the single most important file for Claude Code. It persists across sessions, loads automatically, and provides context without consuming conversation tokens.

### Root CLAUDE.md Template

Use this as your project root `CLAUDE.md`. Copy and customize:

```markdown
# CLAUDE.md

## Project Overview
- Name: [Your Project Name]
- Type: [web app / API / CLI / library / monorepo]
- Stack: [primary language, framework, key dependencies]
- Repository structure: [brief description]

## Build & Development
- Install: `[install command]`
- Dev: `[dev server command]`
- Build: `[build command]`
- Test: `[test command]`
- Test single: `[single test command pattern]`
- Lint: `[lint command]`
- Format: `[format command]`
- Type check: `[type check command]`

## Code Conventions
- Style guide: [ESLint config / Prettier / team rules]
- Naming: [camelCase for vars, PascalCase for components, etc.]
- File naming: [kebab-case.ts / PascalCase.tsx / snake_case.py]
- Imports: [absolute paths / barrel files / path aliases]
- Tests: [co-located / separate directory / naming pattern]
- Commits: [conventional commits / custom format]

## Architecture
- Pattern: [MVC / Clean Architecture / Hexagonal / DDD]
- State management: [Redux / Zustand / Context / Pinia]
- API layer: [REST / GraphQL / tRPC / gRPC]
- Database: [PostgreSQL / MongoDB / SQLite]
- Auth: [JWT / OAuth / Session]

## Important Paths
- Source: src/
- Tests: tests/ or src/**/*.test.ts
- Config: config/
- API routes: src/routes/ or src/app/api/
- Components: src/components/
- Database: prisma/ or src/db/

## Common Tasks
- Add a new feature: [steps specific to your project]
- Add a new API endpoint: [steps]
- Add a new component: [steps]
- Run database migration: [command]
- Deploy: [deployment steps]

## Things to Avoid
- Don't modify [critical files] without team discussion
- Don't use [deprecated patterns]
- Don't commit [file types to exclude]
- Don't install packages without checking for alternatives already in use
- Don't bypass TypeScript with `any` type

## Current Focus
- [Current sprint/milestone goals]
- [Active feature branches and their purpose]
```

### Subdirectory CLAUDE.md Examples

#### `src/CLAUDE.md` (Source Code)

```markdown
# Source Code Conventions

## File Organization
- Group by feature, not by type
- Each feature directory: index.ts, types.ts, *.test.ts
- Shared utilities in src/lib/

## Patterns
- Use dependency injection for services
- Prefer composition over inheritance
- All async operations must handle errors explicitly
- Use Result<T, E> pattern instead of throwing

## Naming
- Interfaces: prefix with I (IUserRepository)
- Types: suffix with Type only if ambiguous
- Constants: UPPER_SNAKE_CASE
- Enums: PascalCase members
```

#### `tests/CLAUDE.md` (Testing)

```markdown
# Testing Conventions

## Structure
- Mirror source directory structure
- One test file per source module
- Use descriptive test names: "should [expected behavior] when [condition]"

## Patterns
- Arrange-Act-Assert (AAA) pattern
- Use factories for test data (tests/factories/)
- Mock external services, never the module under test
- Integration tests in tests/integration/
- E2E tests in tests/e2e/

## Commands
- Run all: `npm test`
- Run single: `npm test -- --testPathPattern="auth"`
- Run with coverage: `npm test -- --coverage`
- Watch mode: `npm test -- --watch`
```

#### `packages/api/CLAUDE.md` (Monorepo Package)

```markdown
# API Package

## Overview
Express/Fastify API server for the main application.

## Stack
- Runtime: Node.js 24 LTS
- Framework: Fastify v5
- ORM: Drizzle
- Validation: Zod
- Auth: JWT with refresh tokens

## Commands (run from this directory)
- Dev: `pnpm dev`
- Test: `pnpm test`
- Build: `pnpm build`
- Migrate: `pnpm db:migrate`
- Seed: `pnpm db:seed`

## Conventions
- Route files export a Fastify plugin
- Business logic in services/, not routes/
- Use Zod schemas for request/response validation
- Shared types imported from @monorepo/shared
- All database queries through repository pattern
```

---

## .claude/settings.json: Project Configuration

### Complete Settings Schema

```json
{
  "model": "opus",
  "effortLevel": "high",
  "outputStyle": "Concise",
  "permissions": {
    "allow": [
      "Bash(npm run test:*)",
      "Bash(npm run lint)",
      "Bash(npm run build)",
      "Bash(npx tsc --noEmit)",
      "Bash(git commit *)",
      "Read(src/**)"
    ],
    "deny": [
      "Read(**/.env)",
      "Edit(prisma/migrations/**)"
    ],
    "ask": [
      "Bash(git push *)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-secrets.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write",
            "args": ["${tool_input.file_path}"],
            "async": true
          }
        ]
      }
    ]
  },
  "env": { "CLAUDE_CODE_SUBAGENT_MODEL": "haiku" },
  "statusLine": { "type": "command", "command": ".claude/statusline.sh" },
  "enabledPlugins": ["acme-tools@acme"],
  "autoMemoryEnabled": true
}
```

Hook config: the `hooks` value is an array of `{ matcher, hooks: [{ type, command, ... }] }` entries. The command receives the hook event as JSON on stdin — extract fields with `jq` or the `${tool_input.field}` substitution, not the old `$CLAUDE_FILE_PATH` env var. Full hook reference: [../agents/hooks-automation-prompt.md](../agents/hooks-automation-prompt.md).

MCP servers belong in `.mcp.json` at the project root (committed, team-shared), not in `settings.json`. Full MCP setup: [../agents/mcp-integration-prompt.md](../agents/mcp-integration-prompt.md).

`"auto"` / `"bypassPermissions"` as `defaultMode` are ignored in project/local settings — they only work in `~/.claude/settings.json` or managed settings.

### Settings hierarchy

```
managed policy settings          highest precedence, org-controlled
your-project/.claude/settings.local.json   personal, not committed
your-project/.claude/settings.json         team, committed to git
~/.claude/settings.json                     user-global
```

More specific wins. **Commit project `settings.json`** so the team shares configuration; keep machine-specific overrides in `settings.local.json` (gitignored).

---

## .claude/skills/ and .claude/commands/: Custom Commands

Custom commands have been merged into skills. A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy`. Existing `.claude/commands/` files keep working; skills are recommended — they support a directory of supporting files, model-invocation, and subagent execution. Full authoring: [../agents/agent-skills-prompt.md](../agents/agent-skills-prompt.md).

```
.claude/skills/
├── review/SKILL.md      → /review
├── deploy/SKILL.md       → /deploy
└── new-feature/SKILL.md  → /new-feature
```

### Skill file format

`SKILL.md` = YAML frontmatter + Markdown instructions. Use `$ARGUMENTS` / `$1` / `$2` for parameters, `` !`cmd` `` for injected context, `@file` for file references.

#### Example: `.claude/skills/review/SKILL.md`

```markdown
---
description: Review the current changes for correctness, security, performance, tests, and style. Use when the user asks for a review.
allowed-tools: Bash(git diff *)
---

## Current changes

!`git diff HEAD`

## Instructions

Review the diff above against:
1. Correctness — does it do what it should?
2. Security — injection, auth, data exposure
3. Performance — N+1 queries, leaks, needless work
4. Tests — new paths covered, edge cases
5. Style — matches CLAUDE.md conventions

Focus on: $ARGUMENTS. Give feedback with file:line references.
```

Usage: `/review the authentication middleware changes`

#### Example: `.claude/commands/new-feature.md`

```markdown
Implement a new feature following our project's APEI cycle:

Feature: $ARGUMENTS

## Step 1: Analyze
- Read CLAUDE.md for project conventions
- Identify affected files and dependencies
- Check existing patterns for similar features

## Step 2: Plan
- Create a numbered implementation checklist
- Identify test cases needed
- List files to create/modify

## Step 3: Execute
- Implement step by step
- Add tests after each component
- Follow conventions from CLAUDE.md

## Step 4: Verify
- Run full test suite
- Run linter and type checker
- Verify the feature works end-to-end
```

Usage: `/new-feature user profile image upload with S3 storage`

#### Example: `.claude/commands/debug.md`

```markdown
Debug the following issue systematically:

Issue: $ARGUMENTS

## Protocol
1. **Reproduce**: Find the exact steps to trigger the bug
2. **Isolate**: Narrow down to the specific file and function
3. **Root cause**: Analyze deeply — add `ultrathink` to the prompt if the cause is not obvious
4. **Fix**: Apply the minimal fix
5. **Verify**: Write a regression test
6. **Document**: Note the fix in the commit message

Use the project's test suite to verify the fix doesn't break anything.
```

Usage: `/debug login fails when email contains a plus sign`

---

## Placing Prompts from This Repository

### Strategy 1: Single Prompt in CLAUDE.md (Simple Projects)

For small projects, embed the core prompt directly in your `CLAUDE.md`:

```markdown
# CLAUDE.md

## System Prompt
[Paste the content of prompts/english/agents/claude-agent-system-prompt.md here]

## Project Overview
[Your project-specific context]

## Build & Development
[Your project-specific commands]
```

### Strategy 2: Custom Commands (Task-Specific Prompts)

For projects needing multiple prompt types, use custom commands:

```
.claude/commands/
├── review.md          ← Content from code-review-prompt.md
├── security.md        ← Content from security-audit-prompt.md
├── refactor.md        ← Content from refactoring-prompt.md
├── test.md            ← Content from testing-strategies-prompt.md
├── debug.md           ← Content from debugging-troubleshooting-prompt.md
└── optimize.md        ← Content from performance-optimization-prompt.md
```

This way, you invoke each prompt as a slash command when needed, keeping token usage efficient.

### Strategy 3: Layered CLAUDE.md (Complex Projects)

For complex projects, distribute prompt content across CLAUDE.md files:

```
project/
├── CLAUDE.md                     ← Agent System Prompt + project overview
├── src/
│   ├── CLAUDE.md                 ← Code conventions from Foundation Prompt
│   ├── components/
│   │   └── CLAUDE.md             ← Web Development prompt patterns
│   └── api/
│       └── CLAUDE.md             ← API Development prompt patterns
├── tests/
│   └── CLAUDE.md                 ← Testing Strategies prompt patterns
├── infrastructure/
│   └── CLAUDE.md                 ← Cloud & Infrastructure prompt patterns
└── .claude/
    └── commands/                 ← Task-specific prompts as commands
```

### Strategy 4: Team Shared Configuration (Team Projects)

For teams, create a shared prompt repository and reference it:

```
your-org/
├── claude-prompts/               ← Fork of this repo, customized
│   └── team/
│       ├── code-review.md        ← Team-specific review standards
│       ├── security.md           ← Company security requirements
│       └── onboarding.md         ← New developer setup
└── your-project/
    ├── CLAUDE.md                 ← References team standards
    └── .claude/
        └── commands/             ← Symlink or copy from claude-prompts/
```

---

## Complex Scenario: Multi-Prompt Composition

### When You Need Multiple Prompts at Once

Some tasks require combining prompts. Here's how to compose them effectively:

#### Scenario: Full-Stack Feature (Frontend + Backend + Database)

**CLAUDE.md** approach — add a task-specific section:

```markdown
# CLAUDE.md

## Current Task Context
This task involves full-stack changes. Follow these combined guidelines:

### Frontend (from Web Development prompt)
- Use React Server Components by default
- Client components only for interactivity
- Validate with Zod on both client and server

### Backend (from API Development prompt)
- RESTful endpoints with proper status codes
- Idempotency keys for mutations
- Rate limiting on public endpoints

### Database (from Database prompt)
- Migrations are forward-only
- Index all foreign keys
- Use transactions for multi-table operations
```

#### Scenario: Security-Critical Release

Create a compound command:

```markdown
<!-- .claude/commands/secure-release.md -->
Perform a security-focused release review combining:

## Security Audit (from security-audit-prompt)
- Check OWASP Top 10
- Review authentication flows
- Scan for hardcoded secrets
- Check dependency vulnerabilities

## Compliance Check (from compliance-governance-prompt)
- Verify data handling meets GDPR requirements
- Check PII exposure in logs
- Validate consent flows

## Performance Baseline (from performance-optimization-prompt)
- Measure response times for critical paths
- Check for memory leaks under load
- Verify CDN caching headers

Target: $ARGUMENTS
```

#### Scenario: Legacy Migration

```markdown
<!-- .claude/commands/migrate.md -->
Orchestrate a migration using combined strategies:

## Step 1: Audit (Architecture Patterns prompt)
- Map current architecture
- Identify coupling points
- Document data flows

## Step 2: Plan (Migration & Upgrade prompt)
- Order changes by dependency
- Plan rollback at each step
- Set up feature flags

## Step 3: Execute (Refactoring prompt)
- Apply strangler fig pattern
- Refactor in small, testable steps
- Maintain backward compatibility

## Step 4: Validate (Testing Strategies prompt)
- Run contract tests
- Verify integration points
- Load test critical paths

Migration target: $ARGUMENTS
```

---

## Prompt Composition Conflict Matrix

When combining multiple prompts, be aware of potential conflicts:

| Combination | Potential Conflict | Resolution |
|-------------|-------------------|------------|
| Security + Performance | Security may add overhead | Prioritize security; optimize within constraints |
| Refactoring + Testing | Refactoring may break tests | Update tests alongside refactoring; never skip |
| Architecture + Migration | New arch patterns vs. legacy constraints | Incremental migration; don't rewrite everything |
| Full-Stack + broad context | Full-stack needs detailed context | Use directory-level CLAUDE.md and `.claude/rules/` with `paths:` to scope context |
| Deep review + token budget | Review needs depth; long sessions bloat context | Run `/code-review` in a fresh subagent; `/clear` between review and fix passes |

---

## User-Global Configuration

### ~/.claude/CLAUDE.md (Personal Defaults)

Set your personal coding preferences that apply to all projects:

```markdown
# Personal Claude Code Preferences

## My Defaults
- Prefer TypeScript over JavaScript
- Use functional programming patterns when possible
- Always add JSDoc for public APIs
- I prefer explicit error handling over try/catch

## Communication
- Be concise, skip obvious explanations
- Show code diffs, not full file rewrites
- Ask before making large refactors

## My Workflow
- I use Git Flow branching
- I prefer squash merges
- I want conventional commit messages
```

### ~/.claude/settings.json (Personal Tool Settings)

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Edit",
      "Write"
    ]
  },
  "enableAllProjectMcpServers": false
}
```

Put MCP servers in `.mcp.json` (project root), not `settings.json`. For a hosted GitHub MCP server with OAuth instead of a PAT, see [../agents/mcp-integration-prompt.md](../agents/mcp-integration-prompt.md).

---

## Real-World Setup Examples

### Example 1: Solo Developer — Next.js SaaS

```
my-saas/
├── CLAUDE.md                          # Stack: Next.js 16, Prisma 7, Stripe
├── .claude/
│   ├── settings.json                  # Auto-format, auto-lint hooks
│   └── commands/
│       ├── new-page.md                # Template for new pages
│       ├── new-api.md                 # Template for API routes
│       └── deploy.md                  # Deployment checklist
├── src/
│   ├── CLAUDE.md                      # Component patterns, data fetching
│   └── ...
└── prisma/
    └── CLAUDE.md                      # Schema conventions, migration steps
```

### Example 2: Team of 5 — Microservices

```
platform/
├── CLAUDE.md                          # Architecture overview, shared conventions
├── .claude/
│   ├── settings.json                  # Shared hooks for all services
│   └── commands/
│       ├── review.md                  # Team code review standards
│       ├── new-service.md             # Service scaffolding template
│       └── incident.md               # Incident response checklist
├── services/
│   ├── auth-service/
│   │   ├── CLAUDE.md                  # Auth patterns, token management
│   │   └── ...
│   ├── payment-service/
│   │   ├── CLAUDE.md                  # Payment flow, idempotency rules
│   │   └── ...
│   └── notification-service/
│       ├── CLAUDE.md                  # Queue patterns, retry logic
│       └── ...
├── shared/
│   └── CLAUDE.md                      # Shared types, utilities, contracts
└── infrastructure/
    └── CLAUDE.md                      # Terraform modules, K8s manifests
```

### Example 3: Enterprise — Multi-Team Monorepo

```
enterprise-mono/
├── CLAUDE.md                          # Org-wide: architecture principles, ADRs
├── .claude/
│   ├── settings.json                  # Enterprise hooks (security, compliance)
│   └── commands/
│       ├── security-check.md          # Company security audit protocol
│       ├── compliance-review.md       # GDPR/SOC2 compliance check
│       ├── onboard-dev.md             # New developer setup
│       └── adr.md                     # Create Architecture Decision Record
├── apps/
│   ├── customer-portal/
│   │   ├── CLAUDE.md                  # Customer-facing app conventions
│   │   └── .claude/
│   │       └── commands/
│   │           └── a11y-check.md      # Accessibility audit for this app
│   ├── admin-dashboard/
│   │   └── CLAUDE.md
│   └── mobile-app/
│       └── CLAUDE.md
├── libs/
│   ├── ui-components/
│   │   └── CLAUDE.md                  # Design system patterns
│   ├── api-client/
│   │   └── CLAUDE.md
│   └── auth/
│       └── CLAUDE.md
├── services/
│   └── [same as microservices above]
└── tools/
    └── CLAUDE.md                      # Internal tooling conventions
```

---

## Multi-Session Workflow Patterns

### Pattern 1: Deep Work Sessions

```
Session 1: Architecture (plan mode, /effort xhigh)
├── Read CLAUDE.md for context
├── Design solution architecture
├── Document decisions in CLAUDE.md
└── Create implementation plan

/clear → Reset context

Session 2: Implementation (/effort high)
├── CLAUDE.md auto-loads previous decisions
├── Execute plan step by step
├── Run tests after each step
└── Update CLAUDE.md with progress

/clear → Reset context

Session 3: Review & Polish
├── /code-review → adversarial review in a fresh subagent
├── Apply the fixes
├── /compact if context is bloated
└── Update CLAUDE.md with learnings
```

### Pattern 2: Parallel Workstreams

When working on multiple features simultaneously:

```
CLAUDE.md tracks:
## Active Workstreams
### Feature A (branch: feat/user-profiles)
- Status: Step 3/5 — implementing profile API
- Last session: designed database schema
- Next: implement CRUD endpoints

### Feature B (branch: feat/notifications)
- Status: Step 1/4 — analyzing requirements
- Next: design notification data model

### Bug Fix (branch: fix/auth-race)
- Status: Identified root cause
- Next: implement fix and regression test
```

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|---------|
| CLAUDE.md not being read | File not in project root | Move to repo root directory |
| Hooks not firing | Invalid JSON in settings.json | Validate JSON syntax |
| Custom command not showing | Wrong directory or extension | Must be `.claude/commands/*.md` |
| Context lost between sessions | CLAUDE.md not updated | Use `/memory` to save state |
| Too many tokens consumed | CLAUDE.md too large | Split into directory-level files |
| Team settings conflicting | Multiple settings sources | Use project `.claude/settings.json` |
| MCP server not connecting | Wrong command or env vars | Test server command manually |

---

## Checklist: Setting Up Your Project

- [ ] Create root `CLAUDE.md` with project overview and conventions
- [ ] Create `.claude/settings.json` with hooks and permissions
- [ ] Add `.claude/commands/` for task-specific prompts you use often
- [ ] Add subdirectory `CLAUDE.md` files for complex projects
- [ ] Commit `.claude/` directory to git for team sharing
- [ ] Add sensitive values (tokens, secrets) to `.gitignore` or use env vars
- [ ] Test hooks by making a small edit and verifying auto-format runs
- [ ] Test custom commands with `/command-name`
- [ ] Review token usage with `/cost` after first session

---

## Remember

> **Configuration is an investment. A well-configured Claude Code environment multiplies every session's productivity.**

Key principles:
1. **CLAUDE.md is your project's brain** — keep it accurate and up to date
2. **Hooks automate quality** — auto-format, auto-lint, block risky edits
3. **Custom commands are your shortcuts** — turn complex workflows into one-liners
4. **Layer your configuration** — global defaults + project specifics + directory context
5. **Commit your config** — team alignment through shared `.claude/` settings
6. **Update after every session** — CLAUDE.md should grow smarter with your project
