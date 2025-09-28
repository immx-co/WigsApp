from uuid import uuid4

from schemas.base import Base
from sqlalchemy import Column, DateTime, Numeric, String
from sqlalchemy.sql import func

try:
    from sqlalchemy.dialects.postgresql import JSONB, UUID

    UUID_TYPE = UUID(as_uuid=False)
    JSON_TYPE = JSONB
except Exception:
    from sqlalchemy import JSON

    UUID_TYPE = String
    JSON_TYPE = JSON


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(UUID_TYPE, primary_key=True, default=lambda: str(uuid4()))
    user_login = Column(String, nullable=False)
    items = Column(JSON_TYPE, nullable=False)
    total = Column(Numeric(12, 2), nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
