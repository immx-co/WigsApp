from enum import StrEnum


class Category(StrEnum):
    """Модель, содержащая в себе все категории товаров."""

    FOR_OLD_MAN = "FOR_OLD_MAN"
    FOR_GRANNY = "FOR_GRANNY"
    FOR_CHILDREN = "FOR_CHILDREN"