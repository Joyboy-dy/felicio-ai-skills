---
name: nextjs-architecture-pattern
description: Scaffold, architect, and review production-grade Next.js 15 applications using a clean, opinionated layered architecture. Use for any new project setup, feature scaffolding, code review, or refactoring session. Covers three project profiles: full-stack (Next.js + Supabase/PostgreSQL), frontend-only (Next.js + external REST/GraphQL API), and hybrid BFF. Enforces strict separation of concerns: domain, use cases, ports, infrastructure, and UI. Always applies TypeScript, App Router conventions, Server Actions, co-located components, and DI container patterns.
---

# Next.js Architecture Pattern

An opinionated, production-grade architecture system for Next.js 15 applications. Built around clean architecture principles adapted for the App Router paradigm. Three profiles cover the full spectrum of real-world project structures.

---

## Project Profiles

| Profile | Stack | When to use |
|---|---|---|
| **A** | Next.js + Supabase / PostgreSQL | SaaS, dashboards, full-stack apps |
| **B** | Next.js + External REST/GraphQL API | Client-side apps consuming a backend you don't own |
| **C** | Next.js BFF + Supabase + External microservices | Hybrid platforms, aggregation layers |

---

## Core Laws (Non-Negotiable)

1. **Dependency flows inward** — `app/` depends on `core/`, never the reverse.
2. **`page.tsx` is a compositor** — zero logic, zero `"use client"`, pure assembly of server components.
3. **`_data/` fetchers call use cases, never infrastructure directly.**
4. **TypeScript everywhere** — every interface, every prop, every return type, every use case I/O.
5. **One use case = one file** — no god use cases, no shared mutation files.

---

## Layer Map

```
┌─────────────────────────────────────────────────┐
│            app/  (Next.js App Router)            │  UI Layer
│   page.tsx · layout.tsx · Server Actions        │
│   _components/  ·  _data/                       │
├─────────────────────────────────────────────────┤
│            core/  (framework-agnostic)           │  Domain + Use Cases
│   domain/  ·  use-cases/  ·  ports/             │
├─────────────────────────────────────────────────┤
│         infrastructure/  (adapters)              │  DB, APIs, services
│   repositories/  ·  services/  ·  di/           │
├─────────────────────────────────────────────────┤
│            lib/  (pure utilities)                │  Shared helpers, Zod, constants
└─────────────────────────────────────────────────┘
```

---

## Profile A — Full-Stack Next.js + Supabase

### Directory Structure

```
src/
├── app/
│   ├── layout.tsx                        # Root layout (providers, fonts, metadata)
│   ├── (auth)/
│   │   ├── login/
│   │   │   ├── page.tsx                  # Compositor only — no logic
│   │   │   ├── _components/              # LoginForm, OAuthButtons
│   │   │   └── _data/                    # Page metadata, static labels
│   │   └── register/
│   │       ├── page.tsx
│   │       ├── _components/
│   │       └── _data/
│   ├── (dashboard)/
│   │   ├── layout.tsx                    # Dashboard shell (Sidebar, Topbar)
│   │   ├── dashboard/
│   │   │   ├── page.tsx
│   │   │   ├── _components/
│   │   │   └── _data/
│   │   │       └── fetchers.ts           # Calls core/use-cases ONLY
│   │   └── [feature]/
│   │       ├── page.tsx
│   │       ├── [id]/
│   │       │   ├── page.tsx
│   │       │   ├── _components/
│   │       │   └── _data/
│   │       ├── _components/
│   │       └── _data/
│   │           └── fetchers.ts
│   ├── api/
│   │   ├── webhooks/
│   │   │   └── stripe/route.ts
│   │   └── auth/
│   │       └── callback/route.ts
│   └── actions/                          # Server Actions — thin controllers
│       ├── auth.actions.ts
│       └── [feature].actions.ts
│
├── components/
│   ├── ui/                               # Shadcn UI primitives
│   ├── layouts/                          # Navbar, Footer, Sidebar, Shells
│   └── my-components/                    # Custom composites (shared across routes)
│
├── core/
│   ├── domain/
│   │   ├── entities/                     # Pure TypeScript interfaces
│   │   ├── value-objects/                # Immutable domain primitives
│   │   └── errors/                       # Domain-specific error classes
│   ├── use-cases/
│   │   └── [feature]/
│   │       ├── create-[entity].use-case.ts
│   │       ├── list-[entity].use-case.ts
│   │       └── delete-[entity].use-case.ts
│   └── ports/                            # Abstract interfaces (contracts)
│       ├── [entity].repository.port.ts
│       └── [service].port.ts
│
├── infrastructure/
│   ├── database/
│   │   ├── supabase/
│   │   │   ├── client.ts                 # createServerClient / createBrowserClient
│   │   │   └── schema.types.ts           # Generated: supabase gen types typescript
│   │   └── repositories/
│   │       └── [entity].repository.ts    # implements [Entity]RepositoryPort
│   ├── services/
│   │   ├── stripe.service.ts
│   │   ├── resend.service.ts
│   │   └── [third-party].service.ts
│   └── di/
│       └── container.ts                  # Manual DI — singleton instances
│
├── lib/
│   ├── utils.ts                          # cn(), formatDate(), slugify()
│   ├── validations/
│   │   └── [feature].schema.ts           # Zod schemas + inferred types
│   └── constants/
│       └── routes.ts                     # APP_ROUTES typed map
│
├── hooks/                                # Client-side React hooks only
│   ├── use-debounce.ts
│   └── use-[feature].ts
│
├── types/
│   ├── api.types.ts                      # ApiResponse<T>, PaginatedResponse<T>
│   └── next.types.ts                     # PageProps, LayoutProps helpers
│
└── middleware.ts                         # Auth guards, redirects
```

### Data Flow

```
page.tsx
  └── _data/fetchers.ts
        └── core/use-cases/list-[entity].use-case.ts
              └── core/ports/[entity].repository.port.ts
                    └── infrastructure/repositories/[entity].repository.ts
                          └── infrastructure/database/supabase/client.ts
                                └── Supabase / PostgreSQL
```

---

## Profile B — Frontend + External API

Remove `core/` and `infrastructure/`. Replace with a `services/` layer.

### Directory Structure (delta)

```
src/
├── app/                                  # Same co-location rules as Profile A
│   └── [feature]/
│       ├── page.tsx
│       ├── _components/
│       └── _data/
│           └── fetchers.ts               # Calls services/ only
│
├── services/
│   ├── api.client.ts                     # Base fetch wrapper (auth headers, errors)
│   ├── [feature].service.ts              # CRUD methods via API client
│   └── auth.service.ts
│
├── hooks/
│   └── use-[feature].ts                  # TanStack Query hooks wrapping services/
│
└── types/
    ├── api.types.ts                      # ApiResponse<T> — mirrors backend DTOs
    └── domain.types.ts                   # Entity interfaces
```

### Data Flow

```
# Read (Server Component)
page.tsx → _data/fetchers.ts → services/[feature].service.ts → External API

# Write (Client Component)
_components/CreateForm.tsx ("use client")
  └── hooks/use-[feature].ts (TanStack Query mutation)
        └── services/[feature].service.ts
              └── External API
```

---

## Profile C — Hybrid BFF

Next.js acts as a Backend-For-Frontend: own data via `core/` + `infrastructure/`, external services via `services/`, orchestrated through Route Handlers.

```
src/app/api/
├── [external-service]/
│   └── [action]/route.ts     # Proxy + auth injection
├── analytics/
│   └── route.ts              # Aggregates from multiple sources
└── webhooks/
    └── [provider]/route.ts   # Stripe, Feexpay, Pawapay callbacks
```

---

## Implementation Patterns

### Entity

```typescript
// core/domain/entities/job.entity.ts
import type { Money } from '@/core/domain/value-objects/money.vo';

export interface Job {
  id: string;
  title: string;
  description: string;
  salary: Money;
  status: JobStatus;
  createdAt: Date;
  postedBy: string;
}

export type JobStatus = 'draft' | 'published' | 'closed';
```

### Value Object

```typescript
// core/domain/value-objects/money.vo.ts
type Currency = 'XOF' | 'EUR' | 'USD';

export class Money {
  private constructor(
    public readonly amount: number,
    public readonly currency: Currency
  ) {
    if (amount < 0) throw new Error('Amount cannot be negative');
  }

  static of(amount: number, currency: Currency): Money {
    return new Money(amount, currency);
  }

  format(): string {
    return `${this.amount.toLocaleString()} ${this.currency}`;
  }
}
```

### Repository Port

```typescript
// core/ports/job.repository.port.ts
import type { Job } from '@/core/domain/entities/job.entity';

export interface JobFilters {
  status?: Job['status'];
  postedBy?: string;
  limit?: number;
  offset?: number;
}

export interface JobRepositoryPort {
  findById(id: string): Promise<Job | null>;
  findAll(filters?: JobFilters): Promise<Job[]>;
  save(job: Omit<Job, 'id' | 'createdAt'>): Promise<Job>;
  update(id: string, data: Partial<Job>): Promise<Job>;
  delete(id: string): Promise<void>;
}
```

### Use Case

```typescript
// core/use-cases/jobs/create-job.use-case.ts
import type { JobRepositoryPort } from '@/core/ports/job.repository.port';
import type { Job } from '@/core/domain/entities/job.entity';
import { Money } from '@/core/domain/value-objects/money.vo';

interface CreateJobInput {
  title: string;
  description: string;
  salaryAmount: number;
  postedBy: string;
}

interface CreateJobOutput {
  job: Job | null;
  success: boolean;
  error?: string;
}

export class CreateJobUseCase {
  constructor(private readonly jobRepo: JobRepositoryPort) {}

  async execute(input: CreateJobInput): Promise<CreateJobOutput> {
    try {
      const salary = Money.of(input.salaryAmount, 'XOF');
      const job = await this.jobRepo.save({
        title: input.title,
        description: input.description,
        salary,
        status: 'draft',
        postedBy: input.postedBy,
      });
      return { job, success: true };
    } catch (err) {
      return { job: null, success: false, error: (err as Error).message };
    }
  }
}
```

### Repository Implementation (Supabase)

```typescript
// infrastructure/database/repositories/job.repository.ts
import type { JobRepositoryPort, JobFilters } from '@/core/ports/job.repository.port';
import type { Job } from '@/core/domain/entities/job.entity';
import { Money } from '@/core/domain/value-objects/money.vo';
import { createServerClient } from '@/infrastructure/database/supabase/client';

export class SupabaseJobRepository implements JobRepositoryPort {
  private supabase = createServerClient();

  async findById(id: string): Promise<Job | null> {
    const { data, error } = await this.supabase
      .from('jobs')
      .select('*')
      .eq('id', id)
      .single();

    if (error || !data) return null;
    return this.toEntity(data);
  }

  async findAll(filters?: JobFilters): Promise<Job[]> {
    let query = this.supabase.from('jobs').select('*');
    if (filters?.status) query = query.eq('status', filters.status);
    if (filters?.limit) query = query.limit(filters.limit);
    if (filters?.offset) query = query.range(filters.offset, filters.offset + (filters.limit ?? 10) - 1);

    const { data } = await query;
    return (data ?? []).map((row) => this.toEntity(row));
  }

  async save(job: Omit<Job, 'id' | 'createdAt'>): Promise<Job> {
    const { data, error } = await this.supabase
      .from('jobs')
      .insert({ ...job, salary: job.salary.amount })
      .select()
      .single();

    if (error) throw new Error(error.message);
    return this.toEntity(data);
  }

  async update(id: string, updates: Partial<Job>): Promise<Job> {
    const { data, error } = await this.supabase
      .from('jobs')
      .update(updates)
      .eq('id', id)
      .select()
      .single();

    if (error) throw new Error(error.message);
    return this.toEntity(data);
  }

  async delete(id: string): Promise<void> {
    await this.supabase.from('jobs').delete().eq('id', id);
  }

  private toEntity(row: Record<string, unknown>): Job {
    return {
      id: row.id as string,
      title: row.title as string,
      description: row.description as string,
      salary: Money.of(row.salary as number, 'XOF'),
      status: row.status as Job['status'],
      createdAt: new Date(row.created_at as string),
      postedBy: row.posted_by as string,
    };
  }
}
```

### DI Container

```typescript
// infrastructure/di/container.ts
// Instantiate once — import from here everywhere, never re-instantiate
import { SupabaseJobRepository } from '@/infrastructure/database/repositories/job.repository';
import { CreateJobUseCase } from '@/core/use-cases/jobs/create-job.use-case';
import { ListJobsUseCase } from '@/core/use-cases/jobs/list-jobs.use-case';
import { DeleteJobUseCase } from '@/core/use-cases/jobs/delete-job.use-case';

const jobRepository = new SupabaseJobRepository();

export const createJobUseCase = new CreateJobUseCase(jobRepository);
export const listJobsUseCase = new ListJobsUseCase(jobRepository);
export const deleteJobUseCase = new DeleteJobUseCase(jobRepository);
```

### Server Action

```typescript
// app/actions/job.actions.ts
'use server';
import { createJobUseCase } from '@/infrastructure/di/container';
import { createJobSchema } from '@/lib/validations/job.schema';
import { auth } from '@/lib/auth'; // replace with your auth helper
import { revalidatePath } from 'next/cache';

export async function createJobAction(_: unknown, formData: FormData) {
  const session = await auth();
  if (!session) return { success: false, error: 'Unauthorized' };

  const parsed = createJobSchema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) {
    return { success: false, errors: parsed.error.flatten().fieldErrors };
  }

  const result = await createJobUseCase.execute({
    ...parsed.data,
    postedBy: session.user.id,
  });

  if (!result.success) return { success: false, error: result.error };

  revalidatePath('/dashboard/jobs');
  return { success: true };
}
```

### Page Fetcher (`_data/fetchers.ts`)

```typescript
// app/(dashboard)/jobs/_data/fetchers.ts
import { listJobsUseCase } from '@/infrastructure/di/container';
import type { Job } from '@/core/domain/entities/job.entity';

export async function getPublishedJobs(): Promise<Job[]> {
  const result = await listJobsUseCase.execute({ status: 'published' });
  return result.jobs ?? [];
}
```

### Page Compositor (`page.tsx`)

```typescript
// app/(dashboard)/jobs/page.tsx
import type { Metadata } from 'next';
import { getPublishedJobs } from './_data/fetchers';
import { JobList } from './_components/JobList';
import { JobsHeader } from './_components/JobsHeader';

export const metadata: Metadata = {
  title: 'Jobs',
};

export default async function JobsPage() {
  const jobs = await getPublishedJobs();

  return (
    <>
      <JobsHeader />
      <JobList jobs={jobs} />
    </>
  );
}
```

### API Client (Profile B)

```typescript
// services/api.client.ts
import { getToken } from '@/lib/auth';

const BASE_URL = process.env.NEXT_PUBLIC_API_URL!;

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();

  const res = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ message: res.statusText }));
    throw new Error(error.message ?? 'API error');
  }

  return res.json() as Promise<T>;
}

export const apiClient = {
  get: <T>(url: string) => request<T>(url),
  post: <T>(url: string, body: unknown) =>
    request<T>(url, { method: 'POST', body: JSON.stringify(body) }),
  patch: <T>(url: string, body: unknown) =>
    request<T>(url, { method: 'PATCH', body: JSON.stringify(body) }),
  delete: <T>(url: string) => request<T>(url, { method: 'DELETE' }),
};
```

### Zod Validation Schema

```typescript
// lib/validations/job.schema.ts
import { z } from 'zod';

export const createJobSchema = z.object({
  title: z.string().min(3).max(100),
  description: z.string().min(20),
  salaryAmount: z.coerce.number().positive(),
});

export const updateJobSchema = createJobSchema.partial();

export type CreateJobDTO = z.infer<typeof createJobSchema>;
export type UpdateJobDTO = z.infer<typeof updateJobSchema>;
```

### Global Types

```typescript
// types/api.types.ts
export interface ApiResponse<T> {
  data: T | null;
  success: boolean;
  error?: string;
}

export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  total: number;
  page: number;
  limit: number;
}

// types/next.types.ts
export type PageProps<
  P extends Record<string, string> = Record<string, string>,
  S extends Record<string, string | string[] | undefined> = Record<string, string | string[] | undefined>
> = {
  params: Promise<P>;
  searchParams: Promise<S>;
};
```

### Middleware (Auth Guard)

```typescript
// middleware.ts
import { createServerClient } from '@supabase/ssr';
import { NextResponse, type NextRequest } from 'next/server';

const PROTECTED_ROUTES = ['/dashboard'];
const AUTH_ROUTES = ['/login', '/register'];

export async function middleware(request: NextRequest) {
  const response = NextResponse.next();

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll: () => request.cookies.getAll(),
        setAll: (cookiesToSet) => {
          cookiesToSet.forEach(({ name, value, options }) => {
            response.cookies.set(name, value, options);
          });
        },
      },
    }
  );

  const { data: { session } } = await supabase.auth.getSession();
  const { pathname } = request.nextUrl;

  const isProtected = PROTECTED_ROUTES.some((r) => pathname.startsWith(r));
  const isAuthRoute = AUTH_ROUTES.some((r) => pathname.startsWith(r));

  if (!session && isProtected) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  if (session && isAuthRoute) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  return response;
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico|api/webhooks).*)'],
};
```

---

## Architecture Decision Rules

### 5 Questions — Ask Before Creating Any File

1. Business logic? → `core/use-cases/` or `core/domain/`
2. DB access or external service call? → `infrastructure/`
3. UI mutation triggered by user? → `app/actions/`
4. Component used on one page only? → `app/[route]/_components/`
5. Component reused across routes? → `components/my-components/`

### Hard Rules

| ❌ Forbidden | ✅ Correct |
|---|---|
| `import { supabase } from '...'` inside `page.tsx` | Call `_data/fetchers.ts` |
| Business logic inside a Server Action | Delegate to a Use Case |
| `"use client"` on `page.tsx` | Extract interactive parts to `_components/` |
| Prisma/Supabase imported in `core/` | Port interface in `core/ports/`, implementation in `infrastructure/` |
| Direct fetch inside a React component (Profile A) | Route through `_data/fetchers.ts` |
| Hardcoded UI strings in components | Extract to `_data/` or a locale file |
| Re-instantiating repositories outside `container.ts` | Always import from `infrastructure/di/container.ts` |
| Redefining an entity type in `types/` when it exists in `core/domain/` | Import from the single source |

---

## Common Pitfalls

**Supabase directly in Server Actions** — Acceptable for simple throwaway CRUD. The moment the action grows to 3+ steps, extract a Use Case immediately.

**`_data/` that grows too large** — If a fetcher exceeds ~30 lines, it's a disguised Use Case. Move it.

**`container.ts` not used as the single source** — Instantiating repositories in multiple places breaks the singleton and creates inconsistent state.

**Over-engineering an MVP** — For projects under 3 weeks or prototypes, use a simplified Profile B: `services/` + `_data/` + `_components/`. Migrate to `core/` on demand when complexity requires it.

**Type duplication** — Never redefine an entity in `types/domain.types.ts` if it already exists in `core/domain/entities/`. Always import from the source of truth.

---

## Bootstrap Checklist

- [ ] Select profile (A, B, or C)
- [ ] Scaffold directory structure
- [ ] Configure `tsconfig.json` path aliases (`@/core`, `@/infrastructure`, `@/lib`, etc.)
- [ ] Generate Supabase types: `supabase gen types typescript --local > src/infrastructure/database/supabase/schema.types.ts`
- [ ] Create `lib/constants/routes.ts` with typed route map
- [ ] Create `types/api.types.ts` with `ApiResponse<T>` and `PaginatedResponse<T>`
- [ ] Wire `infrastructure/di/container.ts` with first repositories
- [ ] Set up `middleware.ts` with auth guards
- [ ] Add first Zod schemas in `lib/validations/`
- [ ] Verify no `"use client"` on any `page.tsx`

---

## References

- [Next.js App Router](https://nextjs.org/docs/app)
- [Supabase SSR with Next.js](https://supabase.com/docs/guides/auth/server-side/nextjs)
- [Shadcn UI](https://ui.shadcn.com)
- [Zod](https://zod.dev)
- [TanStack Query](https://tanstack.com/query) (Profile B mutations)
