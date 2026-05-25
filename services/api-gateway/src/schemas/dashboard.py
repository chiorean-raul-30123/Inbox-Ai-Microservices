from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    totalDocuments: int
    unsortedDocuments: int
    routedDocuments: int
    needsReviewDocuments: int
    reviewedDocuments: int

    hrDocuments: int
    financeDocuments: int
    legalDocuments: int

    averageConfidence: float | None