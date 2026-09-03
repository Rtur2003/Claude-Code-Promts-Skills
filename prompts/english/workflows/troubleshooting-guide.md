# Troubleshooting Decision Flowchart

> A systematic guide for diagnosing and resolving issues using the right prompts and tools.

## Quick Decision Tree

```
Issue Detected
│
├── Is the app crashing or completely broken?
│   ├── YES → P0: Use Agent System + Debugging & Troubleshooting
│   └── NO ↓
│
├── Is it a performance problem?
│   ├── YES → Use Agent System + Performance Optimization
│   │   ├── Frontend slow? → Check Core Web Vitals, bundle size
│   │   ├── Backend slow? → Profile endpoints, check DB queries
│   │   └── Infrastructure? → Check CPU, memory, network, scaling
│   └── NO ↓
│
├── Is it a security concern?
│   ├── YES → Use Agent System + Security Audit
│   │   ├── Vulnerability found? → OWASP Top 10 analysis
│   │   ├── Dependency issue? → npm audit / pip audit
│   │   └── Data breach risk? → Add Compliance & Governance
│   └── NO ↓
│
├── Is it a deployment/infrastructure issue?
│   ├── YES → Use Agent System + Cloud & Infrastructure
│   │   ├── Container issues? → Check logs, resources, probes
│   │   ├── Scaling issues? → Review HPA, resource limits
│   │   └── Network issues? → DNS, certificates, security groups
│   └── NO ↓
│
├── Is it a data issue?
│   ├── YES → Use Data Engineering or Database & SQL
│   │   ├── Pipeline failure? → Check DAG logs, data quality
│   │   ├── Query performance? → EXPLAIN ANALYZE, add indexes
│   │   └── Data drift? → Model monitoring, quality checks
│   └── NO ↓
│
└── Is it a code quality issue?
    ├── YES → Use Agent System + Code Review / Refactoring
    └── NO → Start with Agent System + Debugging & Troubleshooting
```

## Diagnostic Workflow

### Step 1: Identify the Symptom

| Symptom | Category | First Check |
|---------|----------|-------------|
| App won't start | Crash | Logs, dependencies, config |
| Slow response time | Performance | Profiler, network tab, DB queries |
| Wrong data returned | Logic Bug | Unit tests, input validation |
| Intermittent errors | Reliability | Logs over time, resource limits |
| High memory usage | Memory Leak | Heap snapshots, process monitoring |
| Failed deployment | DevOps | CI/CD logs, health checks |
| 500 errors in prod | Backend | Application logs, error tracking |
| UI not rendering | Frontend | Console errors, network tab |
| Auth failures | Security | Token expiry, CORS, cookies |
| Data inconsistency | Database | Transactions, race conditions |

### Step 2: Gather Evidence

```bash
# Quick system health check
echo "=== System Resources ===" && free -h && df -h
echo "=== Recent Errors ===" && journalctl --since "1 hour ago" -p err --no-pager | tail -20
echo "=== Process Status ===" && ps aux --sort=-%mem | head -10
echo "=== Network ===" && ss -tuln | head -20
echo "=== Docker/K8s ===" && docker ps 2>/dev/null || kubectl get pods -A 2>/dev/null
```

### Step 3: Match to Prompt

| Evidence | Prompt Combination | Why |
|----------|-------------------|-----|
| Stack trace, error logs | Agent System + Debugging & Troubleshooting | DEBUG protocol for root cause |
| High latency metrics | Agent System + Performance | MEASURE protocol for optimization |
| Suspicious activity logs | Agent System + Security Audit | OWASP-based assessment |
| Failed CI/CD pipeline | Agent System + Git & VCS | Branch, deploy troubleshooting |
| Broken tests | Agent System + Testing | Test strategy & fix |
| Messy codebase | Agent System + Refactoring | SAFE protocol for cleanup |
| Missing documentation | Agent System + Documentation | CLEAR protocol |
| Migration failure | Agent System + Migration | MIGRATE protocol with rollback |
| Container crashes | Agent System + Cloud & Infrastructure | CLOUD protocol |
| Data pipeline failure | Agent System + Data Engineering | PIPELINE protocol |
| Compliance violation | Agent System + Compliance | GOVERN protocol |
| API errors | Agent System + API Design | SCHEMA protocol |

### Step 4: Apply the APEI Cycle

```
For every issue, follow APEI:

ANALYZE
├── Reproduce the issue (or collect evidence if intermittent)
├── Identify scope and impact (how many users, which features)
├── Check what changed recently (commits, deploys, config)
└── Classify severity (P0-P3)

PLAN
├── Identify root cause (not just symptoms)
├── Design the fix (smallest change that solves the problem)
├── Plan verification (how to prove it's fixed)
└── Consider side effects (what else could break)

EXECUTE
├── Implement the fix
├── Add tests for the failure scenario
├── Verify the fix in a staging environment
└── Deploy with monitoring

ITERATE
├── Confirm fix in production
├── Monitor for regression
├── Write postmortem (P0/P1)
└── Update runbooks and documentation
```

## Common Issue Patterns

### Pattern 1: "It works locally but not in production"

```
Checklist:
- [ ] Environment variables match? (check .env vs production config)
- [ ] Database connection string correct? (localhost vs remote host)
- [ ] File paths absolute vs relative? (/app/ vs ./)
- [ ] Node/Python version match? (check Dockerfile)
- [ ] Missing dependencies? (devDependencies vs dependencies)
- [ ] Different OS? (case-sensitive file names, line endings)
- [ ] Network access? (firewall, security groups, CORS)
- [ ] Memory/CPU limits? (container constraints)
```

### Pattern 2: "It was working yesterday"

```
Checklist:
- [ ] Any recent deployments? (git log --since="yesterday")
- [ ] Configuration changes? (check config management, secrets)
- [ ] Infrastructure changes? (scaling, certificates, DNS)
- [ ] Dependency updates? (lock file changes)
- [ ] External service changes? (API deprecation, rate limits)
- [ ] Traffic pattern changes? (sudden spike, new region)
- [ ] Certificate/token expiry? (SSL, API keys, OAuth tokens)
- [ ] Database migration? (schema changes, data changes)
```

### Pattern 3: "Intermittent failures"

```
Checklist:
- [ ] Resource exhaustion? (connection pool, file handles, memory)
- [ ] Race conditions? (concurrent writes, shared state)
- [ ] Network timeouts? (DNS, load balancer, upstream)
- [ ] Scheduled tasks? (cron jobs conflicting with traffic)
- [ ] Auto-scaling lag? (cold starts, scaling thresholds)
- [ ] Cache invalidation? (stale data, TTL expiry)
- [ ] External dependency? (third-party API reliability)
- [ ] Time-based? (time zones, daylight saving, epoch issues)
```

## Escalation Matrix

| Severity | Response | Who | Communication |
|----------|----------|-----|---------------|
| **P0** | Immediate | On-call + Team Lead | Incident channel, status page |
| **P1** | < 1 hour | On-call engineer | Team notification |
| **P2** | < 4 hours | Assigned engineer | Ticket update |
| **P3** | Next sprint | Any team member | Backlog item |

## Prevention: Proactive Monitoring

| What to Monitor | Tool | Alert Threshold |
|-----------------|------|-----------------|
| Error rate | Sentry, Datadog | > 1% of requests |
| Response time (p95) | APM | > 2x baseline |
| CPU usage | CloudWatch/Prometheus | > 80% sustained |
| Memory usage | CloudWatch/Prometheus | > 85% |
| Disk usage | System monitoring | > 90% |
| SSL certificate expiry | Cert monitoring | < 30 days |
| Dependency vulnerabilities | Snyk, Dependabot | Any critical/high |
| Failed deployments | CI/CD | Any failure |
| Database connections | DB monitoring | > 80% pool |
| Queue depth | Queue monitoring | Growing > 5 min |

---

## Remember

The best debugging skill is **systematic elimination**:
1. **Reproduce** the issue reliably
2. **Isolate** the component (binary search)
3. **Understand** the root cause (not just the symptom)
4. **Fix** with the smallest change
5. **Verify** the fix solves the problem
6. **Prevent** recurrence with tests and monitoring
