import db
from fastapi import APIRouter, Depends, HTTPException, status
from hasher.passlib_hasher import hash_password
from hasher.verify_password import verify_password
from models.users.person_create import PersonCreate
from models.users.person_verify import PersonVerify
from schemas.person import Person
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

user_router = APIRouter(prefix="/person", tags=["Users"])


@user_router.post("/add", response_model=PersonCreate)
async def create_person(
    person: PersonCreate, session: AsyncSession = Depends(db.get_db)
) -> Person:
    """Добавляет юзера в бд при регистрации.

    Args:
        person (PersonCreate): Модель юзера.
        session (AsyncSession, optional): Сессия бд.

    Returns:
        Person: Созданный юзер.
    """

    hashed = hash_password(person.password)

    new_person = Person(login=person.login, password=hashed)
    session.add(new_person)
    await session.commit()
    await session.refresh(new_person)
    return new_person


@user_router.post(
    "/verify",
    response_model=bool,
    responses={
        401: {"description": "Incorrect password."},
        404: {"description": "User not found."},
    },
)
async def verify_person(
    payload: PersonVerify, session: AsyncSession = Depends(db.get_db)
) -> bool:
    """Возвращает True, если пользователь существует и пароль совпадает, иначе False.

    Args:
        payload (PersonVerify): Модель верификации юзера.
        session (AsyncSession, optional): Сессия бд.

    Returns:
        bool: Существует ли пользователь и совпадает ли пароль.
    """

    result = await session.execute(select(Person).where(Person.login == payload.login))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    if not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password."
        )

    return True
