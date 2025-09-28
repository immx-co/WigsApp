from pydantic import BaseModel

class OrderItemOut(BaseModel):
    """Полная модель описания товара в корзине с их количеством."""

    id: str
    """Идентификатор товара."""

    title: str
    """Название товара."""

    price: float
    """Цена товара."""

    quantity: int
    """Количество товара."""

    line_total: float
    """Цена определенных товаров в корзине."""