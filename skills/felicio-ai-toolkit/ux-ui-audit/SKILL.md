---
name: ux-ui-audit
description: Act as a Lead UX/UI Designer to audit code and interfaces. Use when asked to review, polish, or improve a component, page, or full interface. Covers all UX edge cases: loading states, error handling, form validation feedback, empty states, optimistic updates, destructive action confirmation, skeleton screens, accessibility (ARIA, keyboard nav, focus management, color contrast), and native user experience patterns. Produces concrete, ready-to-implement code fixes — not just recommendations. Works with React, Next.js, Tailwind CSS, and TypeScript by default.
---

# UX/UI Audit Skill

Act as a Lead UX/UI Designer with strong engineering skills. When given a component, page, or codebase to review, perform a structured audit and return **concrete code fixes**, not abstract recommendations. Every issue raised must be accompanied by a corrected implementation.

---

## Audit Mindset

Before touching any code, read the interface through three lenses:

1. **User lens** — What is the user trying to accomplish? Where can they get stuck, confused, or lose trust?
2. **Edge case lens** — What happens when things go wrong, take time, or produce no result?
3. **Craft lens** — Does this feel native, intentional, and polished? Or does it feel like an unfinished prototype?

---

## Audit Checklist

Work through every category below. Flag each issue with a severity level, then fix it.

**Severity scale:**
- `[critical]` — Breaks the experience or blocks the user
- `[major]` — Degrades trust or causes frustration
- `[minor]` — Rough edge, suboptimal but functional
- `[polish]` — Fine-tuning that elevates quality

---

### 1. Loading States

Every async operation must have a visual representation of progress. Audit for:

- [ ] **Initial page/component load** — Skeleton screen or shimmer, not a blank flash or a spinner blocking the full viewport
- [ ] **Action loading** (form submit, button click, mutation) — Button enters disabled + loading state immediately on click, with a spinner or label change (`"Saving..."`, `"Deleting..."`)
- [ ] **Pagination / infinite scroll** — Skeleton rows appended below, not a full-page reload indicator
- [ ] **Slow network resilience** — If a request exceeds ~3s, surface a non-intrusive status (`"Still loading..."`)
- [ ] **No layout shift** — Loading placeholders must match the dimensions of the content they replace

```tsx
// ✅ Button loading state pattern
interface LoadingButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  loading?: boolean;
  children: React.ReactNode;
}

export function LoadingButton({ loading, disabled, children, ...props }: LoadingButtonProps) {
  return (
    <button
      {...props}
      disabled={disabled || loading}
      aria-busy={loading}
      className={cn(
        'relative inline-flex items-center gap-2 transition-opacity',
        loading && 'cursor-not-allowed opacity-70',
        props.className
      )}
    >
      {loading && (
        <svg
          className="h-4 w-4 animate-spin"
          viewBox="0 0 24 24"
          fill="none"
          aria-hidden="true"
        >
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4l3-3-3-3v4a8 8 0 00-8 8h4z" />
        </svg>
      )}
      {children}
    </button>
  );
}

// ✅ Skeleton pattern
export function CardSkeleton() {
  return (
    <div className="animate-pulse rounded-lg border bg-muted p-4 space-y-3" aria-hidden="true">
      <div className="h-4 w-2/3 rounded bg-muted-foreground/20" />
      <div className="h-3 w-full rounded bg-muted-foreground/10" />
      <div className="h-3 w-4/5 rounded bg-muted-foreground/10" />
    </div>
  );
}
```

---

### 2. Error States

Never let an error fail silently or render a raw stack trace. Audit for:

- [ ] **Network / server errors** — Inline error message with a retry action, not just a toast that disappears
- [ ] **404 / empty query results** — Dedicated empty state UI (see §4)
- [ ] **Partial failures** — If one item in a list fails to load, show a per-item error, not a full-page crash
- [ ] **Error boundaries** — Wrap every major section in a React Error Boundary with a fallback UI
- [ ] **Toast vs. inline** — Use toasts for background operations (file upload, sync). Use inline errors for user-initiated foreground actions (form submit, delete)

```tsx
// ✅ Error boundary with fallback
'use client';
import { Component, type ReactNode } from 'react';

interface Props {
  fallback?: ReactNode;
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? (
        <div role="alert" className="flex flex-col items-center gap-3 rounded-lg border border-destructive/30 bg-destructive/5 p-6 text-center">
          <p className="text-sm font-medium text-destructive">Something went wrong.</p>
          <button
            className="text-xs underline underline-offset-2"
            onClick={() => this.setState({ hasError: false })}
          >
            Try again
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

// ✅ Inline async error
interface AsyncErrorProps {
  message: string;
  onRetry?: () => void;
}

export function AsyncError({ message, onRetry }: AsyncErrorProps) {
  return (
    <div role="alert" className="flex items-center justify-between gap-2 rounded-md border border-destructive/30 bg-destructive/5 px-3 py-2 text-sm text-destructive">
      <span>{message}</span>
      {onRetry && (
        <button onClick={onRetry} className="shrink-0 font-medium underline underline-offset-2">
          Retry
        </button>
      )}
    </div>
  );
}
```

---

### 3. Form Validation & Input Errors

Forms are where most UX failures concentrate. Audit for:

- [ ] **Inline field-level errors** — Error message directly below the input, not a banner at the top of the form
- [ ] **Error timing** — Validate on blur for format errors (email, phone). Validate on submit for required fields. Never validate on every keystroke
- [ ] **Error message quality** — Specific and actionable (`"Email must include an @ symbol"`) not generic (`"Invalid input"`)
- [ ] **Input state styling** — Error: red border + error text. Focus: visible ring (never removed)
- [ ] **Disabled submit** — Never disable the submit button before submission. Disable it only while a request is in flight
- [ ] **Label association** — Every input has a `<label>` with matching `htmlFor` / `id`. No placeholder-only labels
- [ ] **Autocomplete attributes** — Name, email, phone, address fields carry correct `autoComplete` values
- [ ] **Password fields** — Always include a show/hide toggle

```tsx
// ✅ Field with proper error handling
interface FieldProps {
  id: string;
  label: string;
  error?: string;
  required?: boolean;
  hint?: string;
}

export function Field({
  id,
  label,
  error,
  required,
  hint,
  ...inputProps
}: FieldProps & React.InputHTMLAttributes<HTMLInputElement>) {
  const errorId = `${id}-error`;
  const hintId = `${id}-hint`;

  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor={id} className="text-sm font-medium leading-none">
        {label}
        {required && <span aria-hidden="true" className="ml-1 text-destructive">*</span>}
      </label>
      {hint && (
        <p id={hintId} className="text-xs text-muted-foreground">{hint}</p>
      )}
      <input
        id={id}
        aria-describedby={[hint ? hintId : '', error ? errorId : ''].filter(Boolean).join(' ') || undefined}
        aria-invalid={!!error}
        aria-required={required}
        className={cn(
          'rounded-md border bg-background px-3 py-2 text-sm outline-none transition-colors',
          'focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-1',
          error ? 'border-destructive focus-visible:ring-destructive/50' : 'border-input'
        )}
        {...inputProps}
      />
      {error && (
        <p id={errorId} role="alert" className="flex items-center gap-1 text-xs text-destructive">
          <span aria-hidden="true">↑</span>
          {error}
        </p>
      )}
    </div>
  );
}
```

---

### 4. Empty States

An empty state is a UX opportunity, not an afterthought. Audit for:

- [ ] **No raw empty arrays** — A list that renders nothing when `data.length === 0` is a broken experience
- [ ] **Contextual messaging** — Explain why it's empty and what the user can do next
- [ ] **Primary action** — Most empty states should include a CTA that resolves the emptiness
- [ ] **Illustration or icon** — Visual anchor helps users understand the context at a glance

```tsx
interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
}

export function EmptyState({ icon, title, description, action }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 rounded-lg border border-dashed bg-muted/30 px-6 py-12 text-center">
      {icon && <div className="text-muted-foreground/50" aria-hidden="true">{icon}</div>}
      <div className="space-y-1">
        <p className="text-sm font-medium">{title}</p>
        {description && (
          <p className="text-xs text-muted-foreground max-w-xs">{description}</p>
        )}
      </div>
      {action && (
        <button
          onClick={action.onClick}
          className="mt-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90"
        >
          {action.label}
        </button>
      )}
    </div>
  );
}
```

---

### 5. Destructive Actions

Every irreversible action must be confirmed. Audit for:

- [ ] **Confirmation dialog** — Delete, revoke, cancel subscription, leave team: always confirm
- [ ] **Double-friction for critical data** — For permanent data loss, require typing a resource name or "DELETE"
- [ ] **Destructive button placement** — Never place destructive actions next to primary actions
- [ ] **Optimistic delete with undo** — For soft-deletable items, prefer optimistic removal + toast with undo over a blocking modal

```tsx
// ✅ Confirmation dialog pattern
interface ConfirmDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  description: string;
  confirmLabel?: string;
  onConfirm: () => void | Promise<void>;
  loading?: boolean;
}

export function ConfirmDialog({
  open,
  onOpenChange,
  title,
  description,
  confirmLabel = 'Delete',
  onConfirm,
  loading,
}: ConfirmDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription>{description}</DialogDescription>
        </DialogHeader>
        <DialogFooter className="gap-2 sm:gap-0">
          <button
            onClick={() => onOpenChange(false)}
            className="rounded-md border px-4 py-2 text-sm"
          >
            Cancel
          </button>
          <LoadingButton
            loading={loading}
            onClick={onConfirm}
            className="rounded-md bg-destructive px-4 py-2 text-sm font-medium text-destructive-foreground"
          >
            {confirmLabel}
          </LoadingButton>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

// ✅ Optimistic delete + undo toast
async function handleDelete(id: string, deletedItem: unknown) {
  // 1. Remove from UI immediately
  setItems((prev) => prev.filter((item) => item.id !== id));

  let undone = false;

  // 2. Show undo window (5s)
  toast('Item deleted', {
    action: {
      label: 'Undo',
      onClick: () => {
        undone = true;
        setItems((prev) => [...prev, deletedItem]);
      },
    },
    duration: 5000,
  });

  // 3. Commit after undo window closes
  await new Promise((res) => setTimeout(res, 5200));
  if (!undone) await deleteItemAction(id);
}
```

---

### 6. Accessibility (a11y)

Audit for WCAG 2.1 AA compliance as a baseline. Never treat accessibility as optional.

- [ ] **Color contrast** — Text: 4.5:1 minimum. Large text / UI components: 3:1 minimum
- [ ] **Focus management** — Every interactive element is keyboard-reachable. Focus rings are never removed without a custom replacement. When a modal opens, focus moves to it. When it closes, focus returns to the trigger
- [ ] **ARIA roles and labels** — Icon-only buttons have `aria-label`. Dynamic regions use `aria-live`. Loaders use `aria-busy`. Errors use `role="alert"`
- [ ] **Keyboard navigation** — Modals trap focus. Dropdowns close on Escape. Lists support arrow key navigation where expected
- [ ] **Screen reader flow** — Logical heading hierarchy (`h1` → `h2` → `h3`). Decorative images have `alt=""`. Informative images have descriptive alt text
- [ ] **Reduced motion** — Animations respect `prefers-reduced-motion`
- [ ] **Touch targets** — Minimum 44×44px tap target on mobile

```tsx
// ✅ Icon button with proper label
<button
  aria-label="Delete item"
  className="rounded p-2 hover:bg-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
>
  <TrashIcon className="h-4 w-4" aria-hidden="true" />
</button>

// ✅ Live region for async status messages
<div aria-live="polite" aria-atomic="true" className="sr-only">
  {statusMessage}
</div>

// ✅ Reduced motion — global CSS
/*
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
*/

// ✅ Focus trap in modal (Radix Dialog handles this automatically)
// ✅ Return focus to trigger on modal close
const triggerRef = useRef<HTMLButtonElement>(null);

<DialogClose
  onCloseAutoFocus={(e) => {
    e.preventDefault();
    triggerRef.current?.focus();
  }}
/>
```

---

### 7. Native User Experience Patterns

Make the interface feel like it belongs on the platform. Audit for:

- [ ] **Optimistic updates** — Mutations update the UI before the server responds. Roll back on error
- [ ] **Debounced search** — Search inputs debounce at 300ms minimum before firing requests
- [ ] **Persistent state** — Filters, sort order, and pagination survive soft navigation via URL search params
- [ ] **Scroll restoration** — After navigation, scroll position is restored or reset intentionally
- [ ] **Responsive behavior** — Tables become cards on mobile. Sidebars become drawers. Modals become bottom sheets on small screens
- [ ] **Browser semantics** — Use `<button>` not `<div onClick>`. Use `<a href>` not `<div onClick={() => router.push()}>`. Use `<form>` with `action` where applicable

```tsx
// ✅ Debounced search with useDeferredValue
import { useDeferredValue, useState } from 'react';

export function useSearch(initial = '') {
  const [query, setQuery] = useState(initial);
  const deferredQuery = useDeferredValue(query);
  return { query, setQuery, deferredQuery };
}

// ✅ Filters persisted in URL
import { useRouter, useSearchParams } from 'next/navigation';

export function useFilter(key: string) {
  const router = useRouter();
  const params = useSearchParams();
  const value = params.get(key) ?? '';

  function set(val: string) {
    const next = new URLSearchParams(params.toString());
    if (val) next.set(key, val);
    else next.delete(key);
    router.push(`?${next.toString()}`, { scroll: false });
  }

  return [value, set] as const;
}

// ✅ Optimistic update with rollback
async function handleToggleFavorite(id: string) {
  const previous = items;
  setItems((prev) =>
    prev.map((item) => item.id === id ? { ...item, favorite: !item.favorite } : item)
  );

  try {
    await toggleFavoriteAction(id);
  } catch {
    setItems(previous); // rollback
    toast.error('Failed to update. Please try again.');
  }
}
```

---

### 8. Micro-interactions & Polish

The difference between "it works" and "it feels great". Audit for:

- [ ] **Transition consistency** — All interactive state changes use `transition-colors` or `transition-all` at 150–200ms
- [ ] **Tooltips** — Icon buttons, truncated text, and ambiguous controls expose a tooltip on hover/focus
- [ ] **Success feedback** — After a successful action, confirm it: button turns green briefly, checkmark appears, or a toast fires
- [ ] **Progress indicators** — Multi-step forms and file uploads show a step counter or progress bar
- [ ] **Meaningful exit animations** — Deleted items animate out before DOM removal

```tsx
// ✅ Transient success state on button
const [saved, setSaved] = useState(false);

async function handleSave() {
  await saveAction();
  setSaved(true);
  setTimeout(() => setSaved(false), 2000);
}

<LoadingButton
  onClick={handleSave}
  className={cn('transition-colors', saved && 'bg-green-600 hover:bg-green-700')}
>
  {saved ? (
    <><CheckIcon className="h-4 w-4" aria-hidden="true" /> Saved</>
  ) : 'Save changes'}
</LoadingButton>

// ✅ List item exit animation (Framer Motion)
import { AnimatePresence, motion } from 'framer-motion';

<AnimatePresence>
  {items.map((item) => (
    <motion.div
      key={item.id}
      layout
      initial={{ opacity: 1 }}
      exit={{ opacity: 0, height: 0, marginBottom: 0 }}
      transition={{ duration: 0.15 }}
    >
      <ItemCard item={item} />
    </motion.div>
  ))}
</AnimatePresence>
```

---

## Audit Output Format

When performing a full audit, structure the response as:

```
## UX/UI Audit — [Component / Page Name]

### Summary
[2–3 sentences on overall quality and the most critical issues]

### Issues

#### [critical] Button has no loading state
**Where:** `components/CreateForm.tsx`, line 42
**Problem:** Clicking Submit fires the action but the button remains active.
The user receives no feedback and can double-submit.
**Fix:**
[corrected code block]

#### [major] Empty state missing
**Where:** `app/(dashboard)/jobs/page.tsx`
**Problem:** When `jobs.length === 0` the page renders nothing.
**Fix:**
[corrected code block]

...

### What's Already Good
[Acknowledge solid patterns already in place]
```

---

## Hard Rules

| ❌ Never | ✅ Always |
|---|---|
| `outline: none` without a custom `focus-visible` ring | Visible focus ring on every interactive element |
| Full-viewport spinner blocking the page | Scoped inline or button-level loading indicator |
| Generic `"Something went wrong"` with no recovery | Specific message + retry action |
| Delete with no confirmation or undo | Confirmation dialog or optimistic undo toast |
| Placeholder as the only field label | Visible `<label>` associated via `htmlFor` |
| Disable submit before first attempt | Disable only during in-flight request |
| `<div onClick>` for navigation | `<a href>` or `<Link>` |
| `<div onClick>` for actions | `<button type="button">` |
| Validate every keystroke | Validate on blur (format) or submit (required) |
| Empty list renders nothing | `<EmptyState>` component with contextual CTA |
| Animations without `prefers-reduced-motion` check | Respect `prefers-reduced-motion: reduce` |

---

## References

- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [Inclusive Components](https://inclusive-components.design)
- [Nielsen's 10 Usability Heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/)
- [Radix UI Accessibility Primitives](https://www.radix-ui.com)
- [Framer Motion](https://www.framer.com/motion/)
- [Apple HIG — Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback)