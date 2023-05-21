from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from context import create_user, is_user_exists


class RegisterCheck(BaseMiddleware):

    def __init__(self):
        pass

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        session_maker = data['session_maker']
        if not await is_user_exists(user_id=event.from_user.id, session_maker=session_maker):
            await create_user(user_id=event.from_user.id,
                              username=event.from_user.username, session_maker=session_maker)
        return await handler(event, data)
