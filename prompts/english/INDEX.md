# Prompt Index

Global router for the library. Find your task below, open that one file. Don't read the whole repo.

Selection logic source: [workflows/prompt-selector-guide.md](workflows/prompt-selector-guide.md)

## Route by task

### Running Claude Code

| Task | Open |
|---|---|
| Any autonomous coding task | [agents/claude-agent-system-prompt.md](agents/claude-agent-system-prompt.md) |
| Pick a model or effort level | [workflows/model-selection-guide.md](workflows/model-selection-guide.md) |
| What a current Claude Code build can do | [workflows/claude-code-native-features-guide.md](workflows/claude-code-native-features-guide.md) |
| Set thinking depth / effort / plan mode | [agents/claude-code-modes-prompt.md](agents/claude-code-modes-prompt.md) |
| Set up `.claude/` config, CLAUDE.md, permissions | [agents/claude-code-workflow-prompt.md](agents/claude-code-workflow-prompt.md) |
| Write or debug a Claude skill | [agents/agent-skills-prompt.md](agents/agent-skills-prompt.md) |
| Connect a DB / browser / API via MCP | [agents/mcp-integration-prompt.md](agents/mcp-integration-prompt.md) |
| Bundle skills/agents/hooks into a plugin | [agents/claude-code-plugins-prompt.md](agents/claude-code-plugins-prompt.md) |
| Parallel agents, workflows, audits, writer/reviewer | [agents/multi-agent-orchestration-prompt.md](agents/multi-agent-orchestration-prompt.md) |
| Automate on a lifecycle event | [agents/hooks-automation-prompt.md](agents/hooks-automation-prompt.md) |
| Build an agent programmatically | [workflows/agent-sdk-guide.md](workflows/agent-sdk-guide.md) |

### Building software

| Task | Open |
|---|---|
| Web frontend (React, Vue, Angular, Svelte) | [project-types/web-development-prompt.md](project-types/web-development-prompt.md) |
| REST / GraphQL / gRPC API | [project-types/api-development-prompt.md](project-types/api-development-prompt.md) + [agents/api-design-graphql-prompt.md](agents/api-design-graphql-prompt.md) |
| End-to-end full-stack app | [agents/fullstack-development-prompt.md](agents/fullstack-development-prompt.md) |
| Mobile (iOS, Android, RN, Flutter, KMP) | [project-types/mobile-development-prompt.md](project-types/mobile-development-prompt.md) |
| Desktop (Tauri, Electron, MAUI) | [project-types/desktop-development-prompt.md](project-types/desktop-development-prompt.md) |
| Data pipelines / streaming | [project-types/data-science-ml-prompt.md](project-types/data-science-ml-prompt.md) + [agents/data-engineering-prompt.md](agents/data-engineering-prompt.md) |
| ML / AI feature | [project-types/data-science-ml-prompt.md](project-types/data-science-ml-prompt.md) + [agents/ai-llm-integration-prompt.md](agents/ai-llm-integration-prompt.md) |
| DevOps / CI-CD / IaC / Kubernetes | [project-types/devops-cicd-prompt.md](project-types/devops-cicd-prompt.md) + [agents/cloud-infrastructure-prompt.md](agents/cloud-infrastructure-prompt.md) |
| Database schema / SQL / indexing | [project-types/database-sql-prompt.md](project-types/database-sql-prompt.md) + [agents/database-optimization-prompt.md](agents/database-optimization-prompt.md) |
| Game (Unity, Unreal, Godot, Bevy) | [project-types/game-development-prompt.md](project-types/game-development-prompt.md) |
| Embedded / IoT / firmware | [project-types/embedded-iot-prompt.md](project-types/embedded-iot-prompt.md) |
| Smart contracts / web3 | [project-types/blockchain-web3-prompt.md](project-types/blockchain-web3-prompt.md) |
| Language-agnostic / other | [project-types/general-software-development-prompt.md](project-types/general-software-development-prompt.md) |

### Improving existing code

| Task | Open |
|---|---|
| Review a PR / change set | [agents/code-review-prompt.md](agents/code-review-prompt.md) |
| Find security vulnerabilities | [agents/security-audit-prompt.md](agents/security-audit-prompt.md) |
| Root-cause a production incident | [agents/debugging-troubleshooting-prompt.md](agents/debugging-troubleshooting-prompt.md) |
| Reduce complexity / technical debt | [agents/refactoring-prompt.md](agents/refactoring-prompt.md) |
| Build or fix a test strategy | [agents/testing-strategies-prompt.md](agents/testing-strategies-prompt.md) |
| Fix latency / throughput / cost | [agents/performance-optimization-prompt.md](agents/performance-optimization-prompt.md) |
| Migrate a framework / runtime / DB | [agents/migration-upgrade-prompt.md](agents/migration-upgrade-prompt.md) |
| Add logs / metrics / traces / alerts | [agents/monitoring-observability-prompt.md](agents/monitoring-observability-prompt.md) |
| Harden fault tolerance | [agents/error-handling-resilience-prompt.md](agents/error-handling-resilience-prompt.md) |
| WCAG / accessibility audit | [agents/accessibility-audit-prompt.md](agents/accessibility-audit-prompt.md) |

### Deciding

| Task | Open |
|---|---|
| Design system architecture | [agents/architecture-patterns-prompt.md](agents/architecture-patterns-prompt.md) |
| Choose tools / libraries | [agents/technology-stack-prompt.md](agents/technology-stack-prompt.md) |
| Regulated / compliance scope (GDPR, HIPAA, SOC 2) | [agents/compliance-governance-prompt.md](agents/compliance-governance-prompt.md) |
| Branching / commits / release process | [agents/git-version-control-prompt.md](agents/git-version-control-prompt.md) |
| Set up DX / linting / onboarding | [agents/developer-experience-tooling-prompt.md](agents/developer-experience-tooling-prompt.md) |
| Structure a monorepo | [agents/monorepo-complex-projects-prompt.md](agents/monorepo-complex-projects-prompt.md) |
| Write documentation | [agents/documentation-prompt.md](agents/documentation-prompt.md) |
| Design a UI component system | [agents/ui-design-systems-prompt.md](agents/ui-design-systems-prompt.md) |

## Catalogs

- Agent prompts: [agents/INDEX.md](agents/INDEX.md) (with token counts)
- Project-type prompts: [project-types/INDEX.md](project-types/INDEX.md)
- Workflow guides: [workflows/INDEX.md](workflows/INDEX.md)
- Archived prompts: [agents/archive/INDEX.md](agents/archive/INDEX.md)

## Foundation Prompt

| Prompt | Purpose | File |
|--------|---------|------|
| Foundation ⭐ | Universal best practices, APEI cycle | [View](base/claude-foundation-prompt.md) |

## Project-Type Prompts

| Prompt | Technologies | File |
|--------|-------------|------|
| Web Development | React 19, Vue, Angular, Svelte, Tailwind v4, Core Web Vitals | [View](project-types/web-development-prompt.md) |
| API Development | REST, GraphQL, gRPC, Hono, Fastify v5, idempotency | [View](project-types/api-development-prompt.md) |
| Data Science & ML | Python, PyTorch, scikit-learn, MLOps, LLM apps | [View](project-types/data-science-ml-prompt.md) |
| Mobile | Swift 6, Kotlin, Compose, KMP, React Native, Flutter | [View](project-types/mobile-development-prompt.md) |
| DevOps & CI/CD | Kubernetes, Gateway API, Docker, OpenTofu, GitHub Actions, Cloudflare | [View](project-types/devops-cicd-prompt.md) |
| Database & SQL | PostgreSQL 17, pgvector, Valkey, SQLite, indexing | [View](project-types/database-sql-prompt.md) |
| General Software | Python, TypeScript, Go, Rust, Java, C# | [View](project-types/general-software-development-prompt.md) |
| Game Development | Unity 6, Unreal 5, Godot 4, Bevy, netcode | [View](project-types/game-development-prompt.md) |
| Embedded & IoT | C, Rust (Embassy), ESP-IDF, Zephyr, Matter, MQTT 5, TinyML | [View](project-types/embedded-iot-prompt.md) |
| Blockchain & Web3 | Solidity 0.8, Foundry, L2s, ERC-4337/7702 | [View](project-types/blockchain-web3-prompt.md) |
| Desktop Apps | Tauri 2, Electron, .NET MAUI, Qt 6 | [View](project-types/desktop-development-prompt.md) |

## Examples & Guides

- Examples: [examples/](examples/)
- Workflow guides: [workflows/INDEX.md](workflows/INDEX.md)
- Prompt selector: [workflows/prompt-selector-guide.md](workflows/prompt-selector-guide.md)
- Prompt review checklist: [workflows/prompt-review-checklist.md](workflows/prompt-review-checklist.md)
- Portfolio maintenance: [workflows/portfolio-maintenance-guide.md](workflows/portfolio-maintenance-guide.md)
