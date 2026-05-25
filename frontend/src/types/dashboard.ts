export type DashboardSummaryResponse = {
  totalDocuments: number;
  unsortedDocuments: number;
  routedDocuments: number;
  needsReviewDocuments: number;
  reviewedDocuments: number;
  hrDocuments: number;
  financeDocuments: number;
  legalDocuments: number;
  averageConfidence: number | null;
};