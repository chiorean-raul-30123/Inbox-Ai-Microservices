import { Navigate } from "react-router-dom";

import { useAuth } from "../auth/AuthContext";

export function InboxRedirectPage() {
  const { user } = useAuth();

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (user.role.name === "HR") {
    return <Navigate to="/inbox/hr" replace />;
  }

  if (user.role.name === "FINANCE") {
    return <Navigate to="/inbox/finance" replace />;
  }

  if (user.role.name === "LEGAL") {
    return <Navigate to="/inbox/legal" replace />;
  }

  return <Navigate to="/" replace />;
}