# Example: Building a Full-Stack Application

## Scenario

You need to build a full-stack todo application with user authentication using Next.js, tRPC, and Prisma. The app should support:
- User registration and login
- Creating, reading, updating, and deleting todos
- Client-side form validation
- Responsive design with loading states

## Prompts Used

1. **Foundation Prompt** - Core development principles
2. **Web Development Prompt** - Frontend best practices
3. **API Development Prompt** - Type-safe API layer

---

## Iteration 1: Project Scaffolding & Data Layer

### Step 1: ANALYZE

```markdown
## Analysis Summary

**Problem**: Build a full-stack todo app with authentication
**Stack**: Next.js 16 (App Router), tRPC v11, Prisma 7, PostgreSQL 18, Auth.js
**Key Files**:
- prisma/schema.prisma
- src/server/routers/todo.ts
- src/server/routers/auth.ts
- src/app/(auth)/login/page.tsx
- src/app/dashboard/page.tsx
**Risks**:
- Unauthorized access to other users' todos
- Missing input sanitization on todo content
- Session token exposure in client-side code
**Success Criteria**:
- Full CRUD for todos scoped to authenticated user
- Working auth flow with session management
- Responsive UI with optimistic updates
```

### Step 2: PLAN

```markdown
#### Iteration 1: Foundation
- [ ] Initialize Next.js project with TypeScript
- [ ] Configure Prisma with PostgreSQL
- [ ] Define User and Todo models
- [ ] Set up tRPC with Next.js App Router

#### Iteration 2: Frontend
- [ ] Build todo list and form components
- [ ] Add client-side validation with Zod
- [ ] Implement optimistic updates

#### Iteration 3: Authentication
- [ ] Integrate NextAuth.js with credentials provider
- [ ] Add auth middleware to tRPC procedures
- [ ] Protect routes with Next.js middleware

#### Iteration 4: Polish
- [ ] Add error boundaries and loading states
- [ ] Implement responsive design
- [ ] Add toast notifications
```

### Step 3: EXECUTE

#### Database Schema

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  password  String
  name      String
  todos     Todo[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Todo {
  id        String   @id @default(cuid())
  title     String
  completed Boolean  @default(false)
  userId    String
  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([userId])
}
```

#### tRPC Setup

```typescript
// src/server/trpc.ts
import { initTRPC, TRPCError } from '@trpc/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';

const t = initTRPC.context<{ prisma: typeof prisma }>().create();

export const router = t.router;
export const publicProcedure = t.procedure;

export const protectedProcedure = t.procedure.use(async ({ next }) => {
    const session = await getServerSession(authOptions);

    if (!session?.user) {
        throw new TRPCError({ code: 'UNAUTHORIZED' });
    }

    return next({
        ctx: { userId: session.user.id },
    });
});
```

#### Todo Router

```typescript
// src/server/routers/todo.ts
import { z } from 'zod';
import { router, protectedProcedure } from '../trpc';

const todoInput = z.object({
    title: z.string().min(1, 'Title is required').max(200),
});

export const todoRouter = router({
    list: protectedProcedure.query(async ({ ctx }) => {
        return ctx.prisma.todo.findMany({
            where: { userId: ctx.userId },
            orderBy: { createdAt: 'desc' },
        });
    }),

    create: protectedProcedure
        .input(todoInput)
        .mutation(async ({ ctx, input }) => {
            return ctx.prisma.todo.create({
                data: { title: input.title, userId: ctx.userId },
            });
        }),

    toggle: protectedProcedure
        .input(z.object({ id: z.string() }))
        .mutation(async ({ ctx, input }) => {
            const todo = await ctx.prisma.todo.findUnique({
                where: { id: input.id },
            });

            if (!todo || todo.userId !== ctx.userId) {
                throw new TRPCError({ code: 'NOT_FOUND' });
            }

            return ctx.prisma.todo.update({
                where: { id: input.id },
                data: { completed: !todo.completed },
            });
        }),

    delete: protectedProcedure
        .input(z.object({ id: z.string() }))
        .mutation(async ({ ctx, input }) => {
            const todo = await ctx.prisma.todo.findUnique({
                where: { id: input.id },
            });

            if (!todo || todo.userId !== ctx.userId) {
                throw new TRPCError({ code: 'NOT_FOUND' });
            }

            return ctx.prisma.todo.delete({ where: { id: input.id } });
        }),
});
```

### Step 4: ITERATE

```markdown
✓ Prisma schema validates and migrates
✓ tRPC router type-checks correctly
⚠ Need to scope all queries by userId → Fixed with ownership check
```

---

## Iteration 2: Frontend Components

### Step 1: ANALYZE
```markdown
**Focus**: Build React components for todo CRUD
**Dependencies**: tRPC client, React Hook Form, Zod
**Key Concern**: Optimistic updates for responsive UX
```

### Step 2: PLAN
```markdown
- [ ] TodoForm component with validation
- [ ] TodoList component with toggle and delete
- [ ] Optimistic update hooks
```

### Step 3: EXECUTE

#### Todo Form

```tsx
// src/components/TodoForm.tsx
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { trpc } from '@/lib/trpc';

const schema = z.object({
    title: z.string().min(1, 'Title is required').max(200),
});

type FormData = z.infer<typeof schema>;

export function TodoForm() {
    const utils = trpc.useUtils();
    const { register, handleSubmit, reset, formState: { errors } } = useForm<FormData>({
        resolver: zodResolver(schema),
    });

    const createTodo = trpc.todo.create.useMutation({
        onSuccess: () => {
            utils.todo.list.invalidate();
            reset();
        },
    });

    const onSubmit = (data: FormData) => {
        createTodo.mutate(data);
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="flex gap-2">
            <input
                {...register('title')}
                placeholder="What needs to be done?"
                className="flex-1 rounded-lg border px-4 py-2"
                disabled={createTodo.isPending}
            />
            <button
                type="submit"
                disabled={createTodo.isPending}
                className="rounded-lg bg-blue-600 px-4 py-2 text-white"
            >
                {createTodo.isPending ? 'Adding...' : 'Add'}
            </button>
            {errors.title && (
                <p className="text-sm text-red-500">{errors.title.message}</p>
            )}
        </form>
    );
}
```

#### Todo List with Optimistic Updates

```tsx
// src/components/TodoList.tsx
'use client';

import { trpc } from '@/lib/trpc';

export function TodoList() {
    const utils = trpc.useUtils();
    const { data: todos, isLoading } = trpc.todo.list.useQuery();

    const toggleTodo = trpc.todo.toggle.useMutation({
        onMutate: async ({ id }) => {
            await utils.todo.list.cancel();
            const previous = utils.todo.list.getData();

            utils.todo.list.setData(undefined, (old) =>
                old?.map((t) => (t.id === id ? { ...t, completed: !t.completed } : t))
            );

            return { previous };
        },
        onError: (_err, _vars, context) => {
            utils.todo.list.setData(undefined, context?.previous);
        },
        onSettled: () => utils.todo.list.invalidate(),
    });

    const deleteTodo = trpc.todo.delete.useMutation({
        onSuccess: () => utils.todo.list.invalidate(),
    });

    if (isLoading) {
        return <div className="animate-pulse space-y-2">
            {[...Array(3)].map((_, i) => (
                <div key={i} className="h-12 rounded-lg bg-gray-200" />
            ))}
        </div>;
    }

    if (!todos?.length) {
        return <p className="text-center text-gray-500">No todos yet. Add one above!</p>;
    }

    return (
        <ul className="space-y-2">
            {todos.map((todo) => (
                <li key={todo.id} className="flex items-center gap-3 rounded-lg border p-3">
                    <input
                        type="checkbox"
                        checked={todo.completed}
                        onChange={() => toggleTodo.mutate({ id: todo.id })}
                        className="h-5 w-5"
                    />
                    <span className={todo.completed ? 'flex-1 line-through text-gray-400' : 'flex-1'}>
                        {todo.title}
                    </span>
                    <button
                        onClick={() => deleteTodo.mutate({ id: todo.id })}
                        className="text-red-500 hover:text-red-700"
                    >
                        Delete
                    </button>
                </li>
            ))}
        </ul>
    );
}
```

### Step 4: ITERATE
```markdown
✓ Form validation working with Zod + React Hook Form
✓ Optimistic updates provide instant feedback
✓ Loading skeleton prevents layout shift
⚠ Delete has no confirmation → Added confirm dialog
```

---

## Iteration 3: Authentication

### Step 1: ANALYZE
```markdown
**Focus**: Integrate NextAuth.js with credentials provider
**Risk**: Session hijacking, CSRF attacks, password storage
**Key Decisions**: Use bcrypt for passwords, JWT for sessions
```

### Step 3: EXECUTE

#### NextAuth Configuration

```typescript
// src/lib/auth.ts
import { type NextAuthOptions } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import bcrypt from 'bcrypt';
import { prisma } from './prisma';

export const authOptions: NextAuthOptions = {
    providers: [
        CredentialsProvider({
            name: 'credentials',
            credentials: {
                email: { label: 'Email', type: 'email' },
                password: { label: 'Password', type: 'password' },
            },
            async authorize(credentials) {
                if (!credentials?.email || !credentials?.password) {
                    return null;
                }

                const user = await prisma.user.findUnique({
                    where: { email: credentials.email },
                });

                if (!user) return null;

                const isValid = await bcrypt.compare(credentials.password, user.password);
                if (!isValid) return null;

                return { id: user.id, email: user.email, name: user.name };
            },
        }),
    ],
    callbacks: {
        async jwt({ token, user }) {
            if (user) token.id = user.id;
            return token;
        },
        async session({ session, token }) {
            if (session.user) session.user.id = token.id as string;
            return session;
        },
    },
    pages: {
        signIn: '/login',
    },
    session: { strategy: 'jwt' },
};
```

#### Route Protection Middleware

```typescript
// src/middleware.ts
export { default } from 'next-auth/middleware';

export const config = {
    matcher: ['/dashboard/:path*', '/api/trpc/:path*'],
};
```

### Step 4: ITERATE
```markdown
✓ Login/register flow working end-to-end
✓ Protected routes redirect to login
✓ tRPC procedures reject unauthenticated requests
⚠ Missing rate limiting on login → Added next-rate-limit
```

---

## Iteration 4: Polish

### Step 3: EXECUTE

#### Error Boundary

```tsx
// src/components/ErrorBoundary.tsx
'use client';

import { Component, type ReactNode } from 'react';

interface Props {
    children: ReactNode;
    fallback?: ReactNode;
}

interface State {
    hasError: boolean;
}

export class ErrorBoundary extends Component<Props, State> {
    state: State = { hasError: false };

    static getDerivedStateFromError(): State {
        return { hasError: true };
    }

    render() {
        if (this.state.hasError) {
            return this.props.fallback ?? (
                <div className="rounded-lg border border-red-200 bg-red-50 p-4">
                    <h2 className="font-semibold text-red-800">Something went wrong</h2>
                    <button
                        onClick={() => this.setState({ hasError: false })}
                        className="mt-2 text-red-600 underline"
                    >
                        Try again
                    </button>
                </div>
            );
        }

        return this.props.children;
    }
}
```

### Step 4: ITERATE

```bash
npm run build && npm run test
```

### Results
```
✓ Build completed successfully (4.2s)
✓ 38 tests passing
✓ Lighthouse: Performance 96, Accessibility 100
✓ All CRUD operations working with auth
```

### Final Commit
```
feat(app): implement full-stack todo application

Complete Next.js todo app with:
- tRPC API with type-safe procedures
- Prisma ORM with PostgreSQL
- NextAuth.js credentials authentication
- React Hook Form with Zod validation
- Optimistic updates for responsive UX
- Error boundaries and loading states
- Responsive Tailwind CSS design

Closes #12
```

---

## Key Learnings

1. **Type safety end-to-end** - tRPC + Zod eliminates API contract mismatches
2. **Scope all queries by user** - Ownership checks prevent IDOR vulnerabilities
3. **Optimistic updates matter** - Users perceive the app as significantly faster
4. **Iterate in layers** - Data → UI → Auth → Polish keeps each iteration focused

## Related Prompts Used

- [Web Development Prompt](../project-types/web-development-prompt.md)
- [API Development Prompt](../project-types/api-development-prompt.md)
- [Agent System Prompt](../agents/claude-agent-system-prompt.md)
