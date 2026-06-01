import { useEffect, useMemo, useState } from "react";
import { Shield, Trash2, UserPlus } from "lucide-react";

import { createUser, deactivateUser, fetchUsers } from "../api/usersApi";
import { Layout } from "../components/Layout";
import type { ManagedUserResponse } from "../types/users";
import { roleOptions } from "../types/users";
import { useAuth } from "../auth/AuthContext";

export function AdminUsersPage() {
  const { user: currentUser } = useAuth();

  const [users, setUsers] = useState<ManagedUserResponse[]>([]);
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [roleId, setRoleId] = useState(2);

  const [isLoading, setIsLoading] = useState(true);
  const [isCreating, setIsCreating] = useState(false);
  const [actionUserId, setActionUserId] = useState<string | null>(null);

  const [message, setMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const activeUsersCount = useMemo(
    () => users.filter((user) => user.is_active).length,
    [users],
  );

  async function loadUsers() {
    try {
      setErrorMessage("");
      const data = await fetchUsers();
      setUsers(data);
    } catch {
      setErrorMessage("Could not load users.");
    } finally {
      setIsLoading(false);
    }
  }

  function resetForm() {
    setFullName("");
    setEmail("");
    setPassword("");
    setRoleId(2);
  }

  function validateForm() {
    if (fullName.trim().length < 2) {
      return "Full name must have at least 2 characters.";
    }

    if (!email.includes("@")) {
      return "Please enter a valid email address.";
    }

    if (password.length < 8) {
      return "Password must have at least 8 characters.";
    }

    if (!/[a-z]/.test(password)) {
      return "Password must contain at least one lowercase letter.";
    }

    if (!/[A-Z]/.test(password)) {
      return "Password must contain at least one uppercase letter.";
    }

    if (!/\d/.test(password)) {
      return "Password must contain at least one digit.";
    }

    if (!/[@$!%*?&]/.test(password)) {
      return "Password must contain at least one special character: @$!%*?&.";
    }

    return "";
  }

  async function handleCreateUser() {
    setMessage("");
    setErrorMessage("");

    const validationMessage = validateForm();

    if (validationMessage) {
      setErrorMessage(validationMessage);
      return;
    }

    try {
      setIsCreating(true);

      const createdUser = await createUser({
        full_name: fullName.trim(),
        email: email.trim(),
        password,
        role_id: roleId,
      });

      setUsers((currentUsers) => [createdUser, ...currentUsers]);
      setMessage("User created successfully.");
      resetForm();
    } catch (error: any) {
      const detail = error.response?.data?.detail;
      setErrorMessage(detail || "Could not create user.");
    } finally {
      setIsCreating(false);
    }
  }

  async function handleDeactivateUser(userId: string) {
    setMessage("");
    setErrorMessage("");

    if (userId === currentUser?.id) {
      setErrorMessage("You cannot deactivate your own account.");
      return;
    }

    const confirmed = window.confirm(
      "Are you sure you want to deactivate this user?",
    );

    if (!confirmed) {
      return;
    }

    try {
      setActionUserId(userId);

      const updatedUser = await deactivateUser(userId);

      setUsers((currentUsers) =>
        currentUsers.map((user) =>
          user.id === updatedUser.id ? updatedUser : user,
        ),
      );

      setMessage("User deactivated successfully.");
    } catch (error: any) {
      const detail = error.response?.data?.detail;
      setErrorMessage(detail || "Could not deactivate user.");
    } finally {
      setActionUserId(null);
    }
  }

  useEffect(() => {
    loadUsers();
  }, []);

  return (
    <Layout>
      <div className="flex flex-col gap-2">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-900 text-white">
            <Shield size={22} />
          </div>

          <div>
            <h1 className="text-3xl font-bold text-slate-900">
              User Management
            </h1>
            <p className="mt-1 text-slate-500">
              Create users, assign roles, and deactivate accounts.
            </p>
          </div>
        </div>
      </div>

      {message && (
        <div className="mt-6 rounded-xl bg-green-50 p-4 text-sm font-medium text-green-700">
          {message}
        </div>
      )}

      {errorMessage && (
        <div className="mt-6 rounded-xl bg-red-50 p-4 text-sm font-medium text-red-700">
          {errorMessage}
        </div>
      )}

      <div className="mt-8 grid grid-cols-1 gap-6 xl:grid-cols-[420px_1fr]">
        <section className="rounded-2xl bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100 text-slate-700">
              <UserPlus size={20} />
            </div>

            <div>
              <h2 className="text-lg font-bold text-slate-900">
                Create User
              </h2>
              <p className="text-sm text-slate-500">
                New users can access the system based on their assigned role.
              </p>
            </div>
          </div>

          <div className="mt-6 space-y-4">
            <div>
              <label className="text-sm font-medium text-slate-700">
                Full Name
              </label>
              <input
                value={fullName}
                onChange={(event) => setFullName(event.target.value)}
                className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2 outline-none focus:border-slate-900"
                placeholder="Jane Doe"
              />
            </div>

            <div>
              <label className="text-sm font-medium text-slate-700">
                Email
              </label>
              <input
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2 outline-none focus:border-slate-900"
                placeholder="jane.doe@company.com"
                type="email"
              />
            </div>

            <div>
              <label className="text-sm font-medium text-slate-700">
                Password
              </label>
              <input
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2 outline-none focus:border-slate-900"
                placeholder="Temporary password"
                type="password"
              />
              <p className="mt-2 text-xs text-slate-500">
                Must include uppercase, lowercase, digit and special character.
              </p>
            </div>

            <div>
              <label className="text-sm font-medium text-slate-700">
                Role
              </label>
              <select
                value={roleId}
                onChange={(event) => setRoleId(Number(event.target.value))}
                className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2 outline-none focus:border-slate-900"
              >
                {roleOptions.map((role) => (
                  <option key={role.id} value={role.id}>
                    {role.label}
                  </option>
                ))}
              </select>
            </div>

            <button
              onClick={handleCreateUser}
              disabled={isCreating}
              className="w-full rounded-lg bg-slate-900 px-4 py-2 font-medium text-white hover:bg-slate-800 disabled:opacity-50"
            >
              {isCreating ? "Creating..." : "Create User"}
            </button>
          </div>
        </section>

        <section className="rounded-2xl bg-white p-6 shadow-sm">
          <div className="flex flex-col justify-between gap-3 md:flex-row md:items-center">
            <div>
              <h2 className="text-lg font-bold text-slate-900">
                System Users
              </h2>
              <p className="text-sm text-slate-500">
                {activeUsersCount} active users out of {users.length} total.
              </p>
            </div>
          </div>

          {isLoading ? (
            <p className="mt-6 text-slate-600">Loading users...</p>
          ) : (
            <div className="mt-6 overflow-hidden rounded-xl border border-slate-200">
              <table className="w-full border-collapse text-left text-sm">
                <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
                  <tr>
                    <th className="px-4 py-3">User</th>
                    <th className="px-4 py-3">Role</th>
                    <th className="px-4 py-3">Status</th>
                    <th className="px-4 py-3">Created</th>
                    <th className="px-4 py-3 text-right">Actions</th>
                  </tr>
                </thead>

                <tbody className="divide-y divide-slate-100">
                  {users.map((user) => {
                    const isCurrentUser = user.id === currentUser?.id;

                    return (
                      <tr key={user.id} className="hover:bg-slate-50">
                        <td className="px-4 py-4">
                          <p className="font-semibold text-slate-900">
                            {user.full_name}
                          </p>
                          <p className="text-slate-500">{user.email}</p>
                        </td>

                        <td className="px-4 py-4">
                          <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">
                            {user.role.name}
                          </span>
                        </td>

                        <td className="px-4 py-4">
                          <span
                            className={`rounded-full px-3 py-1 text-xs font-semibold ${
                              user.is_active
                                ? "bg-green-50 text-green-700"
                                : "bg-slate-100 text-slate-500"
                            }`}
                          >
                            {user.is_active ? "Active" : "Inactive"}
                          </span>
                        </td>

                        <td className="px-4 py-4 text-slate-500">
                          {new Date(user.created_at).toLocaleDateString()}
                        </td>

                        <td className="px-4 py-4 text-right">
                          <button
                            onClick={() => handleDeactivateUser(user.id)}
                            disabled={
                              !user.is_active ||
                              isCurrentUser ||
                              actionUserId === user.id
                            }
                            className="inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-red-600 hover:bg-red-50 disabled:cursor-not-allowed disabled:opacity-40"
                          >
                            <Trash2 size={16} />
                            {actionUserId === user.id
                              ? "Deactivating..."
                              : "Deactivate"}
                          </button>
                        </td>
                      </tr>
                    );
                  })}

                  {users.length === 0 && (
                    <tr>
                      <td
                        colSpan={5}
                        className="px-4 py-8 text-center text-slate-500"
                      >
                        No users found.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </div>
    </Layout>
  );
}