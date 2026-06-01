import { NavLink } from "react-router-dom";
import { BarChart3, FileText, Inbox, LogOut, Settings, Upload,Users,Activity } from "lucide-react";

import { useAuth } from "../auth/AuthContext";

export function Sidebar() {
  const { user, logoutUser } = useAuth();
  const roleName = user?.role.name;

  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `flex items-center gap-3 rounded-xl px-3 py-2 text-sm font-medium ${
      isActive
        ? "bg-slate-900 text-white"
        : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
    }`;

  return (
    <aside className="flex h-screen w-72 flex-col border-r border-slate-200 bg-white px-4 py-5">
      <div>
        <h1 className="text-xl font-bold text-slate-900">Inbox AI</h1>
        <p className="mt-1 text-sm text-slate-500">Document Routing System</p>
      </div>

      <nav className="mt-8 flex flex-1 flex-col gap-2">
        {roleName === "ADMIN" && (
          <>
            <NavLink to="/" className={linkClass}>
              <BarChart3 size={18} />
              Dashboard
            </NavLink>

            <NavLink to="/upload" className={linkClass}>
              <Upload size={18} />
              Upload
            </NavLink>

            <NavLink to="/needs-review" className={linkClass}>
              <FileText size={18} />
              Needs Review
            </NavLink>
            <NavLink to="/admin/users" className={linkClass}>
              <Users size={18} />
              User Management
            </NavLink>
            <NavLink to="/system-health" className={linkClass}>
              <Activity size={18} />
              Operations Center
            </NavLink>

            <NavLink to="/settings" className={linkClass}>
              <Settings size={18} />
              Settings
            </NavLink>
          </>
        )}

        {roleName === "HR" && (
          <NavLink to="/inbox/hr" className={linkClass}>
            <Inbox size={18} />
            HR Inbox
          </NavLink>
        )}

        {roleName === "FINANCE" && (
          <NavLink to="/inbox/finance" className={linkClass}>
            <Inbox size={18} />
            Finance Inbox
          </NavLink>
        )}

        {roleName === "LEGAL" && (
          <NavLink to="/inbox/legal" className={linkClass}>
            <Inbox size={18} />
            Legal Inbox
          </NavLink>
        )}
      </nav>

      <div className="border-t border-slate-200 pt-4">
        <p className="text-sm font-medium text-slate-900">{user?.full_name}</p>
        <p className="text-xs text-slate-500">{user?.role.name}</p>

        <button
          onClick={logoutUser}
          className="mt-4 flex w-full items-center gap-3 rounded-xl px-3 py-2 text-sm font-medium text-red-600 hover:bg-red-50"
        >
          <LogOut size={18} />
          Logout
        </button>
      </div>
    </aside>
  );
}