import { FileText, Trash2 } from "lucide-react";

import type { DocumentListItemResponse } from "../../types/documents";

type MailListProps = {
  documents: DocumentListItemResponse[];
  selectedDocumentId: string | null;
  searchValue: string;
  onSelectDocument: (document: DocumentListItemResponse) => void;
  onDeleteDocument?: (document: DocumentListItemResponse) => void;
};

function formatConfidence(value: number | null) {
  if (value === null) return "Unknown confidence";
  return `${(value * 100).toFixed(1)}% confidence`;
}

function getStatusStyle(status: string) {
  if (status === "ROUTED") return "bg-emerald-50 text-emerald-700 ring-emerald-100";
  if (status === "NEEDS_REVIEW") return "bg-amber-50 text-amber-700 ring-amber-100";
  if (status === "DELETED") return "bg-slate-100 text-slate-600 ring-slate-200";
  if (status.includes("FAILED")) return "bg-red-50 text-red-700 ring-red-100";
  return "bg-slate-100 text-slate-600 ring-slate-200";
}

export function MailList({
  documents,
  selectedDocumentId,
  searchValue,
  onSelectDocument,
  onDeleteDocument,
}: MailListProps) {
  return (
    <section className="flex w-[420px] min-w-[320px] max-w-[440px] flex-col border-r border-slate-200 bg-white lg:w-[420px]">
      <div className="border-b border-slate-200 px-5 py-4">
        <div className="flex items-center justify-between gap-3">
          <div>
            <h2 className="text-xl font-bold text-slate-950">Inbox</h2>
            <p className="mt-1 text-sm text-slate-500">
              {documents.length} document{documents.length === 1 ? "" : "s"}
            </p>
          </div>

          <div className="rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700">
            AI routed
          </div>
        </div>
      </div>

      {documents.length === 0 ? (
        <div className="flex flex-1 items-center justify-center p-8">
          <div className="text-center">
            <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-3xl bg-slate-50">
              <FileText className="text-slate-300" size={40} />
            </div>
            <p className="mt-4 font-semibold text-slate-800">No documents found</p>
            <p className="mt-1 text-sm text-slate-500">
              {searchValue ? "Try changing your search." : "Routed documents will appear here."}
            </p>
          </div>
        </div>
      ) : (
        <div className="min-h-0 flex-1 overflow-y-auto p-2">
          {documents.map((document) => {
            const isSelected = selectedDocumentId === document.id;

            return (
              <button
                key={document.id}
                onClick={() => onSelectDocument(document)}
                className={`group mb-2 w-full rounded-2xl border px-4 py-4 text-left transition-all duration-200 ease-out hover:-translate-y-0.5 hover:shadow-md ${
                  isSelected
                    ? "border-blue-100 bg-blue-50 shadow-sm ring-1 ring-blue-100"
                    : "border-transparent bg-white hover:border-slate-200 hover:bg-slate-50"
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="truncate text-sm font-semibold text-slate-900">
                      AI Document Router
                    </p>
                    <p className="mt-1 truncate text-sm font-medium text-slate-700">
                      {document.original_filename}
                    </p>
                  </div>

                  <div className="flex shrink-0 items-center gap-2">
                    <span
                      className={`rounded-full px-2.5 py-1 text-[11px] font-semibold ring-1 ${getStatusStyle(
                        document.status
                      )}`}
                    >
                      {document.status}
                    </span>

                    {onDeleteDocument && (
                      <span
                        role="button"
                        tabIndex={0}
                        title="Move to deleted"
                        onClick={(event) => {
                          event.stopPropagation();
                          onDeleteDocument(document);
                        }}
                        onKeyDown={(event) => {
                          if (event.key === "Enter" || event.key === " ") {
                            event.stopPropagation();
                            onDeleteDocument(document);
                          }
                        }}
                        className="rounded-xl p-2 text-slate-300 opacity-0 transition-all duration-200 hover:bg-red-50 hover:text-red-600 group-hover:opacity-100"
                      >
                        <Trash2 size={16} />
                      </span>
                    )}
                  </div>
                </div>

                <p className="mt-3 line-clamp-2 text-sm leading-6 text-slate-500">
                  Classified as{" "}
                  <span className="font-semibold text-slate-700">
                    {document.predicted_label ?? "unknown"}
                  </span>{" "}
                  with {formatConfidence(document.confidence_score)}.
                </p>

                {document.confidence_score !== null && (
                  <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-slate-100">
                    <div
                      className="h-full rounded-full bg-blue-600 transition-all duration-500"
                      style={{
                        width: `${Math.min(100, Math.max(0, document.confidence_score * 100))}%`,
                      }}
                    />
                  </div>
                )}

                <div className="mt-3 flex items-center justify-between text-xs text-slate-400">
                  <span>{new Date(document.created_at).toLocaleString()}</span>
                  <span>{(document.file_size / 1024).toFixed(1)} KB</span>
                </div>
              </button>
            );
          })}
        </div>
      )}
    </section>
  );
}