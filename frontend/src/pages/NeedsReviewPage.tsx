import { useEffect, useState } from "react";

import { fetchNeedsReviewDocuments } from "../api/documentsApi";
import { DocumentTable } from "../components/DocumentTable";
import { Layout } from "../components/Layout";
import type { DocumentListItemResponse } from "../types/documents";

export function NeedsReviewPage() {
  const [documents, setDocuments] = useState<DocumentListItemResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  async function loadNeedsReviewDocuments() {
    try {
      const data = await fetchNeedsReviewDocuments();
      setDocuments(data);
    } catch {
      setErrorMessage("Could not load needs review documents.");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    loadNeedsReviewDocuments();
  }, []);

  return (
    <Layout>
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Needs Review</h1>
        <p className="mt-2 text-slate-500">
          Documents that require manual validation.
        </p>
      </div>

      <div className="mt-8">
        {isLoading && <p className="text-slate-600">Loading documents...</p>}

        {errorMessage && (
          <div className="rounded-xl bg-red-50 p-4 text-red-700">
            {errorMessage}
          </div>
        )}

        {!isLoading && !errorMessage && <DocumentTable documents={documents} />}
      </div>
    </Layout>
  );
}