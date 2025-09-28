from pydantic import BaseModel

from models.order.order_item_in import OrderItemIn


class OrderCreate(BaseModel):
    """Модель описания количества товаров в корзине."""

    items: list[OrderItemIn]
    """Список товаров в корзине."""