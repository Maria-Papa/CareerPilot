import { Button } from '@/components/ui/button';
import Link from 'next/link';

export default function HomePage() {
  return (
    <div
      role="main"
      className="min-h-[calc(100vh - var(--header-offset) - var(--footer-offset))] flex items-center justify-center px-6"
    >
      <section className="w-full max-w-xl text-center space-y-10">
        <header className="space-y-3">
          <h1 className="text-4xl font-semibold tracking-tight">CareerPilot</h1>
          <p className="text-base text-muted-foreground">
            Your personal career system — structured, truthful, reusable.
          </p>
        </header>

        <p className="text-sm leading-relaxed text-muted-foreground">
          CareerPilot helps you capture what you’ve actually done in your
          career, structure it once, and reuse it everywhere — CVs,
          applications, interviews, and decisions.
        </p>

        <ul className="space-y-5 text-left">
          <li className="space-y-1">
            <p className="font-medium">Capture your real experience</p>
            <p className="text-sm text-muted-foreground">
              Turn past roles and projects into clear, structured career notes.
            </p>
          </li>

          <li className="space-y-1">
            <p className="font-medium">Reuse your data everywhere</p>
            <p className="text-sm text-muted-foreground">
              Generate tailored CVs, cover letters, and interview answers from a
              single source of truth.
            </p>
          </li>

          <li className="space-y-1">
            <p className="font-medium">Automate the busy work</p>
            <p className="text-sm text-muted-foreground">
              Track applications, explore matches, and run job-search workflows
              with less effort.
            </p>
          </li>
        </ul>

        <div className="space-y-3">
          <Button asChild size="lg" className="w-full">
            <Link href="/career/setup">Start by capturing my career</Link>
          </Button>

          <Link
            href="/jobs"
            className="block text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            I already have career data
          </Link>
        </div>
      </section>
    </div>
  );
}
