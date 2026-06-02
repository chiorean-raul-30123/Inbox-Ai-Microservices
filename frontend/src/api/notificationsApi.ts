import { axiosClient } from "./axiosClient";
import type { NotificationListResponse, NotificationResponse } from "../types/notifications";

export async function fetchNotifications() {
  const response = await axiosClient.get<NotificationListResponse>(
    "/notifications",
  );

  return response.data;
}

export async function markNotificationAsRead(notificationId: string) {
  const response = await axiosClient.patch<NotificationResponse>(
    `/notifications/${notificationId}/read`,
  );

  return response.data;
}

export async function markAllNotificationsAsRead() {
  const response = await axiosClient.patch("/notifications/read-all");
  return response.data;
}