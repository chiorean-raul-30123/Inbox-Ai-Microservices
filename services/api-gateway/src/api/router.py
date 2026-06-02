from fastapi import APIRouter

from src.api.v1.auth import router as authRouter
from src.api.v1.dashboard import router as dashboardRouter
from src.api.v1.documents import router as documentsRouter
from src.api.v1.settings import router as settingsRouter
from src.api.v1.emails import router as emailsRouter
from src.api.v1.scan import router as scanRouter
from src.api.v1.user import router as userRouter
from src.api.v1.systemHealth import router as systemHealthRouter
from src.api.v1.system import router as systemRouter
from src.api.v1.audit import router as auditRouter
from src.api.v1.notifications import router as notificationsRouter


apiRouter = APIRouter()
apiRouter.include_router(authRouter)
apiRouter.include_router(documentsRouter)
apiRouter.include_router(dashboardRouter)
apiRouter.include_router(settingsRouter)
apiRouter.include_router(emailsRouter)
apiRouter.include_router(scanRouter)
apiRouter.include_router(userRouter)
apiRouter.include_router(systemHealthRouter)
apiRouter.include_router(systemRouter)
apiRouter.include_router(auditRouter)
apiRouter.include_router(notificationsRouter)