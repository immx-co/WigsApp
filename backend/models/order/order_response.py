from pydantic import BaseModel

from models.order.order_item_out import OrderItemOut


class OrderResponse(BaseModel):
    """Модель сводки оформленных товаров."""

    items: list[OrderItemOut]
    """Список оформленных товаров."""

    total: float
    """Полная стоимость заказа."""