// src/app/jobs/new/page.tsx
import JobForm from "@/components/job/JobForm";

export default function NewJobPage() {
  return (
    <div className="space-y-6 max-w-xl mx-auto">
      <h1 className="text-3xl font-semibold">Add New Job Application</h1>
      <JobForm />
    </div>
  );
}
