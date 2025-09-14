from pydantic import BaseModel
from models.goods.category import Category


class GoodsBase(BaseModel):
    """Базовая модель описания товара."""

    id: str
    """Идентификатор товара."""

    title: str
    """Заголовок товара."""

    category: Category
    """Категория товара."""

    price: int
    """Цена товара."""

    image: str
    """Ссылка на фотографию товара."""

    description: str
    """Описание товара."""