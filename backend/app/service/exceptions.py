class ServiceError(Exception):
    """Excepción base para errores de negocio o validación en la capa service."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ValidationError(ServiceError):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class NotFoundError(ServiceError):
    def __init__(self, message: str):
        super().__init__(message, status_code=404)


class ConflictError(ServiceError):
    def __init__(self, message: str):
        super().__init__(message, status_code=409)


class BusinessRuleError(ServiceError):
    """Excepción para incumplimiento de reglas de negocio (HTTP 422)."""

    def __init__(self, message: str = "La operación incumple una regla de negocio"):
        super().__init__(message, status_code=422)
