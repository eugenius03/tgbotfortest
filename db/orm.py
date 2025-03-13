from sqlalchemy.exc import NoResultFound
from db.engine import async_engine, async_session, Base
from db.models import OrderOrm

class AsyncORM:

    @staticmethod
    async def create_order(user_id: int, product: str, total: int, status: str):
        async with async_session.begin() as session:
            order = OrderOrm(user_id=user_id, product=product, total=total, status=status)
            session.add(order)
            await session.commit()
            return order.order_id
        
    @staticmethod
    async def edit_status(order_id: int, status: str):
        async with async_session.begin() as session:
            order = await session.get(OrderOrm, order_id)
            if order is None:
                raise NoResultFound
            order.status = status
            await session.commit()
            return order