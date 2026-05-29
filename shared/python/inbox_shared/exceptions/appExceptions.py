class AppException(Exception):
    """Base exception for the application."""


class ValidationException(AppException):
    """Raised when business validation fails."""


class ResourceNotFoundException(AppException):
    """Raised when a requested resource does not exist."""


class AuthenticationException(AppException):
    """Raised when authentication fails."""


class AuthorizationException(AppException):
    """Raised when user is not allowed to perform an action."""


class ConflictException(AppException):
    """Raised when a resource conflict occurs."""


class UnsupportedFileTypeException(ValidationException):
    """Raised when uploaded file type is not supported."""


class MissingFileException(ValidationException):
    """Raised when an expected uploaded file is missing."""


class StorageUploadException(AppException):
    """Raised when file upload to object storage fails."""


class StorageDownloadException(AppException):
    """Raised when file download from object storage fails."""


class DocumentFileException(AppException):
    """Raised when a document cannot be read or processed."""


class ExternalServiceException(AppException):
    """Raised when an external service call fails."""


class MessagePublishException(AppException):
    """Raised when publishing a queue message fails."""


class ModelArtifactException(AppException):
    """Raised when AI model artifacts are missing or invalid."""


class ModelInferenceException(AppException):
    """Raised when model inference fails."""