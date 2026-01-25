'use client';

import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { useEffect, useRef, useState } from 'react';

const THEMES = [
  {
    id: 'theme-midnight-teal',
    label: 'Midnight Teal',
    desc: 'Calm, focused',
    swatch: 'from-teal-500 to-cyan-600',
  },
  {
    id: 'theme-neon-ember',
    label: 'Neon Ember',
    desc: 'Energetic',
    swatch: 'from-orange-400 to-rose-500',
  },
  {
    id: 'theme-slate-violet',
    label: 'Slate Violet',
    desc: 'Elegant',
    swatch: 'from-violet-500 to-purple-700',
  },
  {
    id: 'theme-paper-mint',
    label: 'Paper Mint',
    desc: 'Fresh',
    swatch: 'from-emerald-400 to-emerald-600',
  },
  {
    id: 'theme-sunlit-amber',
    label: 'Sunlit Amber',
    desc: 'Warm',
    swatch: 'from-amber-400 to-orange-500',
  },
  {
    id: 'theme-soft-sky',
    label: 'Soft Sky',
    desc: 'Clean',
    swatch: 'from-sky-400 to-blue-500',
  },
];

function setThemeCookie(themeId: string) {
  try {
    document.cookie = `cp_theme=${encodeURIComponent(themeId)}; Path=/; Max-Age=${60 * 60 * 24 * 365}; SameSite=Lax`;
  } catch {}
}

export default function ThemeSwitcher() {
  const triggerRef = useRef<HTMLButtonElement | null>(null);

  const [theme, setTheme] = useState<string | null>(null);

  useEffect(() => {
    try {
      const cookie = document.cookie
        .split('; ')
        .find((c) => c.startsWith('cp_theme='));
      const cookieValue = cookie
        ? decodeURIComponent(cookie.split('=')[1])
        : null;
      const htmlTheme =
        document.documentElement.getAttribute('data-theme') ?? null;
      const initial = htmlTheme ?? cookieValue ?? 'theme-midnight-teal';

      const id = window.setTimeout(() => setTheme(initial), 0);
      return () => window.clearTimeout(id);
    } catch {
      // ignore
    }
  }, []);

  useEffect(() => {
    if (!theme) return;
    document.documentElement.setAttribute('data-theme', theme);
    setThemeCookie(theme);
    try {
      localStorage.setItem('cp_theme', theme);
    } catch {}
  }, [theme]);

  const swatch = theme ? (
    <span
      className={`w-3 h-3 rounded-sm bg-gradient-to-br ${
        THEMES.find((t) => t.id === theme)?.swatch ?? THEMES[0].swatch
      }`}
      aria-hidden
    />
  ) : (
    <span className="w-3 h-3 rounded-sm opacity-0" aria-hidden />
  );

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          ref={triggerRef}
          variant="ghost"
          className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-[var(--surface-border)] bg-card text-sm focus-visible:ring-0 focus-visible:outline-none hover:bg-transparent active:bg-transparent"
          aria-label="Open theme switcher"
        >
          {swatch}
          <span className="text-sm text-muted-foreground">Theme</span>
          <svg
            width="12"
            height="12"
            viewBox="0 0 24 24"
            fill="none"
            className="text-muted-foreground"
            aria-hidden
          >
            <path
              d="M6 9l6 6 6-6"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </Button>
      </DropdownMenuTrigger>

      <DropdownMenuContent
        align="end"
        sideOffset={8}
        className="min-w-[220px] p-2 rounded-md border border-[var(--surface-border)] bg-[var(--popover-bg)] shadow-lg backdrop-blur-md"
      >
        {THEMES.map((t) => {
          const checked = theme === t.id;
          return (
            <DropdownMenuItem
              key={t.id}
              onSelect={() => setTheme(t.id)}
              className={`my-1 flex items-center gap-3 px-3 py-2 rounded-full text-left ${
                checked
                  ? 'bg-[var(--accent-soft)]'
                  : 'hover:bg-[var(--accent-soft)]'
              }`}
            >
              <span
                className={`w-4 h-4 rounded-sm bg-gradient-to-br ${t.swatch}`}
                aria-hidden
              />
              <div className="flex flex-col text-sm">
                <span className="font-medium text-foreground">{t.label}</span>
                <span className="text-xs text-muted-foreground">{t.desc}</span>
              </div>
            </DropdownMenuItem>
          );
        })}

        <DropdownMenuSeparator className="my-2 border-[var(--surface-border)]" />

        <div className="flex justify-between px-1">
          <Button
            variant="outline"
            size="sm"
            className="text-xs px-2 py-1 rounded-md"
            onClick={() => {
              try {
                document.cookie = 'cp_theme=; Path=/; Max-Age=0; SameSite=Lax';
              } catch {}
              try {
                localStorage.removeItem('cp_theme');
              } catch {}
              setTheme('theme-midnight-teal');
              triggerRef.current?.focus();
            }}
          >
            Reset
          </Button>

          <Button
            variant="ghost"
            size="sm"
            className="text-xs px-2 py-1 rounded-md"
            onClick={() => {
              triggerRef.current?.focus();
            }}
          >
            Close
          </Button>
        </div>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
