from pathlib import Path

import clamd

from inbox_shared.config.securitySettings import securitySettings
from inbox_shared.exceptions import (
    MalwareDetectedException,
    SecurityScanException,
)


class SecurityScanService:
    def __init__(self) -> None:
        self.enabled = securitySettings.clamavEnabled

    def scanFile(self, filePath: str) -> None:
        if not self.enabled:
            return

        path = Path(filePath)

        if not path.exists():
            raise SecurityScanException(
                f"Cannot scan missing file: {filePath}"
            )

        try:
            client = clamd.ClamdNetworkSocket(
                host=securitySettings.clamavHost,
                port=securitySettings.clamavPort,
            )

            client.ping()

            with open(path, "rb") as file:
                result = client.instream(file)

            print(f"Raw ClamAV result: {result}")

        except Exception as exception:
            raise SecurityScanException(
                "Security scan service is unavailable."
            ) from exception

        if not result:
            return

        scanStatus = next(iter(result.values()))

        print(f"Parsed ClamAV status: {scanStatus}")

        status, signature = scanStatus

        if status == "FOUND":
            raise MalwareDetectedException(
                f"The uploaded file failed the security scan: {signature}."
            )

        if status != "OK":
            raise SecurityScanException(
                f"Unexpected antivirus scan result: {status}."
            )