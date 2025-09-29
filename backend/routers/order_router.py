import db
from fastapi import APIRouter, Depends, HTTPException, status
from models.order.order_create import OrderCreate
from models.order.order_item_out import OrderItemOut
from models.order.order_response import OrderResponse
from schemas.goods.goods import Goods
from schemas.orders.order import Order
from schemas.users.person import Person
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

order_router = APIRouter(prefix="/order", tags=["Orders"])


@order_router.get(
    "/{user_login}",
    response_model=list[OrderResponse],
    responses={"404": {"description": "User not found."}},
)
async def get_orders_by_user(
    user_login: str, session: AsyncSession = Depends(db.get_db)
) -> list[OrderResponse]:
    """Возвращает заказы конкретного юзера.

    Args:
        user_login (str): Имя пользователя.
        session (AsyncSession, optional): Сессия дб.

    Raises:
        HTTPException_404: Пользователь не найден.

    Returns:
        response (list[OrderResponse]): Заказы конкретного юзера.
    """
    query_user = await session.execute(select(Person).where(Person.login == user_login))
    user = query_user.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    result = await session.execute(
        select(Order)
        .where(Order.user_login == user_login)
        .order_by(Order.created_at.desc())
    )
    rows = result.scalars().all()

    response: list[OrderResponse] = []
    for row in rows:
        response.append(
            OrderResponse(
                order_id=str(row.order_id),
                created_at=row.created_at,
                items=row.items,
                total=float(row.total),
            )
        )

    return response


@order_router.post(
    "/place",
    response_model=OrderResponse,
    responses={
        400: {"description": "Bad request"},
        404: {"description": "Goods not found"},
    },
)
async def place_order(
    payload: OrderCreate, session: AsyncSession = Depends(db.get_db)
) -> OrderResponse:
    """Принимает товары из корзины, проверяет их наличие и возвращает сводку заказа."""
    if not payload.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Items list is empty."
        )

    query_user = await session.execute(select(Person).where(Person.is_active.is_(True)))
    active_user = query_user.scalar_one_or_none()
    if not active_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to place an order, you need to login.",
        )

    ids = [i.id for i in payload.items]
    result = await session.execute(select(Goods).where(Goods.goods_id.in_(ids)))
    rows = result.scalars().all()
    found: dict[str, Goods] = {row.goods_id: row for row in rows}

    missing = [i.id for i in payload.items if i.id not in found]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Goods not found: {', '.join(missing)}",
        )

    out_items: list[OrderItemOut] = []
    total = 0.0
    for item in payload.items:
        goods = found[item.id]
        price = float(goods.price)
        line_total = price * item.qty
        total += line_total
        out_items.append(
            OrderItemOut(
                id=goods.goods_id,
                title=goods.title,
                price=price,
                quantity=item.qty,
                line_total=line_total,
            )
        )

    order_row = Order(
        user_login=active_user.login,
        items=[item.model_dump() for item in out_items],
        total=round(total, 2),
    )
    session.add(order_row)
    await session.commit()

    return OrderResponse(items=out_items, total=total)
