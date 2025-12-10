// src/app/page.tsx
import { Button } from '@/components/ui/button';
import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="flex flex-col items-center mt-20 gap-6">
      <h1 className="text-5xl font-bold text-center">CareerPilot</h1>
      <p className="text-lg text-muted-foreground">
        Your personal career command center.
      </p>

      <Link href="/jobs">
        <Button size="lg">View Job Applications</Button>
      </Link>
    </div>
  );
}
