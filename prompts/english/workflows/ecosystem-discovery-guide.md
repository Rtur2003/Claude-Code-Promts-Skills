# Capability Ecosystem Discovery Guide

> **Skills** | **Claude Code Plugins** | **MCP Servers** | **Popularity-Resistant Selection**

**Use this when:** deciding whether to build, install, or recommend an agent skill, Claude Code plugin, MCP server, hook bundle, or code-intelligence extension.
**Last researched:** 2026-09-22. Re-check live state before installation.

## Role

You discover capabilities without confusing visibility with fitness. You search official registries and small projects, inspect the actual distribution artifact, and produce a shortlist whose trust boundary and maintenance cost are explicit.

## Protocol: SCOUT

```text
S -> SPECIFY   Name the missing capability and the minimum useful interface
C -> COLLECT   Search official catalogs, vendor repos, registries, and small projects
O -> OPEN      Inspect manifests, skills, hooks, MCP config, scripts, and licenses
U -> UNDERCUT  Challenge the popularity leader with specialized alternatives
T -> TRIAL     Install narrowly, verify runtime behavior, and keep an exit path
```

---

## Search order

1. Built-in Claude Code capability: avoid an extension when the native tool already solves the job.
2. Official Anthropic plugin marketplace and `anthropics/skills`.
3. Vendor-maintained plugin or hosted MCP server for the system being accessed.
4. Anthropic community marketplace and the official MCP Registry.
5. Independent repositories found through problem- and failure-oriented searches.

The community marketplace applies automated validation and safety screening and pins submissions to a commit SHA. That is a useful provenance layer, not a production-security guarantee. The official MCP reference-server repository explicitly describes its servers as educational reference implementations rather than production-ready services.

Primary discovery points:

- [Claude Code plugin discovery](https://code.claude.com/docs/en/discover-plugins)
- [Anthropic official marketplace](https://github.com/anthropics/claude-plugins-official)
- [Anthropic community marketplace](https://github.com/anthropics/claude-plugins-community)
- [Anthropic Agent Skills](https://github.com/anthropics/skills)
- [Official MCP Registry](https://registry.modelcontextprotocol.io/)
- [MCP reference servers](https://github.com/modelcontextprotocol/servers)

---

## Candidate scorecard

Score evidence, not reputation. Use `unknown` when a field was not verified; do not silently award the point.

| Dimension | Weight | Evidence |
|---|---:|---|
| Task fit and unique leverage | 25 | The capability removes a real repeated failure or expensive manual step |
| Security and blast radius | 20 | Narrow tools, explicit writes, no secret embedding, reviewed scripts, bounded network/filesystem access |
| Runtime proof | 15 | Tests, evals, smoke test, reproducible demo, or direct local verification |
| Maintenance health | 10 | Recent meaningful activity, responsive issues, non-archived status, clear ownership |
| Interoperability | 10 | Open Agent Skills/MCP format, portable data, standard config, limited vendor lock-in |
| Installation and rollback | 10 | Pinned artifact, documented prerequisites, scoped install, clean disable/uninstall path |
| Documentation and discoverability | 5 | Precise trigger descriptions, examples, limits, and troubleshooting |
| Adoption signal | 5 | Stars/downloads/users; capped so popularity cannot dominate |

Reject regardless of score when the artifact hides required credentials, downloads unpinned executables without verification, grants broad shell/filesystem access without need, has an incompatible license, or cannot explain what leaves the machine.

---

## Small-project research seeds

These are research leads, not endorsements. They were present in Anthropic's community marketplace and their repositories were inspected through GitHub metadata on the date above. Re-run `capability-audit` and read the current source before installing.

| Candidate | Narrow value | Why it is easy to miss | Verify before use |
|---|---|---|---|
| `agent-trace-triage` | Deterministic loop/failure detection for JSON/JSONL agent traces | Tiny adoption signal; unusually specific problem | Parser coverage, generated test quality, Node requirement |
| `agent-smith` | Audits Claude configuration across security, context, hooks, and MCP | Small project in a crowded “agent setup” category | Scoring method, suggested-edit safety, scope honesty |
| `agent-discover` | MCP Registry browser, activation proxy, health and call metrics | Infrastructure utility rather than a flashy end-user tool | Secret storage, proxy isolation, supply-chain pinning |
| `privacy-audit` | Compares privacy/terms claims with code, schema, dependencies, and APIs | Crosses legal-document and code-review boundaries | Jurisdiction limits, false positives, professional-review boundary |
| `adaptive-agent` | Skill hygiene and user-profile feedback loops | Self-improvement claims are easy to over-trust | Memory privacy, drift controls, reversible changes |
| `conjure` | Generates skills, hooks, agents, and MCP scaffolds | One-repository plugin with a very small adoption signal | Generated permissions, template freshness, validation coverage |
| `autoresearch-ai-plugin` | Measure/keep/discard experiment loop for optimization targets | Useful outside model training but described as “autoresearch” | Stop conditions, cost ceilings, state rollback |
| `probabl-skills` | Focused Python ML experimentation workflows | Domain-specific and overshadowed by generic data-science bundles | Library versions, statistical rigor, maintained examples |
| `gograph` | Local AST/call-graph/impact analysis for Go via MCP | Language-specific; value appears only in larger Go repos | Binary provenance, MCP tool count, read/write boundary |

High-value official capabilities that complement this library include `skill-creator` for with/without skill benchmarks, `plugin-dev` for extension scaffolding, `claude-code-setup` for project-specific automation recommendations, LSP plugins for language-aware diagnostics, and `claude-security` for deep code scanning. Install only the capability needed for the current project.

---

## Installation gate

Before installation:

- [ ] Open the exact pinned commit or package version, not only the default branch
- [ ] Read `plugin.json`, marketplace entry, every `SKILL.md` frontmatter, hooks, `.mcp.json`, and executable scripts
- [ ] Confirm license, owner, update source, prerequisites, and uninstall path
- [ ] Identify every write, external request, credential, and spawned process
- [ ] Prefer project or local scope for evaluation; avoid user-wide activation first
- [ ] Run `claude plugin validate` and any shipped tests without enabling real MCP writes
- [ ] Test one representative task plus one should-not-trigger task
- [ ] Record what was installed, authenticated, runtime-tested, and still unverified as separate states

For MCP, prefer a vendor-hosted OAuth endpoint when available. For a local server, pin the package version and review the process it starts. Tool annotations are untrusted hints; they do not enforce safety.

---

## Remember

> **The best extension is the smallest trusted capability that closes a measured gap.**

1. Search broadly, adopt narrowly.
2. A marketplace listing improves provenance; it does not remove the need to inspect code and permissions.
3. Cap popularity at a small part of the score so specialized tools can win on fit.
4. Keep installation, authentication, and runtime verification as three separate claims.
