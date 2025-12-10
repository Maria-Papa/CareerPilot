// frontend/src/hooks/useJobs.ts
import * as api from '@/lib/api';
import type { Job } from '@/types/job';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

type JobsQueryKey = readonly ['jobs'];

export function useJobs() {
  // useQuery expects an options object with queryKey & queryFn
  return useQuery<Job[], Error, Job[], JobsQueryKey>({
    queryKey: ['jobs'],
    queryFn: () => api.getJobs(),
    // staleTime / cacheTime can be tuned
    staleTime: 1000 * 30,
  });
}

export function useCreateJob() {
  const qc = useQueryClient();

  return useMutation<Job, Error, Partial<Job>, unknown>({
    mutationFn: (payload: Partial<Job>) => api.createJob(payload),
    onSuccess: () => {
      // invalidate by query key as an object
      qc.invalidateQueries({ queryKey: ['jobs'] });
    },
  });
}

export function useUpdateJob() {
  const qc = useQueryClient();

  return useMutation<
    Job,
    Error,
    { id: number; payload: Partial<Job> },
    unknown
  >({
    mutationFn: ({ id, payload }) => api.updateJob(id, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['jobs'] }),
  });
}

export function useDeleteJob() {
  const qc = useQueryClient();

  return useMutation<void, Error, number, unknown>({
    mutationFn: (id: number) => api.deleteJob(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['jobs'] }),
  });
}
