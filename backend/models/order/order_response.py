from datetime import datetime

from models.order.order_item_out import OrderItemOut
from pydantic import BaseModel


class OrderResponse(BaseModel):
    """Модель сводки оформленных товаров."""

    order_id: str
    """Идентификатор заказа."""

    created_at: datetime | None = None
    """Дата и время оформления заказа."""

    items: list[OrderItemOut]
    """Список оформленных товаров."""

    total: float
    """Полная стоимость заказа."""
