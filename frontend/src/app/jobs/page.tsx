// src/app/jobs/page.tsx
import JobCard from '@/components/job/JobCard';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

async function getJobs() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/jobs`);
  return res.json();
}

export default async function JobsPage() {
  const jobs = await getJobs();

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-semibold">Job Applications</h1>
        <Link href="/jobs/new">
          <Button>Add New Job</Button>
        </Link>
      </div>

      <div className="grid gap-4">
        {jobs.map((job: any) => (
          <JobCard key={job.id} job={job} />
        ))}
      </div>
    </div>
  );
}
