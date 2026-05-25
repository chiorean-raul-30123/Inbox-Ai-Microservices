import { axiosClient } from "./axiosClient";
import type {
  DocumentListItemResponse,
  DocumentDownloadUrlResponse,
  BulkUploadResponse,
} from "../types/documents";

export async function uploadDocument(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await axiosClient.post("/documents/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
}

export async function uploadBulkDocuments(files: File[]) {
  const formData = new FormData();

  files.forEach((file) => {
    formData.append("files", file);
  });

  const response = await axiosClient.post<BulkUploadResponse>(
    "/documents/upload-bulk",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
}

export async function fetchHrInbox() {
  const response = await axiosClient.get<DocumentListItemResponse[]>(
    "/documents/inbox/hr"
  );

  return response.data;
}

export async function fetchFinanceInbox() {
  const response = await axiosClient.get<DocumentListItemResponse[]>(
    "/documents/inbox/finance"
  );

  return response.data;
}

export async function fetchLegalInbox() {
  const response = await axiosClient.get<DocumentListItemResponse[]>(
    "/documents/inbox/legal"
  );

  return response.data;
}

export async function fetchNeedsReviewDocuments() {
  const response = await axiosClient.get<DocumentListItemResponse[]>(
    "/documents/inbox/needs-review"
  );

  return response.data;
}

export async function fetchDocumentDownloadUrl(documentId: string) {
  const response = await axiosClient.get<DocumentDownloadUrlResponse>(
    `/documents/${documentId}/download-url`
  );

  return response.data;
}

export async function moveDocumentToDeleted(documentId: string) {
  const response = await axiosClient.post(`/documents/${documentId}/delete`);
  return response.data;
}

export async function fetchDeletedDocuments() {
  const response = await axiosClient.get<DocumentListItemResponse[]>(
    "/documents/deleted"
  );

  return response.data;
}

export async function uploadScannedDocument(file: File, submittedBy?: string) {
  const formData = new FormData();

  formData.append("file", file);

  if (submittedBy) {
    formData.append("submittedBy", submittedBy);
  }

  const response = await axiosClient.post("/scan/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
}