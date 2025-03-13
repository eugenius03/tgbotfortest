from sqlalchemy import Integer, BigInteger,text
from db.engine import Base 
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated
import datetime

bigpk = Annotated[int, mapped_column(BigInteger,primary_key=True)]
bigint = Annotated[int, mapped_column(BigInteger)]


class OrderOrm(Base):
    __tablename__ = "order"

    order_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[bigint]
    product: Mapped[str]
    total: Mapped[int]
    status: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"),onupdate=lambda: datetime.datetime.now())










