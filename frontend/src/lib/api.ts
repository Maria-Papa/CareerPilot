// frontend/src/lib/api.ts
import type { Job } from '@/types/job';

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

async function handleRes(res: Response) {
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status} ${res.statusText} - ${text}`);
  }
  return res.json();
}

export async function getJobs(): Promise<Job[]> {
  const res = await fetch(`${API_URL}/jobs`, { cache: 'no-store' });
  return handleRes(res);
}

export async function getJob(id: number): Promise<Job> {
  const res = await fetch(`${API_URL}/jobs/${id}`, { cache: 'no-store' });
  return handleRes(res);
}

export async function createJob(payload: Partial<Job>): Promise<Job> {
  const res = await fetch(`${API_URL}/jobs`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return handleRes(res);
}

export async function updateJob(
  id: number,
  payload: Partial<Job>
): Promise<Job> {
  const res = await fetch(`${API_URL}/jobs/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return handleRes(res);
}

export async function deleteJob(id: number): Promise<void> {
  const res = await fetch(`${API_URL}/jobs/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Delete failed');
}
