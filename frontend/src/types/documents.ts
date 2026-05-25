export type DocumentStatus =
  | "UNSORTED"
  | "RECEIVED"
  | "QUEUED_FOR_PROCESSING"
  | "PROCESSING"
  | "PROCESSING_FAILED"
  | "CLASSIFIED"
  | "QUEUED_FOR_DISPATCH"
  | "ROUTED"
  | "NEEDS_REVIEW"
  | "DISPATCH_FAILED"
  | "REPROCESS_REQUESTED"
  | "REVIEWED"
  | "ARCHIVED"
  | "FAILED"
  | "DELETED";

export type DepartmentType = "HR" | "FINANCE" | "LEGAL" | "NEEDS_REVIEW";

export type DocumentLabel = "HR" | "FINANCE" | "LEGAL";

export type DocumentListItemResponse = {
  id: string;
  original_filename: string;
  mime_type: string;
  file_size: number;
  status: DocumentStatus;
  predicted_label: DocumentLabel | null;
  final_label: DocumentLabel | null;
  department: DepartmentType | null;
  confidence_score: number | null;
  created_at: string;
  updated_at: string;
};

export type DocumentDownloadUrlResponse = {
  downloadUrl: string;
};

export type BulkUploadItemResponse = {
  originalFilename: string;
  documentId?: string | null;
  status?: DocumentStatus | null;
  department?: DepartmentType | null;
  success: boolean;
  message: string;
};

export type BulkUploadResponse = {
  uploadedDocuments: BulkUploadItemResponse[];
  failedDocuments: BulkUploadItemResponse[];
};