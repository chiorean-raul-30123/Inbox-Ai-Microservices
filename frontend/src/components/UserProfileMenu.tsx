import { useState } from "react";
import { LogOut, User } from "lucide-react";

import { useAuth } from "../auth/AuthContext";

export function UserProfileMenu() {
  const { user, logoutUser } = useAuth();
  const [isOpen, setIsOpen] = useState(false);

  if (!user) {
    return null;
  }

  const initials = user.full_name
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen((current) => !current)}
        className="flex h-11 w-11 items-center justify-center rounded-full bg-slate-900 text-sm font-bold text-white shadow-sm hover:bg-slate-800"
        title="User profile"
      >
        {initials || <User size={20} />}
      </button>

      {isOpen && (
        <div className="absolute right-0 z-50 mt-3 w-72 rounded-2xl border border-slate-200 bg-white p-4 shadow-lg">
          <div className="flex items-center gap-3 border-b border-slate-100 pb-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-slate-900 text-sm font-bold text-white">
              {initials}
            </div>

            <div>
              <p className="font-semibold text-slate-900">{user.full_name}</p>
              <p className="text-sm text-slate-500">{user.email}</p>
              <p className="mt-1 text-xs font-medium text-blue-600">
                {user.role.name}
              </p>
            </div>
          </div>

          <button
            onClick={logoutUser}
            className="mt-4 flex w-full items-center gap-3 rounded-xl px-3 py-2 text-sm font-medium text-red-600 hover:bg-red-50"
          >
            <LogOut size={18} />
            Logout
          </button>
        </div>
      )}
    </div>
  );
}