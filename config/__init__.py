from sqlalchemy.engine import URL
import logging

postgres_url = URL.create(
    "postgresql+asyncpg",
    username='postgres',
    host='localhost',
    database='pay0pay_bot',
    port=5432,
    password='postgres'
)

telegram_token = 'Указать здесь токен'

LIMIT = 100


logger = logging.getLogger(__name__)
