export type AuditResponse = {
  id: string;

  action: string;

  user_id: string | null;

  document_id: string | null;

  details: Record<string, any> | null;

  created_at: string;
};