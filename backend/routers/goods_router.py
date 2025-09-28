import db
from fastapi import APIRouter, Depends, HTTPException, status
from models.goods.category import Category
from models.goods.goods_base import GoodsBase
from models.goods.goods_create import GoodsCreate
from schemas.goods.goods import Goods
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

goods_router = APIRouter(prefix="/goods", tags=["Goods"])


@goods_router.get("/all", response_model=list[GoodsBase])
async def get_all_goods(session: AsyncSession = Depends(db.get_db)) -> list[GoodsBase]:
    """Возвращает все товары из бд.

    Args:
        session (AsyncSession, optional): Сессия бд.

    Returns:
        list[GoodsBase]: Все имеющие в бд товары.
    """

    result = await session.execute(select(Goods))
    rows = result.scalars().all()

    return [
        GoodsBase(
            id=row.goods_id,
            title=row.title,
            category=row.category,
            price=row.price,
            image=row.image,
            description=row.description,
        )
        for row in rows
    ]


@goods_router.get(
    "/{goods_id}",
    response_model=GoodsBase,
    responses={404: {"description": "Goods not found."}},
)
async def get_goods_by_id(
    goods_id: str, session: AsyncSession = Depends(db.get_db)
) -> GoodsBase:
    """Возвращает товар по идентификатору товара.

    Args:
        goods_id (str): Идентификатор товара.
        session (AsyncSession, optional): Сессия бд.

    Raises:
        (HTTPException): Товар не найден (404)

    Returns:
        (GoodsBase): Найденный товар.
    """
    
    result = await session.execute(select(Goods).where(Goods.goods_id == goods_id))
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Goods not found."
        )

    try:
        category = Category(row.category)
    except Exception:
        category = row.category

    return GoodsBase(
        id=row.goods_id,
        title=row.title,
        category=category,
        price=row.price,
        image=row.image,
        description=row.description,
    )


@goods_router.post("/add", response_model=GoodsCreate)
async def create_goods(goods: GoodsCreate, session: AsyncSession = Depends(db.get_db)):
    """Добавляет товар в бд.

    Args:
        goods (GoodsCreate): Модель создания товара.
        session (AsyncSession, optional): Сессия бд.
    """

    new_goods = Goods(
        goods_id=goods.id,
        title=goods.title,
        category=goods.category.value,
        price=goods.price,
        image=goods.image,
        description=goods.description,
    )
    session.add(new_goods)
    await session.commit()
    await session.refresh(new_goods)
    return goods

@goods_router.get("/by_category/{category}", response_model=list[GoodsBase])
async def get_goods_by_category(
    category: Category, 
    session: AsyncSession = Depends(db.get_db)) -> list[GoodsBase]:
    
    result = await session.execute(select(Goods).where(Goods.category == category.value))
    goods_by_category = result.scalars().all()

    all_goods: list[GoodsBase] = []
    for goods in goods_by_category:
        all_goods.append(GoodsBase(
            id=goods.goods_id,
            category=Category(goods.category),
            description=goods.description,
            image=goods.image,
            price=goods.price,
            title=goods.title,
        ))
    return all_goods

@goods_router.get("/categories/full", response_model=list[str])
async def get_all_categories() -> list[str]:
    return [cat.value for cat in Category]