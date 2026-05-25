import { fetchFinanceInbox } from "../api/documentsApi";
import { MailAppShell } from "../components/mail/MailAppShell";

export function FinanceInboxPage() {
  return (
    <MailAppShell
      title="Finance Inbox"
      departmentName="Finance"
      fetchDocuments={fetchFinanceInbox}
    />
  );
}