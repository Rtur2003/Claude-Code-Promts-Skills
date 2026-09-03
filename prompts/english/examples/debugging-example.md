# Example: Debugging a Production Bug

## Scenario

Your production application is experiencing intermittent 500 errors on the `/api/orders` endpoint. Users are complaining that sometimes their orders fail to process.

## Prompts Used

1. **Agent System Prompt** — APEI workflow
2. **Debugging & Troubleshooting Prompt** — DEBUG protocol for root-cause diagnosis

---

## Step 1: FIND (Detect the Error)

### Error Report
```markdown
**Type**: Runtime
**Priority**: P1 (High - main feature broken)
**Status**: Investigating

### Error Message
```
Error: Connection timeout after 30000ms
    at PostgresClient.connect (/app/node_modules/pg/lib/client.js:123:11)
    at Pool._acquireClient (/app/node_modules/pg/lib/pool.js:198:7)
    at OrderService.getOrders (/app/src/services/orderService.js:45:23)
```

### Location
- **File**: src/services/orderService.js
- **Line**: 45
- **Function**: getOrders

### Reproduction Steps
1. Make 10+ concurrent requests to /api/orders
2. Error appears randomly after ~30 seconds
3. Happens more frequently during peak hours

### Environment
- Node.js 18.17.0
- PostgreSQL 15.2
- pg@8.11.0 (database driver)
```

---

## Step 2: UNDERSTAND (Root Cause Analysis)

### 5 Whys Analysis
```markdown
**Problem**: API returns 500 error with connection timeout

1. **Why?** → Database query timing out
2. **Why?** → No available connections in pool
3. **Why?** → All 10 connections are in use
4. **Why?** → Connections not being released after queries
5. **Why?** → Error handler doesn't release connection on exception

**Root Cause**: Missing connection release in error handling path
```

### Code Investigation
```javascript
// Found in src/services/orderService.js
async getOrders(userId) {
    const client = await pool.connect();  // Line 45
    
    const result = await client.query(
        'SELECT * FROM orders WHERE user_id = $1',
        [userId]
    );
    
    client.release();  // Only releases on success!
    return result.rows;
    
    // If query throws, connection is never released!
}
```

### Confirmation
```bash
# Check active connections
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';
# Result: 10 (max pool size)

# Check waiting queries
SELECT count(*) FROM pg_stat_activity WHERE wait_event_type = 'Client';
# Result: 15 (queries waiting for connection)
```

---

## Step 3: LIST (Evaluate Solutions)

### Solution Options

#### Option A: Try-Finally Block
```javascript
async getOrders(userId) {
    const client = await pool.connect();
    try {
        const result = await client.query(
            'SELECT * FROM orders WHERE user_id = $1',
            [userId]
        );
        return result.rows;
    } finally {
        client.release();  // Always releases, even on error
    }
}
```
**Pros**: Simple, guarantees release
**Cons**: Requires refactoring each function
**Risk**: Low
**Effort**: 2 hours

#### Option B: Use pool.query() Directly
```javascript
async getOrders(userId) {
    const result = await pool.query(
        'SELECT * FROM orders WHERE user_id = $1',
        [userId]
    );
    return result.rows;
}
```
**Pros**: Pool handles connection automatically, simplest code
**Cons**: Can't use transactions easily
**Risk**: Low
**Effort**: 1 hour

#### Option C: Connection Wrapper Utility
```javascript
async function withConnection(fn) {
    const client = await pool.connect();
    try {
        return await fn(client);
    } finally {
        client.release();
    }
}

// Usage
async getOrders(userId) {
    return withConnection(async (client) => {
        const result = await client.query(
            'SELECT * FROM orders WHERE user_id = $1',
            [userId]
        );
        return result.rows;
    });
}
```
**Pros**: Reusable, supports transactions
**Cons**: More complex pattern
**Risk**: Low
**Effort**: 3 hours

### Selected Solution: Option C
**Rationale**: Best balance of safety and flexibility. Can reuse for all database operations and supports transactions.

---

## Step 4: ACT (Apply Fix)

### Implementation

#### Step 4.1: Create Utility
```javascript
// src/utils/database.js
const pool = require('../config/database');

/**
 * Execute a function with a managed database connection.
 * Ensures connection is always released, even on error.
 */
async function withConnection(fn) {
    const client = await pool.connect();
    try {
        return await fn(client);
    } finally {
        client.release();
    }
}

/**
 * Execute a function within a database transaction.
 * Automatically commits on success, rolls back on error.
 */
async function withTransaction(fn) {
    return withConnection(async (client) => {
        await client.query('BEGIN');
        try {
            const result = await fn(client);
            await client.query('COMMIT');
            return result;
        } catch (error) {
            await client.query('ROLLBACK');
            throw error;
        }
    });
}

module.exports = { withConnection, withTransaction };
```

#### Step 4.2: Refactor Service
```javascript
// src/services/orderService.js
const { withConnection, withTransaction } = require('../utils/database');

class OrderService {
    async getOrders(userId) {
        return withConnection(async (client) => {
            const result = await client.query(
                'SELECT * FROM orders WHERE user_id = $1 ORDER BY created_at DESC',
                [userId]
            );
            return result.rows;
        });
    }
    
    async createOrder(userId, items) {
        return withTransaction(async (client) => {
            // Create order
            const orderResult = await client.query(
                'INSERT INTO orders (user_id, status) VALUES ($1, $2) RETURNING id',
                [userId, 'pending']
            );
            const orderId = orderResult.rows[0].id;
            
            // Add items
            for (const item of items) {
                await client.query(
                    'INSERT INTO order_items (order_id, product_id, quantity) VALUES ($1, $2, $3)',
                    [orderId, item.productId, item.quantity]
                );
            }
            
            return { orderId };
        });
    }
}

module.exports = new OrderService();
```

#### Step 4.3: Add Tests
```javascript
// tests/services/orderService.test.js
const { withConnection } = require('../../src/utils/database');

describe('Database Connection Management', () => {
    it('should release connection on success', async () => {
        const poolSpy = jest.spyOn(pool, 'connect');
        const releaseSpy = jest.fn();
        poolSpy.mockResolvedValue({ 
            query: jest.fn().mockResolvedValue({ rows: [] }),
            release: releaseSpy
        });
        
        await withConnection(async (client) => {
            await client.query('SELECT 1');
        });
        
        expect(releaseSpy).toHaveBeenCalled();
    });
    
    it('should release connection on error', async () => {
        const poolSpy = jest.spyOn(pool, 'connect');
        const releaseSpy = jest.fn();
        poolSpy.mockResolvedValue({ 
            query: jest.fn().mockRejectedValue(new Error('Query failed')),
            release: releaseSpy
        });
        
        await expect(withConnection(async (client) => {
            await client.query('SELECT 1');
        })).rejects.toThrow('Query failed');
        
        expect(releaseSpy).toHaveBeenCalled();  // Still released!
    });
});
```

---

## Step 5: VERIFY (Report)

### Verification Steps

```bash
# 1. Run unit tests
npm test -- --grep "Database Connection"
# ✓ should release connection on success
# ✓ should release connection on error

# 2. Run integration tests
npm run test:integration
# ✓ All 45 tests passing

# 3. Load test
npx autocannon -c 100 -d 60 http://localhost:3000/api/orders
# Result: 0 errors, avg response time 45ms

# 4. Check connection pool
SELECT count(*) FROM pg_stat_activity WHERE state = 'idle';
# Result: 8 (connections being released properly)
```

### Fix Report
```markdown
## Fix Report

### Bug
Intermittent 500 errors on /api/orders due to connection pool exhaustion

### Root Cause
Database connections were not being released when queries threw errors,
causing the connection pool to eventually fill up and new queries to timeout.

### Solution
Created `withConnection` and `withTransaction` utilities that use try-finally
to guarantee connection release. Refactored all database operations to use
these utilities.

### Files Changed
- src/utils/database.js (new)
- src/services/orderService.js
- src/services/userService.js
- src/services/productService.js
- tests/services/*.test.js

### Verification
- Unit tests: ✓ All passing
- Integration tests: ✓ All passing
- Load test: ✓ 0 errors under 100 concurrent connections
- Production monitoring: ✓ No connection timeouts in 24 hours

### Prevention
- [x] Added unit tests for connection release
- [x] Added integration tests for error scenarios
- [x] Added connection pool monitoring alert
- [x] Updated developer documentation
- [x] Added linting rule to flag direct pool.connect() calls
```

### Commit
```
fix(database): ensure connections are released on error

Connection pool was being exhausted when queries threw errors
because connections weren't being released in error handlers.

Created withConnection and withTransaction utilities that
guarantee connection release using try-finally pattern.

- Add database utilities (src/utils/database.js)
- Refactor all services to use utilities
- Add unit and integration tests
- Add connection pool monitoring

Fixes #567
```

---

## Key Learnings

1. **Always use try-finally for resources**: Connections, file handles, locks
2. **Monitor your connection pools**: Alert on high usage
3. **Load test error scenarios**: Not just happy paths
4. **Create reusable utilities**: Don't repeat error-prone patterns

## Related Prompts

- [Debugging & Troubleshooting Prompt](../agents/debugging-troubleshooting-prompt.md)
- [Performance Optimization Prompt](../agents/performance-optimization-prompt.md)
- [Database Design Prompt](../project-types/database-sql-prompt.md)
