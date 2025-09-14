from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
import uvicorn
import db
from models.person_create import PersonCreate
from sqlalchemy.ext.asyncio import AsyncSession

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_db()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.post("/people/")
async def create_person(person: PersonCreate, session: AsyncSession = Depends(db.get_db)):
    new_person = db.Person(name=person.name, age=person.age)
    session.add(new_person)
    await session.commit()
    await session.refresh(new_person)
    return new_person


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)