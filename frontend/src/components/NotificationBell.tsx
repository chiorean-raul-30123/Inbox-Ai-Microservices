import { useEffect, useState } from "react";
import { Bell, CheckCheck, FileText, ShieldAlert, X } from "lucide-react";

import {
  fetchNotifications,
  markAllNotificationsAsRead,
  markNotificationAsRead,
} from "../api/notificationsApi";
import type { NotificationResponse } from "../types/notifications";

function getNotificationIcon(notification: NotificationResponse) {
  if (notification.status?.includes("FAILED")) {
    return <ShieldAlert size={18} className="text-red-600" />;
  }

  return <FileText size={18} className="text-blue-600" />;
}

function formatTime(value: string) {
  return new Date(value).toLocaleString();
}

export function NotificationBell() {
  const [notifications, setNotifications] = useState<NotificationResponse[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [isOpen, setIsOpen] = useState(false);

  async function loadNotifications() {
    try {
      const data = await fetchNotifications();
      setNotifications(data.notifications);
      setUnreadCount(data.unread_count);
    } catch {
      setNotifications([]);
      setUnreadCount(0);
    }
  }

  async function handleOpen() {
    setIsOpen(true);
    await loadNotifications();
  }

  async function handleMarkAsRead(notification: NotificationResponse) {
    if (notification.is_read) {
      return;
    }

    const updatedNotification = await markNotificationAsRead(notification.id);

    setNotifications((current) =>
      current.map((item) =>
        item.id === updatedNotification.id ? updatedNotification : item,
      ),
    );

    setUnreadCount((current) => Math.max(0, current - 1));
  }

  async function handleMarkAllAsRead() {
    await markAllNotificationsAsRead();

    setNotifications((current) =>
      current.map((item) => ({
        ...item,
        is_read: true,
      })),
    );

    setUnreadCount(0);
  }

  useEffect(() => {
    loadNotifications();

    const intervalId = window.setInterval(loadNotifications, 30000);

    return () => window.clearInterval(intervalId);
  }, []);

  return (
    <>
      <button
        onClick={handleOpen}
        className="relative flex h-11 w-11 items-center justify-center rounded-full border border-slate-200 bg-white text-slate-700 shadow-sm hover:bg-slate-50"
        title="Notifications"
      >
        <Bell size={20} />

        {unreadCount > 0 && (
          <span className="absolute -right-1 -top-1 flex h-5 min-w-5 items-center justify-center rounded-full bg-red-600 px-1 text-xs font-bold text-white">
            {unreadCount > 9 ? "9+" : unreadCount}
          </span>
        )}
      </button>

      {isOpen && (
        <div className="fixed inset-0 z-50 bg-slate-950/30 backdrop-blur-sm">
          <div className="absolute right-0 top-0 flex h-full w-full max-w-md flex-col bg-white shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-200 px-6 py-5">
              <div>
                <h2 className="text-xl font-bold text-slate-950">
                  Notifications
                </h2>
                <p className="text-sm text-slate-500">
                  {unreadCount} unread notification{unreadCount === 1 ? "" : "s"}.
                </p>
              </div>

              <button
                onClick={() => setIsOpen(false)}
                className="rounded-xl p-2 text-slate-400 hover:bg-slate-100 hover:text-slate-700"
              >
                <X size={20} />
              </button>
            </div>

            <div className="flex items-center justify-between border-b border-slate-100 px-6 py-3">
              <p className="text-sm font-medium text-slate-600">
                Latest activity
              </p>

              <button
                onClick={handleMarkAllAsRead}
                disabled={unreadCount === 0}
                className="flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100 disabled:opacity-40"
              >
                <CheckCheck size={16} />
                Mark all read
              </button>
            </div>

            <div className="min-h-0 flex-1 overflow-y-auto p-3">
              {notifications.length === 0 ? (
                <div className="flex h-full items-center justify-center text-center">
                  <div>
                    <Bell className="mx-auto text-slate-300" size={42} />
                    <p className="mt-4 font-semibold text-slate-800">
                      No notifications
                    </p>
                    <p className="mt-1 text-sm text-slate-500">
                      Document events will appear here.
                    </p>
                  </div>
                </div>
              ) : (
                notifications.map((notification) => (
                  <button
                    key={notification.id}
                    onClick={() => handleMarkAsRead(notification)}
                    className={`mb-2 w-full rounded-2xl border p-4 text-left transition hover:bg-slate-50 ${
                      notification.is_read
                        ? "border-slate-100 bg-white"
                        : "border-blue-100 bg-blue-50"
                    }`}
                  >
                    <div className="flex gap-3">
                      <div className="mt-1 flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-white shadow-sm">
                        {getNotificationIcon(notification)}
                      </div>

                      <div className="min-w-0 flex-1">
                        <div className="flex items-start justify-between gap-3">
                          <p className="font-semibold text-slate-950">
                            {notification.title}
                          </p>

                          {!notification.is_read && (
                            <span className="mt-1 h-2 w-2 shrink-0 rounded-full bg-blue-600" />
                          )}
                        </div>

                        <p className="mt-1 text-sm leading-6 text-slate-600">
                          {notification.message}
                        </p>

                        <div className="mt-3 flex flex-wrap gap-2 text-xs">
                          {notification.target_department && (
                            <span className="rounded-full bg-slate-100 px-2.5 py-1 font-semibold text-slate-600">
                              {notification.target_department}
                            </span>
                          )}

                          {notification.status && (
                            <span className="rounded-full bg-slate-100 px-2.5 py-1 font-semibold text-slate-600">
                              {notification.status}
                            </span>
                          )}
                        </div>

                        <p className="mt-3 text-xs text-slate-400">
                          {formatTime(notification.created_at)}
                        </p>
                      </div>
                    </div>
                  </button>
                ))
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}