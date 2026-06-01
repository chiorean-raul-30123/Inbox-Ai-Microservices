import { useEffect, useMemo, useState } from "react";
import {
  CheckCircle2,
  Download,
  ExternalLink,
  FileText,
  Gauge,
  Inbox,
  RefreshCw,
  Search,
  Send,
  Tag,
} from "lucide-react";

import {
  fetchDocumentDownloadUrl,
  fetchNeedsReviewDocuments,
  reviewDocument,
} from "../api/documentsApi";
import { MailList } from "../components/mail/MailList";
import type {
  DocumentLabel,
  DocumentListItemResponse,
} from "../types/documents";
import { Layout } from "../components/Layout";

function formatConfidence(value: number | null) {
  if (value === null) return "-";
  return `${(value * 100).toFixed(1)}%`;
}

function getConfidenceWidth(value: number | null) {
  if (value === null) return "0%";
  return `${Math.min(100, Math.max(0, value * 100))}%`;
}

const routingOptions: { label: string; value: DocumentLabel }[] = [
  { label: "HR Inbox", value: "HR" },
  { label: "Finance Inbox", value: "FINANCE" },
  { label: "Legal Inbox", value: "LEGAL" },
];

export function NeedsReviewPage() {
  const [documents, setDocuments] = useState<DocumentListItemResponse[]>([]);
  const [selectedDocument, setSelectedDocument] =
    useState<DocumentListItemResponse | null>(null);

  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);
  const [selectedLabel, setSelectedLabel] = useState<DocumentLabel>("HR");

  const [searchValue, setSearchValue] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [isLoadingUrl, setIsLoadingUrl] = useState(false);
  const [isRouting, setIsRouting] = useState(false);

  const [message, setMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  async function loadNeedsReviewDocuments(isManualRefresh = false) {
    try {
      setErrorMessage("");

      if (isManualRefresh) {
        setIsRefreshing(true);
      } else {
        setIsLoading(true);
      }

      const data = await fetchNeedsReviewDocuments();
      setDocuments(data);

      if (data.length > 0) {
        setSelectedDocument((current) => {
          if (!current) return data[0];
          return data.find((item) => item.id === current.id) ?? data[0];
        });
      } else {
        setSelectedDocument(null);
      }
    } catch {
      setErrorMessage("Could not load needs review documents.");
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  }

  async function loadDownloadUrl(documentId: string) {
    try {
      setIsLoadingUrl(true);
      setDownloadUrl(null);

      const data = await fetchDocumentDownloadUrl(documentId);
      setDownloadUrl(data.downloadUrl);
    } catch {
      setDownloadUrl(null);
    } finally {
      setIsLoadingUrl(false);
    }
  }

  async function handleRouteDocument() {
    if (!selectedDocument) return;

    try {
      setIsRouting(true);
      setMessage("");
      setErrorMessage("");

      await reviewDocument(selectedDocument.id, {
        final_label: selectedLabel,
      });

      setDocuments((currentDocuments) => {
        const nextDocuments = currentDocuments.filter(
          (document) => document.id !== selectedDocument.id
        );

        setSelectedDocument(nextDocuments[0] ?? null);

        return nextDocuments;
      });

      setMessage(`Document routed to ${selectedLabel} inbox.`);
    } catch (error: any) {
      const detail = error.response?.data?.detail;
      setErrorMessage(detail || "Could not route document.");
    } finally {
      setIsRouting(false);
    }
  }

  useEffect(() => {
    loadNeedsReviewDocuments();
  }, []);

  useEffect(() => {
    setDownloadUrl(null);

    if (selectedDocument) {
      loadDownloadUrl(selectedDocument.id);

      if (selectedDocument.predicted_label) {
        setSelectedLabel(selectedDocument.predicted_label);
      } else {
        setSelectedLabel("HR");
      }
    }
  }, [selectedDocument?.id]);

  const filteredDocuments = useMemo(() => {
    const value = searchValue.trim().toLowerCase();

    if (!value) {
      return documents;
    }

    return documents.filter((document) => {
      return (
        document.original_filename.toLowerCase().includes(value) ||
        document.status.toLowerCase().includes(value) ||
        document.predicted_label?.toLowerCase().includes(value) ||
        document.incoming_email?.subject.toLowerCase().includes(value) ||
        document.incoming_email?.sender_email.toLowerCase().includes(value)
      );
    });
  }, [documents, searchValue]);

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#f3f6fb]">
        <div className="rounded-2xl bg-white px-8 py-6 shadow-sm">
          <p className="text-sm font-medium text-slate-600">
            Loading needs review documents...
          </p>
        </div>
      </div>
    );
  }

  return (
    <Layout>
      <div className="flex h-[calc(100vh-8rem)] overflow-hidden rounded-3xl border border-slate-200 bg-[#f3f6fb] shadow-sm">
        <div className="flex min-w-0 flex-1 flex-col">
          <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-6">
            <div>
              <h1 className="text-lg font-bold text-slate-950">Needs Review</h1>
              <p className="text-sm text-slate-500">
                Manually validate low-confidence documents.
              </p>
            </div>

            <div className="flex items-center gap-3">
              <div className="relative hidden md:block">
                <Search
                  size={17}
                  className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
                />
                <input
                  value={searchValue}
                  onChange={(event) => setSearchValue(event.target.value)}
                  placeholder="Search documents"
                  className="h-10 w-72 rounded-xl border border-slate-200 bg-slate-50 pl-9 pr-3 text-sm outline-none transition focus:border-blue-500 focus:bg-white"
                />
              </div>

              <button
                onClick={() => loadNeedsReviewDocuments(true)}
                className="flex h-10 items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 text-sm font-medium text-slate-700 hover:bg-slate-50"
              >
                <RefreshCw
                  size={16}
                  className={isRefreshing ? "animate-spin" : ""}
                />
                Refresh
              </button>
            </div>
          </header>

          {message && (
            <div className="border-b border-green-100 bg-green-50 px-6 py-3 text-sm font-medium text-green-700">
              {message}
            </div>
          )}

          {errorMessage && (
            <div className="border-b border-red-100 bg-red-50 px-6 py-3 text-sm font-medium text-red-700">
              {errorMessage}
            </div>
          )}

          <div className="flex min-h-0 flex-1">
            <MailList
              documents={filteredDocuments}
              selectedDocumentId={selectedDocument?.id ?? null}
              searchValue={searchValue}
              onSelectDocument={setSelectedDocument}
            />

            {!selectedDocument ? (
              <section className="flex min-w-0 flex-1 items-center justify-center bg-[#f8fafc] p-6">
                <div className="max-w-sm text-center">
                  <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-3xl bg-white shadow-sm">
                    <FileText className="text-slate-300" size={42} />
                  </div>
                  <p className="mt-5 text-lg font-semibold text-slate-800">
                    No document selected
                  </p>
                  <p className="mt-1 text-sm text-slate-500">
                    Select a document to preview and route it manually.
                  </p>
                </div>
              </section>
            ) : (
              <section className="min-w-0 flex-1 overflow-y-auto bg-[#f8fafc] p-4 md:p-6">
                <div className="mx-auto max-w-6xl overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
                  <div className="border-b border-slate-200 px-6 py-5 md:px-8 md:py-6">
                    <div className="flex flex-wrap items-start justify-between gap-4">
                      <div className="min-w-0">
                        <p className="flex items-center gap-2 text-sm font-semibold text-amber-600">
                          <Inbox size={16} />
                          Needs Review
                        </p>

                        <h1 className="mt-3 break-words text-2xl font-bold text-slate-950">
                          {selectedDocument.incoming_email?.subject ??
                            selectedDocument.original_filename}
                        </h1>

                        <div className="mt-4 grid gap-1 text-sm text-slate-600">
                          <p>
                            <span className="font-semibold text-slate-900">
                              From:
                            </span>{" "}
                            <span className="font-medium text-slate-800">
                              {selectedDocument.incoming_email?.sender_name ??
                                "AI Document Router"}
                            </span>
                            {selectedDocument.incoming_email?.sender_email && (
                              <span className="text-slate-500">
                                {" "}
                                &lt;{selectedDocument.incoming_email.sender_email}
                                &gt;
                              </span>
                            )}
                          </p>

                          <p>
                            <span className="font-semibold text-slate-900">
                              Received:
                            </span>{" "}
                            {new Date(
                              selectedDocument.incoming_email?.received_at ??
                                selectedDocument.created_at
                            ).toLocaleString()}
                          </p>
                        </div>
                      </div>

                      <span className="rounded-full bg-amber-50 px-4 py-2 text-sm font-semibold text-amber-700 ring-1 ring-amber-100">
                        {selectedDocument.status}
                      </span>
                    </div>
                  </div>

                  {selectedDocument.incoming_email?.body && (
                    <div className="border-b border-slate-200 px-6 py-6 md:px-8">
                      <p className="whitespace-pre-line text-sm leading-7 text-slate-700">
                        {selectedDocument.incoming_email.body}
                      </p>
                    </div>
                  )}

                  <div className="grid gap-4 border-b border-slate-200 bg-slate-50 px-6 py-5 md:grid-cols-3 md:px-8">
                    <div className="rounded-2xl bg-white p-4 shadow-sm">
                      <div className="flex items-center gap-2 text-xs font-semibold uppercase text-slate-500">
                        <Tag size={15} />
                        Predicted Label
                      </div>
                      <p className="mt-2 text-xl font-bold text-slate-950">
                        {selectedDocument.predicted_label ?? "-"}
                      </p>
                    </div>

                    <div className="rounded-2xl bg-white p-4 shadow-sm">
                      <div className="flex items-center gap-2 text-xs font-semibold uppercase text-slate-500">
                        <Gauge size={15} />
                        Confidence
                      </div>
                      <p className="mt-2 text-xl font-bold text-slate-950">
                        {formatConfidence(selectedDocument.confidence_score)}
                      </p>

                      <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-100">
                        <div
                          className="h-full rounded-full bg-amber-500 transition-all duration-500"
                          style={{
                            width: getConfidenceWidth(
                              selectedDocument.confidence_score
                            ),
                          }}
                        />
                      </div>
                    </div>

                    <div className="rounded-2xl bg-white p-4 shadow-sm">
                      <div className="flex items-center gap-2 text-xs font-semibold uppercase text-slate-500">
                        <CheckCircle2 size={15} />
                        Current Department
                      </div>
                      <p className="mt-2 text-xl font-bold text-slate-950">
                        {selectedDocument.department ?? "NEEDS_REVIEW"}
                      </p>
                    </div>
                  </div>

                  <div className="border-b border-slate-200 bg-white px-6 py-5 md:px-8">
                    <div className="flex flex-col gap-4 rounded-2xl border border-amber-100 bg-amber-50 p-4 md:flex-row md:items-end md:justify-between">
                      <div>
                        <label className="text-sm font-semibold text-slate-900">
                          Route document to
                        </label>

                        <select
                          value={selectedLabel}
                          onChange={(event) =>
                            setSelectedLabel(event.target.value as DocumentLabel)
                          }
                          className="mt-2 w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-800 outline-none focus:border-slate-900 md:w-72"
                        >
                          {routingOptions.map((option) => (
                            <option key={option.value} value={option.value}>
                              {option.label}
                            </option>
                          ))}
                        </select>

                        <p className="mt-2 text-sm text-slate-600">
                          This will mark the document as reviewed and send it to
                          the selected department inbox.
                        </p>
                      </div>

                      <button
                        onClick={handleRouteDocument}
                        disabled={isRouting}
                        className="flex items-center justify-center gap-2 rounded-xl bg-slate-950 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-600 disabled:opacity-50"
                      >
                        <Send size={16} />
                        {isRouting ? "Routing..." : "Route Document"}
                      </button>
                    </div>
                  </div>

                  <div className="p-5 md:p-8">
                    <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4 md:p-5">
                      <div className="flex flex-wrap items-center justify-between gap-4">
                        <div className="flex min-w-0 items-center gap-3">
                          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-red-50">
                            <FileText className="text-red-600" size={28} />
                          </div>

                          <div className="min-w-0">
                            <p className="truncate font-semibold text-slate-950">
                              {selectedDocument.original_filename}
                            </p>
                            <p className="text-sm text-slate-500">
                              PDF attachment •{" "}
                              {(selectedDocument.file_size / 1024).toFixed(1)} KB
                            </p>
                          </div>
                        </div>

                        {downloadUrl && (
                          <div className="flex gap-2">
                            <a
                              href={downloadUrl}
                              target="_blank"
                              rel="noreferrer"
                              className="flex items-center gap-2 rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
                            >
                              <ExternalLink size={16} />
                              Open
                            </a>

                            <a
                              href={downloadUrl}
                              download
                              className="flex items-center gap-2 rounded-xl bg-slate-950 px-4 py-2 text-sm font-semibold text-white transition hover:bg-blue-600"
                            >
                              <Download size={16} />
                              Download
                            </a>
                          </div>
                        )}
                      </div>

                      <div className="mt-5 overflow-hidden rounded-2xl border border-slate-200 bg-white">
                        {isLoadingUrl && (
                          <div className="p-6 text-sm text-slate-500">
                            Loading PDF preview...
                          </div>
                        )}

                        {!isLoadingUrl && downloadUrl && (
                          <iframe
                            src={downloadUrl}
                            title={selectedDocument.original_filename}
                            className="h-[520px] w-full md:h-[650px]"
                          />
                        )}

                        {!isLoadingUrl && !downloadUrl && (
                          <div className="p-6 text-sm text-red-600">
                            Could not load PDF preview.
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </section>
            )}
          </div>
        </div>
      </div>
    </Layout>
  );
}