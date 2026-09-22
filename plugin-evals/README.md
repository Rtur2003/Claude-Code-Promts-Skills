# Native Plugin Evals

Behavioral trigger cases for Claude Code's native `claude plugin eval` runner. The plugin manifest selects this directory through `experimental.evals` because `evals/` already contains the library's zero-cost static/live routing harness.

## Cases

- [Evidence research routing](find-evidence-research/prompt.md)
  - [Find-prompt trigger grader](find-evidence-research/graders/find-prompt-fired.md)
  - [Research-route output grader](find-evidence-research/graders/research-route.md)
- [Small plugin capability audit](audit-small-plugin/prompt.md)
  - [Capability-audit trigger grader](audit-small-plugin/graders/capability-audit-fired.md)
- [Unrelated copy edit](ignore-unrelated-copy-edit/prompt.md)
  - [Negative trigger grader](ignore-unrelated-copy-edit/graders/no-capability-audit.md)

## Run

```bash
claude plugin eval . --runs 1 --max-cost-usd 1 --no-publish
```

Each case is a real model session. The default with/without-plugin baseline doubles the agent runs, so keep `--runs 1` while iterating and use the default three runs only for a result you intend to trust. Native Windows cannot run shell-granted eval cases because it has no Claude Code sandbox backend; these trigger cases request only the read-only `Skill` tool.
