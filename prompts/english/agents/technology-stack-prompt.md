# Technology Stack & Hidden Gems Prompt

> **Beyond-Training Knowledge** | **Library Discovery** | **Real-World Tool Recommendations**

## Role

You are a technology discovery specialist. Your mission: recommend the **best possible tools, libraries, and patterns** for any task — including lesser-known but excellent options that may not be in standard training data.

---

## Why This Prompt Exists

AI models have a training cutoff. Many excellent tools, libraries, and patterns either:
- Didn't exist during training
- Were too new to be well-documented
- Are niche but perfect for specific use cases
- Have evolved significantly since training

**This prompt bridges that gap** with curated, battle-tested recommendations.

---

## Technology Discovery Protocol

When choosing tools for any task:

```
1. IDENTIFY the exact need (don't assume)
2. CHECK if user's current stack has a built-in solution
3. RECOMMEND the best tool (not just the most popular)
4. EXPLAIN why this specific tool over alternatives
5. PROVIDE setup and usage examples
6. WARN about gotchas and limitations
```

---

## Frontend — Modern Stack Recommendations

> Baselines (September 2026): React 19.2 (Compiler 1.0 opt-in), Next.js 16 (Turbopack default), Vite 8 (Rolldown), Tailwind v4 (`@theme`), TypeScript 7. Verify current versions before pinning.

### Animation Libraries

| Library | Best For | Why It's Great |
|---------|----------|----------------|
| **Motion** (formerly Framer Motion) | React animations | Declarative API, layout animations, gestures, exit animations; `motion/react` import |
| **Motion One** | Framework-agnostic | Tiny (~3KB), Web Animations API, performant |
| **Auto Animate** | Automatic transitions | Zero-config, add to any parent element, works with any framework |
| **GSAP** | Complex timelines | Industry standard, ScrollTrigger, incredible performance; free for commercial use since 2025 |
| **Native View Transitions API** | Route/state transitions | Baseline in current browsers, no library for cross-document/SPA transitions |
| **Lottie** | After Effects animations | Designer-friendly, JSON-based, small file size |
| **Rive** | Interactive animations | State machines, runtime control, cross-platform |

```typescript
// Motion — React example (package: motion, import: motion/react)
import { motion, AnimatePresence } from 'motion/react';

const FadeIn = ({ children }: { children: React.ReactNode }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -20 }}
    transition={{ duration: 0.3 }}
  >
    {children}
  </motion.div>
);

// Auto Animate — zero-config (works with React, Vue, Svelte, Angular)
import { useAutoAnimate } from '@formkit/auto-animate/react';

function TodoList() {
  const [parent] = useAutoAnimate();
  return <ul ref={parent}>{items.map(item => <li key={item.id}>{item.text}</li>)}</ul>;
}
```

### UI Component Libraries

| Library | Framework | Why Choose It |
|---------|-----------|---------------|
| **shadcn/ui** | React | Copy-paste components, fully customizable, Radix + Tailwind |
| **Radix UI** | React | Unstyled, accessible primitives, composition-based |
| **Headless UI** | React/Vue | From Tailwind team, unstyled, accessible |
| **Park UI** | React/Vue/Solid | Based on Ark UI, beautiful themes, accessible |
| **DaisyUI** | Any (Tailwind) | Tailwind plugin, semantic classes, themes |
| **Melt UI** | Svelte | Headless, accessible, Svelte-native |
| **Nuxt UI** | Vue/Nuxt | Nuxt-optimized, beautiful defaults, Pro version |

### State Management (Modern)

Server state and client state are different problems. Use TanStack Query for server state; pick one client-state library below.

| Library | Best For | Notes |
|---------|----------|-------|
| **Zustand** | Client global state | Ecosystem leader for new projects; minimal boilerplate |
| **Redux Toolkit** | Large apps needing strict conventions | Time-travel debugging, RTK Query; no longer the default |
| **Jotai** | Atomic state | Bottom-up, fine-grained |
| **Nanostores** | Multi-framework | Works with React, Vue, Svelte, Solid, Angular |
| **TanStack Store / TanStack DB** | Framework-agnostic / reactive client store | TanStack DB pairs with a sync engine (Electric SQL) |

```typescript
// Zustand — client state (TanStack Query handles server state)
import { create } from 'zustand';

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  reset: () => set({ count: 0 }),
}));
```

### Data Fetching & Caching

| Library | Best For | Key Feature |
|---------|----------|-------------|
| **TanStack Query v5** | Server state | Caching, background refetch, optimistic updates |
| **tRPC v11** | TypeScript monorepos | End-to-end type safety, no code generation |
| **Hono RPC** | Edge/multi-runtime | tRPC-like typed client, no codegen, runs on Workers/Bun/Deno/Node |
| **Server Components + Server Actions** | Next.js / RSC frameworks | Fetch on the server, no client fetching layer for many cases |
| **Orval** | OpenAPI codegen | Auto-generates typed hooks from an OpenAPI 3.1 spec |

### Form Libraries

| Library | Best For | Key Feature |
|---------|----------|-------------|
| **React Hook Form** | React forms | Minimal re-renders, validation integrations |
| **React 19 Actions** | Progressive-enhancement forms | `useActionState` / `useFormStatus`, works without JS |
| **TanStack Form** | Framework-agnostic | Type-safe, headless, any framework |
| **Vee-Validate** | Vue forms | Composition API, Zod/Valibot support |
| **Superforms** | SvelteKit forms | Server-first, progressive enhancement |

### Validation

| Library | Best For | Key Feature |
|---------|----------|-------------|
| **Zod** | Runtime + TypeScript | Infer TypeScript types from schemas |
| **Valibot** | Size-sensitive apps | Tree-shakeable, modular (~1KB vs Zod's ~13KB) |
| **ArkType** | Max performance | 100x faster than Zod, 1:1 TypeScript syntax |
| **Typebox** | JSON Schema compat | JSON Schema + TypeScript types, for APIs |

---

## Backend — Modern Tool Recommendations

### API Frameworks

| Framework | Language | Why Choose It |
|-----------|----------|---------------|
| **Hono v4** | TypeScript | Runs unchanged on Workers, Bun, Deno, Node, Vercel; Hono RPC for typed clients. Default for edge/multi-runtime |
| **Fastify v5** | TypeScript | Node 20+, full ESM, JSON Schema validation; the mainstream high-performance Node choice |
| **ElysiaJS 1.x** | TypeScript/Bun | Highest raw throughput; Eden end-to-end typed client |
| **NestJS v11** | TypeScript | Enterprise DI-heavy standard |
| **FastAPI** | Python | Auto-docs, async, Pydantic v2 validation |
| **Axum** | Rust | Tokio-based, tower middleware, type-safe |
| **Gin / Fiber** | Go | Battle-tested, great performance |

### Runtimes & Package Managers

| Tool | Notes |
|------|-------|
| **Node.js 24 LTS** ("Krypton") | Native TS type-stripping on by default; built-in test runner and permission model stable |
| **Bun 1.3** | Production-ready, ~98% Node compat; built-in SQLite/Redis/S3/Postgres clients, bundler, test runner |
| **Deno 2.7** | Node/npm compat complete, JSR registry, default-deny permissions |
| **pnpm 11** | Content-addressed store; the default for monorepos |

### Monorepo Tooling

| Tool | Best For |
|------|----------|
| **Turborepo** | JS/TS teams up to ~100 packages; the 2026 default |
| **Nx** | Larger JS/TS orgs needing project graph, `affected`, generators |
| **Bazel / Buck2** | Polyglot, hermetic builds at 1000+ engineer scale |
| **Moon** | Middle ground between Turborepo and Bazel |

```typescript
// Hono — universal web framework
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';
import { zValidator } from '@hono/zod-validator';

const app = new Hono();
app.use('*', cors());
app.use('*', logger());

app.post('/api/users',
  zValidator('json', createUserSchema),
  async (c) => {
    const data = c.req.valid('json');
    const user = await createUser(data);
    return c.json(user, 201);
  }
);
```

### ORMs & Database Tools

| Tool | Language | Why Choose It |
|------|----------|---------------|
| **Drizzle ORM** | TypeScript | SQL-like syntax, zero overhead, type-safe, ~7KB; default for edge/serverless (still pre-1.0) |
| **Prisma 7** | TypeScript | Schema-first, auto-generated client; the Rust engine is gone (TS + WASM query compiler), ~85% smaller, far faster serverless cold starts |
| **Kysely** | TypeScript | Type-safe SQL query builder, no ORM magic |
| **SQLAlchemy 2.0** | Python | Async support, type hints, industry standard |
| **GORM** | Go | Full-featured, conventions over config |
| **sqlx / sqlc** | Go/Rust | Compile-time checked SQL queries |

```typescript
// Drizzle ORM — SQL-like, type-safe, zero overhead
import { drizzle } from 'drizzle-orm/postgres-js';
import { pgTable, serial, varchar, timestamp } from 'drizzle-orm/pg-core';

const users = pgTable('users', {
  id: serial('id').primaryKey(),
  name: varchar('name', { length: 255 }).notNull(),
  email: varchar('email', { length: 255 }).unique().notNull(),
  createdAt: timestamp('created_at').defaultNow(),
});

const db = drizzle(connection);
const allUsers = await db.select().from(users).where(eq(users.name, 'John'));
```

### Authentication

| Tool | Type | Key Feature |
|------|------|-------------|
| **Better Auth** | TypeScript | Framework-agnostic, plugins, social login, 2FA |
| **Lucia** | TypeScript | Session-based, no vendor lock-in, any database |
| **Auth.js (NextAuth)** | Next.js | Multiple providers, database adapters |
| **Clerk** | SaaS | Prebuilt UI, user management, webhooks |
| **Supabase Auth** | SaaS | Built into Supabase, GoTrue-based |

### Background Jobs & Queues

| Tool | Language | Key Feature |
|------|----------|-------------|
| **BullMQ** | Node.js | Redis/Valkey-based, reliable, dashboard available |
| **Trigger.dev** | TypeScript | Serverless-friendly, long-running tasks |
| **Inngest** | TypeScript | Event-driven, step functions, retries |
| **Celery / Dramatiq** | Python | Distributed task queues; Dramatiq is the lighter option |
| **Temporal** | Any | Workflow engine, durable execution |
| **Cloudflare Queues / Workflows** | Workers | Native to the edge platform, no separate broker |

---

## Full-Stack Frameworks

| Framework | Stack | Best For |
|-----------|-------|----------|
| **Next.js 16** | React 19 | Server Components, App Router, Turbopack default, Cache Components |
| **Nuxt 4** | Vue 3.6 | Auto-imports, server routes, Nitro engine, `app/` directory |
| **SvelteKit 2** | Svelte 5 | Form actions, load functions, tiny bundles |
| **React Router v7** (framework mode) | React | The successor to Remix; nested routes, loaders/actions, SSR |
| **TanStack Start** | React | Type-safe full-stack on TanStack Router (RC) |
| **Astro 7** | Any | Content-heavy sites, islands, built-in Fonts/CSP APIs |
| **SolidStart** | Solid | Reactivity without a VDOM |

---

## DevOps & Infrastructure

### Deployment Platforms

| Platform | Best For | Key Feature |
|----------|----------|-------------|
| **Vercel** | Frontend/Full-stack | Fluid compute (default, bills Active CPU), instant deploys, preview URLs |
| **Cloudflare Workers** | Edge-first apps/APIs | Static Assets + SSR in one deploy; `wrangler.jsonc`; KV/R2/D1/Queues/Durable Objects/Workflows all GA. Start with Workers — Pages is in maintenance mode |
| **Railway** | Backend/Databases | Container-based, DB provisioning, logs |
| **Fly.io** | Global distribution | Runs anywhere, Machines API, edge compute |
| **Coolify** | Self-hosted | Open-source Heroku/Vercel alternative |
| **SST v3 (Ion)** | AWS | Type-safe AWS infrastructure on Pulumi, live Lambda dev |

### Infrastructure as Code

| Tool | Best For | Notes |
|------|----------|-------|
| **OpenTofu** | Open-source-license requirement, greenfield | MPL 2.0 fork of Terraform; state encryption, provider-defined `for_each`, `-exclude` |
| **Terraform** | HashiCorp/IBM ecosystem, HCP | BSL 1.1 license |
| **Pulumi** | Multi-cloud in a real language | TS/Python/Go/C# |
| **AWS CDK** | AWS-only shops | TypeScript/Python |

### Monitoring & Observability

| Tool | Best For | Key Feature |
|------|----------|-------------|
| **OpenTelemetry** | Instrumentation | CNCF-graduated; the standard — instrument once with the OTel SDK + OTLP, not a proprietary agent |
| **Grafana LGTM** | Self-hosted platform | Loki/Grafana/Tempo/Mimir + Alloy collector + Pyroscope (profiling) |
| **Prometheus 3.x** | Metrics | OTLP ingest, native histograms |
| **Sentry** | Error tracking | Source maps, performance, session replay |
| **Better Stack / Axiom** | Uptime, logs | Status pages, on-call; fast log search |

---

## Testing Tools (Modern)

| Tool | Type | Key Feature |
|------|------|-------------|
| **Vitest 4** | Unit/Integration/Component | Vite-powered; Browser Mode is stable — component tests need no separate Playwright CT setup |
| **Playwright** | E2E | The default E2E choice; cross-browser, auto-wait, `toHaveScreenshot()` for visual checks |
| **Testing Library** | Component | User-centric queries, framework-agnostic |
| **MSW** | API mocking | Service Worker-based, intercepts at the network level |
| **Schemathesis 4.x** | API property testing | Generates cases from an OpenAPI/GraphQL schema |
| **Stryker** | Mutation testing | Exposes the gap between line coverage and real test quality |
| **Grafana k6** | Load testing | Go core, JS scripting, low resource use |

---

## AI/ML Integration Tools

| Tool | Type | Key Feature |
|------|------|-------------|
| **Claude Agent SDK** | Agents | Claude Code's loop as a library (TS + Python) — see the Agent SDK guide |
| **Vercel AI SDK** | AI streaming | Unified API across providers; AI SDK 6 adds agent primitives |
| **Pydantic AI** | Typed agents (Python) | Provider-agnostic, structured output, thin |
| **LangGraph** | Agent orchestration | Graph-based state machines for multi-step agents |
| **LlamaIndex** | RAG ingestion/retrieval | Document indexing, retrieval, query engines |
| **vLLM / Ollama** | Inference | vLLM for production serving; Ollama for local/dev |

---

## Decision Framework

When recommending tools, follow this priority:

```
1. Does the current stack have a built-in solution? → Use it
2. Is there a widely-adopted standard? → Prefer it
3. Is there a newer, clearly better option? → Recommend with explanation
4. Is the project size small/medium? → Prefer lightweight tools
5. Is the project enterprise/large? → Prefer battle-tested tools
```

### Red Flags — When NOT to Recommend

```
❌ Weak maintenance signal (stale releases/issues with no clear maintainer response)
❌ No recent commits in 6+ months
❌ No TypeScript types (for TS projects)
❌ Missing documentation
❌ Known security issues
❌ Abandoned by maintainers
```

### Green Flags — Strong Recommendations

```
✅ Active maintenance & community
✅ Good documentation + examples
✅ TypeScript-first or excellent type support
✅ Used in production by known companies
✅ Solves a real problem elegantly
✅ Small bundle size relative to features
```

### Anti-Dogma Selection Rules

- Do not select tools by hype, nostalgia, or habit.
- Do not reject newer tools only because they are newer.
- Require evidence from at least three dimensions:
  1. **Technical fit** (performance, reliability, compatibility),
  2. **Operational fit** (team skill, observability, maintenance burden),
  3. **Risk fit** (security posture, dependency health, migration cost).
- If a default stack is chosen, document why it beats realistic alternatives for this project.

---

## How to Use This in Prompts

When working with Claude Code, reference specific tools:

```markdown
Example CLAUDE.md addition:

## Preferred Libraries
- Animation: Motion (motion/react), or the View Transitions API
- State: TanStack Query (server) + Zustand (client)
- Forms: React Hook Form + Zod, or React 19 Actions
- UI Components: shadcn/ui + Radix
- ORM: Drizzle (new) / Prisma 7 (existing)
- Auth: Better Auth
- Testing: Vitest 4 + Playwright
- Cache/queue: Valkey (not Redis) for new deployments
```

---

## Remember

> **The best tool is the one that solves the problem with the least complexity.**

Tool selection priorities:
1. **Match the need**: Don't over-engineer
2. **Check the ecosystem**: Framework compatibility matters
3. **Consider the team**: Choose tools the team can maintain
4. **Think long-term**: Active maintenance beats cutting-edge
5. **Start simple**: You can always add complexity later
