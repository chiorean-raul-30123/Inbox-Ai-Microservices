import { useState } from "react";
import { Eye, EyeOff, Lock, LogOut, User, X } from "lucide-react";

import { changePassword } from "../api/authApi";
import { useAuth } from "../auth/AuthContext";

export function UserProfileMenu() {
  const { user, logoutUser } = useAuth();

  const [isOpen, setIsOpen] = useState(false);
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [showPasswordForm, setShowPasswordForm] = useState(false);

  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmNewPassword, setConfirmNewPassword] = useState("");

  const [showCurrentPassword, setShowCurrentPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);

  const [message, setMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  if (!user) {
    return null;
  }

  const initials = user.full_name
    .split(" ")
    .map((part) => part[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();

  function resetPasswordForm() {
    setCurrentPassword("");
    setNewPassword("");
    setConfirmNewPassword("");
    setShowCurrentPassword(false);
    setShowNewPassword(false);
  }

  function closeModal() {
    setIsOpen(false);
    setShowPasswordForm(false);
    setMessage("");
    setErrorMessage("");
    resetPasswordForm();
  }

  function validatePasswordForm() {
    if (!currentPassword) {
      return "Current password is required.";
    }

    if (newPassword.length < 8) {
      return "New password must have at least 8 characters.";
    }

    if (!/[a-z]/.test(newPassword)) {
      return "New password must contain at least one lowercase letter.";
    }

    if (!/[A-Z]/.test(newPassword)) {
      return "New password must contain at least one uppercase letter.";
    }

    if (!/\d/.test(newPassword)) {
      return "New password must contain at least one digit.";
    }

    if (!/[@$!%*?&]/.test(newPassword)) {
      return "New password must contain at least one special character: @$!%*?&.";
    }

    if (newPassword !== confirmNewPassword) {
      return "New password and confirmation do not match.";
    }

    if (currentPassword === newPassword) {
      return "New password must be different from current password.";
    }

    return "";
  }

  async function handleChangePassword() {
    setMessage("");
    setErrorMessage("");

    const validationMessage = validatePasswordForm();

    if (validationMessage) {
      setErrorMessage(validationMessage);
      return;
    }

    try {
      setIsChangingPassword(true);

      await changePassword({
        current_password: currentPassword,
        new_password: newPassword,
      });

      setMessage("Password changed successfully.");
      setShowPasswordForm(false);
      resetPasswordForm();
    } catch (error: any) {
      const detail = error.response?.data?.detail;
      setErrorMessage(detail || "Could not change password.");
    } finally {
      setIsChangingPassword(false);
    }
  }

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="flex h-11 w-11 items-center justify-center rounded-full bg-slate-900 text-sm font-bold text-white shadow-sm hover:bg-slate-800"
        title="User profile"
      >
        {initials || <User size={20} />}
      </button>

      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto bg-slate-950/40 px-4 py-8 backdrop-blur-sm">
          <div className="max-h-[90vh] w-full max-w-lg overflow-y-auto rounded-3xl border border-slate-200 bg-white shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-200 px-6 py-5">
              <div className="flex items-center gap-4">
                <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-slate-900 text-lg font-bold text-white">
                  {initials}
                </div>

                <div>
                  <h2 className="text-xl font-bold text-slate-950">
                    My Profile
                  </h2>
                  <p className="text-sm text-slate-500">
                    Account details and password settings.
                  </p>
                </div>
              </div>

              <button
                onClick={closeModal}
                className="rounded-xl p-2 text-slate-400 hover:bg-slate-100 hover:text-slate-700"
              >
                <X size={20} />
              </button>
            </div>

            <div className="space-y-5 px-6 py-6">
              <div className="grid gap-4 md:grid-cols-2">
                <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                  <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Full Name
                  </p>
                  <p className="mt-2 font-semibold text-slate-950">
                    {user.full_name}
                  </p>
                </div>

                <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                  <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Role
                  </p>
                  <p className="mt-2 font-semibold text-slate-950">
                    {user.role.name}
                  </p>
                </div>

                <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4 md:col-span-2">
                  <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Email
                  </p>
                  <p className="mt-2 font-semibold text-slate-950">
                    {user.email}
                  </p>
                </div>

                <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4 md:col-span-2">
                  <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Password
                  </p>
                  <div className="mt-2 flex items-center justify-between gap-4">
                    <p className="font-semibold tracking-[0.25em] text-slate-950">
                      ••••••••••••
                    </p>

                    <button
                      onClick={() => {
                        setShowPasswordForm((current) => !current);
                        setMessage("");
                        setErrorMessage("");
                      }}
                      className="flex items-center gap-2 rounded-xl bg-slate-950 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800"
                    >
                      <Lock size={16} />
                      Change Password
                    </button>
                  </div>
                </div>
              </div>

              {message && (
                <div className="rounded-xl bg-green-50 p-4 text-sm font-medium text-green-700">
                  {message}
                </div>
              )}

              {errorMessage && (
                <div className="rounded-xl bg-red-50 p-4 text-sm font-medium text-red-700">
                  {errorMessage}
                </div>
              )}

              {showPasswordForm && (
                <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
                  <h3 className="text-lg font-bold text-slate-950">
                    Change Password
                  </h3>
                  <p className="mt-1 text-sm text-slate-500">
                    Enter your current password and choose a new secure password.
                  </p>

                  <div className="mt-5 space-y-4">
                    <div>
                      <label className="text-sm font-medium text-slate-700">
                        Current Password
                      </label>

                      <div className="mt-2 flex rounded-xl border border-slate-300 bg-white focus-within:border-slate-900">
                        <input
                          value={currentPassword}
                          onChange={(event) =>
                            setCurrentPassword(event.target.value)
                          }
                          type={showCurrentPassword ? "text" : "password"}
                          className="min-w-0 flex-1 rounded-xl px-3 py-2 outline-none"
                        />

                        <button
                          type="button"
                          onClick={() =>
                            setShowCurrentPassword((current) => !current)
                          }
                          className="px-3 text-slate-400 hover:text-slate-700"
                        >
                          {showCurrentPassword ? (
                            <EyeOff size={18} />
                          ) : (
                            <Eye size={18} />
                          )}
                        </button>
                      </div>
                    </div>

                    <div>
                      <label className="text-sm font-medium text-slate-700">
                        New Password
                      </label>

                      <div className="mt-2 flex rounded-xl border border-slate-300 bg-white focus-within:border-slate-900">
                        <input
                          value={newPassword}
                          onChange={(event) =>
                            setNewPassword(event.target.value)
                          }
                          type={showNewPassword ? "text" : "password"}
                          className="min-w-0 flex-1 rounded-xl px-3 py-2 outline-none"
                        />

                        <button
                          type="button"
                          onClick={() =>
                            setShowNewPassword((current) => !current)
                          }
                          className="px-3 text-slate-400 hover:text-slate-700"
                        >
                          {showNewPassword ? (
                            <EyeOff size={18} />
                          ) : (
                            <Eye size={18} />
                          )}
                        </button>
                      </div>
                    </div>

                    <div>
                      <label className="text-sm font-medium text-slate-700">
                        Confirm New Password
                      </label>

                      <input
                        value={confirmNewPassword}
                        onChange={(event) =>
                          setConfirmNewPassword(event.target.value)
                        }
                        type="password"
                        className="mt-2 w-full rounded-xl border border-slate-300 px-3 py-2 outline-none focus:border-slate-900"
                      />
                    </div>

                    <p className="text-xs text-slate-500">
                      Password must include uppercase, lowercase, digit and one
                      special character: @$!%*?&.
                    </p>

                    <div className="flex justify-end gap-3">
                      <button
                        onClick={() => {
                          setShowPasswordForm(false);
                          setErrorMessage("");
                          resetPasswordForm();
                        }}
                        className="rounded-xl border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                      >
                        Cancel
                      </button>

                      <button
                        onClick={handleChangePassword}
                        disabled={isChangingPassword}
                        className="rounded-xl bg-slate-950 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800 disabled:opacity-50"
                      >
                        {isChangingPassword ? "Saving..." : "Save Password"}
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>

            <div className="flex justify-between border-t border-slate-200 bg-slate-50 px-6 py-4">
              <button
                onClick={logoutUser}
                className="flex items-center gap-2 rounded-xl px-4 py-2 text-sm font-semibold text-red-600 hover:bg-red-50"
              >
                <LogOut size={16} />
                Logout
              </button>

              <button
                onClick={closeModal}
                className="rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}