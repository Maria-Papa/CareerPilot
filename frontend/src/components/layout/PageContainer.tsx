import { ReactNode } from 'react';

export function PageContainer({ children }: { children: ReactNode }) {
  return <div className="w-full max-w-4xl mx-auto py-10 px-4">{children}</div>;
}
