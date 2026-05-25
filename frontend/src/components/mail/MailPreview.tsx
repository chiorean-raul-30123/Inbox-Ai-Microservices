import { useEffect, useState } from "react";
import {
  CheckCircle2,
  Download,
  ExternalLink,
  FileText,
  Gauge,
  Inbox,
  Tag,
} from "lucide-react";

import { fetchDocumentDownloadUrl } from "../../api/documentsApi";
import type { DocumentListItemResponse } from "../../types/documents";

type MailPreviewProps = {
  document: DocumentListItemResponse | null;
  departmentName: string;
};

function formatConfidence(value: number | null) {
  if (value === null) return "-";
  return `${(value * 100).toFixed(1)}%`;
}

function getConfidenceWidth(value: number | null) {
  if (value === null) return "0%";
  return `${Math.min(100, Math.max(0, value * 100))}%`;
}

export function MailPreview({ document, departmentName }: MailPreviewProps) {
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);
  const [isLoadingUrl, setIsLoadingUrl] = useState(false);

  async function loadDownloadUrl(documentId: string) {
    try {
      setIsLoadingUrl(true);
      const data = await fetchDocumentDownloadUrl(documentId);
      setDownloadUrl(data.downloadUrl);
    } catch {
      setDownloadUrl(null);
    } finally {
      setIsLoadingUrl(false);
    }
  }

  useEffect(() => {
    setDownloadUrl(null);

    if (document) {
      loadDownloadUrl(document.id);
    }
  }, [document?.id]);

  if (!document) {
    return (
      <section className="flex min-w-0 flex-1 items-center justify-center bg-[#f8fafc] p-6">
        <div className="max-w-sm text-center">
          <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-3xl bg-white shadow-sm transition hover:-translate-y-1 hover:shadow-md">
            <FileText className="text-slate-300" size={42} />
          </div>
          <p className="mt-5 text-lg font-semibold text-slate-800">
            Select a document to preview
          </p>
          <p className="mt-1 text-sm text-slate-500">
            Routed documents will open in the reading pane.
          </p>
        </div>
      </section>
    );
  }

  return (
    <section className="min-w-0 flex-1 overflow-y-auto bg-[#f8fafc] p-4 md:p-6">
      <div className="mx-auto max-w-6xl overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm transition-all duration-200">
        <div className="border-b border-slate-200 px-6 py-5 md:px-8 md:py-6">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div className="min-w-0">
              <p className="flex items-center gap-2 text-sm font-semibold text-blue-600">
                <Inbox size={16} />
                {departmentName} Inbox
              </p>

              <h1 className="mt-3 break-words text-2xl font-bold text-slate-950">
                {document.original_filename}
              </h1>

              <div className="mt-4 grid gap-1 text-sm text-slate-600">
                <p>
                  <span className="font-semibold text-slate-900">From:</span>{" "}
                  AI Document Router
                </p>
                <p>
                  <span className="font-semibold text-slate-900">To:</span>{" "}
                  {departmentName} Department
                </p>
                <p>
                  <span className="font-semibold text-slate-900">Received:</span>{" "}
                  {new Date(document.created_at).toLocaleString()}
                </p>
              </div>
            </div>

            <span className="rounded-full bg-emerald-50 px-4 py-2 text-sm font-semibold text-emerald-700 ring-1 ring-emerald-100">
              {document.status}
            </span>
          </div>
        </div>

        <div className="grid gap-4 border-b border-slate-200 bg-slate-50 px-6 py-5 md:grid-cols-3 md:px-8">
          <div className="rounded-2xl bg-white p-4 shadow-sm transition duration-200 hover:-translate-y-0.5 hover:shadow-md">
            <div className="flex items-center gap-2 text-xs font-semibold uppercase text-slate-500">
              <Tag size={15} />
              Predicted Label
            </div>
            <p className="mt-2 text-xl font-bold text-slate-950">
              {document.predicted_label ?? "-"}
            </p>
          </div>

          <div className="rounded-2xl bg-white p-4 shadow-sm transition duration-200 hover:-translate-y-0.5 hover:shadow-md">
            <div className="flex items-center gap-2 text-xs font-semibold uppercase text-slate-500">
              <Gauge size={15} />
              Confidence
            </div>
            <p className="mt-2 text-xl font-bold text-slate-950">
              {formatConfidence(document.confidence_score)}
            </p>

            <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-100">
              <div
                className="h-full rounded-full bg-blue-600 transition-all duration-500"
                style={{ width: getConfidenceWidth(document.confidence_score) }}
              />
            </div>
          </div>

          <div className="rounded-2xl bg-white p-4 shadow-sm transition duration-200 hover:-translate-y-0.5 hover:shadow-md">
            <div className="flex items-center gap-2 text-xs font-semibold uppercase text-slate-500">
              <CheckCircle2 size={15} />
              Department
            </div>
            <p className="mt-2 text-xl font-bold text-slate-950">
              {document.department ?? departmentName}
            </p>
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
                    {document.original_filename}
                  </p>
                  <p className="text-sm text-slate-500">
                    PDF attachment • {(document.file_size / 1024).toFixed(1)} KB
                  </p>
                </div>
              </div>

              {downloadUrl && (
                <div className="flex gap-2">
                  <a
                    href={downloadUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center gap-2 rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:-translate-y-0.5 hover:bg-slate-50 hover:shadow-sm"
                  >
                    <ExternalLink size={16} />
                    Open
                  </a>

                  <a
                    href={downloadUrl}
                    download
                    className="flex items-center gap-2 rounded-xl bg-slate-950 px-4 py-2 text-sm font-semibold text-white transition hover:-translate-y-0.5 hover:bg-blue-600 hover:shadow-sm"
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
                  title={document.original_filename}
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
  );
}