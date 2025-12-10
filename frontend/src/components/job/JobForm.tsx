// src/components/job/JobForm.tsx
'use client';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';

const schema = z.object({
  title: z.string().min(1),
  company: z.string().min(1),
  status: z.string().min(1),
});

export default function JobForm() {
  const form = useForm({
    resolver: zodResolver(schema),
    defaultValues: { title: '', company: '', status: 'Applied' },
  });

  async function onSubmit(values: any) {
    await fetch(`${process.env.NEXT_PUBLIC_API_URL}/jobs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(values),
    });
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
      <Input placeholder="Job Title" {...form.register('title')} />
      <Input placeholder="Company" {...form.register('company')} />
      <Input placeholder="Status" {...form.register('status')} />

      <Button type="submit">Save</Button>
    </form>
  );
}
