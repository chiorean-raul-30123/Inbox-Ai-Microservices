import httpx

from fastapi import APIRouter


router = APIRouter(
    prefix="/system",
    tags=["System Health"],
)


services = [
    {
        "name": "API Gateway",
        "url": "http://localhost:8100/health",
    },
    {
        "name": "Upload Input Service",
        "url": "http://localhost:8101/health",
    },
    {
        "name": "Email Input Service",
        "url": "http://localhost:8102/health",
    },
    {
        "name": "Scan Input Service",
        "url": "http://localhost:8103/health",
    },
]


@router.get("/health")
def getSystemHealth():
    result = []

    for service in services:
        try:
            response = httpx.get(
                service["url"],
                timeout=2.0,
            )

            result.append(
                {
                    "name": service["name"],
                    "status": "UP" if response.status_code == 200 else "DOWN",
                }
            )

        except Exception:
            result.append(
                {
                    "name": service["name"],
                    "status": "DOWN",
                }
            )

    return {
        "services": result,
    }