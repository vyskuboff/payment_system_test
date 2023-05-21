from sqlalchemy import select, update
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker

from db.models import User


async def get_user(user_id: int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(select(User).where(User.user_id == user_id))
            return sql_res.scalars().one_or_none()


async def get_users(specialist_type: str, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(User).
                                           where(User.specialist_type == specialist_type and User.is_muted == False))
            return result.scalars().all()


async def create_user(user_id: int, username: str, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            user = User(
                user_id=user_id,
                username=username,
                balance=0
            )
            try:
                session.add(user)
            except ProgrammingError as e:
                pass


async def is_user_exists(user_id: int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(select(User).where(User.user_id == user_id))
            return sql_res.scalars().one_or_none()


async def get_user_by(session_maker: sessionmaker, **kwargs):
    async with session_maker() as session:
        async with session.begin():
            sql_res = await session.execute(select(User).filter_by(**kwargs))
            return sql_res.scalars().one_or_none()


async def update_user(user_id, session_maker: sessionmaker, **kwargs):
    async with session_maker() as session:
        query = (
            update(User)
                .where(User.user_id == user_id)
                .values(**kwargs)
                .execution_options(synchronize_session="fetch")
        )

        await session.execute(query)
        await session.commit()
