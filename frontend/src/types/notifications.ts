export type NotificationResponse = {
  id: string;
  title: string;
  message: string;
  status: string | null;
  target_department: string | null;
  document_id: string | null;
  correlation_id: string | null;
  is_read: boolean;
  created_at: string;
};

export type NotificationListResponse = {
  notifications: NotificationResponse[];
  unread_count: number;
};