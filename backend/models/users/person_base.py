from pydantic import BaseModel


class PersonBase(BaseModel):
    """Базовая модель юзера."""

    login: str
    """Логин пользователя."""

    password: str
    """Пароль пользователя."""
