# Project-Type Prompts Index

> Use with the [Foundation Prompt](../base/claude-foundation-prompt.md) for interactive Claude sessions.

## Catalog

| # | Prompt | Technologies | File |
|---|--------|-------------|------|
| 1 | **Web Development** | React 19, Vue, Angular, Svelte 5, Tailwind v4, Core Web Vitals | [View](web-development-prompt.md) |
| 2 | **API Development** | REST, GraphQL, gRPC, Hono, Fastify v5, idempotency, OpenAPI 3.1 | [View](api-development-prompt.md) |
| 3 | **Data Science & ML** | Python, PyTorch, scikit-learn, MLOps, LLM apps, vector DBs | [View](data-science-ml-prompt.md) |
| 4 | **Mobile** | Swift 6, Kotlin, Jetpack Compose, KMP, React Native, Flutter | [View](mobile-development-prompt.md) |
| 5 | **DevOps & CI/CD** | Kubernetes, Gateway API, Docker, OpenTofu, GitHub Actions, Cloudflare | [View](devops-cicd-prompt.md) |
| 6 | **Database & SQL** | PostgreSQL 17, pgvector, Valkey, SQLite, indexing | [View](database-sql-prompt.md) |
| 7 | **General Software** | Python, TypeScript, Go, Rust, Java, C# | [View](general-software-development-prompt.md) |
| 8 | **Game Development** | Unity 6, Unreal 5, Godot 4, Bevy, netcode | [View](game-development-prompt.md) |
| 9 | **Embedded Systems & IoT** | C, Rust (Embassy), ESP-IDF, Zephyr, Matter, MQTT 5, TinyML | [View](embedded-iot-prompt.md) |
| 10 | **Blockchain & Web3** | Solidity 0.8, Foundry, L2s, ERC-4337/7702 | [View](blockchain-web3-prompt.md) |
| 11 | **Desktop Apps** | Tauri 2, Electron, Qt 6, .NET MAUI | [View](desktop-development-prompt.md) |

---

## Usage

### Option 1: Foundation + Project Type
Combine the Foundation prompt with a project-type prompt for domain-specific guidance.

### Option 2: Multi-Domain
Combine Foundation + multiple project-type prompts for full-stack work:
```
Foundation + Web Development + API Development
```

---

## Recommended Combinations

| Project | Prompts |
|---------|---------|
| React / Vue app | Foundation + Web Development |
| REST / GraphQL API | Foundation + API Development |
| ML / Data Science | Foundation + Data Science & ML |
| iOS / Android app | Foundation + Mobile |
| DevOps / Infra | Foundation + DevOps & CI/CD |
| Database design | Foundation + Database & SQL |
| General software | Foundation + General Software |
| Game development | Foundation + Game Development |
| Embedded / IoT | Foundation + Embedded Systems & IoT |
| Smart contracts / dApps | Foundation + Blockchain & Web3 |
| Desktop app | Foundation + Desktop Apps |
| Full-stack app | Foundation + Web + API |
