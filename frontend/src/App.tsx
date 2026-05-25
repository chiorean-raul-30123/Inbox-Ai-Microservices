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
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/inbox/finance"
            element={
              <ProtectedRoute>
                <FinanceInboxPage />
              </ProtectedRoute>
            }
          />
          
          <Route
            path="/inbox/legal"
            element={
              <ProtectedRoute>
                <LegalInboxPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/inbox/hr"
            element={
              <ProtectedRoute>
                <HrInboxPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/needs-review"
            element={
              <ProtectedRoute>
                <NeedsReviewPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/settings"
            element={
              <ProtectedRoute>
                <SettingsPage />
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

          <Route
            path="/todo"
            element={
              <ProtectedRoute>
                <ToDoPage />
              </ProtectedRoute>
            }
          />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}