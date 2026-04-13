# Reference — Wrapping Shadcn Components

**Absolute rule: never modify /components/ui/. Always wrap.**

When the user provides a `npx shadcn@latest add X` command, immediately create
the corresponding wrapper in `/components/primitives/`.

---

## Button → AppButton

```tsx
// components/primitives/AppButton.tsx
import { Button, buttonVariants } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import { type VariantProps } from "class-variance-authority"

interface AppButtonProps extends React.ComponentProps<typeof Button> {
  // Additional brand variants
  size?: "sm" | "md" | "lg" | "xl"
}

export function AppButton({ className, size = "md", ...props }: AppButtonProps) {
  return (
    <Button
      className={cn(
        // Reset Shadcn defaults → brand tokens
        "font-medium tracking-wide transition-all duration-150",
        // No box-shadow, no glow — clean visible focus
        "focus-visible:ring-2 focus-visible:ring-[oklch(var(--ring))] focus-visible:ring-offset-2",
        // Hover: no scale — slight translation
        "hover:-translate-y-px active:translate-y-0",
        size === "xl" && "h-12 px-8 text-base",
        className
      )}
      {...props}
    />
  )
}
```

## Card → AppCard

```tsx
// components/primitives/AppCard.tsx
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { cn } from "@/lib/utils"

interface AppCardProps extends React.ComponentProps<typeof Card> {
  variant?: "default" | "elevated" | "ghost" | "outlined"
  grain?: boolean
  interactive?: boolean
}

export function AppCard({
  variant = "default",
  grain = false,
  interactive = false,
  className,
  children,
  ...props
}: AppCardProps) {
  return (
    <Card
      className={cn(
        "relative overflow-hidden rounded-xl",
        // Removing default Shadcn shadow
        "shadow-none",
        // Variants — elevation via color contrast, not shadow
        variant === "default"  && "border border-[oklch(var(--border))] bg-[oklch(var(--card))]",
        variant === "elevated" && "border border-[oklch(var(--border-strong,var(--border)))] bg-[oklch(var(--card-elevated,var(--card)))]",
        variant === "ghost"    && "border-transparent bg-transparent",
        variant === "outlined" && "border-2 border-[oklch(var(--primary))] bg-transparent",
        // Interactivity — no zoom, reveal via border
        interactive && "cursor-pointer transition-colors duration-150 hover:border-[oklch(var(--accent))]",
        // Optional premium grain
        grain && "after:absolute after:inset-0 after:pointer-events-none after:bg-noise after:opacity-[0.04] after:mix-blend-overlay",
        className
      )}
      {...props}
    >
      {children}
    </Card>
  )
}

// Re-export sub-components for fluid usage
export { CardContent, CardHeader, CardTitle, CardDescription }
```

## Input → AppInput

```tsx
// components/primitives/AppInput.tsx
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"
import { Label } from "@/components/ui/label"

interface AppInputProps extends React.ComponentProps<typeof Input> {
  label?: string
  hint?: string
  error?: string
}

export function AppInput({ label, hint, error, className, id, ...props }: AppInputProps) {
  const inputId = id || label?.toLowerCase().replace(/\s/g, '-')
  
  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <Label htmlFor={inputId} className="text-sm font-medium text-[oklch(var(--foreground))]">
          {label}
        </Label>
      )}
      <Input
        id={inputId}
        className={cn(
          "border-[oklch(var(--border))] bg-[oklch(var(--background))]",
          "focus-visible:ring-1 focus-visible:ring-[oklch(var(--ring))] focus-visible:border-[oklch(var(--ring))]",
          "placeholder:text-[oklch(var(--muted-foreground))]",
          "transition-colors duration-100",
          error && "border-[oklch(var(--destructive))]",
          className
        )}
        aria-describedby={error ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined}
        aria-invalid={!!error}
        {...props}
      />
      {hint && !error && (
        <p id={`${inputId}-hint`} className="text-xs text-[oklch(var(--muted-foreground))]">{hint}</p>
      )}
      {error && (
        <p id={`${inputId}-error`} role="alert" className="text-xs text-[oklch(var(--destructive))]">{error}</p>
      )}
    </div>
  )
}
```

## Badge → AppBadge

```tsx
// components/primitives/AppBadge.tsx
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"

type BadgeStatus = "default" | "success" | "warning" | "error" | "info" | "neutral"

interface AppBadgeProps extends React.ComponentProps<typeof Badge> {
  status?: BadgeStatus
  dot?: boolean
}

const statusStyles: Record<BadgeStatus, string> = {
  default: "bg-[oklch(var(--primary)/0.1)] text-[oklch(var(--primary))] border-[oklch(var(--primary)/0.2)]",
  success: "bg-[oklch(0.92_0.05_150)] text-[oklch(0.30_0.12_150)] border-[oklch(0.80_0.08_150)]",
  warning: "bg-[oklch(0.95_0.06_60)]  text-[oklch(0.40_0.12_60)]  border-[oklch(0.85_0.08_60)]",
  error:   "bg-[oklch(0.95_0.05_20)]  text-[oklch(0.40_0.15_20)]  border-[oklch(0.80_0.10_20)]",
  info:    "bg-[oklch(0.93_0.04_220)] text-[oklch(0.35_0.10_220)] border-[oklch(0.80_0.06_220)]",
  neutral: "bg-[oklch(var(--muted))]  text-[oklch(var(--muted-foreground))] border-[oklch(var(--border))]",
}

export function AppBadge({ status = "default", dot = false, className, children, ...props }: AppBadgeProps) {
  return (
    <Badge
      className={cn(
        "inline-flex items-center gap-1.5 border font-medium",
        "shadow-none",  // Removing default Shadcn shadow
        statusStyles[status],
        className
      )}
      {...props}
    >
      {dot && (
        <span className="inline-block h-1.5 w-1.5 rounded-full bg-current opacity-70" aria-hidden />
      )}
      {children}
    </Badge>
  )
}
```

## Dialog → AppDialog

```tsx
// components/primitives/AppDialog.tsx
import {
  Dialog, DialogContent, DialogHeader, DialogTitle,
  DialogDescription, DialogFooter
} from "@/components/ui/dialog"
import { cn } from "@/lib/utils"

interface AppDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  title: string
  description?: string
  size?: "sm" | "md" | "lg" | "xl"
  children: React.ReactNode
  footer?: React.ReactNode
}

const sizeMap = { sm: "max-w-sm", md: "max-w-md", lg: "max-w-lg", xl: "max-w-xl" }

export function AppDialog({ open, onOpenChange, title, description, size = "md", children, footer }: AppDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className={cn(
        sizeMap[size],
        "rounded-2xl border border-[oklch(var(--border))] bg-[oklch(var(--card))]",
        "shadow-none",  // No massive shadow — the backdrop handles depth
      )}>
        <DialogHeader>
          <DialogTitle className="text-[oklch(var(--foreground))]">{title}</DialogTitle>
          {description && <DialogDescription>{description}</DialogDescription>}
        </DialogHeader>
        {children}
        {footer && <DialogFooter>{footer}</DialogFooter>}
      </DialogContent>
    </Dialog>
  )
}
```

## Select → AppSelect

```tsx
// components/primitives/AppSelect.tsx
import {
  Select, SelectContent, SelectItem,
  SelectTrigger, SelectValue
} from "@/components/ui/select"
import { cn } from "@/lib/utils"

interface SelectOption { value: string; label: string; disabled?: boolean }

interface AppSelectProps {
  options: SelectOption[]
  value?: string
  onValueChange?: (value: string) => void
  placeholder?: string
  disabled?: boolean
  className?: string
}

export function AppSelect({ options, placeholder = "Select...", className, ...props }: AppSelectProps) {
  return (
    <Select {...props}>
      <SelectTrigger className={cn(
        "border-[oklch(var(--border))] bg-[oklch(var(--background))]",
        "focus:ring-1 focus:ring-[oklch(var(--ring))]",
        "shadow-none",
        className
      )}>
        <SelectValue placeholder={placeholder} />
      </SelectTrigger>
      <SelectContent className="border-[oklch(var(--border))] bg-[oklch(var(--card))] shadow-none rounded-xl">
        {options.map(opt => (
          <SelectItem
            key={opt.value}
            value={opt.value}
            disabled={opt.disabled}
            className="focus:bg-[oklch(var(--accent)/0.1)] focus:text-[oklch(var(--accent))]"
          >
            {opt.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  )
}
```

## Table → AppTable

```tsx
// components/primitives/AppTable.tsx
import {
  Table, TableBody, TableCell, TableHead,
  TableHeader, TableRow
} from "@/components/ui/table"
import { cn } from "@/lib/utils"

interface Column<T> {
  key: keyof T | string
  label: string
  align?: "left" | "right" | "center"
  render?: (row: T) => React.ReactNode
}

interface AppTableProps<T extends Record<string, unknown>> {
  columns: Column<T>[]
  data: T[]
  className?: string
  striped?: boolean
}

export function AppTable<T extends Record<string, unknown>>({
  columns, data, className, striped = false
}: AppTableProps<T>) {
  return (
    <div className={cn("rounded-xl border border-[oklch(var(--border))] overflow-hidden", className)}>
      <Table>
        <TableHeader>
          <TableRow className="bg-[oklch(var(--muted))] hover:bg-[oklch(var(--muted))]">
            {columns.map(col => (
              <TableHead key={String(col.key)} className={cn(
                "text-[oklch(var(--muted-foreground))] font-medium text-xs uppercase tracking-wider",
                col.align === "right" && "text-right",
                col.align === "center" && "text-center",
              )}>
                {col.label}
              </TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((row, i) => (
            <TableRow
              key={i}
              className={cn(
                "border-[oklch(var(--border))] transition-colors",
                striped && i % 2 === 0 && "bg-[oklch(var(--muted)/0.4)]",
                "hover:bg-[oklch(var(--accent)/0.05)]"  // Subtle hover, no aggressive highlight
              )}
            >
              {columns.map(col => (
                <TableCell key={String(col.key)} className={cn(
                  col.align === "right" && "text-right",
                  col.align === "center" && "text-center",
                )}>
                  {col.render ? col.render(row) : String(row[col.key as keyof T] ?? '')}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
```

---

## Business Block Pattern

After primitives, compose business blocks in `/components/blocks/`:

```
blocks/
├── HeroSection.tsx          ← Landing hero (no full-screen gradient!)
├── PricingCard.tsx          ← Pricing card
├── FeatureGrid.tsx          ← Asymmetric feature grid
├── TestimonialCarousel.tsx  ← Testimonials
├── StatsBanner.tsx          ← Key metrics banner
└── NavBar.tsx               ← Navigation (no generic blur-backdrop!)
```

Each block imports **only from `/primitives/`**, never from `/ui/` directly.
