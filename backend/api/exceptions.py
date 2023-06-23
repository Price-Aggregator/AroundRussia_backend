class ServiceError(Exception):
    """Внутренние ошибки сервиса."""
    pass


class InvalidDate(Exception):
    """В запросе указана некорректная дата."""
    pass


class EmptyResponse(Exception):
    """Сервер вернул пустой ответ."""
    pass
