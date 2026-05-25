import { CalendarDays, CheckSquare, Mail, ShieldAlert, Trash2 } from "lucide-react";

import { MailSidebar } from "../components/mail/MailSidebar";
import { UserProfileMenu } from "../components/UserProfileMenu";

type PlaceholderPageProps = {
  title: string;
  description: string;
  activeSection: string;
  icon: "mail" | "calendar" | "trash" | "spam" | "todo";
};

const iconMap = {
  mail: Mail,
  calendar: CalendarDays,
  trash: Trash2,
  spam: ShieldAlert,
  todo: CheckSquare,
};

export function PlaceholderPage({
  title,
  description,
  activeSection,
  icon,
}: PlaceholderPageProps) {
  const Icon = iconMap[icon];

  return (
    <div className="flex h-screen overflow-hidden bg-slate-100">
      <MailSidebar activeSection={activeSection} />

      <div className="flex flex-1 flex-col">
        <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-6">
          <div>
            <h1 className="text-lg font-bold text-slate-900">{title}</h1>
            <p className="text-sm text-slate-500">{description}</p>
          </div>

          <UserProfileMenu />
        </header>

        <main className="flex flex-1 items-center justify-center">
          <div className="rounded-2xl bg-white p-10 text-center shadow-sm">
            <Icon className="mx-auto text-slate-300" size={72} />
            <h2 className="mt-6 text-2xl font-bold text-slate-900">{title}</h2>
            <p className="mt-2 max-w-md text-slate-500">
              This section is prepared in the interface and will be implemented later.
            </p>
          </div>
        </main>
      </div>
    </div>
  );
}