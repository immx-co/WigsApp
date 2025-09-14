from pydantic import BaseModel
from datetime import datetime
from models.goods.goods_base import GoodsBase


class OrderBase(BaseModel):
    """Базовая модель описания заказа."""

    items: list[GoodsBase]
    """Товары, добавленные в корзину."""

    is_completed: bool
    """Оформлен ли товар."""

    timestamp: datetime = datetime.now()
    """Время оформления заказа."""
