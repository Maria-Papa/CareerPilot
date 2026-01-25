import { Button } from '@/components/ui/button';
import Link from 'next/link';

export default function Sidebar() {
  return (
    <aside
      className="sidebar h-full w-[280px] shrink-0 flex flex-col px-4 py-6 border-r border-[var(--surface-border)] bg-[var(--sidebar-bg)]"
      aria-label="Sidebar"
    >
      {/* Scrollable menu area */}
      <div className="flex-1 overflow-y-auto">
        {[
          {
            title: 'Workspace',
            items: [
              { href: '/', icon: '🏠', label: 'Overview', active: true },
              { href: '/jobs', icon: '📄', label: 'Applications' },
              { href: '/interviews', icon: '🗓', label: 'Interviews' },
              { href: '/assessments', icon: '🧪', label: 'Assessments' },
            ],
          },
          {
            title: 'Decisions',
            items: [
              { href: '/salary', icon: '💶', label: 'Salary & COL' },
              { href: '/comparisons', icon: '📊', label: 'Comparisons' },
              { href: '/relocation', icon: '🧭', label: 'Relocation' },
            ],
          },
          {
            title: 'Automation',
            items: [
              {
                href: '/automation/email',
                icon: '📥',
                label: 'Email scanning',
              },
              {
                href: '/automation/scraper',
                icon: '🕷',
                label: 'Job scraping',
              },
              { href: '/automation/cv', icon: '📑', label: 'CV generator' },
            ],
          },
        ].map((section) => (
          <div key={section.title} className="mb-4">
            <div className="text-xs uppercase tracking-wider text-muted-foreground mb-2">
              {section.title}
            </div>

            <nav className="flex flex-col gap-2" aria-label={section.title}>
              {section.items.map((item) => (
                <Button
                  key={item.href}
                  asChild
                  variant="ghost"
                  className={`flex items-center gap-3 p-2 rounded-md text-sm ${
                    item.active
                      ? 'text-[var(--sidebar-foreground)] bg-[rgba(255,255,255,0.02)]'
                      : 'text-muted-foreground hover:text-foreground'
                  }`}
                >
                  <Link
                    href={item.href}
                    className="flex w-full items-center justify-start"
                  >
                    <span className="icon" aria-hidden>
                      {item.icon}
                    </span>
                    <span>{item.label}</span>
                  </Link>
                </Button>
              ))}
            </nav>
          </div>
        ))}
      </div>

      {/* Footer pinned to bottom */}
      <div className="mt-4 p-3 rounded-md bg-[var(--accent-soft)] border border-[var(--accent)] text-sm text-muted-foreground">
        <div className="mb-1 font-medium">You own the data.</div>
        <div className="text-xs">
          CareerPilot keeps a single source of truth for your career, locally.
        </div>
      </div>
    </aside>
  );
}
