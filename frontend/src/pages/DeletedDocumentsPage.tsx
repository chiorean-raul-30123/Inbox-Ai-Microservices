import { fetchDeletedDocuments } from "../api/documentsApi";
import { MailAppShell } from "../components/mail/MailAppShell";

export function DeletedDocumentsPage() {
  return (
    <MailAppShell
      title="Deleted"
      departmentName="Deleted"
      fetchDocuments={fetchDeletedDocuments}
    />
  );
}