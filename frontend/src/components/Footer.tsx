import { Button } from '@/components/ui/button';
import Link from 'next/link';

export default function Footer() {
  return (
    <footer
      role="contentinfo"
      className="w-full border-t border-[var(--sidebar-border)] bg-card h-[var(--footer-offset)] flex items-center"
    >
      <div className="w-full max-w-[2000px] mx-auto px-[var(--page-padding)] flex flex-col md:flex-row justify-between items-center gap-2">
        <div className="flex items-center gap-3">
          <div className="text-sm text-[var(--muted-foreground)]">
            <strong className="font-medium">CareerPilot</strong>
            <span className="ml-2">— Local · Open Source · Yours</span>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <nav aria-label="Footer links" className="flex items-center gap-3">
            <Button asChild variant="ghost" size="sm" className="p-0">
              <Link
                href="/privacy"
                className="text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
              >
                Privacy
              </Link>
            </Button>

            <Button asChild variant="ghost" size="sm" className="p-0">
              <Link
                href="/terms"
                className="text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
              >
                Terms
              </Link>
            </Button>

            <Button asChild variant="ghost" size="sm" className="p-0">
              <Link
                href="/about"
                className="text-sm text-[var(--muted-foreground)] hover:text-[var(--foreground)]"
              >
                About
              </Link>
            </Button>
          </nav>

          <div className="text-sm text-[var(--muted-foreground)]">
            © {new Date().getFullYear()} CareerPilot
          </div>
        </div>
      </div>
    </footer>
  );
}
