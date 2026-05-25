import {
  CalendarDays,
  CheckSquare,
  Inbox,
  ShieldAlert,
  Trash2,
} from "lucide-react";
import { NavLink } from "react-router-dom";

type MailSidebarProps = {
  activeSection: string;
};

export function MailSidebar({ activeSection }: MailSidebarProps) {
  const items = [
    { key: "inbox", label: "Inbox", icon: Inbox, path: "/inbox" },
    { key: "calendar", label: "Calendar", icon: CalendarDays, path: "/calendar" },
    { key: "trash", label: "Deleted", icon: Trash2, path: "/deleted" },
    { key: "spam", label: "Spam", icon: ShieldAlert, path: "/spam" },
    { key: "todo", label: "To Do", icon: CheckSquare, path: "/todo" },
  ];

  return (
    <aside className="flex h-full w-20 shrink-0 flex-col items-center border-r border-slate-800 bg-[#0f172a] py-4">
      <div className="mb-7 flex h-11 w-11 items-center justify-center rounded-2xl bg-blue-600 text-sm font-bold text-white shadow-lg shadow-blue-900/30 transition duration-200 hover:-translate-y-1 hover:scale-105">
        AI
      </div>

      <nav className="flex flex-1 flex-col gap-3">
        {items.map((item) => {
          const Icon = item.icon;
          const isActive = activeSection === item.key;

          return (
            <NavLink
              key={item.key}
              to={item.path}
              title={item.label}
              className={`group relative flex h-12 w-12 items-center justify-center rounded-2xl transition-all duration-200 ease-out hover:-translate-y-1 hover:scale-110 hover:shadow-xl ${
                isActive
                  ? "bg-blue-600 text-white shadow-lg shadow-blue-900/30"
                  : "text-slate-400 hover:bg-white hover:text-[#0f172a]"
              }`}
            >
              <Icon
                size={22}
                className="transition-transform duration-200 group-hover:scale-110"
              />

              <span className="pointer-events-none absolute left-16 scale-95 rounded-xl bg-slate-950 px-3 py-2 text-xs font-semibold text-white opacity-0 shadow-lg transition-all duration-200 group-hover:scale-100 group-hover:opacity-100">
                {item.label}
              </span>
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}