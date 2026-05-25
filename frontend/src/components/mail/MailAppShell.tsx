import { useEffect, useMemo, useState } from "react";
import { RefreshCw, Search } from "lucide-react";

import {
  moveDocumentToDeleted,
} from "../../api/documentsApi";
import type { DocumentListItemResponse } from "../../types/documents";
import { MailList } from "./MailList";
import { MailPreview } from "./MailPreview";
import { MailSidebar } from "./MailSidebar";
import { UserProfileMenu } from "../UserProfileMenu";

type MailAppShellProps = {
  title: string;
  departmentName: string;
  fetchDocuments: () => Promise<DocumentListItemResponse[]>;
  allowDelete?: boolean;
};

export function MailAppShell({
  title,
  departmentName,
  fetchDocuments,
  allowDelete = true,
}: MailAppShellProps) {
  const [documents, setDocuments] = useState<DocumentListItemResponse[]>([]);
  const [selectedDocument, setSelectedDocument] =
    useState<DocumentListItemResponse | null>(null);
  const [searchValue, setSearchValue] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  async function loadDocuments(isManualRefresh = false) {
    try {
      setErrorMessage("");

      if (isManualRefresh) {
        setIsRefreshing(true);
      } else {
        setIsLoading(true);
      }

      const data = await fetchDocuments();
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
      setErrorMessage(`Could not load ${title}.`);
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  }

  async function handleDeleteDocument(document: DocumentListItemResponse) {
    try {
      await moveDocumentToDeleted(document.id);

      setDocuments((current) => {
        const nextDocuments = current.filter((item) => item.id !== document.id);

        if (selectedDocument?.id === document.id) {
          setSelectedDocument(nextDocuments[0] ?? null);
        }

        return nextDocuments;
      });
    } catch {
      setErrorMessage("Could not move document to deleted.");
    }
  }

  useEffect(() => {
    loadDocuments();
  }, []);

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
        document.department?.toLowerCase().includes(value)
      );
    });
  }, [documents, searchValue]);

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#f3f6fb]">
        <div className="rounded-2xl bg-white px-8 py-6 shadow-sm">
          <p className="text-sm font-medium text-slate-600">Loading inbox...</p>
        </div>
      </div>
    );
  }

  if (errorMessage) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#f3f6fb]">
        <div className="rounded-2xl border border-red-100 bg-red-50 p-5 text-sm font-medium text-red-700">
          {errorMessage}
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen overflow-hidden bg-[#f3f6fb]">
      <MailSidebar activeSection="inbox" />

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-6">
          <div>
            <h1 className="text-lg font-bold text-slate-950">{title}</h1>
            <p className="text-sm text-slate-500">
              {departmentName} department mailbox
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
              onClick={() => loadDocuments(true)}
              className="flex h-10 items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 text-sm font-medium text-slate-700 hover:bg-slate-50"
            >
              <RefreshCw
                size={16}
                className={isRefreshing ? "animate-spin" : ""}
              />
              Refresh
            </button>

            <UserProfileMenu />
          </div>
        </header>

        <div className="flex min-h-0 flex-1">
          <MailList
            documents={filteredDocuments}
            selectedDocumentId={selectedDocument?.id ?? null}
            searchValue={searchValue}
            onSelectDocument={setSelectedDocument}
            onDeleteDocument={allowDelete ? handleDeleteDocument : undefined}
          />

          <MailPreview
            document={selectedDocument}
            departmentName={departmentName}
          />
        </div>
      </div>
    </div>
  );
}