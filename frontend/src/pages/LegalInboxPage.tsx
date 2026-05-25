import { fetchLegalInbox } from "../api/documentsApi";
import { MailAppShell } from "../components/mail/MailAppShell";

export function LegalInboxPage() {
  return (
    <MailAppShell
      title="Legal Inbox"
      departmentName="Legal"
      fetchDocuments={fetchLegalInbox}
    />
  );
}