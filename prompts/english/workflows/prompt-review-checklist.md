# Prompt Review Checklist

Use this checklist for periodic prompt quality reviews.

---

## Review Cadence

- Monthly: review recently edited prompts
- Quarterly: review all active prompts in `prompts/english/agents/`

---

## Mandatory Structure Check

- [ ] A `**Use this when:**` line and `**Skip to:**` anchor list under the title
- [ ] `## Role` exists (one or two sentences)
- [ ] A protocol section exists — `## Protocol: <ACRONYM>` or `## <Name> Protocol` — mapping to the phases
- [ ] Phase sections exist (`## Phase 1: …`, `## Phase 2: …`, or a single `## Phases`) with actionable `- [ ]` checklists or step lists
- [ ] `## Remember` exists and is the final section
- [ ] No stale versions or Claude model IDs stated from memory (see the Currency Rule in CONTRIBUTING.md)

---

## No Vague Advice Check

For each recommendation in the prompt:

- [ ] Ends with a concrete decision, or
- [ ] Names a concrete tool, or
- [ ] Includes a concrete validation step

Fail the review if a recommendation is generic without an action.

---

## Outcome & Clarity Check

- [ ] Prompt scope is explicit (what it should and should not do)
- [ ] Steps are ordered and executable
- [ ] Success criteria are measurable
- [ ] Internal links resolve

---

## Review Result Template

```markdown
## Prompt Review Result

**Prompt**: `<path>`
**Decision**: keep / update / merge / archive

### Structure
- Use this when / Skip to header: pass/fail
- Role: pass/fail
- Protocol: pass/fail
- Phase sections: pass/fail
- Remember final: pass/fail

### Currency
- No stale versions or model IDs: pass/fail
- Notes:

### No Vague Advice
- Pass/Fail
- Notes:

### Required Actions
1. ...
2. ...
```
