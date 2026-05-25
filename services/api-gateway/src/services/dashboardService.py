from sqlalchemy.orm import Session

from inbox_shared.enums import DepartmentType, DocumentStatus
from inbox_shared.repositories import DashboardRepository
from src.schemas.dashboard import DashboardSummaryResponse


class DashboardService:
    def __init__(self, dashboardRepository: DashboardRepository) -> None:
        self.dashboardRepository = dashboardRepository

    def getSummary(self, db: Session) -> DashboardSummaryResponse:
        return DashboardSummaryResponse(
            totalDocuments=self.dashboardRepository.countAllDocuments(db),
            unsortedDocuments=self.dashboardRepository.countDocumentsByStatus(
                db,
                DocumentStatus.UNSORTED,
            ),
            routedDocuments=self.dashboardRepository.countDocumentsByStatus(
                db,
                DocumentStatus.ROUTED,
            ),
            needsReviewDocuments=self.dashboardRepository.countDocumentsByStatus(
                db,
                DocumentStatus.NEEDS_REVIEW,
            ),
            reviewedDocuments=self.dashboardRepository.countDocumentsByStatus(
                db,
                DocumentStatus.REVIEWED,
            ),
            hrDocuments=self.dashboardRepository.countDocumentsByDepartment(
                db,
                DepartmentType.HR,
            ),
            financeDocuments=self.dashboardRepository.countDocumentsByDepartment(
                db,
                DepartmentType.FINANCE,
            ),
            legalDocuments=self.dashboardRepository.countDocumentsByDepartment(
                db,
                DepartmentType.LEGAL,
            ),
            averageConfidence=self.dashboardRepository.getAverageConfidence(db),
        )