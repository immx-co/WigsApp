from schemas.base import Base
from sqlalchemy import Column, Integer, String


class Goods(Base):
    __tablename__ = "goods"
    id = Column(Integer, primary_key=True, index=True)
    goods_id = Column(String)
    title = Column(String)
    category = Column(String)
    price = Column(Integer)
    image = Column(String)
    description = Column(String)