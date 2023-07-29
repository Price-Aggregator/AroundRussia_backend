from typing import Final

from django.utils.translation import gettext_lazy as _

URL_WITH_CITIES: Final[str] = (
    'https://api.travelpayouts.com/data/ru/cities.json?_gl=1'
    '*100i7ih*_ga*MTUzMTY3NDIzNi4xNjg1ODI4ODQx*_ga_1WLL0NEBEH'
    '*MTY4NjA2MDAyMi45LjAuMTY4NjA2MDAyMi42MC4wLjA.'
)
"""Ссылка содержащая список городов с их координатами и IATA кодами."""

URL_CALENDAR: Final[str] = (
    'https://api.travelpayouts.com/aviasales/v3/grouped_prices'
)
"""Ссылка содержащая сгруппированные цены для календаря."""

URL_SEARCH: Final[str] = (
    'https://api.travelpayouts.com/aviasales/v3/prices_for_dates'
)
"""Ссылка содержащая сгруппированные цены по датам."""

URL_AVIASALES: Final[str] = 'https://www.aviasales.ru'
"""Ссылка на сайт aviasales.ru."""

COUNT_TICKET: Final[int] = 1000
"""Количество билетов в ответе."""

CACHE_TTL: Final[int] = 60
"""Время в течении которого кэш валиден (в секундах).
   Для тестирования указана 1 минута. 12 часов = 43200."""

MONTH_SLICE: Final[int] = 7
"""Индекс для среза строки даты, возвращает подстроку в формате YYYY-MM."""

WEEK: Final[int] = 7
"""Количество дней в неделе."""

PERIOD_MAX: Final[int] = 30
"""Максимально допустимая разница между датой вылета и возврата."""

PERIOD: Final[int] = 15
"""Количество дней за которые будут возвращаться цены."""

PERIOD_SLICE: Final[int] = 8
"""Количество дней до/после запрашиваемой даты включительно."""

BLOCK_CITY: Final[set[str]] = {'AAQ', 'EGO', 'BZK', 'VOZ', 'GDZ', 'KRR',
                               'URS', 'LPK', 'ROV', 'ESL', 'SIP'}
"""Города закрытые из-за СВО."""

CATEGORIES: Final[set[str]] = {'activity', 'flight', 'hotel'}
"""Допустимые категории активностей."""

MAX_IMAGES_PER_TRAVEL: Final[int] = 20
"""Максимальное количество изображений для одного путешествия."""

MEDIA_FORMATS: Final[tuple[str]] = ('jpeg', 'jpg', 'png', 'svg')
"""Разрешенные медиа-форматы."""

FILE_FORMATS: Final[set[str]] = ('pdf')
"""Разрешенные форматы файлов."""


class CustomMessages:
    INVALID_CREDENTIALS_ERROR = _('Не получается войти с предоставленными '
                                  'данными.')
    INACTIVE_ACCOUNT_ERROR = _("Аккаунт пользователя неактивен.")
    INVALID_TOKEN_ERROR = _("Неправильный токен.")
    INVALID_UID_ERROR = _("Пользователь не найден.")
    STALE_TOKEN_ERROR = _("Токен устарел.")
    PASSWORD_MISMATCH_ERROR = _("Поля паролей не совпадают.")
    USERNAME_MISMATCH_ERROR = _("Два поля {0} не совпадают.")
    INVALID_PASSWORD_ERROR = _("Неправильный пароль.")
    EMAIL_NOT_FOUND = _("Не найден пользователь с указанной почтой.")
    CANNOT_CREATE_USER_ERROR = _("Невозможно создать аккаунт.")
