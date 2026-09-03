# Claude Code Plugins Prompt

> **plugin.json Manifest** | **Bundled Components** | **Marketplace Distribution**

**Use this when:** packaging skills, subagents, hooks, MCP servers, or LSP configs into one installable unit to reuse across repos or share with a team or the community.
**Skip to:** [Protocol](#protocol-bundle) · [Phase 1 Decide](#phase-1-decide--plugin-or-standalone) · [Phase 2 Build](#phase-2-build--directory-and-manifest) · [Components](#components) · [Phase 3 Test](#phase-3-test--load-locally) · [Phase 4 Distribute](#phase-4-distribute--marketplace) · [Remember](#remember)

## Role

You build and distribute Claude Code plugins. A plugin is a directory with a `.claude-plugin/plugin.json` manifest plus component directories at the plugin root. It bundles skills, subagents, hooks, MCP servers, LSP configs, background monitors, and default settings into a versioned unit that installs from a marketplace with one command.

## Protocol: BUNDLE

```
B → BOUNDARY  — Decide plugin vs standalone .claude/ config
U → UNIT      — Create the directory and plugin.json manifest
N → NEST      — Add components at the plugin root (never inside .claude-plugin/)
D → DRIVE     — Test with --plugin-dir; iterate with /reload-plugins
L → LIST      — Publish through a marketplace.json
E → EVOLVE    — Bump version on every change users should receive
```

Stop only when `claude --plugin-dir ./<plugin>` loads every component, `/help` shows the namespaced skills, and `claude plugin validate` passes.

---

## Phase 1: DECIDE — plugin or standalone?

| Approach | Skill name | Best for |
|---|---|---|
| **Standalone** `.claude/` directory | `/hello` | Personal workflow, one-project customization, fast iteration |
| **Plugin** | `/plugin-name:hello` | Sharing with teammates, distributing to the community, versioned releases, reuse across repos |

Start standalone. Convert to a plugin when a second repo needs the same setup, or when you want to distribute it.

### Convert existing `.claude/` config

```bash
mkdir -p my-plugin/.claude-plugin
# manifest (below), then:
cp -r .claude/skills my-plugin/
cp -r .claude/agents my-plugin/
# hooks: copy the "hooks" object from settings.json into my-plugin/hooks/hooks.json
```

After migrating, remove the originals from `.claude/` — project/user `.claude/agents/` override same-named plugin agents, so the plugin version takes effect only once the originals are gone. Plugin skills are namespaced, so `/skill-name` and `/plugin:skill-name` both remain.

---

## Phase 2: BUILD — directory and manifest

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # ONLY this goes inside .claude-plugin/
├── skills/
│   └── review/SKILL.md
├── agents/
│   └── security-reviewer.md
├── hooks/
│   └── hooks.json
├── .mcp.json
├── .lsp.json
├── monitors/
│   └── monitors.json
├── bin/                      # executables added to Bash PATH while enabled
└── settings.json             # default settings when enabled (agent, subagentStatusLine)
```

**The one common mistake:** only `plugin.json` goes inside `.claude-plugin/`. Every component directory (`skills/`, `agents/`, `hooks/`, `.mcp.json`, …) sits at the plugin root. The plugin root is the directory you pass to `--plugin-dir` — never `~/.claude/`.

### plugin.json

```json
{
  "name": "acme-tools",
  "description": "Acme's shared review, deploy, and DB workflows",
  "version": "1.2.0",
  "author": { "name": "Acme Platform Team" },
  "homepage": "https://github.com/acme/claude-plugins",
  "repository": "https://github.com/acme/claude-plugins",
  "license": "MIT"
}
```

| Field | Purpose |
|---|---|
| `name` | Unique id and skill namespace. Skills become `/acme-tools:review`. |
| `description` | Shown in the plugin manager. |
| `version` | If set, users receive updates only when you bump it. If omitted, version falls back to the source. |
| `author`, `homepage`, `repository`, `license` | Optional; attribution and discovery. |

A plugin that ships exactly one skill can put `SKILL.md` at the plugin root and use its frontmatter `name` for the command.

---

## Components

| Component | File | Notes |
|---|---|---|
| **Skills** | `skills/<name>/SKILL.md` | Namespaced `/plugin:name`. Model-invoked by default. Full authoring: [agent-skills-prompt](agent-skills-prompt.md). |
| **Subagents** | `agents/<name>.md` | Same frontmatter as project agents. Overridden by same-named project/user agents. See [multi-agent-orchestration-prompt](multi-agent-orchestration-prompt.md). |
| **Hooks** | `hooks/hooks.json` | Same schema as the `hooks` object in `settings.json`. Command receives hook JSON on stdin. See [hooks-automation-prompt](hooks-automation-prompt.md). |
| **MCP servers** | `.mcp.json` | Same entry shape as project `.mcp.json`. `${CLAUDE_PLUGIN_ROOT}` resolves to the install dir. See [mcp-integration-prompt](mcp-integration-prompt.md). |
| **LSP servers** | `.lsp.json` | Code intelligence. Users need the language-server binary installed. Prefer the official pre-built LSP plugins for common languages. |
| **Monitors** | `monitors/monitors.json` | Background watchers; each stdout line is delivered to Claude as a notification. Started automatically when the plugin is active. |
| **Executables** | `bin/` | Added to the Bash tool's `PATH` while the plugin is enabled. Not allowed in plugins distributed through claude.ai org settings. |
| **Default settings** | `settings.json` | Only `agent` (activate a plugin agent as the main thread) and `subagentStatusLine` keys are honored. |
| **Workflows** | `workflows/` | Dynamic-workflow scripts, namespaced `/plugin:workflow-name`. |

Variables inside plugin skills: `${CLAUDE_PLUGIN_ROOT}` (install dir), `${CLAUDE_PLUGIN_DATA}` (persistent data dir that survives updates).

### hooks.json example

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "jq -r '.tool_input.file_path' | xargs npm run lint:fix" }
        ]
      }
    ]
  }
}
```

---

## Phase 3: TEST — load locally

```bash
claude --plugin-dir ./my-plugin              # load one plugin for this session
claude --plugin-dir ./my-plugin.zip          # a zipped plugin
claude --plugin-url https://ci.example.com/build/my-plugin.zip   # fetched at startup
claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two       # multiple
```

- `/reload-plugins` picks up edits without restarting (skills, agents, hooks, plugin MCP, plugin LSP).
- `claude plugin init <name>` scaffolds a skills-directory plugin at `~/.claude/skills/<name>/` that loads automatically as `<name>@skills-dir` — no marketplace needed for personal use.
- A local `--plugin-dir` plugin overrides an installed marketplace plugin of the same name for that session (except managed force-enabled/disabled plugins).

### Verify each component

- [ ] Skills: `/plugin-name:skill-name` runs
- [ ] Agents: appear in `/context` under Custom Agents; `@`-mention by scoped name works
- [ ] Hooks: trigger the matching event, confirm the effect; check the debug log for matched hooks and exit codes
- [ ] MCP: `/mcp` shows the server connected
- [ ] LSP: `/plugin` **Errors** tab is clean (a missing binary shows `Executable not found in $PATH`)

```bash
claude plugin validate ./my-plugin           # add --strict to fail on warnings
```

---

## Phase 4: DISTRIBUTE — marketplace

### Team / private marketplace

`.claude-plugin/marketplace.json` in a repo:

```json
{
  "name": "acme",
  "owner": { "name": "Acme Platform Team" },
  "plugins": [
    {
      "name": "acme-tools",
      "source": "./plugins/acme-tools",
      "description": "Shared review, deploy, and DB workflows"
    }
  ]
}
```

```bash
claude plugin marketplace add acme/claude-plugins        # GitHub or GitLab owner/repo
/plugin install acme-tools@acme
/plugin uninstall acme-tools@acme
```

Settings: `additionalMarketplaces` (register extra ones), `allowedMarketplaces` (restrict to a list), `blockedMarketplaces` (policy deny). Private repos work — the marketplace clones with your git credentials. Add `enabledPlugins` to `.claude/settings.json` so a repo declares its plugins for everyone (including cloud sessions).

### Public marketplaces

| Marketplace | What it is | Add / install |
|---|---|---|
| `claude-plugins-official` | Curated by Anthropic. Auto-registered on first interactive launch. | `claude plugin marketplace add anthropics/claude-plugins-official` |
| `claude-community` | Public community submissions after review. | `/plugin marketplace add anthropics/claude-plugins-community`, install `@claude-community` |

Submit to the community marketplace via claude.ai (`claude.ai/admin-settings/directory/submissions/plugins/new`, needs a Team/Enterprise org) or Console (`platform.claude.com/plugins/submit`, individuals). Run `claude plugin validate` first — the review pipeline runs the same check plus safety screening. Approved plugins are pinned to a commit SHA and synced nightly.

The official marketplace is curated separately; the submission form does not add to it.

---

## Phase 5: EVOLVE — versioning

- Set `version` in `plugin.json`. Users receive an update only when you bump it.
- Semantic versioning: patch for fixes, minor for new components, major for breaking changes to a skill's interface.
- Ship a `README.md` with install and usage instructions.
- `plugin-dependencies` lets you declare version constraints on other plugins your plugin needs.

---

## Remember

> **A plugin is the packaging layer, not a new capability. Build the components first, then bundle what proved useful.**

Before publishing:
1. Every component works when loaded with `--plugin-dir`
2. `claude plugin validate` passes (`--strict` for a public submission)
3. `version` is set and the README explains what installs
4. Nothing sensitive is in `bin/`, `.mcp.json` env, or committed config
