import { useEffect, useMemo, useState } from "react";
import {
  AlertTriangle,
  CheckCircle2,
  Clock3,
  FileText,
  History,
  Search,
  Shield,
  User,
} from "lucide-react";

import { fetchAuditLogs } from "../api/auditApi";
import { Layout } from "../components/Layout";
import type { AuditResponse } from "../types/audit";

function getActionStyle(action: string) {
  if (
    action.includes("FAILED")
  ) {
    return "bg-red-50 text-red-700 border-red-100";
  }

  if (
    action.includes("REVIEW")
  ) {
    return "bg-amber-50 text-amber-700 border-amber-100";
  }

  if (
    action.includes("ROUTED")
  ) {
    return "bg-green-50 text-green-700 border-green-100";
  }

  if (
    action.includes("UPLOADED") ||
    action.includes("RECEIVED")
  ) {
    return "bg-blue-50 text-blue-700 border-blue-100";
  }

  return "bg-slate-50 text-slate-700 border-slate-200";
}

function getActionIcon(action: string) {
  if (
    action.includes("FAILED")
  ) {
    return (
      <AlertTriangle
        size={16}
        className="text-red-600"
      />
    );
  }

  if (
    action.includes("REVIEW")
  ) {
    return (
      <Shield
        size={16}
        className="text-amber-600"
      />
    );
  }

  if (
    action.includes("ROUTED")
  ) {
    return (
      <CheckCircle2
        size={16}
        className="text-green-600"
      />
    );
  }

  return (
    <FileText
      size={16}
      className="text-blue-600"
    />
  );
}

function formatActionLabel(action: string) {
  return action
    .split("_")
    .join(" ")
    .toLowerCase()
    .replace(
      /\b\w/g,
      (char) => char.toUpperCase()
    );
}

export function AuditCenterPage() {
  const [logs, setLogs] = useState<AuditResponse[]>([]);
  const [searchValue, setSearchValue] = useState("");
  const [selectedLog, setSelectedLog] =
    useState<AuditResponse | null>(null);

  const [isLoading, setIsLoading] =
    useState(true);

  const [errorMessage, setErrorMessage] =
    useState("");

  async function loadAuditLogs() {
    try {
      const data =
        await fetchAuditLogs();

      setLogs(data);

      if (data.length > 0) {
        setSelectedLog(data[0]);
      }
    } catch {
      setErrorMessage(
        "Could not load audit logs."
      );
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    loadAuditLogs();
  }, []);

  const filteredLogs = useMemo(() => {
    const value =
      searchValue.trim().toLowerCase();

    if (!value) {
      return logs;
    }

    return logs.filter((log) => {
      return (
        log.action
          .toLowerCase()
          .includes(value) ||
        log.document_id
          ?.toLowerCase()
          .includes(value) ||
        JSON.stringify(log.details)
          .toLowerCase()
          .includes(value)
      );
    });
  }, [logs, searchValue]);

  if (isLoading) {
    return (
      <Layout>
        <p className="text-slate-600">
          Loading audit logs...
        </p>
      </Layout>
    );
  }

  if (errorMessage) {
    return (
      <Layout>
        <div className="rounded-xl bg-red-50 p-4 text-red-700">
          {errorMessage}
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div>
        <h1 className="text-3xl font-bold text-slate-900">
          Audit & Compliance Center
        </h1>

        <p className="mt-2 text-slate-500">
          Complete activity history across
          users, documents and AI workflows.
        </p>
      </div>

      <div className="mt-8 flex h-[calc(100vh-14rem)] min-w-0 overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
        <section className="flex w-[420px] shrink-0 flex-col border-r border-slate-200">
          <div className="border-b border-slate-200 p-5">
            <div className="relative">
              <Search
                size={16}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
              />

              <input
                value={searchValue}
                onChange={(event) =>
                  setSearchValue(
                    event.target.value
                  )
                }
                placeholder="Search audit logs"
                className="w-full rounded-xl border border-slate-300 py-2 pl-9 pr-3 text-sm outline-none focus:border-slate-900"
              />
            </div>
          </div>

          <div className="flex-1 overflow-y-auto p-2">
            {filteredLogs.map((log) => {
              const isSelected =
                selectedLog?.id === log.id;

              return (
                <button
                  key={log.id}
                  onClick={() =>
                    setSelectedLog(log)
                  }
                  className={`mb-2 w-full rounded-2xl border p-4 text-left transition ${
                    isSelected
                      ? "border-blue-100 bg-blue-50"
                      : "border-transparent hover:border-slate-200 hover:bg-slate-50"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      {getActionIcon(
                        log.action
                      )}

                      <span className="font-semibold text-slate-900">
                        {formatActionLabel(
                          log.action
                        )}
                      </span>
                    </div>

                    <Clock3
                      size={14}
                      className="text-slate-400"
                    />
                  </div>

                  <div
                    className={`mt-3 inline-flex rounded-full border px-3 py-1 text-xs font-semibold ${getActionStyle(
                      log.action
                    )}`}
                  >
                    {log.action}
                  </div>

                  <p className="mt-3 text-xs text-slate-500">
                    {new Date(
                      log.created_at
                    ).toLocaleString()}
                  </p>
                </button>
              );
            })}
          </div>
        </section>

        <section className="min-w-0 flex-1 overflow-y-auto p-8">
          {!selectedLog ? (
            <div className="flex h-full items-center justify-center text-slate-500">
              Select an audit entry.
            </div>
          ) : (
            <>
              <div className="flex items-center gap-3">
                {getActionIcon(
                  selectedLog.action
                )}

                <h2 className="text-2xl font-bold text-slate-900">
                  {formatActionLabel(
                    selectedLog.action
                  )}
                </h2>
              </div>

              <div className="mt-6 grid gap-5 md:grid-cols-2">
                <div className="rounded-2xl bg-slate-50 p-5">
                  <p className="text-xs font-semibold uppercase text-slate-500">
                    Action
                  </p>

                  <p className="mt-2 font-semibold text-slate-900">
                    {selectedLog.action}
                  </p>
                </div>

                <div className="rounded-2xl bg-slate-50 p-5">
                  <p className="text-xs font-semibold uppercase text-slate-500">
                    Timestamp
                  </p>

                  <p className="mt-2 font-semibold text-slate-900">
                    {new Date(
                      selectedLog.created_at
                    ).toLocaleString()}
                  </p>
                </div>

                <div className="rounded-2xl bg-slate-50 p-5">
                  <div className="flex items-center gap-2">
                    <User size={16} />

                    <p className="text-xs font-semibold uppercase text-slate-500">
                      User
                    </p>
                  </div>

                  <p className="mt-2 break-all font-mono text-sm text-slate-900">
                    {selectedLog.user_id ??
                      "System"}
                  </p>
                </div>

                <div className="rounded-2xl bg-slate-50 p-5">
                  <div className="flex items-center gap-2">
                    <History size={16} />

                    <p className="text-xs font-semibold uppercase text-slate-500">
                      Document
                    </p>
                  </div>

                  <p className="mt-2 break-all font-mono text-sm text-slate-900">
                    {selectedLog.document_id ??
                      "N/A"}
                  </p>
                </div>
              </div>

              <div className="mt-8">
                <h3 className="text-lg font-bold text-slate-900">
                  Event Details
                </h3>

                <div className="mt-4 max-w-full overflow-x-auto rounded-2xl border border-slate-200 bg-slate-50 p-5">
                    <pre className="whitespace-pre-wrap break-words text-sm text-slate-800">
                    {JSON.stringify(
                      selectedLog.details,
                      null,
                      2
                    )}
                  </pre>
                </div>
              </div>
            </>
          )}
        </section>
      </div>
    </Layout>
  );
}