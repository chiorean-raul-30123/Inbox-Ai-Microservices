import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import { AuthProvider } from "./auth/AuthContext";
import { ProtectedRoute } from "./auth/ProtectedRoute";
import { DashboardPage } from "./pages/DashboardPage";
import { LoginPage } from "./pages/LoginPage";
import { NeedsReviewPage } from "./pages/NeedsReviewPage";
import { SettingsPage } from "./pages/SettingsPage";
import { HrInboxPage } from "./pages/HrInboxPage";
import { FinanceInboxPage } from "./pages/FinanceInboxPage";
import { LegalInboxPage } from "./pages/LegalInboxPage";
import { InboxRedirectPage } from "./pages/InboxRedirectPage";
import { PlaceholderPage } from "./pages/PlaceholderPage";
import { ClientSubmitPage } from "./pages/ClientSubmitPage";
import { DeletedDocumentsPage } from "./pages/DeletedDocumentsPage";
import { CalendarPage } from "./pages/CalendarPage";
import { ToDoPage } from "./pages/ToDoPage";
import { UploadPage } from "./pages/UploadPage";
import { AdminUsersPage } from "./pages/AdminUsersPage";
import { OperationsCenterPage } from "./pages/OperationsCenterPage";
import { AuditCenterPage } from "./pages/AuditCenterPage";


export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/client-submit" element={<ClientSubmitPage />} />

          <Route
            path="/"
            element={
              <ProtectedRoute allowedRoles={["ADMIN"]}>
                <DashboardPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/upload"
            element={
              <ProtectedRoute allowedRoles={["ADMIN"]}>
                <UploadPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/needs-review"
            element={
              <ProtectedRoute allowedRoles={["ADMIN"]}>
                <NeedsReviewPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/admin/users"
            element={
              <ProtectedRoute allowedRoles={["ADMIN"]}>
                <AdminUsersPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/system-health"
            element={
              <ProtectedRoute allowedRoles={["ADMIN"]}>
                <OperationsCenterPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/audit"
            element={
              <ProtectedRoute allowedRoles={["ADMIN"]}>
                <AuditCenterPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/settings"
            element={
              <ProtectedRoute allowedRoles={["ADMIN"]}>
                <SettingsPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/inbox/hr"
            element={
              <ProtectedRoute allowedRoles={["ADMIN", "HR"]}>
                <HrInboxPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/inbox/finance"
            element={
              <ProtectedRoute allowedRoles={["ADMIN", "FINANCE"]}>
                <FinanceInboxPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/inbox/legal"
            element={
              <ProtectedRoute allowedRoles={["ADMIN", "LEGAL"]}>
                <LegalInboxPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/inbox"
            element={
              <ProtectedRoute>
                <InboxRedirectPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/calendar"
            element={
              <ProtectedRoute>
                <CalendarPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/deleted"
            element={
              <ProtectedRoute>
                <DeletedDocumentsPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/todo"
            element={
              <ProtectedRoute>
                <ToDoPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/spam"
            element={
              <ProtectedRoute>
                <PlaceholderPage
                  title="Spam"
                  description="Suspicious or ignored messages."
                  activeSection="spam"
                  icon="spam"
                />
              </ProtectedRoute>
            }
          />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}