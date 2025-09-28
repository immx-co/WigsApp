from pydantic import BaseModel, Field


class OrderItemIn(BaseModel):
    """Модель описания товара в корзине."""

    id: str
    """goods_id товара"""

    qty: int = Field(..., gt=0)
    """Количество товара."""
