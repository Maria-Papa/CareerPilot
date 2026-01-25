import Footer from '@/components/layout/Footer';
import Header from '@/components/layout/Header';
import { PageContainer } from '@/components/layout/PageContainer';
import Sidebar from '@/components/layout/Sidebar';
import { ReactQueryProvider } from '@/providers/ReactQueryProvider';
import type { Metadata } from 'next';
import { Geist, Geist_Mono } from 'next/font/google';
import { cookies } from 'next/headers';
import React from 'react';
import '../styles/globals.css';

const geistSans = Geist({ variable: '--font-geist-sans', subsets: ['latin'] });
const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
});

export const metadata: Metadata = {
  title: 'CareerPilot',
  description: 'Track your career',
};

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const cookieStore = await cookies();
  const themeCookie = cookieStore.get('cp_theme')?.value;
  const initialTheme = themeCookie ?? 'theme-midnight-teal';

  return (
    <html lang="en" data-theme={initialTheme} className="antialiased">
      <body
        className={`${geistSans.variable} ${geistMono.variable} bg-background text-foreground`}
      >
        <ReactQueryProvider>
          <div className="flex min-h-screen flex-col">
            <Header />

            <div className="flex flex-1 w-full max-w-[2000px] mx-auto gap-6 px-[var(--page-padding)]">
              <aside className="hidden lg:block w-[280px] shrink-0">
                <Sidebar />
              </aside>

              <main
                role="main"
                className="flex-1 min-h-[calc(100vh-var(--header-offset)-var(--footer-offset))]"
              >
                <PageContainer>{children}</PageContainer>
              </main>
            </div>

            <Footer />
          </div>
        </ReactQueryProvider>
      </body>
    </html>
  );
}
