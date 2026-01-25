import { Card } from '@/components/ui/card';
import { cn } from '@/lib/utils';

export function AppCard(props: React.ComponentProps<typeof Card>) {
  const { className, ...rest } = props;

  return (
    <Card
      className={cn(
        'border border-[var(--surface-border)] bg-card shadow-sm',
        className
      )}
      {...rest}
    />
  );
}
