from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import sessionmaker

from db.models import Transaction


async def create_transaction(user_to, user_from, amount: float, session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            transaction = Transaction(
                user_to=user_to,
                user_from=user_from,
                amount=amount
            )

            try:
                session.add(transaction)
            except ProgrammingError as e:
                pass

