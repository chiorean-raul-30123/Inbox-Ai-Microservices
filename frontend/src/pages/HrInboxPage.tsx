import { fetchHrInbox } from "../api/documentsApi";
import { MailAppShell } from "../components/mail/MailAppShell";

export function HrInboxPage() {
  return (
    <MailAppShell
      title="HR Inbox"
      departmentName="HR"
      fetchDocuments={fetchHrInbox}
    />
  );
}