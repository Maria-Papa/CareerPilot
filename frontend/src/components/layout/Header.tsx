'use client';

import { Button } from '@/components/ui/button';
import Link from 'next/link';
import ThemeSwitcher from '../shared/ThemeSwitcher';

export default function Header() {
  return (
    <header className="sticky top-0 z-40 backdrop-blur-md bg-card/80 border-b border-[var(--surface-border)] h-[var(--header-offset)] flex items-center">
      <div className="mx-auto w-full max-w-[2000px] flex items-center justify-between px-[var(--page-padding)]">
        {/* Left: Brand + Nav */}
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-md bg-gradient-to-b from-[var(--accent)] to-[var(--accent-foreground)] text-[var(--card-foreground)] font-bold flex items-center justify-center shadow-lg">
              CP
            </div>
            <div className="leading-tight">
              <div className="text-base font-semibold">CareerPilot</div>
              <div className="text-xs text-muted-foreground">
                Personal ATS &amp; Career OS
              </div>
            </div>
          </div>

          <nav className="flex gap-2" aria-label="Primary">
            <Button
              asChild
              variant="ghost"
              size="sm"
              className="px-3 py-1 rounded-full text-sm"
            >
              <Link
                href="/"
                className="text-muted-foreground hover:text-foreground"
              >
                Dashboard
              </Link>
            </Button>

            <Button
              asChild
              variant="ghost"
              size="sm"
              className="px-3 py-1 rounded-full text-sm"
            >
              <Link
                href="/jobs"
                className="text-muted-foreground hover:text-foreground"
              >
                Applications
              </Link>
            </Button>

            <Button
              asChild
              variant="ghost"
              size="sm"
              className="px-3 py-1 rounded-full text-sm"
            >
              <Link
                href="/salary"
                className="text-muted-foreground hover:text-foreground"
              >
                Salary &amp; COL
              </Link>
            </Button>

            <Button
              asChild
              variant="ghost"
              size="sm"
              className="px-3 py-1 rounded-full text-sm"
            >
              <Link
                href="/automations"
                className="text-muted-foreground hover:text-foreground"
              >
                Automations
              </Link>
            </Button>
          </nav>
        </div>

        {/* Right: Theme + Pill + CTA */}
        <div className="flex items-center gap-4">
          <ThemeSwitcher />

          <div className="flex items-center gap-3">
            <div className="px-3 py-1 rounded-full border border-[var(--surface-border)] text-xs text-muted-foreground">
              Local · Open Source · Yours
            </div>

            <Button
              asChild
              variant="default"
              size="sm"
              className="inline-flex items-center gap-2 rounded-full px-3 py-1 text-sm font-medium bg-gradient-to-r from-[var(--accent)] to-[var(--accent-foreground)] text-[var(--card-foreground)] shadow-lg"
            >
              <Link href="/jobs/new">
                <span className="text-lg">＋</span>
                <span>New Application</span>
              </Link>
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
}
