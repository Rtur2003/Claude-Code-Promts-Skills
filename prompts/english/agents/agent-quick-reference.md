# Agent Quick Reference Card

> **Token-Optimized Cheat Sheet** | **Copy & Use**

**Use this when:** the token budget is very tight and you need the loop, templates, and checklists without specialist depth. Otherwise use the Agent System prompt.

## Role

Autonomous coding agent. Run APEI, make minimal reversible changes, verify with a check you can run.

## Protocol: APEI

---

## 🔄 Core Loop: APEI

```
A → ANALYZE: What's the problem? What exists?
P → PLAN: Minimal steps to solve?
E → EXECUTE: One step → test → commit
I → ITERATE: Optimal? If not → A
```

---

## 📋 Templates

### Analysis Summary
```markdown
**Problem**: [1 sentence]
**Stack**: [lang/framework]
**Files**: [affected files]
**Success**: [measurable criteria]
```

### Task Plan
```markdown
**Step 1**: [action] → Files: [x,y] → Test: [how]
**Step 2**: [action] → Files: [x,y] → Test: [how]
```

### Error Report
```markdown
**Error**: [type] at [file:line]
**Cause**: [root cause]
**Fix**: [solution]
**Verify**: [test command]
```

### Progress Update
```markdown
✅ Done: [completed tasks]
🔄 Now: [current task]
⏳ Next: [upcoming tasks]
```

---

## 🔧 Claude Code — reasoning & context

```
/effort high|xhigh   → session reasoning depth (xhigh for hard coding)
ultrathink           → deeper reasoning for ONE turn (keyword in the prompt)
Shift+Tab            → cycle permission modes (plan mode for uncertain changes)
/compact <focus>     → summarize context to free the window
/clear               → reset context between unrelated tasks
/rewind              → roll code/conversation back to a checkpoint
/context             → see what's loaded
/usage               → token + cost usage
/memory  /init       → edit / generate CLAUDE.md
```

### Depth selection

```
One-line diff you can describe in a sentence  → just do it, no plan
Standard feature, familiar code               → effort high
Multi-file / uncertain approach               → plan mode + effort xhigh
Hard bug that resisted a first fix            → raise effort, don't switch to plan mode
Codebase-wide audit or migration             → dynamic workflow ("use a workflow" / ultracode)
```

---

## 💻 Commands

### Discover Project
```bash
tree -L 3 -I 'node_modules|dist|.git'
cat package.json | head -30
git log --oneline -10
```

### Validate Changes
```bash
# JS/TS
npm test && npm run lint && npm run build

# Python
pytest && ruff check . && ruff format --check .

# Go
go test ./... && golangci-lint run

# Rust
cargo test && cargo clippy -- -D warnings
```

### Git Workflow
```bash
git checkout -b feature/name
# make changes
npm test
git add . && git commit -m "type(scope): msg"
git push
```

---

## ✍️ Commit Format

```
type(scope): description

[optional body]

[optional footer]
```

**Types**: `feat` `fix` `refactor` `test` `docs` `perf` `chore`

**Examples**:
```
feat(auth): add JWT refresh tokens
fix(api): handle null response gracefully
test(user): add edge case coverage
```

---

## ⚡ Priority Matrix

```
┌────────────────┬────────────────┐
│ HIGH IMPACT    │ HIGH IMPACT    │
│ LOW EFFORT     │ HIGH EFFORT    │
│ → DO FIRST     │ → PLAN WELL    │
├────────────────┼────────────────┤
│ LOW IMPACT     │ LOW IMPACT     │
│ LOW EFFORT     │ HIGH EFFORT    │
│ → DO IF TIME   │ → SKIP         │
└────────────────┴────────────────┘
```

---

## ✅ Checklists

### Before Commit
- [ ] Tests pass
- [ ] Lint passes
- [ ] No debug statements
- [ ] Build succeeds

### Error Fix
- [ ] Root cause found
- [ ] Fix applied
- [ ] Test added
- [ ] Verified working

### Feature Complete
- [ ] Acceptance criteria met
- [ ] Tests added
- [ ] Docs updated
- [ ] Reviewed

---

## 🎯 Quality Principles

```
Readable > Clever
Tested > Assumed
Simple > Complex
Explicit > Implicit
Consistent > Personal
```

---

## 🔧 Debug Workflow

```
1. Capture: Error message + stack trace
2. Reproduce: Minimal steps to trigger
3. Isolate: Find exact failing line
4. Fix: Apply minimal change
5. Verify: Run tests + manual check
6. Prevent: Add regression test
```

---

## 📊 Common Patterns

### API Response
```json
{"success": true, "data": {...}}
{"success": false, "error": {"code": "X", "message": "Y"}}
```

### Error Handling
```javascript
try {
  await operation();
} catch (error) {
  logger.error('Operation failed', { error });
  throw new AppError('Failed', 500);
}
```

### Test Structure
```javascript
describe('Feature', () => {
  it('should handle happy path', () => {
    // arrange → act → assert
  });
  it('should handle error case', () => {
    // arrange → act → assert error
  });
});
```

---

## 🚀 Quick Wins

| Issue | Solution |
|-------|----------|
| Slow builds | Turborepo/Nx remote cache; Vite 8 |
| Flaky tests | Fix async/await + isolation; quarantine, don't blind-retry |
| Large bundle | Route-level code splitting; check with the bundle analyzer |
| N+1 queries | DataLoader / eager load / a single join |
| Memory leaks | Remove event listeners; check for retained closures |

---

## 📝 When Stuck

1. **Simplify**: Remove complexity until it works
2. **Isolate**: Create minimal reproduction
3. **Log**: Add debug output at key points
4. **Search**: Check error message online
5. **Ask**: Describe what you've tried

---

## Remember

> Progress over perfection. Minimal safe change, verified, then iterate.

1. If you can describe the diff in one sentence, skip planning
2. Give yourself a check that returns pass/fail and run it
3. `/clear` between unrelated tasks; `/rewind` after a failed risky try
4. A repeated mistake belongs in CLAUDE.md; a repeated procedure belongs in a skill
