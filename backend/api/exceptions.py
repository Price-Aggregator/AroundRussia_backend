class ServiceError(Exception):
    """Внутренние ошибки сервиса."""
    pass


class InvalidDateError(Exception):
    """В запросе указана некорректная дата."""
    pass


class EmptyResponseError(Exception):
    """Сервер вернул пустой ответ."""
    pass
