import type { DocumentListItemResponse } from "../types/documents";

type DocumentTableProps = {
  documents: DocumentListItemResponse[];
};

export function DocumentTable({ documents }: DocumentTableProps) {
  if (documents.length === 0) {
    return (
      <div className="rounded-2xl bg-white p-6 text-slate-500 shadow-sm">
        No documents found.
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-2xl bg-white shadow-sm">
      <table className="w-full text-left text-sm">
        <thead className="border-b border-slate-200 bg-slate-50 text-slate-600">
          <tr>
            <th className="px-4 py-3">Filename</th>
            <th className="px-4 py-3">Status</th>
            <th className="px-4 py-3">Predicted</th>
            <th className="px-4 py-3">Final</th>
            <th className="px-4 py-3">Department</th>
            <th className="px-4 py-3">Confidence</th>
          </tr>
        </thead>

        <tbody>
          {documents.map((document) => (
            <tr key={document.id} className="border-b border-slate-100">
              <td className="px-4 py-3 font-medium text-slate-900">
                {document.original_filename}
              </td>
              <td className="px-4 py-3">{document.status}</td>
              <td className="px-4 py-3">{document.predicted_label ?? "-"}</td>
              <td className="px-4 py-3">{document.final_label ?? "-"}</td>
              <td className="px-4 py-3">{document.department ?? "-"}</td>
              <td className="px-4 py-3">
                {document.confidence_score === null
                  ? "-"
                  : `${(document.confidence_score * 100).toFixed(1)}%`}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}