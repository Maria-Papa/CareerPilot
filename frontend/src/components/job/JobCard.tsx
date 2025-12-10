// src/components/job/JobCard.tsx
'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function JobCard({ job }: { job: any }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{job.title}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-1">
        <p className="font-medium">{job.company}</p>
        <p className="text-sm text-muted-foreground">{job.status}</p>
      </CardContent>
    </Card>
  );
}
