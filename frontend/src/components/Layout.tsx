import type { ReactNode } from "react";

import { Sidebar } from "./Sidebar";
import { UserProfileMenu } from "./UserProfileMenu";

export function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="flex h-screen overflow-hidden bg-slate-100">
      <Sidebar />

      <div className="flex min-h-0 flex-1 flex-col">
        <header className="flex h-16 shrink-0 items-center justify-end border-b border-slate-200 bg-white px-8">
          <UserProfileMenu />
        </header>

        <main className="min-h-0 flex-1 overflow-y-auto p-8">
          {children}
        </main>
      </div>
    </div>
  );
}