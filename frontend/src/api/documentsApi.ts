import { axiosClient } from "./axiosClient";
import type {
  DocumentListItemResponse,
  DocumentDownloadUrlResponse,
  BulkUploadResponse,
} from "../types/documents";

export type UploadDocumentMetadata = {
  senderEmail?: string;
  senderName?: string;
  subject?: string;
  body?: string;
};

export async function uploadDocument(
  file: File,
  metadata?: UploadDocumentMetadata
) {
  const formData = new FormData();

  formData.append("file", file);

  if (metadata?.senderEmail) {
    formData.append("senderEmail", metadata.senderEmail);
  }

  if (metadata?.senderName) {
    formData.append("senderName", metadata.senderName);
  }

  if (metadata?.subject) {
    formData.append("subject", metadata.subject);
  }

  if (metadata?.body) {
    formData.append("body", metadata.body);
  }

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

export type ScanUploadMetadata = {
  senderEmail?: string;
  senderName?: string;
  subject?: string;
  body?: string;
};

export async function uploadScannedDocument(
  file: File,
  metadata?: ScanUploadMetadata
) {
  const formData = new FormData();

  formData.append("file", file);

  if (metadata?.senderEmail) {
    formData.append("senderEmail", metadata.senderEmail);
  }

  if (metadata?.senderName) {
    formData.append("senderName", metadata.senderName);
  }

  if (metadata?.subject) {
    formData.append("subject", metadata.subject);
  }

  if (metadata?.body) {
    formData.append("body", metadata.body);
  }

  const response = await axiosClient.post(
    "/scan/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
}


export async function simulateIncomingEmail(request: {
  senderEmail: string;
  senderName?: string;
  subject: string;
  body?: string;
  attachments: File[];
}) {
  const formData = new FormData();

  formData.append("senderEmail", request.senderEmail);
  formData.append("subject", request.subject);

  if (request.senderName) {
    formData.append("senderName", request.senderName);
  }

  if (request.body) {
    formData.append("body", request.body);
  }

  request.attachments.forEach((file) => {
    formData.append("attachments", file);
  });

  const response = await axiosClient.post("/emails/simulate", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
}