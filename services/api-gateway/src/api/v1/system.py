import socket
import time

import httpx
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from inbox_shared.database import getDb
from inbox_shared.config.storageSettings import storageSettings
from inbox_shared.config.securitySettings import securitySettings

from src.api.v1.dashboard import getDashboardService


router = APIRouter(
    prefix="/system",
    tags=["System"],
)
def checkHttpService(name: str, url: str):
    started = time.time()

    try:
        response = httpx.get(
            url,
            timeout=2.0,
        )

        latency = round((time.time() - started) * 1000)

        return {
            "name": name,
            "status": "UP" if response.status_code == 200 else "DOWN",
            "latencyMs": latency,
        }

    except Exception:
        return {
            "name": name,
            "status": "DOWN",
            "latencyMs": None,
        }


def checkTcpService(
    name: str,
    host: str,
    port: int,
):
    try:
        socket.create_connection(
            (host, port),
            timeout=2,
        ).close()

        return {
            "name": name,
            "status": "UP",
        }

    except Exception:
        return {
            "name": name,
            "status": "DOWN",
        }
    
@router.get("/overview")
def getSystemOverview(
    db: Session = Depends(getDb),
):
    dashboardService = getDashboardService()

    services = [
        checkHttpService(
            "API Gateway",
            "http://localhost:8100/health",
        ),
        checkHttpService(
            "Upload Input",
            "http://localhost:8101/health",
        ),
        checkHttpService(
            "Email Input",
            "http://localhost:8102/health",
        ),
        checkHttpService(
            "Scan Input",
            "http://localhost:8103/health",
        ),
    ]

    infrastructure = [
        checkTcpService(
            "PostgreSQL",
            "localhost",
            5433,
        ),
        checkTcpService(
            "RabbitMQ",
            "localhost",
            5672,
        ),
        checkTcpService(
            "MinIO",
            "localhost",
            9002,
        ),
        checkTcpService(
            "ClamAV",
            securitySettings.clamavHost,
            securitySettings.clamavPort,
        ),
    ]

    summary = dashboardService.getSummary(db)

    return {
        "services": services,
        "infrastructure": infrastructure,
        "summary": summary,
        "lastUpdated": int(time.time()),
    }