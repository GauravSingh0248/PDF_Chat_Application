class AppException(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code

        super().__init__(message)


class DocumentNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            code="DOCUMENT_NOT_FOUND",
            message="Document not found.",
            status_code=404,
        )


class DocumentNotReadyException(AppException):
    def __init__(self):
        super().__init__(
            code="DOCUMENT_NOT_READY",
            message="Document is not ready for chat.",
            status_code=409,
        )