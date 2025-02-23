from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_userlist_keyboard(action: str, users: list[str]) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    
    for user in users:
        kb_builder.row(InlineKeyboardButton(text=user, callback_data=f"{action}:{user}"))
    
    return kb_builder.as_markup()