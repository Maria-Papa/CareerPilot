import { AppCard } from '@/components/shared/AppCard';
import { Button } from '@/components/ui/button';
import {
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import Link from 'next/link';

export default function HomePage() {
  return (
    <AppCard className="w-full max-w-2xl mx-auto">
      <CardHeader className="text-center space-y-3">
        <CardTitle className="text-4xl font-semibold tracking-tight">
          CareerPilot
        </CardTitle>
        <CardDescription className="text-base">
          Your personal career system — structured, truthful, reusable.
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-8 text-center">
        <p className="text-sm text-muted-foreground leading-relaxed">
          CareerPilot helps you capture what you’ve actually done in your
          career, structure it once, and reuse it everywhere — CVs,
          applications, interviews, and decisions.
        </p>

        <ul className="space-y-5 text-left mx-auto max-w-md">
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
      </CardContent>
    </AppCard>
  );
}
