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


class QuizNotFoundException(AppException):
    def __init__(self, quiz_id: str):
        super().__init__(
            code="QUIZ_NOT_FOUND",
            message=f"Quiz with id '{quiz_id}' not found",
            status_code=404,
        )


class InvalidQuizQuestionException(AppException):
    def __init__(self, question_id: int):
        super().__init__(
            code="INVALID_QUIZ_QUESTION",
            message=f"Invalid question id '{question_id}'",
            status_code=400,
        )


